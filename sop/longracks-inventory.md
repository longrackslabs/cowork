# Longracks Labs Inventory Management

## Overview
This SOP automates inventory recounts for Longracks Labs' eBay nozzle business, syncing counts to Google Sheets and eBay. There are two nozzle generations:

- **Gen 1 (X1/P1)** — `/lr1 XYZ` — updates the spreadsheet AND pushes quantities to eBay, Gen 1 only.
- **Gen 2 (H2/P2S/X2D)** — `/lr2 XYZ` — updates the spreadsheet AND pushes quantities to eBay, Gen 2 only. (Previously spreadsheet-only while listings were unsettled — the old FAH023 duplicate is gone and all four Gen 2 SKUs now have real, settled item IDs as of 2026-08.)
- **Both generations at once** — `/lri` accept either 3 digits (Gen 1 only, same as `/lr1`) or 6 digits (first 3 = Gen 1, last 3 = Gen 2 — runs both recounts, e.g. `/lri 444111`). These are no longer plain aliases for `/lr1` — they're the combined-run commands.

**Active year: 2026** — the Inventory tab is inside "Longracks Labs 2026" (spreadsheet ID above) in gpeden Drive. This spreadsheet contains everything: inventory, financials, orders, taxes.

**Required MCP Servers:**
- `google-sheets` - For reading/writing inventory spreadsheet
- `ebay` - For updating eBay listing quantities via API

**Important:** Call MCP tools directly in the main session — do NOT route through subagents (Task tool), as MCP tools are not available to subagents.

## When to Use
Trigger this when the user:
- Uses `/lr1 X,Y,Z` or `/lr1 XYZ` — Gen 1 recount only
- Uses `/lr2 X,Y,Z` or `/lr2 XYZ` — Gen 2 recount only
- Uses `/lri` with 3 digits — Gen 1 recount only (same as `/lr1`)
- Uses `/lri` with 6 digits — Gen 1 + Gen 2 recount, both generations in one command
- Says "update inventory" followed by numbers
- Mentions stock counts or inventory

**The commands:**
- `/lr1 X,Y,Z` — Gen 1 recount, update stock and eBay quantities
- `/lr2 X,Y,Z` — Gen 2 recount, update stock and eBay quantities
- `/lri` — 3 digits = Gen 1 only; 6 digits (first 3 = Gen 1, last 3 = Gen 2) = both, run as two full passes

For restocking or logging a placed order, see `~/cowork/sop/bambu-nozzle-restock.md` — that's a separate workflow, not part of this SOP.

## Input Format
Counts can be given comma-separated (`6,2,5`) or as a bare digit string (`625`). Tray counts are always single digits, so a 3-digit string unambiguously maps to X,Y,Z in order — both forms mean the same thing.

For `/lri` specifically, a 6-digit string splits into two groups of 3: first 3 = Gen 1 (X,Y,Z), last 3 = Gen 2 (X,Y,Z). E.g. `444111` → Gen 1 = 4,4,4 and Gen 2 = 1,1,1.

## Product SKUs and Color Coding

### Gen 1 (X1/P1)
The inventory uses color-coded trays:
- **Red tray** = NZ-2MM (0.2mm Stainless Steel nozzles)
- **Yellow tray** = NZ-4MM (0.4mm Hardened Steel nozzles)
- **Blue tray** = NZ-6MM (0.6mm Hardened Steel nozzles)

Additional SKU:
- **NZ-BNDL-246** = Bundle pack (contains 0.2mm, 0.4mm, and 0.6mm)

### Gen 2 (H2/P2S/X2D)
- **NZ-2MM-FAH059** = 0.2mm Stainless Steel nozzle
- **NZ-4MM-FAH060** = 0.4mm Hardened Steel nozzle
- **NZ-6MM-FAH061** = 0.6mm Hardened Steel nozzle
- **NZ-BNDL-GEN2-246** = Bundle pack (contains 0.2mm, 0.4mm, and 0.6mm)

## eBay Item IDs
These are the eBay item IDs for each SKU (used for API calls):

**Gen 1:**
- NZ-2MM: 167382780779
- NZ-4MM: 167391459174
- NZ-6MM: 167415316825
- NZ-BNDL-246: 167415298121

**Gen 2:**
- NZ-2MM-FAH059: 168592306309
- NZ-4MM-FAH060: 168360624279
- NZ-6MM-FAH061: 168592321742
- NZ-BNDL-GEN2-246: 168592324431

## Workflow

### Step 1: Parse Input
Parse counts per the Input Format section above:
- X = 0.2mm SKU count
- Y = 0.4mm SKU count
- Z = 0.6mm SKU count

**Examples:**
- `/lr1 2,5,3` or `/lr1 253` → NZ-2MM=2, NZ-4MM=5, NZ-6MM=3, Bundle=2
- `/lr2 2,5,3` or `/lr2 253` → NZ-2MM-FAH059=2, NZ-4MM-FAH060=5, NZ-6MM-FAH061=3, Bundle=2

**Bundle calculation:** the bundle SKU is always the floor of the lowest individual SKU count — never round up. For counts of 2,5,3 → bundle = 2.

### Step 2: Spreadsheet Update
**Spreadsheet ID:** `1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys`
**Sheet Name:** `Inventory`

Every recount updates the "On Hand" column (column B) AND clears the "Ordered" column (column C) for the same rows — a recount already reflects whatever arrived, so there's no separate "received" step or trigger. Just always clear Ordered.

**Gen 1:**
- **NZ-2MM** (row 6) → On Hand B6, clear C6
- **NZ-4MM** (row 7) → On Hand B7, clear C7
- **NZ-6MM** (row 8) → On Hand B8, clear C8
- **NZ-BNDL-246** (row 9) → On Hand B9 = floor of the lowest individual count, clear C9

**Gen 2:**
- **NZ-2MM-FAH059** (row 10) → On Hand B10, clear C10
- **NZ-4MM-FAH060** (row 11) → On Hand B11, clear C11
- **NZ-6MM-FAH061** (row 12) → On Hand B12, clear C12
- **NZ-BNDL-GEN2-246** (row 13) → On Hand B13 = floor of the lowest individual count, clear C13

**Example MCP call (Gen 1, counts 2,5,3):**
```
google-sheets:batch_update_cells
  spreadsheet_id: 1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys
  sheet: Inventory
  ranges: {
    "B6:B9": [[2], [5], [3], [2]],       # 2mm, 4mm, 6mm, bundle
    "C6:C9": [[""], [""], [""], [""]]    # clear Ordered
  }
```

**Example MCP call (Gen 2, counts 2,5,3):**
```
google-sheets:batch_update_cells
  spreadsheet_id: 1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys
  sheet: Inventory
  ranges: {
    "B10:B13": [[2], [5], [3], [2]],     # 2mm, 4mm, 6mm, bundle
    "C10:C13": [[""], [""], [""], [""]]  # clear Ordered
  }
```

The spreadsheet auto-calculates Target +/- to show reorder needs.

### Step 3: eBay Listing Updates
Use the eBay MCP to update listing quantities directly via API — for whichever generation was recounted (Gen 1 for `/lr1`, Gen 2 for `/lr2`).

**Process:**
1. Use `ebay_revise_listing` to update each SKU's quantity
2. Update all four listings in parallel for efficiency

**Example MCP calls (Gen 1, counts 2,5,3):**
```
ebay_revise_listing
  itemId: 167382780779
  fields: {"Quantity": 2}  # NZ-2MM

ebay_revise_listing
  itemId: 167391459174
  fields: {"Quantity": 5}  # NZ-4MM

ebay_revise_listing
  itemId: 167415316825
  fields: {"Quantity": 3}  # NZ-6MM

ebay_revise_listing
  itemId: 167415298121
  fields: {"Quantity": 2}  # NZ-BNDL-246
```

**Example MCP calls (Gen 2, counts 2,5,3):**
```
ebay_revise_listing
  itemId: 168592306309
  fields: {"Quantity": 2}  # NZ-2MM-FAH059

ebay_revise_listing
  itemId: 168360624279
  fields: {"Quantity": 5}  # NZ-4MM-FAH060

ebay_revise_listing
  itemId: 168592321742
  fields: {"Quantity": 3}  # NZ-6MM-FAH061

ebay_revise_listing
  itemId: 168592324431
  fields: {"Quantity": 2}  # NZ-BNDL-GEN2-246
```

**Important notes:**
- Setting quantity to 0 marks the listing as "Out of stock"
- Setting quantity > 0 activates the listing automatically
- The API handles both restocking and marking out-of-stock seamlessly
- All updates happen instantly via API (no browser required)

### Step 4: Verification & Completion
After updates, verify by reading back the updated data:
```
google-sheets:get_sheet_data
  spreadsheet_id: 1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys
  sheet: Inventory
  range: A6:J9    # Gen 1
  range: A10:J13  # Gen 2
```

Then report:
- Spreadsheet updated (SKU=count for each of the four rows)
- Show the auto-calculated "Total" and "Target +/-" columns from the verification read
- Note eBay listings updated via API
- Any reorder needs based on Target +/-

### Step 5: Report Shortages (Don't Auto-Restock)
After completing the inventory update, mention any 🔴 Reorder shortages as an FYI — but do NOT auto-trigger the restock workflow. Restocking is a separate action George triggers manually (e.g., "restock" or "load the cart") when he has enough GC points built up.
