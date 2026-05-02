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

# (species, skin) pairs whose model the static stager should refuse to
# emit even if the visual-difference filter would accept it. Used for cases
# where the pack-derived model wouldn't be a meaningful chip on the wiki:
#  * Aura — in-game effect is a particle system, not a body recolor; the
#    pack's `aura/<dex>_<species>.json` overrides texture keys that *do*
#    render but produce a near-no-op variant for the static viewer.
#  * Texture-only orphans — pack ships only a textures/<skin>/<slug>/ dir
#    with no model JSON, so nothing would stage anyway; adding the pair
#    here keeps `ingest_pokedex.py`'s NO_VISIBLE_MODEL_COSMETICS in 1:1
#    correspondence.
# Keep this set in sync with `NO_VISIBLE_MODEL_COSMETICS` in
# `scripts/ingest_pokedex.py` — they're the canonical join key for skin
# chips that should not surface anywhere on the wiki. Species name uses
# the wiki content slug (lowercase, hyphenated), since the static stager
# operates on slugs not display names.
SUPPRESSED_COSMETICS = {
    ("weezing",   "aura"),
    ("mudkip",    "aura"),
    ("klink",     "aura"),
    ("klang",     "aura"),
    ("klinklang", "aura"),
    ("krookodile", "valentine"),
    ("trubbish",   "halloween"),
    ("litwick",    "christmas"),
}

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
    # Giratina ships its two formes as separate model files. Standard tab
    # uses the Altered Forme; Origin Forme gets a dedicated form tab routed
    # to its own output directory (single.html maps `Origin` → variant
    # "origin").
    "giratina_altered": "giratina",
    # Origin Forme: regular and shiny route to `origin/`/`origin_shiny/`;
    # cosmetic skins (Summer so far) get their own `origin_<skin>/` slot
    # so the Origin form tab can surface chips independent of the Altered
    # tab. Layout in pokedex/single.html maps Origin form → variant
    # `origin` and resolves chip dirs as `origin_<skin>/<slug>/`.
    "giratina_origin":  ({"regular": "origin",
                          "shiny":   "origin_shiny",
                          "summer":  "origin_summer"}, "giratina"),
    # Shellos ships separate east/west static-cuboid models. The wiki page
    # exposes "West Sea" (default tab) and "East Sea" form tabs. West routes
    # to the canonical `regular/`/`shiny/` slots; East gets its own
    # `east/`/`east_shiny/` output dirs (single.html maps form name "East
    # Sea" → variant "east"; the shiny toggle picks up `east_shiny/`).
    "shellos_west": "shellos",
    "shellos_east": ({"regular": "east", "shiny": "east_shiny"}, "shellos"),
    # Burmy / Wormadam ship three cloak models (Plant, Sandy, Trash). Plant
    # is the canonical Standard form on the wiki page. Sandy and Trash get
    # dedicated output variants (sandy/ + sandy_shiny/, trash/ + trash_shiny/);
    # single.html maps form name "Sandy"/"Trash" → variant key. Christmas
    # ships only the Plant cloak, so christmas burmy_sandy/burmy_trash and
    # the wormadam equivalents are absent from the pack and don't stage.
    "burmy_plant":     "burmy",
    "burmy_sandy":     ({"regular": "sandy", "shiny": "sandy_shiny"}, "burmy"),
    "burmy_trash":     ({"regular": "trash", "shiny": "trash_shiny"}, "burmy"),
    "wormadam_plant":  "wormadam",
    "wormadam_sandy":  ({"regular": "sandy", "shiny": "sandy_shiny"}, "wormadam"),
    "wormadam_trash":  ({"regular": "trash", "shiny": "trash_shiny"}, "wormadam"),
    # Cosmetic-skin reskins of regional bodies (Alolan / Galarian). The pack
    # ships these as `<skin>/<dex>_<species>_<region>.json` — the regional
    # body, not the standard one, is the canvas the cosmetic overlay was
    # authored against. Route them to dedicated `<region>_<skin>/` output
    # dirs so the regional form tab exposes the chip without colliding with
    # the standard form's `<skin>/` slot. The pack uses both `_alola` and
    # `_alolan` suffixes inconsistently across files; both forms appear
    # here keyed by their actual filename stem.
    # Pichu surfing variants: pack ships five distinct surfing-themed
    # models under `pokemon_skins/surfing/172_pichu_<variant>.json` (the
    # Summer event in-game presents them as five "Surfing Pichu" outfits:
    # Ash Hat, Azumarill, Green, Pink, Pokeball). The wiki page exposes
    # them as five form tabs ("Surfing 1" .. "Surfing 5") routed to their
    # own `surfing_1`..`surfing_5` output dirs. Layout in
    # pokedex/single.html maps form name → variant via prefix replace.
    "pichu_ash_hat":   ({"surfing": "surfing_1"}, "pichu"),
    "pichu_azumarill": ({"surfing": "surfing_2"}, "pichu"),
    "pichu_green":     ({"surfing": "surfing_3"}, "pichu"),
    "pichu_pink":      ({"surfing": "surfing_4"}, "pichu"),
    "pichu_pokeball":  ({"surfing": "surfing_5"}, "pichu"),
    "pikachu_ash_hat":   ({"surfing": "surfing_1"}, "pikachu"),
    "pikachu_azumarill": ({"surfing": "surfing_2"}, "pikachu"),
    "pikachu_green":     ({"surfing": "surfing_3"}, "pikachu"),
    "pikachu_pink":      ({"surfing": "surfing_4"}, "pikachu"),
    "pikachu_pokeball":  ({"surfing": "surfing_5"}, "pikachu"),
    "raichu_ash_hat":   ({"surfing": "surfing_1"}, "raichu"),
    "raichu_azumarill": ({"surfing": "surfing_2"}, "raichu"),
    "raichu_green":     ({"surfing": "surfing_3"}, "raichu"),
    "raichu_pink":      ({"surfing": "surfing_4"}, "raichu"),
    "raichu_pokeball":  ({"surfing": "surfing_5"}, "raichu"),
    "sandslash_alola":   ({"christmas":     "alolan_christmas"},     "sandslash"),
    "marowak_alola":     ({"christmas":     "alolan_christmas"},     "marowak"),
    "marowak_alolan":    ({"summer":        "alolan_summer"},        "marowak"),
    "vulpix_alola":      ({"christmas":     "alolan_christmas"},     "vulpix"),
    "ninetales_alola":   ({"christmas":     "alolan_christmas"},     "ninetales"),
    "ninetales_alolan":  ({"valentine":     "alolan_valentine"},     "ninetales"),
    "golem_alola":       ({"christmas":     "alolan_christmas"},     "golem"),
    "muk_alola":         ({"christmas":     "alolan_christmas"},     "muk"),
    # Exeggutor's `thanksgiving/10035_exeggutor_alolan.json` is a flat-icon
    # placeholder (parent: pokemon_skin_icons/regular/icon), not a real 3D
    # model — the placeholder check upstream skips it, so no thanksgiving
    # output is produced here.
    "exeggutor_alolan":  ({"easter":        "alolan_easter",
                           "summer":        "alolan_summer"},        "exeggutor"),
    "weezing_galarian":  ({"christmas":     "galarian_christmas"},   "weezing"),
    "rapidash_galarian": ({"valentine":     "galarian_valentine"},   "rapidash"),
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


# ---------------------------------------------------------------------------
# Per-(slug, skin_variant) fix-ups
#
# A few species in the resource pack ship JSON models whose face UVs don't
# line up with the texture atlases they reference — usually because the
# model author hand-tweaked one variant against an unshipped atlas, or the
# variant override accidentally collapsed a "body + eye outline" two-atlas
# scheme down to a single atlas. Three.js renders honestly: faces sampling
# transparent pixels disappear, faces sampling the wrong atlas show
# garbage colors. The in-game pack happens to mask these via tinting,
# index-palette quirks, or fallback paths that aren't trivially
# reproducible from the static cuboid JSON alone.
#
# Each fix-up here is a tiny, scoped patch applied AFTER parent merge +
# path rewrite + visual-difference filter, but BEFORE we serialise the
# JSON and copy textures. Fix-ups can mutate `model` in place (and/or
# return a replacement dict), and may write auxiliary PNGs into
# `out_dir`. Add new entries sparingly, with the in-pack diagnosis above
# the fix-up function so the next reader can verify the heuristic still
# applies after a pack update.
# ---------------------------------------------------------------------------

def _restore_shiny_eye_atlas(slug: str):
    """Build a fix-up that restores the regular-form eye atlas reference
    on a species's shiny variant when the pack's shiny model collapses
    `particle` onto the body atlas. The pattern: regular has a separate
    `regular/<slug>/eye.png` referenced by `particle` and consumed by
    eye-element faces; the shiny variant overrides `particle` to
    `shiny/<slug>/<slug>` (same as `texture`), which makes those eye-UV
    faces sample the shiny body atlas at half resolution and render
    body-color blocks where the eye outlines should be. Restoring the
    regular eye atlas keeps the eye outlines black and the body shiny.

    Canonical cases: Gurdurr, Scraggy. Add new species with the same
    pattern by registering ("<slug>", "shiny") → _restore_shiny_eye_atlas("<slug>")
    in SPECIES_FIXUPS."""
    body_ref = f"pokemon_skins/shiny/{slug}/{slug}"
    eye_ref  = f"pokemon_skins/regular/{slug}/eye"
    def _fix(model: dict, textures: dict, used_keys: set[str],
             out_dir: Path) -> dict:
        tex = dict(model.get("textures") or {})
        if tex.get("particle") == body_ref:
            tex["particle"] = eye_ref
        model = dict(model)
        model["textures"] = tex
        return model
    return _fix


def _fix_gurdurr_christmas(model: dict, textures: dict, used_keys: set[str],
                           out_dir: Path) -> dict:
    """Christmas pack model has 502 body faces (`#2`) whose UVs all sit in
    the bottom-edge band of the body atlas — UV (0/0.5/0.75/1.1, 15.9) on
    a 32×32 atlas → pixels (0–2, 31). The shipped regular body atlas is
    transparent in that row, so 80 % of the model renders invisible and
    only the Santa hat / cane (`#1`) shows up — what the user sees as
    "missing actual pokemon model". The model file references
    `pokemon_skins/regular/gurdurr/gurdurr`, so we can't fix this just
    by swapping atlases; we synthesise a Christmas-only body atlas with
    those bottom-row pixels filled in with Gurdurr's actual palette
    sampled from the regular atlas's colored 24×24 quadrant.
    Subsequent staging runs regenerate the synthesised file from
    scratch.

    The regular atlas's colored region is a 4-color palette (beige body
    skin, dark-red muscle, pink pads, bright-red accent), each as a
    144-pixel block. The Christmas model's `#2` UVs target three
    distinct columns at row 31 (NearestFilter rounding):

      pixel (0, 31) — 286 faces — main body silhouette
      pixel (1, 31) — 173 faces — secondary accent
      pixel (2, 31) — 38 faces  — tertiary accent
      pixel (3, 31) — pad slot (not currently sampled, but kept filled
                                 to absorb edge-rounding artefacts)

    We assign palette colours to those positions in face-count order so
    the most common chip lands the body's main beige, and the smaller
    chips pick up the accent colours.
    """
    if not HAS_PIL:
        return model
    src = TEXTURES_BASE / "pokemon_skins/regular/gurdurr/gurdurr.png"
    if not src.exists():
        return model
    img = Image.open(src).convert("RGBA")
    # Sample the four palette colours from corners of the 24×24 colored
    # quadrant. The regular atlas is laid out as 12×12 tiles; one
    # representative pixel from each quadrant gives us the four base
    # colours without needing to know the exact tile boundaries.
    body_main   = img.getpixel((0, 0))     # beige skin
    accent_a    = img.getpixel((12, 0))    # dark red
    accent_b    = img.getpixel((12, 12))   # pink pads
    accent_c    = img.getpixel((0, 12))    # bright red
    # Sanity: bail if the regular atlas changed shape and we'd be
    # filling with transparent / wrong-bucket colours.
    if any(c[3] == 0 for c in (body_main, accent_a, accent_b, accent_c)):
        return model
    # Map bottom-row pixels by face-count rank. Indexes match the UV
    # buckets enumerated in the docstring.
    img.putpixel((0, 31), body_main)
    img.putpixel((1, 31), accent_a)
    img.putpixel((2, 31), accent_b)
    img.putpixel((3, 31), accent_c)
    out_dir.mkdir(parents=True, exist_ok=True)
    img.save(out_dir / "gurdurr.png")

    # Re-target the body ref to a virtual path so the texture-copy step
    # below doesn't overwrite our synthesised body atlas. The viewer's
    # filename-from-basename rule still resolves it to `gurdurr.png` in
    # the staged dir regardless of the ref's path component.
    tex = dict(model.get("textures") or {})
    if tex.get("2") == "pokemon_skins/regular/gurdurr/gurdurr":
        tex["2"] = "pokemon_skins/christmas/gurdurr/gurdurr"

    # Restore the regular Gurdurr's eye-feature face refs onto the
    # Christmas model. The Christmas pack model keeps the eye-element
    # geometry — same `from`/`to` cuboids that exist on the regular
    # form — but rewires every face to `#2` (the body atlas), so they
    # sample the bottom-edge palette pixel and render as a solid skin
    # color instead of the black-outline eye detail the regular has.
    # That's the "face a little off" the user reported.
    #
    # We match Christmas elements to regular eye elements by their
    # `from`/`to` corners and overwrite the matching Christmas cube's
    # `faces` map with the regular cube's faces (which reference
    # `#particle`, the regular eye atlas). `#particle` is rewritten to
    # `#eye` and the eye atlas is registered under a fresh `eye`
    # texture key — the Christmas `particle` key is left alone since
    # it's still used by the hat atlas. Appending instead of replacing
    # would land the eye cubes coincident with the Christmas body
    # cubes and Z-fight (which is exactly what the user observed).
    eye_atlas_ref = "pokemon_skins/regular/gurdurr/eye"
    if (TEXTURES_BASE / f"{eye_atlas_ref}.png").exists():
        regular_path = MODELS_BASE / "regular/533_gurdurr.json"
        try:
            regular = json.loads(regular_path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
            regular = None
        if regular is not None:
            tex["eye"] = eye_atlas_ref
            # Build a lookup of regular eye elements keyed by their
            # cube coordinates (rounded to 4 decimals to absorb float
            # repr noise across pack-edit roundtrips).
            def _key(fr, to):
                return tuple(round(c, 4) for c in (fr + to))
            eye_by_key = {}
            for src_el in regular.get("elements") or []:
                faces = src_el.get("faces") or {}
                if not any(isinstance(fv, dict) and fv.get("texture") == "#particle"
                           for fv in faces.values()):
                    continue
                fr, to = src_el.get("from"), src_el.get("to")
                if fr and to:
                    eye_by_key[_key(fr, to)] = src_el
            new_elements = []
            matched_keys: set[tuple] = set()
            replaced = 0
            for el in model.get("elements") or []:
                fr, to = el.get("from"), el.get("to")
                k = _key(fr, to) if (fr and to) else None
                src = eye_by_key.get(k) if k is not None else None
                if src is not None:
                    # Take the regular eye element's faces verbatim and
                    # rename #particle → #eye.
                    src_faces = json.loads(json.dumps(src.get("faces") or {}))
                    for fv in src_faces.values():
                        if isinstance(fv, dict) and fv.get("texture") == "#particle":
                            fv["texture"] = "#eye"
                    el = dict(el)
                    el["faces"] = src_faces
                    replaced += 1
                    matched_keys.add(k)
                new_elements.append(el)
            # Append any regular eye cubes the Christmas model doesn't
            # have a position-matching counterpart for (the pack
            # dropped a few during the Christmas-skin authoring pass).
            for k, src_el in eye_by_key.items():
                if k in matched_keys:
                    continue
                el = json.loads(json.dumps(src_el))
                for fv in (el.get("faces") or {}).values():
                    if isinstance(fv, dict) and fv.get("texture") == "#particle":
                        fv["texture"] = "#eye"
                new_elements.append(el)
            if replaced or len(new_elements) != len(model.get("elements") or []):
                model = dict(model)
                model["elements"] = new_elements

    model["textures"] = tex
    return model


SPECIES_FIXUPS = {
    ("gurdurr", "shiny"):     _restore_shiny_eye_atlas("gurdurr"),
    ("scraggy", "shiny"):     _restore_shiny_eye_atlas("scraggy"),
    ("gurdurr", "christmas"): _fix_gurdurr_christmas,
}


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
    # Hard-suppression check: editorial decisions to keep certain
    # (species, skin) chips off the wiki even when the pack ships geometry
    # for them (see SUPPRESSED_COSMETICS for rationale).
    if (slug, skin_variant) in SUPPRESSED_COSMETICS:
        return False
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

    # Find which texture keys element faces actually use. Drives the
    # visual-difference filter below, the path-rewrite for non-regular
    # variants, and the texture-copy step.
    textures = model.get("textures") or {}
    used_keys: set[str] = set()
    for e in model.get("elements") or []:
        for f in (e.get("faces") or {}).values():
            t = f.get("texture") if isinstance(f, dict) else None
            if isinstance(t, str) and t.startswith("#"):
                used_keys.add(t[1:])

    # Path-rewrite pass for non-regular variants. Many shiny / cosmetic
    # variant JSONs in the pack only declare `particle`/`2`/`5` overrides
    # that no element face references — the in-game runtime achieves the
    # actual visual swap by treating the entire texture base path as
    # variant-scoped (`pokemon_skins/regular/...` → `pokemon_skins/shiny/...`)
    # and then rendering the parent's geometry against the swapped atlas.
    # A static parent-merge alone leaves all element-referenced texture
    # entries pointing back at `regular/<slug>/...`, so the staged shiny
    # ends up byte-identical to regular (canonical examples: Paras shiny,
    # Swadloon shiny). For each merged texture key that points at a
    # `pokemon_skins/regular/<slug>/<file>` path, swap to the
    # `pokemon_skins/<skin>/<slug>/<file>` path when that PNG exists in
    # the pack. `path_rewrites_used` tracks whether any
    # *element-face-referenced* key got swapped, which is what the
    # visual-difference filter consults below.
    path_rewrites_used = False
    if skin_variant != "regular":
        regular_prefix = "pokemon_skins/regular/"
        for k, v in list(textures.items()):
            if not isinstance(v, str) or not v.startswith(regular_prefix):
                continue
            candidate = f"pokemon_skins/{skin_variant}/" + v[len(regular_prefix):]
            if (TEXTURES_BASE / f"{candidate}.png").exists():
                textures[k] = candidate
                if k in used_keys:
                    path_rewrites_used = True

    # Visual-difference filter for cosmetic variants. If the variant's
    # JSON overrode no key that any element face references AND no
    # element-key's texture path got rewritten to the variant directory,
    # the merged model samples exactly the same atlas as regular and would
    # render identically — bail before writing anything so the chip doesn't
    # get surfaced. (Alakazam aura, Weezing aura, Mewtwo aura, etc. are the
    # canonical "no real reskin" cases; the in-game aura is a separate
    # particle effect we can't render in a static viewer.)
    if skin_variant != "regular" and not (variant_override_keys & used_keys) and not path_rewrites_used:
        return False

    # Per-(slug, skin_variant) fix-ups for known data quirks where the
    # pack's model JSON references atlases the model's UVs don't actually
    # align with. Each fix-up returns the (possibly mutated) `model` dict
    # and may copy/synthesise auxiliary PNGs into `out_dir`. See
    # SPECIES_FIXUPS below for the canonical list and per-case rationale.
    # Fix-ups can add new elements (with new texture-key refs); we
    # recompute `used_keys` post-fixup so the texture-copy pass below
    # picks up any new keys those new elements pull in.
    fixup = SPECIES_FIXUPS.get((slug, skin_variant))
    if fixup is not None:
        model = fixup(model, textures, used_keys, out_dir)
        used_keys = set()
        for e in model.get("elements") or []:
            for f in (e.get("faces") or {}).values():
                t = f.get("texture") if isinstance(f, dict) else None
                if isinstance(t, str) and t.startswith("#"):
                    used_keys.add(t[1:])

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{slug}.json").write_text(json.dumps(model))

    # Only copy textures that are actually referenced by an element face's
    # `#key`. Without this filter, the aura PNG (referenced by an unused
    # `"2"` key) would still get copied alongside the regular PNG — and
    # because the viewer derives texture filenames from the ref's last
    # path segment, the variant PNG would collide with the regular body
    # PNG and silently take over.
    refs = sorted({v for k, v in (model.get("textures") or {}).items() if k in used_keys and v})
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

    # Each entry pairs the canonical *output-variant* name (used for
    # routing, fixup logic, and `skin_variant=` arg into stage_static_model)
    # with the *source path* under MODELS_BASE. They're usually equal, but
    # `anniversary_shiny` lives nested at `anniversary/shiny/` in the pack
    # while needing its own top-level output dir.
    sources: list[tuple[str, str]] = (
        [(v, v) for v in (("regular",) + COSMETIC_SKINS + FORM_VARIANTS)]
        + [("anniversary_shiny", "anniversary/shiny"),
           ("alolan_shiny",      "alolan/shiny"),
           ("galarian_shiny",    "galarian/shiny"),
           # `surfing/` ships its own per-species models (currently Pichu's
           # five "Surfing Pichu" outfits, plus Pikachu/Raichu equivalents
           # which the wiki doesn't yet route). SLUG_OVERRIDES funnels the
           # individual files into per-variant output dirs.
           ("surfing",           "surfing")]
    )
    for variant, source_path in sources:
        v_dir = MODELS_BASE / source_path
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
