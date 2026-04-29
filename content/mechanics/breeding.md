---
title: "Breeding"
subtitle: "How eggs, inheritance, hatching, and size actually work on Pokéfind"
---

Pokéfind's breeding system follows mainline Pokémon for the broad strokes — egg
groups, Destiny Knot, Everstone, Power items — but several pieces are
Pokéfind-specific. Everything below is sourced directly from the server code,
not from the games.

> **Video walkthrough:** [WarriorToxic — Breeding overview](https://youtu.be/WqY39BbB3bw).
> Recorded before the size system existed, so it doesn't cover XS/XL inheritance —
> see the [size video](https://youtu.be/Fu2NnmfpAhk) (linked again in the size
> section below) for that.

## At a glance

| | |
|---|---|
| **Cost per attempt** | 25 Tokens |
| **Hatch timer** | 1 hour by default (server-tunable, capped at 24h) |
| **Eligible Pokémon** | Gen 1–5 only (dex IDs 1–649) |
| **Custom result** | Manaphy + Ditto → Phione |
| **Breeding venue** | Daycare NPCs **or** in-world Breeding Machines |
| **Egg pickup** | At the breeding location, or using `/breed` with Legend rank |

## Who can breed with whom

The compatibility check runs in this order — fail any line and the pair is
rejected at the menu.

1. **Both Pokémon must be Gen 1–5.** Anything past Volcanion is unbreedable.
2. **Neither parent's egg group can be `undiscovered`.** This is the standard
   Legendary/baby-form lock.
3. **Egg-group overlap.** The pair must share at least one egg group **or** one
   parent must be Ditto. Ditto is treated as a wildcard egg group.
4. **Gender pairing.** One Female + one Male, with two exceptions:
    - Either parent may be Ditto.
    - Two Genderless Pokémon **cannot** breed; one must be Ditto.
    - **Two Dittos cannot breed** either — one of them has to actually be a species.
5. **Skin / form locks.** Shadow, Anniversary, Shiny Anniversary, Alola, Shiny
   Alola, Galarian, and Shiny Galarian Pokémon cannot breed.
   Purified Pokémon cannot breed. A Pokémon hatched from a traded egg you
   haven't opened yourself cannot breed.
6. **Gym-assigned Pokémon cannot breed** — pull them off the gym roster first.

## What gets inherited

### IVs

The egg gets a number of IVs copied from the parent pool; the rest roll random
0–31.

- **Default**: 3 IVs inherited.
- **Destiny Knot** (held by either parent): bumped to **5 IVs** inherited.
- **Power items** (held by either parent): the matching IV is forced through.
  If both parents hold a Power item, one parent's stat is forced and the other
  parent's slot rolls random.

| Item | Inherited IV |
|---|---|
| Power Weight | HP |
| Power Bracer | Attack |
| Power Belt | Defense |
| Power Lens | Special Attack |
| Power Band | Special Defense |
| Power Anklet | Speed |

### Nature

- **Everstone on either parent**: the egg always gets that parent's nature.
  (Either gender works — there's no "must be female" restriction Pokéfind-side.)
- **No Everstone**: random *preferred* nature for the offspring's species.

### Ability

- Default: a random standard ability from the offspring's species.
- If the **female** parent is not Ditto and her ability exists in the offspring's
  pool, there's an **80%** chance to inherit it.
- If the female has the species' **Hidden Ability**, there's a **60%** chance
  the offspring also gets the Hidden Ability.
- **Hidden Ability via Ditto**: if the *male* has the Hidden Ability and the
  female is Ditto, the 60% Hidden Ability roll still applies. (Yes — male can
  pass Hidden Ability through Ditto.)

### Moves

- The egg starts with **one** random move from the species' base moveset.
- Any **egg move that both parents currently know** is inherited.
- Total cap is 4 moves; oldest is dropped first if the inheritance would push
  past 4.

### Poké Ball

The offspring inherits the **female's** ball, with two downgrades:
- If the female is Ditto, the egg comes in a regular Poké Ball.
- If the female is in a Master Ball, the egg comes in a regular Poké Ball.

### Species

Standard rule: if either parent has a baby form earlier in its evolution line,
the egg hatches as that baby form. Otherwise it hatches as the parent species.

## Pokémon size — the Pokéfind-specific bit

Every Pokémon on Pokéfind has a **size tier** that scales the rendered model.
Size is its own attribute (separate from IVs, nature, etc.) and **breeding can
pass it down**.

> **Video walkthrough:** [WarriorToxic — Size breeding explained](https://youtu.be/Fu2NnmfpAhk).

### The seven tiers

| Tier | Model scale | Breed pass-rate | Spawns wild? |
|---|---|---|---|
| **XXS** | 0.40× | 5% | No |
| **XS**  | 0.60× | 20% | Yes |
| **S**   | 0.80× | 50% | Yes |
| **N** (Normal) | 1.00× | 100% | Yes |
| **L**   | 1.35× | 50% | Yes |
| **XL**  | 1.70× | 20% | Yes |
| **XXL** | 2.00× | 5% | No |

XXS and XXL **never** appear in wild encounters. The only way to get them is to
hatch one from an egg.

### Size in the wild

Wild spawns roll on a fixed distribution: 62.5% N, 12.5% S/L, 6.25% XS/XL.

### Size in eggs

Eggs roll on a wider distribution before the inheritance check runs:
50% N, 15% S/L, 7% XS/XL, 3% XXS/XXL.

### How breeding actually inherits size

The egg's "starting size" is picked 50/50 from one of the two parents. Then a
**single roll** decides whether that size sticks:

> `roll < parent_size.breedChance` → offspring keeps the parent's size
> otherwise → offspring drops to **Normal** (N)

Practical reading of the table:
- An **XXS or XXL** parent only passes its size **5% of the time** — the other
  95% of the time the egg comes out Normal.
- An **XS or XL** parent passes its size **20%** of the time.
- An **S or L** parent passes its size **50%** of the time.
- A **Normal** parent always passes Normal.

Because the starting size is rolled per-parent (50/50), and only the chosen
parent's `breedChance` matters, two XXL parents still only have a ~5% chance
of producing an XXL egg — **size doesn't compound from both parents**. To farm
extreme sizes, just keep hatching; pairing two XXLs isn't significantly better
than pairing one XXL with anything.

## Hatching

Eggs incubate while the player **walks**. The trigger is the player movement
event, gated on:

- not riding a Pokémon,
- not flying or gliding,
- not currently in battle,
- standing on a non-air block.

Each block walked decrements `stepsLeft` on every egg in the incubator by 1.
A parent species's egg-step count comes from its `egg_steps` species field —
1,285 for Magikarp, 5,140 for most starters, up to 10,280 for Lapras / Snorlax /
Larvitar / Beldum / Dratini / Bagon / Gible / Phione / Happiny / Munchlax /
Wailmer / Relicanth / Unown / Chansey.

### Hatch boosters

- **Flame Body / Magma Armor** in the player's party: each block consumes **2
  steps** of egg progress instead of 1 (effectively half the walking distance).
- **Hatch Boost 25 / Hatch Boost 50** items: snip 25% or 50% off every
  incubator egg's remaining steps the moment they're used.

When `stepsLeft` hits zero the egg is flagged ready, the player gets an "EGG
READY TO HATCH" title, and the egg waits in the incubator until manually
hatched at a station.

## Incubator capacity by rank

The number of eggs you can carry at once is gated by Trainer rank:

| Rank | Egg slots |
|---|---|
| Player    | 1 |
| Pro       | 2 |
| Expert    | 3 |
| Elite     | 4 |
| Champion  | 5 |
| Legendary | 6 |

## Things that don't work the way they do in the games

- **No Mega Evolution interactions** — Mega stones / Mega forms are not on this
  server, so nothing breeds into a Mega-only state.
- **No Gen 6+ Pokémon are breedable.** Even if you've caught a Gen 6 species
  through events, it cannot be paired.
- **The only custom hybrid result is Manaphy + Ditto → Phione.** No other
  cross-species "produces a different baby" rules are implemented.
- **Two Genderless Pokémon are blocked.** Vanilla allows certain Genderless
  species to breed with each other only via Ditto; Pokéfind enforces this
  strictly.
- **Anniversary, Shadow, and Alolan forms are sterile** — even if a normal-form
  counterpart of the species would normally breed.
