#!/usr/bin/env python3
"""
Software renderer for Minecraft block-model JSON files.

Used to generate icon PNGs for Pokemon skin variants whose flat icons aren't
present in the resource pack but whose 3D model + textures are. Reads model
JSON from `assets/minecraft/models/pokemon_skins/<skin>/<id>_<species>.json`
and texture PNGs from `assets/minecraft/textures/pokemon_skins/<skin>/<species>/`.

Output is a 64x64 PNG using the model's `display.gui` transform — the same
transform Minecraft uses to render inventory icons — so output should match
what the game would show in the Pokebox screen.

Requires: numpy + Pillow.

Usage:
    python3 scripts/render_models.py --pack PATH --skin regular --species pikachu
    python3 scripts/render_models.py --batch --out static/images/pokedex/
"""

from __future__ import annotations

import argparse
import io
import json
import math
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PACK = Path("/home/jack/.minecraft/resourcepacks/devhelditem.zip")
DEFAULT_OUT = ROOT / "static/images/pokedex"
ICON_SIZE = 64           # output width/height in pixels
SUPERSAMPLE = 2          # render at NxN, downsample for antialiased edges
WORK_SIZE = ICON_SIZE * SUPERSAMPLE


# ---------- Texture loader ----------

class TextureBundle:
    """Loads texture PNGs referenced by a Minecraft model JSON."""

    def __init__(self, zf: zipfile.ZipFile, refs: dict[str, str]):
        self.images: dict[str, np.ndarray] = {}
        for name, ref in refs.items():
            # ref is like "pokemon_skins/regular/pikachu/pikachu"
            path = f"assets/minecraft/textures/{ref}.png"
            if path not in zf.namelist():
                continue
            with zf.open(path) as f:
                img = Image.open(io.BytesIO(f.read())).convert("RGBA")
            arr = np.array(img, dtype=np.uint8)
            self.images[name] = arr

    def sample(self, tex_name: str, u: float, v: float) -> tuple[int, int, int, int]:
        """Nearest-neighbor sample at uv coords (in 0..16 model space — Minecraft
        UVs are scaled to texture pixel size)."""
        key = tex_name.lstrip("#")
        arr = self.images.get(key)
        if arr is None:
            arr = self.images.get("texture")
        if arr is None:
            arr = self.images.get("0")
        if arr is None:
            return (0, 0, 0, 0)
        h, w = arr.shape[:2]
        # Minecraft UVs are in 0..16 of the texture's pixel size; convert to pixel coords
        # The texture's logical size matches its actual pixel size for these models.
        px = int(u / 16.0 * w) % w
        py = int(v / 16.0 * h) % h
        return tuple(arr[py, px])


# ---------- Geometry / transforms ----------

def rotation_matrix(axis: str, angle_deg: float) -> np.ndarray:
    """3x3 rotation matrix for a rotation around X, Y, or Z by angle_deg degrees."""
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=np.float64)
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=np.float64)
    if axis == "z":
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=np.float64)
    raise ValueError(f"bad axis: {axis}")


def cuboid_corners(frm: np.ndarray, to: np.ndarray) -> np.ndarray:
    """8 corners of an axis-aligned box, indexed by (z=0/1, y=0/1, x=0/1)."""
    x0, y0, z0 = frm
    x1, y1, z1 = to
    return np.array([
        [x0, y0, z0], [x1, y0, z0], [x0, y1, z0], [x1, y1, z0],
        [x0, y0, z1], [x1, y0, z1], [x0, y1, z1], [x1, y1, z1],
    ], dtype=np.float64)


# Face definitions: (face_name, vertex_indices_into_cuboid_corners, default_uv_axis_pair)
# Vertex order is CCW when looking from outside the box.
FACE_VERTICES = {
    "down":  [0, 1, 5, 4],   # y = y0
    "up":    [2, 6, 7, 3],   # y = y1
    "north": [0, 2, 3, 1],   # z = z0
    "south": [4, 5, 7, 6],   # z = z1
    "west":  [0, 4, 6, 2],   # x = x0
    "east":  [1, 3, 7, 5],   # x = x1
}


def build_geometry(elements: list[dict]) -> list[dict]:
    """Convert model elements into a flat list of triangle records.
    Each record: {verts:(3, V3), uvs:(3, V2), texture:str, normal_y:float (for shading)}.
    """
    triangles: list[dict] = []
    for el in elements:
        frm = np.array(el["from"], dtype=np.float64)
        to = np.array(el["to"], dtype=np.float64)
        corners = cuboid_corners(frm, to)

        # Apply per-element rotation if present
        if "rotation" in el:
            rot = el["rotation"]
            origin = np.array(rot.get("origin", [8, 8, 8]), dtype=np.float64)
            R = rotation_matrix(rot["axis"], rot["angle"])
            corners = ((corners - origin) @ R.T) + origin

        for face_name, face_def in el.get("faces", {}).items():
            idxs = FACE_VERTICES[face_name]
            quad = corners[idxs]  # 4 verts in 3D
            uv = face_def.get("uv", [0, 0, 16, 16])
            u0, v0, u1, v1 = uv
            # Quad UVs are always [u0,v0]-[u1,v0]-[u1,v1]-[u0,v1] in Minecraft
            quad_uvs = np.array([
                [u0, v0], [u0, v1], [u1, v1], [u1, v0],
            ], dtype=np.float64)
            tex = face_def.get("texture", "#texture")
            # Two triangles per quad
            for tri_idx in [(0, 1, 2), (0, 2, 3)]:
                triangles.append({
                    "verts": quad[list(tri_idx)],
                    "uvs": quad_uvs[list(tri_idx)],
                    "texture": tex,
                    "face": face_name,
                })
    return triangles


def apply_gui_transform(triangles: list[dict], display: dict) -> list[dict]:
    """Apply the model's display.gui transform: rotate, translate, scale."""
    gui = display.get("gui", {}) if isinstance(display, dict) else {}
    rotation = gui.get("rotation", [30, -50, 0])
    translation = gui.get("translation", [0, 0, 0])
    scale = gui.get("scale", [1, 1, 1])

    Rx = rotation_matrix("x", rotation[0])
    Ry = rotation_matrix("y", rotation[1])
    Rz = rotation_matrix("z", rotation[2])
    R = Rz @ Ry @ Rx
    S = np.diag(scale).astype(np.float64)
    T = np.array(translation, dtype=np.float64)

    out = []
    for tri in triangles:
        # Center the model on (8, 8, 8) — Minecraft's block-space center
        verts = tri["verts"] - np.array([8, 8, 8], dtype=np.float64)
        verts = verts @ R.T @ S + T
        out.append({**tri, "verts": verts})
    return out


# ---------- Rasterizer ----------

def rasterize(triangles: list[dict], textures: TextureBundle, size: int) -> np.ndarray:
    """Software rasterize triangles into an RGBA image (numpy uint8 HxWx4)."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    zbuf = np.full((size, size), -1e9, dtype=np.float64)

    # Compute world-to-screen scale: model-space coords are roughly -8..+8 after
    # GUI transform. Map that range to (0, size) with a margin.
    # Actually after centering and the standard GUI scale (~0.6), values typically
    # fall in -10..+10. Use a generous mapping.
    half = size / 2.0
    world_to_screen = (size - 4) / 22.0  # leaves a 2-px margin

    for tri in triangles:
        v = tri["verts"]
        uv = tri["uvs"]
        # Project to screen: x screen = world.x * scale + half, y screen = -world.y * scale + half
        sx = v[:, 0] * world_to_screen + half
        sy = -v[:, 1] * world_to_screen + half
        sz = v[:, 2]  # depth, larger = farther back (in Minecraft's left-handed system after rotation)

        # Backface cull: if triangle is wound CW in screen space after the CCW model
        # convention, it's facing away. Cross product z component sign tells us.
        # We DON'T cull here because some interior model parts depend on both sides.

        # Triangle bounding box (clamped to image)
        min_x = max(0, int(math.floor(min(sx))))
        max_x = min(size - 1, int(math.ceil(max(sx))))
        min_y = max(0, int(math.floor(min(sy))))
        max_y = min(size - 1, int(math.ceil(max(sy))))
        if max_x < min_x or max_y < min_y:
            continue

        # Edge function for barycentric coords
        x0, y0 = sx[0], sy[0]
        x1, y1 = sx[1], sy[1]
        x2, y2 = sx[2], sy[2]
        denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(denom) < 1e-9:
            continue

        # Vectorize over the bounding box
        ys, xs = np.mgrid[min_y:max_y + 1, min_x:max_x + 1]
        ys_f = ys + 0.5
        xs_f = xs + 0.5

        w0 = ((y1 - y2) * (xs_f - x2) + (x2 - x1) * (ys_f - y2)) / denom
        w1 = ((y2 - y0) * (xs_f - x2) + (x0 - x2) * (ys_f - y2)) / denom
        w2 = 1 - w0 - w1

        mask = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not mask.any():
            continue

        # Interpolate Z and UV
        z = w0 * sz[0] + w1 * sz[1] + w2 * sz[2]
        u = w0 * uv[0, 0] + w1 * uv[1, 0] + w2 * uv[2, 0]
        v_uv = w0 * uv[0, 1] + w1 * uv[1, 1] + w2 * uv[2, 1]

        # Sample texture per pixel inside the mask
        ys_in, xs_in = ys[mask], xs[mask]
        z_in = z[mask]
        u_in = u[mask]
        v_in = v_uv[mask]

        tex_key = tri["texture"].lstrip("#")
        arr = textures.images.get(tex_key)
        if arr is None:
            arr = textures.images.get("texture")
        if arr is None:
            arr = textures.images.get("0")
        if arr is None:
            continue
        h, w = arr.shape[:2]
        # Minecraft UVs are 0..16 in model space; map to texture pixel space
        px = (u_in / 16.0 * w).astype(np.int32) % w
        py = (v_in / 16.0 * h).astype(np.int32) % h
        colors = arr[py, px]   # (N, 4) RGBA

        # Z-buffer test (smaller z = closer to camera in our orthographic projection)
        # Actually after our transform, larger z = closer (camera looks down -Z), but
        # since GUI rotation reorients, just use "larger z wins" if it gave better
        # results in testing. Here we use larger-z-wins (closer to camera).
        for i in range(len(z_in)):
            yy, xx = int(ys_in[i]), int(xs_in[i])
            if z_in[i] > zbuf[yy, xx] and colors[i, 3] > 0:
                zbuf[yy, xx] = z_in[i]
                img[yy, xx] = colors[i]

    return img


# ---------- Renderer entry point ----------

def render_model(zf: zipfile.ZipFile, model_path: str, out_path: Path) -> bool:
    """Render the model at zf://model_path to out_path. Returns True on success."""
    if model_path not in zf.namelist():
        return False
    with zf.open(model_path) as f:
        model = json.load(f)
    elements = model.get("elements", [])
    if not elements:
        return False
    refs = model.get("textures", {})
    textures = TextureBundle(zf, refs)
    if not textures.images:
        return False
    triangles = build_geometry(elements)
    triangles = apply_gui_transform(triangles, model.get("display", {}))
    img_arr = rasterize(triangles, textures, WORK_SIZE)
    img = Image.fromarray(img_arr, "RGBA")
    if SUPERSAMPLE > 1:
        img = img.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return True


# ---------- CLI ----------

def find_model_path(zf: zipfile.ZipFile, skin: str, species_id: int, species_name: str) -> str | None:
    """Find the model JSON for a given (skin, species) pair. Slug variants tried."""
    candidates = [
        re.sub(r"[^a-z0-9]+", "", species_name.lower()),
        re.sub(r"[^a-z0-9]+", "_", species_name.lower()).strip("_"),
    ]
    for slug in candidates:
        path = f"assets/minecraft/models/pokemon_skins/{skin}/{species_id}_{slug}.json"
        if path in zf.namelist():
            return path
    return None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--skin", default="regular")
    p.add_argument("--species", help="Species name (e.g., pikachu)")
    p.add_argument("--id", type=int, help="National-dex id (required with --species)")
    p.add_argument("--single", help="Render a single explicit model path inside the pack zip")
    args = p.parse_args()

    if not args.pack.exists():
        print(f"pack not found: {args.pack}", file=sys.stderr)
        return 1

    with zipfile.ZipFile(args.pack) as zf:
        if args.single:
            out = args.out / "render-single.png"
            ok = render_model(zf, args.single, out)
            print(f"{'OK' if ok else 'FAIL'}  {args.single} -> {out}")
            return 0 if ok else 1

        if args.species and args.id is not None:
            path = find_model_path(zf, args.skin, args.id, args.species)
            if not path:
                print(f"no model file found for {args.skin}/{args.id}_{args.species}", file=sys.stderr)
                return 1
            slug = re.sub(r"[^a-z0-9]+", "-", args.species.lower()).strip("-")
            out = args.out / (f"{slug}.png" if args.skin == "regular" else f"{slug}-{args.skin}.png")
            ok = render_model(zf, path, out)
            print(f"{'OK' if ok else 'FAIL'}  {path} -> {out}")
            return 0 if ok else 1

        print("specify --species + --id, or --single PATH", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
