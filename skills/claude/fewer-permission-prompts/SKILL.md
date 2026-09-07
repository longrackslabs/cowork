---
name: fewer-permission-prompts
description: Scan transcripts for common read-only commands and MCP tool calls, then add a prioritized allowlist to settings.json to reduce permission prompts.
---

Run the cross-harness permission analyzer and update Claude's allowlist.

Follow the SOP at ~/cowork/sop/fewer-permission-prompts.md.

Execute:
```bash
python3 ~/cowork/scripts/fewer-permission-prompts.py --harness claude
```
