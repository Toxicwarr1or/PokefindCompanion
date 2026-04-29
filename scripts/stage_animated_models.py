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
import struct

try:
    from PIL import Image
    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False
import sys
from pathlib import Path

MODELS_DIR = Path("/home/jack/Downloads/models")
PACK_BM_TEXTURES = Path("/tmp/devhelditem/assets/bettermodel/textures")
PACK_BM_MODELS = Path("/tmp/devhelditem/assets/bettermodel/models/modern_item")

# Per-(species, skin) overrides where the bbmodel's body geometry doesn't
# fit the variant atlas, so we composite the BetterModel exporter's part
# files instead. Each entry lists the part-file *suffixes* (after
# `<species>_v_<skin>_`) to include — we drop holiday/event sub-variants
# (halloween, valentine, gamer when not the wanted skin) and keep the
# core body parts for that skin.
PART_FILE_OVERRIDES: dict[tuple[str, str], tuple[str, ...]] = {
    # Rotom's meme skin is a 64×64 Bart Simpson character UV-unwrapped on
    # a different geometry from the regular 32×32 ghost-ish rotom. The
    # BetterModel exporter ships meme-specific part files
    # (rotom_v_meme_rotom_1.json + lefthand/righthand) — compose those.
    ("rotom", "meme"): ("rotom", "lefthand", "righthand"),
}
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

# Cosmetic skins we ship — each gets its own output directory under
# `static/models-3d/<skin>/`. The canonical list of skin keys lives in
# `data/cosmetic_skins.yaml` (shared with the static stager and the
# pokedex template); below we map bbmodel-texture *tokens* (single-word
# slices of a bbmodel texture name like `charizard_halloween`) to those
# canonical skin keys. Aliases handle short-form tokens for multi-word
# skin keys (`lunar` → `lunar_new_year`).
COSMETIC_SKINS_YAML = Path(__file__).resolve().parent.parent / "data/cosmetic_skins.yaml"


def _load_canonical_skin_keys() -> tuple[str, ...]:
    keys: list[str] = []
    for line in COSMETIC_SKINS_YAML.read_text().splitlines():
        s = line.strip()
        if s.startswith("- key:"):
            keys.append(s.split(":", 1)[1].strip())
    return tuple(keys)


CANONICAL_SKIN_KEYS = _load_canonical_skin_keys()

# Token → canonical key. Identity entries cover the simple single-word
# skins (`shiny`, `aura`, `halloween`, …); explicit aliases bridge
# bbmodel names that abbreviate the canonical key (`lunar` for
# `lunar_new_year`, `april`/`fool`/`fools` for `april_fools`, etc.).
COSMETIC_SKIN_TOKENS: dict[str, str] = {k: k for k in CANONICAL_SKIN_KEYS}
COSMETIC_SKIN_TOKENS.update({
    "anni": "anniversary",
    "xmas": "christmas",
    "spook": "halloween", "spooky": "halloween",
    "lunar": "lunar_new_year",
    "avengers": "marvel",
    "april": "april_fools",
    "aprilfools": "april_fools",
    "fool": "april_fools", "fools": "april_fools",
    "cake": "cakemon",
    "sword": "sword_and_shield", "shield": "sword_and_shield",
})

# Output directory order (regular always first), preserving the YAML order.
SKINS: tuple[str, ...] = ("regular",) + CANONICAL_SKIN_KEYS


def copy_texture(src: Path, dst: Path) -> None:
    """Copy a PNG, stripping any animation: when `<src>.mcmeta` declares a
    vertical frame sprite-sheet, write only the first square frame so the
    static viewer doesn't show all frames stacked at once. Mewtwo's gamer
    atlas is the canonical case (64×192 = three 64×64 frames + an mcmeta);
    leaving it intact made the body's UVs sample frames 2 and 3 by
    accident."""
    mcmeta = src.with_suffix(src.suffix + ".mcmeta")
    if mcmeta.exists() and _HAS_PIL:
        try:
            meta = json.loads(mcmeta.read_text())
        except json.JSONDecodeError:
            meta = {}
        if "animation" in meta:
            try:
                with Image.open(src) as img:
                    w, h = img.size
                    if h > w:
                        img.crop((0, 0, w, w)).save(dst)
                        return
            except Exception:
                pass
    shutil.copy2(src, dst)


def png_pixel_width(path: Path) -> int | None:
    """Read just the IHDR width from a PNG without pulling in PIL."""
    if not path or not path.exists():
        return None
    with open(path, "rb") as f:
        f.read(16)  # signature + IHDR length + 'IHDR'
        return int(struct.unpack(">I", f.read(4))[0])


def make_uv_scaler(bb: dict, file_widths: dict[str, int] | None = None):
    """Returns `uv_scale_for(tex_idx)` for converting bbmodel face UVs to
    0..16 space. The rule (verified by reverse-engineering the BetterModel
    exporter's output for Charizard / Weavile / Seismitoad / Bisharp /
    Rotom):

      * If the resourcepack file is *larger* than the bbmodel-embedded
        texture, the exporter padded the embedded into the bigger file at
        native pixel size (top-left, transparent margins). UV `u` lands at
        file pixel `u`, so sample at `u / file_width` →
        `scale = 16 / file_width`. Bisharp & Magnezone fall here.

      * Otherwise (file == embedded, or file smaller — a downscale), the
        bbmodel UV is in the texture's own `uv_width` units; UV
        `uv_width` covers the whole texture, so `scale = 16 / uv_width`.
        Charizard, Weavile, Seismitoad, and Rotom all fall here.

    Why not `embedded_width` directly? Blockbench scales the embedded
    texture to fit the per-texture `uv_width` UV space, so face UVs are
    expressed in `uv_width` units — not embedded pixels — when the file
    isn't padded.

    `file_widths` is a per-role lookup `{"body": int, "flame": int}` built
    up-front by reading PNG headers in `stage_one`."""
    proj_w = float((bb.get("resolution") or {}).get("width", 16) or 16)
    textures = bb.get("textures") or []
    file_widths = file_widths or {}

    # Find the bbmodel texture entries that the *shipped* atlas (body, flame)
    # actually corresponds to, ignoring skin variants. Faces in the bbmodel
    # may reference any texture index (Weavile authors faces against an
    # event/anniversary texture for instance), but the staged JSON only
    # ships the body and optional flame atlases — so UV scaling must be
    # relative to *those* textures' metadata, not whatever the face is bound
    # to in the bbmodel.
    body_t: dict = {}
    flame_t: dict = {}
    for t in textures:
        n = (t.get("name") or "")
        if not n or is_variant_texture_name(n):
            continue
        if "flame" in n.lower():
            if not flame_t:
                flame_t = t
        elif not body_t:
            body_t = t

    def _scale_for_role(t: dict, role: str) -> float:
        uv_w = float(t.get("uv_width") or proj_w)
        emb_w = float(t.get("width") or uv_w)
        file_w = float(file_widths.get(role) or 0)
        # Empirically verified against the BetterModel exporter's UVs:
        #   - uv_width == embedded_width: bbmodel UVs are file-pixel
        #     coordinates, so divisor = file_width (Bisharp, Magnezone,
        #     Rotom, Charizard).
        #   - uv_width != embedded_width: Blockbench scaled the embedded
        #     into the uv_width logical space; divisor = uv_width
        #     (Weavile, Seismitoad, Arcanine).
        divisor = file_w if uv_w == emb_w and file_w > 0 else uv_w
        return 16.0 / divisor if divisor > 0 else 16.0 / proj_w

    body_scale = _scale_for_role(body_t, "body") if body_t else 16.0 / proj_w
    flame_scale = _scale_for_role(flame_t, "flame") if flame_t else body_scale

    def uv_scale_for(tex_idx) -> float:
        # Route by the face's bound texture name — flame textures go to
        # `flame_scale` regardless of which index they're at; everything
        # else to `body_scale`.
        if isinstance(tex_idx, int) and 0 <= tex_idx < len(textures):
            if "flame" in (textures[tex_idx].get("name") or "").lower():
                return flame_scale
        return body_scale
    return uv_scale_for


def is_variant_texture_name(name: str) -> bool:
    """Quick check: does this bbmodel texture name look like a cosmetic
    skin variant (not the regular base body atlas)? Used by `make_uv_scaler`
    to pick the canonical regular body/flame textures whose dimensions
    drive the UV scaler — variant atlases sometimes have different sizes
    and would skew the scale."""
    tokens = set(name.lower().removesuffix(".png").split("_"))
    return any(t in tokens for t in COSMETIC_SKIN_TOKENS)


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


def _emit_bone(node: dict, parent_world_origin: list[float],
               elements_by_uuid: dict, uv_scale_for, tex_remap,
               skip_groups: set[str]) -> dict:
    """Recursively emit one bbmodel outliner node as a bones-tree dict.

    Bbmodel cubes are stored in absolute world coords with parent bones'
    rotations *not* baked in — at zero rotation the cubes occupy their
    "rest before any pose" positions, and the bone rotations are what bring
    them into the rest pose seen in Blockbench. We translate cube vertices
    into the bone-local frame so that downstream three.js group rotation
    around `bone.origin` produces the rendered rest pose without us having
    to bake any matrices in Python."""
    world_origin = list(node.get("origin") or [0.0, 0.0, 0.0])[:3]
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
            out_children.append(_emit_bone(
                child, world_origin, elements_by_uuid,
                uv_scale_for, tex_remap, skip_groups))
    return {
        "name": node.get("name") or "",
        "origin": local_origin,
        "rotation": rotation,
        "elements": out_elements,
        "children": out_children,
    }


def walk_bbmodel_to_bones(bb: dict, root_name: str, uv_scale_for, tex_remap,
                          skip_groups: set[str]) -> list[dict]:
    """Walk the bbmodel outliner and emit the base-skin bones — the body
    group plus any auxiliary top-level sibling groups that aren't
    hitboxes and aren't named after a cosmetic skin.

    Most bbmodels keep the base skin in a "body" group, but some name it
    after the species (arbok, bidoof…) or leave it unnamed. Some (Mewtwo,
    Mew) split base geometry across multiple top-level groups: the main
    body in one, then auxiliary cubes (Mewtwo's "shadow_*" psychic-aura
    cubes around the head, "tail6_*" tail-tip extension) in unnamed
    siblings. Those need to render alongside the body on every skin —
    they're not skin-specific.

    Skin-named top-level groups (Charizard's "halloween", "christmas",
    etc.) are *excluded* from the base walk; `walk_skin_addon_group`
    picks them up only for the matching skin tab."""
    elements_by_uuid = {e["uuid"]: e for e in bb.get("elements", []) if "uuid" in e}
    skin_names = {k.lower() for k in COSMETIC_SKIN_TOKENS.keys()}
    skin_names |= {v.lower() for v in COSMETIC_SKIN_TOKENS.values()}

    body_group = None
    for top in bb.get("outliner", []) or []:
        if isinstance(top, dict) and top.get("name") == root_name:
            body_group = top
            break
    if body_group is None:
        for top in bb.get("outliner", []) or []:
            if not isinstance(top, dict):
                continue
            if (top.get("name") or "").lower() == "hitbox":
                continue
            body_group = top
            break
    if body_group is None:
        return []

    def is_hitbox_group(node: dict) -> bool:
        """Hitbox groups can be named "hitbox" or anonymous — in the latter
        case the single cube inside carries a `hitbox_*` name. Detect both."""
        if (node.get("name") or "").lower() == "hitbox":
            return True
        kids = node.get("children") or []
        if len(kids) == 1 and isinstance(kids[0], str):
            cube = elements_by_uuid.get(kids[0])
            if cube and (cube.get("name") or "").lower().startswith("hitbox"):
                return True
        return False

    bones: list[dict] = [_emit_bone(body_group, [0.0, 0.0, 0.0], elements_by_uuid,
                                    uv_scale_for, tex_remap, skip_groups)]
    for top in bb.get("outliner", []) or []:
        if not isinstance(top, dict) or top is body_group:
            continue
        if is_hitbox_group(top):
            continue
        name = (top.get("name") or "").lower()
        if name and name in skin_names:
            continue   # picked up per-skin by walk_skin_addon_group
        aux_bone = _emit_bone(top, [0.0, 0.0, 0.0], elements_by_uuid,
                              uv_scale_for, tex_remap, skip_groups)
        # Auxiliary base bones are typically VFX cubes that the in-game
        # renderer fades / pulses (Mewtwo's psychic-aura `shadow_*` cubes
        # around the head, the `tail6_*` energy trail behind it). Mark
        # them translucent so the viewer renders them at reduced opacity
        # — without this hint they show as solid colored blocks where the
        # in-game effect is a glow.
        aux_bone["opacity"] = 0.4
        bones.append(aux_bone)
    return bones


def walk_skin_addon_group(bb: dict, skin_key: str, uv_scale_for, tex_remap,
                          skip_groups: set[str]) -> dict | None:
    """Find a top-level bbmodel group that adds skin-specific geometry
    (Charizard's `christmas` group has a Santa hat, `halloween` has horns,
    etc.) and emit it as a parallel bone tree. Matches by canonical skin
    key OR any of its bbmodel-token aliases (so `lunar` → lunar_new_year,
    `xmas` → christmas, etc.). Returns None if no such group exists for
    the requested skin."""
    aliases: set[str] = {skin_key.lower()}
    for token, dirname in COSMETIC_SKIN_TOKENS.items():
        if dirname == skin_key:
            aliases.add(token)
    elements_by_uuid = {e["uuid"]: e for e in bb.get("elements", []) if "uuid" in e}
    for top in bb.get("outliner", []) or []:
        if not isinstance(top, dict):
            continue
        if (top.get("name") or "").lower() in aliases:
            return _emit_bone(top, [0.0, 0.0, 0.0], elements_by_uuid,
                              uv_scale_for, tex_remap, skip_groups)
    return None


def texture_kind(name: str, species: str) -> tuple[str, str] | None:
    """Classify a bbmodel texture name into `(skin, role)` where skin is
    `regular` or one of `COSMETIC_SKIN_TOKENS.values()`, and role is
    `body` or `flame`. Returns None when the name doesn't belong to this
    species (different prefix).

    Examples (species='charizard'):
      'charizard'              -> ('regular', 'body')
      'charizard_shiny'        -> ('shiny',     'body')
      'charizard_aura'         -> ('aura',      'body')
      'charizard_halloween'    -> ('halloween', 'body')
      'charizard_flame'        -> ('regular',   'flame')
      'charizard_flame_shiny'  -> ('shiny',     'flame')
      'charizard_flame_aura'   -> ('aura',      'flame')
    Form tokens like 'alola'/'galarian' are accepted as part of the body
    name (alolan_exeggutor's base body texture is 'alolan_exeggutor_alola').
    When a name carries multiple skin tokens (e.g. 'charizard_flame_halloween'
    *and* '_shiny'), we pick whichever appears first in the SKINS order."""
    nl = name.lower()
    sp = species.lower()
    if nl == sp:
        suffix_tokens: set[str] = set()
    elif nl.startswith(sp + "_"):
        suffix_tokens = set(nl[len(sp) + 1:].split("_"))
    else:
        return None
    skin = "regular"
    for token, dirname in COSMETIC_SKIN_TOKENS.items():
        if token in suffix_tokens:
            skin = dirname
            break
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
    plus the source PNG paths to copy. If a non-regular skin lacks its own
    flame texture, the output reuses the regular flame (Charizard's flame
    is shared between shiny and the regular body atlas, for instance)."""
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
        elif s == "regular" and r == "flame" and skin != "regular":
            if regular_flame_fallback is None:
                regular_flame_fallback = n
    # A non-regular skin is only "real" if the bbmodel ships a *body*
    # atlas for it — flame is a per-cube particle layer, sharing it with
    # the regular skin alone doesn't constitute a recolor. Without this
    # guard, the regular-flame fallback below would cause every skin in
    # SKINS to produce a flame-only output for fire types (Charizard ends
    # up with chips for cosmic, gamer, mecha, etc. it doesn't have).
    if skin != "regular" and not body_name:
        return {}, []
    if not flame_name and skin != "regular":
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


def stage_from_part_files(species: str, skin: str, slug: str, out_dir: Path,
                          part_suffixes: tuple[str, ...]) -> str:
    """Stage a skin by combining the BetterModel exporter's part files into
    a single flat-elements JSON. Used when the bbmodel's geometry doesn't
    match the variant atlas (Rotom meme is the canonical case — the meme
    atlas is a different model entirely)."""
    elements: list[dict] = []
    textures: dict[str, str] = {}
    texture_srcs: set[Path] = set()
    found_any = False
    for suffix in part_suffixes:
        p = PACK_BM_MODELS / f"{species}_v_{skin}_{suffix}_1.json"
        if not p.exists():
            continue
        try:
            part = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        found_any = True
        # Texture refs are namespaced `bettermodel:item/<file>` — drop the
        # namespace prefix so the viewer's path-tail filename rule resolves
        # them to a sibling PNG in the staged dir.
        for k, v in (part.get("textures") or {}).items():
            if isinstance(v, str):
                clean = v.replace("bettermodel:", "bettermodel/")
                textures.setdefault(k, clean)
                rel = clean.split("/", 1)[1] if "/" in clean else clean
                texture_srcs.add(PACK_BM_TEXTURES / f"{rel}.png")
        for elem in part.get("elements") or []:
            elements.append(elem)
    if not found_any or not elements:
        return "no-parts"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{slug}.json").write_text(
        json.dumps({"textures": textures, "elements": elements})
    )
    for src in sorted(texture_srcs):
        if not src.exists():
            return f"missing-texture:{src.name}"
        copy_texture(src, out_dir / src.name)
    return "ok"


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
    # The UV scaler depends on the *resourcepack* file dimensions (see
    # `make_uv_scaler` for why), so resolve regular textures up front to get
    # those sizes, then build the scaler, then walk the model. Geometry is
    # shared between regular and shiny so we only do this once.
    regular_textures, regular_srcs = derive_textures(bb, species, "regular")
    file_widths: dict[str, int] = {}
    for src in regular_srcs:
        w = png_pixel_width(src)
        if not w:
            continue
        role = "flame" if "flame" in src.stem.lower() else "body"
        file_widths.setdefault(role, w)
    uv_scale_for = make_uv_scaler(bb, file_widths)
    tex_remap = make_tex_remap(bb)
    base_bones = walk_bbmodel_to_bones(bb, ROOT_BONE_DEFAULT, uv_scale_for, tex_remap, SKIP_BONES)
    if not base_bones:
        return {"regular": "no-root"}
    statuses: dict[str, str] = {}
    for skin in SKINS:
        # Skin-as-overlay variants (shiny, aura) only ship for the base
        # `regular` form variant — alolan/galarian forms don't have shipped
        # aura/shiny atlases in the pack.
        if skin != "regular" and variant != "regular":
            continue

        # If this (species, skin) is in PART_FILE_OVERRIDES, build the
        # output from the BetterModel exporter's part files instead of
        # the bbmodel — used when the variant atlas targets a different
        # geometry than the bbmodel's body (Rotom meme).
        override_parts = PART_FILE_OVERRIDES.get((species, skin))
        if override_parts is not None:
            out_dir = OUT_BASE / skin / slug
            statuses[skin] = stage_from_part_files(species, skin, slug, out_dir,
                                                   override_parts)
            continue

        if skin == "regular":
            textures, texture_srcs = regular_textures, regular_srcs
        else:
            textures, texture_srcs = derive_textures(bb, species, skin)
        if not textures:
            statuses[skin] = "no-texture"
            continue
        # Skip variant skins whose body atlas has different dimensions to
        # the regular's after multi-frame cropping — that means the variant
        # is a different model's atlas and rendering the regular geometry
        # against it produces visual garbage. Cases where we DO want the
        # variant (Rotom meme has a meme-specific exporter geometry) are
        # handled via PART_FILE_OVERRIDES above.
        if skin != "regular" and file_widths.get("body"):
            body_src = next((s for s in texture_srcs
                             if "flame" not in s.stem.lower()), None)
            if body_src and body_src.exists():
                bw = png_pixel_width(body_src)
                if bw and bw != file_widths["body"]:
                    statuses[skin] = "size-mismatch"
                    continue
        # Some skins (Charizard's christmas/halloween/easter/thanksgiving/
        # summer) ship extra geometry in their own top-level bbmodel group
        # alongside `body`. When staging that skin, walk the addon group
        # too and append it as a parallel bone tree — its sub-bones mirror
        # the body's transforms, so cubes inside (Santa hat, horns, etc.)
        # render in the right place automatically.
        bones_payload = list(base_bones)
        if skin != "regular":
            addon = walk_skin_addon_group(bb, skin, uv_scale_for, tex_remap, SKIP_BONES)
            if addon is not None:
                bones_payload.append(addon)
        out_dir = (OUT_BASE / skin / slug) if skin != "regular" else (OUT_BASE / variant / slug)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{slug}.json").write_text(
            json.dumps({"textures": textures, "bones": bones_payload})
        )
        missing: str | None = None
        for src in texture_srcs:
            if not src.exists():
                missing = src.name
                break
            copy_texture(src, out_dir / src.name)
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
