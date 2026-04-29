---
title: "Currencies"
subtitle: "PokéCoins, Tokens, Battle Points, Challenge Coins, Wish Dust, and PokéGems — what each one is, how you earn it, and where it gets spent"
---

Pokefind ships **six** distinct currencies that all live on your trainer profile. Three are the day-to-day economy you hit constantly; two are tied to specific gameplay loops; one is a paid premium currency from the web store.

> The `/coins` command also responds to `/balance`, `/bal`, `/money`, `/eco`, `/economy`, `/tokens`, and `/battlepoints` — they all open the same readout: PokéCoins, Tokens, and Battle Points side-by-side.

---

## Main currencies

### <img class="currency-icon" src="/images/currencies/coins.png" alt=""> PokéCoins

The base economy. Earned almost everywhere, spent almost everywhere.

- **What it is:** the "money" in your trainer wallet. The chat colour is gold.
- **Earned from:** quest payouts, voting rewards, defeating trainers, selling items, and miscellaneous in-world drops.
- **Spent on:** the Pokémart and most NPC shops, item purchases throughout the world, and quest-gated services.

### <img class="currency-icon" src="/images/currencies/tokens.png" alt=""> Tokens

A more involved currency than PokéCoins — typically reserved for bigger one-time unlocks rather than consumables.

- **What it is:** a secondary spending currency separate from PokéCoins.
- **Earned from:** voting rewards and Vote-Shop bundles sold in 25 / 50 / 100 token packs.
- **Spent on:**
  - **Bikes** — purchased from the Bike menu at varying token prices per cosmetic.
  - **Bags** — purchased from the Bag menu at **400 tokens** apiece.
  - **Evolution stones** — traded for at the **Mystery Man** NPC.
  - **Breeding** — each breeding session at the Daycare costs **25 tokens**.

### <img class="currency-icon" src="/images/currencies/bp.png" alt=""> Battle Points (BP)

Pure PvE-tower reward.

- **What it is:** the Battle Tower's payout currency, displayed in aqua.
- **Earned from:** clearing rounds in the **Battle Tower** (with bonus payouts on Iconic-Trainer rounds at round 10), plus voting rewards.
- **Spent at:** the **Battle Shop** NPC near the Battle Tower entrance — the NPC's greeting line, *"We only take Battle Points here!"*, makes the gate explicit. The shop's catalogue is **competitive Pokémon held items and battle items**, including:
  - **Held items** — Focus Sash (48 BP), Focus Band & PP Up (168), Muscle Band & Silk Scarf (216), the type-boost stones (Black Belt, Black Glasses, Charcoal, Dragon Fang, Hard Stone, Magnet, Miracle Seed, Mystic Water, Never-Melt Ice, Odd Incense, Poison Barb, Sharp Beak, Silver Powder, Soft Sand, Spell Tag, Wise Glasses — all 288), Big Root, Black Sludge (378), Expert Belt, Flame Orb (456), Leftovers (468), Choice Band, Choice Scarf, Choice Specs, Eviolite, Life Orb (768), Destiny Knot (12 000)
  - **Battle items** — Absorb Bulb, Cell Battery, Air Balloon (48 each)
  - **Utility consumables** — Ability Capsule, Max PP (336)

---

## Lesser-used currencies

### Challenge Coins

Tied to the Challenges system.

- **Earned from:** completing specific Challenge events (some pay flat amounts, others roll a chance-based drop).
- **Spent at:** the **Challenge Shop** — opens via the `/challenges` command (also `/challenge`, `/challengelog`, `/challengeslog`). The Challenges menu has a Shop button that opens the Challenge Shop where Challenge Coins are spent.

### Wish Dust

The voting-rewards currency. The chat-reward popup uses a Glowstone-Dust icon for it.

- **Earned from:** voting on server lists. The amount per vote scales with the active **wish-dust multiplier**, which staff can boost during community events.
- **Spent at:** the **Vote Shop** — open via the `/vote` command. The Vote menu lists the active voting sites and provides access to the Vote Shop, where Wish Dust is spent on items that may carry cooldowns and per-account purchase limits.

---

## Premium currency

### <img class="currency-icon" src="/images/currencies/pokegems.png" alt=""> PokéGems

The paid currency, bought outside the game.

- **Where you buy them:** [`store.pokefind.co`](https://store.pokefind.co/). Purchases credit your account next time you log in — the welcome message reads *"Thank you for your purchase of N PokéGems!"*.
- **Acquired through four channels:**
  - **Tebex purchase** — direct buy on the web store
  - **Manual** — staff-issued
  - **Awarded** — given out during events / promotions
  - **Spent** — outflows from the in-game PokéGems Store
- **Spent at:** the in-game **PokéGems Store** menu, organised into categories of items with optional purchase-option variants.
- **Display glyph:** the PokéGems Unicode character; chat colour green.
- **Donator ranks** (PRO, EXPERT, ELITE) are also bought from the same web store, but as direct rank purchases — they aren't priced in PokéGems in-game.

---

## At-a-glance comparison

| Currency | Tier | Primary source | Primary sink |
| --- | --- | --- | --- |
| <img class="currency-icon" src="/images/currencies/coins.png" alt=""> **PokéCoins** | Main | Quests, voting, drops | Pokémart / general shops |
| <img class="currency-icon" src="/images/currencies/tokens.png" alt=""> **Tokens** | Main | Vote rewards, vote-shop bundles | Bikes, bags, breeding, Mystery Man stones |
| <img class="currency-icon" src="/images/currencies/bp.png" alt=""> **Battle Points** | Main | Battle Tower runs | Battle Shop (held items, battle items) |
| **Challenge Coins** | Lesser | Challenge events | Challenge Shop (`/challenges`) |
| **Wish Dust** | Lesser | Voting (with event multiplier) | Vote Shop (`/vote`) |
| <img class="currency-icon" src="/images/currencies/pokegems.png" alt=""> **PokéGems** | Premium | `store.pokefind.co` purchase | In-game PokéGems Store |

---

## How to check your balances

| Command | Shows |
| --- | --- |
| `/coins` (or any of its aliases) | PokéCoins, Tokens, Battle Points |
| Talk to the **Battle Shop** NPC | BP balance + tower-shop catalogue |
| `/vote` → Vote Shop | Wish Dust balance + voting-shop catalogue |
| `/challenges` → Challenge Shop | Challenge Coin balance + challenge catalogue |
| Open the **PokéGems Store** | PokéGems balance + premium catalogue |
