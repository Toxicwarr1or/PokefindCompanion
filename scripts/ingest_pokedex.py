#!/usr/bin/env python3
"""
Ingest species_gen6.json into Hugo content/pokedex/<slug>.md, one file per BASE species.
Regional variants (Alolan / Galarian / Kyoto / Jataro / Haikou / Shiloh / Zeinova) are
merged into their base species as entries in a `forms` array, rendered as tabs.

Sprites are downloaded from the PokeAPI sprite repo (open-license) by national-dex id.
Form-specific sprites are attempted with PokeAPI's variant-suffix convention
(`19-alola.png`, `646-black.png`, etc.); falls back to empty if 404.

Gen 6 species (national-dex 650–721) are excluded — see --include-gen6 to keep them.

Manually-injected forms: Kyurem (Black, White) and Meloetta (Pirouette) are not in the
species data file but are added as form tabs with canonical stats.

Usage:
    python3 scripts/ingest_pokedex.py [--species PATH] [--keep-existing] [--include-gen6]
                                      [--no-sprites]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile

# Optional 3D-model renderer (numpy + Pillow). Imported lazily so the script
# still works without numpy if --no-render is passed.
try:
    from render_models import render_model, find_model_path  # type: ignore
    RENDERER_AVAILABLE = True
except Exception:
    RENDERER_AVAILABLE = False
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SPECIES = Path("/home/jack/Downloads/species_gen6.json")
DEFAULT_PACK = Path("/home/jack/.minecraft/resourcepacks/devhelditem.zip")
DEFAULT_MOVES_DATA = Path("/home/jack/ClaudeProjects/PokemonWorld-master/pokemon-world-core/src/main/resources/data/moves.json")
MOVES_CONTENT_DIR = ROOT / "content/moves"


MOVE_LOOKUP: dict[str, dict] = {}


def load_move_lookup(path: Path) -> dict:
    """Load moves.json into a name -> attrs map. Returns {} if path missing."""
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    out: dict[str, dict] = {}
    for rec in data:
        name = rec.get("name")
        if not name:
            continue
        out[name] = {
            "type": (rec.get("type") or "").title(),
            "category": (rec.get("damage_class") or "").title(),  # Physical/Special/Status
            "power": rec.get("power"),
            "accuracy": rec.get("accuracy"),
            "pp": rec.get("pp"),
        }
    return out
TOXIC_PACK_REGULAR = Path("/home/jack/.minecraft/resourcepacks/ToxicPackDNA2/assets/minecraft/textures/pokemon_skin_icons/regular")

# Per-form icon sources from ToxicPackDNA2. Pack uses inconsistent IDs (sometimes
# national dex, sometimes server-internal sequence) — explicit mapping is safer
# than trying to guess. Keyed by (base species name, form name).
TOXIC_FORM_FILES = {
    ("Rotom", "Heat"):     "479_heat.png",
    ("Rotom", "Wash"):     "479_wash.png",
    ("Rotom", "Frost"):    "479_frost.png",
    ("Rotom", "Fan"):      "479_fan.png",
    ("Rotom", "Mow"):      "479_mow.png",
    ("Shaymin", "Sky"):    "492_sky.png",
    ("Tornadus", "Therian"):  "33_therian.png",
    ("Thundurus", "Therian"): "642_therian.png",
    ("Landorus", "Therian"):  "37_therian.png",
    ("Darmanitan", "Zen"): "24_zen.png",
    # Arceus plates
    ("Arceus", "Bug"):      "46_bug.png",
    ("Arceus", "Dark"):     "47_dark.png",
    ("Arceus", "Dragon"):   "48_dragon.png",
    ("Arceus", "Electric"): "49_electric.png",
    ("Arceus", "Fairy"):    "50_fairy.png",
    ("Arceus", "Fighting"): "51_fighting.png",
    ("Arceus", "Fire"):     "52_fire.png",
    ("Arceus", "Flying"):   "53_flying.png",
    ("Arceus", "Ghost"):    "54_ghost.png",
    ("Arceus", "Ground"):   "55_ground.png",
    ("Arceus", "Ice"):      "56_ice.png",
    ("Arceus", "Poison"):   "57_poison.png",
    ("Arceus", "Psychic"):  "58_psychic.png",
    ("Arceus", "Rock"):     "59_rock.png",
    ("Arceus", "Steel"):    "60_steel.png",
    ("Arceus", "Grass"):    "61_grass.png",
    ("Arceus", "Water"):    "62_water.png",
    # Sawsbuck seasonal (Standard = Spring per main games)
    ("Sawsbuck", "Summer"): "586_summer.png",
    ("Sawsbuck", "Autumn"): "586_autumn.png",
    ("Sawsbuck", "Winter"): "586_winter.png",
}
CONTENT_DIR = ROOT / "content/pokedex"
IMAGES_DIR = ROOT / "static/images/pokedex"

POKEAPI_SPRITE_BASE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"

# Server resource-pack icon paths. Each (skin) folder has <id>.png keyed by national dex.
PACK_ICON_BASE = "assets/minecraft/textures/pokemon_skin_icons/{skin}/{id}.png"
# Shiny variants of regional anniversary forms live in nested subdirectories.
PACK_ICON_NESTED_SHINY = "assets/minecraft/textures/pokemon_skin_icons/{skin}/shiny/{id}.png"
# Per-species 3D-model parts. Existence of a directory under pokemon_skins/<skin>/<slug>/
# proves the skin is "available" for that species, even if no flat icon exists.
PACK_SKINS_DIR_PREFIX = "assets/minecraft/textures/pokemon_skins/"

# Fallback texture paths in the bettermodel pack (3D model UV maps; less ideal as
# 2D icons but better than nothing for species the icon folder doesn't cover).
BETTERMODEL_BASE = "assets/bettermodel/textures/item/{slug}_{slug}.png"
BETTERMODEL_VARIANT = "assets/bettermodel/textures/item/{slug}_v_{skin}_{slug}_{skin}.png"

# Mapping of pokemon_skin_icons folder name to bettermodel variant suffix where they
# differ. Most match directly; only special cases listed.
BETTERMODEL_SKIN_ALIAS = {
    "lunar_new_year": "lunar",
    "april_fools": "april",
    "sword_and_shield": "sword",
}

# Form prefixes that map to the anniversary icon set in the pack.
ANNIVERSARY_PREFIXES = {"Kyoto", "Jataro", "Haikou", "Shiloh", "Zeinova"}

# Cosmetic skins of the Standard form, in display order. Each becomes its own tab when an
# icon exists for the species. "regular" is the Standard tab itself; the rest are cosmetic
# variants. Server-region anniversary forms get tabs named after the prefix (Kyoto / etc.)
# rather than the literal "anniversary" skin label.
COSMETIC_SKINS = [
    "regular",
    "shiny",
    "halloween",
    "christmas",
    "easter",
    "valentine",
    "thanksgiving",
    "summer",
    "lunar_new_year",
    "april_fools",
    "shadow",
    "aura",
    "gamer",
    "mecha",
    "cosmic",
    "marvel",
    "disney",
    "modeler",
    "fusemon",
    "meme",
    "monochrome",
    "sword_and_shield",
]


def skin_label(skin: str) -> str:
    """Pretty tab label for a cosmetic skin folder name."""
    return skin.replace("_", " ").title()

# PokeAPI's regional-form filename suffix convention. Server-region prefixes have no
# upstream sprite; we map them to None so the script doesn't bother trying.
FORM_SUFFIX = {
    "Standard": "",
    "Alolan":   "-alola",
    "Galarian": "-galar",
    "Hisuian":  "-hisui",
    "Paldean":  "-paldea",
    "Kyoto":    None,
    "Jataro":   None,
    "Haikou":   None,
    "Shiloh":   None,
    "Zeinova":  None,
}

REGIONAL_PREFIXES = [p for p in FORM_SUFFIX.keys() if p != "Standard"]

# PokeAPI uses dedicated form IDs (10000-range) for Alolan / Galarian / Hisuian
# variants. The local species_gen6.json file uses negative IDs for these,
# which don't resolve upstream. Map each (base species, form prefix) pair to
# the canonical PokeAPI form ID so we can fetch a real sprite for the tab.
POKEAPI_FORM_IDS = {
    # ---------- Alolan (Gen 7) ----------
    ("Rattata",    "Alolan"): 10091,
    ("Raticate",   "Alolan"): 10092,
    ("Raichu",     "Alolan"): 10100,
    ("Sandshrew",  "Alolan"): 10101,
    ("Sandslash",  "Alolan"): 10102,
    ("Vulpix",     "Alolan"): 10103,
    ("Ninetales",  "Alolan"): 10104,
    ("Diglett",    "Alolan"): 10105,
    ("Dugtrio",    "Alolan"): 10106,
    ("Meowth",     "Alolan"): 10107,
    ("Persian",    "Alolan"): 10108,
    ("Geodude",    "Alolan"): 10109,
    ("Graveler",   "Alolan"): 10110,
    ("Golem",      "Alolan"): 10111,
    ("Grimer",     "Alolan"): 10112,
    ("Muk",        "Alolan"): 10113,
    ("Exeggutor",  "Alolan"): 10114,
    ("Marowak",    "Alolan"): 10115,
    # ---------- Galarian (Gen 8) ----------
    ("Meowth",     "Galarian"): 10161,
    ("Ponyta",     "Galarian"): 10162,
    ("Rapidash",   "Galarian"): 10163,
    ("Slowpoke",   "Galarian"): 10164,
    ("Slowbro",    "Galarian"): 10165,
    ("Farfetch'd", "Galarian"): 10166,
    ("Farfetchd",  "Galarian"): 10166,
    ("Weezing",    "Galarian"): 10167,
    ("Mr. Mime",   "Galarian"): 10168,
    ("Mr Mime",    "Galarian"): 10168,
    ("Articuno",   "Galarian"): 10169,
    ("Zapdos",     "Galarian"): 10170,
    ("Moltres",    "Galarian"): 10171,
    ("Slowking",   "Galarian"): 10172,
    ("Corsola",    "Galarian"): 10173,
    ("Zigzagoon",  "Galarian"): 10174,
    ("Linoone",    "Galarian"): 10175,
    ("Darumaka",   "Galarian"): 10176,
    ("Darmanitan", "Galarian"):     10177,
    ("Darmanitan", "Galarian Zen"): 10178,
    ("Yamask",     "Galarian"):     10179,
    ("Stunfisk",   "Galarian"):     10180,
}

# Manually-injected forms not present in the species data file. Keyed by base name.
# Each form provides: ability set, type override, base-stat override, sprite-suffix,
# and an editorial note describing how the form change is triggered in-game.

def _form(name, types, abilities, stats, suffix, note, hidden=""):
    return {
        "name": name,
        "types": types,
        "abilities": abilities,
        "hidden_ability": hidden,
        "base_stats": dict(zip(("hp", "atk", "def", "spa", "spd", "spe"), stats)),
        "sprite_suffix": suffix,
        "note": note,
    }

# Arceus's 17 plates (default Normal stays as Standard form). Stats are identical
# (120 across the board); the plate held determines its type.
_ARCEUS_PLATES = [
    ("Fighting", "fist"),     ("Flying", "sky"),       ("Poison", "toxic"),
    ("Ground", "earth"),      ("Rock", "stone"),       ("Bug", "insect"),
    ("Ghost", "spooky"),      ("Steel", "iron"),       ("Fire", "flame"),
    ("Water", "splash"),      ("Grass", "meadow"),     ("Electric", "zap"),
    ("Psychic", "mind"),      ("Ice", "icicle"),       ("Dragon", "draco"),
    ("Dark", "dread"),        ("Fairy", "pixie"),
]
_ARCEUS_FORMS = [
    _form(t, [t], ["Multitype"], (120, 120, 120, 120, 120, 120),
          f"-{plate}", f"Holding the {plate.title()} Plate changes Arceus's type to {t}.")
    for t, plate in _ARCEUS_PLATES
]

EXTRA_FORMS = {
    "Kyurem": [
        _form("Black", ["Dragon", "Ice"], ["Teravolt"],
              (125, 170, 100, 120, 90, 95), "-black",
              "Fused with Zekrom via the DNA Splicers. Physical-attacking form."),
        _form("White", ["Dragon", "Ice"], ["Turboblaze"],
              (125, 120, 90, 170, 100, 95), "-white",
              "Fused with Reshiram via the DNA Splicers. Special-attacking form."),
    ],
    "Meloetta": [
        _form("Pirouette", ["Normal", "Fighting"], ["Serene Grace"],
              (100, 128, 90, 77, 77, 128), "-pirouette",
              "Form change via Relic Song. Reverts on switch out or fainting."),
    ],
    "Giratina": [
        _form("Origin", ["Ghost", "Dragon"], ["Levitate"],
              (150, 120, 100, 120, 100, 90), "-origin",
              "Holding the Griseous Orb. Sword-like body, Atk and SpA up, Def and SpD down."),
    ],
    "Rotom": [
        _form("Heat", ["Electric", "Fire"], ["Levitate"],
              (50, 65, 107, 105, 107, 86), "-heat",
              "Possesses a microwave oven. Signature move: Overheat."),
        _form("Wash", ["Electric", "Water"], ["Levitate"],
              (50, 65, 107, 105, 107, 86), "-wash",
              "Possesses a washing machine. Signature move: Hydro Pump."),
        _form("Frost", ["Electric", "Ice"], ["Levitate"],
              (50, 65, 107, 105, 107, 86), "-frost",
              "Possesses a refrigerator. Signature move: Blizzard."),
        _form("Fan", ["Electric", "Flying"], ["Levitate"],
              (50, 65, 107, 105, 107, 86), "-fan",
              "Possesses an electric fan. Signature move: Air Slash."),
        _form("Mow", ["Electric", "Grass"], ["Levitate"],
              (50, 65, 107, 105, 107, 86), "-mow",
              "Possesses a lawnmower. Signature move: Leaf Storm."),
    ],
    "Arceus": _ARCEUS_FORMS,
    "Deoxys": [
        _form("Attack", ["Psychic"], ["Pressure"],
              (50, 180, 20, 180, 20, 150), "-attack",
              "Form change via the Meteorite. Glass-cannon offensive build."),
        _form("Defense", ["Psychic"], ["Pressure"],
              (50, 70, 160, 70, 160, 90), "-defense",
              "Form change via the Meteorite. Walls and recovers."),
        _form("Speed", ["Psychic"], ["Pressure"],
              (50, 95, 90, 95, 90, 180), "-speed",
              "Form change via the Meteorite. Out-runs anything in the game."),
    ],
    "Shaymin": [
        _form("Sky", ["Grass", "Flying"], ["Serene Grace"],
              (100, 103, 75, 120, 75, 127), "-sky",
              "Form change via the Gracidea flower (only during the day, only when not frozen)."),
    ],
    "Wormadam": [
        _form("Sandy", ["Bug", "Ground"], ["Anticipation"],
              (60, 79, 105, 59, 85, 36), "-sandy",
              "Cloak determined by the environment Burmy was last in before evolving."),
        _form("Trash", ["Bug", "Steel"], ["Anticipation"],
              (60, 69, 95, 69, 95, 36), "-trash",
              "Cloak determined by the environment Burmy was last in before evolving."),
    ],
    "Burmy": [
        _form("Sandy", ["Bug"], ["Shed Skin"],
              (40, 29, 45, 29, 45, 36), "-sandy",
              "Cloak changes after each battle based on the surrounding terrain."),
        _form("Trash", ["Bug"], ["Shed Skin"],
              (40, 29, 45, 29, 45, 36), "-trash",
              "Cloak changes after each battle based on the surrounding terrain."),
    ],
    "Castform": [
        _form("Sunny", ["Fire"], ["Forecast"],
              (70, 70, 70, 70, 70, 70), "-sunny",
              "Forecast triggers in harsh sunlight. Type changes; stats unchanged."),
        _form("Rainy", ["Water"], ["Forecast"],
              (70, 70, 70, 70, 70, 70), "-rainy",
              "Forecast triggers in rain. Type changes; stats unchanged."),
        _form("Snowy", ["Ice"], ["Forecast"],
              (70, 70, 70, 70, 70, 70), "-snowy",
              "Forecast triggers in hail or snow. Type changes; stats unchanged."),
    ],
    "Darmanitan": [
        _form("Zen", ["Fire", "Psychic"], ["Zen Mode"],
              (105, 30, 105, 140, 105, 55), "-zen",
              "Switches to Zen Mode automatically below 50% HP via the Zen Mode ability."),
    ],
    "Cherrim": [
        _form("Sunshine", ["Grass"], ["Flower Gift"],
              (70, 60, 70, 87, 78, 85), "-sunshine",
              "Bloom form active in harsh sunlight. Boosts party Atk and SpD."),
    ],
    "Tornadus": [
        _form("Therian", ["Flying"], ["Regenerator"],
              (79, 100, 80, 110, 90, 121), "-therian",
              "Reverse World form change. Quadrupedal storm-being."),
    ],
    "Thundurus": [
        _form("Therian", ["Electric", "Flying"], ["Volt Absorb"],
              (79, 105, 70, 145, 80, 101), "-therian",
              "Reverse World form change. Bull-like silhouette, special attacker."),
    ],
    "Landorus": [
        _form("Therian", ["Ground", "Flying"], ["Intimidate"],
              (89, 145, 90, 105, 80, 91), "-therian",
              "Reverse World form change. Tiger silhouette, physical attacker."),
    ],
    "Keldeo": [
        _form("Resolute", ["Water", "Fighting"], ["Justified"],
              (91, 72, 90, 129, 90, 108), "-resolute",
              "Appearance change when Keldeo knows Secret Sword. Same stats and types."),
    ],
    "Sawsbuck": [
        _form("Summer", ["Normal", "Grass"], ["Chlorophyll"],
              (80, 100, 70, 60, 70, 95), "-summer",
              "Coat changes with the season."),
        _form("Autumn", ["Normal", "Grass"], ["Chlorophyll"],
              (80, 100, 70, 60, 70, 95), "-autumn",
              "Coat changes with the season."),
        _form("Winter", ["Normal", "Grass"], ["Chlorophyll"],
              (80, 100, 70, 60, 70, 95), "-winter",
              "Coat changes with the season."),
    ],
    "Deerling": [
        _form("Summer", ["Normal", "Grass"], ["Chlorophyll"],
              (60, 60, 50, 40, 50, 75), "-summer",
              "Coat changes with the season."),
        _form("Autumn", ["Normal", "Grass"], ["Chlorophyll"],
              (60, 60, 50, 40, 50, 75), "-autumn",
              "Coat changes with the season."),
        _form("Winter", ["Normal", "Grass"], ["Chlorophyll"],
              (60, 60, 50, 40, 50, 75), "-winter",
              "Coat changes with the season."),
    ],
    "Genesect": [
        _form("Burn", ["Bug", "Steel"], ["Download"],
              (71, 120, 95, 120, 95, 99), "-burn",
              "Holding the Burn Drive. Techno Blast becomes Fire-type."),
        _form("Chill", ["Bug", "Steel"], ["Download"],
              (71, 120, 95, 120, 95, 99), "-chill",
              "Holding the Chill Drive. Techno Blast becomes Ice-type."),
        _form("Douse", ["Bug", "Steel"], ["Download"],
              (71, 120, 95, 120, 95, 99), "-douse",
              "Holding the Douse Drive. Techno Blast becomes Water-type."),
        _form("Shock", ["Bug", "Steel"], ["Download"],
              (71, 120, 95, 120, 95, 99), "-shock",
              "Holding the Shock Drive. Techno Blast becomes Electric-type."),
    ],
}


def texture_slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def content_slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def skins_dir_candidates(name: str) -> list[str]:
    """Slug candidates for matching pokemon_skins/<skin>/<slug>/ directories.
    The pack uses inconsistent conventions: 'pikachu', 'porygon-z', 'nidoran_f',
    'farfetchd', 'mrmime'. Generate every plausible variant."""
    n = name.lower().strip()
    return list(dict.fromkeys([
        re.sub(r"[^a-z0-9]+", "", n),                       # mrmime, farfetchd
        re.sub(r"[^a-z0-9]+", "_", n).strip("_"),           # nidoran_f, mr_mime
        re.sub(r"[^a-z0-9]+", "-", n).strip("-"),           # porygon-z, ho-oh
        n.replace(" ", "").replace("'", "").replace(":", "").replace(".", ""),
    ]))


_CONTROL_CHARS = set(range(0x00, 0x20)) | {0x7F} | set(range(0x80, 0xA0))


def _sanitize(text) -> str:
    cleaned = "".join(c for c in str(text) if ord(c) not in _CONTROL_CHARS)
    replacements = {
        "â€œ": "\"", "â€": "\"",
        "â€™": "'", "â€˜": "'",
        "â€“": "-", "â€”": "-",
        "Â": "",
    }
    for bad, good in replacements.items():
        cleaned = cleaned.replace(bad, good)
    return cleaned


def yaml_string(value) -> str:
    return "'" + _sanitize(value).replace("'", "''") + "'"


def yaml_list(values) -> str:
    if not values:
        return "[]"
    return "[" + ", ".join(yaml_string(v) for v in values) + "]"


def detect_form(name: str) -> tuple[str, str]:
    stripped = name.strip()
    for prefix in REGIONAL_PREFIXES:
        token = prefix + " "
        if stripped.startswith(token):
            return (stripped[len(token):].strip(), prefix)
    return (stripped, "Standard")


# ---------- Sprite download (PokeAPI) ----------

class SpriteCache:
    """Resolves sprites in priority order:
       1. Server resource-pack icon (regular/ for Standard, anniversary/ for server-region forms)
       2. PokeAPI default sprite (Standard form only, falls back when pack lacks the species)
    Variant forms with no pack icon and no PokeAPI mapping (Alolan/Galarian/Kyurem-Black/etc.)
    return None and the layout shows a placeholder."""

    def __init__(self, pack_path: Path, enable_pokeapi: bool, enable_render: bool = True):
        self.images_dir = IMAGES_DIR
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.enable_pokeapi = enable_pokeapi
        self.enable_render = enable_render and RENDERER_AVAILABLE
        self.pokeapi_tried: dict[tuple[str, int], bool] = {}
        self.pack_zip = zipfile.ZipFile(pack_path) if pack_path.exists() else None
        self.pack_names = set(self.pack_zip.namelist()) if self.pack_zip else set()
        # Map (skin, species_slug) -> True for every per-species directory under
        # pokemon_skins/<skin>/<slug>/. Used to determine "skin is available" even
        # when no flat icon exists.
        self.skins_dirs: set[tuple[str, str]] = set()
        for n in self.pack_names:
            if not n.startswith(PACK_SKINS_DIR_PREFIX):
                continue
            rest = n[len(PACK_SKINS_DIR_PREFIX):]
            parts = rest.split("/")
            if len(parts) >= 2 and parts[1]:
                self.skins_dirs.add((parts[0], parts[1]))

    def close(self):
        if self.pack_zip:
            self.pack_zip.close()

    def _extract_pack(self, member: str, save_as: str) -> str | None:
        if not self.pack_zip or member not in self.pack_names:
            return None
        target = self.images_dir / f"{save_as}.png"
        with self.pack_zip.open(member) as src:
            target.write_bytes(src.read())
        return f"images/pokedex/{save_as}.png"

    def _fetch_pokeapi(self, dex_id: int, save_as: str, variant: str = "") -> str | None:
        """Fetch a sprite from PokeAPI. variant='' is the default front sprite;
        variant='shiny' uses the shiny subdirectory."""
        # PokeAPI uses the 10000-10999 range for regional / alternate-form
        # sprites (Alolan, Galarian, etc.) — those are valid even though the
        # base mainline range stops at 1010.
        if not self.enable_pokeapi or dex_id <= 0:
            return None
        if dex_id > 1010 and not (10000 <= dex_id <= 10999):
            return None
        target = self.images_dir / f"{save_as}.png"
        if target.exists():
            return f"images/pokedex/{save_as}.png"
        cache_key = (variant, dex_id)
        if self.pokeapi_tried.get(cache_key) is False:
            return None
        sub = f"{variant}/" if variant else ""
        url = f"{POKEAPI_SPRITE_BASE}/{sub}{dex_id}.png"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "PokefindWikiIngest/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                target.write_bytes(r.read())
            self.pokeapi_tried[cache_key] = True
            time.sleep(0.05)
            return f"images/pokedex/{save_as}.png"
        except urllib.error.HTTPError as e:
            self.pokeapi_tried[cache_key] = False
            if e.code != 404:
                print(f"  PokeAPI fetch {url}: HTTP {e.code}", file=sys.stderr)
            return None
        except Exception as e:
            self.pokeapi_tried[cache_key] = False
            print(f"  PokeAPI fetch {url}: {e}", file=sys.stderr)
            return None

    def has_skins_dir(self, skin: str, species_slug_candidates: list[str]) -> bool:
        """True iff any candidate slug appears as a directory under pokemon_skins/<skin>/."""
        for slug in species_slug_candidates:
            if (skin, slug) in self.skins_dirs:
                return True
        return False

    def has_pack_nested_shiny(self, dex_id: int, parent_skin: str) -> bool:
        return PACK_ICON_NESTED_SHINY.format(skin=parent_skin, id=dex_id) in self.pack_names

    def extract_pack_nested_shiny(self, dex_id: int, parent_skin: str, save_as: str) -> str | None:
        member = PACK_ICON_NESTED_SHINY.format(skin=parent_skin, id=dex_id)
        return self._extract_pack(member, save_as)

    def has_pack_skin(self, dex_id: int, skin: str) -> bool:
        return PACK_ICON_BASE.format(skin=skin, id=dex_id) in self.pack_names

    def has_bettermodel(self, species_slug: str, skin: str | None = None) -> bool:
        if skin is None or skin == "regular":
            return BETTERMODEL_BASE.format(slug=species_slug) in self.pack_names
        bm_skin = BETTERMODEL_SKIN_ALIAS.get(skin, skin)
        return BETTERMODEL_VARIANT.format(slug=species_slug, skin=bm_skin) in self.pack_names

    def extract_pack_skin(self, dex_id: int, skin: str, save_as: str) -> str | None:
        member = PACK_ICON_BASE.format(skin=skin, id=dex_id)
        return self._extract_pack(member, save_as)

    def extract_bettermodel(self, species_slug: str, save_as: str, skin: str | None = None) -> str | None:
        if skin is None or skin == "regular":
            member = BETTERMODEL_BASE.format(slug=species_slug)
        else:
            bm_skin = BETTERMODEL_SKIN_ALIAS.get(skin, skin)
            member = BETTERMODEL_VARIANT.format(slug=species_slug, skin=bm_skin)
        return self._extract_pack(member, save_as)

    def fetch_pokeapi(self, dex_id: int, save_as: str) -> str | None:
        return self._fetch_pokeapi(dex_id, save_as)

    def fetch_pokeapi_shiny(self, dex_id: int, save_as: str) -> str | None:
        return self._fetch_pokeapi(dex_id, save_as, variant="shiny")

    def render_from_models(self, dex_id: int, skin: str, species_name: str, save_as: str) -> str | None:
        """Render a 64x64 icon from the model JSON + textures in pokemon_skins/.
        Returns rel-URL on success, None if no model or render failed."""
        if not self.enable_render or not self.pack_zip or not isinstance(dex_id, int) or dex_id <= 0:
            return None
        target = self.images_dir / f"{save_as}.png"
        if target.exists():
            return f"images/pokedex/{save_as}.png"
        path = find_model_path(self.pack_zip, skin, dex_id, species_name)
        if not path:
            return None
        try:
            ok = render_model(self.pack_zip, path, target)
        except Exception as e:
            print(f"  render fail {path}: {e}", file=sys.stderr)
            return None
        if not ok:
            return None
        return f"images/pokedex/{save_as}.png"

    def model_url(self, dex_id: int, skin: str, species_name: str) -> str | None:
        """Resolve the URL of the per-skin model JSON inside static/models/, or None.
        Tier order (best quality first):
          1. bbmodel converted output — proper bone-rigged model from .bbmodel files
          2. pokemon_skins/<skin>/<id>_<species>.json — single-file static models
          3. bettermodel composite — assembled from multi-part files (no rig data)"""
        if not isinstance(dex_id, int) or dex_id <= 0:
            return None
        slug_candidates = [
            re.sub(r"[^a-z0-9]+", "_", species_name.lower()).strip("_"),
            re.sub(r"[^a-z0-9]+", "", species_name.lower()),
        ]

        # Tier 1: bbmodel converted output (rigged, properly positioned)
        # Only the Standard tab uses this — variants of bbmodel species fall
        # through to bettermodel composites for now (variant texture overrides
        # would require a follow-up).
        if skin == "regular":
            for slug in slug_candidates:
                if not slug:
                    continue
                cand = ROOT / f"static/models/bbmodel/{slug}.json"
                if cand.exists():
                    return f"/models/bbmodel/{slug}.json"

        # Tier 2: pokemon_skins/<skin>/<id>_<species>.json (must exist on disk)
        if self.pack_zip:
            path = find_model_path(self.pack_zip, skin, dex_id, species_name)
            if path:
                prefix = "assets/minecraft/models/pokemon_skins/"
                if path.startswith(prefix):
                    rel = path[len(prefix):]
                    local_path = ROOT / "static/models" / rel
                    if local_path.exists():
                        return f"/models/{rel}"

        # Tier 3: bettermodel composite at static/models/bettermodel/<slug>[_<variant>].json
        variant_alias = {
            "regular": None,
            "lunar_new_year": "lunar",
            "april_fools": "april",
            "sword_and_shield": "sword",
        }
        variant = variant_alias.get(skin, skin)
        for slug in slug_candidates:
            if not slug:
                continue
            if variant is None:
                candidate = ROOT / f"static/models/bettermodel/{slug}.json"
                if candidate.exists():
                    return f"/models/bettermodel/{slug}.json"
            else:
                candidate = ROOT / f"static/models/bettermodel/{slug}_{variant}.json"
                if candidate.exists():
                    return f"/models/bettermodel/{slug}_{variant}.json"
                base = ROOT / f"static/models/bettermodel/{slug}.json"
                if base.exists():
                    return f"/models/bettermodel/{slug}.json"
        return None


# ---------- Form payload assembly ----------

def species_form_data(species: dict) -> dict:
    abilities_dict = species.get("abilities", {}) or {}
    regular = [v for k, v in abilities_dict.items() if k != "h"]
    hidden = abilities_dict.get("h", "")
    moves = species.get("moves", {}) or {}
    sorted_moves = sorted(moves.items(), key=lambda kv: (kv[1], kv[0]))
    return {
        "types": [t.capitalize() for t in species.get("types", [])],
        "abilities": regular,
        "hidden_ability": hidden,
        "description": species.get("description", "") or "",
        "height_m": species.get("height", 0),
        "weight_kg": species.get("weight", 0),
        "egg_groups": species.get("egg_groups", []) or [],
        "egg_steps": species.get("egg_steps", 0) or 0,
        "growth_rate": species.get("growth_rate", "") or "",
        "base_stats": {
            "hp": species.get("hp", 0),
            "atk": species.get("attack", 0),
            "def": species.get("defense", 0),
            "spa": species.get("special_attack", 0),
            "spd": species.get("special_defense", 0),
            "spe": species.get("speed", 0),
        },
        "notable_moves": [enrich_move(m, level=lv) for m, lv in sorted_moves],
        "tms": [enrich_move(m) for m in sorted(species.get("machines", []) or [])],
        "tutor_moves": [enrich_move(m) for m in sorted(species.get("tutor_moves", []) or [])],
        "egg_moves": [enrich_move(m) for m in sorted(species.get("egg_moves", []) or [])],
    }


def enrich_move(name: str, level: int | None = None) -> dict:
    """Look up a move's metadata and return the enriched dict the layout uses."""
    info = MOVE_LOOKUP.get(name) or {}
    out = {
        "move": name,
        "type": info.get("type", ""),
        "category": info.get("category", ""),
        "power": info.get("power"),
        "accuracy": info.get("accuracy"),
        "pp": info.get("pp"),
    }
    if level is not None:
        out["level"] = level
    return out


def render_form_yaml(form_name: str, form: dict, sprite_rel: str | None, kind: str,
                     model_url: str | None = None, indent: str = "  ",
                     base_description: str = "") -> str:
    lines = []
    lines.append(f"{indent}- name: {yaml_string(form_name)}")
    lines.append(f"{indent}  kind: {yaml_string(kind)}")
    if model_url:
        lines.append(f"{indent}  model: {yaml_string(model_url)}")
    # Only emit a per-form description when it actually differs from the
    # base species' (the page's <h1> subtitle already shows the base copy).
    form_desc = (form.get("description") or "").strip()
    if form_desc and form_desc != base_description.strip():
        lines.append(f"{indent}  description: {yaml_string(form_desc)}")
    lines.append(f"{indent}  types: {yaml_list(form.get('types', []))}")
    lines.append(f"{indent}  abilities: {yaml_list(form.get('abilities', []))}")
    if form.get("hidden_ability"):
        lines.append(f"{indent}  hidden_ability: {yaml_string(form['hidden_ability'])}")
    sprite_yaml = yaml_string(sprite_rel) if sprite_rel else "''"
    lines.append(f"{indent}  sprite: {sprite_yaml}")
    if form.get("egg_groups"):
        lines.append(f"{indent}  egg_groups: {yaml_list(form['egg_groups'])}")
    if form.get("egg_steps"):
        lines.append(f"{indent}  egg_steps: {form['egg_steps']}")
    if form.get("growth_rate"):
        lines.append(f"{indent}  growth_rate: {yaml_string(form['growth_rate'])}")
    if form.get("height_m") is not None:
        lines.append(f"{indent}  height_m: {form.get('height_m', 0)}")
    if form.get("weight_kg") is not None:
        lines.append(f"{indent}  weight_kg: {form.get('weight_kg', 0)}")
    if form.get("note"):
        lines.append(f"{indent}  note: {yaml_string(form['note'])}")
    bs = form.get("base_stats") or {}
    lines.append(f"{indent}  base_stats:")
    for k in ("hp", "atk", "def", "spa", "spd", "spe"):
        lines.append(f"{indent}    {k}: {bs.get(k, 0)}")
    def emit_move_entry(entry: dict, ind: str, include_level: bool):
        lines.append(f"{ind}- move: {yaml_string(entry['move'])}")
        if include_level and entry.get("level") is not None:
            lines.append(f"{ind}  source: {yaml_string('Level ' + str(entry['level']))}")
        if entry.get("type"):
            lines.append(f"{ind}  type: {yaml_string(entry['type'])}")
        if entry.get("category"):
            lines.append(f"{ind}  category: {yaml_string(entry['category'])}")
        if entry.get("power") is not None:
            pw = "—" if entry["power"] in (0, None) else str(entry["power"])
            lines.append(f"{ind}  power: {yaml_string(pw)}")
        if entry.get("accuracy") is not None:
            acc = "∞" if entry["accuracy"] == 0 else str(entry["accuracy"])
            lines.append(f"{ind}  accuracy: {yaml_string(acc)}")
        if entry.get("pp") is not None:
            lines.append(f"{ind}  pp: {yaml_string(entry['pp'])}")

    # Per-form locations + competitive sets
    if form.get("locations"):
        lines.append(f"{indent}  locations: " + yaml_list(form["locations"]))
    if form.get("competitive_sets"):
        lines.append(f"{indent}  competitive_sets:")
        for s in form["competitive_sets"]:
            for sub in _render_set_yaml(s):
                lines.append(f"{indent}  {sub}")
    if form.get("notable_moves"):
        lines.append(f"{indent}  notable_moves:")
        for entry in form["notable_moves"]:
            emit_move_entry(entry, f"{indent}    ", include_level=True)
    if form.get("tms"):
        lines.append(f"{indent}  tms:")
        for entry in form["tms"]:
            emit_move_entry(entry, f"{indent}    ", include_level=False)
    if form.get("tutor_moves"):
        lines.append(f"{indent}  tutor_moves:")
        for entry in form["tutor_moves"]:
            emit_move_entry(entry, f"{indent}    ", include_level=False)
    if form.get("egg_moves"):
        lines.append(f"{indent}  egg_moves:")
        for entry in form["egg_moves"]:
            emit_move_entry(entry, f"{indent}    ", include_level=False)
    return "\n".join(lines)


def _scalar_or_list_yaml(value) -> str:
    """Smogon set fields can be a string or a list of alternatives. Render both."""
    if value is None or value == "":
        return "''"
    if isinstance(value, list):
        return "[" + ", ".join(yaml_string(str(x)) for x in value) + "]"
    return yaml_string(value)


def _render_set_yaml(s: dict) -> list[str]:
    out = [f"  - name: {yaml_string(s.get('name', ''))}"]
    if s.get("tier"):
        out.append(f"    tier: {yaml_string(s['tier'])}")
    if s.get("auto"):
        out.append("    auto: true")
    moves = s.get("moves") or []
    if moves:
        out.append("    moves:")
        for m in moves:
            if isinstance(m, list):
                out.append(f"      - {_scalar_or_list_yaml(m)}")
            else:
                out.append(f"      - {yaml_string(m)}")
    if s.get("ability"):
        out.append(f"    ability: {_scalar_or_list_yaml(s['ability'])}")
    if s.get("item"):
        out.append(f"    item: {_scalar_or_list_yaml(s['item'])}")
    if s.get("nature"):
        out.append(f"    nature: {_scalar_or_list_yaml(s['nature'])}")
    if s.get("evs"):
        evs = s["evs"]
        out.append("    evs:")
        for k in ("hp", "atk", "def", "spa", "spd", "spe"):
            if k in evs:
                out.append(f"      {k}: {evs[k]}")
    if s.get("ivs"):
        ivs = s["ivs"]
        out.append("    ivs:")
        for k in ("hp", "atk", "def", "spa", "spd", "spe"):
            if k in ivs:
                out.append(f"      {k}: {ivs[k]}")
    return out


def render_page(
    base_name: str,
    base_species: dict,
    forms_yaml: list[str],
    skins: list[str] | None = None,
    locations: list[str] | None = None,
    competitive_sets: list[dict] | None = None,
) -> str:
    description = _sanitize(base_species.get("description") or "").strip().replace("\n", " ")
    lines = ["---"]
    lines.append(f"title: {yaml_string(base_name)}")
    if description:
        lines.append(f"subtitle: {yaml_string(description)}")
    lines.append(f"date: {date.today().isoformat()}")
    lines.append(f"dex_number: {yaml_string(base_species.get('id', ''))}")
    lines.append(f"skins: {yaml_list(skins or [])}")
    lines.append("forms:")
    lines.extend(forms_yaml)
    lines.append("region: ''")
    # locations / competitive_sets are now per-form (inside each form entry)
    pass
    lines.append("anniversary: ''")
    lines.append("tier: ''")
    lines.append("video: ''")
    lines.append("---\n")
    return "\n".join(lines)


# ---------- Main ----------

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--species", type=Path, default=DEFAULT_SPECIES)
    p.add_argument("--keep-existing", action="store_true")
    p.add_argument("--include-gen6", action="store_true",
                   help="Keep gen 6 species (national-dex 650-721). Excluded by default.")
    p.add_argument("--include-gen7", action="store_true",
                   help="Keep gen 7 species (national-dex 722-809). Excluded by default.")
    p.add_argument("--no-sprites", action="store_true",
                   help="Skip PokeAPI sprite downloads (pack icons still extracted).")
    p.add_argument("--no-render", action="store_true",
                   help="Skip 3D-model rendering for missing icons.")
    p.add_argument("--pack", type=Path, default=DEFAULT_PACK,
                   help="Resource-pack zip with pokemon_skin_icons.")
    args = p.parse_args()

    if not args.species.exists():
        print(f"species file not found: {args.species}", file=sys.stderr)
        return 1

    species_list = json.loads(args.species.read_text())
    print(f"Loaded {len(species_list)} species from {args.species}")

    global MOVE_LOOKUP
    MOVE_LOOKUP = load_move_lookup(DEFAULT_MOVES_DATA)
    if MOVE_LOOKUP:
        print(f"Loaded {len(MOVE_LOOKUP)} move records for level-up table enrichment")
    else:
        print("WARNING: moves data not found — level-up rows will lack power/accuracy/PP", file=sys.stderr)

    # Spawn locations, Smogon competitive sets, and anniversary safari spawns
    try:
        from build_pokedex_extras import (
            parse_map_yml, build_region_to_towns, parse_spawn_rates,
            species_locations, load_smogon_sets, fallback_set,
            parse_safari_anniversary_spawns,
            MAP_YML, SPAWN_CSV, ANNI_SAFARI,
        )
        map_data = parse_map_yml(MAP_YML) if MAP_YML.exists() else {}
        region_to_towns = build_region_to_towns(map_data) if map_data else {}
        spawn_data = parse_spawn_rates(SPAWN_CSV) if SPAWN_CSV.exists() else {}
        smogon_sets = load_smogon_sets()
        safari_anniversary_set = parse_safari_anniversary_spawns(ANNI_SAFARI)
        print(f"Loaded extras: {len(map_data)} map regions, {len(spawn_data)} species in spawn data, "
              f"{len(smogon_sets)} species with Smogon sets, "
              f"{len(safari_anniversary_set)} anniversary species in safari script")
    except Exception as e:
        print(f"WARNING: extras data unavailable ({e}) — locations/sets will be empty", file=sys.stderr)
        spawn_data, region_to_towns, smogon_sets, safari_anniversary_set = {}, {}, {}, set()
        species_locations = lambda *a, **k: []
        fallback_set = lambda *a, **k: None

    # Filter gen 6 / gen 7 / orphan-negative-id species
    # Negative-id species are server-custom regional variants. Keep those whose name
    # starts with a recognized prefix (they merge into base species as form tabs).
    # Drop the rest (standalone server-custom anniversaries like Goard, Frostfang, etc.)
    excluded_gen6 = 0
    excluded_gen7 = 0
    excluded_orphan_negative = 0
    kept: list[dict] = []
    for s in species_list:
        sid = s.get("id")
        if isinstance(sid, int) and 650 <= sid <= 721 and not args.include_gen6:
            excluded_gen6 += 1
            continue
        if isinstance(sid, int) and 722 <= sid <= 809 and not args.include_gen7:
            excluded_gen7 += 1
            continue
        if isinstance(sid, int) and sid < 0:
            first = (s.get("name") or "").strip().split(" ", 1)[0]
            if first not in REGIONAL_PREFIXES:
                excluded_orphan_negative += 1
                continue
        kept.append(s)
    species_list = kept
    print(f"Filtered: gen6={excluded_gen6} gen7={excluded_gen7} orphan-negative={excluded_orphan_negative}")
    print(f"  {len(species_list)} species remain")

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Group species by base name + form prefix
    grouped: dict[str, dict[str, dict]] = {}
    for s in species_list:
        base, form = detect_form(s["name"])
        grouped.setdefault(base, {})[form] = s

    print(f"Grouped into {len(grouped)} base entries.")

    sprite_cache = SpriteCache(
        pack_path=args.pack,
        enable_pokeapi=not args.no_sprites,
        enable_render=not args.no_render,
    )
    if not args.no_render and not RENDERER_AVAILABLE:
        print("WARNING: numpy/Pillow unavailable — rendering tier disabled", file=sys.stderr)

    # Collect every move + ability name encountered, classified as kind.
    # Used to auto-generate stub pages under content/moves/.
    encountered: dict[str, str] = {}   # name -> kind ("move" | "ability")
    def note_move(name: str):
        if name and name not in encountered:
            encountered[name] = "move"
    def note_ability(name: str):
        if name and name not in encountered:
            encountered[name] = "ability"
    def harvest(form_data: dict | None):
        if not form_data:
            return
        for a in form_data.get("abilities", []) or []:
            note_ability(a)
        if form_data.get("hidden_ability"):
            note_ability(form_data["hidden_ability"])
        for m in form_data.get("notable_moves", []) or []:
            note_move(m.get("move"))
        for m in form_data.get("tms", []) or []:
            note_move(m.get("move") if isinstance(m, dict) else m)
        for m in form_data.get("tutor_moves", []) or []:
            note_move(m.get("move") if isinstance(m, dict) else m)
        for m in form_data.get("egg_moves", []) or []:
            note_move(m.get("move") if isinstance(m, dict) else m)

    written = 0
    skipped_existing = 0
    used_slugs: set[str] = set()
    collisions: list[tuple[str, str]] = []
    sprite_sources: dict[str, int] = {
        "pack-regular": 0,
        "bettermodel-base": 0,
        "pokeapi": 0,
        "none": 0,
    }
    skins_count_total = 0

    for base_name, form_map in grouped.items():
        cslug = content_slug(base_name)
        if cslug in used_slugs:
            base_species = next(iter(form_map.values()))
            raw_id = base_species.get("id", "?")
            id_part = f"n{abs(raw_id)}" if isinstance(raw_id, int) and raw_id < 0 else str(raw_id)
            cslug = f"{cslug}-id{id_part}"
            collisions.append((base_name, cslug))
        used_slugs.add(cslug)

        md_path = CONTENT_DIR / f"{cslug}.md"
        if args.keep_existing and md_path.exists():
            skipped_existing += 1
            continue

        standard_record = form_map.get("Standard")
        standard_id = standard_record.get("id") if standard_record else None
        standard_data = species_form_data(standard_record) if standard_record else None

        # ---- Single Standard sprite: pack regular icon → bettermodel → PokeAPI ----
        rel = None
        source = "none"
        if standard_record is not None and isinstance(standard_id, int) and standard_id > 0:
            species_slug = texture_slug(standard_record["name"].strip())
            save_as = content_slug(base_name)
            if sprite_cache.has_pack_skin(standard_id, "regular"):
                rel = sprite_cache.extract_pack_skin(standard_id, "regular", save_as)
                source = "pack-regular"
            elif sprite_cache.has_bettermodel(species_slug, "regular"):
                rel = sprite_cache.extract_bettermodel(species_slug, save_as, "regular")
                source = "bettermodel-base"
            else:
                rel = sprite_cache.fetch_pokeapi(standard_id, save_as)
                if rel:
                    source = "pokeapi"
        sprite_sources[source] = sprite_sources.get(source, 0) + 1

        # ---- Cosmetic skins list (no stat changes) ----
        skins: list[str] = []
        if standard_record is not None and isinstance(standard_id, int) and standard_id > 0:
            slug_candidates = skins_dir_candidates(standard_record["name"])
            for skin in COSMETIC_SKINS:
                if skin == "regular":
                    continue
                if sprite_cache.has_pack_skin(standard_id, skin) or \
                   sprite_cache.has_skins_dir(skin, slug_candidates):
                    skins.append(skin_label(skin))
        skins_count_total += len(skins)

        # ---- Forms (stat-changing variants) — re-emitted as tabs ----
        forms_yaml: list[str] = []
        base_description = ""

        # Standard form: spawn-region locations + Smogon sets (with auto-built fallback)
        if standard_data is not None:
            harvest(standard_data)
            standard_data["locations"] = species_locations(base_name, spawn_data, region_to_towns)
            std_sets = list(smogon_sets.get(base_name, []))
            if not std_sets:
                fb = fallback_set(base_name, standard_data.get("notable_moves") or [],
                                  standard_data.get("base_stats"))
                if fb:
                    std_sets = [fb]
            standard_data["competitive_sets"] = std_sets
            base_description = (standard_data.get("description") or "").strip()
            forms_yaml.append(render_form_yaml("Standard", standard_data, rel, kind="form",
                                                base_description=base_description))

        # Regional forms (Kyoto / Jataro / Haikou / Shiloh / Zeinova / Alolan / Galarian)
        for prefix in REGIONAL_PREFIXES:
            if prefix not in form_map:
                continue
            species_record = form_map[prefix]
            form_data = species_form_data(species_record)
            harvest(form_data)
            full_name = species_record["name"].strip()
            # Anniversary forms (Kyoto/Jataro/Haikou/Shiloh/Zeinova): location =
            # safari script if present, otherwise empty. Alolan/Galarian don't
            # spawn in the safari and have no spawn-region data.
            if full_name in safari_anniversary_set:
                form_data["locations"] = ["Sometimes found in the Safari Zone during anniversary events"]
            else:
                form_data["locations"] = []
            # Anniversary/regional forms get an auto-built set from THEIR own
            # movepool (not the base form's). Smogon doesn't publish anniversary
            # sets, so fallback is the only option here.
            fb = fallback_set(full_name, form_data.get("notable_moves") or [],
                              form_data.get("base_stats"))
            form_data["competitive_sets"] = [fb] if fb else []
            # Try PokeAPI for Alolan / Galarian / Hisuian / Paldean forms.
            # Anniversary regional prefixes (Kyoto, Jataro, etc.) have no
            # upstream sprite — the lookup just returns None and we fall back
            # to the (no sprite) placeholder, same as before.
            form_sprite = None
            form_id = POKEAPI_FORM_IDS.get((base_name, prefix))
            if form_id:
                save_as = f"{content_slug(base_name)}-{prefix.lower()}"
                form_sprite = sprite_cache.fetch_pokeapi(form_id, save_as)
            forms_yaml.append(render_form_yaml(prefix, form_data, form_sprite, kind="form",
                                                base_description=base_description))

        # Manually-injected forms (Kyurem Black/White, Meloetta Pirouette, etc.)
        if base_name in EXTRA_FORMS:
            base_species = standard_record or next(iter(form_map.values()))
            for extra in EXTRA_FORMS[base_name]:
                merged = {
                    "egg_groups": base_species.get("egg_groups", []) or [],
                    "growth_rate": base_species.get("growth_rate", "") or "",
                    "height_m": base_species.get("height", 0),
                    "weight_kg": base_species.get("weight", 0),
                    "notable_moves": [],
                    **extra,
                }
                expected_filename = f"{content_slug(base_name)}{extra['sprite_suffix']}.png"
                manual_path = IMAGES_DIR / expected_filename
                if not manual_path.exists():
                    src_filename = TOXIC_FORM_FILES.get((base_name, extra["name"]))
                    if src_filename:
                        src = TOXIC_PACK_REGULAR / src_filename
                        if src.exists():
                            manual_path.parent.mkdir(parents=True, exist_ok=True)
                            manual_path.write_bytes(src.read_bytes())
                form_sprite = f"images/pokedex/{expected_filename}" if manual_path.exists() else None
                harvest(merged)
                forms_yaml.append(render_form_yaml(extra["name"], merged, form_sprite, kind="form",
                                                    base_description=base_description))

        base_species = form_map.get("Standard") or next(iter(form_map.values()))
        md = render_page(base_name, base_species, forms_yaml, skins=skins)
        md_path.write_text(md, encoding="utf-8")
        written += 1

    sprite_cache.close()

    # ---- Auto-generate stub pages for every move + ability encountered ----
    MOVES_CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    moves_written = 0
    moves_skipped = 0
    for name in sorted(encountered):
        kind = encountered[name]
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        if not slug:
            continue
        target = MOVES_CONTENT_DIR / f"{slug}.md"
        if target.exists():
            moves_skipped += 1
            continue
        lines = ["---"]
        lines.append(f"title: {yaml_string(name)}")
        # `kind` is reserved by Hugo for content-type classification; use a
        # different field name to avoid colliding with the engine.
        lines.append(f"entry_kind: {yaml_string(kind)}")
        lines.append(f"date: {date.today().isoformat()}")
        if kind == "move":
            lines.append("type: ''           # e.g. 'Fire'")
            lines.append("category: ''       # 'Physical', 'Special', or 'Status'")
            lines.append("power: ''          # numeric power (or empty for status)")
            lines.append("accuracy: ''       # numeric accuracy")
            lines.append("pp: ''             # base PP")
            lines.append("priority: ''       # priority bracket (default 0)")
            lines.append("contact: ''        # 'Yes' or 'No'")
            lines.append("effect: ''         # one-line effect summary")
        else:
            lines.append("type: ''           # leave empty for abilities")
            lines.append("effect: ''         # one-line effect summary")
        lines.append("---\n\n## Description\n\n## Mechanics on Pokefind\n")
        target.write_text("\n".join(lines), encoding="utf-8")
        moves_written += 1

    print(f"Moves/abilities encountered: {len(encountered)} ({moves_written} stubs written, {moves_skipped} pre-existing)")

    avg_skins = skins_count_total / max(written, 1)
    print(f"Wrote {written} pokedex pages, {skins_count_total} total skin entries (avg {avg_skins:.1f}/species)")
    if skipped_existing:
        print(f"Skipped {skipped_existing} existing files (--keep-existing)")
    print("Sprite sources:")
    for src, n in sprite_sources.items():
        print(f"  {src:<18} {n}")
    if collisions:
        print(f"{len(collisions)} slug collisions disambiguated by dex id:")
        for original, slug in collisions[:10]:
            print(f"  {original!r} -> {slug}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
