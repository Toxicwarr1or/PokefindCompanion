---
title: "The Wild"
subtitle: "Leaving spawn, how wild Pokémon are picked, dimensions, homes and claims"
---

<!--
  STATUS: scaffold 2026-09-25. Spawn mechanism verified against SurvivalSpawnManager.java / SpawnManager.java (see SurvivalSpawns tool).
  TODO: territory → biome tables, honey pools, group/claim command reference.
-->

Spawn is a separate lobby server. The **Wild Portal** or `/wild` drops you at a random unclaimed spot in the survival world; `/wild nether` and `/wild end` do the same for those dimensions once you hold the badge that unlocks them (see [Gyms](../gyms/)). `/spawn` brings you back; `/home` brings you to a home you have set.

---

## How wild spawns are chosen

PokéSurvival does not use a per-species biome table. Each spawn tick:

1. A random column within about 100 blocks of a player is picked.
2. Its **biome** is read and rolled against a weighted table to pick a **territory** (Terralith and other custom biomes are covered; anything unlisted uses the global pool).
3. A weighted roll inside that territory picks the species, using the shared gen 1–5 spawn sheet.
4. Rows gated above your **trainer level**, or whose minimum level exceeds your obedience cap, are skipped — so what you meet scales with your badges.

Ways to steer it:

- **Honey** — draws Pokémon from Honey's pools; buy it from Honey's shop after her tutorial.
- **Amulets** — while worn, one in five rolls near you pulls from the amulet's type.
- **Safari Zone** — a catch-only reserve at spawn whose pools rotate every quarter; see [Safari Zone](../safari-zone/).

No wild Pokémon spawn inside the gym areas at spawn.

Rare spawns are announced in the Discord `#survival-rare-spawns` feed.

## Dimensions

| Dimension | Requirement |
| --- | --- |
| Overworld | none |
| Nether | Badge 3 |
| End | Badge 6 |

Portals at spawn route you straight into the corresponding wild dimension.

## Homes, groups and claims

- `/home set <name>`, `/home <name>`, `/home list`, `/home delete <name>` — personal homes.
- `/group` — create a group, invite members, claim chunks, set group homes and warps, manage roles and flags.
- `/back` returns to your last location (Legendary rank).

*TODO: claim limits, group flag list, how claims interact with the season reset.*

## Useful commands

| Command | What it does | Rank |
| --- | --- | --- |
| `/wild`, `/wild nether`, `/wild end` | Random teleport into the wild | everyone |
| `/home …` | Homes | everyone |
| `/group` | Groups and claims | everyone |
| `/vault` | Season-safe vault (see [Seasons](../seasons/)) | everyone |
| `/recipes` | Recipes you have unlocked | everyone |
| `/shop` | Survival shop | everyone |
| `/mobdex` | Your MobDex of custom mobs | everyone |
| `/traits` | Your trait progress | everyone |
| `/berryinfo` | Berry growing info | everyone |
| `/toggleparty` | Toggle your Pokémon party following you | everyone |
| `/offhand` | Swap held item to offhand | everyone |
| `/kit` | Daily kit | Pro |
| `/craft` | Portable crafting table | Elite |
| `/feed` | Restore hunger | Elite |
| `/ec` | Enderchest | Champion |
| `/back` | Return to last location | Legendary |
