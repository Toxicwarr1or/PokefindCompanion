#!/usr/bin/env python3
"""
Extract Pokemon model JSONs and texture PNGs from the resource pack into
static/models/ and static/textures/ for the in-browser 3D viewer.

Mirrors the resource-pack tree under those directories:
    pack: assets/minecraft/models/pokemon_skins/<skin>/<id>_<species>.json
       -> static/models/<skin>/<id>_<species>.json
    pack: assets/minecraft/textures/pokemon_skins/<skin>/<species>/<part>.png
       -> static/textures/pokemon_skins/<skin>/<species>/<part>.png

The texture path inside the model JSON (e.g., "pokemon_skins/regular/pikachu/pikachu")
is the canonical key the viewer uses to resolve the URL — the script preserves it.

Usage:
    python3 scripts/extract_models.py [--pack PATH]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PACK = Path("/home/jack/.minecraft/resourcepacks/devhelditem.zip")
DEFAULT_SPECIES = Path("/home/jack/Downloads/species_gen6.json")
MODELS_OUT = ROOT / "static/models"
TEXTURES_OUT = ROOT / "static/textures"

MODELS_PREFIX = "assets/minecraft/models/pokemon_skins/"
TEXTURES_PREFIX = "assets/minecraft/textures/"
BETTERMODEL_PREFIX = "assets/bettermodel/models/modern_item/"
BETTERMODEL_TEX_PREFIX = "assets/bettermodel/textures/"


def species_slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


# Known variant tokens used as either `_v_<variant>_` infixes or trailing `_<variant>_index`
# suffixes in bettermodel filenames. Anything matching is excluded from the base-form set.
VARIANT_TOKENS = {
    "shiny", "halloween", "easter", "christmas", "anniversary", "aura", "valentine",
    "shadow", "summer", "meme", "thanksgiving", "cosmic", "sword", "monochrome",
    "flame", "fan", "frost", "heat", "mow", "wash", "sky", "xmas", "alola",
    "galarian", "hisui", "paldea", "fusemon", "marvel", "modeler", "mecha",
    "gamer", "lunar", "april", "disney", "starwars",
}


def is_base_part(filename: str, slug: str) -> bool:
    """A bettermodel filename is a base-form part of `slug` iff:
       - starts with `<slug>_`
       - has no `_v_<variant>_` infix
       - the segments after `<slug>_` and before the trailing `_<index>` contain
         no known variant token
    """
    if not filename.startswith(slug + "_"):
        return False
    rest = filename[len(slug) + 1:]   # everything after slug_
    rest = rest.rsplit("_", 1)[0]     # drop trailing _<index>
    if not rest:
        return False
    if "_v_" in f"_{rest}_":
        return False
    segments = rest.split("_")
    for seg in segments:
        if seg in VARIANT_TOKENS:
            return False
    return True


def is_variant_part(filename: str, slug: str, variant: str) -> bool:
    """A bettermodel filename is a `variant`-specific part of `slug` iff:
       - starts with `<slug>_v_<variant>_`  (dedicated variant part), OR
       - starts with `<slug>_` and contains `_<variant>_<index>` at the tail
         (per-part costume override)
    """
    if filename.startswith(f"{slug}_v_{variant}_"):
        return True
    if filename.startswith(f"{slug}_"):
        rest = filename[len(slug) + 1:]
        rest_no_idx = rest.rsplit("_", 1)[0]
        if rest_no_idx.endswith(f"_{variant}") or rest_no_idx == variant:
            return True
    return False


def merge_models(zf: zipfile.ZipFile, member_paths: list[str]) -> dict | None:
    """Combine multiple bettermodel JSON files into one model. Each file's
    elements get appended; texture refs union into one dict (later parts win on
    key collisions, which is the desired behavior for variant overrides)."""
    elements: list = []
    textures: dict = {}
    for path in member_paths:
        try:
            with zf.open(path) as f:
                data = json.load(f)
        except Exception:
            continue
        for el in data.get("elements", []) or []:
            elements.append(el)
        for k, v in (data.get("textures") or {}).items():
            textures[k] = v
    if not elements:
        return None
    return {"textures": textures, "elements": elements}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    p.add_argument("--species", type=Path, default=DEFAULT_SPECIES,
                   help="species JSON, used to compute slugs for bettermodel grouping.")
    args = p.parse_args()

    if not args.pack.exists():
        print(f"pack not found: {args.pack}", file=sys.stderr)
        return 1

    MODELS_OUT.mkdir(parents=True, exist_ok=True)
    TEXTURES_OUT.mkdir(parents=True, exist_ok=True)

    models_extracted = 0
    textures_referenced: set[str] = set()
    bad_models = 0

    with zipfile.ZipFile(args.pack) as zf:
        # Model JSONs
        for name in zf.namelist():
            if not name.startswith(MODELS_PREFIX):
                continue
            if not name.endswith(".json"):
                continue
            rel = name[len(MODELS_PREFIX):]   # e.g. "regular/25_pikachu.json"
            out = MODELS_OUT / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            try:
                with zf.open(name) as src:
                    data = src.read()
                # Validate JSON; collect texture refs
                model = json.loads(data)
                if not model.get("elements"):
                    # Skip parent-only billboard models — viewer can't render them
                    bad_models += 1
                    continue
                for tex_ref in (model.get("textures") or {}).values():
                    textures_referenced.add(tex_ref)
                out.write_bytes(data)
                models_extracted += 1
            except Exception as e:
                print(f"  bad model {name}: {e}", file=sys.stderr)
                bad_models += 1

        # Textures referenced by extracted models
        textures_extracted = 0
        textures_missing: list[str] = []
        for ref in sorted(textures_referenced):
            # ref is like "pokemon_skins/regular/pikachu/pikachu" — append .png
            member = f"{TEXTURES_PREFIX}{ref}.png"
            if member not in zf.namelist():
                textures_missing.append(ref)
                continue
            out = TEXTURES_OUT / f"{ref}.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as src:
                out.write_bytes(src.read())
            textures_extracted += 1

    print(f"Extracted {models_extracted} models (skipped {bad_models} parent-only billboards)")
    print(f"Extracted {textures_extracted} textures ({len(textures_missing)} referenced but missing in pack)")
    if textures_missing:
        report = ROOT / "scripts/missing_viewer_textures.txt"
        report.write_text("\n".join(textures_missing) + "\n")
        print(f"Missing-texture list: {report}")

    # ---- Bettermodel: group parts by species/variant and merge into single files ----
    if args.species.exists():
        species_list = json.loads(args.species.read_text())
        # Sort slugs longest-first so multi-word species (alolan_exeggutor) match
        # before single-word substrings (exeggutor).
        all_slugs = sorted(
            {species_slug(s["name"]) for s in species_list if s.get("name")},
            key=len, reverse=True,
        )
        with zipfile.ZipFile(args.pack) as zf:
            bm_members = [n for n in zf.namelist()
                          if n.startswith(BETTERMODEL_PREFIX) and n.endswith(".json")]
            bm_filenames = {n: n[len(BETTERMODEL_PREFIX):-5] for n in bm_members}

            # Map each filename to the longest matching species slug
            file_to_slug: dict[str, str] = {}
            for path, fname in bm_filenames.items():
                for slug in all_slugs:
                    if fname.startswith(slug + "_"):
                        file_to_slug[path] = slug
                        break

            # Group base parts per species
            base_groups: dict[str, list[str]] = {}
            for path, slug in file_to_slug.items():
                fname = bm_filenames[path]
                if is_base_part(fname, slug):
                    base_groups.setdefault(slug, []).append(path)

            bm_models_written = 0
            bm_textures_referenced: set[str] = set()
            bm_out = MODELS_OUT / "bettermodel"
            bm_out.mkdir(parents=True, exist_ok=True)

            for slug, parts in base_groups.items():
                merged = merge_models(zf, sorted(parts))
                if not merged:
                    continue
                target = bm_out / f"{slug}.json"
                target.write_text(json.dumps(merged))
                bm_models_written += 1
                for ref in merged.get("textures", {}).values():
                    bm_textures_referenced.add(ref)

            # Group variant parts per (species, variant)
            variant_groups: dict[tuple[str, str], list[str]] = {}
            for path, slug in file_to_slug.items():
                fname = bm_filenames[path]
                for variant in VARIANT_TOKENS:
                    if is_variant_part(fname, slug, variant):
                        variant_groups.setdefault((slug, variant), []).append(path)

            bm_variant_written = 0
            for (slug, variant), parts in variant_groups.items():
                # Variant model = base parts + variant parts (variant wins on overlap)
                base_parts = base_groups.get(slug, [])
                # Filter base parts that ARE overridden by variant parts (same suffix structure)
                # For simplicity, just include all base parts then all variant parts; later
                # elements just overlap geometrically — visually fine for icons.
                merged = merge_models(zf, sorted(base_parts) + sorted(parts))
                if not merged:
                    continue
                target = bm_out / f"{slug}_{variant}.json"
                target.write_text(json.dumps(merged))
                bm_variant_written += 1
                for ref in merged.get("textures", {}).values():
                    bm_textures_referenced.add(ref)

            # Extract bettermodel textures referenced by any merged model
            bm_textures_out = TEXTURES_OUT / "bettermodel"
            bm_tex_extracted = 0
            for ref in sorted(bm_textures_referenced):
                # Refs look like 'bettermodel:item/charizard_charizard'.
                # Map to assets/bettermodel/textures/item/charizard_charizard.png
                m = re.match(r"bettermodel:(.+)", ref)
                rel = m.group(1) if m else ref
                member = f"{BETTERMODEL_TEX_PREFIX}{rel}.png"
                if member not in zf.namelist():
                    continue
                target = bm_textures_out / f"{rel}.png"
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src:
                    target.write_bytes(src.read())
                bm_tex_extracted += 1

            print(f"Bettermodel: {bm_models_written} base models, {bm_variant_written} variant models, "
                  f"{bm_tex_extracted} textures")

    # Final size summary
    def dir_size(p: Path) -> int:
        return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
    print(f"static/models/   = {dir_size(MODELS_OUT) / 1024 / 1024:.1f} MB")
    print(f"static/textures/ = {dir_size(TEXTURES_OUT) / 1024 / 1024:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
