---
title: "Trainer Level"
subtitle: "Your save's progression number — and the wild-spawn unlocks it controls"
---

Your **Trainer Level** (TL) is the per-save progression number that grows every time you battle wild Pokémon. It does two big jobs at once:

1. It sets the **wild-encounter level cap** — the maximum level a wild Pokémon can be when it spawns for you, and the cap that bounds [trading](/mechanics/trading/).
2. It **unlocks species** — many wild spawn entries carry a hidden Trainer-Level minimum, so rare and late-tier Pokémon simply don't appear until your TL is high enough.

## How you gain Trainer XP

Trainer XP is awarded for defeating wild Pokémon and trainers, scaled by your save difficulty. Behind the scenes:

- **Gen 1 and Gen 2** share a fixed XP table — 51 hand-tuned thresholds, with Gen 2 picking up where Gen 1 leaves off (TL 30).
- **Gen 3, Gen 4, Gen 5** use the same simple curve: `XP = level⁴`. So TL 50 = 6.25M XP, TL 100 = 100M XP, TL 200 = 1.6B XP.

| Generation | Max Trainer Level |
|---|---:|
| Gen 1 | 30 |
| Gen 2 | 50 |
| Gen 3 | 200 |
| Gen 4 | 200 |
| Gen 5 | 200 |

In Gen 1 and Gen 2 you can earn XP freely up to the cap — there's no per-stage gate. In Gen 3 onward your TL is also **gated by gym badges**:

| Badges held | Trainer Level cap |
|---:|---:|
| 0 |  10 |
| 1 |  15 |
| 2 |  19 |
| 3 |  23 |
| 4 |  27 |
| 5 |  30 |
| 6 |  35 |
| 7 |  40 |
| 8 | uncapped (200) |

If you try to gain XP while at the badge cap, the game blocks it with a "you can not gain any more Trainer Experience until you obtain a new gym badge" message. Beating the next gym lifts the cap immediately.

## Wild encounter level cap

Whatever your TL is, every wild spawn you bump into is clamped to the per-generation **maximum wild level**. The full per-TL table is on the [Trading page](/mechanics/trading/) — it's the same table that decides what level of Pokémon you can trade and receive. As a quick recap: the cap climbs from 6 at very low TL to 100 at the very top.

A spawn whose `minLevel` is higher than your wild cap won't appear at all. So even if a species has no explicit TL gate, you might still need to grind some levels before its baseline-level entries become reachable.

## Species unlocks

Each row of Pokéfind's spawn data has a per-row Trainer-Level minimum. Until your TL passes that number, the row is filtered out — that species can't roll on your wild encounters. Different generations gate different species:

**The matrix below is not every wild spawn — only the ones that are level-locked.** Any species not listed either spawns from TL 1 in every region it appears in (no effective gate at all), or doesn't spawn wild anywhere on Pokéfind (see the "Pokémon that don't spawn wild" table at the bottom of the page).

A spawn becomes available only once **both** of these are true:

1. Your Trainer Level meets the spawn row's explicit TL gate (if any).
2. The wild-encounter level cap for your TL is **at least the species' minimum spawn level** — otherwise the encounter would roll a level the cap forbids, so the spawn is filtered out.

The cells below give the **effective** lowest TL at which the species can start being seen in each region — already factoring both checks together. An em-dash (—) means the species has no wild spawn entry in that region.

Because the Gen 2 wild cap is locked at level 6 until TL 32 (it then climbs to 10, 14, 18, 21, 26, …), almost every carryover species in Jataro is implicitly locked behind TL 32+ even when its explicit gate is much lower. That's why Dratini reads TL 34 in Gen 2: the explicit gate is 12, but Dratini's minimum spawn level is 16, and TL 34 is the first Jataro level whose wild cap (18) reaches it.

| Pokémon | Gen 1 | Gen 2 | Gen 3 | Gen 4 | Gen 5 |
|---|---:|---:|---:|---:|---:|
| Metapod      |  2 | 32 |  5 |  5 |  5 |
| Butterfree   |  3 | 32 |  7 |  7 |  7 |
| Kakuna       |  2 | 32 |  5 |  5 |  5 |
| Beedrill     |  3 | 32 |  7 |  7 |  7 |
| Pidgeotto    |  6 | 34 | 13 | 13 | 13 |
| Pidgeot      | 12 | 39 | 25 | 25 | 25 |
| Fearow       |  7 | 35 | 15 | 15 | 15 |
| Arbok        |  8 | 36 | 17 | 17 | 17 |
| Pikachu      |  6 | 34 | 13 | 13 | 13 |
| Raichu       | 10 | 37 | 21 | 21 | 21 |
| Sandslash    |  8 | 36 | 17 | 17 | 17 |
| Nidorina     |  6 | 34 | 13 | 13 | 13 |
| Nidoqueen    |  6 | 34 | 13 | 13 | 13 |
| Nidorino     |  6 | 34 | 13 | 13 | 13 |
| Nidoking     |  6 | 34 | 13 | 13 | 13 |
| Golbat       |  8 | 36 | 17 | 17 | 17 |
| Gloom        |  7 | 35 | 15 | 15 | 15 |
| Parasect     |  8 | 36 | 17 | 17 | 17 |
| Venomoth     | 11 | 38 | 23 | 23 | 23 |
| Dugtrio      |  9 | 36 | 19 | 19 | 19 |
| Persian      |  9 | 37 | 19 | 19 | 19 |
| Golduck      | 11 | 38 | 23 | 23 | 23 |
| Primeape     |  9 | 37 | 19 | 19 | 19 |
| Poliwhirl    |  8 | 36 | 17 | 17 | 17 |
| Kadabra      |  6 | 34 | 13 | 13 | 13 |
| Machop       |  3 |  3 |  3 |  3 |  3 |
| Machoke      |  9 | 37 | 19 | 19 | 19 |
| Weepinbell   |  7 | 35 | 15 | 15 | 15 |
| Tentacruel   | 10 | 37 | 21 | 21 | 21 |
| Rapidash     | 14 | 40 | 29 | 29 | 29 |
| Slowbro      | 13 | 40 | 27 | 27 | 27 |
| Magneton     | 10 | 37 | 21 | 21 | 21 |
| Dodrio       | 11 | 38 | 23 | 23 | 23 |
| Dewgong      | 12 | 39 | 25 | 25 | 25 |
| Muk          | 13 | 40 | 27 | 27 | 27 |
| Haunter      |  8 | 36 | 17 | 17 | 17 |
| Onix         |  6 | 34 | 13 | 13 | 13 |
| Hypno        |  9 | 36 | 19 | 19 | 19 |
| Kingler      |  9 | 37 | 19 | 19 | 19 |
| Electrode    | 10 | 37 | 21 | 21 | 21 |
| Marowak      |  9 | 37 | 19 | 19 | 19 |
| Lickitung    |  — | 34 | 13 | 13 | 13 |
| Weezing      | 12 | 39 | 25 | 25 | 25 |
| Rhyhorn      |  7 | 35 | 15 | 15 | 15 |
| Rhydon       | 15 | 41 | 31 | 31 | 31 |
| Chansey      | 14 | 34 | 25 | 25 | 25 |
| Kangaskhan   |  6 | 33 | 13 | 13 | 13 |
| Seadra       | 11 | 38 | 23 | 23 | 23 |
| Seaking      | 11 | 38 | 23 | 23 | 23 |
| Mr. Mime     |  6 | 34 | 13 | 13 | 13 |
| Scyther      |  6 | 34 | 13 | 13 | 13 |
| Jynx         |  6 | 34 | 13 | 13 | 13 |
| Electabuzz   |  6 | 34 | 13 | 13 | 13 |
| Magmar       |  6 | 34 | 13 | 13 | 13 |
| Pinsir       |  6 | 34 | 13 | 13 | 13 |
| Tauros       |  6 | 34 | 13 | 13 | 13 |
| Gyarados     |  8 | 35 | 20 | 20 | 20 |
| Lapras       | 15 | 34 | 25 | 25 | 25 |
| Ditto        | 12 | 12 | 21 | 21 | 21 |
| Snorlax      | 15 | 34 | 25 | 25 | 25 |
| Dratini      | 12 | 34 | 13 | 13 | 13 |
| Dragonair    | 16 | 37 | 25 | 25 | 25 |
| Dragonite    | 25 | 48 | 45 | 45 | 45 |
| Mareep       |  — | 32 | 10 | 10 | 10 |
| Flaaffy      |  — | 34 | 15 | 15 | 15 |
| Ampharos     |  — | 40 | 29 | 29 | 29 |
| Sudowoodo    |  — | 35 | 15 | 15 | 15 |
| Sunflora     |  — | 35 | 15 | 15 | 15 |
| Misdreavus   |  — | 33 | 10 | 10 | 10 |
| Pineco       |  — | 33 | 10 | 10 | 10 |
| Forretress   |  — | 39 | 25 | 25 | 25 |
| Gligar       |  — | 35 | 15 | 15 | 15 |
| Heracross    |  — | 35 | 15 | 15 | 15 |
| Sneasel      |  — | 33 | 10 | 10 | 10 |
| Corsola      |  — | 35 | 15 | 15 | 15 |
| Delibird     |  — | 32 | 10 | 10 | 10 |
| Mantine      |  — | 35 | 15 | 15 | 15 |
| Skarmory     |  — | 38 | 25 | 25 | 25 |
| Houndour     |  — |  — | 10 | 10 | 10 |
| Houndoom     |  — |  — | 20 | 20 | 20 |
| Stantler     |  — | 34 | 13 | 13 | 13 |
| Miltank      |  — | 34 | 13 | 13 | 13 |
| Larvitar     |  — |  — |  — | 13 | 13 |
| Pupitar      |  — |  — |  — | 25 | 25 |
| Tyranitar    |  — |  — |  — | 45 | 45 |
| Mightyena    |  — |  — | 13 | 13 | 13 |
| Linoone      |  — |  — | 15 | 15 | 15 |
| Silcoon      |  — |  — |  5 |  5 |  5 |
| Beautifly    |  — |  — |  7 |  7 |  7 |
| Cascoon      |  — |  — |  5 |  5 |  5 |
| Dustox       |  — |  — |  7 |  7 |  7 |
| Lombre       |  — |  — | 11 | 11 | 11 |
| Nuzleaf      |  — |  — | 11 | 11 | 11 |
| Swellow      |  — |  — | 17 | 17 | 17 |
| Pelipper     |  — |  — | 17 | 17 | 17 |
| Ralts        |  — |  — | 13 | 13 | 13 |
| Kirlia       |  — |  — | 17 | 17 | 17 |
| Gardevoir    |  — |  — | 30 | 30 | 30 |
| Masquerain   |  — |  — | 17 | 17 | 17 |
| Breloom      |  — |  — | 17 | 17 | 17 |
| Vigoroth     |  — |  — | 17 | 17 | 17 |
| Slaking      |  — |  — | 30 | 30 | 30 |
| Ninjask      |  — |  — | 15 | 15 | 15 |
| Whismur      |  — |  — |  7 |  7 |  7 |
| Loudred      |  — |  — | 15 | 15 | 15 |
| Exploud      |  — |  — | 29 | 29 | 29 |
| Makuhita     |  — |  — |  7 |  7 |  7 |
| Hariyama     |  — |  — | 17 | 17 | 17 |
| Aron         |  — |  — | 15 | 15 | 15 |
| Lairon       |  — |  — | 25 | 25 | 25 |
| Aggron       |  — |  — | 35 | 35 | 35 |
| Medicham     |  — |  — | 27 | 27 | 27 |
| Manectric    |  — |  — | 19 | 19 | 19 |
| Plusle       |  — |  — | 13 | 13 | 13 |
| Minun        |  — |  — | 13 | 13 | 13 |
| Swalot       |  — |  — | 19 | 19 | 19 |
| Carvanha     |  — |  — | 15 | 15 | 15 |
| Sharpedo     |  — |  — | 25 | 25 | 25 |
| Wailmer      |  — |  — | 15 | 15 | 15 |
| Wailord      |  — |  — | 30 | 30 | 30 |
| Camerupt     |  — |  — | 23 | 23 | 23 |
| Torkoal      |  — |  — | 10 | 10 | 10 |
| Spoink       |  — |  — | 10 | 10 | 10 |
| Grumpig      |  — |  — | 23 | 23 | 23 |
| Trapinch     |  — |  — | 15 | 15 | 15 |
| Vibrava      |  — |  — | 25 | 25 | 25 |
| Flygon       |  — |  — | 35 | 35 | 35 |
| Cacturne     |  — |  — | 23 | 23 | 23 |
| Altaria      |  — |  — | 25 | 25 | 25 |
| Zangoose     |  — |  — | 11 | 11 | 11 |
| Seviper      |  — |  — | 11 | 11 | 11 |
| Lunatone     |  — |  — | 12 | 12 | 12 |
| Solrock      |  — |  — | 12 | 12 | 12 |
| Whiscash     |  — |  — | 21 | 21 | 21 |
| Crawdaunt    |  — |  — | 21 | 21 | 21 |
| Claydol      |  — |  — | 25 | 25 | 25 |
| Feebas       |  — |  — | 10 | 10 | 10 |
| Kecleon      |  — |  — | 11 | 11 | 11 |
| Banette      |  — |  — | 27 | 27 | 27 |
| Duskull      |  — |  — | 11 | 11 | 11 |
| Dusclops     |  — |  — | 27 | 27 | 27 |
| Tropius      |  — |  — | 11 | 11 | 11 |
| Chimecho     |  — |  — | 11 | 11 | 11 |
| Absol        |  — |  — | 11 | 11 | 11 |
| Snorunt      |  — |  — | 13 | 13 | 13 |
| Glalie       |  — |  — | 31 | 31 | 31 |
| Sealeo       |  — |  — | 23 | 23 | 23 |
| Walrein      |  — |  — | 31 | 31 | 31 |
| Clamperl     |  — |  — | 15 | 15 | 15 |
| Relicanth    |  — |  — | 15 | 15 | 15 |
| Luvdisc      |  — |  — | 10 | 10 | 10 |
| Bagon        |  — |  — | 13 | 13 | 13 |
| Shelgon      |  — |  — | 25 | 25 | 25 |
| Salamence    |  — |  — | 45 | 45 | 45 |
| Beldum       |  — |  — | 13 | 13 | 13 |
| Metang       |  — |  — | 20 | 20 | 20 |
| Metagross    |  — |  — | 45 | 45 | 45 |
| Staravia     |  — |  — |  — | 13 | 13 |
| Staraptor    |  — |  — |  — | 25 | 25 |
| Bibarel      |  — |  — |  — | 15 | 15 |
| Luxio        |  — |  — |  — | 11 | 11 |
| Luxray       |  — |  — |  — | 35 | 35 |
| Purugly      |  — |  — |  — | 27 | 27 |
| Skuntank     |  — |  — |  — | 25 | 25 |
| Happiny      |  — |  — |  — | 25 | 25 |
| Gible        |  — |  — |  — | 13 | 13 |
| Gabite       |  — |  — |  — | 25 | 25 |
| Garchomp     |  — |  — |  — | 45 | 45 |
| Croagunk     |  — |  — |  — | 15 | 15 |
| Toxicroak    |  — |  — |  — | 15 | 15 |
| Herdier      |  — |  — |  — |  — | 13 |
| Stoutland    |  — |  — |  — |  — | 23 |
| Tranquill    |  — |  — |  — |  — | 13 |
| Unfezant     |  — |  — |  — |  — | 25 |
| Zebstrika    |  — |  — |  — |  — | 19 |
| Swoobat      |  — |  — |  — |  — | 23 |
| Drilbur      |  — |  — |  — |  — | 15 |
| Excadrill    |  — |  — |  — |  — | 23 |
| Audino       |  — |  — |  — |  — | 10 |
| Gurdurr      |  — |  — |  — |  — | 17 |
| Seismitoad   |  — |  — |  — |  — |  5 |
| Whirlipede   |  — |  — |  — |  — | 12 |
| Scolipede    |  — |  — |  — |  — | 25 |
| Sandile      |  — |  — |  — |  — |  8 |
| Krokorok     |  — |  — |  — |  — | 16 |
| Krookodile   |  — |  — |  — |  — | 24 |
| Crustle      |  — |  — |  — |  — | 25 |
| Scraggy      |  — |  — |  — |  — |  6 |
| Scrafty      |  — |  — |  — |  — | 12 |
| Yamask       |  — |  — |  — |  — | 12 |
| Cofagrigus   |  — |  — |  — |  — | 22 |
| Garbodor     |  — |  — |  — |  — | 25 |
| Zorua        |  — |  — |  — |  — | 12 |
| Zoroark      |  — |  — |  — |  — | 24 |
| Gothita      |  — |  — |  — |  — | 13 |
| Gothorita    |  — |  — |  — |  — | 17 |
| Gothitelle   |  — |  — |  — |  — | 30 |
| Deerling     |  — |  — |  — |  — |  4 |
| Sawsbuck     |  — |  — |  — |  — | 12 |
| Emolga       |  — |  — |  — |  — |  8 |
| Karrablast   |  — |  — |  — |  — | 11 |
| Foongus      |  — |  — |  — |  — |  8 |
| Amoonguss    |  — |  — |  — |  — | 14 |
| Jellicent    |  — |  — |  — |  — | 29 |
| Alomomola    |  — |  — |  — |  — | 12 |
| Ferroseed    |  — |  — |  — |  — | 10 |
| Ferrothorn   |  — |  — |  — |  — | 25 |
| Eelektrik    |  — |  — |  — |  — | 11 |
| Eelektross   |  — |  — |  — |  — | 35 |
| Beheeyem     |  — |  — |  — |  — | 25 |
| Lampent      |  — |  — |  — |  — | 18 |
| Chandelure   |  — |  — |  — |  — | 30 |
| Axew         |  — |  — |  — |  — | 15 |
| Fraxure      |  — |  — |  — |  — | 25 |
| Haxorus      |  — |  — |  — |  — | 45 |
| Cryogonal    |  — |  — |  — |  — | 15 |
| Mienshao     |  — |  — |  — |  — | 25 |
| Druddigon    |  — |  — |  — |  — | 18 |
| Golett       |  — |  — |  — |  — | 12 |
| Golurk       |  — |  — |  — |  — | 40 |
| Pawniard     |  — |  — |  — |  — | 15 |
| Bisharp      |  — |  — |  — |  — | 30 |
| Bouffalant   |  — |  — |  — |  — | 13 |
| Braviary     |  — |  — |  — |  — | 44 |
| Mandibuzz    |  — |  — |  — |  — | 44 |
| Heatmor      |  — |  — |  — |  — | 13 |
| Durant       |  — |  — |  — |  — | 15 |
| Deino        |  — |  — |  — |  — | 13 |
| Zweilous     |  — |  — |  — |  — | 25 |
| Hydreigon    |  — |  — |  — |  — | 45 |
| Larvesta     |  — |  — |  — |  — | 25 |
| Volcarona    |  — |  — |  — |  — | 45 |

## Pokémon that don't spawn wild

Across all five regions, **188 species have no positive wild spawn rate in any biome** — they're either evolution-only, starter-only, fossil revivals, gift Pokémon, event/legendary spawns, or otherwise locked behind a non-overworld system (gym rewards, tournament prizes, breeding). They will never appear from an ambient overworld wild encounter, regardless of Trainer Level.

That said, "doesn't spawn wild" doesn't mean "unobtainable in the wild." Many of the species below still show up semi-regularly through other systems — Safari Zone runs, Honey Trees, fishing, and similar mechanisms each have their own pools that draw from outside the standard biome spawn tables. If you're hunting one of these, check those systems before assuming it's locked to evolution or events.

<table>
<thead><tr><th colspan="4" style="text-align:center">Pokémon</th></tr></thead>
<tbody>
<tr><td>Bulbasaur</td><td>Igglybuff</td><td>Registeel</td><td>Dialga</td></tr>
<tr><td>Ivysaur</td><td>Togepi</td><td>Latias</td><td>Palkia</td></tr>
<tr><td>Venusaur</td><td>Togetic</td><td>Latios</td><td>Heatran</td></tr>
<tr><td>Charmander</td><td>Bellossom</td><td>Kyogre</td><td>Regigigas</td></tr>
<tr><td>Charmeleon</td><td>Politoed</td><td>Groudon</td><td>Giratina</td></tr>
<tr><td>Charizard</td><td>Espeon</td><td>Rayquaza</td><td>Cresselia</td></tr>
<tr><td>Squirtle</td><td>Umbreon</td><td>Jirachi</td><td>Phione</td></tr>
<tr><td>Wartortle</td><td>Slowking</td><td>Deoxys</td><td>Manaphy</td></tr>
<tr><td>Blastoise</td><td>Steelix</td><td>Turtwig</td><td>Darkrai</td></tr>
<tr><td>Ninetales</td><td>Scizor</td><td>Grotle</td><td>Shaymin</td></tr>
<tr><td>Vileplume</td><td>Kingdra</td><td>Torterra</td><td>Arceus</td></tr>
<tr><td>Arcanine</td><td>Porygon2</td><td>Chimchar</td><td>Victini</td></tr>
<tr><td>Poliwrath</td><td>Smoochum</td><td>Monferno</td><td>Snivy</td></tr>
<tr><td>Alakazam</td><td>Elekid</td><td>Infernape</td><td>Servine</td></tr>
<tr><td>Machamp</td><td>Magby</td><td>Piplup</td><td>Serperior</td></tr>
<tr><td>Victreebel</td><td>Blissey</td><td>Prinplup</td><td>Tepig</td></tr>
<tr><td>Golem</td><td>Raikou</td><td>Empoleon</td><td>Pignite</td></tr>
<tr><td>Cloyster</td><td>Entei</td><td>Roserade</td><td>Emboar</td></tr>
<tr><td>Gengar</td><td>Suicune</td><td>Cranidos</td><td>Oshawott</td></tr>
<tr><td>Exeggutor</td><td>Lugia</td><td>Rampardos</td><td>Dewott</td></tr>
<tr><td>Starmie</td><td>Ho-Oh</td><td>Shieldon</td><td>Samurott</td></tr>
<tr><td>Vaporeon</td><td>Celebi</td><td>Bastiodon</td><td>Pansage</td></tr>
<tr><td>Jolteon</td><td>Treecko</td><td>Ambipom</td><td>Simisage</td></tr>
<tr><td>Flareon</td><td>Grovyle</td><td>Mismagius</td><td>Pansear</td></tr>
<tr><td>Porygon</td><td>Sceptile</td><td>Honchkrow</td><td>Simisear</td></tr>
<tr><td>Omanyte</td><td>Torchic</td><td>Weavile</td><td>Panpour</td></tr>
<tr><td>Omastar</td><td>Combusken</td><td>Magnezone</td><td>Simipour</td></tr>
<tr><td>Kabuto</td><td>Blaziken</td><td>Lickilicky</td><td>Gigalith</td></tr>
<tr><td>Kabutops</td><td>Mudkip</td><td>Rhyperior</td><td>Conkeldurr</td></tr>
<tr><td>Aerodactyl</td><td>Marshtomp</td><td>Tangrowth</td><td>Tirtouga</td></tr>
<tr><td>Articuno</td><td>Swampert</td><td>Electivire</td><td>Carracosta</td></tr>
<tr><td>Zapdos</td><td>Ludicolo</td><td>Magmortar</td><td>Archen</td></tr>
<tr><td>Moltres</td><td>Shiftry</td><td>Togekiss</td><td>Archeops</td></tr>
<tr><td>Mewtwo</td><td>Shedinja</td><td>Yanmega</td><td>Escavalier</td></tr>
<tr><td>Mew</td><td>Azurill</td><td>Leafeon</td><td>Accelgor</td></tr>
<tr><td>Chikorita</td><td>Delcatty</td><td>Glaceon</td><td>Cobalion</td></tr>
<tr><td>Bayleef</td><td>Lileep</td><td>Gliscor</td><td>Terrakion</td></tr>
<tr><td>Meganium</td><td>Cradily</td><td>Mamoswine</td><td>Virizion</td></tr>
<tr><td>Cyndaquil</td><td>Anorith</td><td>Porygon-Z</td><td>Tornadus</td></tr>
<tr><td>Quilava</td><td>Armaldo</td><td>Gallade</td><td>Thundurus</td></tr>
<tr><td>Typhlosion</td><td>Milotic</td><td>Probopass</td><td>Reshiram</td></tr>
<tr><td>Totodile</td><td>Castform</td><td>Dusknoir</td><td>Zekrom</td></tr>
<tr><td>Croconaw</td><td>Wynaut</td><td>Froslass</td><td>Landorus</td></tr>
<tr><td>Feraligatr</td><td>Huntail</td><td>Rotom</td><td>Kyurem</td></tr>
<tr><td>Crobat</td><td>Groebyss</td><td>Uxie</td><td>Keldeo</td></tr>
<tr><td>Pichu</td><td>Regirock</td><td>Mesprit</td><td>Meloetta</td></tr>
<tr><td>Cleffa</td><td>Regice</td><td>Azelf</td><td>Genesect</td></tr>
</tbody>
</table>

## Practical takeaways

- **Battle constantly in early gens.** Until you've banked enough TL, half the dex literally won't appear.
- **Always push for the next badge in Gen 3+.** The badge gate is the most common reason your XP bar appears stuck.
- **Plan trades around the receiving player's TL** — the wild-cap table that gates trading is the same table that gates your encounters, so a low-TL friend can't accept high-level trades even if their save has the species. See the [Trading page](/mechanics/trading/) for the full per-TL cap.
- **Late-region grinds happen at TL 25 and TL 45 (Gen 3 / 4 / 5)** — those are the two biggest unlock waves; if you're missing rare spawns from those gens, check whether you've crossed both thresholds.
