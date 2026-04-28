#!/usr/bin/env python3
"""
Stage 3D-viewer assets for the Pokefind wiki. Three sources are processed:

  1. Static cuboid models in `pokemon_skins/regular/<dex>_<species>.json`
     → Standard form's viewer, served from static/models-3d/regular/<slug>/.

  2. Static cuboid models in `pokemon_skins/{alolan,galarian}/...`
     → form-tab viewers under static/models-3d/{alolan,galarian}/<slug>/.

  3. BetterModel rigs in `bettermodel/models/modern_item/<species>_<part>_1.json`
     for species whose regular/ JSON is just a 140-byte placeholder
     (Charizard, Blastoise, Venusaur, etc.). All non-skin-variant parts are
     concatenated into a single composite JSON in rest pose so the existing
     simple-cuboid viewer can render them.

Skipped: parts with skin/seasonal/form-variant suffixes (christmas, halloween,
shiny, etc.); those are layered onto the base in-game by the rig system, but
the wiki only needs the base-skin rest pose.

Re-run when the resource pack updates:
    unzip -q -o ~/.minecraft/resourcepacks/devhelditem.zip -d /tmp/devhelditem
    python3 scripts/stage_models_3d.py
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

PACK = Path("/tmp/devhelditem/assets/minecraft")
BETTERMODEL = Path("/tmp/devhelditem/assets/bettermodel")
MODELS_BASE = PACK / "models/pokemon_skins"
TEXTURES_BASE = PACK / "textures"
BM_MODELS = BETTERMODEL / "models/modern_item"
BM_TEXTURES = BETTERMODEL / "textures"
OUT_BASE = Path(__file__).resolve().parent.parent / "static/models-3d"

# Filename-stem → wiki-slug overrides for species the resource pack stores
# without the conventional hyphen / dot. Add as new mismatches surface.
SLUG_OVERRIDES = {
    "mrmime":      "mr-mime",
    "mimejr":      "mime-jr",
    "farfetchd":   "farfetch-d",
    "hooh":        "ho-oh",
    "nidoranf":    "nidoran-f",
    "nidoranm":    "nidoran-m",
    "missingno":   None,
    "missing_no":  None,
}

# BetterModel part-name suffixes that flag a SKIN-variant or form-variant
# version of the part. We only stage the base parts. Any part whose suffix
# (the last underscore-separated token before "_1") matches one of these is
# skipped during composite assembly.
BM_SKIP_PART_TOKENS = {
    "christmas", "halloween", "easter", "summer", "thanksgiving", "valentine",
    "winter", "spring", "spook", "spooky", "patrick", "stpatrick", "stpatricks",
    "starwars", "anniversary", "anni", "shiny", "fool", "fools", "april",
    "april_fools", "cakemon", "cake", "modeler", "monochrome", "meme", "aura",
    "shadow", "marvel", "avengers", "disney", "cosmic", "lunar", "fusemon",
    "sword_and_shield", "swordandshield", "gamer", "mecha", "surfing",
    "alolan", "alola",   # those have their own dedicated folder
    "galarian", "galar",
}


def wiki_slug(model_stem: str) -> str | None:
    """Convert a `<dex>_<species>` filename stem to the wiki's pokedex slug,
    or return None to skip placeholder species."""
    after_dex = re.sub(r"^\d+_", "", model_stem)
    if after_dex in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[after_dex]
    slug = re.sub(r"[^a-z0-9]+", "-", after_dex.lower()).strip("-")
    return slug or None


def species_folder_to_slug(name: str) -> str | None:
    """Same as wiki_slug but for plain species folder names (no dex prefix),
    used by texture-lookup paths."""
    if name in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[name]
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or None


def stage_static_model(model_path: Path, out_dir: Path, slug: str) -> bool:
    """Copy a single static-cuboid JSON model + its texture(s) into out_dir.
    Returns True iff staged."""
    try:
        model = json.loads(model_path.read_text())
    except json.JSONDecodeError:
        return False
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{slug}.json").write_bytes(model_path.read_bytes())

    seen: set[str] = set()
    for tex_ref in (model.get("textures") or {}).values():
        if not tex_ref or tex_ref in seen:
            continue
        seen.add(tex_ref)
        src = TEXTURES_BASE / f"{tex_ref}.png"
        if not src.exists():
            continue
        dst = out_dir / src.name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            shutil.copy2(src, dst)
    return True


# ---------- BetterModel composite assembly ----------

def _bm_part_token(filename_stem: str, species: str) -> str:
    """Return the part-name segment between '<species>_' and '_1', e.g.
    'charizard_left_arm_1' → 'left_arm'."""
    if not filename_stem.startswith(species + "_"):
        return ""
    rest = filename_stem[len(species) + 1:]
    if rest.endswith("_1"):
        rest = rest[:-2]
    return rest


def _bm_part_is_base(part_token: str) -> bool:
    """Reject a part if any of its underscore-separated tokens is a known
    skin/form-variant marker. Special-case `shiny_<form>` etc. by scanning
    every sub-token."""
    if not part_token:
        return False
    for tok in part_token.split("_"):
        if tok.lower() in BM_SKIP_PART_TOKENS:
            return False
    # Reject `_v_` form-variant parts (mega, gmax, etc.): the part token starts
    # with 'v' if the underlying file was named '<species>_v_<...>'.
    if re.match(r"^v(?:_|$)", part_token):
        return False
    # Reject parts named exactly after their species (the canonical "main body"
    # part is duplicated as <species>_<species>_1 in the pack — we already get
    # the body geometry via the dedicated `body` part, and the duplicate uses
    # different element coordinates that conflict).
    return True


def assemble_bettermodel(species_filename: str, out_dir: Path, slug: str) -> bool:
    """Find every base-skin part for `species_filename` (the bettermodel's
    own species key, e.g. 'charizard'), concatenate their `elements` arrays,
    and emit a single composite JSON. Returns True iff anything was staged."""
    if not BM_MODELS.exists():
        return False
    matches = sorted(BM_MODELS.glob(f"{species_filename}_*_1.json"))
    if not matches:
        return False

    composite_elements: list[dict] = []
    composite_textures: dict[str, str] = {}
    for part_path in matches:
        token = _bm_part_token(part_path.stem, species_filename)
        if not _bm_part_is_base(token):
            continue
        try:
            part = json.loads(part_path.read_text())
        except json.JSONDecodeError:
            continue
        composite_elements.extend(part.get("elements") or [])
        # First non-empty texture map wins; later parts use the same keys.
        for k, v in (part.get("textures") or {}).items():
            composite_textures.setdefault(k, v)

    if not composite_elements:
        return False

    # Rewrite texture refs from `bettermodel:item/foo` to `bettermodel/item/foo`
    # so the viewer's last-segment + .png lookup finds the texture file we
    # copy alongside the model.
    for k in list(composite_textures.keys()):
        composite_textures[k] = composite_textures[k].replace("bettermodel:", "bettermodel/")

    out_dir.mkdir(parents=True, exist_ok=True)
    composite = {"textures": composite_textures, "elements": composite_elements}
    (out_dir / f"{slug}.json").write_text(json.dumps(composite))

    # Copy referenced textures.
    seen: set[str] = set()
    for tex_ref in composite_textures.values():
        if tex_ref in seen:
            continue
        seen.add(tex_ref)
        # Resolve `bettermodel/item/foo` → bettermodel/textures/item/foo.png
        rel = tex_ref.split("/", 1)[1] if "/" in tex_ref else tex_ref
        src = BM_TEXTURES / f"{rel}.png"
        if not src.exists():
            continue
        dst = out_dir / src.name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            shutil.copy2(src, dst)
    return True


# ---------- Main ----------

def main() -> int:
    if not MODELS_BASE.exists():
        print(f"Pack not extracted at {MODELS_BASE}", file=sys.stderr)
        print("Run: unzip -q -o ~/.minecraft/resourcepacks/devhelditem.zip -d /tmp/devhelditem",
              file=sys.stderr)
        return 1
    OUT_BASE.mkdir(parents=True, exist_ok=True)

    pokedex_pages = {p.stem for p in (Path(__file__).resolve().parent.parent
                                      / "content/pokedex").glob("*.md")}

    summary = {"regular_static": 0, "regular_composite": 0, "regular_skipped_no_page": 0,
               "alolan": 0, "galarian": 0}
    bm_attempted: list[str] = []
    bm_failed: list[str] = []

    # --- 1. Walk regular/ for static + collect placeholder species names ---
    placeholder_species: list[tuple[Path, str]] = []  # (path, bettermodel-key)
    regular_dir = MODELS_BASE / "regular"
    for model_path in sorted(regular_dir.glob("*.json")):
        slug = wiki_slug(model_path.stem)
        if not slug:
            continue
        if slug not in pokedex_pages:
            summary["regular_skipped_no_page"] += 1
            continue
        if model_path.stat().st_size < 256:
            # Placeholder — try the bettermodel composite path next.
            bm_key = re.sub(r"^\d+_", "", model_path.stem)
            placeholder_species.append((model_path, bm_key, slug))
            continue
        if stage_static_model(model_path, OUT_BASE / "regular" / slug, slug):
            summary["regular_static"] += 1

    # --- 2. Try BetterModel composite for each placeholder ---
    for _, bm_key, slug in placeholder_species:
        bm_attempted.append(slug)
        if assemble_bettermodel(bm_key, OUT_BASE / "regular" / slug, slug):
            summary["regular_composite"] += 1
        else:
            bm_failed.append(slug)

    # --- 3. Walk alolan/ and galarian/ for static models ---
    for variant in ("alolan", "galarian"):
        v_dir = MODELS_BASE / variant
        if not v_dir.exists():
            continue
        for model_path in sorted(v_dir.glob("*.json")):
            if model_path.stat().st_size < 256:
                continue
            slug = wiki_slug(model_path.stem)
            if not slug or slug not in pokedex_pages:
                continue
            if stage_static_model(model_path, OUT_BASE / variant / slug, slug):
                summary[variant] += 1

    print("Staged:")
    print(f"  regular (static cuboid):   {summary['regular_static']}")
    print(f"  regular (bettermodel rig): {summary['regular_composite']}")
    print(f"  alolan forms:              {summary['alolan']}")
    print(f"  galarian forms:            {summary['galarian']}")
    print(f"Skipped: regular without a wiki page: {summary['regular_skipped_no_page']}")
    if bm_failed:
        print(f"BetterModel composite failed for {len(bm_failed)} species "
              f"(likely no parts in the pack): {', '.join(bm_failed[:10])}"
              + ("…" if len(bm_failed) > 10 else ""), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
