#!/usr/bin/env python3
"""Build the PokéSurvival recipe browser assets.

Reads the recipe export and two unpacked texture trees, then writes everything the
page at /pokefind/pokesurvival/recipes/ needs into static/recipes/:

  recipes.json      the export, with an `icon` filename stamped on every item id
  icons/<slug>.png  one icon per distinct item id (native resolution, scaled by CSS)
  gui/<station>.png the in-game container panels, cropped from the vanilla textures
  MISSING.txt       ids that fell back to a stand-in icon (give these a real texture)

Usage:
  python3 scripts/build_survival_recipes.py \
      --recipes  ~/Documents/pokefind-survival-recipes/recipes.json \
      --pack     <dir holding assets/ from the Pokéfind resource pack> \
      --vanilla  <dir holding assets/ from the Minecraft client jar> \
      [--item-java <PokemonWorld Item.java>]

Item id resolution, in order:
  minecraft:X   vanilla textures/item/x.png; otherwise a block, drawn as an isometric
                cube from its block textures (top + side, or front where it has one).
  item:X        Item.java gives (material, custom_model_data) → the pack's
                items/<material>.json range_dispatch → model → layer0 texture.
                Damage-keyed items (apricorns, lids, discs, shards) resolve by name.
  mythic:X      by normalised name against the pack's survival texture folders;
                vanilla-named gear (Diamond_Sword …) uses the vanilla texture.
Anything unresolved gets a labelled stand-in and is listed in MISSING.txt.
"""
import argparse, json, os, re, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcmodel_render import ModelLoader, render as render_model

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'static' / 'recipes'

# ---------------------------------------------------------------- helpers

def norm(s):
    """CamelCase / SNAKE_CASE / spaces → lower snake."""
    s = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', s)
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')

APRICORN_CODES = {'red': 'r', 'blue': 'bu', 'black': 'bk', 'green': 'g', 'pink': 'p',
                  'white': 'w', 'yellow': 'y', 'purple': 'pur'}

def load_png(p):
    return Image.open(p).convert('RGBA')

def tint(img, rgb):
    r, g, b = rgb
    px = img.load(); w, h = img.size
    for y in range(h):
        for x in range(w):
            pr, pg, pb, pa = px[x, y]
            px[x, y] = (pr * r // 255, pg * g // 255, pb * b // 255, pa)
    return img

def iso_cube(top, left, right, size=32):
    """Draw a Minecraft-inventory-style isometric cube from three 16x16 faces.

    Output is size×size. Top face is the diamond (S/2,0)-(S,S/4)-(S/2,S/2)-(0,S/4);
    the left and right faces hang below it. Each output pixel is mapped back to
    (u,v) on its face and sampled nearest-neighbour, so pixel art stays crisp.
    """
    S = size
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    faces = {'top': (top.convert('RGBA'), 1.0), 'left': (left.convert('RGBA'), 0.8), 'right': (right.convert('RGBA'), 0.6)}
    px = {k: (v[0].load(), v[0].size, v[1]) for k, v in faces.items()}
    o = out.load()
    for y in range(S):
        for x in range(S):
            cx, cy = x + 0.5, y + 0.5
            # top: T + u*(R-T) + v*(L-T), R-T=(S/2,S/4), L-T=(-S/2,S/4)
            u = ((cx - S / 2) / (S / 2) + cy / (S / 4)) / 2
            v = (cy / (S / 4) - (cx - S / 2) / (S / 2)) / 2
            face = None
            if 0 <= u < 1 and 0 <= v < 1:
                face = 'top'
            elif cx < S / 2:
                u = cx / (S / 2); v = (cy - S / 4 - u * S / 4) / (S / 2)
                if 0 <= v < 1: face = 'left'
            else:
                u = (cx - S / 2) / (S / 2); v = (cy - S / 2 + u * S / 4) / (S / 2)
                if 0 <= u < 1 and 0 <= v < 1: face = 'right'
            if face is None:
                continue
            p, (w, h), shade = px[face]
            r, g, b, a = p[min(int(u * w), w - 1), min(int(v * h), h - 1)]
            o[x, y] = (int(r * shade), int(g * shade), int(b * shade), a)
    return out

# ---------------------------------------------------------------- resolvers

class Resolver:
    def __init__(self, pack, vanilla, item_defs):
        self.pack = Path(pack) / 'assets' / 'minecraft'
        self.van = Path(vanilla) / 'assets' / 'minecraft'
        self.item_defs = item_defs
        self.missing = []
        self.loader = ModelLoader(self.pack, self.van)
        self.apricorn_models = {f.stem.split('_', 1)[1]: f'survival/apricorns/{f.stem}' for f in (self.pack / 'models/survival/apricorns').glob('*.json')}
        # index every pack texture by basename for name lookups
        self.pack_tex = {}
        for sub in ('textures/survival/mythic/items/pokefind', 'textures/survival/items',
                    'textures/survival/apricorn', 'textures/survival/discs',
                    'textures/survival/mythic/items/weapons', 'textures/survival/mythic/items/crafting',
                    'textures/pokemon_items/evolution', 'textures/pokemon_items/medicine',
                    'textures/pokemon_items/berries', 'textures/pokemon_items/usable',
                    'textures/pokemon_items/gems'):
            d = self.pack / sub
            if d.is_dir():
                for f in sorted(d.glob('*.png')):
                    self.pack_tex.setdefault(f.stem, f)

    # -- vanilla ------------------------------------------------------------
    BLOCK_FACES = {
        # id: (top, side[, front])
        'crafting_table': ('crafting_table_top', 'crafting_table_side', 'crafting_table_front'),
        'barrel': ('barrel_top', 'barrel_side'),
        'hay_block': ('hay_block_top', 'hay_block_side'),
        'quartz_block': ('quartz_block_top', 'quartz_block_side'),
        'ochre_froglight': ('ochre_froglight_top', 'ochre_froglight_side'),
        'pearlescent_froglight': ('pearlescent_froglight_top', 'pearlescent_froglight_side'),
        'verdant_froglight': ('verdant_froglight_top', 'verdant_froglight_side'),
        'snow_block': ('snow', 'snow'),
        'oak_log': ('oak_log_top', 'oak_log'),
        'crafter': ('crafter_top', 'crafter_east', 'crafter_north'),
    }
    FLAT_BLOCKS = {'cobweb': 'cobweb', 'glass_pane': 'glass_pane_top'}
    TAGS = {'#minecraft:logs': 'oak_log', '#minecraft:wool': 'white_wool'}

    def vanilla(self, name):
        name = {'nether_quartz': 'quartz', 'compass': 'compass_16', 'tm01': 'music_disc_13'}.get(name.lower(), name.lower())
        p = self.van / 'textures' / 'item' / f'{name}.png'
        if name == 'potion':
            base = load_png(p); ov = tint(load_png(self.van / 'textures/item/potion_overlay.png'), (0x38, 0x5d, 0xc6))
            ov.alpha_composite(base); return ov
        if name.startswith('leather_') and p.exists():
            base = tint(load_png(p), (0xA0, 0x65, 0x40))
            ovp = self.van / 'textures' / 'item' / f'{name}_overlay.png'
            if ovp.exists(): base.alpha_composite(load_png(ovp))
            return base
        if p.exists():
            return load_png(p)
        if name in self.FLAT_BLOCKS:
            return load_png(self.van / 'textures/block' / f'{self.FLAT_BLOCKS[name]}.png')
        faces = self.BLOCK_FACES.get(name)
        bt = self.van / 'textures' / 'block'
        if faces is None and (bt / f'{name}.png').exists():
            faces = (name, name)
        if faces:
            top = load_png(bt / f'{faces[0]}.png'); side = load_png(bt / f'{faces[1]}.png')
            front = load_png(bt / f'{faces[2]}.png') if len(faces) > 2 else side
            return iso_cube(top, side, front)
        return None

    # -- pack ----------------------------------------------------------------
    def model_texture(self, model_path):
        """Follow a model reference to its layer0 texture png in the pack."""
        mp = self.pack / 'models' / f'{model_path}.json'
        if not mp.exists():
            return None
        try:
            m = json.loads(mp.read_text(errors='replace'))
        except json.JSONDecodeError:
            mm = re.search(r'"layer0"\s*:\s*"([^"]+)"', mp.read_text(errors='replace'))
            m = {'textures': {'layer0': mm.group(1)}} if mm else {}
        tex = (m.get('textures') or {}).get('layer0') or next(iter((m.get('textures') or {}).values()), None)
        if not tex and m.get('parent'):
            return self.model_texture(m['parent'].split(':', 1)[-1])
        if not tex:
            return None
        tex = tex.split(':', 1)[-1]
        tp = self.pack / 'textures' / f'{tex}.png'
        return tp if tp.exists() else None

    def by_cmd(self, material, cmd):
        defp = self.pack / 'items' / f'{material.lower()}.json'
        if not defp.exists():
            return None
        text = defp.read_text(errors='replace')
        # A few pack files are truncated, so scan with a regex instead of json.loads.
        for m in re.finditer(r'"threshold":(\d+),"model":\{"type":"model","model":"([^"]+)"', text):
            if int(m.group(1)) == cmd:
                return self.from_model(m.group(2))
        return None

    def from_model(self, model_path):
        """3D models are rendered in the inventory view; flat ones use their layer0 texture."""
        img = render_model(self.loader, model_path, size=64)
        if img is not None:
            return img
        tp = self.model_texture(model_path)
        return load_png(tp) if tp else None

    def apricorn(self, raw):
        m = re.match(r'(cooked_)?(\w+?)_apricorn$', norm(raw))
        if not m: return None
        key = m.group(2) + ('_cooked' if m.group(1) else '')
        return self.from_model(self.apricorn_models[key]) if key in self.apricorn_models else None

    def by_name(self, raw):
        n = norm(raw)
        cands = [n]
        m = re.match(r'(cooked_)?(\w+?)_apricorn$', n)
        if m and m.group(2) in APRICORN_CODES:
            cands.append(f'apricorn_{APRICORN_CODES[m.group(2)]}' + ('_cooked' if m.group(1) else ''))
        cands.append(n.replace('_', ''))
        for c in cands:
            if c in self.pack_tex:
                return load_png(self.pack_tex[c])
        return None

    # -- entry point ---------------------------------------------------------
    def resolve(self, item_id):
        ns, _, name = item_id.partition(':')
        img = None; note = None
        if item_id in self.TAGS:
            img = self.vanilla(self.TAGS[item_id])
        elif ns == 'minecraft':
            img = self.vanilla(name)
        elif ns == 'item':
            d = self.item_defs.get(name)
            img = self.apricorn(name)
            if img is None and d and d.get('kind') == 'cmd':
                img = self.by_cmd(d['material'], d['cmd'])
            if img is None and d and d.get('kind') == 'plain':
                img = self.vanilla(d['material'])
            if img is None and name == 'TM01':
                img = self.vanilla('tm01'); note = 'music disc stand-in (menu icon)'
            if img is None:
                img = self.by_name(name)
        elif ns == 'mythic':
            img = self.apricorn(name) or self.by_name(name)
            if img is None and re.match(r'(Diamond|Golden|Iron|Leather|Netherite|Stone|Wooden)_', name):
                img = self.vanilla(name)
            if img is None:
                # stand-ins for custom items the current pack has no texture for
                if name.endswith('Crystal'):
                    img = self.by_name(name[:-7] + '_gem'); note = 'type gem used as stand-in'
                elif name.endswith('ImbuementArmor'):
                    img = self.vanilla('enchanted_book'); note = 'enchanted book stand-in'
                elif name.endswith('Imbuement'):
                    img = self.vanilla('enchanted_book'); note = 'enchanted book stand-in'
                elif name.endswith('Template'):
                    img = self.vanilla('paper'); note = 'paper stand-in'
        if img is None and name.upper() == 'CRAFTING_TERMINAL':
            img = self.vanilla('crafter'); note = 'crafter block stand-in'
        if img is None:
            img = self.placeholder(); note = 'NO TEXTURE FOUND'
        if note:
            self.missing.append(f'{item_id}\t{note}')
        return img

    @staticmethod
    def placeholder():
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle((1, 1, 14, 14), outline=(255, 0, 255, 255))
        d.line((1, 1, 14, 14), fill=(255, 0, 255, 255)); d.line((14, 1, 1, 14), fill=(255, 0, 255, 255))
        return im

# ---------------------------------------------------------------- GUI panels

# Crops from the vanilla container textures (0,0 origin), plus the slot origins
# in that cropped image. Item icons are 16×16 drawn at each origin.
GUI = {
    'crafting_table': {'crop': (0, 0, 176, 83), 'slots': {'grid': [(30 + 18 * c, 17 + 18 * r) for r in range(3) for c in range(3)], 'out': (124, 35)}},
    'brewing_stand':  {'crop': (0, 0, 176, 83), 'slots': {'ingredient': (79, 17), 'fuel': (17, 17), 'bottles': [(56, 51), (79, 58), (102, 51)], 'bubbles': (63, 14), 'arrow': (97, 16)}},
    'furnace':        {'crop': (0, 0, 176, 83), 'slots': {'in': (56, 17), 'fuel': (56, 53), 'out': (116, 35), 'flame': (56, 36), 'arrow': (79, 34)}},
    'smoker':         {'crop': (0, 0, 176, 83), 'slots': {'in': (56, 17), 'fuel': (56, 53), 'out': (116, 35), 'flame': (56, 36), 'arrow': (79, 34)}},
    'smithing_table': {'crop': (0, 0, 176, 83), 'slots': {'template': (8, 48), 'base': (26, 48), 'addition': (44, 48), 'out': (98, 48)}},
}

def build_gui(van_dir, out_dir):
    src = Path(van_dir) / 'assets/minecraft/textures/gui'
    out_dir.mkdir(parents=True, exist_ok=True)
    for station, spec in GUI.items():
        fn = 'smithing' if station == 'smithing_table' else station
        im = load_png(src / 'container' / f'{fn}.png').crop(spec['crop'])
        im.save(out_dir / f'{station}.png')
    # progress sprites, shown "complete" so the panel looks like a finished craft
    for name, rel in {'furnace_flame': 'sprites/container/furnace/lit_progress.png',
                      'furnace_arrow': 'sprites/container/furnace/burn_progress.png',
                      'brew_arrow': 'sprites/container/brewing_stand/brew_progress.png',
                      'brew_bubbles': 'sprites/container/brewing_stand/bubbles.png'}.items():
        p = src / rel
        if p.exists():
            load_png(p).save(out_dir / f'{name}.png')
    return {k: v['slots'] for k, v in GUI.items()}

# ---------------------------------------------------------------- unlocks

# Attribute key → how the in-game /traits menu words it ('#' = the threshold).
ATTRIBUTE_LABELS = {
    'catch': 'Catch # Pokémon', 'defeat_wild': 'Defeat # wild Pokémon', 'defeat_trainer': 'Defeat # trainer NPCs',
    'defeat_player': 'Defeat # trainers in battle', 'pokedex': 'Reach # Pokédex entries', 'breeding': 'Breed # Pokémon',
    'commerce': 'Collect # coins', 'healing_power': 'Heal # HP in total', 'status_recovery': 'Cure # status effects',
}
# Keys the attributes config does not grant. None = unknown, show a generic badge.
MANUAL_UNLOCKS = {
    'CRAFTING_TERMINAL': {'label': 'Beat Gym 5', 'trait': 'Gym badges', 'progress': 5,
                          'how': 'Granted when you beat the fifth PokéSurvival gym (Delphine, Water). See the Gyms page.'},
    'RECIPE_NETHERITE': {'label': 'Nether access (beat Gym 3)', 'trait': 'Gym badges', 'progress': 3,
                         'how': 'No separate unlock — you need Netherite Ingots, and the Nether only opens once you beat the third gym (Dex, Electric/Normal).'},
}

def build_unlocks(attr_path):
    """Map each recipe unlock key (e.g. RECIPE_CATCH_25) to the trait threshold that grants it."""
    out = dict(MANUAL_UNLOCKS)
    if not os.path.exists(attr_path):
        return out
    cfg = json.load(open(attr_path))
    for attr, tiers in cfg.items():
        akey = attr.lower()
        for t in tiers:
            reward = t.get('REWARD') or {}
            cos = reward.get('GiveCosmetic')
            if not cos:
                continue
            key = re.sub(r'^survival_[a-z0-9]+_', '', cos).upper()       # survival_beta_recipe_catch_5 → RECIPE_CATCH_5
            label_fmt = ATTRIBUTE_LABELS.get(akey, akey.replace('_', ' ').capitalize() + ' #')
            out[key] = {
                'attribute': akey,
                'trait': label_fmt.replace('# ', '').replace(' #', '').strip(),
                'progress': t.get('PROGRESS'),
                'label': label_fmt.replace('#', str(t.get('PROGRESS'))),
                'reward': re.sub(r'&[0-9a-fk-or]', '', reward.get('ShowReward') or reward.get('Name') or ''),
            }
    return out

# ---------------------------------------------------------------- main

def all_ids(recipes):
    ids = set()
    def slot(s):
        if s:
            ids.update(s['accepts'])
    for r in recipes:
        if r['output'].get('id'):
            ids.add(r['output']['id'])
        for k in ('ingredient', 'bottle', 'template', 'base', 'addition', 'input'):
            if k in r: slot(r[k])
        for s in r.get('inputs', []): slot(s)
        for row in r.get('grid', []):
            for s in row: slot(s)
    return sorted(ids)

def icon_slug(item_id):
    return re.sub(r'[^a-z0-9]+', '-', item_id.lower()).strip('-')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--recipes', required=True)
    ap.add_argument('--pack', required=True)
    ap.add_argument('--vanilla', required=True)
    ap.add_argument('--attributes', default=str(HERE / 'data' / 'survival_attributes.json'),
                    help='survival attributes config (PRODUCTION/survival_attributes.json from the pokefind S3 bucket)')
    ap.add_argument('--item-defs', default=str(HERE / 'data' / 'survival_item_defs.json'),
                    help='JSON of item: id → {kind, material, cmd} parsed from Item.java')
    a = ap.parse_args()

    data = json.load(open(a.recipes))
    item_defs = json.load(open(a.item_defs)) if os.path.exists(a.item_defs) else {}
    res = Resolver(a.pack, a.vanilla, item_defs)

    icons_dir = OUT / 'icons'
    if icons_dir.exists():
        shutil.rmtree(icons_dir)
    icons_dir.mkdir(parents=True)

    icon_map = {}
    ids = all_ids(data['recipes']) + [c['icon'] for c in data['menu'] if c.get('icon')] + ['minecraft:BLAZE_POWDER', 'minecraft:COAL']
    for item_id in sorted(set(ids)):
        img = res.resolve(item_id)
        slug = icon_slug(item_id)
        img.save(icons_dir / f'{slug}.png')
        icon_map[item_id] = f'{slug}.png'

    any_tile = Image.new('RGBA', (16, 16), (0, 0, 0, 0))   # generic 'any item' tile for pattern recipes
    dr = ImageDraw.Draw(any_tile)
    for i in range(0, 16, 4):
        dr.line((i, 0, i + 1, 0), fill=(255, 255, 255, 180)); dr.line((i, 15, i + 1, 15), fill=(255, 255, 255, 180))
        dr.line((0, i, 0, i + 1), fill=(255, 255, 255, 180)); dr.line((15, i, 15, i + 1), fill=(255, 255, 255, 180))
    dr.text((5, 2), '?', fill=(255, 255, 255, 220))
    any_tile.save(icons_dir / 'any.png')
    slots = build_gui(a.vanilla, OUT / 'gui')

    export = dict(data)
    export['icons'] = icon_map
    export['gui'] = slots
    export['unlocks'] = build_unlocks(a.attributes)
    json.dump(export, open(OUT / 'recipes.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    (OUT / 'MISSING.txt').write_text('\n'.join(res.missing) + '\n')
    used = {r['unlock'] for r in data['recipes'] if r.get('unlock')}
    unknown = sorted(k for k in used if k not in export['unlocks'])
    if unknown:
        print('unlock keys with no known source:', ', '.join(unknown))
    print(f'{len(icon_map)} icons, {len(res.missing)} stand-ins (see static/recipes/MISSING.txt), '
          f'{len(data["recipes"])} recipes → {OUT}')

if __name__ == '__main__':
    main()
