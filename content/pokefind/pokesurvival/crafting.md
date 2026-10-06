---
title: "Crafting & Machines"
subtitle: "Poké Balls from Apricorns, unlockable recipes, and the Breeding, Fossil and Trading machines"
---

<!--
  STATUS: scaffold 2026-09-25. Poké Ball chain verified against Survival Tutorials/survival-pokeball-tutorial.json (Sep 9).
  Machines/blocks from the survival.world.blocks package. TODO: other ball recipes, berry list, recipe unlock rules, Smith/Fletcher menus.
-->

PokéSurvival replaces a lot of PokéWorld's NPC services with things you grow, craft or build yourself. `/recipes` shows every recipe you have unlocked so far; recipes unlock as your trainer attributes progress (`/attributes`).

---

## Poké Balls from scratch

Professor Redwood's *From Tree to Poké Ball* tutorial walks through the chain:

1. **Get a Berry Pot** from Uncle Jesse at spawn (free). Use it in hand — do not place it in a hole.
2. Inside the pot, switch to **Apricorns**, pick an empty slot and plant a **Red Apricorn**. Harvest nine.
3. **Smelt** the Apricorns in a furnace → Cooked Red Apricorns.
4. **Poké Ball Lid**: three Cooked Red Apricorns in the middle row of the crafting grid.
5. **Iron Disc**: three Iron Ingots in the middle row (nine ingots makes three).
6. **Poké Ball**: Lid on top, **Stone Button** in the middle, Iron Disc underneath, in a single column.

Other Apricorn colours make other balls — Blue and Red together make a Great Ball. *TODO: full ball table.*

## Berries and Apricorns

Grown in Berry Pots. `/berryinfo` explains growth. *TODO: berry list and how each is unlocked.*

## Machines

Place-able blocks that replace NPC services in the wild:

| Machine | Does |
| --- | --- |
| **Breeding Machine** | Breed two compatible Pokémon for an egg |
| **Fossil Incubator** | Revive fossils found while mining |
| **Trading Machine** | Trade Pokémon with another player |

*TODO: recipes, timings, fossil list.*

## Smith and Fletcher

The **Smith** at spawn handles gear; the **Fletcher** *TODO*. Both open a menu on click.

## Evolution Stones

Found in the world rather than bought. *TODO: where.*
