#!/usr/bin/env python3
"""
Compute auxiliary Pokedex data:
  1. Spawn-region → towns map, derived from gen5 spawn rates spreadsheet
     and the prod-map.yml region geometry. For each species, returns the
     list of towns whose bbox overlaps any of the spawn regions where that
     species spawns.
  2. Competitive movesets per species, sourced from pkmn.cc smogon set data
     (gen 6 and gen 8 — combined, deduped, capped at 2 sets per species).

This module is imported by ingest_pokedex.py; running it standalone prints
diagnostics on its own data to stdout.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPAWN_CSV = Path("/tmp/spawn_rates_5.csv")
MAP_YML = Path("/home/jack/Downloads/prod-map.yml")
ANNI_SAFARI = Path("/home/jack/Downloads/annisafari.json")
SMOGON_GEN6 = Path(__file__).resolve().parent / "gen6.json"
SMOGON_GEN8 = Path(__file__).resolve().parent / "gen8.json"


def parse_safari_anniversary_spawns(path: Path) -> set[str]:
    """Return the set of full anniversary species names (e.g., 'Kyoto Blastoise',
    'Zeinova Bouffalant') that the anniversary safari script can spawn.
    The file is JSON-with-duplicate-keys so we can't just json.load it cleanly —
    regex over the source instead."""
    if not path.exists():
        return set()
    text = path.read_text()
    out: set[str] = set()
    # Look for object literals that have BOTH species and skin: "Shiny Anniversary"
    # (the markers for anniversary-form safari spawns)
    pattern = re.compile(
        r'\{[^{}]*?"species"\s*:\s*"([^"]+)"[^{}]*?"skin"\s*:\s*"Shiny Anniversary"[^{}]*?\}',
        re.DOTALL,
    )
    for m in pattern.finditer(text):
        out.add(m.group(1).strip())
    return out


# ---------- prod-map.yml parsing ----------

_BBOX_RE = re.compile(r"^\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*:\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*$")
_AREA_KEY_RE = re.compile(r"^&[0-9a-f]&l(.+)$", re.IGNORECASE)


def parse_map_yml(path: Path) -> dict[str, dict]:
    """Returns {region_name: {bbox: (x1,y1,z1,x2,y2,z2), display: str}}."""
    out: dict[str, dict] = {}
    in_regions = False
    text = path.read_text()
    for line in text.splitlines():
        if not in_regions:
            if line.startswith("regions:"):
                in_regions = True
            continue
        # End of regions block at next top-level key
        if line and not line.startswith(" "):
            break
        m_kv = re.match(r"^\s+([^:]+):\s*(.+)$", line)
        if not m_kv:
            continue
        key = m_kv.group(1).strip()
        val = m_kv.group(2).strip()
        m = _BBOX_RE.match(val)
        if not m:
            continue
        x1, y1, z1, x2, y2, z2 = map(int, m.groups())
        bbox = (min(x1, x2), min(y1, y2), min(z1, z2),
                max(x1, x2), max(y1, y2), max(z1, z2))
        # Pretty display name: strip Minecraft color codes from area_ keys
        display = key
        if key.startswith("area_"):
            inner = key[len("area_"):]
            mm = _AREA_KEY_RE.match(inner)
            if mm:
                display = mm.group(1).replace("_", " ")
            else:
                display = inner.replace("_", " ")
        out[key] = {"bbox": bbox, "display": display}
    return out


def boxes_overlap(a, b) -> bool:
    return (a[0] <= b[3] and a[3] >= b[0]
            and a[1] <= b[4] and a[4] >= b[1]
            and a[2] <= b[5] and a[5] >= b[2])


# ---------- Spawn rates spreadsheet parsing ----------

# Map spreadsheet region label -> yml region prefix
SPAWN_REGION_TO_YML_PREFIX = {
    "Grass-Bug":   "grass_bug",
    "Ground-Rock": "ground_rock",
    "Dragon":      "dragon",
    "Electric":    "electric",
    "Fighting":    "fighting",
    "Fire":        "fire",
    "Flying":      "flying",
    "Ghost":       "ghost",
    "Ice":         "ice",
    "Normal":      "normal",
    "Poison":      "poison",
    "Psychic":     "psychic",
    "Steel":       "steel",
    "Water":       "water",
    # "Cave" doesn't map to a typed yml region — skip it (handled separately as
    # a generic location label).
}


def parse_spawn_rates(csv_path: Path) -> dict[str, dict]:
    """Returns {species_name: {region_label: rate, ...}}.
    Skips 'Global' (catch-all rate). Only includes regions with a non-empty
    spawn rate."""
    species_spawns: dict[str, dict[str, float]] = {}
    current_species: str | None = None
    with csv_path.open() as f:
        reader = csv.reader(f)
        next(reader, None)  # header
        for row in reader:
            # row: [id, name, region, rate, ...]
            if not row:
                continue
            row = (row + [""] * 8)[:8]
            id_col, name_col, region_col, rate_col = row[0], row[1], row[2], row[3]
            if name_col:  # new species row
                current_species = name_col.strip()
                species_spawns.setdefault(current_species, {})
                if region_col == "Global":
                    continue
            if not current_species or not region_col or region_col == "Global":
                continue
            region = region_col.strip()
            try:
                rate = float(rate_col) if rate_col else 0.0
            except ValueError:
                rate = 0.0
            if rate > 0:
                species_spawns.setdefault(current_species, {})[region] = rate
    return species_spawns


# ---------- Spawn region -> towns mapping ----------

def build_region_to_towns(map_data: dict[str, dict]) -> dict[str, list[str]]:
    """For each typed spawn region (grass_bug_1, electric_1, etc.) return the
    pretty names of towns (area_*) that overlap its bbox."""
    towns = {k: v for k, v in map_data.items() if k.startswith("area_") and "world" not in k and "minimap" not in k}
    spawn_regions = {k: v for k, v in map_data.items()
                     if not k.startswith(("area_", "nospawn_", "world", "minimap", "tmp"))}

    region_towns: dict[str, list[str]] = {}
    for sr_key, sr in spawn_regions.items():
        towns_in: list[str] = []
        for t_key, t in towns.items():
            if boxes_overlap(sr["bbox"], t["bbox"]):
                towns_in.append(t["display"])
        region_towns[sr_key] = sorted(set(towns_in))
    return region_towns


def species_locations(species_name: str,
                      species_spawns: dict[str, dict[str, float]],
                      region_to_towns: dict[str, list[str]]) -> list[str]:
    """Return alphabetized list of distinct towns where this species spawns."""
    spawns = species_spawns.get(species_name)
    if not spawns:
        return []
    towns: set[str] = set()
    for region_label in spawns.keys():
        if region_label == "Cave":
            towns.add("Caves")
            continue
        prefix = SPAWN_REGION_TO_YML_PREFIX.get(region_label)
        if not prefix:
            continue
        for sr_key, sr_towns in region_to_towns.items():
            if sr_key == prefix or sr_key.startswith(prefix + "_"):
                towns.update(sr_towns)
    return sorted(towns)


# ---------- Smogon competitive sets ----------

def _is_mega_set(s: dict) -> bool:
    """Pokefind doesn't support Mega Evolution. Drop sets that require it."""
    name = (s.get("name") or "").lower()
    if "mega " in name or name.startswith("mega") or " mega" in name:
        return True
    items = s.get("item") or ""
    items = items if isinstance(items, list) else [items]
    for it in items:
        if it and ("ite" in it.lower() and any(suf in it.lower() for suf in ("nite", "ite y", "ite x"))):
            return True
        if it and "mega" in it.lower():
            return True
    return False


def load_smogon_sets() -> dict[str, list[dict]]:
    """Combine gen6 + gen8 sets into {species_name: [set, set, ...]}, deduped,
    Mega-filtered, keyed by species name as Smogon spells it."""
    out: dict[str, list[dict]] = {}
    for path in (SMOGON_GEN6, SMOGON_GEN8):
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        for species_name, tier_blob in data.items():
            for tier, sets in tier_blob.items():
                for set_name, payload in sets.items():
                    entry = {"name": set_name, "tier": tier.upper(), **payload}
                    if _is_mega_set(entry):
                        continue
                    out.setdefault(species_name, []).append(entry)
    deduped: dict[str, list[dict]] = {}
    for species, sets in out.items():
        seen: set[tuple] = set()
        kept = []
        for s in sets:
            key = (s.get("name"), tuple(_flatten_moves(s.get("moves") or [])))
            if key in seen:
                continue
            seen.add(key)
            kept.append(s)
        deduped[species] = kept[:2]
    return deduped


def _flatten_moves(moves: list) -> list[str]:
    """Smogon's move slots can be a single string or a list of alternatives.
    For dedup keying, take the first option of each slot."""
    out = []
    for m in moves:
        if isinstance(m, list):
            out.append(m[0] if m else "")
        else:
            out.append(m)
    return out


def fallback_set(species_name: str, level_moves: list[dict],
                 base_stats: dict | None) -> dict | None:
    """Generate a basic build for species lacking a Smogon set. Picks four
    high-power moves from the species' level-up pool, prefers physical or
    special based on base stats. Returns a single set dict."""
    if not level_moves:
        return None

    def power_of(m: dict) -> float:
        try:
            return float(m.get("power") or 0)
        except ValueError:
            return 0.0

    # Decide attacking direction
    atk = (base_stats or {}).get("atk", 0)
    spa = (base_stats or {}).get("spa", 0)
    prefer = "Physical" if atk >= spa else "Special"

    scored = []
    for m in level_moves:
        cat = m.get("category", "")
        score = power_of(m)
        if cat == prefer:
            score *= 1.2
        if cat == "Status":
            score = max(score, 5)   # keep some utility above zero
        scored.append((score, m))
    scored.sort(key=lambda t: t[0], reverse=True)
    top4 = [m for _, m in scored[:4]]
    if not top4:
        return None
    return {
        "name": "Auto-built (no Smogon set)",
        "tier": "—",
        "moves": [m.get("move") for m in top4],
        "ability": "",
        "item": "",
        "nature": "",
        "evs": {},
        "auto": True,
    }


# ---------- CLI for spot-checking ----------

if __name__ == "__main__":
    map_data = parse_map_yml(MAP_YML)
    region_to_towns = build_region_to_towns(map_data)
    spawns = parse_spawn_rates(SPAWN_CSV)
    smogon = load_smogon_sets()

    print(f"Map regions parsed: {len(map_data)}")
    print(f"Spawn regions with town overlaps: {sum(1 for v in region_to_towns.values() if v)}")
    print(f"Species in spawn data: {len(spawns)}")
    print(f"Species with smogon sets: {len(smogon)}")
    print()
    for name in ("Bulbasaur", "Charizard", "Weedle", "Pikachu", "Dragonite"):
        towns = species_locations(name, spawns, region_to_towns)
        sets = smogon.get(name, [])
        print(f"{name}: locations={towns or '—'}, smogon_sets={len(sets)}")
        for s in sets:
            print(f"   {s.get('tier'):>4} {s.get('name')}")
