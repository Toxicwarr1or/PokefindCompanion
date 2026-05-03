#!/usr/bin/env python3
"""Build per-item pages under content/items/<slug>.md.

Architecture
------------
ITEMS holds the hand-curated payload for each item — slug, display name,
category, effect / boost summary, description, holder requirements. Items
that should NOT have a page (e.g. they're truly admin-only and have no
description worth surfacing) just don't get an entry here.

`find_quest_rewards(item_name)` scans `~/Desktop/quests/*.json` for
`GiveItem` stages mentioning the item by name and emits a "Quest reward:
<quest>" line per matching quest. Quest IDs are pretty-printed from
their filenames; we don't currently dive into the script to surface
*which step* of the quest hands the item out — that's possible (the
GiveItem call's surrounding If / Comment / step keys carry it) but
isn't free, so we keep it shallow until per-step accuracy matters.

`find_shop_sources(item_name)` scans the PokemonWorld + PokefindCore
script trees for shop scripts that sell the item. Only matches in
folders containing `shop` in the path are surfaced, to avoid false
positives from NPC battle teams that hold the item.

Re-run idempotently. Adding new items just means appending to ITEMS.

Usage
-----
    python3 scripts/build_item_pages.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

REPO        = Path(__file__).resolve().parent.parent
# Single canonical quest tree — `~/Desktop/quests/` holds every quest
# for gens 1–5 (top-level files are cross-gen / utility scripts; per-gen
# subdirs `gen1/` … `gen5/` hold the main-quest, iconic, gym, and
# Shadow Quest (sq*) JSONs). Scanned recursively so all gen subdirs are
# walked. Seasonal / event quests inside this tree are filtered out by
# `_is_seasonal()` so only year-round permanent rewards surface.
QUEST_SOURCE_DIRS = [
    Path.home() / "Desktop/quests",
]
BATTLE_TOWER_SHOP_JAVA = (Path.home()
    / "ClaudeProjects/PokemonWorld-master/pokemon-world/src/main/java"
    / "co/pokefind/pokemon/battletower/menu/BattleTowerShopMenu.java")
OUT_DIR = REPO / "content/items"

# Filename tokens that mark a quest as "really a shop / vendor / sale"
# rather than a reward-paying quest. Used to relabel the surfaced source
# from "Quest reward" → "Shop" so the user can tell at a glance whether
# the item costs coins or comes free.
SHOP_NAME_TOKENS = ("shop", "mart", "vendor", "store", "sale", "roulette")

# Seasonal / event shops are excluded from the wiki's "Where to find"
# list — they're time-limited and confuse the year-round availability
# picture. Filename or path tokens listed here trigger an unconditional
# skip during quest scanning. Items that should still credit the
# permanent shops (Challenge / Wish / Premium / Battle Tower) get those
# entries from MANUAL_SHOP_SOURCES + parse_battle_tower_shop() instead.
SEASONAL_TOKENS = (
    # Holiday events
    "christmas", "xmas", "halloween", "hw22", "hw24", "hw25",
    "easter", "summer", "surfing", "thanksgiving", "cornucopia",
    "valentine", "lunar",
    # Halloween rebrand for the PMMO collab
    "trickotreat",
    # PMMO spring event — match on `showdown` so legitimate quests like
    # `gen3-honey-spring*` aren't falsely tagged as seasonal.
    "showdown",
    # Anniversary / 12 Days of Christmas content
    "anniversary", "annisale", "annigems", "12days", "day12gems",
    "day10gems", "day11gems", "day11hat",
    # Black Friday + summer-sub-events
    "blackfriday", "summer_event",
)

# Path-fragment exclusions on top of the seasonal filter. The match is
# substring-on-the-posix-path of each candidate quest file, so anchoring
# the fragment with a directory segment (e.g. `gen4/mcrate-`) is what
# scopes a rule to a single gen.
#
#   gen4/mcrate-      — Gen 4 monthly crates (Mcrate Enigma, Berries1,
#                       Consumables1/2, Currency1/2, Hatcher1). User
#                       requested these be excluded; equivalent crates
#                       in other gens stay in.
#   gen4/cm-suppmain  — Gen 4 "CM Suppmain" rewards script; tagged for
#                       removal alongside the gen4 crates.
EXCLUDED_PATH_FRAGMENTS = (
    "gen4/mcrate-",
    "gen4/cm-suppmain",
)

# Hand-curated permanent shop sources for items the source code shows
# are sold across the always-available shop trio (TrainerManager.java
# bottom block — Challenge Shop "csm" + Wish Shop "vsm"). Premium
# /store is the cash-shop tier exposed via the in-game `/store` command;
# we surface it as a third bullet for the user-named items.
#
# Confirmed against PokemonWorld-master/.../trainer/TrainerManager.java
# 2026-05-03:
#   vsm.add(new PokemonShopItem(Item.RARE_CANDY,    4));
#   vsm.add(new PokemonShopItem(Item.LUCKY_EGG,     20));
#   vsm.add(new PokemonShopItem(Item.EXP_SHARE,     84), 2, -1);
#   vsm.add(new PokemonShopItem(Item.SHINY_CHARM,   210), -1, 604800);
#   csm.add(new PokemonShopItem(Item.RARE_CANDY,    3));
#   csm.add(new PokemonShopItem(Item.LUCKY_EGG,     2));
#   csm.add(new PokemonShopItem(Item.EXP_SHARE,     84), 2, -1);
#   csm.add(new PokemonShopItem(Item.SHINY_CHARM,   42), -1, 604800);
#   csm.add(new PokemonShopItem(Item.XP_BOOST_ELIXIR, 42), -1, 604800);
# (XP Boost Elixir is intentionally Wish-Shop-absent.)
MANUAL_SHOP_SOURCES: dict[str, list[str]] = {
    "Exp. Share":         ["Shop: **Challenge Shop** (84 ⛀, limit 2)",
                           "Shop: **Wish Shop** (84 ✨, limit 2)",
                           "Shop: **Premium /store**"],
    "Lucky Egg":          ["Shop: **Challenge Shop** (2 ⛀)",
                           "Shop: **Wish Shop** (20 ✨)",
                           "Shop: **Premium /store**"],
    "Rare Candy":         ["Shop: **Challenge Shop** (3 ⛀)",
                           "Shop: **Wish Shop** (4 ✨)",
                           "Shop: **Premium /store**"],
    "Shiny Charm":        ["Shop: **Challenge Shop** (42 ⛀, weekly)",
                           "Shop: **Wish Shop** (210 ✨, weekly)",
                           "Shop: **Premium /store**"],
    "XP Boost Elixir":    ["Shop: **Challenge Shop** (42 ⛀, weekly)",
                           "Shop: **Premium /store**"],

    # Aunty Alma — recurring NPC who sells the six EV-lowering berries
    # at 4 000 coins each. Confirmed via the gen-4 shop script
    # (`aunty-alma.json` ShopMenu); the same NPC ships in gens 1–5 so
    # the wiki credits her once across all five regions.
    "Pomeg Berry":   ["Shop: **Aunty Alma's Shop** (4 000 coins; gen 1–5)"],
    "Kelpsy Berry":  ["Shop: **Aunty Alma's Shop** (4 000 coins; gen 1–5)"],
    "Qualot Berry":  ["Shop: **Aunty Alma's Shop** (4 000 coins; gen 1–5)"],
    "Hondew Berry":  ["Shop: **Aunty Alma's Shop** (4 000 coins; gen 1–5)"],
    "Grepa Berry":   ["Shop: **Aunty Alma's Shop** (4 000 coins; gen 1–5)"],
    "Tamato Berry":  ["Shop: **Aunty Alma's Shop** (4 000 coins; gen 1–5)"],
}


# ---------------------------------------------------------------------------
# Seed data — first wave of 12 items spanning every category on the items
# index page. Keep boost / effect text terse and factual; descriptions can
# stretch a sentence or two for context. `holder` is for species-locked
# items; `consumed` is for one-shot berries / herbs / sashes.
# ---------------------------------------------------------------------------

def _type_booster(slug, name, type_name):
    """Convenience builder for the 20+ "boosts type X moves by 1.2×" items."""
    return {
        "slug": slug,
        "name": name,
        "category": "Type-boosting",
        "boost": f"Multiplies {type_name}-type move power by 1.2× (+20%).",
        "description": (f"{name} boosts the power of every {type_name}-type move the holder uses — "
                        f"a flat ×1.2 multiplier on move base power. STAB-only in spirit (the move "
                        f"must be {type_name}-type), but the holder isn't required to share the type."),
    }


def _arceus_plate(slug, name, type_name):
    """The 17 elemental Plates — same numbers as the type-boosters, plus
    the Arceus type-change."""
    return {
        "slug": slug,
        "name": name,
        "category": "Arceus Plate",
        "boost": f"Multiplies {type_name}-type move power by 1.2× (+20%); changes Arceus's type to {type_name} via Multitype.",
        "description": (f"One of the seventeen elemental Plates. Held by Arceus, the {name} switches its type to "
                        f"{type_name}. Held by anything else, it boosts {type_name}-type moves by ×1.2 — same "
                        f"numbers as the standard type-boosters, just packaged as a stone tablet."),
    }


def _resist_berry(slug, name, type_name):
    """One-shot type-resist berries — halve a single super-effective hit
    of the matching type."""
    return {
        "slug": slug,
        "name": name,
        "category": "Type-resist berry",
        "boost": f"Halves the damage of one super-effective {type_name}-type attack.",
        "description": (f"{name} cuts the damage of a single super-effective {type_name}-type hit in half, then "
                        f"is consumed. Most useful on Pokémon with a 4× weakness to {type_name} (Earth-type "
                        f"berries on Steel + Rock holders, etc.) where halving the damage can flip a one-shot "
                        f"into a two-shot."),
        "consumed": "Yes — eaten on the matching super-effective hit.",
    }


def _status_cure_berry(slug, name, status_name):
    return {
        "slug": slug,
        "name": name,
        "category": "Status-cure berry",
        "boost": f"Cures the holder's {status_name} the moment it triggers.",
        "description": (f"Single-use status patch. The moment the holder is afflicted with {status_name}, "
                        f"the {name} is consumed and the status is cleared. Useful on setup sweepers that "
                        f"can't afford to lose a turn to the matching ailment on the way in."),
        "consumed": f"Yes — eaten when {status_name} applies.",
    }


def _ev_lower_berry(slug, name, stat_name, friendship=True):
    extra = " Also raises friendship." if friendship else ""
    return {
        "slug": slug,
        "name": name,
        "category": "EV-lowering berry",
        "boost": f"Lowers the holder's {stat_name} EVs by 10 (down to a minimum of 0).{extra}",
        "description": (f"Used outside battle: feeding {name} to a Pokémon trims its {stat_name} EVs back, "
                        f"useful when correcting a botched EV spread without a full reset. Repeatable "
                        f"until the EV total in that stat reaches 0."),
    }


ITEMS: list[dict] = [
    # =====================================================================
    # Type-boosting items — all share the ×1.2 multiplier on their type.
    # =====================================================================
    _type_booster("silk-scarf",      "Silk Scarf",      "Normal"),
    {
        "slug": "charcoal",
        "name": "Charcoal",
        "category": "Type-boosting",
        "boost": "Multiplies Fire-type move power by 1.2× (+20%).",
        "description": ("Charcoal boosts the power of every Fire-type move the holder uses — a flat ×1.2 multiplier "
                        "on the move's base power. Pairs cleanly with single-type Fire attackers that don't need a "
                        "Choice item's lock-in. STAB-only — the move must be Fire-type, but the holder doesn't "
                        "have to be."),
    },
    _type_booster("mystic-water",    "Mystic Water",    "Water"),
    _type_booster("sea-incense",     "Sea Incense",     "Water"),
    _type_booster("wave-incense",    "Wave Incense",    "Water"),
    _type_booster("magnet",          "Magnet",          "Electric"),
    _type_booster("miracle-seed",    "Miracle Seed",    "Grass"),
    _type_booster("rose-incense",    "Rose Incense",    "Grass"),
    _type_booster("never-melt-ice",  "Never-Melt Ice",  "Ice"),
    _type_booster("black-belt",      "Black Belt",      "Fighting"),
    _type_booster("poison-barb",     "Poison Barb",     "Poison"),
    _type_booster("soft-sand",       "Soft Sand",       "Ground"),
    _type_booster("sharp-beak",      "Sharp Beak",      "Flying"),
    _type_booster("twisted-spoon",   "Twisted Spoon",   "Psychic"),
    _type_booster("odd-incense",     "Odd Incense",     "Psychic"),
    _type_booster("silver-powder",   "Silver Powder",   "Bug"),
    _type_booster("hard-stone",      "Hard Stone",      "Rock"),
    _type_booster("rock-incense",    "Rock Incense",    "Rock"),
    _type_booster("spell-tag",       "Spell Tag",       "Ghost"),
    _type_booster("dragon-fang",     "Dragon Fang",     "Dragon"),
    _type_booster("black-glasses",   "Black Glasses",   "Dark"),
    _type_booster("metal-coat",      "Metal Coat",      "Steel"),

    # =====================================================================
    # Arceus Plates — type-boost mirror with the Arceus type-change kicker.
    # =====================================================================
    _arceus_plate("draco-plate",   "Draco Plate",   "Dragon"),
    _arceus_plate("dread-plate",   "Dread Plate",   "Dark"),
    _arceus_plate("earth-plate",   "Earth Plate",   "Ground"),
    _arceus_plate("fist-plate",    "Fist Plate",    "Fighting"),
    {
        "slug": "flame-plate",
        "name": "Flame Plate",
        "category": "Arceus Plate",
        "boost": "Multiplies Fire-type move power by 1.2× (+20%); also changes Arceus's type to Fire.",
        "description": ("One of the seventeen elemental Plates. Held by Arceus, the Flame Plate switches its type to Fire "
                        "(Multitype activates the swap). Held by anything else, it functions as a Fire-type damage booster — "
                        "identical numbers to Charcoal (×1.2 power on Fire moves) — without the Arceus type-change."),
    },
    _arceus_plate("icicle-plate",  "Icicle Plate",  "Ice"),
    _arceus_plate("insect-plate",  "Insect Plate",  "Bug"),
    _arceus_plate("iron-plate",    "Iron Plate",    "Steel"),
    _arceus_plate("meadow-plate",  "Meadow Plate",  "Grass"),
    _arceus_plate("mind-plate",    "Mind Plate",    "Psychic"),
    _arceus_plate("pixie-plate",   "Pixie Plate",   "Fairy"),
    _arceus_plate("sky-plate",     "Sky Plate",     "Flying"),
    _arceus_plate("splash-plate",  "Splash Plate",  "Water"),
    _arceus_plate("spooky-plate",  "Spooky Plate",  "Ghost"),
    _arceus_plate("stone-plate",   "Stone Plate",   "Rock"),
    _arceus_plate("toxic-plate",   "Toxic Plate",   "Poison"),
    _arceus_plate("zap-plate",     "Zap Plate",     "Electric"),
    # =====================================================================
    # Choice items — all three lock moves; differ only in which stat scales.
    # =====================================================================
    {
        "slug": "choice-band",
        "name": "Choice Band",
        "category": "Choice item",
        "boost": "Multiplies Attack by 1.5× (+50%). The holder is locked into the first move it uses until it switches out.",
        "description": ("Choice Band turns a physical attacker into a one-shot wrecking ball. The ×1.5 Attack boost is one "
                        "of the biggest single-stat buffs in the game; the cost is move-lock — once you click Earthquake, "
                        "Earthquake is your only option until the holder leaves the field. Best on Pokémon with strong "
                        "STAB coverage or partners that can pivot it out (U-turn, Volt Switch, Baton Pass)."),
    },
    {
        "slug": "choice-specs",
        "name": "Choice Specs",
        "category": "Choice item",
        "boost": "Multiplies Special Attack by 1.5× (+50%). The holder is locked into the first move it uses until it switches out.",
        "description": ("The special-attacker counterpart to Choice Band: ×1.5 Special Attack, same move-lock penalty. "
                        "Mainstay item on glass-cannon special wallbreakers like Latios, Hydreigon, and Volcarona — anything "
                        "whose strongest STAB will one-shot the wall in front of it."),
    },
    {
        "slug": "choice-scarf",
        "name": "Choice Scarf",
        "category": "Choice item",
        "boost": "Multiplies Speed by 1.5× (+50%). The holder is locked into the first move it uses until it switches out.",
        "description": ("Speed control in item form. ×1.5 Speed flips most relevant matchups in the holder's favour — a "
                        "Modest Hydreigon goes from outrun by Garchomp to outspeeding it by 6 — at the cost of being "
                        "stuck on whichever attack was clicked first. Best on revenge killers and lead-cleaning sweepers."),
    },
    # =====================================================================
    # Damage modifiers — flat % power / defense changes outside of Choice.
    # =====================================================================
    {
        "slug": "life-orb",
        "name": "Life Orb",
        "category": "Damage modifier",
        "boost": "Multiplies attacking-move damage by 5324/4096 (≈1.30, +30%); the holder takes ~10% max-HP recoil on each successful hit.",
        "description": ("Life Orb is the universal damage-amp: no type restriction, no move-lock, no situational gate — just "
                        "raw ×1.30 damage on every attacking move (the 5324/4096 fixed-point multiplier you'll find in the "
                        "source). The HP recoil adds up quickly on multi-turn sweepers (~30% HP lost over three hits), so "
                        "it's best on Pokémon that either hit hard enough to one-shot threats or have a reliable recovery / "
                        "U-turn pivot. Magic Guard and Sheer Force holders skip the recoil entirely."),
    },
    {
        "slug": "expert-belt",
        "name": "Expert Belt",
        "category": "Damage modifier",
        "boost": "Multiplies super-effective move damage by 1.2× (+20%). No effect on neutral / resisted hits.",
        "description": ("The coverage-attacker's signature item. Expert Belt rewards predicting your opponent's switch by "
                        "boosting only the hits that already do extra damage. No HP cost, no move-lock — just a quieter "
                        "+20% on the moves that matter. Falls behind Life Orb when the holder mostly clicks STAB into "
                        "neutral targets."),
    },
    {
        "slug": "muscle-band",
        "name": "Muscle Band",
        "category": "Damage modifier",
        "boost": "Multiplies physical move power by 1.1× (+10%).",
        "description": ("A subtle physical-side power boost — half a Life Orb without the recoil and without locking moves. "
                        "Niche pick on Pokémon that don't want a Choice Band but still want a slight damage edge."),
    },
    {
        "slug": "wise-glasses",
        "name": "Wise Glasses",
        "category": "Damage modifier",
        "boost": "Multiplies special move power by 1.1× (+10%).",
        "description": ("Special-attacker mirror of Muscle Band. Same caveat — the +10% is small, and Choice Specs / "
                        "Life Orb usually win out unless you specifically need to keep flexibility."),
    },
    {
        "slug": "assault-vest",
        "name": "Assault Vest",
        "category": "Damage modifier",
        "boost": "Multiplies Special Defense by 1.5× (+50%); the holder cannot use status moves.",
        "description": ("Defensive item with offensive intent: a special tank that still hits hard. Common on Pokémon "
                        "with high HP / decent base SpD that want to absorb special hits while pressuring back — "
                        "Conkeldurr, Slaking, Tornadus-Therian, Magearna. The status-move ban is the trap; Recover, "
                        "Roost, and Toxic are all off the table."),
    },
    {
        "slug": "eviolite",
        "name": "Eviolite",
        "category": "Damage modifier",
        "boost": "Multiplies BOTH Defense and Special Defense by 1.5× (+50%) — only on Pokémon that can still evolve.",
        "description": ("Pre-evolutions with Eviolite often out-bulk their fully-evolved forms. Applies a ×1.5 boost "
                        "to both Defense and Special Defense, gated on the holder still having an evolution available. "
                        "Canonical wearers: Chansey, Porygon2, Dusclops, Doublade, Scyther, Type: Null."),
        "holder": "Pokémon with at least one further evolution.",
    },
    # =====================================================================
    # One-time safety nets — single-trigger insurance items.
    # =====================================================================
    {
        "slug": "focus-sash",
        "name": "Focus Sash",
        "category": "One-time safety net",
        "boost": "Survives a one-shot KO at 1 HP — but only when the holder was at full HP when the hit landed.",
        "description": ("The classic suicide-lead insurance policy. Focus Sash guarantees the holder survives any single hit "
                        "that would otherwise KO it (including critical hits and one-shot moves), provided it was at full HP "
                        "when the attack connected. Disabled by passive damage (Stealth Rock, Sandstorm, Spikes), so leads "
                        "with a Sash usually want hazard control or a fast pivot."),
        "consumed": "Yes — disappears after the save.",
    },
    {
        "slug": "focus-band",
        "name": "Focus Band",
        "category": "One-time safety net",
        "boost": "Random chance to survive a one-shot KO at 1 HP, even from less-than-full HP. Less reliable than Focus Sash.",
        "description": ("Focus Sash's stochastic cousin. Each hit that would knock out the holder rolls a small chance to "
                        "leave it on 1 HP instead. Doesn't require full HP, so it can save the holder repeatedly — but the "
                        "low odds make it a curiosity item for trainers who want chaos over consistency."),
    },
    {
        "slug": "air-balloon",
        "name": "Air Balloon",
        "category": "One-time safety net",
        "boost": "The holder is treated as Flying-type for Ground-immunity purposes until the balloon pops on the first move that hits.",
        "description": ("Air Balloon is short-term Levitate: any incoming attack pops the balloon, but until then the "
                        "holder ignores Ground-type moves entirely. Common on Steel + Rock types that hate Earthquake "
                        "spam — Magnezone, Excadrill, Bisharp — and on setup sweepers that want one extra free turn."),
        "consumed": "Yes — pops on the first move the holder is hit by.",
    },
    {
        "slug": "mental-herb",
        "name": "Mental Herb",
        "category": "One-time safety net",
        "boost": "Single-use cure for move-binding effects — Taunt, Encore, Disable, Attract, Heal Block, Torment.",
        "description": ("A pre-emptive protect against the locking effects that shut down setup. The herb is consumed the "
                        "instant any matching status hits, restoring the holder's ability to use whatever set of moves "
                        "the lock would have forbidden."),
        "consumed": "Yes — eaten when the matching status applies.",
    },
    {
        "slug": "power-herb",
        "name": "Power Herb",
        "category": "One-time safety net",
        "boost": "Lets the holder execute a charge move (Solar Beam, Sky Attack, Geomancy, etc.) in a single turn instead of two.",
        "description": ("Bypasses the charge turn on slow two-turn moves — most famously turns Geomancy from setup-fodder "
                        "into a one-turn +2/+2/+2 sweep. Single-use, but the swing in tempo is enormous when the move "
                        "in question would otherwise be too slow to be worth running."),
        "consumed": "Yes — eaten on the charge-skipping move.",
    },
    {
        "slug": "white-herb",
        "name": "White Herb",
        "category": "One-time safety net",
        "boost": "Restores any stat the holder had lowered, single-use.",
        "description": ("Resets any stat-drop the holder is currently sitting on. Best on Pokémon that voluntarily "
                        "lower their own stats with moves like Overheat, Leaf Storm, or Shell Smash — burn the herb on "
                        "the first big hit, keep the offensive boost, and settle into a clean stat line."),
        "consumed": "Yes — eaten the moment any stat is below baseline.",
    },
    # =====================================================================
    # Recovery & passive HP — turn-tick heals and HP-stealing modifiers.
    # =====================================================================
    {
        "slug": "leftovers",
        "name": "Leftovers",
        "category": "Recovery & passive HP",
        "boost": "Restores 1/16 of the holder's max HP at the end of each turn.",
        "description": ("The default tank item: passive recovery on every Pokémon, every turn, no setup. Stacks neatly with "
                        "Toxic stalling, Substitute chip, and weather-damage offsets. Black Sludge does the same thing for "
                        "Poison types (and damages every other holder), but Leftovers is universal."),
    },
    {
        "slug": "black-sludge",
        "name": "Black Sludge",
        "category": "Recovery & passive HP",
        "boost": "On Poison types: restores 1/16 max HP per turn. On every other type: deals 1/8 max HP damage per turn.",
        "description": ("Leftovers for Poison types — and a slow execution for everything else. Common on Toxapex, "
                        "Crobat, Tentacruel; pairs with Toxic stalling and bulky pivots that don't mind the chip."),
        "holder": "Best on Poison types — damages all other holders.",
    },
    {
        "slug": "big-root",
        "name": "Big Root",
        "category": "Recovery & passive HP",
        "boost": "Increases HP recovered by HP-stealing moves (Giga Drain, Drain Punch, Leech Seed, Horn Leech) by 30%.",
        "description": ("A dedicated drain-build item. Every life-stealing move heals more — particularly noticeable on "
                        "Drain Punch Conkeldurr, Giga Drain Roserade, and Leech Seed Whimsicott."),
    },
    {
        "slug": "sitrus-berry",
        "name": "Sitrus Berry",
        "category": "Recovery & passive HP",
        "boost": "Restores 1/4 of the holder's max HP once when its HP drops to 1/2 or below.",
        "description": ("Bigger emergency heal than Oran. Confirmed in source: triggers when HP ≤ ½ max, restores ¼ of "
                        "max HP. Used on bulky setup sweepers that want one HP cushion to start the boost chain — "
                        "Belly Drum users in particular love it for the post-Drum recovery."),
        "consumed": "Yes — single trigger.",
    },
    {
        "slug": "oran-berry",
        "name": "Oran Berry",
        "category": "Recovery & passive HP",
        "boost": "Restores 10 HP once when the holder's HP drops to 1/2 or below.",
        "description": ("The quieter sibling of Sitrus — flat 10 HP heal at the same ½-HP trigger. Mostly relevant in "
                        "low-level / breeding contexts where 10 HP is meaningful; at competitive levels Sitrus's "
                        "percentage scaling wins."),
        "consumed": "Yes — single trigger.",
    },
    # =====================================================================
    # Status orbs — self-applied conditions that synergize with abilities.
    # =====================================================================
    {
        "slug": "toxic-orb",
        "name": "Toxic Orb",
        "category": "Status orb",
        "boost": "Self-inflicts Toxic poison on the holder at the end of the second turn.",
        "description": ("Pure utility: badly poisons the holder so abilities like Poison Heal (Gliscor, Breloom) flip the "
                        "damage tick into a +1/8 HP heal, or Toxic Boost / Guts cash in the status for an Attack boost. The "
                        "delayed activation lets a sleeper turn-1 attack uninterrupted before the orb kicks in."),
    },
    {
        "slug": "flame-orb",
        "name": "Flame Orb",
        "category": "Status orb",
        "boost": "Self-inflicts Burn on the holder at the end of the second turn.",
        "description": ("Burn is a damage-tick + Attack drop in one — devastating on most holders, but a feature when "
                        "combined with Guts (Conkeldurr, Swellow), Flare Boost (Volcarona pre-Mega), or Magic Guard. "
                        "Same delayed activation as Toxic Orb, so a turn-1 attack still goes off cleanly."),
    },
    # =====================================================================
    # Status-cure berries — single-use auto-clear of one specific status.
    # Lum is the catch-all; the rest are status-specific.
    # =====================================================================
    _status_cure_berry("cheri-berry",  "Cheri Berry",  "Paralysis"),
    _status_cure_berry("chesto-berry", "Chesto Berry", "Sleep"),
    _status_cure_berry("pecha-berry",  "Pecha Berry",  "Poison"),
    _status_cure_berry("rawst-berry",  "Rawst Berry",  "Burn"),
    _status_cure_berry("aspear-berry", "Aspear Berry", "Freeze"),
    _status_cure_berry("persim-berry", "Persim Berry", "Confusion"),
    {
        "slug": "lum-berry",
        "name": "Lum Berry",
        "category": "Status-cure berry",
        "boost": "Cures any major status condition (paralysis, sleep, poison, burn, freeze, confusion) the moment it triggers.",
        "description": ("The catch-all status berry — a single-use insurance policy against the entire major-status list. "
                        "Often paired with setup sweepers (Dragon Dance, Calm Mind) that can't afford to lose a turn to "
                        "Will-O-Wisp or Thunder Wave on the way in."),
        "consumed": "Yes — eaten the moment status applies.",
    },

    # =====================================================================
    # Type-resist berries — halve one super-effective hit, then consumed.
    # =====================================================================
    _resist_berry("occa-berry",   "Occa Berry",   "Fire"),
    _resist_berry("passho-berry", "Passho Berry", "Water"),
    _resist_berry("wacan-berry",  "Wacan Berry",  "Electric"),
    _resist_berry("rindo-berry",  "Rindo Berry",  "Grass"),
    _resist_berry("yache-berry",  "Yache Berry",  "Ice"),
    _resist_berry("chople-berry", "Chople Berry", "Fighting"),
    _resist_berry("kebia-berry",  "Kebia Berry",  "Poison"),
    _resist_berry("shuca-berry",  "Shuca Berry",  "Ground"),
    _resist_berry("coba-berry",   "Coba Berry",   "Flying"),
    _resist_berry("payapa-berry", "Payapa Berry", "Psychic"),
    _resist_berry("tanga-berry",  "Tanga Berry",  "Bug"),
    _resist_berry("charti-berry", "Charti Berry", "Rock"),
    _resist_berry("kasib-berry",  "Kasib Berry",  "Ghost"),
    _resist_berry("haban-berry",  "Haban Berry",  "Dragon"),
    _resist_berry("colbur-berry", "Colbur Berry", "Dark"),
    _resist_berry("babiri-berry", "Babiri Berry", "Steel"),
    _resist_berry("chilan-berry", "Chilan Berry", "Normal"),
    _resist_berry("roseli-berry", "Roseli Berry", "Fairy"),
    # =====================================================================
    # Switch & escape — pivot tools.
    # =====================================================================
    {
        "slug": "eject-button",
        "name": "Eject Button",
        "category": "Switch & escape",
        "boost": "Triggers a free switch the moment the holder is hit by an attacking move.",
        "description": ("Reactive momentum tool. As soon as the holder takes an attacking hit, it's pulled back to the bench "
                        "and the player picks a replacement — the attacker doesn't get to move again. Useful on bulky pivots "
                        "that want to scout an opposing move or set up a slower partner."),
        "consumed": "Yes — single-use; the button breaks after triggering.",
    },
    {
        "slug": "red-card",
        "name": "Red Card",
        "category": "Switch & escape",
        "boost": "When the holder is hit by an attack, the *attacker* is forced out and replaced randomly.",
        "description": ("Eject Button's mirror: instead of pulling the holder back, Red Card sends the opponent off the "
                        "field and swaps in a random opposing party member. Brutal against setup sweepers — Dragon Dance "
                        "boosts evaporate when Salamence is forced out — and a great hazard-spam enabler when the new "
                        "switch-in eats Stealth Rock damage."),
        "consumed": "Yes — single-use.",
    },
    {
        "slug": "shed-shell",
        "name": "Shed Shell",
        "category": "Switch & escape",
        "boost": "Lets the holder switch out unconditionally, even when trapped by Mean Look, Shadow Tag, Arena Trap, or Magnet Pull.",
        "description": ("The trap-break-out item. Mostly seen on Pokémon that lose 1-on-1 to a notorious trapper — Heatran "
                        "with Shed Shell to escape opposing Magnezones, Latios with Shed Shell vs. Tyranitar's Pursuit. "
                        "Trades the actual battle item for an emergency escape hatch."),
    },

    # =====================================================================
    # Accuracy / crit modifiers.
    # =====================================================================
    {
        "slug": "scope-lens",
        "name": "Scope Lens",
        "category": "Accuracy / crit",
        "boost": "Boosts the holder's critical-hit ratio by one stage.",
        "description": ("Slot-machine damage on every attack. With Scope Lens, the holder lands a critical hit on roughly "
                        "1/8 of attacks (one stage above baseline), which combos cleanly with high-crit moves like "
                        "Stone Edge, Cross Chop, or Night Slash for a sky-high effective crit rate."),
    },
    {
        "slug": "wide-lens",
        "name": "Wide Lens",
        "category": "Accuracy / crit",
        "boost": "Multiplies the holder's move accuracy by 1.1× (+10%).",
        "description": ("Reliability item: turns 90% accuracy moves into ~99% (capped at 100), 80% moves into ~88%, etc. "
                        "Most useful on Pokémon clicking Fire Blast / Hydro Pump / Stone Edge — moves whose miss-rate is "
                        "the only thing standing between the user and a clean two-hit OHKO."),
    },
    # =====================================================================
    # Species-specific — useless on the wrong holder.
    # =====================================================================
    {
        "slug": "light-ball",
        "name": "Light Ball",
        "category": "Species-specific",
        "boost": "Multiplies BOTH Attack and Special Attack by 2× — Pikachu only.",
        "description": ("Pikachu's signature item. Held by anything else, the Light Ball does nothing — the boost "
                        "is gated on the holder being Pikachu specifically, so even Pichu and Raichu don't qualify. "
                        "The simultaneous ×2 on both offensive stats pushes the otherwise-frail Mouse Pokémon into "
                        "OU-relevant power tiers, which is why it's banned in most format pools alongside Mega Stones."),
        "holder": "Pikachu only.",
    },
    {
        "slug": "thick-club",
        "name": "Thick Club",
        "category": "Species-specific",
        "boost": "Multiplies Attack by 2× — Cubone or Marowak only (any region's Marowak counts).",
        "description": ("Hard bone of some sort. Cubone or Marowak holding it doubles its already-respectable Attack stat "
                        "and starts threatening one-shots on neutral targets. The check is on species name, so Alolan and "
                        "other regional Marowak variants qualify alongside the standard form."),
        "holder": "Cubone or Marowak only.",
    },
    {
        "slug": "soul-dew",
        "name": "Soul Dew",
        "category": "Species-specific",
        "boost": "Multiplies BOTH Special Attack and Special Defense by 1.5× — Latios or Latias only.",
        "description": ("The Eon-twins' signature stat-amp. Confirmed in source: ×1.5 to Special Attack AND Special "
                        "Defense (NOT a type-specific boost) when held by Latios or Latias. Effectively turns either "
                        "Eon Pokémon into a budget Choice Specs + Assault Vest hybrid that doesn't lock moves."),
        "holder": "Latios or Latias only.",
    },
    {
        "slug": "lucky-punch",
        "name": "Lucky Punch",
        "category": "Species-specific",
        "boost": "Massively boosts Chansey's critical-hit ratio (effectively +2 stages).",
        "description": ("Chansey's joke item: the world's bulkiest Normal-type suddenly has a near-permanent crit threat "
                        "on Seismic Toss / Night Shade. Largely a meme pick at high levels — Chansey usually wants Eviolite "
                        "to live forever — but legal in formats that ban Eviolite."),
        "holder": "Chansey only.",
    },
    {
        "slug": "reek",
        "name": "Reek",
        "category": "Species-specific",
        "boost": "Massively boosts Farfetch'd's critical-hit ratio (effectively +2 stages).",
        "description": ("Farfetch'd's signature stalk of leek. Same critical-hit treatment as Lucky Punch on Chansey — "
                        "huge boost in crit-rate, useless on every other holder. The name is a typo of \"Leek\" that "
                        "snuck into the codebase early on and stuck around as a running joke; in-game it's officially "
                        "\"Reek\" everywhere now."),
        "holder": "Farfetch'd only.",
    },
    {
        "slug": "quick-powder",
        "name": "Quick Powder",
        "category": "Species-specific",
        "boost": "Doubles Speed — only on un-transformed Ditto.",
        "description": ("Ditto-only Speed booster. Once Ditto Transforms into something, the powder stops mattering "
                        "(Transform overwrites the held-item interaction). Lets a Ditto outspeed faster threats before "
                        "it copies them, which is the whole reason to run a Ditto in the first place."),
        "holder": "Untransformed Ditto only.",
    },
    {
        "slug": "metal-powder",
        "name": "Metal Powder",
        "category": "Species-specific",
        "boost": "Doubles Defense — only on un-transformed Ditto.",
        "description": ("Quick Powder's defensive sibling. Doubles Ditto's Defense pre-Transform — useful for surviving "
                        "the hit that comes immediately after the copy, since Ditto can't move on the turn it transforms."),
        "holder": "Untransformed Ditto only.",
    },
    {
        "slug": "deep-sea-tooth",
        "name": "Deep Sea Tooth",
        "category": "Species-specific",
        "boost": "Doubles Special Attack on Clamperl. Used to evolve Clamperl into Huntail when traded while held.",
        "description": ("Half of the Clamperl evolution split. Doubles Clamperl's already-strong Special Attack — turns "
                        "what's otherwise a frail prevo into a credible glass-cannon special wallbreaker. Trading "
                        "Clamperl while it holds the Tooth evolves it into Huntail."),
        "holder": "Clamperl only.",
    },
    {
        "slug": "deep-sea-scale",
        "name": "Deep Sea Scale",
        "category": "Species-specific",
        "boost": "Doubles Special Defense on Clamperl. Used to evolve Clamperl into Gorebyss when traded while held.",
        "description": ("The other half of the Clamperl split. Doubles Special Defense for Clamperl-only specbulk — "
                        "and triggers Gorebyss evolution when Clamperl is traded holding it."),
        "holder": "Clamperl only.",
    },

    # =====================================================================
    # Iron Ball — singleton item with its own niche.
    # =====================================================================
    {
        "slug": "iron-ball",
        "name": "Iron Ball",
        "category": "Held utility",
        "boost": "Halves the holder's Speed and lets Ground-type moves hit Flying types / Levitate holders.",
        "description": ("The Speed-down + Ground-immunity-bypass item. Specifically useful on slow Trick Room sweepers "
                        "that want to be even slower than usual, or as a Tricked-onto-the-opponent gimmick to drop their "
                        "Speed and break their Levitate / Flying immunity."),
    },
    # =====================================================================
    # Out-of-battle / utility items — XP boosters, capsules, charms.
    # =====================================================================
    {
        "slug": "lucky-egg",
        "name": "Lucky Egg",
        "category": "Out-of-battle XP",
        "boost": "Activates double XP for the holding player for 30 minutes per use.",
        "description": ("The grind accelerator. Right-click while held to double the *player's* earned XP for the next "
                        "thirty minutes — the activation is announced server-wide so everyone knows you've started the "
                        "timer. Useful when burning through a backlog of party levels or the EV-trained set you just "
                        "finished IV-cloning. The buff is per-player (unlike XP Boost Elixir, which is server-wide), so "
                        "multiple players can each have one active without stepping on each other."),
        "duration": "30 minutes per activation.",
    },
    {
        "slug": "xp-boost-elixir",
        "name": "XP Boost Elixir",
        "category": "Out-of-battle XP",
        "boost": "Server-wide XP boost for 30 minutes per use.",
        "description": ("Lucky Egg's bigger cousin: a single elixir use boosts XP gain *for everyone on the server* "
                        "for thirty minutes, broadcast via boss-bar so the whole server knows who started the ride. "
                        "Cannot be activated within 30 minutes of the daily restart — the elixir refuses to start a "
                        "buff window that wouldn't finish before the server reset."),
        "duration": "30 minutes per activation.",
    },
    {
        "slug": "exp-share",
        "name": "Exp. Share",
        "category": "Out-of-battle XP",
        "boost": "Distributes a share of battle XP to the holder, even if it didn't take part in the fight.",
        "description": ("Held by a benched Pokémon, Exp. Share splits a portion of every battle's XP onto it. Designed to "
                        "let trainers level a low-level partner without grinding it directly. Stacked with Lucky Egg + "
                        "XP Boost Elixir during a buffed window for maximum throughput."),
    },
    {
        "slug": "ability-capsule",
        "name": "Ability Capsule",
        "category": "Out-of-battle utility",
        "boost": "Switches a Pokémon between its two normal abilities (does not unlock Hidden Abilities).",
        "description": ("Right-click on a Pokémon to flip its ability between the two non-hidden options. Single-use; the "
                        "capsule is consumed on the swap. Hidden abilities aren't reachable via Capsule — those need an "
                        "Ability Patch (or a wild encounter that already has the HA)."),
        "consumed": "Yes — single-use.",
    },
    {
        "slug": "shiny-charm",
        "name": "Shiny Charm",
        "category": "Out-of-battle utility",
        "boost": "Activates a 30-minute window of boosted shiny encounter rates in the wild.",
        "description": ("Right-click while held to start a 30-minute window of boosted shiny encounter rates for the "
                        "activator. Pair with a Lucky Egg + XP Boost Elixir window to multitask the grind — three "
                        "concurrent buffs covering levels, server-wide XP, and shiny chance."),
        "duration": "30 minutes per activation.",
    },
    {
        "slug": "rare-candy",
        "name": "Rare Candy",
        "category": "Out-of-battle utility",
        "boost": "Raises a Pokémon's level by one when used.",
        "description": ("Skip a level's worth of grind. Right-click on a Pokémon's summary to bump its level up by one — "
                        "stat gains apply normally, EVs are not earned for the level-up. Caps out at the same level "
                        "ceiling as battle-XP grinding."),
        "consumed": "Yes — single-use per level.",
    },

    # =====================================================================
    # EV-lowering berries — out-of-battle EV correction tools.
    # =====================================================================
    _ev_lower_berry("pomeg-berry",  "Pomeg Berry",  "HP"),
    _ev_lower_berry("kelpsy-berry", "Kelpsy Berry", "Attack"),
    _ev_lower_berry("qualot-berry", "Qualot Berry", "Defense"),
    _ev_lower_berry("hondew-berry", "Hondew Berry", "Special Attack"),
    _ev_lower_berry("grepa-berry",  "Grepa Berry",  "Special Defense"),
    _ev_lower_berry("tamato-berry", "Tamato Berry", "Speed"),
]


# ---------------------------------------------------------------------------
# Quest extraction
# ---------------------------------------------------------------------------

# Match `GiveItem` in both shapes the quest grammar uses:
#   "GiveItem": "<name>"                (count==1, sugar form)
#   "GiveItem": ["<name>", <count_or_chance>, ...]
# Either group 1 (string form) or group 2 (array form) carries the name.
GIVE_ITEM_PATTERN = re.compile(
    r'"GiveItem"\s*:\s*(?:"([^"]+)"|\[\s*"([^"]+)")',
    re.IGNORECASE,
)


def _quest_pretty(stem: str) -> str:
    """Convert a quest filename stem to a human-readable title."""
    s = stem.lstrip("0")          # strip leading zero(s) used for sort order
    s = re.sub(r"[-_]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.title()


def _classify_source(path: Path) -> str:
    """Return either 'Shop' or 'Quest reward' based on path/filename hints.
    Match shop tokens on word boundaries — any path part split on
    `[-_./]` whose tokens include a shop word is a Shop. Substring
    matching was too loose (e.g. 'QuestsToRemember' contains 'store',
    which would mis-tag every quest in that tree as a shop)."""
    word_split = re.compile(r"[-_./\s]+")
    def _has_shop_token(s: str) -> bool:
        return any(w in SHOP_NAME_TOKENS for w in word_split.split(s.lower()) if w)
    for part in path.parts:
        if _has_shop_token(part):
            return "Shop"
    if _has_shop_token(path.stem):
        return "Shop"
    return "Quest reward"


def _is_seasonal(path: Path) -> bool:
    """True iff any path part or filename stem matches a seasonal token —
    used to drop event-only quests (Christmas / Halloween / Easter /
    Summer / Thanksgiving / Valentine / Anniversary / Black Friday)
    from "Where to find" lists."""
    parts_lower = [p.lower() for p in path.parts]
    stem_lower = path.stem.lower()
    if any(any(tok in p for tok in SEASONAL_TOKENS) for p in parts_lower):
        return True
    if any(tok in stem_lower for tok in SEASONAL_TOKENS):
        return True
    return False


def _is_excluded(path: Path) -> bool:
    """True iff the quest file is on the explicit EXCLUDED_PATH_FRAGMENTS
    blocklist — separate from seasonal filtering since these are
    one-off editorial decisions (e.g. the Gen 4 monthly crates and
    the Gen 4 CM Suppmain rewards) rather than time-of-year events."""
    posix = path.as_posix().lower()
    return any(frag.lower() in posix for frag in EXCLUDED_PATH_FRAGMENTS)


# ---------------------------------------------------------------------------
# Battle Tower Shop parser
# ---------------------------------------------------------------------------
# The shop's inventory is hardcoded as `ITEMS.add(getItem(Item.X, BUY, SELL))`
# rows in BattleTowerShopMenu.java. We parse those statements once at
# script start and turn them into a {ITEM_ENUM_NAME: buy_price} lookup.
# The shop's currency is Battle Points (BattlePointsCurrency.java).
_BATTLE_TOWER_PATTERN = re.compile(
    r'getItem\s*\(\s*Item\.([A-Z_]+)\s*,\s*(\d+)\s*,\s*\d+\s*\)'
)


def _load_battle_tower_inventory() -> dict[str, int]:
    """Return {ENUM_NAME: buy_price_in_BP} parsed from the Java shop file.
    Empty dict if the source isn't reachable (e.g. the repo isn't checked
    out at the expected path)."""
    if not BATTLE_TOWER_SHOP_JAVA.is_file():
        return {}
    try:
        text = BATTLE_TOWER_SHOP_JAVA.read_text(encoding="utf-8")
    except Exception:
        return {}
    return {m.group(1): int(m.group(2))
            for m in _BATTLE_TOWER_PATTERN.finditer(text)}


_BATTLE_TOWER_INVENTORY = _load_battle_tower_inventory()


def _name_to_enum(item_name: str) -> str:
    """Map an item display name (e.g. "Focus Sash", "Exp. Share") to its
    `Item.<ENUM_NAME>` form (FOCUS_SASH, EXP_SHARE). Strips punctuation
    and uppercases / underscores."""
    s = re.sub(r"[^A-Za-z0-9]+", "_", item_name).strip("_")
    return s.upper()


def find_battle_tower_shop_source(item_name: str, enum_override: str | None = None) -> list[str]:
    """If the named item is sold in the Battle Tower Shop, return a
    single "Shop: **Battle Tower Shop** (N BP)" line. Empty list
    otherwise. Pass `enum_override` for items whose Java enum name
    diverges from the display name (e.g. "Stick" → REEK)."""
    enum_name = enum_override or _name_to_enum(item_name)
    price = _BATTLE_TOWER_INVENTORY.get(enum_name)
    if price is None:
        return []
    return [f"Shop: **Battle Tower Shop** ({price} BP)"]


def find_quest_rewards(item_name: str) -> list[str]:
    """Scan every QUEST_SOURCE_DIR for files whose `GiveItem` grammar
    references this item, classify each match as a Shop or Quest reward,
    and emit a deduped list of "<Kind>: **<Pretty>**" lines. Seasonal /
    event-only quests are skipped — see _is_seasonal()."""
    target = item_name.lower()
    found: list[str] = []
    seen: set[str] = set()
    for base in QUEST_SOURCE_DIRS:
        if not base.is_dir():
            continue
        for qf in sorted(base.rglob("*.json")):
            if _is_seasonal(qf) or _is_excluded(qf):
                continue
            try:
                text = qf.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if '"GiveItem"' not in text:
                continue
            for m in GIVE_ITEM_PATTERN.finditer(text):
                given = (m.group(1) or m.group(2) or "").lower()
                if given == target:
                    pretty = _quest_pretty(qf.stem)
                    kind = _classify_source(qf)
                    label = f"{kind}: **{pretty}**"
                    if label in seen:
                        break
                    seen.add(label)
                    found.append(label)
                    break
    return found


# ---------------------------------------------------------------------------
# Markdown emission
# ---------------------------------------------------------------------------

def _yaml_quote(s: str) -> str:
    """Render a string in YAML single-quoted form (escapes embedded
    quotes by doubling them, per YAML spec)."""
    return "'" + s.replace("'", "''") + "'"


def write_page(item: dict) -> None:
    slug = item["slug"]
    name = item["name"]
    # Compose locations from three sources. Order matters — quest-tree
    # rewards first (most likely to be the discoverable in-game answer),
    # then permanent shops the user explicitly named, then the Battle
    # Tower Shop's BP-priced inventory.
    locations: list[str] = []
    locations.extend(find_quest_rewards(name))
    locations.extend(MANUAL_SHOP_SOURCES.get(name, []))
    locations.extend(find_battle_tower_shop_source(name, item.get("enum_override")))
    # Drop dupes while preserving order.
    seen: set[str] = set()
    locations = [l for l in locations if not (l in seen or seen.add(l))]
    # Note: do NOT emit `type: 'page'` here — that diverts Hugo to the
    # `layouts/page/` template tree, bypassing our `layouts/items/single.html`.
    # Letting Hugo derive the type from the section (items) keeps it on the
    # right template.
    lines = ["---",
             f"title: {_yaml_quote(name)}",
             f"date: {date.today().isoformat()}"]
    for k in ("category", "boost", "holder", "duration", "consumed"):
        if v := item.get(k):
            lines.append(f"{k}: {_yaml_quote(v)}")
    if d := item.get("description"):
        lines.append(f"description: {_yaml_quote(d)}")
    if locations:
        lines.append("locations:")
        for loc in locations:
            lines.append(f"  - {_yaml_quote(loc)}")
    lines.append("---")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{slug}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote items/{slug}.md  ({len(locations)} locations)")


def main() -> int:
    missing = [str(d) for d in QUEST_SOURCE_DIRS if not d.is_dir()]
    for m in missing:
        print(f"warning: quest source dir not found: {m}", file=sys.stderr)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for item in ITEMS:
        write_page(item)
    print(f"\n{len(ITEMS)} item pages written under {OUT_DIR.relative_to(REPO)}/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
