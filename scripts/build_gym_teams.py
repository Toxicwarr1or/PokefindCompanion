#!/usr/bin/env python3
"""
Walk QuestsToRemember/Gen{3,4,5}/ for gym + elite-four JSON files, extract each
leader/E4 member's name and final-battle Pokemon team, and write
content/gym-teams/<gen>.md per generation with the structured roster in
frontmatter for the layout to render.

Gym JSONs use duplicate-key conventions (the Lucille script-stage system) so
they can't be json.load()'d cleanly — we parse with a streaming brace-depth
scanner that surfaces each `BattleNpc` block in source order.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTS = Path("/home/jack/ClaudeProjects/QuestsToRemember")
OUT_DIR = ROOT / "content/gym-teams"


# ---------- Color-code stripping ----------

def strip_codes(s: str) -> str:
    """Strip Minecraft color/format codes (&x or §x), special icon glyphs, and
    leading non-printable markers so display names look clean."""
    if not s:
        return ""
    s = re.sub(r"[&§][0-9a-fk-or]", "", s)
    # Strip private-use glyphs and other non-ASCII custom-font markers
    s = re.sub(r"[^\x20-\x7e]+", " ", s)
    return s.strip(" |").strip()


# ---------- BattleNpc block extractor ----------

# Stage names that wrap a [npc-key, intro, win, loss, [team], options] array.
# Covers gen3 (AutoHardcoreBattleNpc), gen4 (AutoNpcBattleStage), gen5 (BattleNpc)
# and a few related variants found in the legacy quest files.
_BATTLE_STAGES = (
    "BattleNpc", "NpcBattleStage", "AutoNpcBattleStage",
    "AutoHardcoreBattleNpc", "AutoBattleNpc", "HardcoreBattleNpc",
    "BattleNpcMultiplyExperience", "AutoBattleNpcMultiplyExperience",
    "NoExperienceBattleNpc", "NoExperienceHardcoreNpcBattleStage",
    "HardcoreNpcBattleStage",
)
_BATTLE_NPC_RE = re.compile(
    r'"(' + "|".join(re.escape(s) for s in _BATTLE_STAGES) + r')"\s*:\s*\[',
    re.DOTALL,
)


def find_battle_npc_blocks(text: str) -> list[str]:
    """Return source slices of each BattleNpc array, including the surrounding
    [...] brackets."""
    blocks: list[str] = []
    for m in _BATTLE_NPC_RE.finditer(text):
        # Find the opening bracket and walk to the matching close
        start = text.find("[", m.start())
        if start < 0:
            continue
        depth = 0
        i = start
        in_str = False
        esc = False
        while i < len(text):
            c = text[i]
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif in_str:
                if c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "[":
                    depth += 1
                elif c == "]":
                    depth -= 1
                    if depth == 0:
                        blocks.append(text[start:i + 1])
                        break
            i += 1
    return blocks


def parse_battle_npc(block: str) -> dict | None:
    """Extract entity_key (NPC reference) and team (list of {species, level,
    nature, moves}) from a BattleNpc array source slice."""
    # First string literal in the array is the entity key. The block opens
    # with [, then any whitespace, then "<key>". Grab whatever's between the
    # first pair of quotes (entity keys can include digits, e.g. "Battle1").
    m = re.match(r'\[\s*"([^"]+)"', block)
    if not m:
        return None
    entity_key = m.group(1)
    # Find the inner team array — it's the first nested array of cube objects
    # with `species`. Search for the array that begins right before "species".
    species_pos = block.find('"species"')
    if species_pos < 0:
        return None
    # Walk backward to find the enclosing [
    i = species_pos
    depth = 0
    while i > 0:
        c = block[i]
        if c == "]":
            depth += 1
        elif c == "[":
            if depth == 0:
                team_start = i
                break
            depth -= 1
        i -= 1
    else:
        return None
    # Walk forward to find matching close
    depth = 0
    j = team_start
    in_str = False
    esc = False
    while j < len(block):
        c = block[j]
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif in_str:
            if c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    team_text = block[team_start:j + 1]
                    break
        j += 1
    else:
        return None

    # Parse each {...} pokemon object inside the team array
    pokemon: list[dict] = []
    obj_starts: list[int] = []
    depth = 0
    in_str = False
    esc = False
    for k, c in enumerate(team_text):
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif in_str:
            if c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                if depth == 0:
                    obj_starts.append(k)
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0 and obj_starts:
                    o_start = obj_starts.pop()
                    obj_text = team_text[o_start:k + 1]
                    p = _parse_pokemon_obj(obj_text)
                    if p:
                        pokemon.append(p)

    # Trainer NPCs in some files use anonymous battle slots ("Battle1") with
    # the speaker name embedded in the first dialog object's KEY:
    #   {"&b&lAvia": "intro line ..."}  ← Avia is the trainer name.
    # Surface that as a hint so the caller can use it when CreateEntity is absent.
    speaker_hint = ""
    sm = re.search(r'\{\s*"([^"]+)"\s*:', block)
    if sm:
        speaker_hint = strip_codes(sm.group(1))

    return {"entity_key": entity_key, "team": pokemon, "speaker_hint": speaker_hint}


def _parse_pokemon_obj(obj_text: str) -> dict | None:
    """Lenient extractor for {species, level, nature, moves: [...]} objects
    that may have malformed JSON (Lucille scripts often do)."""
    species = re.search(r'"species"\s*:\s*"([^"]+)"', obj_text)
    if not species:
        return None
    level = re.search(r'"level"\s*:\s*"?(\d+)"?', obj_text)
    nature = re.search(r'"nature"\s*:\s*"([^"]+)"', obj_text)
    moves_match = re.search(r'"moves"\s*:\s*\[(.*?)\]', obj_text, re.DOTALL)
    moves: list[str] = []
    if moves_match:
        moves = [m.strip().strip('"') for m in re.findall(r'"([^"]+)"', moves_match.group(1))]
    return {
        "species": species.group(1),
        "level": int(level.group(1)) if level else None,
        "nature": nature.group(1) if nature else "",
        "moves": moves,
    }


# ---------- CreateEntity name extractor ----------

_CREATE_ENTITY_RE = re.compile(r'"CreateEntity"\s*:\s*\{', re.DOTALL)


def find_entity_names(text: str) -> dict[str, str]:
    """Return {entity_key: clean_display_name}.

    Three conventions to handle:
      - gen5: "CreateEntity": { "key": "Foo", "name": ["...&lFoo", ...] }
      - gen4: top-level "npcs" object — keys are NPC IDs, values include "name"
      - gen3: "CreateEntity": { "key": "leader_norman", ... }
    """
    out: dict[str, str] = {}

    # gen5 / gen3 — CreateEntity blocks (duplicate-key script style)
    for m in _CREATE_ENTITY_RE.finditer(text):
        start = text.find("{", m.start())
        if start < 0:
            continue
        depth = 0
        i = start
        in_str = False
        esc = False
        while i < len(text):
            c = text[i]
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif in_str:
                if c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        block = text[start:i + 1]
                        key_m = re.search(r'"key"\s*:\s*"([^"]+)"', block)
                        name_m = re.search(r'"name"\s*:\s*\[\s*"([^"]+)"', block)
                        if not name_m:
                            name_m = re.search(r'"name"\s*:\s*"([^"]+)"', block)
                        if key_m:
                            display = strip_codes(name_m.group(1)) if name_m else key_m.group(1)
                            out[key_m.group(1)] = display
                        break
            i += 1

    # gen4 — top-level npcs: { Foo: { name: [...]}, ... }
    npcs_match = re.search(r'"npcs"\s*:\s*\{', text)
    if npcs_match:
        start = text.find("{", npcs_match.start())
        depth = 0
        i = start
        in_str = False
        esc = False
        end = -1
        while i < len(text):
            c = text[i]
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif in_str:
                if c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            i += 1
        if end > 0:
            npcs_text = text[start:end]
            # Find each top-level child key
            depth = 0
            in_str = False
            esc = False
            j = 1
            key_buf = None
            while j < len(npcs_text) - 1:
                c = npcs_text[j]
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif in_str:
                    if c == '"':
                        in_str = False
                else:
                    if c == '"':
                        in_str = True
                    elif c == "{":
                        depth += 1
                    elif c == "}":
                        depth -= 1
                if depth == 1 and c == '"' and not in_str:
                    # Just closed a string — look ahead for a colon → that's a key
                    pass
                j += 1
            # Simpler: regex per top-level NPC
            for em in re.finditer(r'"([A-Za-z_][A-Za-z0-9_]*)"\s*:\s*\{', npcs_text):
                npc_key = em.group(1)
                # Find this NPC's brace block
                obj_start = npcs_text.find("{", em.end() - 1)
                d = 0
                k = obj_start
                in_s = False
                esc2 = False
                while k < len(npcs_text):
                    cc = npcs_text[k]
                    if esc2:
                        esc2 = False
                    elif cc == "\\":
                        esc2 = True
                    elif in_s:
                        if cc == '"':
                            in_s = False
                    else:
                        if cc == '"':
                            in_s = True
                        elif cc == "{":
                            d += 1
                        elif cc == "}":
                            d -= 1
                            if d == 0:
                                obj = npcs_text[obj_start:k + 1]
                                nm = re.search(r'"name"\s*:\s*\[\s*"([^"]+)"', obj)
                                if not nm:
                                    nm = re.search(r'"name"\s*:\s*"([^"]+)"', obj)
                                disp = strip_codes(nm.group(1)) if nm else npc_key
                                out[npc_key] = disp
                                break
                    k += 1
    return out


# ---------- File-level extraction ----------

# Common entity-key conventions for the gym leader's team.
LEADER_KEYS = ("Gym_Leader", "GymLeader", "Leader", "gym_leader", "gymleader")


def _clean_trainer_name(name: str) -> str:
    name = re.sub(r"\s+Gym Leader.*$", "", name).strip()
    name = re.sub(r"\s+Pokemon (Ranger|Trainer).*$", "", name).strip()
    name = re.sub(r"^(Gym\s+)?Leader\s+", "", name).strip()
    return name


def extract_gym(path: Path) -> dict | None:
    """Returns {gym_index, leader_name, leader_team, trainers: [{name, team}, ...]}.

    The leader is the LAST battle stage (or one matching LEADER_KEYS); every
    other battle in the file is a gym trainer. Trainers are listed in source
    order; if the same NPC appears in multiple battle stages (e.g. a rematch
    or a multi-phase fight) we keep the last team only — the final lineup."""
    text = path.read_text()
    entities = find_entity_names(text)
    blocks = find_battle_npc_blocks(text)
    if not blocks:
        return None

    parsed: list[dict] = []
    for blk in blocks:
        b = parse_battle_npc(blk)
        if b and b["team"]:
            parsed.append(b)
    if not parsed:
        return None

    leader_block = None
    for b in parsed:
        ek = b["entity_key"]
        if ek in LEADER_KEYS or ek.lower().startswith("leader_"):
            leader_block = b
    if not leader_block:
        leader_block = parsed[-1]
    leader_key = leader_block["entity_key"]
    leader_name = _clean_trainer_name(entities.get(leader_key, "Gym Leader"))

    # Trainers: every battle other than the leader's. Each battle stage is
    # one trainer fight; we keep them all (no dedupe by entity_key, since
    # anonymous slot keys like "Battle1"/"Battle2" are reused script-wide).
    trainers = []
    for b in parsed:
        if b is leader_block:
            continue
        ek = b["entity_key"]
        # Display name resolution order: CreateEntity name → speaker hint → ek
        nm = entities.get(ek)
        if not nm or nm == ek:
            nm = b.get("speaker_hint") or ek
        trainers.append({"entity_key": ek, "name": _clean_trainer_name(nm), "team": b["team"]})

    m = re.search(r"gym[-_]?(\d+)", path.stem)
    gym_index = int(m.group(1)) if m else 0
    return {
        "gym_index": gym_index,
        "leader_name": leader_name,
        "team": leader_block["team"],
        "trainers": trainers,
    }


def extract_elite_four(path: Path) -> dict | None:
    """Returns {members: [{name, team}, ...]} for E4 + champion."""
    text = path.read_text()
    entities = find_entity_names(text)
    blocks = find_battle_npc_blocks(text)
    by_key: dict[str, dict] = {}
    order: list[str] = []
    for blk in blocks:
        b = parse_battle_npc(blk)
        if not b or not b["team"]:
            continue
        ek = b["entity_key"]
        if not ek:
            continue
        # Skip generic NPCs (League officials, gym trainers, common helper keys)
        skip_prefixes = ("League_Official", "Battle", "league_official", "battle_npc",
                          "Heal", "Trainer", "helper")
        if any(ek.startswith(p) for p in skip_prefixes):
            continue
        if ek not in by_key:
            order.append(ek)
        by_key[ek] = b   # last battle per NPC wins (final team)

    members = []
    for ek in order:
        b = by_key[ek]
        name = entities.get(ek, ek)
        name = re.sub(r"\s+(Elite Four|Champion|Pokemon (Ranger|Trainer)).*$", "", name).strip()
        members.append({"entity_key": ek, "name": name, "team": b["team"]})
    return {"members": members}


# ---------- YAML emission ----------

def yaml_string(value) -> str:
    s = "" if value is None else str(value)
    return "'" + s.replace("'", "''") + "'"


def yaml_list(items) -> str:
    if not items:
        return "[]"
    return "[" + ", ".join(yaml_string(x) for x in items) + "]"


def render_team_yaml(team: list[dict], indent: str) -> list[str]:
    out = []
    for p in team:
        out.append(f"{indent}- species: {yaml_string(p['species'])}")
        if p.get("level") is not None:
            out.append(f"{indent}  level: {p['level']}")
        if p.get("nature"):
            out.append(f"{indent}  nature: {yaml_string(p['nature'])}")
        if p.get("moves"):
            out.append(f"{indent}  moves: {yaml_list(p['moves'])}")
    return out


def render_gen_md(gen_label: str, gyms: list[dict], elite: dict | None) -> str:
    lines = ["---"]
    lines.append(f"title: {yaml_string(gen_label)}")
    lines.append(f"date: {date.today().isoformat()}")
    lines.append("gyms:")
    for g in sorted(gyms, key=lambda x: x["gym_index"]):
        lines.append(f"  - index: {g['gym_index']}")
        lines.append(f"    leader: {yaml_string(g['leader_name'])}")
        lines.append("    team:")
        lines.extend(render_team_yaml(g["team"], "      "))
        if g.get("trainers"):
            lines.append("    trainers:")
            for t in g["trainers"]:
                lines.append(f"      - name: {yaml_string(t['name'])}")
                lines.append("        team:")
                lines.extend(render_team_yaml(t["team"], "          "))
    if elite and elite.get("members"):
        lines.append("elite_four:")
        for m in elite["members"]:
            lines.append(f"  - name: {yaml_string(m['name'])}")
            lines.append("    team:")
            lines.extend(render_team_yaml(m["team"], "      "))
    lines.append("---\n")
    return "\n".join(lines)


# ---------- Main ----------

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = []
    for gen in (3, 4, 5):
        gen_dir = QUESTS / f"Gen{gen}"
        if not gen_dir.exists():
            continue
        gym_files = sorted(gen_dir.glob("*gym*.json"))
        gym_files = [f for f in gym_files if "elite" not in f.stem.lower()]
        gyms = []
        for gf in gym_files:
            try:
                g = extract_gym(gf)
                if g:
                    gyms.append(g)
            except Exception as e:
                print(f"  fail {gf.name}: {e}", file=sys.stderr)
        elite_paths = list(gen_dir.glob("*elite*.json"))
        elite = None
        if elite_paths:
            try:
                elite = extract_elite_four(elite_paths[0])
            except Exception as e:
                print(f"  fail {elite_paths[0].name}: {e}", file=sys.stderr)

        out_path = OUT_DIR / f"gen{gen}.md"
        out_path.write_text(render_gen_md(f"Gen {gen}", gyms, elite), encoding="utf-8")
        summary.append((gen, len(gyms), len((elite or {}).get("members") or [])))

    print("Gen | gyms | E4 members")
    for gen, ng, ne in summary:
        print(f"  Gen {gen}:  {ng} gyms, {ne} E4/champion entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
