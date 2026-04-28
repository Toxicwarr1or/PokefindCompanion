#!/usr/bin/env python3
"""
Walk the LitePack resource pack's pokemon_skins/ directory and emit
content/skins/_index.md with the full {skin_name: [species, ...]} catalog
for the Skins layout to render.

Each subdirectory under pokemon_skins/ is a skin variant (alolan, shiny,
shadow, etc.); its child folders are the Pokémon species that have an
entry for that skin.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

# `devhelditem.zip` is the live in-game pack — extract it via:
#   unzip -q -o ~/.minecraft/resourcepacks/devhelditem.zip -d /tmp/devhelditem
# Re-extract whenever the user updates it.
PACK_ROOT = Path("/tmp/devhelditem/assets/minecraft")
TEXTURES_DIR = PACK_ROOT / "textures/pokemon_skins"
MODELS_DIR = PACK_ROOT / "models/pokemon_skins"
WIKI_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = WIKI_ROOT / "content/skins/_index.md"

# Skins to skip when emitting:
#   regular           — baseline texture every Pokémon has (noise)
#   shiny             — too noisy, every species has one (per user)
#   ssundee_galarian  — content-creator one-off, dropped per user
#   woc_models        — War of Crypto custom models, dropped per user
#   pokemon_skins     — leftover misc subfolder, not a real skin set
EXCLUDE_SKINS = {
    "regular", "shiny", "ssundee_galarian", "woc_models", "pokemon_skins",
    # Random is dissolved — its species are reassigned via SYNTHETIC_SKINS
    # / SKIN_MERGE below; nothing should land in a "Random" tab.
    "random",
    # Cakemon == April Fools (per user); just keep April Fools.
    "cakemon",
}

# Per-skin entries to drop. Keys are the resource pack folder name; values
# are the species-folder names that should NOT appear under that skin.
EXCLUDE_PER_SKIN = {
    "starwars":          {"chebacca", "chewbacca", "jedi", "stormtrooper"},
    "galarian":          {"shiny"},
    "alolan":            {"old", "shiny"},
    "anniversary_shiny": {"shiny"},
}

# Source-skin → destination-skin merges. The source folder's species get
# folded into the destination tab and the source folder no longer appears
# as its own tab.
SKIN_MERGE = {
    "avengers": "marvel",   # Avengers is a Marvel subset; merged
    "surfing":  "summer",   # Surfing skins released alongside Summer events
}

# Hand-assigned species for synthetic skin categories that don't have their
# own folder in the resource pack. Each entry is {label, description, species[]}.
# Species names use the same folder/slug convention as the rest of the script.
SYNTHETIC_SKINS = {
    "detective": {
        "label": "Detective",
        "description": "Detective-themed reskins (movie tie-in).",
        "species": ["pikachu", "raichu"],
    },
    "stone": {
        "label": "Stone",
        "description": "Stone / statue-form reskins.",
        "species": ["dialga"],
    },
}

# Folders inside the source pack we should never surface as species (they're
# placeholders / shared assets, not real Pokémon).
EXCLUDE_SPECIES_FOLDERS = {"statue"}

# Display names for each skin folder.
SKIN_DISPLAY = {
    "alolan":            "Alolan",
    "anniversary":       "Anniversary",
    "anniversary_shiny": "Shiny Anniversary",
    "april_fools":       "April Fools",
    "aura":              "Aura",
    "avengers":          "Avengers",
    "cakemon":           "Cakemon",
    "christmas":         "Christmas",
    "cosmic":            "Cosmic",
    "disney":            "Disney",
    "easter":            "Easter",
    "fusemon":           "Fusemon",
    "galarian":          "Galarian",
    "gamer":             "Gamer",
    "halloween":         "Halloween",
    "lunar_new_year":    "Lunar New Year",
    "marvel":            "Marvel",
    "mecha":             "Mecha",
    "meme":              "Meme",
    "modeler":           "Modeler",
    "monochrome":        "Monochrome",
    "random":            "Random",
    "shadow":            "Shadow",
    "starwars":          "Star Wars",
    "summer":            "Summer",
    "surfing":           "Surfing",
    "sword_and_shield":  "Sword & Shield",
    "thanksgiving":      "Thanksgiving",
    "valentine":         "Valentine",
}

# One-line description per skin so the section makes sense at a glance.
SKIN_DESCRIPTION = {
    "alolan":            "Tropical regional variants from the Alola region.",
    "anniversary":       "Server-anniversary recolors — limited drops from past anniversaries.",
    "anniversary_shiny": "Shiny variants of the anniversary recolors. Even rarer.",
    "april_fools":       "April Fools event reskins.",
    "aura":              "Aura skins — visual aura effect overlaid on the species' default model.",
    "avengers":          "Marvel-Avengers themed crossover skins.",
    "cakemon":           "Cake-themed reskins from a past April Fools.",
    "christmas":         "Holiday-themed reskins from past Christmas events.",
    "cosmic":            "Cosmic / space-themed reskins from the Cosmic Discovery arc.",
    "disney":            "Disney-themed crossover skins.",
    "easter":            "Spring / Easter event reskins, including the safari hunts.",
    "fusemon":           "Fusion skins — two species visually combined.",
    "galarian":          "Regional variants from the Galar region.",
    "gamer":             "Video-game / gamer culture themed reskins.",
    "halloween":         "Spooky reskins released during past Halloween events.",
    "lunar_new_year":    "Lunar New Year event skins.",
    "marvel":            "Marvel-character crossover skins (separate from the Avengers set).",
    "mecha":             "Mech / robot styled reskins.",
    "meme":              "Meme / joke skins.",
    "modeler":           "Custom modeler showcase skins.",
    "monochrome":        "Monochrome (black-and-white) reskins.",
    "random":            "Miscellaneous one-off skins.",
    "shadow":            "Shadow Pokémon — corrupted forms tied to the Shadow quest arcs.",
    "starwars":          "Star Wars-themed crossover skins.",
    "summer":            "Summer event reskins (beach, swim, etc.).",
    "surfing":           "Surfing-themed reskins.",
    "sword_and_shield":  "Sword & Shield-themed reskins.",
    "thanksgiving":      "Thanksgiving event reskins.",
    "valentine":         "Valentine event reskins (pinks, roses, etc.).",
}


def species_display(folder_name: str) -> str:
    """Pretty-print a species folder name (e.g. mrmime → 'Mr. Mime',
    nidoranf → 'Nidoran-F', alolan_exeggutor → 'Exeggutor')."""
    name = folder_name
    # Strip a leading regional prefix if it leaked into the species folder
    for prefix in ("alolan_", "galarian_"):
        if name.startswith(prefix):
            name = name[len(prefix):]
    # Specific renames
    specials = {
        "mrmime":      "Mr. Mime",
        "mr_mime":     "Mr. Mime",
        "nidoranf":    "Nidoran-F",
        "nidoran_f":   "Nidoran-F",
        "nidoranm":    "Nidoran-M",
        "nidoran_m":   "Nidoran-M",
        "farfetchd":   "Farfetch'd",
        "ho-oh":       "Ho-Oh",
        "hooh":        "Ho-Oh",
        "porygonz":    "Porygon-Z",
        "porygon2":    "Porygon2",
        "mimejr":      "Mime Jr.",
    }
    if name.lower() in specials:
        return specials[name.lower()]
    # Capitalize each underscore-separated word
    return " ".join(w.capitalize() for w in name.replace("-", " ").replace("_", " ").split())


def species_slug(folder_name: str) -> str:
    """Best-effort URL slug matching the wiki's pokedex pages."""
    name = folder_name.lower()
    for prefix in ("alolan_", "galarian_"):
        if name.startswith(prefix):
            name = name[len(prefix):]
    return re.sub(r"[^a-z0-9]+", "-", name).strip("-")


def yaml_string(value) -> str:
    s = "" if value is None else str(value)
    return "'" + s.replace("'", "''") + "'"


_MODEL_NAME_RE = re.compile(r"^\d{1,4}_([a-z][a-z0-9_]*?)(?:_\w+)?\.json$", re.IGNORECASE)


def species_for_skin(skin_name: str) -> list[str]:
    """Return the deduped set of species folder names that have any asset
    (texture or model) under this skin. Walks both trees recursively to
    capture region-grouped layouts (e.g. anniversary/zeinova/charizard)."""
    skin_excludes = EXCLUDE_PER_SKIN.get(skin_name, set())
    found: set[str] = set()
    for root in (TEXTURES_DIR / skin_name, MODELS_DIR / skin_name):
        if not root.exists():
            continue
        # Texture trees: each LEAF directory is a species.
        for d in root.rglob("*"):
            if d.is_dir():
                # Treat as a species folder if it has no further subdirs.
                if not any(c.is_dir() for c in d.iterdir()):
                    if d.name not in EXCLUDE_SPECIES_FOLDERS and d.name not in skin_excludes:
                        found.add(d.name)
        # Model trees: each <dex>_<species>.json file names a species.
        for f in root.rglob("*.json"):
            m = _MODEL_NAME_RE.match(f.name)
            if m:
                name = m.group(1).lower()
                if name not in EXCLUDE_SPECIES_FOLDERS and name not in skin_excludes:
                    found.add(name)
    return sorted(found)


def main() -> int:
    if not TEXTURES_DIR.exists() and not MODELS_DIR.exists():
        print(f"Resource pack not found under {PACK_ROOT}", file=sys.stderr)
        return 1
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Union all skin folders that exist in either tree.
    all_skins: set[str] = set()
    for root in (TEXTURES_DIR, MODELS_DIR):
        if root.exists():
            for d in root.iterdir():
                if d.is_dir():
                    all_skins.add(d.name)

    # First pass: collect raw species per skin folder, applying merges.
    #   - EXCLUDE_SKINS folders are dropped entirely
    #   - SKIN_MERGE folders are folded into their destination's species set
    raw: dict[str, set[str]] = {}
    for name in sorted(all_skins):
        if name in EXCLUDE_SKINS:
            continue
        target = SKIN_MERGE.get(name, name)
        raw.setdefault(target, set()).update(species_for_skin(name))

    # Layer in synthetic categories (Detective, Stone, etc.).
    for synth_key, synth in SYNTHETIC_SKINS.items():
        raw.setdefault(synth_key, set()).update(synth["species"])

    # Build the structured list.
    skin_data: list[dict] = []
    for name in sorted(raw.keys()):
        names = sorted(raw[name])
        if not names:
            continue
        synth = SYNTHETIC_SKINS.get(name)
        species = [{
            "folder": n,
            "name": species_display(n),
            "slug": species_slug(n),
        } for n in names]
        skin_data.append({
            "key": name,
            "label": (synth["label"] if synth else
                      SKIN_DISPLAY.get(name, name.replace("_", " ").title())),
            "description": (synth["description"] if synth else
                            SKIN_DESCRIPTION.get(name, "")),
            "count": len(species),
            "species": species,
        })

    lines = ["---"]
    lines.append("title: 'Skins'")
    lines.append("subtitle: 'Every alternate-look variant for the Pokemon in Pokefind'")
    lines.append(f"date: {date.today().isoformat()}")
    lines.append("layout: skinslist")
    lines.append("skins:")
    for s in skin_data:
        lines.append(f"  - key: {yaml_string(s['key'])}")
        lines.append(f"    label: {yaml_string(s['label'])}")
        if s["description"]:
            lines.append(f"    description: {yaml_string(s['description'])}")
        lines.append(f"    count: {s['count']}")
        lines.append("    species:")
        for sp in s["species"]:
            lines.append(f"      - name: {yaml_string(sp['name'])}")
            lines.append(f"        slug: {yaml_string(sp['slug'])}")
    lines.append("---\n")
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")
    print("Skin | species count")
    for s in skin_data:
        print(f"  {s['label']:<22} {s['count']:>4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
