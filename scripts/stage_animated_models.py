#!/usr/bin/env python3
"""
Stage animated/rigged Pokemon models for the wiki 3D viewer.

Walks every `.bbmodel` under MODELS_DIR and emits a bone-hierarchy JSON per
species — nested groups whose origins/rotations match the Blockbench rig —
plus the body (and optional flame) atlas PNGs from the resource pack. The
viewer (`static/js/mc-model-viewer.js`) reads the `bones` field as nested
THREE.Groups; the prior flat `elements` shape stays supported for the simple
cuboid pokedex models that don't have a rig.

Why we don't use the BetterModel-exported part files: that exporter shrinks
each bone to fit the 16-unit item-display box, losing both absolute scale
(wings end up half-size) and the multi-axis bone rotations needed at rest
(arms and wings come out flat). Walking the bbmodel directly preserves both.

Re-run when the resource pack updates:
    unzip -q -o ~/.minecraft/resourcepacks/devhelditem.zip -d /tmp/devhelditem
    python3 scripts/stage_animated_models.py
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

MODELS_DIR = Path("/home/jack/Downloads/models")
PACK_BM_TEXTURES = Path("/tmp/devhelditem/assets/bettermodel/textures")
WIKI_ROOT = Path(__file__).resolve().parent.parent
POKEDEX_DIR = WIKI_ROOT / "content/pokedex"
OUT_BASE = WIKI_ROOT / "static/models-3d"

# The first top-level outliner group in every bbmodel we ship is the base
# skin; alternate-skin top-level groups (halloween, easter, …) sit beside it.
ROOT_BONE_DEFAULT = "body"

# Bones to drop from the static viewer — animated VFX (mouth flame is the
# canonical case) we don't want frozen mid-flicker on the wiki render.
SKIP_BONES: set[str] = {"flame"}

# Bbmodel filenames are kebab-converted directly to wiki slugs. Filenames
# starting with one of these prefixes route into a variant directory rather
# than `regular/`, matching how stage_models_3d.py partitions form variants.
VARIANT_PREFIXES = ("alolan", "galarian", "hisuian")

# Event/cosmetic skin tokens to filter from texture selection. Note that
# "shiny" is intentionally NOT here — shiny is a first-class skin we ship
# alongside regular and route through a separate output directory.
EVENT_TOKENS: set[str] = {
    "halloween", "easter", "christmas", "xmas", "thanksgiving", "summer",
    "valentine", "shadow", "aura", "anniversary", "anni",
    "modeler", "monochrome", "meme", "cosmic", "marvel", "avengers",
    "disney", "starwars", "lunar", "fusemon", "april", "fool", "fools",
    "cakemon", "cake", "gamer", "mecha", "surfing", "spook", "spooky",
}

# Skins we stage. Shiny gets its own directory under static/models-3d/shiny/,
# matching what the pokedex template at layouts/pokedex/single.html expects.
SKINS = ("regular", "shiny")


def make_uv_scaler(bb: dict):
    """Returns `uv_scale_for(tex_idx)` for converting bbmodel face UVs to
    0..16 space. Face UVs are expressed in the *texture's* uv_width units,
    not the project resolution — when those differ (e.g. project=64 with a
    128-px atlas), using the project value over-scales every UV by 2× and
    faces sample the wrong region of the atlas."""
    proj_w = float((bb.get("resolution") or {}).get("width", 16) or 16)
    textures = bb.get("textures") or []
    def uv_scale_for(tex_idx) -> float:
        if isinstance(tex_idx, int) and 0 <= tex_idx < len(textures):
            uv_w = textures[tex_idx].get("uv_width")
            if uv_w:
                return 16.0 / float(uv_w)
        return 16.0 / proj_w
    return uv_scale_for


def make_tex_remap(bb: dict) -> dict[int, str]:
    """Map bbmodel texture indices to the staged JSON's two material slots.
    Bbmodels carry a long list of skin-variant textures (halloween, shiny, …)
    we don't ship, so we collapse the index space to "#0" (body) and "#1"
    (flame) by name — any bbmodel texture whose name carries "flame" routes
    to #1, everything else to #0."""
    out: dict[int, str] = {}
    for idx, t in enumerate(bb.get("textures") or []):
        name = (t.get("name") or "").lower()
        out[idx] = "#1" if "flame" in name else "#0"
    return out


def cube_to_mc_element(e: dict, uv_scale_for, tex_remap: dict[int, str] | None = None) -> dict | None:
    """Convert a bbmodel cube to an MC-JSON element. UVs are rescaled to
    0..16 space and the cube's single-axis rotation (if any) is preserved.
    Multi-axis bbmodel cube rotations are dropped — those would need full
    vertex transformation and don't fit MC's one-axis rotation field; in
    practice no shipped bbmodel has them on a cube (only on bones)."""
    if "from" not in e or "to" not in e:
        return None
    faces_out: dict[str, dict] = {}
    for fname, f in (e.get("faces") or {}).items():
        if not isinstance(f, dict):
            continue
        tex = f.get("texture")
        if tex_remap is not None and isinstance(tex, int) and tex in tex_remap:
            tex_ref = tex_remap[tex]
        else:
            tex_ref = f"#{tex}" if isinstance(tex, int) else "#0"
        scale = uv_scale_for(tex)
        uv = f.get("uv", [0, 0, 16.0 / scale, 16.0 / scale])
        if isinstance(uv, list) and len(uv) >= 4:
            uv = [uv[0] * scale, uv[1] * scale, uv[2] * scale, uv[3] * scale]
        face_out = {"uv": uv, "texture": tex_ref}
        if "rotation" in f:
            face_out["rotation"] = f["rotation"]
        faces_out[fname] = face_out
    cube = {"from": list(e["from"]), "to": list(e["to"]), "faces": faces_out}
    rot = e.get("rotation")
    origin = e.get("origin") or [0, 0, 0]
    if isinstance(rot, list) and len(rot) >= 3:
        non_zero = [(i, r) for i, r in enumerate(rot[:3]) if r != 0]
        if len(non_zero) == 1:
            axis_idx, angle = non_zero[0]
            cube["rotation"] = {
                "angle": angle, "axis": "xyz"[axis_idx],
                "origin": [origin[0], origin[1], origin[2]],
            }
    elif isinstance(rot, dict):
        cube["rotation"] = rot
    return cube


def walk_bbmodel_to_bones(bb: dict, root_name: str, uv_scale_for, tex_remap,
                          skip_groups: set[str]) -> dict | None:
    """Walk the bbmodel outliner under `root_name` and emit a nested-bones
    dict tree. Each bone records its parent-relative origin, rotation, the
    cubes parented directly to it (in bone-local coords), and child bones.

    Bbmodel cubes are stored in absolute world coords with parent bones'
    rotations *not* baked in — at zero rotation the cubes occupy their
    "rest before any pose" positions, and the bone rotations are what bring
    them into the rest pose seen in Blockbench. We translate cube vertices
    into the bone-local frame so that downstream three.js group rotation
    around `bone.origin` produces the rendered rest pose without us having
    to bake any matrices in Python."""
    elements_by_uuid = {e["uuid"]: e for e in bb.get("elements", []) if "uuid" in e}

    def emit_bone(node: dict, parent_world_origin: list[float]) -> dict:
        world_origin = list(node.get("origin") or [0.0, 0.0, 0.0])[:3]
        # Pad short origin/rotation arrays defensively.
        while len(world_origin) < 3:
            world_origin.append(0.0)
        local_origin = [world_origin[i] - parent_world_origin[i] for i in range(3)]
        rotation = list(node.get("rotation") or [0.0, 0.0, 0.0])[:3]
        while len(rotation) < 3:
            rotation.append(0.0)
        out_elements: list[dict] = []
        out_children: list[dict] = []
        for child in node.get("children", []) or []:
            if isinstance(child, str):
                e = elements_by_uuid.get(child)
                if not e:
                    continue
                mc = cube_to_mc_element(e, uv_scale_for, tex_remap)
                if not mc:
                    continue
                mc["from"] = [mc["from"][i] - world_origin[i] for i in range(3)]
                mc["to"] = [mc["to"][i] - world_origin[i] for i in range(3)]
                rot = mc.get("rotation")
                if isinstance(rot, dict) and "origin" in rot:
                    o = rot["origin"]
                    mc["rotation"] = dict(rot, origin=[
                        o[0] - world_origin[0],
                        o[1] - world_origin[1],
                        o[2] - world_origin[2],
                    ])
                out_elements.append(mc)
            elif isinstance(child, dict):
                if (child.get("name") or "") in skip_groups:
                    continue
                out_children.append(emit_bone(child, world_origin))
        return {
            "name": node.get("name") or "",
            "origin": local_origin,
            "rotation": rotation,
            "elements": out_elements,
            "children": out_children,
        }

    # Most bbmodels keep the base skin in a "body" group, but a fair number
    # name it after the species (arbok, bidoof…) or leave it unnamed. The
    # "hitbox" group always sits beside it as a sibling and contains a single
    # placeholder cube — never treat that one as the root.
    for top in bb.get("outliner", []) or []:
        if isinstance(top, dict) and top.get("name") == root_name:
            return emit_bone(top, [0.0, 0.0, 0.0])
    for top in bb.get("outliner", []) or []:
        if not isinstance(top, dict):
            continue
        if (top.get("name") or "").lower() == "hitbox":
            continue
        return emit_bone(top, [0.0, 0.0, 0.0])
    return None


def texture_kind(name: str, species: str) -> tuple[str, str] | None:
    """Classify a bbmodel texture name into `(skin, role)` where skin is
    'regular' or 'shiny' and role is 'body' or 'flame'. Returns None for
    event-cosmetic variants we don't ship.

    Examples (species='charizard'):
      'charizard'              -> ('regular', 'body')
      'charizard_shiny'        -> ('shiny',   'body')
      'charizard_flame'        -> ('regular', 'flame')
      'charizard_flame_shiny'  -> ('shiny',   'flame')
      'charizard_halloween'    -> None
      'charizard_flame_aura'   -> None
    Form tokens like 'alola'/'galarian' are accepted (alolan_exeggutor's base
    body texture is 'alolan_exeggutor_alola')."""
    nl = name.lower()
    sp = species.lower()
    if nl == sp:
        suffix_tokens: set[str] = set()
    elif nl.startswith(sp + "_"):
        suffix_tokens = set(nl[len(sp) + 1:].split("_"))
    else:
        return None
    if suffix_tokens & EVENT_TOKENS:
        return None
    skin = "shiny" if "shiny" in suffix_tokens else "regular"
    role = "flame" if "flame" in suffix_tokens else "body"
    return skin, role


def resolve_texture_file(species: str, bb_tex_name: str) -> Path | None:
    """Find the resource-pack PNG for a given bbmodel texture name. The
    BetterModel exporter usually prepends the species: bbmodel 'charizard' →
    file 'charizard_charizard.png'. Form variants (alolan/galarian/hisuian)
    additionally get a `_v_<form>_` infix — we don't try to derive the form
    tag, instead falling back to a directory scan and picking the shortest
    matching filename so we don't pick a holiday/skin variant by accident."""
    direct = PACK_BM_TEXTURES / "item" / f"{species}_{bb_tex_name}.png"
    if direct.exists():
        return direct
    suffix = f"_{bb_tex_name}.png"
    candidates = [p for p in (PACK_BM_TEXTURES / "item").glob(f"{species}_*{suffix}")
                  if p.name.endswith(suffix)]
    if not candidates:
        return None
    return min(candidates, key=lambda p: len(p.name))


def derive_textures(bb: dict, species: str, skin: str) -> tuple[dict[str, str], list[Path]]:
    """Pick the body and (optional) flame textures for the requested skin
    plus the source PNG paths to copy. If the species lacks a shiny flame
    texture, the shiny output reuses the regular flame (Charizard's flame
    doesn't recolour for shiny — only the body atlas does)."""
    body_name: str | None = None
    flame_name: str | None = None
    regular_flame_fallback: str | None = None
    for t in bb.get("textures") or []:
        n = (t.get("name") or "").removesuffix(".png")
        if not n:
            continue
        kind = texture_kind(n, species)
        if kind is None:
            continue
        s, r = kind
        if s == skin:
            if r == "body" and body_name is None:
                body_name = n
            elif r == "flame" and flame_name is None:
                flame_name = n
        elif s == "regular" and r == "flame" and skin == "shiny":
            if regular_flame_fallback is None:
                regular_flame_fallback = n
    if not flame_name and skin == "shiny":
        flame_name = regular_flame_fallback
    textures: dict[str, str] = {}
    srcs: list[Path] = []
    if body_name:
        src = resolve_texture_file(species, body_name)
        if src is not None:
            ref = f"bettermodel/item/{src.stem}"
            textures["0"] = ref
            textures["particle"] = ref
            srcs.append(src)
    if flame_name:
        src = resolve_texture_file(species, flame_name)
        if src is not None:
            textures["1"] = f"bettermodel/item/{src.stem}"
            srcs.append(src)
    return textures, srcs


def count_bones_and_elements(bone: dict) -> tuple[int, int]:
    n_bones = 1
    n_elems = len(bone.get("elements") or [])
    for c in bone.get("children") or []:
        b, e = count_bones_and_elements(c)
        n_bones += b
        n_elems += e
    return n_bones, n_elems


def resolve_output_path(species: str) -> tuple[str, str]:
    """Map a bbmodel filename stem to (variant, slug). Filenames like
    `alolan_exeggutor` route to the alolan/ subtree under the bare species
    slug; everything else lives under regular/<slug>."""
    for prefix in VARIANT_PREFIXES:
        if species.startswith(prefix + "_"):
            return prefix, species[len(prefix) + 1:].replace("_", "-")
    return "regular", species.replace("_", "-")


def stage_one(bb_path: Path, pokedex_pages: set[str]) -> dict[str, str]:
    """Stage a single bbmodel for every applicable skin. Returns a dict
    keyed by skin (e.g. 'regular', 'shiny') with per-skin status strings —
    'ok', 'no-page', 'no-root', 'no-texture', or 'missing-texture:<file>'.
    The 'shiny' key is omitted for non-base form variants (alolan/galarian)
    to match the wiki template's "regular form only" shiny policy."""
    species = bb_path.stem  # 'charizard', 'alolan_exeggutor', …
    variant, slug = resolve_output_path(species)
    if slug not in pokedex_pages:
        return {"regular": "no-page"}
    bb = json.loads(bb_path.read_text())
    uv_scale_for = make_uv_scaler(bb)
    tex_remap = make_tex_remap(bb)
    root = walk_bbmodel_to_bones(bb, ROOT_BONE_DEFAULT, uv_scale_for, tex_remap, SKIP_BONES)
    if root is None:
        return {"regular": "no-root"}
    bones_payload = [root]
    statuses: dict[str, str] = {}
    for skin in SKINS:
        if skin == "shiny" and variant != "regular":
            continue
        textures, texture_srcs = derive_textures(bb, species, skin)
        if not textures:
            statuses[skin] = "no-texture"
            continue
        out_dir = (OUT_BASE / "shiny" / slug) if skin == "shiny" else (OUT_BASE / variant / slug)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{slug}.json").write_text(
            json.dumps({"textures": textures, "bones": bones_payload})
        )
        missing: str | None = None
        for src in texture_srcs:
            if not src.exists():
                missing = src.name
                break
            shutil.copy2(src, out_dir / src.name)
        statuses[skin] = f"missing-texture:{missing}" if missing else "ok"
    return statuses


def main() -> int:
    if not MODELS_DIR.is_dir():
        print(f"Models dir not found: {MODELS_DIR}", file=sys.stderr)
        return 1
    if not PACK_BM_TEXTURES.is_dir():
        print(f"Textures not extracted at {PACK_BM_TEXTURES}", file=sys.stderr)
        print("Run: unzip -q -o ~/.minecraft/resourcepacks/devhelditem.zip "
              "-d /tmp/devhelditem", file=sys.stderr)
        return 1

    pokedex_pages = {p.stem for p in POKEDEX_DIR.glob("*.md")}
    per_skin = {skin: {"ok": 0, "no-page": 0, "no-root": 0,
                       "no-texture": 0, "error": 0} for skin in SKINS}
    failures: list[tuple[str, str, str]] = []

    for bb_path in sorted(MODELS_DIR.glob("*.bbmodel")):
        try:
            statuses = stage_one(bb_path, pokedex_pages)
        except Exception as exc:
            statuses = {"regular": f"error:{exc}"}
        for skin, status in statuses.items():
            bucket = per_skin[skin]
            if status == "ok":
                bucket["ok"] += 1
            elif status in bucket:
                bucket[status] += 1
            else:
                bucket["error"] += 1
                failures.append((bb_path.stem, skin, status))

    for skin in SKINS:
        b = per_skin[skin]
        print(f"{skin:>8}: ok={b['ok']}  no-page={b['no-page']}  no-root={b['no-root']}  "
              f"no-texture={b['no-texture']}  error={b['error']}")
    for stem, skin, msg in failures:
        print(f"  ! {stem} [{skin}]: {msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
