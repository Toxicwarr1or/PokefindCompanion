---
title: "Currencies"
subtitle: "PokéCoins, Tokens, Battle Points, Challenge Coins, Wish Dust, and PokéGems — what each one is, how you earn it, and where it gets spent"
---

Pokéfind ships **six** distinct currencies that all live on your trainer profile. Three are the day-to-day economy you hit constantly; two are tied to specific gameplay loops; one is a paid premium currency from the web store.

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
  - **Bags** — purchased from the **Bag shops** scattered across the region.
  - **Bikes** — purchased from the **Bike shops** scattered across the region.
  - **Evolution stones** — traded for at the **Mystery Man** NPC.
  - **Breeding** — each breeding session at the Daycare costs **25 tokens**.

### <img class="currency-icon" src="/images/currencies/bp.png" alt=""> Battle Points (BP)

Pure PvE-tower reward.

- **What it is:** the Battle Tower's payout currency, displayed in aqua.
- **Earned from:** clearing rounds in the **Battle Tower** (with bonus payouts on Iconic-Trainer rounds at round 10), plus voting rewards.
- **Spent at:** the **Battle Tower Shop** NPC near the Battle Tower entrance. The shop sells competitive held items, battle items, EV vitamins, all 17 type plates, and a few high-tier consumables. Items can be sold back at roughly 20% of buy price.

The full catalogue, grouped by buy price (sell price in parentheses):

| Buy | Sell | Items |
| --- | --- | --- |
| **24 BP** | (5) | Iron, Carbos, HP Up, Protein, Zinc, Calcium |
| **48 BP** | (10) | Focus Sash, Cell Battery, Air Balloon, Absorb Bulb, Red Card, Eject Button, Luminous Moss, Snowball, Weakness Policy, Power Herb, Mental Herb, White Herb, Grassy Seed, Electric Seed, Misty Seed, Psychic Seed, Sticky Barb |
| **168 BP** | (34) | Quick Claw, Lucky Punch, Metal Powder, Quick Powder, Focus Band, PP Up, Thick Club |
| **216 BP** | (44) | Muscle Band, Silk Scarf, Float Stone |
| **288 BP** | (58) | Iron Ball, Lagging Tail, Scope Lens, Wide Lens, Bright Powder, Full Incense, Terrain Extender, Reek, Safety Goggles, Shed Shell, the type-boost held items (Black Belt, Black Glasses, Charcoal, Dragon Fang, Hard Stone, Magnet, Miracle Seed, Mystic Water, Odd Incense, Poison Barb, Sharp Beak, Silver Powder, Soft Sand, Spell Tag, Wise Glasses), and all 17 Arceus plates (Draco, Dread, Earth, Fist, Flame, Icicle, Insect, Iron, Meadow, Mind, Pixie, Sky, Splash, Spooky, Stone, Toxic, Zap) |
| **336 BP** | (68) | Ability Capsule, Max PP |
| **378 BP** | (76) | Big Root, Black Sludge, Metronome, Grip Claw, Binding Band |
| **456 BP** | (92) | Shell Bell, Rocky Helmet, Expert Belt, Flame Orb, Toxic Orb |
| **468 BP** | (94) | Leftovers, Protective Pads |
| **768 BP** | (154) | Choice Band, Choice Scarf, Choice Specs, Eviolite, Life Orb, Assault Vest |
| **12 000 BP** | (2 400) | Destiny Knot |

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
- **Spent at:** the in-game **`/store`** command, which opens the PokéGems Store menu. Donator **ranks** (PRO, EXPERT, ELITE) and other premium items are bought here, paid for in PokéGems.
- **Display glyph:** the PokéGems Unicode character; chat colour green.

---

## At-a-glance comparison

| Currency | Tier | Primary source | Primary sink |
| --- | --- | --- | --- |
| <img class="currency-icon" src="/images/currencies/coins.png" alt=""> **PokéCoins** | Main | Quests, voting, drops | Pokémart / general shops |
| <img class="currency-icon" src="/images/currencies/tokens.png" alt=""> **Tokens** | Main | Vote rewards, vote-shop bundles | Bag shops, Bike shops, breeding, Mystery Man stones |
| <img class="currency-icon" src="/images/currencies/bp.png" alt=""> **Battle Points** | Main | Battle Tower runs | Battle Tower Shop (held items, plates, EV vitamins) |
| **Challenge Coins** | Lesser | Challenge events | Challenge Shop (`/challenges`) |
| **Wish Dust** | Lesser | Voting (with event multiplier) | Vote Shop (`/vote`) |
| <img class="currency-icon" src="/images/currencies/pokegems.png" alt=""> **PokéGems** | Premium | `store.pokefind.co` purchase | In-game PokéGems Store |

---

## How to check your balances

| Command | Shows |
| --- | --- |
| `/coins` (or any of its aliases) | PokéCoins, Tokens, Battle Points |
| Talk to the **Battle Tower Shop** NPC | BP balance + tower-shop catalogue |
| `/vote` → Vote Shop | Wish Dust balance + voting-shop catalogue |
| `/challenges` → Challenge Shop | Challenge Coin balance + challenge catalogue |
| `/store` | PokéGems balance + premium / rank catalogue |
