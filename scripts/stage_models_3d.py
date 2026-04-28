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

# Cosmetic skins to stage from `pokemon_skins/<skin>/`. Output lands in
# `static/models-3d/<skin>/<slug>/`. Shared with the animated stager and
# the pokedex template — the canonical list lives in
# `data/cosmetic_skins.yaml` and the same keys must appear in each.
COSMETIC_SKINS_YAML = Path(__file__).resolve().parent.parent / "data/cosmetic_skins.yaml"


def load_cosmetic_skins() -> tuple[str, ...]:
    """Parse data/cosmetic_skins.yaml without pyyaml — the file is a flat
    list of `- key: <name>` / `  label: ...` entries, so a tiny line
    walker is enough and we avoid a runtime dependency."""
    keys: list[str] = []
    for line in COSMETIC_SKINS_YAML.read_text().splitlines():
        s = line.strip()
        if s.startswith("- key:"):
            keys.append(s.split(":", 1)[1].strip())
    return tuple(keys)


COSMETIC_SKINS = load_cosmetic_skins()

# Form-variant directories — distinct physical Pokémon (different stats /
# Pokédex entries), routed under their own top-level output dirs by the
# pokedex template. These run alongside the regular skin loop, not as
# cosmetic skin overlays.
FORM_VARIANTS = ("alolan", "galarian")
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
    # Frillish & Jellicent: the wiki page exposes Male and Female form tabs
    # (see content/pokedex/{frillish,jellicent}.md). Male routes to the
    # default `regular/`/`shiny/` slots (idx-0 form tab). Female `_f` files
    # route to `female/` (regular palette) and `female_shiny/` (shiny
    # palette) — the pokedex template (single.html) maps form name →
    # variant directory and picks up the shiny toggle from `female_shiny/`.
    "frillish_m":  "frillish",
    "frillish_f":  ({"regular": "female", "shiny": "female_shiny"}, "frillish"),
    "jellicent_m": "jellicent",
    "jellicent_f": ({"regular": "female", "shiny": "female_shiny"}, "jellicent"),
    # Unfezant ships male and female sprites too; the wiki page doesn't
    # split forms (yet), so keep male as canonical.
    "unfezant_m":  "unfezant",
    "unfezant_f":  None,
    "combee_f":    "combee",   # Combee ships only the female file
    # Sawsbuck and Deerling have four seasonal models; spring is the base form
    # the wiki page presents (other seasons would need their own form tabs).
    "deerling_spring": "deerling",
    "deerling_summer": None,
    "deerling_autumn": None,
    "deerling_winter": None,
    "sawsbuck_spring": "sawsbuck",
    "sawsbuck_summer": None,
    "sawsbuck_autumn": None,
    "sawsbuck_winter": None,
}


def wiki_slug(model_stem: str) -> str | tuple[str, str] | tuple[dict, str] | None:
    """Convert `<dex>_<species>` filename stem to a wiki output target.
    Returns one of:
      * `str` — slug; staged under the source variant (regular/shiny/...)
        as `<variant>/<slug>/<slug>.json` (default behaviour)
      * `(out_variant, slug)` — explicit static routing; Frillish/Jellicent
        female regular → `female/frillish/` (this form fires only on the
        regular source variant)
      * `({source_variant: out_variant, ...}, slug)` — per-source-variant
        routing; the same Female `_f` file goes to `female/` from the
        regular pack dir and to `female_shiny/` from the shiny pack dir
      * `None` — drop this file (placeholder/duplicate)"""
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


def stage_static_model(model_path: Path, out_dir: Path, slug: str,
                       skin_variant: str = "regular") -> bool:
    """Copy a single static-cuboid JSON model + its texture(s) into out_dir.
    Resolves Minecraft-style `parent` inheritance by inlining the parent's
    `elements` (the shiny/aura/... packs use this pattern almost exclusively
    — only `textures` are overridden). Returns True iff a model with
    geometry was staged.

    `skin_variant` is the source variant we're staging from. The function
    also enforces a *visual-difference filter*: when the variant JSON only
    overrides texture keys that no element face actually references (e.g.
    Alakazam's aura sets `"2"` and `"particle"`, but elements use
    `#kadabra` and `#kadabraears`), the merged model renders identically
    to regular and is *not* staged — its chip would otherwise clutter the
    Available Skins selector with no-op options. Self-contained variants
    (own elements, no parent merge) are always staged."""
    # LitePack JSONs are written with a UTF-8 BOM; `utf-8-sig` strips it.
    try:
        model = json.loads(model_path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False

    # Capture the variant JSON's own texture-key overrides (before we
    # merge in the parent's keys) — these are the keys the variant
    # actively re-points to a different atlas. Used below for the
    # visual-difference filter.
    variant_override_keys: set[str] = set()
    if skin_variant != "regular":
        variant_override_keys = set((model.get("textures") or {}).keys())

    parent_ref = model.get("parent")
    if parent_ref and not model.get("elements"):
        # Parent path is relative to assets/minecraft/models/.
        parent_path = MODELS_BASE.parent / f"{parent_ref}.json"
        if not parent_path.exists():
            return False
        try:
            parent = json.loads(parent_path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return False
        merged = dict(parent)
        merged["elements"] = parent.get("elements", [])
        merged_textures = dict(parent.get("textures") or {})
        merged_textures.update(model.get("textures") or {})
        merged["textures"] = merged_textures
        model = merged

    if not model.get("elements"):
        return False

    # Find which texture keys element faces actually use. Drives both the
    # visual-difference filter below and the texture-copy step.
    textures = model.get("textures") or {}
    used_keys: set[str] = set()
    for e in model.get("elements") or []:
        for f in (e.get("faces") or {}).values():
            t = f.get("texture") if isinstance(f, dict) else None
            if isinstance(t, str) and t.startswith("#"):
                used_keys.add(t[1:])

    # Visual-difference filter for cosmetic variants. If the variant's
    # JSON overrode no key that any element face references, the merged
    # model samples exactly the same atlas as regular and would render
    # identically — bail before writing anything so the chip doesn't get
    # surfaced. (Alakazam aura, Weezing aura, Mewtwo aura, etc. are the
    # canonical cases; the in-game aura is a separate particle effect we
    # can't render in a static viewer.)
    if skin_variant != "regular" and not (variant_override_keys & used_keys):
        return False

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{slug}.json").write_text(json.dumps(model))

    # Only copy textures that are actually referenced by an element face's
    # `#key`. Without this filter, the aura PNG (referenced by an unused
    # `"2"` key) would still get copied alongside the regular PNG — and
    # because the viewer derives texture filenames from the ref's last
    # path segment, the variant PNG would collide with the regular body
    # PNG and silently take over.
    refs = sorted({v for k, v in textures.items() if k in used_keys and v})
    for tex_ref in refs:
        src = TEXTURES_BASE / f"{tex_ref}.png"
        if not src.exists():
            continue
        copy_texture(src, out_dir / src.name)
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

    summary: dict[str, int] = {"skipped_placeholder": 0, "skipped_no_page": 0}

    for variant in ("regular",) + COSMETIC_SKINS + FORM_VARIANTS:
        v_dir = MODELS_BASE / variant
        if not v_dir.exists():
            continue
        for model_path in sorted(v_dir.glob("*.json")):
            # The pack ships icon-stub JSONs for animated/rigged species
            # (parent: "pokemon_skin_icons/<variant>/icon") — those have no
            # real geometry and just point at a 16×16 sprite, so skip them.
            # We can't gate on file size: legitimate shiny parent-merge
            # stubs that override only `textures` are sometimes <160 bytes
            # (e.g. 1_bulbasaur.json, 23_ekans.json), and a size cutoff
            # would silently drop them.
            try:
                head = json.loads(model_path.read_text(encoding="utf-8-sig"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                summary["skipped_placeholder"] += 1
                continue
            parent_ref = (head.get("parent") or "").lower()
            if parent_ref.startswith("pokemon_skin_icons/"):
                summary["skipped_placeholder"] += 1
                continue
            override = wiki_slug(model_path.stem)
            if not override:
                continue
            # `wiki_slug` returns one of:
            #   * `slug` (str)              — keep the source variant
            #   * `(out_variant, slug)`     — pin to a single output variant;
            #                                 fires only on the regular source
            #   * `({src→out, ...}, slug)`  — per-source-variant routing
            if isinstance(override, tuple):
                target, slug = override
                if isinstance(target, dict):
                    out_variant = target.get(variant)
                    if out_variant is None:
                        continue
                else:
                    if variant != "regular":
                        continue
                    out_variant = target
            else:
                out_variant, slug = variant, override
            if slug not in pokedex_pages:
                summary["skipped_no_page"] += 1
                continue
            if stage_static_model(model_path, OUT_BASE / out_variant / slug, slug,
                                  skin_variant=variant):
                summary[out_variant] = summary.get(out_variant, 0) + 1

    print("Staged:")
    for variant in sorted(summary):
        if variant.startswith("skipped"):
            continue
        print(f"  {variant}: {summary[variant]}")
    print(f"Skipped: placeholder={summary['skipped_placeholder']} "
          f"no-page={summary['skipped_no_page']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
