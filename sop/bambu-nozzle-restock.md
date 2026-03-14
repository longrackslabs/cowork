# Bambu Lab Nozzle Restock Workflow

## Overview
Keep the eBay selling engine running. Stock-outs kill ads, and it takes days to
re-prime — that downtime costs more than any cash bridge ever would. Restock early,
restock often. Claude loads the cart, George does the checkout.

**We only stock bare nozzles (NZ- SKUs). No complete hotends (HN- SKUs).**

## Trigger: Manual — George says "restock" or "load the cart"
This is a separate workflow from `inventory`. George triggers it when he has enough
GC balance built up. Don't auto-run after inventory updates.

## Step 1: Check GC Balance & Points
- Check existing GC balance in inventory sheet → **Gift Cards (Active)** tab
- Gift cards cost **490 points each** for $40 from MakerWorld
- **Restock trigger:** 980 points (2 GCs) + shortages exist → pull the trigger
  - 2 GCs ($80) + any leftover GC balance + biz cash to hit $90+ for free shipping
  - Max out-of-pocket: ~$10 (when no leftover GC balance). That $10 becomes inventory that resells for $20+ on eBay — it's not an expense, it's acceleration capital
  - Out-of-stock downtime (ads go dark, days to re-prime) costs more than the cash bridge ever would

## Step 2: Redeem Gift Cards
- On the Points Shop (`https://makerworld.com/en/points`), find the **"Gift Card for $40"** (490 points)
- Click **"Get"** → it shows the gift card code immediately
- **You can only redeem ONE at a time** — no bulk purchase
- Copy the code → switch to Bambu checkout tab → paste into "Enter code" field
- Switch back to MakerWorld → click "Get" again for the next gift card
- Repeat for 2 GCs total (2 × 490 = 980 points = $80)
- Note: card says "Review will be completed within 5 business days" — check if there's a delay

## Step 3: Check Inventory Shortages
- Google Sheet: "Longracks Labs Financials 2026" → Inventory tab
- Look at "Reorder" column for 🔴 Reorder items
- Note the "Reorder Qty" for each NZ- SKU (nozzles only — no hotends)

## Step 4: Load Bambu Lab Shopping Cart

### IMPORTANT — Bambu Lab naming:
- **"Bare Nozzle"** = just the nozzle tip — this is what WE sell (NZ- SKUs)
  - Bambu lists these under "Hotend" category on the Bulk Sale page
- **"Complete Hotend"** = full assembly with fan, heater, wiring — we do NOT stock these

### Always start from an empty cart:
- Before loading, **clear the existing cart** first — go to `https://us.store.bambulab.com/cart` and remove all items
- Then build the full cart from scratch every time
- This avoids complex logic around partial carts, wrong quantities, or stale items
- It takes the same amount of time either way since Claude is doing the work, and reliability matters more than speed

### Exact navigation path:
1. Go to `https://us.store.bambulab.com/pages/promotions/Hotends-Bulk-Sale`
   - (Or: hamburger menu → Sale → Accessory Sale → Hotends Bulk Sale)
2. Click **"For X1C"** filter tab at top of page
3. Page shows two rows:
   - **Top row** = Complete Hotends (~$35.99 each before discount)
   - **Bottom row** = Bare Nozzles (~$15.99 each before discount)
4. Use **+/- buttons** directly on the page to set quantities for each size
5. Click **"Add To Cart"** when done

### Bulk discount tiers (as of Feb 2026):
- 2 items → 5% off
- 3 items → 10% off
- 4 items → 15% off
- 5 items → 20% off
- **6+ items → 30% off** ← sweet spot for us
- Prices shown: bare nozzle $15.99, complete hotend $35.99 (before discount)

### Stock behavior:
- Out-of-stock sizes **disappear entirely** from the page (no "sold out" label)
- 0.2mm bare nozzle is frequently out of stock
- If 0.2mm nozzle is missing from bottom row, it's out of stock — skip it

### Our nozzle sizes and Bambu part numbers:
- 0.2mm Stainless Steel — FAH004 (complete) / FAH004-N-1 (bare nozzle)
- 0.4mm Hardened Steel — FAH001 (complete) / FAH001-N-1 (bare nozzle)
- 0.6mm Hardened Steel — FAH005 (complete) / FAH005-N-1 (bare nozzle)
- 0.8mm Hardened Steel — also available but we don't typically stock

### Buying rules:
- Budget: **$90–$120** (over $90 for free shipping, funded by GCs + biz cash if needed)
- Target **6+ items** to unlock 30% bulk discount
- **Bare nozzles only** (~$11.19 each after 30% off)
- If a size is out of stock, skip it and load up on other sizes
- **Prioritization:** Fill by largest shortage qty first
- Fill cart up to budget, leave checkout for George
- After adding to cart, go to `https://us.store.bambulab.com/cart` to **verify quantities**
  - Known quirk: cart has occasionally dropped an item during add (e.g. 6→5)
  - Always confirm both line items match what was set on the Bulk Sale page

### Test run results (Feb 2026 — confirmed working):
- Navigated to Bulk Sale → filtered "For X1C" → set 0.4mm×4 + 0.6mm×6 → Add To Cart
- Cart showed: 10 items, $111.93 total, 30% discount applied, free shipping qualified
- 0.2mm bare nozzle was out of stock (not shown on page) — confirmed expected behavior
- Complete hotends skipped — nozzles only going forward

## Step 5: Notify George
- Tell George what's in the cart, total price, and anything that was out of stock
- He does the final checkout:
  1. Click Checkout → `https://us.store.bambulab.com/checkouts/{session_id}`
  2. Log into Longracks Labs account
  3. Switch to MakerWorld tab → click "Get" on Gift Card for $40 → copy the code
  4. Switch to Bambu checkout → paste code into **"Enter code"** field → hit **Apply**
  5. **Repeat steps 3-4** for each gift card (one at a time, no bulk redeem)
  6. Any leftover GC balance → tracked in inventory sheet (GC balance tab)
  7. If GCs don't fully cover cart → pay remainder as **"Biz Cash"** per ledger
  8. Click **Pay Now**

### Note on GC volume:
George redeems 100s of gift cards/year from MakerWorld points (high print volume).
Bambu's system only allows one GC redemption at a time — it's tedious but it works.

## Step 6: Post-Checkout Updates
After George completes checkout and provides the order confirmation:

1. **Log the purchase to the Ledger** per `bambu-order.md`
2. **Update Inventory "Ordered" column** — for each SKU purchased, set the Ordered value to the quantity ordered
   - This feeds into the Total column (On Hand + Ordered) and Target +/- calculation
   - Without this, the restock trigger will see the same shortages and try to reorder duplicates
   - When the order arrives, George runs `received X,X,X` — that updates On Hand and clears the Ordered column automatically

## Chrome Profile
Use **Longracks Labs** profile for both MakerWorld and Bambu Lab store.
