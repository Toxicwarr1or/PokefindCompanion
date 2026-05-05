---
title: 'Safari Zone'
subtitle: 'Pay once, swing for thirty Safari Balls, and try your luck across seven biome-themed areas.'
---

The **Safari Zone** is a paid catch-only minigame run by the **Safari Ranger** at the entrance lodge. You hand over **500 coins**, get a stack of Safari Balls, and have until the balls run out (or you walk out of bounds) to catch as many Pokémon as you can. Encounters here use Safari Balls only — you can't bring your team in and battle, and you can't pick a Safari Ball back up off the ground once it's been thrown.

When the run ends — either because you ran out of balls or stepped over the boundary — the Ranger tallies up everything you caught and you're teleported back to the lobby.

## Entry & Safari Balls

- **Cost:** 500 coins, paid to the Safari Ranger.
- **Base balls:** 30 Safari Balls per run.
- **Rank bonus** (added on top of the base 30):
  - **Pro** — +5 balls
  - **Elite** — +10 balls
  - **Expert** — +15 balls
  - **Champion** — +20 balls
  - **Legend** — +25 balls
- **Event bonuses** can stack on top of the rank bonus during seasonal events.

You can't teleport mid-encounter — once a Pokémon appears, you're locked into the Safari battle until you catch it, scare it off, or it flees.

## Pokéblock Feeders

Scattered across the zone are **47 Pokéblock Feeders** — small clickable stations marked with a yellow *Feeder* hologram. Right-click one with a Pokéblock in your inventory to bait the surrounding area.

- **Range:** about 10 blocks around the feeder.
- **Duration:** burns down by **one** for each block of movement any player makes while inside the feeder's range — so 200 "steps" is roughly 200 blocks of in-range walking, pooled across everyone present.
- **Effect:** while active, wild Pokémon that spawn near the feeder have an **80% chance** to roll a Nature that **likes** the Pokéblock's flavor.

| Pokéblock | Flavor | Nature pull |
|---|---|---|
| Red Pokéblock | Spicy | Spicy-loving Natures (Adamant, Brave, Lonely, Naughty) |
| Blue Pokéblock | Dry | Dry-loving Natures (Modest, Mild, Quiet, Rash) |
| Pink Pokéblock | Sweet | Sweet-loving Natures (Gentle, Hasty, Jolly, Naive) |
| Green Pokéblock | Bitter | Bitter-loving Natures (Calm, Careful, Sassy, Careful) |
| Yellow Pokéblock | Sour | Sour-loving Natures (Bold, Impish, Lax, Relaxed) |

Only one feeder can be active per location at a time, and a feeder won't accept a new Pokéblock while it's still running. If you click an active feeder, the Ranger's apprentice has already done your job for you — come back after the timer runs out.

## How encounters work

- **Tall grass / ferns** trigger normal land encounters as you walk through them.
- **Water and ice tiles** trigger surfing encounters — only Water- and Ice-typed Pokémon spawn here.
- Hidden Abilities roll at roughly **5%** per spawn.
- Shiny rolls only happen **while a shiny event window is currently active** server-wide. During that window, Safari spawns roll shiny at **18%**.

If two area definitions overlap (e.g. Hill sitting above the Cave), the spawn pulls from whichever area you're physically standing inside; surfing tiles always pull from the water-typed half of that area's pool.

---

## The encounter menu

When a wild Pokémon appears, you're frozen in place and the *"What will you do?"* menu opens. You have four options, and you'll loop back to the menu every turn until the Pokémon is caught, flees, or you walk away.

- **Throw Ball** — consumes one Safari Ball and throws it. The encounter resolves on hit (catch or break-out). If the ball doesn't land within 10 seconds, the turn ends automatically.
- **Razz Berry** — consumes one Razz Berry from your inventory. The Pokémon **eats** for **1–5 turns**: while eating, it's **less likely to flee**, but it's also **harder to catch**.
- **Throw Rock** — free; throws a cobblestone at the Pokémon. The Pokémon is **angry** for **1–5 turns**: while angry, it's **easier to catch**, but it's also **more likely to flee**.
- **Run** — leaves the encounter cleanly with *"Got away safely!"*. No ball cost, no penalty — just walk away.

Razz Berry and Rock effects do **not** stack: feeding a Razz Berry clears any anger, and throwing a rock interrupts any eating. Each turn the active state ticks down by one; once it expires, flee and catch rates return to baseline.

**Flee chance per turn** is rolled from the Pokémon's species-level Safari flee rate, then doubled if it's angry or halved if it's eating, and clamped between **2%** (rock-bottom floor) and **95%** (effective ceiling). So even the calmest Pokémon can occasionally bolt, and even the most skittish gives you at least a small window to land a ball.

A practical loop most players settle into:

1. Open with a **Razz Berry** if you really want the catch and it has a reputation for fleeing (e.g. Audino, Lapras).
2. If you've got Safari Balls to burn and the Pokémon is something common, lead with a **Rock** — the doubled catch chance pays off quickly even with the doubled flee risk.
3. If a Razz/Rock turn passes without a successful catch, you can re-feed or re-throw on the next menu — or just spam balls while the buff/debuff is still ticking.

---

## Areas

The zone is divided into seven themed regions. Pokémon are at **level 5** across the entire Safari Zone — what changes between areas is *which* species can roll and how heavily the pool is weighted toward each one.

### Area 1 — Entrance

A wide grassland just past the Ranger's lodge. Bug catchers and small Normal-types make up most of the pool, with the rare starter cameo.

- **Common** — Patrat, Pidove, Lillipup, Karrablast
- **Uncommon** — Minccino, Shelmet, Slakoth, Petilil, Bouffalant, Durant
- **Rare** — *(none)*
- **Ultra-Rare** — Bulbasaur, Pansage

### Area 2 — Middle

The mid-zone wetland and brush. The largest, most varied pool in the Safari Zone — Poison- and Bug-types dominate, but a healthy water-edge element brings in Water-type surfing spawns.

- **Common** — Tympole, Sewaddle, Basculin, Petilil, Trubbish, Stunky, Ekans
- **Uncommon** — Croagunk, Grimer, Minccino, Joltik, Bouffalant, Seviper, Zangoose, Poliwag, Ducklett, Finneon
- **Rare** — Foongus, Tynamo, Audino, Venipede, Ferroseed, Pawniard, Carvanha
- **Ultra-Rare** — *(none)*

### Area 3 — Hill

Elevated grasslands above the rest of the zone, with ponds and clearings. Strong Flying- and Normal-type presence, plus the zone's deepest Dragon-type pulls.

- **Common** — Ducklett, Patrat, Pidove, Deerling
- **Uncommon** — Dwebble, Scraggy, Minccino, Magikarp, Blitzle, Druddigon, Azurill, Horsea, Slowpoke, Rufflet
- **Rare** — Sigilyph, Wingull, Vullaby
- **Ultra-Rare** — Castform, Axew, Dratini

### Area 4 — Cave

Underground tunnels with subterranean pools. Cave staples up top, Water-types in the pools, and a couple of well-hidden Psychic / Dark prizes.

- **Common** — Zubat, Purrloin, Basculin
- **Uncommon** — Woobat, Wooper, Roggenrola, Magikarp, Horsea, Chinchou
- **Rare** — Foongus, Clamperl, Lapras, Buizel, Mantyke
- **Ultra-Rare** — Gothita, Solosis, Panpour, Zorua

### Area 5 — Beach

The shoreline at the western edge of the zone. Surfing-heavy pool with sand-and-stone bug life on the dunes and a Squirtle cameo in the water.

- **Common** — Frillish, Basculin, Ducklett
- **Uncommon** — Krabby, Dwebble, Stunfisk, Shellos, Magikarp, Timburr, Maractus, Darumaka, Luvdisc, Wingull
- **Rare** — Alomomola, Clamperl
- **Ultra-Rare** — Drilbur, Sandile, Squirtle

### Area 6 — Fairy Cave

A bright, pastel cavern in the northeast. Fairy- and Normal-types with a heavy weighting toward the easier-to-spot species — ideal if you're hunting a Chansey or Marill.

- **Common** — Cinccino, Snubbull, Marill, Chansey, Swablu
- **Uncommon** — Clefairy, Cottonee
- **Rare** — *(none)*
- **Ultra-Rare** — Igglybuff, Azurill, Ralts, Togepi

### Area 7 — Fire Cave

A volcanic chamber tucked under the southwest cliffs. Almost entirely Fire-types, with a Ground-type detour and a Charmander cameo.

- **Common** — Heatmor, Numel, Vulpix, Nosepass, Growlithe, Gligar, Houndour, Ponyta
- **Uncommon** — *(none)*
- **Rare** — Slugma
- **Ultra-Rare** — Pansear, Charmander, Litwick

---

## Tips

- **Feed before you wander.** A single Pokéblock buys you 200 steps of Nature-targeted spawns within 10 blocks of the feeder — drop one, walk a tight grid around it, and you'll burn through your balls with much better Natures than running blind.
- **Water Pools are typed.** Water/Ice-type entries in a list will only roll on water or ice tiles, not in grass. If you want Lapras (Cave) or Frillish (Beach), you have to be in the water.
- **Mind the boundary.** Stepping out of the Safari Zone region ends your run early — *"You left the Safari Zone!"*. The end-of-run summary still pays out for what you caught, but any unspent balls are forfeit.
- **The cave-dwelling Ultra-Rares (Zorua, Gothita, Solosis) are the rarest catches available in the current zone.** Save your last few Safari Balls for them if you spot one.
