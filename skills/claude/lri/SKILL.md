---
name: lri
description: Recount Longracks Labs nozzle stock — Gen 1 only (3 digits) or Gen 1 + Gen 2 together (6 digits) — and sync to Google Sheets + eBay. Usage: /lri XYZ (Gen 1 only) or /lri XYZABC (Gen 1 + Gen 2, e.g. /lri 444111)
argument-hint: "XYZ (Gen 1 only) or XYZABC (Gen 1 + Gen 2)"
---

Run the Longracks Labs inventory recount for: $ARGUMENTS

Parse the digit string by length:
- **3 digits** (e.g. `253`) → Gen 1 only. Run the Gen 1 section of the SOP for these counts.
- **6 digits** (e.g. `444111`) → Gen 1 + Gen 2. The first 3 digits are Gen 1 counts, the last 3 are Gen 2 counts. Run the Gen 1 section for the first 3, then the Gen 2 section for the last 3 — two full passes (spreadsheet + eBay each) per the SOP.

Follow the SOP at ~/cowork/sop/longracks-inventory.md exactly. This is a recount — update On Hand and clear the Ordered column per Step 2 for each generation being updated. Push updated quantities to eBay per Step 3 for each generation being updated.

Call MCP tools directly in this session. Do not use subagents.
