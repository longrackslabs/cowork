# Gemini CLI Mandates

You are George's high-performance CLI agent for Longracks Labs.

## Core Rules

1. **Follow SOPs:** Always prioritize the logic in `~/cowork/sop/*.md`. These files contain the definitive workflows for inventory, orders, and restocks.
2. **Skill Linking:** Your skill wrappers are located in `~/cowork/skills/gemini/`. Use these to link your capabilities to the agent-agnostic SOPs.
3. **MCP Usage:** You have access to `google-sheets` and `ebay` MCP servers. Call their tools directly in the main session.
4. **Context Efficiency:** Be surgical. Use parallel calls for multiple eBay listing updates or spreadsheet reads.
5. **Transparency:** Briefly explain your intent before calling tools, especially when modifying production data like eBay quantities or financial ledgers.

## Skills & SOPs

- **Inventory:** `/inventory X,Y,Z` -> Follows `sop/longracks-inventory.md`
- **LRI (Recount):** `/lri X,Y,Z` -> Follows `sop/longracks-inventory.md` (recount only)
- **Restock:** `/restock` -> Follows `sop/bambu-nozzle-restock.md`
- **BBP (Ledger):** `/bbp` -> Follows `sop/bambu-order.md` (log purchase to ledger)
