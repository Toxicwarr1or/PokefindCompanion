---
title: "Seasons"
subtitle: "What resets, what carries over, and the end-of-season timeline"
---

<!--
  STATUS: scaffold 2026-09-25. Vault + end-of-season timings verified against VaultManager.java / SeasonEndScheduler.java.
  Keep-box PC page + season length are DESIGN (SeasonalDesign.md), not confirmed shipped — left as TODO on purpose.
-->

PokéSurvival runs in **seasons**. When a season ends the world is replaced and almost everything in it is cleared; a thin layer of your progress survives into the next one.

---

## What resets

- The world — builds, claims, homes, group territory.
- Your inventory, Enderchest, and everything in storage.
- Caught Pokémon outside your party and your first **45 PC slots** — see below.
- Coins and the in-game economy — Marketplace and Auction House listings, job earnings.
- Season leaderboards (Battle Tower and others).

## What carries over

- **Your `/vault`** — a small chest that ignores the reset. 3 slots for everyone, +1 per donor rank up to 9 at Legendary. Only **unstackable** items go in (one item per slot), so it is for gear and keepsakes, not resources.
- **Your party**, and **Pokémon in your first 45 PC slots.** That is page 1 of the PC on Java, or page 1 plus the first half of page 2 on Bedrock. Anything stored past slot 45 is lost with the season.
- **Pokédex** registrations.
- **Rank** and **PokéGems** (both network-wide).

## End-of-season timeline

| When | What happens |
| --- | --- |
| 7 days before | Marketplace and Auction House switch to **claim-only** — you can collect items and money but not list anything new (see [Markets](../markets/)). Daily countdown reminders begin in Discord. |
| 1 day before | An in-game boss bar shows the countdown. |
| Final hours | Reminders at 12h, 6h, 3h, 1h, 30m and 15m. |
| Season end | World swap; new season begins. |
