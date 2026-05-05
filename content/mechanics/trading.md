---
title: "Trading"
subtitle: "Player-to-player Pokémon trading — when it unlocks and how the level cap works"
---

Trading lets two players swap Pokémon (and tradeable items) directly, party-to-party. It's gated behind a Trainer-Level requirement, and once unlocked the Pokémon you can give or receive are still capped by your Trainer Level.

## Unlock requirement

Trading unlocks at **Trainer Level 10**. Both you and the player you're trading with must be Trainer Level 10 or higher — if either side is below, the trade window won't open and you'll get the *"You must be trainer level 10 to trade Pokémon"* message.

A few extra gates apply on top of the level requirement:

- Neither player can be in an active battle.
- Neither player can have an active challenge running.
- Neither player can have an increased difficulty active.
- On Survival, Pokémon obtained during a previous season cannot be traded.

## Pokémon level cap

Each side of a trade is checked against the **maximum wild-encounter level for their Trainer Level**, in the current generation. A Pokémon can only change hands if its level is `≤` that cap on **both** the sending and receiving sides — so the lower of the two players' caps is the one that actually binds the trade.

If the cap blocks a transfer, the rejected player is told the highest level they're allowed to send or receive.

A handful of Pokémon are exempt from being traded at all (the level cap doesn't even come into it):

- Starters (unless they came from an egg, the rank store, or the egg manager).
- Legendaries, when legendary-trading is disabled server-side.
- Bred Pokémon.
- Purified Pokémon (out of the Purification Lab).
- Pokémon currently assigned to a gym.
- Pokémon flagged untradeable individually (event gifts, the Casey gift, etc.).
- Pokémon the receiving player already owns.

## Cap by Trainer Level

The cap depends on which generation you're playing. Gen 1 hands out higher trade caps early; Gen 2 keeps you at level 6 until very late; Gen 3 onward uses a slower, smoother curve that's shared across Gen 3, Gen 4, and Gen 5.

Tables start at Trainer Level 10 (the trade unlock). Repetitive tail rows are collapsed.

### Gen 1

| Trainer Level | Max tradeable Pokémon level |
|---:|---:|
| **10** | **30** |
| 11 |  33 |
| 12 |  36 |
| 13 |  38 |
| 14 |  40 |
| 15 |  42 |
| 16 |  44 |
| 17 |  45 |
| 18 |  47 |
| 19 |  49 |
| 20 |  50 |
| 21 |  51 |
| 22 |  52 |
| 23 |  53 |
| 24 |  54 |
| 25 |  55 |
| 26 |  60 |
| 27 |  70 |
| 28 |  80 |
| 29 |  90 |
| 30 | 100 |

Trainer Level 30 is the cap for Gen 1; from there onward the trade ceiling stays at 100.

### Gen 2

| Trainer Level | Max tradeable Pokémon level |
|---:|---:|
| 30 – 31 |   6 |
| 32 |  10 |
| 33 |  14 |
| 34 |  18 |
| 35 |  21 |
| 36 |  26 |
| 37 |  30 |
| 38 |  33 |
| 39 |  36 |
| 40 |  40 |
| 41 |  44 |
| 42 |  47 |
| 43 |  50 |
| 44 |  51 |
| 45 |  52 |
| 46 |  53 |
| 47 |  54 |
| 48 |  55 |
| 49 |  60 |
| 50 | 100 |

Gen 2 picks up where Gen 1 leaves off — your Trainer Level continues from 30 onward. The trade cap holds at level 6 through the first couple of Trainer Levels and doesn't start climbing until Trainer Level 32. Trainer Level 50 is the Gen 2 cap.

### Gen 3, Gen 4, Gen 5

These three generations share the same trade-cap table.

| Trainer Level | Max tradeable Pokémon level |
|---:|---:|
| 10 |  12 |
| 11 – 12 |  15 |
| 13 – 14 |  18 |
| 15 – 16 |  21 |
| 17 – 18 |  25 |
| 19 – 20 |  28 |
| 21 – 22 |  30 |
| 23 – 24 |  33 |
| 25 – 26 |  36 |
| 27 – 28 |  38 |
| 29 – 30 |  40 |
| 31 – 32 |  44 |
| 33 – 34 |  45 |
| 35 – 36 |  47 |
| 37 – 39 |  49 |
| 40 |  50 |
| 41 |  51 |
| 42 |  52 |
| 43 |  53 |
| 44 |  54 |
| 45 |  55 |
| 46+ | 100 |

Note that the trade unlock at Trainer Level 10 lands you in the **12** bracket on Gen 3+. If you want to trade a higher-level Pokémon to a friend — or receive one — the *receiving* player's Trainer Level is what matters most: they need to be high enough that the cap covers the Pokémon being sent.

## Where trading happens

- `/trade <player>` opens a trade window with another player on the same server.
- In Survival, **Trading Machines** placed in the world also handle player-to-player trades within a 5-block range of each participant.

Trade evolutions (Kadabra, Machoke, Haunter, Graveler, etc.) trigger automatically the moment the trade completes, just like in mainline games.
