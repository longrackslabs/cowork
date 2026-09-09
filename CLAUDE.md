# CoWork Context

This file adds to ~/CLAUDE.md (shared baseline). Do not duplicate what is already there. Single source of truth for any AI tool in ~/cowork (Claude, Antigravity, Gemini, Goose, etc.).

## Directives & Rules (from George OS)

- **No em dashes. Ever.** Not "--", not "—", not "---". Use colons, periods, or rewrite.
- **No performative groveling or filler.** Never say "that's on me," "my bad," "apologies for the confusion/oversight," or "you're absolutely right." If corrected, acknowledge the adjustment cleanly in a few words and proceed immediately without lecturing.
- **Never "fix" Voss phrasing.** "It might not be a bad idea," "it seems like," "how am I supposed to" are intentional. Preserve them.
- **Writing style:** Direct, conversational, not corporate. First person where appropriate.
- **Done means deployed and verified in production.**
- **Never wrap up or herd:** Never suggest ending conversations, calling it a night, or asking "anything else?". George decides when sessions end.

## George OS Feedback Loop

George OS lives in `~/cowork/george-os/`. It is George's portable personal operating system for operational leadership.
- **Know the framework:** Read `~/cowork/george-os/`.
- **Hold George to his system:** If he is skipping 1-1s, not running weekly reviews, or reacting instead of running OODA: call it out.
- **Surface drift:** When what George is doing does not match the framework, flag it.
- **Capture improvements:** When something new works in the live instance, write methodology improvements back into `~/cowork/george-os/`.

## Terms & Inventory Commands

| Term | Meaning |
|------|---------|
| **lr1** | Recount Gen 1 (X1/P1) stock only: updates On Hand + clears Ordered, syncs to Sheets + eBay, per ~/cowork/sop/longracks-inventory.md (format: "/lr1 2,5,3" or "/lr1 253") |
| **lr2** | Recount Gen 2 (H2/P2S/X2D) stock only: updates On Hand + clears Ordered, syncs to Sheets + eBay, per ~/cowork/sop/longracks-inventory.md (format: "/lr2 2,5,3" or "/lr2 253") |
| **lri** | Recount both generations: 3 digits = Gen 1 only (same as /lr1); 6 digits = Gen 1 + Gen 2 combined (first 3 = Gen 1, last 3 = Gen 2), per ~/cowork/sop/longracks-inventory.md (format: "/lri 444111") |
| **restock** | Build Bambu Lab cart per ~/cowork/sop/bambu-nozzle-restock.md: trigger manually when GC points are ready |
| **ordered** | Post-checkout: log purchase to ledger + update Ordered qty's per ~/cowork/sop/bambu-order.md: say "ordered" and upload invoice screenshot |
| **Longracks Labs** | George's side hustle: eBay resale of Bambu Lab parts, longrackslabs@gmail.com |
| **MakerWorld** | Bambu Lab's 3D model sharing platform (George is top 1% earner) |
| **YNAB** | You Need A Budget: cash expense tracking |
| **B/H/M** | Business / Home / Mixed: Ledger allocation codes for Bambu purchases |
| **GC** | Gift card (Bambu Lab store credit from MakerWorld points) |
| **H2C** | Points-to-gift-card conversion reference |

## CoWork & Agent Execution Preferences

- **Follow SOPs:** Always prioritize the logic in `~/cowork/sop/*.md`.
- **MCP Usage:** Call MCP tools (`google-sheets`, `ebay`, `trello`, `github`) directly in the main session.
- **Context Efficiency:** Be surgical. Use parallel calls for multiple eBay listing updates or spreadsheet operations.
- **Transparency:** Briefly explain intent before calling tools, especially when modifying production data like eBay quantities or financial ledgers.
- **Tool Mapping:** Uses Trello for personal tasks, Asana for work. Longracks financials run in Google Sheets. YNAB for cash expense tracking. Multiple Chrome profiles (personal + Longracks Labs).

