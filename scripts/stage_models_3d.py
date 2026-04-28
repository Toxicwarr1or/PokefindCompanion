#!/usr/bin/env python3
"""
Stage 3D-viewer assets for the Pokefind wiki.

Scope (deliberately narrow): only the simple static-cuboid Pokemon models
from the resource pack's `pokemon_skins/{regular,shiny,alolan,galarian}/`
directories. Each `<dex>_<species>.json` is copied to
static/models-3d/<variant>/<wiki-slug>/<wiki-slug>.json with its texture(s)
alongside, and animated wing textures are isolated to a single frame.

Shiny models in the pack mostly use Java's `parent` inheritance pattern —
they inherit elements from the regular model and only override textures.
We resolve `parent` at staging time so the staged JSON is self-contained.

Animated/articulated species (Charizard, Blastoise, Gengar, etc.) use the
BetterModel rig system. Without the server-side rig animation data, those
can't be assembled into a faithful static composite — those species just
fall back to the 2D sprite on the wiki and don't get a 3D viewer.

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

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

PACK = Path("/tmp/devhelditem/assets/minecraft")
MODELS_BASE = PACK / "models/pokemon_skins"
TEXTURES_BASE = PACK / "textures"
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


def wiki_slug(model_stem: str) -> str | None:
    """Convert `<dex>_<species>` filename stem to the wiki's pokedex slug."""
    after_dex = re.sub(r"^\d+_", "", model_stem)
    if after_dex in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[after_dex]
    slug = re.sub(r"[^a-z0-9]+", "-", after_dex.lower()).strip("-")
    return slug or None


def copy_texture(src: Path, dst: Path) -> None:
    """Copy a PNG. When the source has a sibling `<name>.png.mcmeta` describing
    a frame animation (vertical sprite-sheet), extract just the FIRST frame so
    the static viewer doesn't show every wing-flap stage stacked at once."""
    mcmeta = src.with_suffix(src.suffix + ".mcmeta")
    if mcmeta.exists() and HAS_PIL:
        try:
            meta = json.loads(mcmeta.read_text())
        except json.JSONDecodeError:
            meta = {}
        if "animation" in meta:
            try:
                with Image.open(src) as img:
                    w, h = img.size
                    if h > w:
                        frame = img.crop((0, 0, w, w))
                        frame.save(dst)
                        return
            except Exception:
                pass
    shutil.copy2(src, dst)


def stage_static_model(model_path: Path, out_dir: Path, slug: str) -> bool:
    """Copy a single static-cuboid JSON model + its texture(s) into out_dir.
    Resolves Minecraft-style `parent` inheritance by inlining the parent's
    `elements` (the shiny pack uses this pattern almost exclusively — only
    `textures` are overridden). Returns True iff a model with geometry was
    staged."""
    try:
        model = json.loads(model_path.read_text())
    except json.JSONDecodeError:
        return False

    parent_ref = model.get("parent")
    if parent_ref and not model.get("elements"):
        # Parent path is relative to assets/minecraft/models/.
        parent_path = MODELS_BASE.parent / f"{parent_ref}.json"
        if not parent_path.exists():
            return False
        try:
            parent = json.loads(parent_path.read_text())
        except json.JSONDecodeError:
            return False
        merged = dict(parent)
        merged["elements"] = parent.get("elements", [])
        merged_textures = dict(parent.get("textures") or {})
        merged_textures.update(model.get("textures") or {})
        merged["textures"] = merged_textures
        model = merged

    if not model.get("elements"):
        return False

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{slug}.json").write_text(json.dumps(model))

    # Variant-specific texture refs win the basename slot — sort regular paths
    # first so any later variant override copies last.
    refs = list({v for v in (model.get("textures") or {}).values() if v})
    refs.sort(key=lambda r: (0 if "/regular/" in r else 1, r))
    for tex_ref in refs:
        src = TEXTURES_BASE / f"{tex_ref}.png"
        if not src.exists():
            continue
        dst = out_dir / src.name
        copy_texture(src, dst)
    return True


def main() -> int:
    if not MODELS_BASE.exists():
        print(f"Pack not extracted at {MODELS_BASE}", file=sys.stderr)
        print("Run: unzip -q -o ~/.minecraft/resourcepacks/devhelditem.zip -d /tmp/devhelditem",
              file=sys.stderr)
        return 1
    OUT_BASE.mkdir(parents=True, exist_ok=True)

    pokedex_pages = {p.stem for p in (Path(__file__).resolve().parent.parent
                                      / "content/pokedex").glob("*.md")}

    summary = {"regular": 0, "shiny": 0, "alolan": 0, "galarian": 0,
               "skipped_placeholder": 0, "skipped_no_page": 0}

    for variant in ("regular", "shiny", "alolan", "galarian"):
        v_dir = MODELS_BASE / variant
        if not v_dir.exists():
            continue
        for model_path in sorted(v_dir.glob("*.json")):
            # The pack ships ~140-byte icon-stub JSONs for animated/rigged
            # species (parent: "pokemon_skin_icons/...") — skip those.
            # 200-byte cutoff keeps the genuine parent-merge shinies
            # (parent: "pokemon_skins/regular/<id>_<sp>", which start ~250
            # bytes and produce full geometry after the merge).
            if model_path.stat().st_size < 200:
                summary["skipped_placeholder"] += 1
                continue
            slug = wiki_slug(model_path.stem)
            if not slug:
                continue
            if slug not in pokedex_pages:
                summary["skipped_no_page"] += 1
                continue
            if stage_static_model(model_path, OUT_BASE / variant / slug, slug):
                summary[variant] += 1

    print("Staged:")
    print(f"  regular:  {summary['regular']}")
    print(f"  shiny:    {summary['shiny']}")
    print(f"  alolan:   {summary['alolan']}")
    print(f"  galarian: {summary['galarian']}")
    print(f"Skipped: placeholder={summary['skipped_placeholder']} "
          f"no-page={summary['skipped_no_page']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
