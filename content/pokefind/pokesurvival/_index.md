---
title: "PokéSurvival"
subtitle: "Pokéfind's seasonal survival gamemode — one open world, an eight-gym gauntlet, and a reset clock"
---

<!--
  STATUS: scaffold, 2026-09-25. Sources: PokemonWorld survival package (Downloads export),
  Survival2026 scripts on Desktop, Survival Gyms Sep 2026 in Documents.
  Anything marked TODO(release) below was drafted from scripts that may not be live yet — confirm before deploying.
-->

**PokéSurvival** is Pokéfind's survival gamemode: vanilla-style Minecraft survival (mining, building, farming, land claims) with Pokémon living in the world around you. Unlike [PokéWorld](../pokeworld/), there are no regions or authored story quests — the map is one large open world, and the structure comes from a fixed **gym gauntlet at spawn** and a **seasonal reset**.

It is a separate gamemode from PokéWorld. Pokémon, items and progress do not move between the two; the only things shared network-wide are your rank and your PokéGems balance.

*This section is being built out. Pages below are scaffolds — details land as they are confirmed in game.*

---

## How it is laid out

### Spawn

Every season starts at the spawn hub: the Professor's Lab, PokéCenter and PokéMart, the Safari Zone gate, the gyms, the Elite Four, the Battle Tower, the Nether and End portals, and a row of utility NPCs (IV checker, EV trainer, move relearner, breeders, trade-evolve, custom fishing, employment office). A warp NPC and `/poi` get you between them.

[More information →](spawn/) — warp list, points of interest with coordinates, NPC roster.

### The gym gauntlet

Eight gyms, the Elite Four, and the Regional Champion — all at spawn. Badges do more than mark progress: each one raises the **trainer-level cap** and the **Pokémon obedience cap**, and two of them unlock dimensions. You need the third badge to enter the Nether and the sixth to enter the End.

[More information →](gyms/) — gym order and types, level caps per badge, Elite Four lineup.

### The wild

Leave spawn through the Wild Portal or `/wild` and you land in the open survival world. Wild Pokémon spawn by **biome territory**, weighted toward your trainer level. Honey, amulets and the Safari Zone give you ways to steer what appears.

[More information →](wild/) — how spawns are picked, dimension access, homes and claims.

### Safari Zone

A catch-only reserve at spawn: 1,000 coins for a run of Safari Balls, ten areas of level-5 Pokémon, and a roster that changes every three months.

[More information →](safari-zone/) — entry rules, the quarterly rotation, every area's pool by season.

### Trainer NPCs

Click-to-battle trainers scattered through the world, tiered from Beginner to Expert and gated on your badge count, plus roaming trainers and the Iconic trainer rotation that opens up once you hold all eight badges.

[More information →](trainers/) — tier table, cooldowns, what each tier pays.

### Battle Tower

Streak-based NPC battles in six Showdown-style formats (UU, UU+, OU, OU+, Ubers, Ubers+), with seasonal leaderboards and a Battle Shop.

[More information →](battle-tower/)

### Crafting and machines

Grow Apricorns and Berries in a Berry Pot, smelt and craft your own Poké Balls, unlock recipes as you progress, and use the Breeding, Fossil and Trading machines instead of NPC services.

[More information →](crafting/) — the Poké Ball recipe chain, `/recipes`, the Smith and the Fletcher.

### Seasons

The world, your inventory, caught Pokémon and the in-game economy reset when a season ends. A small set of things survive: your `/vault`, your Pokédex, rank and cosmetics.

[More information →](seasons/) — what carries over, the end-of-season timeline.

---

## At-a-glance

| | PokéWorld | PokéSurvival |
| --- | --- | --- |
| **Structure** | Five regions, each its own server | One open world, spawn hub + scaling wild servers |
| **Story** | Authored main quests and side quests | None — progression is the gym gauntlet |
| **Pokémon available** | Grows by region, gen 1 → gen 5 | Gen 1–5 pool from the start, filtered by your trainer level |
| **Building / claims** | No | Yes — survival blocks, `/home`, groups and chunk claims |
| **Reset** | Permanent | Seasonal wipe with a persistent vault |
| **Gyms** | 8 per region, per-region badges | 8 at spawn, badges raise level caps and unlock the Nether/End |
| **Carryover between the two** | Rank and PokéGems only | Rank and PokéGems only |
