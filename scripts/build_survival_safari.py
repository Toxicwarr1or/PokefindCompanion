#!/usr/bin/env python3
"""Regenerate the Areas tables in content/pokefind/pokesurvival/safari-zone.md
from the live survival safari script.

Usage: python3 scripts/build_survival_safari.py [path/to/survival-safari.json]

Only the block between the AREAS-START / AREAS-END markers is replaced; the
prose around it is hand-written. Tiers are relative weight within one quarter's
pool: Common >= 0.10, Uncommon >= 0.04, Rare >= 0.01, Ultra-Rare below.
The Legendary row is kept even when empty so every safari page has the same shape.
"""
import json, sys, re, pathlib

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                   '/home/jack/Desktop/Survival2026/Survival Safari Zone/survival-safari.json')
PAGE = pathlib.Path(__file__).resolve().parents[1] / 'content/pokefind/pokesurvival/safari-zone.md'

QUARTER = {'1-1': 0, '1-4': 1, '1-7': 2, '1-10': 3}
QUARTER_NAMES = ['Jan–Mar', 'Apr–Jun', 'Jul–Sep', 'Oct–Dec']
TIERS = ['Common', 'Uncommon', 'Rare', 'Ultra-Rare', 'Legendary']
TITLES = {
    'Area 1 - Entrance': 'Entrance', 'Area 2 - Orange Desert/Fire': 'Orange Desert',
    'Area 3 - General': 'Central Meadow', 'Area 4 - Desert/Fire': 'Eastern Desert',
    'Area 4.5 - Desert/Water': 'Desert Oasis (water)', 'Area 5 - Jungle': 'Jungle',
    'Area 5.5 - Jungle': 'Deep Jungle', 'Water Area - North River': 'North River (water)',
    'Water Area - East Pond': 'East Pond (ice water)', 'Water Area - West Pond': 'West Pond (water)',
}
DISPLAY = {'Nidoran-M': 'Nidoran♂', 'Nidoran-F': 'Nidoran♀'}


def tier(chance):
    return 0 if chance >= 0.10 else 1 if chance >= 0.04 else 2 if chance >= 0.01 else 3


def main():
    doc = json.loads(SRC.read_text(encoding='utf-8'), object_pairs_hook=lambda p: p)
    names = [v for k, v in doc if k == 'Comment' and 'Area' in v]
    areas = [v for k, v in doc if k == 'SafariZoneArea']
    page = PAGE.read_text(encoding='utf-8')
    # keep the existing blurb under each heading
    blurbs = dict(re.findall(r'^### (.+?)\n\n(.+?)\n', page, re.M))

    out = []
    for name, area in zip(names, areas):
        grid = [[set() for _ in range(4)] for _ in TIERS]
        for entry in area[6]:
            d = dict(entry)
            req = dict(d['requirements'][0])
            q = QUARTER[req['InDateRange'][0].split('-****')[0]]
            grid[tier(d['spawn_chance'])][q].add(DISPLAY.get(d['species'], d['species']))
        title = TITLES.get(name, name)
        out.append(f"### {title}\n\n{blurbs.get(title, '*TODO: describe this area.*')}\n")
        out.append('| | ' + ' | '.join(QUARTER_NAMES) + ' |\n| --- | --- | --- | --- | --- |')
        for t, tname in enumerate(TIERS):
            cells = [', '.join(sorted(grid[t][q])) or '*(none)*' for q in range(4)]
            out.append(f'| **{tname}** | ' + ' | '.join(cells) + ' |')
        out.append('')
    block = '\n'.join(out)

    new = re.sub(r'(<!-- AREAS-START -->\n).*?(<!-- AREAS-END -->)', lambda m: m.group(1) + block + m.group(2),
                 page, flags=re.S)
    if new == page:
        sys.exit('markers not found or nothing changed')
    PAGE.write_text(new, encoding='utf-8')
    print(f'rewrote {PAGE.relative_to(PAGE.parents[3])}: {len(areas)} areas')


if __name__ == '__main__':
    main()
