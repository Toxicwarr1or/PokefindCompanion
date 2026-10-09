#!/usr/bin/env python3
"""Write a `survival_locations:` list onto every Pokédex page's first form.

Mirrors the PokéWorld `locations:` entries (see build_pokedex_extras.py) but for
PokéSurvival, where there are no towns — only biomes. One entry per typing pool
the species spawns in, naming the two biomes where that pool is rolled most
often, plus the sheet's trainer-level and Pokémon-level gates:

    Water: Ocean, Warm River — trainer Lv 13+; Pokémon Lv 16+
    Safari Zone: Jungle — Jan–Jun

Sources
  --java    SurvivalSpawnManager.java  (biome → pool weights; baked into
            scripts/data/survival_biomes.json so later runs work without it)
  --sheet   spawn_rates_5.csv          (species → pool rate + gates; survival
            loads the gen-5 sheet from S3: minecraft/data/spawn_rates_5.xls)
  --safari  survival-safari.json       (quarterly Safari Zone pools)

Re-runs are idempotent: the existing survival_locations line is replaced.
Usage: python3 scripts/build_survival_locations.py [--java …] [--sheet …] [--safari …]
"""
import argparse, csv, json, os, re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEX_DIR = ROOT / 'content' / 'pokedex'
BIOMES_JSON = HERE / 'data' / 'survival_biomes.json'

POOL_LABEL = {'GRASS_BUG': 'Grass/Bug', 'GROUND_ROCK': 'Ground/Rock', 'CAVE': 'Cave', 'GLOBAL': 'Global pool'}
TYPE_TO_POOL = {'Grass': 'GRASS_BUG', 'Bug': 'GRASS_BUG', 'Ground': 'GROUND_ROCK', 'Rock': 'GROUND_ROCK',
                'Water': 'WATER', 'Fire': 'FIRE', 'Ice': 'ICE', 'Electric': 'ELECTRIC', 'Fighting': 'FIGHTING',
                'Flying': 'FLYING', 'Ghost': 'GHOST', 'Poison': 'POISON', 'Psychic': 'PSYCHIC', 'Steel': 'STEEL',
                'Dragon': 'DRAGON', 'Normal': 'NORMAL'}
NETHER_VANILLA = {'nether_wastes', 'basalt_deltas', 'soul_sand_valley', 'warped_forest', 'crimson_forest'}
SAFARI_TITLES = {
    'Area 1 - Entrance': 'Entrance', 'Area 2 - Orange Desert/Fire': 'Orange Desert', 'Area 3 - General': 'Central Meadow',
    'Area 4 - Desert/Fire': 'Eastern Desert', 'Area 4.5 - Desert/Water': 'Desert Oasis', 'Area 5 - Jungle': 'Jungle',
    'Area 5.5 - Jungle': 'Deep Jungle', 'Water Area - North River': 'North River', 'Water Area - East Pond': 'East Pond',
    'Water Area - West Pond': 'West Pond',
}
QUARTER = {'1-1': 0, '1-4': 1, '1-7': 2, '1-10': 3}
MONTHS = ['Jan', 'Apr', 'Jul', 'Oct']; MONTH_END = ['Mar', 'Jun', 'Sep', 'Dec']
BIOMES_PER_POOL = 2


# ---------------------------------------------------------------- sources

def load_biomes(java_path):
    """biome id → {POOL: weight}. A later registerBiome for the same biome replaces the earlier one."""
    if java_path and os.path.exists(java_path):
        src = open(java_path, encoding='utf-8').read()
        table = {}
        for m in re.finditer(r'registerBiome\("([^"]+)"((?:,\s*Territory\.\w+,\s*[\d.]+)+)\)', src):
            agg = defaultdict(float)
            for t, w in re.findall(r'Territory\.(\w+),\s*([\d.]+)', m.group(2)):
                agg[t] += float(w)
            table[m.group(1)] = dict(agg)
        BIOMES_JSON.parent.mkdir(exist_ok=True)
        json.dump(table, open(BIOMES_JSON, 'w'), indent=1, sort_keys=True)
        return table
    return json.load(open(BIOMES_JSON))


def load_sheet(csv_path):
    """dex number (int) → [{pool, rate, tl, min, max}] with a positive rate."""
    out = defaultdict(list)
    dex = None
    for r in csv.reader(open(csv_path, encoding='utf-8', errors='replace')):
        r = (r + [''] * 8)[:8]
        if r[0].strip():
            try: dex = int(r[0])
            except ValueError: dex = None
        if dex is None or not r[3].strip():
            continue
        pool = r[2].strip().upper().replace('-', '_')
        out[dex].append({'pool': pool, 'rate': float(r[3]), 'tl': r[5].strip(), 'min': r[6].strip(), 'max': r[7].strip()})
    return out


def load_safari(path):
    """species (lower) → {area title: set(quarter index)}"""
    out = defaultdict(lambda: defaultdict(set))
    if not path or not os.path.exists(path):
        return out
    doc = json.loads(open(path, encoding='utf-8').read(), object_pairs_hook=lambda p: p)
    names = [v for k, v in doc if k == 'Comment' and 'Area' in v]
    areas = [v for k, v in doc if k == 'SafariZoneArea']
    for name, area in zip(names, areas):
        title = SAFARI_TITLES.get(name, name)
        for e in area[6]:
            d = dict(e)
            q = None
            for req in d.get('requirements') or []:
                rd = dict(req)
                if 'InDateRange' in rd:
                    q = QUARTER.get(rd['InDateRange'][0].split('-****')[0])
            sp = d['species'].lower().replace('-m', '♂').replace('-f', '♀') if d['species'].lower().startswith('nidoran') else d['species'].lower()
            out[sp][title].add(q if q is not None else -1)
    return out


# ---------------------------------------------------------------- formatting

def biome_display(biome):
    ns, _, name = biome.partition(':')
    name = name.split('/')[-1]
    label = ' '.join(w.capitalize() for w in name.split('_'))
    if ns == 'incendium' or (ns == 'minecraft' and name in NETHER_VANILLA):
        label += ' (Nether)'
    elif ns == 'nullscape' or (ns == 'minecraft' and (name.startswith('end_') or name in ('small_end_islands', 'the_end'))):
        label += ' (End)'
    return label


def best_biomes(table, pool, n=BIOMES_PER_POOL):
    """Biomes where this pool is rolled most often; vanilla names win ties for recognisability."""
    scored = []
    for biome, weights in table.items():
        total = sum(weights.values()) or 1
        share = weights.get(pool, 0) / total
        if share > 0:
            scored.append((-share, 0 if biome.startswith('minecraft:') else 1, biome))
    scored.sort()
    return [biome_display(b) for _, _, b in scored[:n]]


def gates(row):
    parts = []
    if row['tl'] and float(row['tl']) > 0:
        parts.append(f"trainer Lv {int(float(row['tl']))}+")
    if row['min'] and float(row['min']) > 0:
        lo = int(float(row['min'])); hi = int(float(row['max'])) if row['max'] and float(row['max']) > 0 else None
        parts.append(f"Pokémon Lv {lo}–{hi}" if hi else f"Pokémon Lv {lo}+")
    return '; '.join(parts)


def quarters_label(qs):
    qs = sorted(q for q in qs if q >= 0)
    if not qs: return 'all year'
    if len(qs) == 4: return 'all year'
    runs, start, prev = [], qs[0], qs[0]
    for q in qs[1:]:
        if q == prev + 1: prev = q; continue
        runs.append((start, prev)); start = prev = q
    runs.append((start, prev))
    return ', '.join(f"{MONTHS[a]}–{MONTH_END[b]}" for a, b in runs)


def entries_for(dex, types, title, sheet, table, safari):
    rows = sheet.get(dex, [])
    wanted = {TYPE_TO_POOL.get(t) for t in types}
    rows = sorted(rows, key=lambda r: (0 if r['pool'] in wanted else 1, -r['rate']))
    out = []
    for r in rows:
        pool = r['pool']
        label = POOL_LABEL.get(pool, pool.capitalize())
        if pool == 'GLOBAL':
            # Only unlisted biomes roll Global, and on survival that is just deep cold
            # ocean, crimson forest and the End island — not worth listing (user, 2026-10-08).
            continue
        where = ', '.join(best_biomes(table, pool))
        if not where:          # e.g. the Cave pool: no survival biome rolls it, so it never spawns
            continue
        g = gates(r)
        out.append(f"{label}: {where}" + (f" — {g}" if g else ''))
    for area, qs in sorted(safari.get(title.lower(), {}).items()):
        out.append(f"Safari Zone: {area} — {quarters_label(qs)}")
    return out


# ---------------------------------------------------------------- page rewrite

def yaml_list(items):
    return '[' + ', '.join("'" + i.replace("'", "''") + "'" for i in items) + ']'


def update_page(path, sheet, table, safari):
    text = open(path, encoding='utf-8').read()
    m = re.search(r"^dex_number: '(\d+)'", text, re.M)
    t = re.search(r"^title: '(.*)'", text, re.M)
    if not m:
        return False
    dex = int(m.group(1)); title = t.group(1).replace("''", "'") if t else ''
    # first form block: from "  - name:" to the next "  - name:" or the end of frontmatter
    fm_end = text.index('\n---', 4)
    fm = text[:fm_end]
    forms = [mm.start() for mm in re.finditer(r'^  - name: ', fm, re.M)]
    if not forms:
        return False
    f0_start = forms[0]
    # the block ends at the next form, or at the next top-level key (single-form pages)
    nxt = re.search(r'^\S', fm[f0_start + 1:], re.M)
    f0_end = min(forms[1] if len(forms) > 1 else fm_end, f0_start + 1 + nxt.start() if nxt else fm_end)
    block = fm[f0_start:f0_end]
    types = re.search(r"^    types: \[(.*)\]", block, re.M)
    types = [x.strip().strip("'") for x in types.group(1).split(',')] if types else []
    entries = entries_for(dex, types, title, sheet, table, safari)
    block = re.sub(r"^    survival_locations: .*\n", '', block, flags=re.M)
    if entries:
        line = f"    survival_locations: {yaml_list(entries)}\n"
        if not block.endswith('\n'): block += '\n'
        block += line
    new = fm[:f0_start] + block + fm[f0_end:] + text[fm_end:]
    if new != text:
        open(path, 'w', encoding='utf-8').write(new)
    return bool(entries)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--java', default=os.path.expanduser('~/Downloads/PokemonWorld/PokemonWorld/pokemon-world/src/main/java/co/pokefind/pokemon/survival/SurvivalSpawnManager.java'))
    ap.add_argument('--sheet', default=os.path.expanduser('~/ClaudeProjects/SurvivalSpawns/spawn_rates_5.csv'))
    ap.add_argument('--safari', default=os.path.expanduser('~/Desktop/Survival2026/Survival Safari Zone/survival-safari.json'))
    a = ap.parse_args()
    table = load_biomes(a.java); sheet = load_sheet(a.sheet); safari = load_safari(a.safari)
    done = total = 0
    for p in sorted(DEX_DIR.glob('*.md')):
        if p.name == '_index.md': continue
        total += 1
        if update_page(p, sheet, table, safari): done += 1
    print(f'{done}/{total} Pokédex pages have survival spawns; biome table {len(table)} biomes; sheet {len(sheet)} species')


if __name__ == '__main__':
    main()
