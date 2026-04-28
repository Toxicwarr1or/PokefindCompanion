#!/usr/bin/env python3
"""
Convert Blockbench .bbmodel files into flat Minecraft-style block-model JSON
files with cuboid elements pre-positioned in world space (using the bbmodel's
bone hierarchy). Each species gets one output file the existing model-viewer.js
can render without further changes.

Embedded textures (base64-encoded inside the .bbmodel) are extracted to
static/textures/bbmodel/<species>/<texture-name>.png. Texture refs in the
output model use the form "bbmodel:<species>/<texture-name>" so the viewer's
existing prefix resolver can map them to URLs.

Usage:
    python3 scripts/convert_bbmodels.py [--src DIR] [--out-models DIR] [--out-textures DIR]
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = Path("/home/jack/Downloads/models")
DEFAULT_OUT_MODELS = ROOT / "static/models/bbmodel"
DEFAULT_OUT_TEXTURES = ROOT / "static/textures/bbmodel"


# ---------- 4x4 matrix helpers (column-major; transform points by matrix.dot(v)) ----------

def mat_identity():
    return [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

def mat_translate(tx, ty, tz):
    m = mat_identity()
    m[0][3] = tx
    m[1][3] = ty
    m[2][3] = tz
    return m

def mat_rotate_x(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1],
    ]

def mat_rotate_y(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1],
    ]

def mat_rotate_z(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

def mat_mul(a, b):
    out = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            out[i][j] = sum(a[i][k] * b[k][j] for k in range(4))
    return out

def mat_apply(m, v):
    """Apply a 4x4 to a 3-vec point (treats as homogeneous w=1)."""
    return [
        m[0][0]*v[0] + m[0][1]*v[1] + m[0][2]*v[2] + m[0][3],
        m[1][0]*v[0] + m[1][1]*v[1] + m[1][2]*v[2] + m[1][3],
        m[2][0]*v[0] + m[2][1]*v[1] + m[2][2]*v[2] + m[2][3],
    ]


def bone_local_transform(origin_world, parent_origin_world, rotation_deg):
    """Compose translate-to-pivot · rotate · translate-from-pivot in the parent's frame.
    Origin is given in WORLD coords (Blockbench convention). The local offset is
    (origin_world - parent_origin_world). Rotation is applied around the bone's
    pivot (which is the bone's origin)."""
    rx, ry, rz = rotation_deg
    tx, ty, tz = origin_world[0] - parent_origin_world[0], origin_world[1] - parent_origin_world[1], origin_world[2] - parent_origin_world[2]
    # Rotate around the bone's pivot (origin_world). To do that in the parent's frame,
    # we need: translate to (origin - parent_origin), rotate, then NOT translate back —
    # because the rotation is about the pivot point itself, the post-rotate position
    # IS the pivot. Children declare their origin in parent's frame; their origin
    # arrives already accounting for any parent rotation when we walk recursively.
    # The simpler formulation: bone_local = T(local_offset) · R(x) · R(y) · R(z)
    # then the bone's pivot is at the local_offset position (post-translate).
    R = mat_mul(mat_mul(mat_rotate_z(rz), mat_rotate_y(ry)), mat_rotate_x(rx))
    T = mat_translate(tx, ty, tz)
    return mat_mul(T, R)


# ---------- Bbmodel parsing ----------

def slug_from_filename(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "_", path.stem.lower()).strip("_")


def collect_elements(outliner_node, elem_by_uuid, parent_world_xform, parent_origin_world, accumulator):
    """Recursively walk outliner, accumulating (world_transform, element) pairs.
    `parent_world_xform` is the cumulative transform from world root down to this
    bone's parent; `parent_origin_world` is the parent's pivot in world coords."""
    if isinstance(outliner_node, str):
        # Direct element reference under the current bone — apply current transform
        el = elem_by_uuid.get(outliner_node)
        if el and el.get("visibility", True):
            accumulator.append((parent_world_xform, el))
        return

    # outliner_node is a bone/group dict
    origin_world = outliner_node.get("origin", [0, 0, 0])
    rotation = outliner_node.get("rotation", [0, 0, 0])
    # Compose this bone's transform in the parent's frame
    local = bone_local_transform(origin_world, parent_origin_world, rotation)
    bone_world_xform = mat_mul(parent_world_xform, local)
    # Walk children
    for child in outliner_node.get("children", []):
        collect_elements(child, elem_by_uuid, bone_world_xform, origin_world, accumulator)


# ---------- Element transform ----------

def transform_element(element: dict, world_xform: list[list[float]]) -> dict:
    """Convert a bbmodel cube into a Minecraft-style element with from/to/faces,
    pre-transformed by world_xform. Axis-aligned input becomes a slightly-skewed
    box in general; we keep it as a thin rotation-cuboid by approximating the
    rotated AABB. (The viewer's BoxGeometry is axis-aligned but we apply the
    rotation by transforming the from/to corners then taking the new AABB plus
    a per-element rotation derived from the world transform.)

    Simplification used here: project the 8 transformed corners and emit an AABB
    in world space. That loses the bone's rotation visually but positions every
    cube correctly. Works fine for the rest pose since most rotations are <30°."""
    frm = element.get("from", [0, 0, 0])
    to = element.get("to", [0, 0, 0])
    # Per-element rotation (around element.origin) — rare in bbmodels; apply it
    # to the cube's corners before applying the bone transform.
    elem_rot = element.get("rotation", [0, 0, 0]) or [0, 0, 0]
    elem_origin = element.get("origin", [0, 0, 0]) or [0, 0, 0]
    # Generate 8 corners of the cube
    x0, y0, z0 = frm
    x1, y1, z1 = to
    corners = [
        [x0, y0, z0], [x1, y0, z0], [x0, y1, z0], [x1, y1, z0],
        [x0, y0, z1], [x1, y0, z1], [x0, y1, z1], [x1, y1, z1],
    ]
    # Apply per-element rotation around element.origin if non-zero
    if any(elem_rot):
        rx, ry, rz = elem_rot
        R = mat_mul(mat_mul(mat_rotate_z(rz), mat_rotate_y(ry)), mat_rotate_x(rx))
        ox, oy, oz = elem_origin
        for i, c in enumerate(corners):
            shifted = [c[0] - ox, c[1] - oy, c[2] - oz]
            rotated = mat_apply(R, shifted)
            corners[i] = [rotated[0] + ox, rotated[1] + oy, rotated[2] + oz]
    # Apply bone world transform
    transformed = [mat_apply(world_xform, c) for c in corners]
    # Take AABB of the transformed corners
    new_x = [c[0] for c in transformed]
    new_y = [c[1] for c in transformed]
    new_z = [c[2] for c in transformed]
    new_from = [min(new_x), min(new_y), min(new_z)]
    new_to = [max(new_x), max(new_y), max(new_z)]

    # Carry over faces with their UVs and texture refs, but we need to rewrite
    # texture refs to use bbmodel: prefix indexed by texture id.
    # Bbmodel face textures are texture-array INDICES (numeric) that the loader
    # resolves through the model's texture array.
    new_faces = {}
    for face_name, face_def in (element.get("faces") or {}).items():
        if face_def is None:
            continue
        tex_idx = face_def.get("texture")
        if tex_idx is None:
            continue
        uv = face_def.get("uv", [0, 0, 16, 16])
        new_faces[face_name] = {
            "uv": uv,
            "texture": f"#tex{tex_idx}",
        }
    if not new_faces:
        return None
    return {
        "from": new_from,
        "to": new_to,
        "faces": new_faces,
    }


# ---------- Main converter ----------

def extract_textures(bbmodel: dict, out_dir: Path, species_slug: str) -> dict[int, str]:
    """Decode embedded base64 textures, write PNGs, return idx -> texture-key map."""
    tex_map: dict[int, str] = {}
    for idx, tex in enumerate(bbmodel.get("textures", []) or []):
        src = tex.get("source")
        name = tex.get("name") or f"tex{idx}"
        clean_name = re.sub(r"[^a-z0-9_-]+", "_", name.lower()).strip("_") or f"tex{idx}"
        if not src or not src.startswith("data:"):
            continue
        # data:image/png;base64,<b64>
        comma = src.find(",")
        if comma < 0:
            continue
        b64 = src[comma + 1:]
        try:
            data = base64.b64decode(b64)
        except Exception:
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / f"{clean_name}.png"
        target.write_bytes(data)
        tex_map[idx] = f"bbmodel:{species_slug}/{clean_name}"
    return tex_map


def convert_bbmodel(src_path: Path, out_models_dir: Path, out_textures_dir: Path) -> bool:
    """Bbmodel elements already live in world-space coordinates; the outliner
    bone hierarchy is for animation, not assembly. So we just enumerate visible
    elements and rewrite their face-texture refs into our `bbmodel:` namespace."""
    species_slug = slug_from_filename(src_path)
    try:
        bbmodel = json.loads(src_path.read_text())
    except Exception as e:
        print(f"  parse fail {src_path.name}: {e}", file=sys.stderr)
        return False

    elements = bbmodel.get("elements", [])
    if not elements:
        return False

    # Extract embedded textures
    tex_dir = out_textures_dir / species_slug
    tex_map = extract_textures(bbmodel, tex_dir, species_slug)

    out_elements: list[dict] = []
    for el in elements:
        if not el.get("visibility", True):
            continue
        frm = el.get("from")
        to = el.get("to")
        if not frm or not to:
            continue
        new_faces: dict = {}
        for face_name, face_def in (el.get("faces") or {}).items():
            if face_def is None:
                continue
            tex_idx = face_def.get("texture")
            if tex_idx is None:
                continue
            new_faces[face_name] = {
                "uv": face_def.get("uv", [0, 0, 16, 16]),
                "texture": f"#tex{tex_idx}",
            }
        if not new_faces:
            continue
        entry = {
            "from": frm,
            "to": to,
            "faces": new_faces,
        }
        # Per-element rotation (around element.origin). Preserve as-is — bbmodel
        # uses [rx, ry, rz] degrees; viewer handles this format.
        rot = el.get("rotation")
        origin = el.get("origin")
        if rot and any(rot):
            entry["bbmodel_rotation"] = rot
            if origin:
                entry["bbmodel_origin"] = origin
        out_elements.append(entry)

    if not out_elements:
        return False

    out_textures: dict[str, str] = {f"tex{idx}": ref for idx, ref in tex_map.items()}
    res = bbmodel.get("resolution") or {}
    out_model = {
        "_source": "bbmodel",
        "_uv_resolution": [res.get("width", 16), res.get("height", 16)],
        "textures": out_textures,
        "elements": out_elements,
    }
    out_models_dir.mkdir(parents=True, exist_ok=True)
    target = out_models_dir / f"{species_slug}.json"
    target.write_text(json.dumps(out_model))
    return True


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--src", type=Path, default=DEFAULT_SRC)
    p.add_argument("--out-models", type=Path, default=DEFAULT_OUT_MODELS)
    p.add_argument("--out-textures", type=Path, default=DEFAULT_OUT_TEXTURES)
    args = p.parse_args()

    if not args.src.exists() or not args.src.is_dir():
        print(f"source dir not found: {args.src}", file=sys.stderr)
        return 1

    files = sorted(args.src.glob("*.bbmodel"))
    print(f"Found {len(files)} .bbmodel files in {args.src}")

    ok = 0
    failed = 0
    for f in files:
        try:
            if convert_bbmodel(f, args.out_models, args.out_textures):
                ok += 1
            else:
                failed += 1
                print(f"  skipped (empty): {f.name}", file=sys.stderr)
        except Exception as e:
            failed += 1
            print(f"  fail {f.name}: {e}", file=sys.stderr)

    print(f"Converted {ok} bbmodels, {failed} failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
