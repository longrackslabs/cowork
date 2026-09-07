# SOP: Fewer Permission Prompts (Cross-Harness)

Analyzes session transcripts across Claude Code, Antigravity (`agy`), and Grok to identify frequently used read-only commands and MCP tools, then populates permission allowlists to minimize interactive prompts.

## Where Things Live

| Component | Location | Notes |
|---|---|---|
| Analyzer Script | `~/cowork/scripts/fewer-permission-prompts.py` | Python 3 script scanning transcripts and generating rules |
| Gemini Skill | `~/cowork/skills/gemini/fewer-permission-prompts/SKILL.md` | Skill wrapper for Antigravity |
| Claude Skill | `~/cowork/skills/claude/fewer-permission-prompts/SKILL.md` | Skill wrapper for Claude Code |
| Claude Config | `~/cowork/.claude/settings.local.json` | Project-level allowlist for Claude |
| Antigravity Config | `~/.gemini/antigravity-cli/settings.json` | Global CLI allowlist for Antigravity |

---

## Safety Criteria

1. **Only Safe, Read-Only Operations:**
   - Git queries: `git status`, `git log`, `git diff`, `git branch`, `git show`, `git blame`
   - GitHub inspection: `gh pr view`, `gh pr list`, `gh issue view`, `gh run view`
   - Filesystem read-only: `ls`, `cat`, `head`, `tail`, `wc`, `grep`, `find`, `which`, `file`, `du`, `df`
   - Process & Service checks: `ps`, `pgrep`, `systemctl status`, `journalctl`
   - Safe MCP tools: tools with `get`, `read`, `list`, `search`, or explicit read-only functions.
2. **Strictly Prohibited from Wildcards:**
   - Interpreters (`python *`, `node *`, `bash *`, `sh *`)
   - Package runners (`npx *`, `uvx *`, `bunx *`)
   - Build/test task runners with wildcards (`npm run *`, `make *`)

---

## Execution

### Run via Script
```bash
# Dry run (preview top candidates without writing)
~/cowork/scripts/fewer-permission-prompts.py --dry-run

# Update specific harness
~/cowork/scripts/fewer-permission-prompts.py --harness agy
~/cowork/scripts/fewer-permission-prompts.py --harness claude

# Update all detected harnesses
~/cowork/scripts/fewer-permission-prompts.py --harness all
```

### Run via Slash Command
- In Antigravity: `/fewer-permission-prompts`
- In Claude Code: `/fewer-permission-prompts`
