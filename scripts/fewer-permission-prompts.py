#!/usr/bin/env python3
"""
Portable Fewer Permission Prompts Analyzer & Generator.
Compatible with Claude Code, Antigravity (agy), and Grok.
"""

import os
import glob
import json
import re
import sys
import argparse
from collections import Counter

# Safe read-only prefixes and tools
SAFE_PREFIXES = {
    "git": ["status", "log", "diff", "show", "branch", "blame", "tag", "remote", "rev-parse", "describe", "stash list"],
    "gh": ["pr view", "pr list", "pr diff", "pr checks", "pr status", "issue view", "issue list", "run view", "run list", "release view", "release list", "auth status"],
    "systemctl": ["status", "is-active", "is-enabled"],
    "docker": ["ps", "images", "logs", "inspect"],
}

SAFE_EXACT = {
    "ls", "pwd", "whoami", "date", "uptime", "which", "file", "uname", "df", "du",
    "cat", "head", "tail", "wc", "grep", "rg", "find", "ps", "pgrep", "journalctl",
    "rclone", "agy", "strings"
}

BLOCKED_EXECUTABLES = {
    "python", "python3", "node", "bun", "deno", "ruby", "perl", "bash", "sh",
    "zsh", "eval", "exec", "ssh", "sudo", "npx", "bunx", "uvx", "uv", "make"
}

def scan_claude_transcripts(limit=50):
    files = sorted(glob.glob(os.path.expanduser("~/.claude/projects/**/*.jsonl"), recursive=True),
                    key=os.path.getmtime, reverse=True)[:limit]
    bash_cmds = Counter()
    mcp_tools = Counter()
    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if not line.strip(): continue
                    try:
                        data = json.loads(line)
                        msg = data.get("message", {})
                        for item in msg.get("content", []):
                            if isinstance(item, dict) and item.get("type") == "tool_use":
                                tname = item.get("name", "")
                                if tname == "Bash":
                                    cmd = item.get("input", {}).get("command", "").strip()
                                    if cmd: bash_cmds[cmd] += 1
                                elif tname.startswith("mcp__"):
                                    mcp_tools[tname] += 1
                    except Exception:
                        pass
        except Exception:
            pass
    return bash_cmds, mcp_tools

def scan_gemini_transcripts(limit=50):
    files = sorted(glob.glob(os.path.expanduser("~/.gemini/antigravity-cli/brain/*/.system_generated/logs/transcript*.jsonl")),
                    key=os.path.getmtime, reverse=True)[:limit]
    bash_cmds = Counter()
    mcp_tools = Counter()
    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "tool_calls" not in line: continue
                    try:
                        data = json.loads(line)
                        for tc in data.get("tool_calls", []):
                            name = tc.get("name", "")
                            args = tc.get("args", {})
                            if name in ("default_api:run_command", "run_command"):
                                cmd = args.get("CommandLine", "").strip()
                                if cmd: bash_cmds[cmd] += 1
                            elif name.startswith("mcp_") or name.startswith("default_api:mcp_"):
                                mcp_tools[name] += 1
                    except Exception:
                        pass
        except Exception:
            pass
    return bash_cmds, mcp_tools

def is_safe_command(cmd_str):
    tokens = cmd_str.split()
    if not tokens:
        return False, ""
    
    base = tokens[0].split("/")[-1]
    if base in BLOCKED_EXECUTABLES:
        return False, ""
    
    # Check compound prefixes like git, gh, systemctl
    if base in SAFE_PREFIXES and len(tokens) >= 2:
        sub = tokens[1]
        for allowed in SAFE_PREFIXES[base]:
            if allowed == sub or allowed.startswith(sub + " "):
                return True, f"{base} {allowed}"
    
    if base in SAFE_EXACT:
        return True, base
        
    return False, ""

def main():
    parser = argparse.ArgumentParser(description="Analyze transcripts and update permission allowlists.")
    parser.add_argument("--harness", choices=["claude", "gemini", "agy", "all"], default="all",
                        help="Target harness to update settings for.")
    parser.add_argument("--dry-run", action="store_true", help="Print table without modifying settings.")
    args = parser.parse_args()

    claude_bash, claude_mcp = scan_claude_transcripts()
    gemini_bash, gemini_mcp = scan_gemini_transcripts()

    all_bash = claude_bash + gemini_bash
    all_mcp = claude_mcp + gemini_mcp

    pattern_counts = Counter()
    for cmd, count in all_bash.items():
        safe, pattern = is_safe_command(cmd)
        if safe:
            pattern_counts[pattern] += count

    for tool, count in all_mcp.items():
        pattern_counts[tool] += count

    ranked = pattern_counts.most_common(25)

    print(f"\nPrioritized Allowlist Candidates (Scanned {len(all_bash)} bash + {len(all_mcp)} MCP unique calls):\n")
    print(f"| {'#':<2} | {'Pattern':<35} | {'Count':<5} |")
    print(f"|{'-'*4}|{'-'*37}|{'-'*7}|")
    for idx, (pat, cnt) in enumerate(ranked, 1):
        print(f"| {idx:<2} | {pat:<35} | {cnt:<5} |")
    print()

    if args.dry_run:
        print("Dry-run specified. No settings modified.")
        return

    # Update Claude settings if requested
    if args.harness in ("claude", "all"):
        claude_settings_path = os.path.expanduser("/home/gpeden/cowork/.claude/settings.local.json")
        if os.path.exists(claude_settings_path):
            try:
                with open(claude_settings_path, "r") as f:
                    cdata = json.load(f)
                allow_list = cdata.setdefault("permissions", {}).setdefault("allow", [])
                added = 0
                for pat, _ in ranked:
                    rule = f"Bash({pat} *)" if not pat.startswith("mcp__") else pat
                    if rule not in allow_list:
                        allow_list.append(rule)
                        added += 1
                with open(claude_settings_path, "w") as f:
                    json.dump(cdata, f, indent=2)
                print(f"Updated Claude settings ({claude_settings_path}): added {added} rules.")
            except Exception as e:
                print(f"Failed updating Claude settings: {e}", file=sys.stderr)

    # Update Gemini / Agy settings if requested
    if args.harness in ("gemini", "agy", "all"):
        agy_settings_path = os.path.expanduser("~/.gemini/antigravity-cli/settings.json")
        if os.path.exists(agy_settings_path):
            try:
                with open(agy_settings_path, "r") as f:
                    gdata = json.load(f)
                allow_list = gdata.setdefault("permissions", {}).setdefault("allow", [])
                added = 0
                for pat, _ in ranked:
                    if pat.startswith("mcp__"):
                        rule = pat.replace("mcp__", "mcp_")
                    else:
                        rule = f"command({pat} *)"
                    if rule not in allow_list:
                        allow_list.append(rule)
                        added += 1
                with open(agy_settings_path, "w") as f:
                    json.dump(gdata, f, indent=2)
                print(f"Updated Antigravity settings ({agy_settings_path}): added {added} rules.")
            except Exception as e:
                print(f"Failed updating Antigravity settings: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
