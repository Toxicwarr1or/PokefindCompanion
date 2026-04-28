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

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

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


def copy_texture(src: Path, dst: Path) -> None:
    """Copy a PNG. When the source has a sibling `<name>.png.mcmeta` describing
    an animation (vertical sprite-sheet), extract just the FIRST frame so the
    static viewer doesn't show every frame of a wing-flap stacked on the
    geometry. Falls back to a plain copy if PIL isn't available or the file
    has no animation metadata."""
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
                        # Vertical sprite-sheet: top-most square is frame 0.
                        frame = img.crop((0, 0, w, w))
                        frame.save(dst)
                        return
            except Exception:
                pass
    shutil.copy2(src, dst)


def stage_static_model(model_path: Path, out_dir: Path, slug: str) -> bool:
    """Copy a single static-cuboid JSON model + its texture(s) into out_dir.
    Returns True iff staged. Resolves Minecraft-style `parent` inheritance
    by inlining the parent model's `elements` array — the shiny pack uses
    this pattern almost exclusively (parent="pokemon_skins/regular/<id>_<sp>",
    only `textures` overridden)."""
    try:
        model = json.loads(model_path.read_text())
    except json.JSONDecodeError:
        return False

    # If the model is just a texture-override of a parent, merge the parent's
    # elements + display under our textures so the file becomes self-contained.
    parent_ref = model.get("parent")
    if parent_ref and not model.get("elements"):
        # parent ref is relative to assets/minecraft/models/, e.g.
        # "pokemon_skins/regular/20_raticate". MODELS_BASE.parent points at
        # …/models, so direct concatenation resolves the file.
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

    # When the model is a parent-merge, the parent's texture entries can
    # carry over a regular-pack path (e.g. parent's "texture" key →
    # pokemon_skins/regular/...) whose basename collides with the child's
    # shiny override. Sort so any path mentioning the parent variant is
    # copied FIRST, then variant-specific overrides win the basename slot.
    refs = list({v for v in (model.get("textures") or {}).values() if v})
    refs.sort(key=lambda r: (0 if "/regular/" in r else 1, r))
    for tex_ref in refs:
        src = TEXTURES_BASE / f"{tex_ref}.png"
        if not src.exists():
            continue
        dst = out_dir / src.name
        copy_texture(src, dst)
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


def assemble_bettermodel(species_filename: str, out_dir: Path, slug: str,
                         variant: str = "regular") -> bool:
    """Find every part for `species_filename` matching the requested skin
    variant ("regular" → bare-token base parts, "shiny" → v_shiny_-prefixed
    parts), concatenate their `elements` arrays, and emit a single composite
    JSON. Returns True iff anything was staged."""
    if not BM_MODELS.exists():
        return False
    matches = sorted(BM_MODELS.glob(f"{species_filename}_*_1.json"))
    if not matches:
        return False

    composite_elements: list[dict] = []
    composite_textures: dict[str, str] = {}
    for part_path in matches:
        token = _bm_part_token(part_path.stem, species_filename)
        if variant == "regular":
            if not _bm_part_is_base(token):
                continue
        elif variant == "shiny":
            # Want v_shiny_<part> with no further variant markers in <part>.
            if not token.startswith("v_shiny_"):
                continue
            inner = token[len("v_shiny_"):]
            # Reject overlays (christmas, halloween, etc.) layered on shiny.
            if any(t in BM_SKIP_PART_TOKENS for t in inner.split("_")):
                continue
        else:
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
            copy_texture(src, dst)
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
               "alolan": 0, "galarian": 0,
               "shiny_static": 0, "shiny_composite": 0}

    # --- 1. Walk regular/ for static + collect placeholder species names ---
    regular_placeholders: list[tuple[Path, str, str]] = []
    regular_dir = MODELS_BASE / "regular"
    for model_path in sorted(regular_dir.glob("*.json")):
        slug = wiki_slug(model_path.stem)
        if not slug:
            continue
        if slug not in pokedex_pages:
            summary["regular_skipped_no_page"] += 1
            continue
        if model_path.stat().st_size < 256:
            bm_key = re.sub(r"^\d+_", "", model_path.stem)
            regular_placeholders.append((model_path, bm_key, slug))
            continue
        if stage_static_model(model_path, OUT_BASE / "regular" / slug, slug):
            summary["regular_static"] += 1

    # --- 2. BetterModel composite for each regular placeholder ---
    for _, bm_key, slug in regular_placeholders:
        if assemble_bettermodel(bm_key, OUT_BASE / "regular" / slug, slug, variant="regular"):
            summary["regular_composite"] += 1

    # --- 3. Walk shiny/ for static + composite for placeholders ---
    shiny_dir = MODELS_BASE / "shiny"
    if shiny_dir.exists():
        shiny_placeholders: list[tuple[str, str]] = []
        for model_path in sorted(shiny_dir.glob("*.json")):
            slug = wiki_slug(model_path.stem)
            if not slug or slug not in pokedex_pages:
                continue
            if model_path.stat().st_size < 256:
                bm_key = re.sub(r"^\d+_", "", model_path.stem)
                shiny_placeholders.append((bm_key, slug))
                continue
            if stage_static_model(model_path, OUT_BASE / "shiny" / slug, slug):
                summary["shiny_static"] += 1
        for bm_key, slug in shiny_placeholders:
            if assemble_bettermodel(bm_key, OUT_BASE / "shiny" / slug, slug, variant="shiny"):
                summary["shiny_composite"] += 1
                continue
            # Final fallback: simple-cuboid species (Bulbasaur, Charmander, …)
            # have no bettermodel parts, but their shiny is just a recoloured
            # texture over the same regular geometry. Re-emit the regular
            # model JSON with texture refs swapped to the shiny path.
            reg_model = OUT_BASE / "regular" / slug / f"{slug}.json"
            if not reg_model.exists():
                continue
            try:
                model = json.loads(reg_model.read_text())
            except json.JSONDecodeError:
                continue
            new_textures = {}
            shiny_textures_copied = 0
            for k, ref in (model.get("textures") or {}).items():
                shiny_ref = ref.replace("regular/", "shiny/", 1) if "regular/" in ref else ref
                src = TEXTURES_BASE / f"{shiny_ref}.png"
                if src.exists():
                    new_textures[k] = shiny_ref
                    shiny_textures_copied += 1
                else:
                    new_textures[k] = ref   # keep original if no shiny exists
            if shiny_textures_copied == 0:
                continue
            out_dir = OUT_BASE / "shiny" / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            model["textures"] = new_textures
            (out_dir / f"{slug}.json").write_text(json.dumps(model))
            for ref in set(new_textures.values()):
                src = TEXTURES_BASE / f"{ref}.png"
                if not src.exists():
                    continue
                dst = out_dir / src.name
                if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
                    copy_texture(src, dst)
            summary["shiny_static"] += 1

    # --- 4. Walk alolan/ and galarian/ for static models ---
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
    print(f"  shiny  (static cuboid):    {summary['shiny_static']}")
    print(f"  shiny  (bettermodel rig):  {summary['shiny_composite']}")
    print(f"  alolan forms:              {summary['alolan']}")
    print(f"  galarian forms:            {summary['galarian']}")
    print(f"Skipped: regular without a wiki page: {summary['regular_skipped_no_page']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
