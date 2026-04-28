#!/usr/bin/env python3
"""
Walk ~/Desktop/quests/gen{1..5}/ and surface every quest that appears in the
in-game /questlog. A quest is "logged" when its top-level definition has
either "Quest": true or "hideInQuestLog": false.

Seasonal/event scripts (Christmas, Easter, Halloween, etc.) are filtered out
by filename pattern — only permanent, year-round quests are kept.

For each quest, extract Key / Name / Description / Author and emit
content/quests/gen{N}.md with the structured list in frontmatter for the
generation-tabbed layout to render.

Quest JSONs use the duplicate-key Lucille script convention (multiple
"CreateEntity" siblings in one object), so json.load can't always parse them.
We fall back to regex-based extraction for the few fields we need.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

QUESTS_ROOT = Path("/home/jack/Desktop/quests")
WIKI_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = WIKI_ROOT / "content/quests"
MAP_YML = Path("/home/jack/Downloads/prod-map.yml")
YT_TSV = Path(__file__).resolve().parent / "youtube_videos.tsv"

# Words too generic to differentiate quests — strip from both sides during
# fuzzy matching so they don't count toward the overlap score.
_VIDEO_STOPWORDS = {
    "pokefind", "pokemon", "the", "of", "a", "an", "to", "in", "on", "for",
    "and", "is", "at", "by", "or", "with", "guide", "complete", "all",
    "act", "part", "ep", "episode", "video", "tutorial", "main", "questline",
    "side", "story", "generation", "gen", "new", "old",
}


_ROMAN_TO_ARABIC = {
    "i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5", "vi": "6",
    "vii": "7", "viii": "8", "ix": "9", "x": "10",
    # The legacy quest titles use "IIII" for IV — preserve that mapping.
    "iiii": "4",
}


def _tokenize(s: str) -> set[str]:
    """Lowercase + split on non-alphanumerics; drop stopwords + 1-char tokens.
    Also normalize Roman-numeral part markers to digits so 'Part I' matches
    'Part 1' across quest titles vs. video titles."""
    toks = re.split(r"[^a-z0-9]+", s.lower())
    out: set[str] = set()
    for t in toks:
        if not t:
            continue
        if t in _ROMAN_TO_ARABIC:
            t = _ROMAN_TO_ARABIC[t]
        if len(t) <= 1 and not t.isdigit():
            continue
        if t in _VIDEO_STOPWORDS:
            continue
        out.add(t)
    return out


# Manual quest_key → video_id overrides. Use this for quests whose names are
# all stopwords (e.g. "Gen 5 Intro" → tokenize() returns empty), or where the
# fuzzy matcher picks the wrong video. The override always wins over fuzzy.
VIDEO_OVERRIDES = {
    "gen5_intro": ("RMZt4aYZM0k", "Welcome to PokeFind (Episode 1: Gen 5 Introduction)"),
    "a_cosmic_discovery_main": ("F-joH5oorY0", "The Electrode Puzzle (A Cosmic Discovery Act 4)"),
}

# Some quests are split across a "main" script and several act/sub scripts
# that don't carry the Quest flag themselves. Concatenate their walkthroughs
# so the per-quest page covers the full story.
# Files are looked up in the same gen{N}/ folder as the main script.
EXTRA_SCRIPTS = {
    "a_cosmic_discovery_main": [
        "a-cosmic-discovery-act1.json",
        "a-cosmic-discovery-act2.json",
        "a-cosmic-discovery-act3.json",
        "a-cosmic-discovery-act4.json",
        "a-cosmic-discovery-act5.json",
    ],
}

# Act-by-act video map for multi-act quests. Each step is tagged with the
# act it belongs to (detected via `"Start": "<sub_script_key>"` calls in
# the main script); the layout renders an act divider + video embed at
# every act boundary.
ACT_VIDEOS = {
    "a_cosmic_discovery_main": {
        "a_cosmic_discovery_act1": ("Poz_poHJUac", "The Cosmic Discovery (Act 1)"),
        "a_cosmic_discovery_act2": ("55-InwocIcw", "The Cosmic Discovery (Act 2)"),
        "a_cosmic_discovery_act3": ("mjW-rFS2pas", "The Cosmic Discovery (Act 3)"),
        "a_cosmic_discovery_act4": ("riBH-LXV640", "The Cosmic Discovery (Act 4)"),
        "a_cosmic_discovery_act5": ("nKW5qq3Znt8", "The Cosmic Discovery (Act 5)"),
    },
}


def load_youtube_videos() -> list[tuple[str, str]]:
    """Read the cached (video_id, title) list. Run fetch_youtube_videos.py
    first to populate it. Empty list if the file is missing."""
    if not YT_TSV.exists():
        return []
    out: list[tuple[str, str]] = []
    for line in YT_TSV.read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        vid, title = line.split("\t", 1)
        out.append((vid, title))
    return out


def match_video_for_quest(quest_name: str, gen: int,
                          videos: list[tuple[str, str]]) -> tuple[str, str] | None:
    """Pick the YouTube video most likely to be a guide for this quest.

    Score = number of meaningful tokens from the quest name that also appear in
    the video title. Tie-broken by:
      - matching gen reference (e.g. 'Generation 3' / 'Gen 3' for gen=3)
      - shorter video title (more focused match)
    Returns None if the best score is below 2 (i.e. not enough overlap to be
    meaningfully linked)."""
    q_toks = _tokenize(quest_name)
    if not q_toks:
        return None
    gen_re = re.compile(rf"\b(?:gen(?:eration)?\s*0*{gen})\b", re.IGNORECASE)

    q_digits = {t for t in q_toks if t.isdigit()}
    # Match: "5-8", "5 - 8", "Part 1 - Part 3", "Parts 1 to 3"
    # NOTE: no leading \b — "Part5-8" runs digits straight after letters with
    # no word boundary, so we match digits anywhere followed by a dash/to/through.
    range_re = re.compile(
        r"(\d+)\s*(?:[-–]|to|through)\s*(?:Part\s*|Parts\s*)?(\d+)\b",
        re.IGNORECASE,
    )
    # The phrase "Generation N" / "Gen N" injects a stray digit ("3") that
    # collides with quest part numbers. Strip those before tokenizing the
    # video title so only meaningful part-numbers count.
    gen_strip_re = re.compile(r"\b(?:gen(?:eration)?)\s*0*\d+\b", re.IGNORECASE)
    best: tuple[int, int, int, int, int, str, str] | None = None  # (score, digit_match, digit_mismatch_neg, gen_bonus, -len, vid, title)
    for vid, title in videos:
        cleaned = gen_strip_re.sub(" ", title)
        v_toks = _tokenize(cleaned)
        # Expand any "Part 5-8" / "Part5-8" range markers to cover every part
        # number in the range, so a "Part 6" quest can match a 5-8 video.
        for rm in range_re.finditer(cleaned):
            try:
                lo, hi = int(rm.group(1)), int(rm.group(2))
                if 0 < hi - lo <= 20:
                    v_toks.update(str(n) for n in range(lo, hi + 1))
            except ValueError:
                pass
        overlap = len(q_toks & v_toks)
        if overlap < 2:
            continue
        v_digits = {t for t in v_toks if t.isdigit()}
        digit_match = len(q_digits & v_digits)
        # Penalty if the video has a number that the quest doesn't share.
        # 'Bitter Rivals Part 1' should NOT match 'Part 9' video (one diff).
        digit_mismatch = -len((q_digits | v_digits) - (q_digits & v_digits))
        if q_digits and digit_match == 0:
            # Quest is numbered but no digit matches — almost always wrong.
            continue
        gen_bonus = 1 if gen_re.search(title) else 0
        candidate = (overlap, digit_match, digit_mismatch, gen_bonus, -len(title), vid, title)
        if best is None or candidate > best:
            best = candidate
    if best is None:
        return None
    return (best[5], best[6])

# Loaded lazily — see _load_towns(). Each entry: (display_name, bbox tuple).
_TOWNS_CACHE: list[tuple[str, tuple[int, int, int, int, int, int]]] | None = None


def _load_towns() -> list[tuple[str, tuple]]:
    """Pull the 'area_*' regions from prod-map.yml and return their display
    names + bboxes. Used to look up which town a coordinate falls inside."""
    global _TOWNS_CACHE
    if _TOWNS_CACHE is not None:
        return _TOWNS_CACHE
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from build_pokedex_extras import parse_map_yml  # type: ignore
        m = parse_map_yml(MAP_YML)
    except Exception:
        _TOWNS_CACHE = []
        return _TOWNS_CACHE
    towns: list[tuple[str, tuple]] = []
    for k, v in m.items():
        if not k.startswith("area_"):
            continue
        if "world" in k or "minimap" in k:
            continue
        towns.append((v.get("display") or k, v["bbox"]))
    _TOWNS_CACHE = towns
    return towns


# Words that follow a capitalized stem to flag a place name. The prod-map
# only covers Zeinova (gen5), so for gen1-4 we mine town names out of the
# quest text itself by spotting these suffix words.
_PLACE_SUFFIXES = (
    "Town", "City", "Village", "Harbor", "Port", "Forest", "Cave",
    "Mountain", "Lake", "Island", "Shrine", "Bay", "Grove", "Hollow",
    "Plains", "Sanctuary", "Temple", "Mine", "Falls", "Park", "Ruins",
    "Garden", "Beach", "Desert", "Crater", "Valley", "Meadow", "Sewer",
    "Castle",
    # NOT included: Gym, HQ, Lab, Center, Stadium, Arena, Tower, Plaza,
    # District, Square, Outskirts — those describe a building or sub-area
    # within a town and would over-capture (e.g. "Finderia Town Gym" should
    # surface as "Finderia Town", not the gym name).
)
_PLACE_RE = re.compile(
    r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s+("
    + "|".join(_PLACE_SUFFIXES)
    + r")\b"
)


def extract_place_names(text: str) -> list[str]:
    """Return distinct place names mentioned in the text (e.g. 'Foretree
    Village', 'Smog Town'), in source order. Used to attach a town label to
    objective steps when the prod-map can't help (gen1-4 regions)."""
    seen: list[str] = []
    seen_set: set[str] = set()
    for m in _PLACE_RE.finditer(text):
        place = f"{m.group(1)} {m.group(2)}"
        # Reject false positives where the leading word is a common verb.
        if m.group(1) in ("Find", "Talk", "Battle", "Fight", "Defeat", "Use",
                          "Catch", "Bring", "Speak", "Meet", "Click", "Pick",
                          "Get", "Give", "Take", "Beat", "The"):
            place = m.group(2)
        if place not in seen_set:
            seen.append(place)
            seen_set.add(place)
    return seen


def town_at(x: float | None, y: float | None, z: float | None) -> str:
    """Return the display name of the town containing (x,y,z). Falls back to
    the nearest town within ~150 blocks if the point is outside every bbox
    (NPCs commonly stand on the edge of a town, just past the area marker).
    Y is ignored; only x/z matter."""
    if x is None or z is None:
        return ""
    best_name = ""
    best_dist = 150.0  # max acceptable distance, in blocks
    for name, b in _load_towns():
        if b[0] <= x <= b[3] and b[2] <= z <= b[5]:
            return name
        # Distance from the point to the bbox
        dx = max(b[0] - x, 0, x - b[3])
        dz = max(b[2] - z, 0, z - b[5])
        d = (dx * dx + dz * dz) ** 0.5
        if d < best_dist:
            best_dist = d
            best_name = name
    return best_name

# Filename markers that flag a script as seasonal/event-only. Case-insensitive
# substring match against the filename stem. If the user adds new seasonal
# series, extend this list.
SEASONAL_MARKERS = (
    "christmas", "xmas", "advent",
    "easter",
    "halloween", "haunt", "spooky", "twisted_tomb", "twisted-tomb",
    "candy-thief", "candy_thief", "costume", "feast-for-one",
    "valentine",
    "summer", "festival",
    "patrick",
    "star_wars", "starwars",
    "_anni_", "anni-", "anniversary",
    "_xmas", "-xmas",
    "_day1", "_day2", "_day3", "_day4", "_day5", "_day6",
    "_day7", "_day8", "_day9", "_day10", "_day11", "_day12",
    "day1-", "day2-", "day3-", "day4-", "day5-", "day6-",
    "day7-", "day8-", "day9-", "day10-", "day11-", "day12-",
    "day-1-", "day-2-", "day-3-", "day-4-", "day-5-", "day-6-",
    "day-7-", "day-8-", "day-9-", "day-10-", "day-11-", "day-12-",
    "_day_", "-day-",
    "christmasday",
    "chaotic-christmas",
    "a-night-to-remember",
    # Minigames and one-off events that show up in /questlog but aren't
    # storyline quests, so they don't belong in the wiki's quest index.
    "day2finderia",
    "zombie-outbreak", "zombie_outbreak",
    "funley-",
    "cm-suppmain",
    "elite-four-daily",
    "woc-intro",
    "villainous-resurrection",
    "baremaw",
    "dw-main",
    "message-in-a-bottle-1",
)

# Exact filename-stem matches (no substring) for quests we want excluded
# without affecting partial-name siblings (e.g. drop gen1 'fossil' but keep
# gen5 'fossil_frenzy_main2').
EXCLUDE_EXACT_STEMS = {
    "fossil",   # Gen 1 "Digging Up The Past"
}


def is_seasonal(stem: str) -> bool:
    s = stem.lower()
    if s in EXCLUDE_EXACT_STEMS:
        return True
    return any(m in s for m in SEASONAL_MARKERS)


# ---------- Color-code stripping ----------

def strip_codes(s: str) -> str:
    """Strip Minecraft color/format codes (&x or §x) and Pokefind's custom-
    font private-use glyphs, while preserving normal Unicode letters
    (é, ü, accented characters in Pokémon names, etc.)."""
    if not s:
        return ""
    s = re.sub(r"[&§][0-9a-fk-or]", "", s)
    # Strip Unicode private-use area (custom Minecraft font icons).
    s = re.sub(r"[\ue000-\uf8ff\U000f0000-\U0010ffff]+", " ", s)
    # Strip the Pokefind decorative prefix glyph ǌ (U+01CC) used as a name icon
    s = s.replace("\u01cc", "")
    return re.sub(r"\s+", " ", s).strip(" |").strip()


# ---------- Field extraction ----------

# A Lucille script root object often has duplicate keys ("CreateEntity" appears
# many times), so json.load may fail. For the four scalar fields we care about
# (Key / Name / Description / Author) we extract with regex against the source.
_FIELD_RES = {
    "key":          re.compile(r'"[Kk]ey"\s*:\s*"([^"]+)"'),
    "name":         re.compile(r'"[Nn]ame"\s*:\s*"([^"]+)"'),
    "description":  re.compile(r'"[Dd]escription"\s*:\s*"((?:[^"\\]|\\.)*)"'),
    "author":       re.compile(r'"[Aa]uthor"\s*:\s*"([^"]+)"'),
}
# Some legacy files quote the boolean (`"hideInQuestLog": "false"`) instead of
# using the JSON literal — accept either form.
_QUEST_FLAG_RE       = re.compile(r'"Quest"\s*:\s*"?true"?')
_HIDE_LOG_FALSE_RE   = re.compile(r'"hideInQuestLog"\s*:\s*"?false"?')
_SHOW_LOG_TRUE_RE    = re.compile(r'"showInQuestLog"\s*:\s*"?true"?')

# Modern (gen4/5) and legacy (gen1-3) prereq stages. We capture every quest
# key referenced inside the stage's value:
#   "Completed": "other_quest"
#   "Completed": ["other_quest", true, ""]
#   "Completed": [["q1", true], ["q2", true]]   ← also seen
#   "CompletedOtherQuestProgress": ["other_quest"]
_PREREQ_BLOCK_RE = re.compile(
    r'"(?:Completed|CompletedOtherQuestProgress)"\s*:\s*'
    r'(?:"([^"]+)"|\[(.*?)\])',
    re.DOTALL,
)
_QUOTED_KEY_RE = re.compile(r'"([A-Za-z_][A-Za-z0-9_]*)"')


def is_logged_quest(text: str) -> bool:
    return bool(
        _QUEST_FLAG_RE.search(text)
        or _HIDE_LOG_FALSE_RE.search(text)
        or _SHOW_LOG_TRUE_RE.search(text)
    )


def extract_quest(path: Path) -> dict | None:
    text = path.read_text(errors="replace")
    if not is_logged_quest(text):
        return None

    out = {"file": path.name}
    for field, regex in _FIELD_RES.items():
        m = regex.search(text)
        if m:
            raw = m.group(1)
            # Decode common JSON escape sequences in the description
            raw = raw.replace('\\"', '"').replace('\\n', ' ').replace('\\\\', '\\')
            out[field] = strip_codes(raw)
        else:
            out[field] = ""

    # Collect prereq quest keys referenced by Completed / CompletedOtherQuestProgress
    prereqs: set[str] = set()
    for m in _PREREQ_BLOCK_RE.finditer(text):
        scalar, array = m.group(1), m.group(2)
        if scalar:
            prereqs.add(scalar)
        elif array:
            # Inside an array, every quoted identifier is a candidate prereq.
            # Filter out the obvious non-key tokens ("true", "false", "").
            for km in _QUOTED_KEY_RE.finditer(array):
                tok = km.group(1)
                if tok in ("true", "false"):
                    continue
                prereqs.add(tok)
    # A quest never lists itself as a prereq
    prereqs.discard(out.get("key", ""))
    out["prereqs"] = sorted(prereqs)

    # Quest must have at least a name or a key to be useful
    if not (out.get("name") or out.get("key")):
        return None
    return out


# ---------- Source-order streaming scanner ----------

def _scan_value(text: str, i: int) -> int:
    """Scan a JSON value starting at index i and return the index just after
    the value's last character. Handles strings, arrays, objects, and scalar
    literals (numbers / true / false / null). Tolerates duplicate-key Lucille
    objects by tracking depth, not parsing structure."""
    n = len(text)
    while i < n and text[i] in " \t\r\n":
        i += 1
    if i >= n:
        return i
    c = text[i]
    if c == '"':
        i += 1
        esc = False
        while i < n:
            ch = text[i]
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                return i + 1
            i += 1
        return i
    if c in "{[":
        close = "}" if c == "{" else "]"
        depth = 0
        in_str = False
        esc = False
        while i < n:
            ch = text[i]
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif in_str:
                if ch == '"':
                    in_str = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == c:
                    depth += 1
                elif ch == close:
                    depth -= 1
                    if depth == 0:
                        return i + 1
            i += 1
        return i
    # scalar literal — read until comma / closing bracket / whitespace
    while i < n and text[i] not in ",}]\r\n":
        i += 1
    return i


def stream_top_level(text: str):
    """Yield (key, value_text) pairs at the root object's depth, in source
    order. Preserves duplicate keys (Lucille script convention) and tolerates
    trailing commas / unconventional whitespace."""
    n = len(text)
    # Find the root '{'
    i = 0
    while i < n and text[i] != "{":
        i += 1
    if i >= n:
        return
    i += 1  # past '{'
    while i < n:
        # skip whitespace + commas
        while i < n and text[i] in " \t\r\n,":
            i += 1
        if i >= n or text[i] == "}":
            return
        if text[i] != '"':
            i += 1
            continue
        # read key string
        key_start = i + 1
        i += 1
        esc = False
        while i < n:
            ch = text[i]
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                break
            i += 1
        key = text[key_start:i]
        i += 1  # past closing quote
        # skip whitespace + colon
        while i < n and text[i] in " \t\r\n":
            i += 1
        if i < n and text[i] == ":":
            i += 1
        while i < n and text[i] in " \t\r\n":
            i += 1
        # read value
        value_start = i
        i = _scan_value(text, i)
        value_text = text[value_start:i]
        yield key, value_text


# ---------- Walkthrough extraction ----------

_BATTLE_STAGE_NAMES = {
    "BattleNpc", "NpcBattleStage", "AutoNpcBattleStage",
    "AutoHardcoreBattleNpc", "AutoBattleNpc", "HardcoreBattleNpc",
    "BattleNpcMultiplyExperience", "AutoBattleNpcMultiplyExperience",
    "NoExperienceBattleNpc", "NoExperienceHardcoreNpcBattleStage",
    "HardcoreNpcBattleStage", "NoExperienceAutoBattleNpc",
}

_REWARD_STAGE_NAMES = {
    "GiveItem", "GivePokemon", "GiveTokens", "GiveCoins",
    "GiveItemStage", "GiveCoinsStage", "GiveTokensStage",
    "GiveTrainerExperience", "GiveTrainerExperienceStage",
    "GiveAchievement",
}

# Stages that gate the next objective on the player entering / being in a
# bbox. We treat these as fallback coordinate sources too — bbox center is
# the "go here" point.
_REGION_STAGE_NAMES = {
    "RegionEntry", "RegionEntryStage", "QuestRegion", "QuestRegionStage",
    "InRegion", "InRegionStage",
    "NoFlyRegionStage", "NoTpRegionStage",
}

# Stages whose value names a target entity_key (NPC the player should
# interact with). Used to derive go-to coordinates for steps that don't have
# an explicit SetPoi.
_TARGET_STAGE_NAMES = {
    "HighlightClickEntity", "HighlightClickEntityStage",
    "ClickEntity", "ClickEntityOptions",
}

# Stages whose value contains explicit destination coordinates. Used as a
# last-resort backfill when a step has neither a SetPoi nor an NPC target —
# typically "follow X to Y" / "go through cutscene to Y" objectives.
_COORD_FALLBACK_STAGES = {
    # ["entity_key", x, y, z, ...]
    "MoveEntity", "ProgressiveMoveEntity", "TeleportEntity",
    # [x, y, z, yaw, pitch]
    "Teleport", "TeleportStage",
    # [x, y, z, label, item_name]
    "PickupItem", "PickupItemStage",
    # [x, y, z, ...] — particle markers / hologram spawn points
    "Hologram", "HologramStage", "Particle", "ParticleStage",
    # ["entity_key", x, y, z, ...] or [x, y, z, ...]
    "SpawnPokemon", "SummonPokemon", "StrikeLightningStage",
}


def _parse_json_array(value_text: str) -> list | None:
    """Best-effort: try strict JSON first; on failure return None. The caller
    falls back to regex extraction for malformed stage values."""
    try:
        return json.loads(value_text)
    except Exception:
        return None


def _parse_npcs_block(value_text: str):
    """Yield (npc_key, body_text) for each child of a legacy `npcs: {...}`
    block. The body text is the full {...} of that npc's definition so the
    caller can pull name + location with regex."""
    # Strip the outer {} wrapping the npcs object
    txt = value_text.strip()
    if not txt.startswith("{"):
        return
    txt = txt[1:]
    # Walk the body looking for top-level keys
    n = len(txt)
    i = 0
    while i < n:
        while i < n and txt[i] in " \t\r\n,":
            i += 1
        if i >= n or txt[i] == "}":
            return
        if txt[i] != '"':
            i += 1
            continue
        # read key
        key_start = i + 1
        i += 1
        esc = False
        while i < n:
            ch = txt[i]
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                break
            i += 1
        key = txt[key_start:i]
        i += 1  # past closing quote
        while i < n and txt[i] in " \t\r\n":
            i += 1
        if i < n and txt[i] == ":":
            i += 1
        while i < n and txt[i] in " \t\r\n":
            i += 1
        # value should start with {
        value_start = i
        i = _scan_value(txt, i)
        yield key, txt[value_start:i]


def _parse_create_entity(value_text: str) -> dict | None:
    """Pull out `key`, location coords, and display name from a CreateEntity
    object. Returns {key, name, x, y, z} or None."""
    key_m = re.search(r'"key"\s*:\s*"([^"]+)"', value_text)
    if not key_m:
        return None
    name_m = re.search(r'"name"\s*:\s*\[\s*"([^"]+)"', value_text)
    if not name_m:
        name_m = re.search(r'"name"\s*:\s*"([^"]+)"', value_text)
    out = {"key": key_m.group(1)}
    if name_m:
        out["name"] = strip_codes(name_m.group(1))
    # Pull from a nested "location": {x, y, z, ...}
    loc_m = re.search(r'"location"\s*:\s*\{([^}]*)\}', value_text, re.DOTALL)
    if loc_m:
        body = loc_m.group(1)
        for axis in ("x", "y", "z"):
            am = re.search(rf'"{axis}"\s*:\s*(-?\d+(?:\.\d+)?)', body)
            if am:
                out[axis] = float(am.group(1))
    # Or from a positional array: "location": [x, y, z, yaw, pitch]
    if "x" not in out:
        arr_m = re.search(r'"location"\s*:\s*\[([^\]]*)\]', value_text, re.DOTALL)
        if arr_m:
            nums = re.findall(r"-?\d+(?:\.\d+)?", arr_m.group(1))
            if len(nums) >= 3:
                out["x"] = float(nums[0])
                out["y"] = float(nums[1])
                out["z"] = float(nums[2])
    return out


def _parse_objective(value_text: str) -> str:
    """Objective value is `["text", weight]` (modern) or `"text"` (legacy)."""
    if value_text.lstrip().startswith('"'):
        m = re.match(r'\s*"((?:[^"\\]|\\.)*)"', value_text)
        if m:
            return strip_codes(m.group(1).replace('\\"', '"'))
    m = re.match(r'\s*\[\s*"((?:[^"\\]|\\.)*)"', value_text)
    if m:
        return strip_codes(m.group(1).replace('\\"', '"'))
    return ""


def _parse_set_poi(value_text: str) -> dict | None:
    """SetPoi value is `[x, y, z, "label"]`."""
    nums = re.findall(r"-?\d+(?:\.\d+)?", value_text)
    if len(nums) < 3:
        return None
    out = {"x": float(nums[0]), "y": float(nums[1]), "z": float(nums[2])}
    label_m = re.search(r'"((?:[^"\\]|\\.)*)"', value_text)
    if label_m:
        out["label"] = strip_codes(label_m.group(1))
    return out


def _parse_teleport(value_text: str) -> dict | None:
    """Teleport value is `[x, y, z, yaw, pitch]`."""
    nums = re.findall(r"-?\d+(?:\.\d+)?", value_text)
    if len(nums) < 3:
        return None
    return {"x": float(nums[0]), "y": float(nums[1]), "z": float(nums[2])}


def _parse_battle_inline(value_text: str) -> dict | None:
    """Light parse of a BattleNpc-style array: pull entity_key, speaker hint,
    and the team list. Returns {entity_key, speaker, team[]}."""
    ek_m = re.match(r'\s*\[\s*"([^"]+)"', value_text)
    if not ek_m:
        return None
    entity_key = ek_m.group(1)
    speaker_m = re.search(r'\{\s*"([^"]+)"\s*:', value_text)
    speaker = strip_codes(speaker_m.group(1)) if speaker_m else ""
    # Find first nested array containing pokemon objects with "species"
    team: list[dict] = []
    sp_pos = value_text.find('"species"')
    if sp_pos > 0:
        # walk back to enclosing [
        depth = 0
        i = sp_pos
        while i > 0:
            ch = value_text[i]
            if ch == "]":
                depth += 1
            elif ch == "[":
                if depth == 0:
                    start = i
                    break
                depth -= 1
            i -= 1
        else:
            start = -1
        if start >= 0:
            # walk forward to matching ]
            depth = 0
            j = start
            in_str = False
            esc = False
            while j < len(value_text):
                ch = value_text[j]
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif in_str:
                    if ch == '"':
                        in_str = False
                else:
                    if ch == '"':
                        in_str = True
                    elif ch == "[":
                        depth += 1
                    elif ch == "]":
                        depth -= 1
                        if depth == 0:
                            team_text = value_text[start:j + 1]
                            for obj_m in re.finditer(
                                r'\{\s*"species"\s*:\s*"([^"]+)"[^}]*?\}',
                                team_text,
                                re.DOTALL,
                            ):
                                obj = obj_m.group(0)
                                lvl_m = re.search(r'"level"\s*:\s*"?(\d+)"?', obj)
                                team.append({
                                    "species": obj_m.group(1),
                                    "level": int(lvl_m.group(1)) if lvl_m else None,
                                })
                            break
                j += 1
    return {"entity_key": entity_key, "speaker": speaker, "team": team}


def _parse_reward(stage: str, value_text: str) -> str | None:
    """Render a one-line summary of a Give* reward."""
    nums = re.findall(r"-?\d+(?:\.\d+)?", value_text)
    items = re.findall(r'"((?:[^"\\]|\\.)*)"', value_text)
    items = [strip_codes(x) for x in items if x.strip()]
    if stage in ("GiveItem", "GiveItemStage"):
        if items:
            count = nums[0] if nums else None
            return f"{count}× {items[0]}" if count and count != "1" else items[0]
    if stage == "GivePokemon":
        # Two source formats:
        #   ["Bulbasaur", 5]                                  ← positional
        #   [{"species": "Bulbasaur", "level": 5, ...}, ...]  ← object form
        sp_m = re.search(r'"species"\s*:\s*"([^"]+)"', value_text)
        species = sp_m.group(1) if sp_m else (items[0] if items else "")
        if not species:
            return None
        lvl_m = re.search(r'"level"\s*:\s*"?(\d+)"?', value_text)
        level = lvl_m.group(1) if lvl_m else (nums[0] if nums else "")
        return f"Pokémon: {species}" + (f" (Lv {level})" if level else "")
    if stage in ("GiveCoins", "GiveCoinsStage") and nums:
        return f"{nums[0]} Coins"
    if stage in ("GiveTokens", "GiveTokensStage") and nums:
        return f"{nums[0]} Tokens"
    if stage in ("GiveTrainerExperience", "GiveTrainerExperienceStage") and nums:
        return f"{nums[0]} Trainer XP"
    if stage == "GiveAchievement" and items:
        return f"Achievement: {items[0]}"
    return None


def collect_entities(text: str) -> dict[str, dict]:
    """Light pass over a script: return {entity_key: {name, x, y, z}} for every
    CreateEntity / npcs-block entry. Used to pre-seed the main quest's entity
    registry with NPCs defined in act/sub scripts so step lookups can resolve
    them across files."""
    out: dict[str, dict] = {}
    for key, val in stream_top_level(text):
        if key == "CreateEntity":
            ent = _parse_create_entity(val)
            if ent and ent.get("key"):
                out[ent["key"]] = ent
        elif key == "npcs":
            for npc_key, npc_body in _parse_npcs_block(val):
                ent = {"key": npc_key}
                name_m = re.search(r'"name"\s*:\s*\[\s*"([^"]+)"', npc_body)
                if not name_m:
                    name_m = re.search(r'"name"\s*:\s*"([^"]+)"', npc_body)
                if name_m:
                    ent["name"] = strip_codes(name_m.group(1))
                loc_m = re.search(r'"location"\s*:\s*\{([^}]*)\}', npc_body, re.DOTALL)
                if loc_m:
                    body = loc_m.group(1)
                    for axis in ("x", "y", "z"):
                        am = re.search(rf'"{axis}"\s*:\s*(-?\d+(?:\.\d+)?)', body)
                        if am:
                            ent[axis] = float(am.group(1))
                out[npc_key] = ent
    return out


def extract_walkthrough(text: str, gen_num: int = 5,
                        extra_entities: dict[str, dict] | None = None,
                        act_keys: set[str] | None = None) -> tuple[list[dict], dict]:
    """Stream the script in source order. Build a list of steps where each
    step is anchored to an Objective and bucket subsequent SetPoi / Teleport /
    Battle / Reward events under it until the next Objective.

    Returns (steps, meta). meta has:
      - final_rewards: any Give* stages that landed before the first Objective
      - start: {npc, x, y, z, town, description} for the quest's starting NPC
    """
    # First pass: collect every CreateEntity (with location) so we can resolve
    # battle entity_keys to display names AND remember NPC coords for the
    # starting-NPC lookup. Also capture AddProperty["Start", ...] description.
    entities: dict[str, str] = {}
    entity_locations: dict[str, dict] = {}
    create_order: list[str] = []
    start_description = ""
    # Pre-seed with entities defined in associated act/sub scripts so steps
    # in the main file can resolve NPCs declared elsewhere.
    if extra_entities:
        for ek, ent in extra_entities.items():
            if ent.get("name"):
                entities[ek] = ent["name"]
            if any(a in ent for a in ("x", "y", "z")):
                entity_locations[ek] = ent
    for key, val in stream_top_level(text):
        if key == "CreateEntity":
            ent = _parse_create_entity(val)
            if ent:
                if ent.get("name"):
                    entities[ent["key"]] = ent["name"]
                if "x" in ent or "y" in ent or "z" in ent:
                    entity_locations[ent["key"]] = ent
                if ent["key"] not in create_order:
                    create_order.append(ent["key"])
        elif key == "npcs":
            # Legacy gen1/2/3 format: top-level "npcs": { key: {name, location}, ... }
            for npc_key, npc_body in _parse_npcs_block(val):
                ent = {"key": npc_key}
                name_m = re.search(r'"name"\s*:\s*\[\s*"([^"]+)"', npc_body)
                if not name_m:
                    name_m = re.search(r'"name"\s*:\s*"([^"]+)"', npc_body)
                if name_m:
                    ent["name"] = strip_codes(name_m.group(1))
                loc_m = re.search(r'"location"\s*:\s*\{([^}]*)\}', npc_body, re.DOTALL)
                if loc_m:
                    body = loc_m.group(1)
                    for axis in ("x", "y", "z"):
                        am = re.search(rf'"{axis}"\s*:\s*(-?\d+(?:\.\d+)?)', body)
                        if am:
                            ent[axis] = float(am.group(1))
                if ent.get("name"):
                    entities[npc_key] = ent["name"]
                if any(a in ent for a in ("x", "y", "z")):
                    entity_locations[npc_key] = ent
                if npc_key not in create_order:
                    create_order.append(npc_key)
        elif key == "AddProperty":
            prop_m = re.match(r'\s*\[\s*"([^"]+)"\s*,\s*"((?:[^"\\]|\\.)*)"', val)
            if prop_m and prop_m.group(1).lower() == "start":
                start_description = strip_codes(prop_m.group(2))

    steps: list[dict] = []
    rewards: list[str] = []
    current: dict | None = None
    # SetPoi sometimes precedes Objective (poi describing where the next
    # objective sends you); cache and apply to the next-created step.
    pending_poi: dict | None = None
    current_act_key: str = ""

    for key, val in stream_top_level(text):
        if key == "Start" and act_keys:
            # `Start` invokes a sub-script; if it matches one of our tracked
            # act sub-scripts, every subsequent objective belongs to that act.
            sm = re.match(r'\s*"([^"]+)"', val)
            if sm and sm.group(1) in act_keys:
                current_act_key = sm.group(1)

        if key in ("Objective", "ObjectiveStage"):
            text_line = _parse_objective(val)
            if not text_line:
                continue
            current = {"text": text_line, "battles": [], "rewards": []}
            if current_act_key:
                current["act_key"] = current_act_key
            if pending_poi:
                current["location"] = pending_poi
                pending_poi = None
            steps.append(current)

        elif key == "SetPoi":
            poi = _parse_set_poi(val)
            if poi:
                if current and "location" not in current:
                    current["location"] = poi
                else:
                    pending_poi = poi

        elif key in _BATTLE_STAGE_NAMES and current is not None:
            b = _parse_battle_inline(val)
            if b:
                trainer = entities.get(b["entity_key"]) or b.get("speaker") or b["entity_key"]
                battle_entry = {
                    "trainer": trainer,
                    "team": b["team"],
                    "entity_key": b["entity_key"],
                }
                # Annotate with the opponent's CreateEntity coords so the
                # walkthrough can render a "where to fight" pin per battle.
                ent = entity_locations.get(b["entity_key"])
                if ent and any(ent.get(a) is not None for a in ("x", "y", "z")):
                    battle_entry["x"] = ent.get("x")
                    battle_entry["y"] = ent.get("y")
                    battle_entry["z"] = ent.get("z")
                current["battles"].append(battle_entry)
                current.setdefault("targets", []).append(b["entity_key"])

        elif key in _TARGET_STAGE_NAMES and current is not None:
            # Pull the first quoted identifier — that's the entity key to
            # interact with. Several syntaxes:
            #   "HighlightClickEntity": "key"
            #   "HighlightClickEntity": ["key"]
            #   "HighlightClickEntity": [["key", ...], ...]
            tm = re.search(r'"([A-Za-z_][\w]*)"', val)
            if tm:
                current.setdefault("targets", []).append(tm.group(1))

        elif key in _REGION_STAGE_NAMES and current is not None:
            # Region bbox: [x1, y1, z1, x2, y2, z2]. Capture the full bbox
            # (so the layout can show the region span) and the centre (so
            # the step still has a single "go here" point in the YAML).
            nums = re.findall(r"-?\d+(?:\.\d+)?", val)
            if len(nums) >= 6:
                x1, y1, z1, x2, y2, z2 = (float(n) for n in nums[:6])
                bbox = (
                    min(x1, x2), min(y1, y2), min(z1, z2),
                    max(x1, x2), max(y1, y2), max(z1, z2),
                )
                current.setdefault("region_bboxes", []).append(bbox)
                current.setdefault("fallback_locs", []).append({
                    "x": round((x1 + x2) / 2, 1),
                    "y": round((y1 + y2) / 2, 1),
                    "z": round((z1 + z2) / 2, 1),
                })

        elif key in _COORD_FALLBACK_STAGES and current is not None:
            # Pull the first three numeric tokens — works for both the
            # ["key", x, y, z, ...] (MoveEntity) and [x, y, z, yaw, pitch]
            # (Teleport) shapes.
            nums = re.findall(r"-?\d+(?:\.\d+)?", val)
            if len(nums) >= 3:
                # MoveEntity-style starts with an entity key string before
                # the numbers, but the entity key isn't a number itself, so
                # the regex picks up the right values either way.
                fallback_loc = {
                    "x": float(nums[0]),
                    "y": float(nums[1]),
                    "z": float(nums[2]),
                }
                current.setdefault("fallback_locs", []).append(fallback_loc)

        elif key in _REWARD_STAGE_NAMES:
            r = _parse_reward(key, val)
            if r:
                if current is not None:
                    current["rewards"].append(r)
                else:
                    rewards.append(r)

    # Backfill location for "go to NPC" steps that lack a SetPoi: use the
    # first referenced entity's CreateEntity coords. Skip steps already marked
    # as region-entry — those are "step into the area" objectives, not point
    # destinations.
    # Build name → entity lookup (lowercased single-word display names) so we
    # can match NPC names mentioned in objective text like "Go to Nurse Daisy".
    name_to_entity: dict[str, str] = {}
    for ek, name in entities.items():
        if ek not in entity_locations:
            continue
        for tok in re.findall(r"[A-Za-z]{3,}", name):
            name_to_entity.setdefault(tok.lower(), ek)

    # Classify each step's location:
    #   battle → at least one BattleNpc; per-trainer coords are already in battles[]
    #   region → triggered by RegionEntry/InRegion; emit the bbox span
    #   npc    → talk to a known NPC; emit point coord with NPC label
    #   destination → MoveEntity/Teleport/PickupItem captured a coord
    for s in steps:
        # Tag battle steps so the layout can render them as "battle" rather
        # than emitting a duplicate location pin.
        if s.get("battles"):
            s.setdefault("location", {})  # may stay empty; battles carry coords
            s["location"].setdefault("kind", "battle")

        if s.get("location") and s["location"].get("x") is not None:
            # already a pinned location from SetPoi during streaming
            s["location"].setdefault("kind", "destination")
            continue

        # Try named NPC targets first.
        chosen = None
        for ek in s.get("targets") or []:
            ent = entity_locations.get(ek)
            if not ent or all(ent.get(a) is None for a in ("x", "y", "z")):
                continue
            chosen = {
                "kind": "npc",
                "x": ent.get("x"),
                "y": ent.get("y"),
                "z": ent.get("z"),
                "label": entities.get(ek, ek),
            }
            break
        # Try to match an NPC mentioned by name in the Objective text.
        if not chosen:
            for tok in re.findall(r"[A-Za-z]{3,}", s.get("text", "")):
                ek = name_to_entity.get(tok.lower())
                if not ek:
                    continue
                ent = entity_locations.get(ek)
                if not ent:
                    continue
                chosen = {
                    "kind": "npc",
                    "x": ent.get("x"),
                    "y": ent.get("y"),
                    "z": ent.get("z"),
                    "label": entities.get(ek, ek),
                }
                break
        # Region bbox if any.
        if not chosen and s.get("region_bboxes"):
            bb = s["region_bboxes"][0]
            chosen = {
                "kind": "region",
                "x": round((bb[0] + bb[3]) / 2, 1),
                "y": round((bb[1] + bb[4]) / 2, 1),
                "z": round((bb[2] + bb[5]) / 2, 1),
                "bbox": [bb[0], bb[1], bb[2], bb[3], bb[4], bb[5]],
            }
        # Otherwise Move/Teleport destination.
        if not chosen:
            fbs = s.get("fallback_locs") or []
            if fbs:
                chosen = dict(fbs[-1])
                chosen["kind"] = "destination"
        if chosen:
            # If the step already has a battle-only location placeholder,
            # merge in the chosen coord but keep the battle kind for layout
            # routing (battles already render their own pins).
            existing = s.get("location") or {}
            if existing.get("kind") == "battle":
                # Battle wins — do not overwrite; battles[] carries coords.
                continue
            s["location"] = chosen
    # Town tagging — gen5 (Zeinova) is the only region in prod-map.yml. For
    # other regions, mine the quest's text + start description + per-step
    # objective text for "X Town" / "X City" / etc. and attach the most
    # relevant place name to each step.
    if gen_num != 5:
        # Collect all place names mentioned anywhere in the script — used as
        # the per-quest fallback when a step's text doesn't name one itself.
        quest_wide_places = extract_place_names(text)
        primary_place = quest_wide_places[0] if quest_wide_places else ""
        for s in steps:
            mentions = extract_place_names(s.get("text", ""))
            if mentions:
                s["_text_town"] = mentions[0]
            elif primary_place:
                s["_text_town"] = primary_place

    # Starter-selection consolidation: a step like "Click your preferred
    # starter!" lists 15 GivePokemon stages (one per option) — collapse all
    # those Pokémon-named rewards into a single "Starter Pokémon" line.
    for s in steps:
        if "starter" not in s.get("text", "").lower():
            continue
        rewards = s.get("rewards") or []
        pokemon_rewards = [r for r in rewards if r.startswith("Pokémon:")]
        if len(pokemon_rewards) >= 2:
            non_pokemon = [r for r in rewards if not r.startswith("Pokémon:")]
            s["rewards"] = ["Starter Pokémon"] + non_pokemon

    # Bookkeeping fields aren't useful in YAML — drop.
    for s in steps:
        s.pop("is_region", None)
        s.pop("targets", None)
        s.pop("fallback_locs", None)
        s.pop("region_bboxes", None)

    # Starting NPC: the FIRST entity referenced by a HighlightClickEntity /
    # ClickEntity stage in source order is reliably the quest-giver. Fall
    # back to the first named CreateEntity if no click stage is found.
    start: dict | None = None
    starter_key = ""
    click_re = re.compile(
        r'"(?:HighlightClickEntity|ClickEntity|ClickEntityOptions)"\s*:\s*'
        r'(?:"([A-Za-z_][\w]*)"|\[\s*"([A-Za-z_][\w]*)"|\{\s*"key"\s*:\s*"([A-Za-z_][\w]*)")'
    )
    cm = click_re.search(text)
    if cm:
        starter_key = cm.group(1) or cm.group(2) or cm.group(3) or ""
    if starter_key and starter_key in entity_locations:
        ent = entity_locations[starter_key]
        start = {
            "npc": entities.get(starter_key, starter_key),
            "x": ent.get("x"),
            "y": ent.get("y"),
            "z": ent.get("z"),
        }
    else:
        for ek in create_order:
            ent = entity_locations.get(ek)
            if not ent or not entities.get(ek):
                continue
            start = {
                "npc": entities[ek],
                "x": ent.get("x"),
                "y": ent.get("y"),
                "z": ent.get("z"),
            }
            break
    if start:
        if gen_num == 5:
            start["town"] = town_at(start.get("x"), start.get("y"), start.get("z"))
        else:
            # Pull a place name from the start description / overall text.
            cand = []
            if start_description:
                cand.extend(extract_place_names(start_description))
            cand.extend(extract_place_names(text))
            start["town"] = cand[0] if cand else ""
        if start_description:
            start["description"] = start_description
    elif start_description:
        start = {"description": start_description}

    # Collapse repeated Pokémon-named entries in final_rewards (e.g. the gen5
    # intro lists every starter option as a "final reward" — that's noise).
    pokemon_finals = [r for r in rewards if r.startswith("Pokémon:")]
    if len(pokemon_finals) >= 2:
        rewards = [r for r in rewards if not r.startswith("Pokémon:")]

    return steps, {"final_rewards": rewards, "start": start}


def slug_for(quest: dict) -> str:
    """Filesystem-safe slug for a quest's per-page output. Prefer the raw
    filename stem (matches the source script) over the internal Key, since
    keys can contain capitalization/punctuation that complicates URLs."""
    stem = Path(quest.get("file", "")).stem
    if stem:
        return re.sub(r"[^a-z0-9-]+", "-", stem.lower()).strip("-")
    return re.sub(r"[^a-z0-9-]+", "-", (quest.get("key") or "quest").lower()).strip("-")


# ---------- Topological ordering ----------

def order_quests(quests: list[dict]) -> list[dict]:
    """Return quests sorted so that every quest follows its prereqs.

    Only considers prereqs that point to another quest IN THIS LIST — cross-
    region prereqs (e.g., a gym key) are ignored for ordering purposes. Within
    a level (no remaining unresolved prereqs), ties are broken alphabetically
    by name to keep output deterministic."""
    keys_in = {q["key"] for q in quests if q.get("key")}
    by_key = {q["key"]: q for q in quests if q.get("key")}
    indeg: dict[str, int] = {k: 0 for k in keys_in}
    children: dict[str, list[str]] = {k: [] for k in keys_in}
    for q in quests:
        k = q.get("key")
        if not k:
            continue
        for p in q.get("prereqs", []):
            if p in keys_in and p != k:
                children[p].append(k)
                indeg[k] += 1

    def sort_key(qkey: str):
        """Tiebreaker for quests at the same topological level.

        Goal: the main-story spine (intro → main quest 1 → main quest 2 → ...)
        comes first in numeric order; everything else is alphabetical.

        Priority tiers (lower wins):
          0: gen{N}-intro / gen{N}_intro
          1: gen{N}-main-quest-{n} / gen{N}_main_quest_{n}, ordered by n;
             Elite Four slots in at 7.5 (between MQ7 and MQ8 in gen5,
             after MQ5/MQ7 at the end in gen3/gen4).
          2: anything else, ordered by display name
        """
        q = by_key[qkey]
        k = qkey.lower()
        if "intro" in k:
            return (0, 0, "")
        if re.search(r"elite[_-]?four", k):
            return (1, 7.5, k)
        m = re.search(r"main[-_]quest[-_]?(\d+)", k)
        if m:
            return (1, float(m.group(1)), k)
        return (2, 0.0, q.get("name", "").lower() or qkey)

    ready = sorted([k for k, d in indeg.items() if d == 0], key=sort_key)
    out_keys: list[str] = []
    while ready:
        k = ready.pop(0)
        out_keys.append(k)
        for child in children.get(k, []):
            indeg[child] -= 1
            if indeg[child] == 0:
                # Insert into ready, keeping it sorted by sort_key
                inserted = False
                for i, r in enumerate(ready):
                    if sort_key(child) < sort_key(r):
                        ready.insert(i, child)
                        inserted = True
                        break
                if not inserted:
                    ready.append(child)

    # Any quest left unvisited (cycle, or has a missing intra-list prereq it
    # depends on circularly) — append at the end, alphabetized.
    leftover = sorted([k for k in keys_in if k not in out_keys], key=sort_key)
    out_keys.extend(leftover)
    # Quests with no key at all (unlikely) get appended last
    keyless = [q for q in quests if not q.get("key")]
    return [by_key[k] for k in out_keys] + keyless


# ---------- YAML emission ----------

def yaml_string(value) -> str:
    s = "" if value is None else str(value)
    return "'" + s.replace("'", "''") + "'"


def render_gen_md(gen_label: str, gen_num: int, quests: list[dict]) -> str:
    lines = ["---"]
    lines.append(f"title: {yaml_string(gen_label)}")
    lines.append(f"date: {date.today().isoformat()}")
    # Override the default quests/single.html (editorial-writeup template) with
    # the auto-generated questlog template that knows how to render quests[].
    lines.append("layout: questlog")
    lines.append(f"gen: {gen_num}")
    lines.append("quests:")
    for q in order_quests(quests):
        lines.append(f"  - key: {yaml_string(q.get('key', ''))}")
        lines.append(f"    slug: {yaml_string(slug_for(q))}")
        lines.append(f"    name: {yaml_string(q.get('name', ''))}")
        if q.get("description"):
            lines.append(f"    description: {yaml_string(q['description'])}")
        if q.get("author"):
            lines.append(f"    author: {yaml_string(q['author'])}")
        lines.append(f"    file: {yaml_string(q.get('file', ''))}")
    lines.append("---\n")
    return "\n".join(lines)


def render_quest_md(gen_num: int, quest: dict, source_path: Path,
                    videos: list[tuple[str, str]] | None = None) -> str:
    """Per-quest walkthrough page. Emits an ordered list of steps in
    frontmatter for the questguide layout to render."""
    text = source_path.read_text(errors="replace")

    # Quests split across a main + act files: pre-collect entities from acts
    # so the main file's objective steps can resolve NPCs defined elsewhere.
    extras = EXTRA_SCRIPTS.get(quest.get("key", "")) or []
    extra_entities: dict[str, dict] = {}
    for fname in extras:
        extra_path = source_path.parent / fname
        if not extra_path.exists():
            continue
        try:
            extra_entities.update(collect_entities(extra_path.read_text(errors="replace")))
        except Exception as e:
            print(f"  fail entities {fname}: {e}", file=sys.stderr)

    act_video_map = ACT_VIDEOS.get(quest.get("key", ""), {})
    steps, meta = extract_walkthrough(text, gen_num, extra_entities or None,
                                      set(act_video_map.keys()) if act_video_map else None)

    # Append walkthrough steps from extra scripts (only if they have their
    # own Objectives — most acts run cinematics under the main's objectives).
    for fname in extras:
        extra_path = source_path.parent / fname
        if not extra_path.exists():
            continue
        try:
            extra_text = extra_path.read_text(errors="replace")
            extra_steps, _ = extract_walkthrough(extra_text, gen_num, extra_entities)
            steps.extend(extra_steps)
        except Exception as e:
            print(f"  fail extra {fname}: {e}", file=sys.stderr)

    lines = ["---"]
    lines.append(f"title: {yaml_string(quest.get('name', '') or quest.get('key', ''))}")
    lines.append(f"date: {date.today().isoformat()}")
    lines.append("layout: questguide")
    lines.append(f"gen: {gen_num}")
    lines.append(f"quest_key: {yaml_string(quest.get('key', ''))}")
    lines.append(f"slug: {yaml_string(slug_for(quest))}")
    if quest.get("description"):
        lines.append(f"description: {yaml_string(quest['description'])}")
    if quest.get("author"):
        lines.append(f"author: {yaml_string(quest['author'])}")
    lines.append(f"source_file: {yaml_string(quest.get('file', ''))}")

    if videos:
        # Hard override for quests where fuzzy matching can't help (titles
        # consisting only of stopwords, or known mis-matches).
        match = VIDEO_OVERRIDES.get(quest.get("key", ""))
        if not match:
            match = match_video_for_quest(quest.get("name", "") or quest.get("key", ""),
                                          gen_num, videos)
        if match:
            lines.append(f"video_id: {yaml_string(match[0])}")
            lines.append(f"video_title: {yaml_string(match[1])}")

    # gen5 intro: starts automatically when the player joins the region — no
    # quest-giver NPC, and the auto-detected starter Pokémon shouldn't appear
    # as the "start" entry. Also clear the noisy final_rewards bucket.
    if quest.get("key") == "gen5_intro":
        meta["final_rewards"] = []
        meta["start"] = {"description": "Triggers automatically when you arrive in Findale Harbor — no NPC required."}

    start = meta.get("start")
    if start:
        lines.append("start:")
        if start.get("npc"):
            lines.append(f"  npc: {yaml_string(start['npc'])}")
        if start.get("description"):
            lines.append(f"  description: {yaml_string(start['description'])}")
        if start.get("town"):
            lines.append(f"  town: {yaml_string(start['town'])}")
        if any(start.get(a) is not None for a in ("x", "y", "z")):
            # YAML 1.1 (used by Hugo) reads bare `y` as a boolean true. Quote
            # the key so the template can address it as `.y`.
            lines.append(f"  x: {start.get('x', 0) or 0}")
            lines.append(f"  \"y\": {start.get('y', 0) or 0}")
            lines.append(f"  z: {start.get('z', 0) or 0}")
    if meta.get("final_rewards"):
        lines.append("final_rewards:")
        for r in meta["final_rewards"]:
            lines.append(f"  - {yaml_string(r)}")

    if steps:
        lines.append("steps:")
        last_act_key = None
        for s in steps:
            ak = s.get("act_key", "")
            lines.append(f"  - text: {yaml_string(s['text'])}")
            # Tag the first step of each act with the act number + video so
            # the layout can render an act-divider header before that step.
            if ak and ak != last_act_key:
                act_num_m = re.search(r"act(\d+)$", ak)
                if act_num_m:
                    lines.append(f"    act: {int(act_num_m.group(1))}")
                vid_pair = act_video_map.get(ak)
                if vid_pair:
                    lines.append(f"    act_video_id: {yaml_string(vid_pair[0])}")
                    lines.append(f"    act_video_title: {yaml_string(vid_pair[1])}")
                last_act_key = ak
            loc = s.get("location")
            if loc and (loc.get("x") is not None or loc.get("kind") == "battle"):
                lines.append("    location:")
                if loc.get("kind"):
                    lines.append(f"      kind: {yaml_string(loc['kind'])}")
                if loc.get("x") is not None:
                    lines.append(f"      x: {loc.get('x') if loc.get('x') is not None else 0}")
                    lines.append(f"      \"y\": {loc.get('y') if loc.get('y') is not None else 0}")
                    lines.append(f"      z: {loc.get('z') if loc.get('z') is not None else 0}")
                if loc.get("label"):
                    lines.append(f"      label: {yaml_string(loc['label'])}")
                if loc.get("bbox"):
                    bb = loc["bbox"]
                    lines.append("      bbox:")
                    lines.append(f"        x1: {bb[0]}")
                    lines.append(f"        \"y1\": {bb[1]}")
                    lines.append(f"        z1: {bb[2]}")
                    lines.append(f"        x2: {bb[3]}")
                    lines.append(f"        \"y2\": {bb[4]}")
                    lines.append(f"        z2: {bb[5]}")
                # gen5 → bbox lookup against prod-map; other gens → text-derived.
                town = ""
                if gen_num == 5:
                    town = town_at(loc.get('x'), loc.get('y'), loc.get('z'))
                else:
                    town = s.get("_text_town", "")
                if town:
                    lines.append(f"      town: {yaml_string(town)}")
            if s.get("battles"):
                lines.append("    battles:")
                for b in s["battles"]:
                    lines.append(f"      - trainer: {yaml_string(b.get('trainer') or '')}")
                    if any(b.get(a) is not None for a in ("x", "y", "z")):
                        lines.append(f"        x: {b.get('x', 0) or 0}")
                        lines.append(f"        \"y\": {b.get('y', 0) or 0}")
                        lines.append(f"        z: {b.get('z', 0) or 0}")
                        t = town_at(b.get("x"), b.get("y"), b.get("z")) if gen_num == 5 else s.get("_text_town", "")
                        if t:
                            lines.append(f"        town: {yaml_string(t)}")
                    if b.get("team"):
                        lines.append("        team:")
                        for p in b["team"]:
                            lines.append(f"          - species: {yaml_string(p.get('species', ''))}")
                            if p.get("level") is not None:
                                lines.append(f"            level: {p['level']}")
            if s.get("rewards"):
                lines.append("    rewards:")
                for r in s["rewards"]:
                    lines.append(f"      - {yaml_string(r)}")
    lines.append("---\n")
    return "\n".join(lines)


# ---------- Main ----------

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    videos = load_youtube_videos()
    print(f"Loaded {len(videos)} cached YouTube videos for matching",
          file=sys.stderr)
    summary = []
    for gen in (1, 2, 3, 4, 5):
        gen_dir = QUESTS_ROOT / f"gen{gen}"
        if not gen_dir.exists():
            print(f"Missing: {gen_dir}", file=sys.stderr)
            continue

        quests: list[dict] = []
        sources: dict[str, Path] = {}   # keyed by source filename (unique)
        skipped_seasonal = 0
        for jf in sorted(gen_dir.glob("*.json")):
            if is_seasonal(jf.stem):
                try:
                    if is_logged_quest(jf.read_text(errors="replace")):
                        skipped_seasonal += 1
                except Exception:
                    pass
                continue
            try:
                q = extract_quest(jf)
                if q:
                    quests.append(q)
                    sources[jf.name] = jf
            except Exception as e:
                print(f"  fail {jf.name}: {e}", file=sys.stderr)

        # Generation tab page (lists all quests with clickable links)
        out_path = OUT_DIR / f"gen{gen}.md"
        out_path.write_text(render_gen_md(f"Gen {gen}", gen, quests), encoding="utf-8")

        # Per-quest walkthrough pages
        per_quest_dir = OUT_DIR / f"gen{gen}"
        per_quest_dir.mkdir(parents=True, exist_ok=True)
        steps_total = 0
        for q in quests:
            src = sources.get(q.get("file", ""))
            if not src:
                continue
            try:
                md = render_quest_md(gen, q, src, videos)
                slug = slug_for(q)
                (per_quest_dir / f"{slug}.md").write_text(md, encoding="utf-8")
                steps_total += md.count("- text:")
            except Exception as e:
                print(f"  fail walkthrough {q.get('file')}: {e}", file=sys.stderr)

        summary.append((gen, len(quests), skipped_seasonal, steps_total))

    print("Gen | quests | seasonal | walkthrough steps")
    for gen, kept, skipped, steps in summary:
        print(f"  Gen {gen}:  {kept:3d} quests, {skipped:3d} seasonal, {steps:5d} steps")
    return 0


if __name__ == "__main__":
    sys.exit(main())
