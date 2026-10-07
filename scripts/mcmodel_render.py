#!/usr/bin/env python3
"""Tiny software renderer for Minecraft JSON item/block models.

Produces the inventory ("gui") view of a model the way the game draws it in a
slot: the model's `display.gui` transform is applied, then it is projected
orthographically looking down -Z with +Y up. Faces are textured with
nearest-neighbour sampling and shaded per face normal, far faces first.

Only what the Pokéfind pack needs is implemented: cuboid `elements` with
optional axis rotation, per-face `uv` + `texture` + `rotation`, `#var`
texture references, parent chains, and `display.gui`. Good enough for icons.
"""
import json, math, re
from pathlib import Path
from PIL import Image

# (TL, TR, BR, BL) corner selectors per face in texture space. x1/y1/z1 = from, 2 = to.
FACE_CORNERS = {
    'north': (('x2', 'y2', 'z1'), ('x1', 'y2', 'z1'), ('x1', 'y1', 'z1'), ('x2', 'y1', 'z1')),
    'south': (('x1', 'y2', 'z2'), ('x2', 'y2', 'z2'), ('x2', 'y1', 'z2'), ('x1', 'y1', 'z2')),
    'east':  (('x2', 'y2', 'z2'), ('x2', 'y2', 'z1'), ('x2', 'y1', 'z1'), ('x2', 'y1', 'z2')),
    'west':  (('x1', 'y2', 'z1'), ('x1', 'y2', 'z2'), ('x1', 'y1', 'z2'), ('x1', 'y1', 'z1')),
    'up':    (('x1', 'y2', 'z1'), ('x2', 'y2', 'z1'), ('x2', 'y2', 'z2'), ('x1', 'y2', 'z2')),
    'down':  (('x1', 'y1', 'z2'), ('x2', 'y1', 'z2'), ('x2', 'y1', 'z1'), ('x1', 'y1', 'z1')),
}
FACE_NORMAL = {'north': (0, 0, -1), 'south': (0, 0, 1), 'east': (1, 0, 0), 'west': (-1, 0, 0), 'up': (0, 1, 0), 'down': (0, -1, 0)}

# Two directional lights plus ambient, roughly what the game uses for GUI items.
LIGHTS = [(0.2, 1.0, -0.7), (-0.2, 1.0, 0.7)]


def _norm(v):
    l = math.sqrt(sum(c * c for c in v)) or 1
    return tuple(c / l for c in v)

LIGHTS = [_norm(l) for l in LIGHTS]


def rot_matrix(axis, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    if axis == 'x': return ((1, 0, 0), (0, c, -s), (0, s, c))
    if axis == 'y': return ((c, 0, s), (0, 1, 0), (-s, 0, c))
    return ((c, -s, 0), (s, c, 0), (0, 0, 1))


def mul(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


class ModelLoader:
    def __init__(self, *roots):
        self.roots = [Path(r) for r in roots]

    def read(self, ref):
        ref = ref.split(':', 1)[-1]
        for r in self.roots:
            p = r / 'models' / f'{ref}.json'
            if p.exists():
                try:
                    return json.loads(p.read_text(errors='replace'))
                except json.JSONDecodeError:
                    return None
        return None

    def texture(self, ref):
        ref = ref.split(':', 1)[-1]
        for r in self.roots:
            p = r / 'textures' / f'{ref}.png'
            if p.exists():
                return Image.open(p).convert('RGBA')
        return None

    def resolve(self, ref, depth=0):
        """Merge the parent chain: nearest elements win, textures/display merge child-over-parent."""
        m = self.read(ref)
        if m is None or depth > 8:
            return None
        out = {'textures': {}, 'display': {}, 'elements': None, 'parent_chain': [ref]}
        if m.get('parent'):
            parent = self.resolve(m['parent'], depth + 1)
            if parent:
                out['textures'].update(parent['textures'])
                out['display'].update(parent['display'])
                out['elements'] = parent['elements']
                out['parent_chain'] += parent['parent_chain']
        out['textures'].update(m.get('textures') or {})
        out['display'].update(m.get('display') or {})
        if m.get('elements'):
            out['elements'] = m['elements']
        return out


def resolve_tex_var(textures, name, depth=0):
    while name.startswith('#') and depth < 8:
        name = textures.get(name[1:], ''); depth += 1
    return None if not name or name.startswith('#') else name


def render(loader, model_ref, size=64, pad=0.0):
    """Return an RGBA icon for the model, or None if it has no elements."""
    m = loader.resolve(model_ref)
    if not m or not m['elements']:
        return None
    gui = m['display'].get('gui') or {}
    rot = gui.get('rotation', [0, 0, 0]); tr = gui.get('translation', [0, 0, 0]); sc = gui.get('scale', [1, 1, 1])
    R = matmul(rot_matrix('x', rot[0]), matmul(rot_matrix('y', rot[1]), rot_matrix('z', rot[2])))

    tex_cache = {}
    def get_tex(face):
        ref = resolve_tex_var(m['textures'], face.get('texture', ''))
        if ref is None: return None
        if ref not in tex_cache:
            tex_cache[ref] = loader.texture(ref)
        return tex_cache[ref]

    quads = []  # (depth, [(sx,sy)]*4, [(u,v)]*4, tex, shade)
    for el in m['elements']:
        f, t = el['from'], el['to']
        c = {'x1': f[0], 'y1': f[1], 'z1': f[2], 'x2': t[0], 'y2': t[1], 'z2': t[2]}
        er = el.get('rotation')
        ER = None
        if er:
            ER = rot_matrix(er['axis'], er['angle']); origin = er.get('origin', [8, 8, 8])
        for fname, face in (el.get('faces') or {}).items():
            tex = get_tex(face)
            if tex is None: continue
            pts = []
            for sel in FACE_CORNERS[fname]:
                p = [c[sel[0]], c[sel[1]], c[sel[2]]]
                if ER:
                    p = [a - b for a, b in zip(p, origin)]; p = mul(ER, p); p = [a + b for a, b in zip(p, origin)]
                p = [a - 8 for a in p]                      # centre the model
                p = [a * s for a, s in zip(p, sc)]          # scale
                p = mul(R, p)                               # rotate
                p = [a + b for a, b in zip(p, tr)]          # translate
                pts.append(p)
            n = FACE_NORMAL[fname]
            if ER: n = mul(ER, n)
            n = _norm(mul(R, n))
            if n[2] <= 0.0:                                 # facing away from the viewer
                continue
            shade = 0.45 + 0.55 * min(1.0, sum(max(0.0, sum(a * b for a, b in zip(n, L))) for L in LIGHTS))
            uv = face.get('uv', [0, 0, 16, 16])
            u1, v1, u2, v2 = [x * tex.width / 16 if i % 2 == 0 else x * tex.height / 16 for i, x in enumerate(uv)]
            uvs = [(u1, v1), (u2, v1), (u2, v2), (u1, v2)]
            r = face.get('rotation', 0) % 360
            for _ in range(r // 90):
                uvs = uvs[-1:] + uvs[:-1]
            depth = sum(p[2] for p in pts) / 4
            quads.append((depth, pts, uvs, tex, shade))

    quads.sort(key=lambda q: q[0])
    S = size; k = S / 16.0 * (1 - pad)
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = img.load()
    for _, pts, uvs, tex, shade in quads:
        scr = [((p[0]) * k + S / 2, (-p[1]) * k + S / 2) for p in pts]
        tpx = tex.load(); tw, th = tex.size
        _fill_quad(px, S, scr, uvs, tpx, tw, th, shade)
    return img


def _fill_quad(px, S, scr, uvs, tpx, tw, th, shade):
    """Rasterise a quad as two triangles with barycentric uv interpolation."""
    for tri in ((0, 1, 2), (0, 2, 3)):
        (x0, y0), (x1, y1), (x2, y2) = (scr[i] for i in tri)
        (u0, v0), (u1, v1), (u2, v2) = (uvs[i] for i in tri)
        minx, maxx = max(0, int(min(x0, x1, x2))), min(S - 1, int(max(x0, x1, x2)) + 1)
        miny, maxy = max(0, int(min(y0, y1, y2))), min(S - 1, int(max(y0, y1, y2)) + 1)
        det = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(det) < 1e-9: continue
        for y in range(miny, maxy + 1):
            cy = y + 0.5
            for x in range(minx, maxx + 1):
                cx = x + 0.5
                l0 = ((y1 - y2) * (cx - x2) + (x2 - x1) * (cy - y2)) / det
                l1 = ((y2 - y0) * (cx - x2) + (x0 - x2) * (cy - y2)) / det
                l2 = 1 - l0 - l1
                if l0 < -1e-6 or l1 < -1e-6 or l2 < -1e-6: continue
                u = l0 * u0 + l1 * u1 + l2 * u2; v = l0 * v0 + l1 * v1 + l2 * v2
                tu = min(tw - 1, max(0, int(u))); tv = min(th - 1, max(0, int(v)))
                r, g, b, a = tpx[tu, tv]
                if a == 0: continue
                px[x, y] = (int(r * shade), int(g * shade), int(b * shade), a)


if __name__ == '__main__':
    import sys
    loader = ModelLoader(*sys.argv[1:-2])
    out = render(loader, sys.argv[-2])
    if out is None: sys.exit('no elements')
    out.save(sys.argv[-1]); print('wrote', sys.argv[-1])
