# Longracks Labs Inventory Management

## Overview
This SOP automates inventory management for Longracks Labs' eBay nozzle business. When George provides stock counts in chat, update the Google Sheets inventory tracker and restock eBay listings directly via the eBay MCP server.

**Active year: 2026** — the Inventory tab is inside "Longracks Labs 2026" (spreadsheet ID above) in gpeden Drive. This spreadsheet contains everything: inventory, financials, orders, taxes.

**Required MCP Servers:**
- `google-sheets` - For reading/writing inventory spreadsheet
- `ebay` - For updating eBay listing quantities via API

**Important:** Call MCP tools directly in the main session — do NOT route through subagents (Task tool), as MCP tools are not available to subagents.

## When to Use
Trigger this when the user:
- Uses the command "inventory X,Y,Z" (e.g., "inventory 2,5,3") — recount, no order expected
- Uses the command "received X,Y,Z" (e.g., "received 2,5,3") — stock arrived, clear Ordered column
- Says "update inventory" followed by three numbers
- Asks to update eBay listings
- Mentions stock counts or inventory

**The 4 commands:**
- `inventory X,Y,Z` — recount, update stock and eBay quantities
- `restock` — build the Bambu cart to replenish low stock
- `order` — record a placed order (sets Ordered column)
- `received X,Y,Z` — same as inventory (recount + eBay update), but triggered by inbound stock; also clears the Ordered column

## Product SKUs and Color Coding

The inventory uses color-coded trays:
- **Red tray** = NZ-2MM (0.2mm Stainless Steel nozzles)
- **Yellow tray** = NZ-4MM (0.4mm Hardened Steel nozzles)
- **Blue tray** = NZ-6MM (0.6mm Hardened Steel nozzles)

Additional SKU:
- **NZ-BNDL-246** = Bundle pack (contains 2mm, 4mm, and 6mm)

## eBay Item IDs
These are the eBay item IDs for each SKU (used for API calls):
- NZ-2MM: 167382780779
- NZ-4MM: 167391459174
- NZ-6MM: 167415316825
- NZ-BNDL-246: 167415298121

## Workflow

### Step 1: Parse Input
When user provides counts in format "X,Y,Z" (via any trigger):
- X = NZ-2MM (0.2mm red tray count)
- Y = NZ-4MM (0.4mm yellow tray count)
- Z = NZ-6MM (0.6mm blue tray count)

**Examples:**
- `inventory 2,5,3` means: NZ-2MM=2, NZ-4MM=5, NZ-6MM=3, Bundle=2
- "update longracks-inventory with 2,5,3" (same result)
- "update inventory 2,5,3" (same result)

**Bundle calculation:** NZ-BNDL-246 is always the floor of the lowest individual SKU count — never round up. For counts of 2,5,3 → bundle = 2.

### Step 2: Spreadsheet Update
**Spreadsheet ID:** `1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys`
**Sheet Name:** `Inventory`

Use the Google Sheets MCP tool to update the "On Hand" column (column B):
- **NZ-2MM** (row 6, cell B6) → red tray count
- **NZ-4MM** (row 7, cell B7) → yellow tray count
- **NZ-6MM** (row 8, cell B8) → blue tray count
- **NZ-BNDL-246** (row 9, cell B9) → floor of the lowest individual count

**Example MCP call:**
```
google-sheets:update_cells
  spreadsheet_id: 1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys
  sheet: Inventory
  range: B6:B9
  data: [[2], [5], [3], [2]]  # 2mm, 4mm, 6mm, bundle
```

**Bundle calculation:** NZ-BNDL-246 is always `floor(min(X,Y,Z))` — never round up.
- Example: counts of 2,5,3 → bundle = 2
- Example: counts of 3,6,2 → bundle = 2

The spreadsheet auto-calculates Target +/- to show reorder needs.

### Step 3: eBay Listing Updates
Use the eBay MCP to update listing quantities directly via API.

**Process:**
1. Use `ebay_revise_listing` to update each SKU's quantity
2. Update all four listings in parallel for efficiency

**Example MCP calls:**
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
  range: A6:J9
```

Then report:
- Spreadsheet updated (NZ-2MM=X, NZ-4MM=Y, NZ-6MM=Z, Bundle=MIN)
- Show the auto-calculated "Total" and "Target +/-" columns from the verification read
- eBay listings updated via API
- Any reorder needs based on Target +/-

### Step 5: Report Shortages (Don't Auto-Restock)
After completing the inventory update, mention any 🔴 Reorder shortages as an FYI — but do NOT auto-trigger the restock workflow. Restocking is a separate action George triggers manually (e.g., "restock" or "load the cart") when he has enough GC points built up.

### Step 6: Clear "Ordered" Column on Receiving
When the command is `received X,Y,Z` (not `inventory`), clear the Ordered column back to empty for all SKUs. The shipment has arrived — Ordered is no longer needed.
