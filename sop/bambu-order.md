# Bambu Purchase Entry

## Overview

This SOP extracts purchase data from Bambu Store order screenshots and appends properly formatted rows to the Ledger tab in the Longracks Labs Financials 2026 spreadsheet. It handles business/personal classification, calculates business percentages for mixed orders, and ensures formulas are correctly copied.

**Required MCP Servers:**
- `google-sheets` - For reading/writing to the Ledger spreadsheet

**Spreadsheet ID:** `1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys`
**Sheet Name:** `Ledger`

## When to Use

Trigger this when the user:
- Says "ordered" with a Bambu Store invoice screenshot
- Asks to log a Bambu purchase to the ledger
- Provides a Bambu Store invoice screenshot with notes about business/personal classification

## Workflow

### Step 1: Extract Data from Screenshot

The user will provide a screenshot of a Bambu Store invoice. Extract the following data:

**Required fields:**
- **Order Date**: From "Order Confirmed" line, format as M/D/YY (e.g., 2/5/26)
- **Order Number**: Alphanumeric string at top of invoice (e.g., `us695045967829590016`)
  - The user MUST include this in their screenshot. If it's not visible, ask them to provide a screenshot showing the order number.
- **Line Items**: All items with names, quantities, and prices
- **Grand Total**: The total amount before any gift card is applied (this becomes "Cart $")
- **Gift Card Amount**: If a gift card was applied, it shows as negative on the invoice. Record as positive number.
- **Net Payment**: The actual cash paid (Grand Total minus Gift Card)

### Step 2: Classify Items and Calculate Business Percentage

Determine whether this order is Business, Hobby (personal), or Mixed:

**Item Classification Rules:**
- **Business (B)**: Items purchased for resale on eBay
  - Nozzles, hotends, and most accessories → Usually business
- **Hobby/Personal (H)**: Items for personal use
  - PLA/filament → Usually personal (unless user states otherwise)
- **Mixed (M)**: Order contains both business and personal items

**When in doubt about an item's classification, ask the user.**

#### Use Column Logic:
- **B** = 100% business (Biz % = 1.0)
- **H** = 0% business (Biz % = 0)
- **M** = Mixed, requires calculating Biz %

#### Calculating Biz % for Mixed Orders:

```
Biz % = (Sum of business item prices) / (Grand Total)
```

**Example:**
- Grand Total: $98.34
- PLA filament: $19.99 (personal)
- Everything else: Business
- Biz % = (98.34 - 19.99) / 98.34 = 0.7968

**CRITICAL:** Enter Biz % as the decimal value like 0.7968 (which displays as 79.68%). The column has percentage formatting, so entering 79.68 will be interpreted as 7968% and display incorrectly.

### Step 3: Confirm Entry with User

Before writing to the spreadsheet, show the user a summary and wait for confirmation:

```
Ready to add this entry to the Ledger:
- Date: 2/5/26
- Order: us695045967829590016
- Cart $: 98.34
- GC $: 0
- Use: M (Mixed)
- Biz %: 0.7968 (79.68%)

Should I proceed?
```

Wait for user approval before continuing.

### Step 4: Write to Spreadsheet

**IMPORTANT:** Use the Google Sheets MCP tool to append the entry.

#### Finding the Next Empty Row:

First, read the Ledger sheet to find the next empty row:

```
google-sheets:get_sheet_data
  spreadsheet_id: 1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys
  sheet: Ledger
  range: A:A
```

Find the first empty cell in column A - that's your target row number.

#### Ledger Column Mapping:

| Col | Header | Manual/Formula | Notes |
|-----|--------|----------------|-------|
| A | Date | Manual | M/D/YY format |
| B | Type | Manual | Always "Purchase" (dropdown) |
| C | Order / Description | Manual | Bambu order number |
| D | Draw $ | Manual | Always 0 unless stated |
| E | Cart $ | Manual | Grand Total from invoice |
| F | GC $ | Manual | Gift card amount (positive) |
| G | Net $ | Formula | `=E-F` (already in blank rows) |
| H | Use | Manual | B, H, or M |
| I | Biz % | Manual | Percentage for M, blank for B/H |
| J | Biz % (Final) | Formula | `=IF($H="B",1,IF($H="H",0,IF($H="M",$I,)))` (already in blank rows) |
| K | Biz Cart $ | Formula | `=$E*$J` (already in blank rows) |
| L | Biz GC $ | Formula | `=$F*$J` (already in blank rows) |
| M | Biz Cash $ | Formula | (already in blank rows) |
| N | Check | Formula | (already in blank rows) |

#### Write Procedure:

Use `batch_update_cells` to write multiple ranges at once. For example, if row 50 is the next empty row:

```
google-sheets:batch_update_cells
  spreadsheet_id: 1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys
  sheet: Ledger
  ranges: {
    "A50": [["2/5/26"]],
    "B50": [["Purchase"]],
    "C50": [["us695045967829590016"]],
    "D50": [[0]],
    "E50": [[98.34]],
    "F50": [[0]],
    "H50": [["M"]],
    "I50": [[79.68]]
  }
```

**CRITICAL POINTS:**
- Enter Biz % as a decimal value like 0.7968 (which displays as 79.68%). The column has percentage formatting.
- Skip columns G, J-N - they already have formulas that will auto-calculate
- Date format: M/D/YY (e.g., 2/5/26)
- Type is always "Purchase"
- Draw $ is usually 0

### Step 5: Verify Entry

After writing, read back the row to confirm formulas calculated correctly:

```
google-sheets:get_sheet_data
  spreadsheet_id: 1ygVSLv8-GSTVSKRcYvScowc-pE98DWhZyCuAIIAyVys
  sheet: Ledger
  range: A50:N50  # Use the actual row number
```

Verify the calculated values:
- **Net $** (column G): should equal Cart $ - GC $
- **Biz Cart $** (column K): should equal Cart $ × Biz %
- **Biz GC $** (column L): should equal GC $ × Biz %
- **Biz Cash $** (column M): should equal Net $ × Biz %

Report the completed entry with these calculated values to the user.

## Common Issues and Solutions

**Issue:** Percentages showing as 7968% instead of 79.68%
**Solution:** Enter as decimal value (0.7968), not percentage (79.68). The column has percentage formatting that multiplies by 100.

**Issue:** Can't find next empty row
**Solution:** Active filters may hide rows. Clear filters or check for actual last row with data

**Issue:** User unsure if item is business or personal
**Solution:** Ask for clarification before proceeding. Don't guess.

## Notes on Mixed Orders

Mixed orders are the most complex scenario. The business percentage represents what portion of the purchase is deductible as a business expense. This must be calculated accurately because:
- It affects tax reporting
- It tracks business vs personal spending
- The formulas cascade this percentage through multiple columns

Always show your math when calculating Biz % so the user can verify it's correct.
