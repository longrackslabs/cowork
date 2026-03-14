---
name: lri
description: Recount Longracks Labs nozzle stock and sync to Google Sheets + eBay. Usage: /lri 0.2mm,0.4mm,0.6mm (e.g. /lri 2,5,3)
argument-hint: "X,Y,Z (0.2mm, 0.4mm, 0.6mm counts)"
---

Run the Longracks Labs inventory recount for counts: $ARGUMENTS

Follow the SOP at ~/cowork/sop/longracks-inventory.md exactly. This is the `inventory` command (recount only — do NOT clear the Ordered column).

Call MCP tools directly in this session. Do not use subagents.
