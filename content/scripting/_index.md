---
title: "Scripting How-To"
subtitle: "Pokéfind quest scripting reference for builders and contributors"
---

A practical reference for writing JSON quest scripts against the Pokéfind/Lucille stage system. Not an exhaustive API reference (the source code is the canonical reference) — this section is for the patterns that get used over and over and the foot-guns that aren't documented anywhere.

Pages are organized by stage type:

- **Triggers** — how players cause stages to fire (`ClickEntity`, `RegionEntry`, `ClickToStart`, etc.)
- **Effects** — what stages produce (`SendMessage`, `NewDialog`, `GiveItem`, `Show/Hide`)
- **Conditions / gates** — `If`, `Equals`, `HasItem`, `HasPokemon`, `Completed`
- **Patterns** — angry-Pokémon blocker, multi-position recurring NPC, found-text framing, modular puzzle script handoff
