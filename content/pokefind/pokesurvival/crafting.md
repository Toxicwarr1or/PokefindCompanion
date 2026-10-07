---
title: "Crafting"
subtitle: "Poké Balls from Apricorns, unlockable recipes, and where the old NPC services went"
---

<!--
  STATUS: 2026-10-07. Poké Ball flow from ~/Documents/survival-pokeball-tutorial.json (current tutorial).
  Services per user: breeding = Breeder NPCs, fossils = Scientist Petra, trading = /trade, /pheal + /pc on own claim.
  Berry mutation pairs are not documented here on purpose (discovery is part of the game).
-->

PokéSurvival replaces a lot of PokéWorld's NPC services with things you grow and craft yourself. `/recipes` shows every recipe by category and crafts it for you on the spot; some start locked and open as your traits grow (`/traits`).

**Looking for a specific recipe?** The [Recipe browser](../recipes/) draws every one of them in its crafting table, brewing stand, furnace or smithing table, exactly as you lay it out in game, and its *How to unlock* tab lists what each trait threshold opens.

---

## Poké Balls from scratch

Professor Redwood's *From Tree to Poké Ball* tutorial at spawn walks you through the loop: grow, craft, catch.

1. **Get a Berry Pot** from Uncle Jesse at spawn. They are free. Hold it and use it; do not dig a hole for it.
2. **Plant.** Open the pot and switch to the **Apricorn** tab with the switch in the bottom-right corner. Pick an empty pot, choose a mulch, and buy a **Red Apricorn** seed with coins.
3. **Water.** Each time the plant reaches a new stage, click it to water it. Every watering adds an extra Apricorn to the harvest.
4. **Craft.** Four Red Apricorns in a **+** shape with a **Copper Ingot** in the centre makes four Poké Balls. Smelt Raw Copper if you have none.

Other Apricorn colours make other balls, and every ball recipe is in the [Recipe browser](../recipes/#poke_ball) under *Catching*. Most of them unlock as your catch count climbs.

**Mulch** goes in before the seed. Growth Mulch grows faster, Rich Mulch yields more, Surprise Mulch adds a random bonus. A composter turns spare berries into mulch, so keep them.

**Finding something to throw at.** There is no tracker command out here. Craft a **Tracker** instead: four Iron Ingots in a + with a Redstone Block in the centre, then click it in your hotbar to see what is nearby. Wild Pokémon follow the biome you stand in; see [The Wild](../wild/).

## Berries and Apricorns

Both grow in Berry Pots, with seeds bought inside the pot, and they unlock in different ways.

- **Apricorns** unlock alongside their ball. When a ball's recipe opens in the [Recipe browser](../recipes/#unlocks), the Apricorn colour it needs becomes available to plant.
- **Berries** are not tied to traits. New kinds come from **mutations**: plant different berries next to each other and there is a chance, not a guarantee, that a new berry unlocks. Keep mixing neighbours to find them all.

## Where the services are

There are no placeable machines in PokéSurvival. The jobs those used to do are handled by NPCs at spawn or by commands:

| Need | Where |
| --- | --- |
| **Breeding** | The Pokémon Breeders at the Breeding Center at spawn (see [Spawn](../spawn/)) |
| **Reviving fossils** | Scientist Petra at spawn (see [Jobs](../jobs/)) |
| **Trading** | `/trade` |
| **Healing** | `/pheal` on your own claim, open to all ranks. Elsewhere, use crafted potions or the Nurse at the PokéCenter at spawn |
| **PC access** | `/pc` on your own claim, open to all ranks. Elsewhere, use the PC station at spawn |

## Evolution Stones and fossils

Neither is bought. Miners dig up **evolution-stone shards** that craft into stones, and Excavators dig up **fossil shards** that combine into a fossil — see [Jobs](../jobs/).
