---
title: "Auction House & Marketplace"
subtitle: "Two ways to trade with other players — timed auctions for anything, and a bulk-goods market for materials"
---

<!--
  STATUS: 2026-10-07. Rules verified against Core AuctionHouseManager / MarketPlaceManager and the survival
  managers on the feat-raid-battles branch (Aug 31): listing via menu, 10–999 min durations, 5% tax on both,
  AH slots per rank, sell-only marketplace, T-7d claim-only. Marketplace categories + order caps come from the
  DEVELOPMENT survival_market_place_dev.json on S3 (no PRODUCTION copy was listed); caps deliberately not stated.
-->

PokéSurvival has two player markets, both opened by command and both using **coins**. Neither has an NPC.

| | Auction House | Marketplace |
| --- | --- | --- |
| **Open with** | `/ah` | `/mp` |
| **For** | One-off items and Pokémon, sold by auction | Bulk materials, sold at a fixed price per unit |
| **How it sells** | Bids over a timer, with an optional Buy-It-Now | Buyers take any quantity instantly |
| **Seller gets** | Final price minus 5% tax | Unit price × amount minus 5% tax |
| **Listings at once** | 3, more with rank (see below) | Depends on rank |

Both lock down in the last week of a season — see [Seasons](../seasons/).

---

## Auction House

`/ah` opens the house. Browse by category — **Pokémon**, **Pokémon Items**, **Combat**, **Tools** and **Misc** — sort, search, or page through everything.

### Selling

Hold the item and use **Sell Item** in the menu. You set:

1. A **starting price**.
2. An optional **Buy-It-Now** price, which must be higher than the start. Enter 0 to skip it.
3. A **duration** in minutes, from 10 up to 999 (about 16½ hours). Enter 0 for the maximum.
4. The **currency**: coins or tokens.

To auction a **Pokémon**, have your party showing and hold the party slot; the game lists the Pokémon rather than the item. Almost anything else in your hand can be listed.

Your listing slots depend on rank:

| Rank | Listings at once |
| --- | --- |
| Player, Pro | 3 |
| Expert, Elite | 5 |
| Champion | 6 |
| Legendary | 7 |

### Bidding

- A bid must beat the current price. If you bid at or above the Buy-It-Now price, you pay that and win on the spot.
- You cannot bid on your own listing, and you cannot raise a bid while you are already the highest bidder.
- When someone outbids you, your coins come straight back. If you were offline, you are told on login.

### When it ends

- With bids, the highest bidder wins and **collects the item from the Auction House**. The seller collects the payout the same way, minus the 5% tax.
- Without bids, the item goes back to the seller to collect.
- You can cancel a listing only while it has **no bids**.

Nothing is handed out automatically. Open `/ah` to claim won items, returned items and earnings.

---

## Marketplace

`/mp` is for raw materials: blocks, wood, ores, food, farming goods, mob drops, brewing supplies, decorative blocks, rare finds and common Pokémon items. Only the items in the market's category list can be sold here; anything else belongs in the Auction House.

**It is entirely player-driven.** The server does not stock the Marketplace. Every listing was put there by another player, and once it sells out the item is gone until someone lists more. There will not always be stock of what you want, and prices rise and fall with supply and demand. If an item is empty, either check back later or ask in chat for players to sell their bulk to the Marketplace.

### Selling

Open the item's page in its category and choose **Sell**. Pick a quantity — a stack, a large stack of 192, a bundle of 1,152, everything you carry, or a custom amount — then a **price per unit**. The menu suggests a **Recommended Price** that matches the current lowest offer, or you can undercut by one, split the spread, or set your own. The items move into escrow and the order goes live immediately. Orders do not expire.

### Buying

Open an item and buy any quantity from the cheapest offers in one click. You pay the listed unit price; the goods land in your inventory.

### Claiming and cancelling

Earnings are not paid out automatically. Open **My Orders** in `/mp` to claim coins from sold orders, minus the 5% tax. You can cancel the unsold remainder of an order at any time and the items come back from escrow.

How many orders you can have open at once depends on rank.

---

## Season end

Seven days before a season ends, both markets switch to **claim-only**:

- The Auction House stops taking listings. Every active auction is ended, bidders are refunded and items go back to their sellers, waiting in `/ah` to be collected.
- The Marketplace stops taking orders. Use My Orders to pull your escrowed items and coins back before the wipe.

Anything left unclaimed when the season ends is lost with it.
