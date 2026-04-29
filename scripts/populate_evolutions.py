#!/usr/bin/env python3
"""Inject full evolution-family trees into pokedex markdown frontmatter.

Source of truth: `PokemonWorld-master/.../resources/data/evolutions.json`
(384 entries — `species`, `to`, `trigger`, `level`, `item`, `held_item`,
`gender`, `time_of_day`, `known_move`, `party_species`, `location`,
`relative_physical_stats`, `happiness`, etc.).

For every species we compute the *entire* connected evolution component
and write it as a flat, depth-annotated `evolution_family` list ordered
by DFS from the family's root. Charmander, Charmeleon, and Charizard all
end up with the same three-entry list; Eevee and every Eeveelution all
get the same eight-entry tree (Eevee + 7 children). The layout template
indents each row by `depth` and highlights the current species.

Each entry shape:
  - species: 'Charmeleon'
    slug:    'charmeleon'
    depth:   1
    method:  'Level 16'    # trigger from immediate parent (root has '')

Entries whose species lacks a wiki page (mostly gen 6+, server-original
Pokémon like Fafnir/Vixen/Cloud, and yet-unpopulated regional forms) are
omitted from the family — they'll come back automatically once their
pages exist.

Re-run any time the source JSON changes:
    python3 scripts/populate_evolutions.py
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVOL_JSON = (Path("/home/jack/ClaudeProjects/PokemonWorld-master/pokemon-world-core")
             / "src/main/resources/data/evolutions.json")
POKEDEX_DIR = ROOT / "content/pokedex"


def normalize(name: str) -> str:
    """Slug-friendly key. Strips diacritics, lowercases, and replaces any
    non-alphanumeric run with a hyphen — matches how the wiki computes
    its filenames."""
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def build_name_to_slug() -> dict[str, str]:
    """Map every wiki page's title (and stem) to its filename stem."""
    out: dict[str, str] = {}
    for md in POKEDEX_DIR.glob("*.md"):
        text = md.read_text()
        m = re.search(r"^title:\s*'?([^'\n]+?)'?\s*$", text, re.M)
        if m:
            out[normalize(m.group(1))] = md.stem
        out[md.stem] = md.stem
    return out


def format_method(e: dict) -> str:
    """Compact human-readable summary of a single evolution trigger."""
    parts: list[str] = []
    trigger = e.get("trigger", "")
    level = e.get("level")
    if trigger == "level_up":
        parts.append(f"Level {level}" if level else "Level up")
    elif trigger == "use_item":
        parts.append(f"Use {e['item']}" if e.get("item") else "Use item")
    elif trigger == "trade":
        parts.append("Trade")
    elif trigger == "shed":
        parts.append("Shed")
    elif trigger:
        parts.append(trigger.replace("_", " ").title())

    if e.get("held_item"):
        parts.append(f"holding {e['held_item']}")
    if e.get("known_move"):
        parts.append(f"knowing {e['known_move']}")
    if e.get("known_move_type"):
        parts.append(f"knowing a {e['known_move_type']}-type move")
    if e.get("gender"):
        parts.append(f"({e['gender']})")
    if e.get("time_of_day"):
        parts.append(f"at {e['time_of_day']}")
    if e.get("raining"):
        parts.append("while raining")
    if e.get("party_species"):
        parts.append(f"with {e['party_species']} in party")
    if e.get("party_type"):
        parts.append(f"with a {e['party_type']}-type Pokémon in party")
    if e.get("trade_species"):
        parts.append(f"trade for {e['trade_species']}")
    # Tyrogue → Hitmontop is encoded as the *absence* of a
    # relative_physical_stats override (the default 0), with the sibling
    # branches Tyrogue → Hitmonlee (+1) and Tyrogue → Hitmonchan (-1)
    # supplying the discriminator. The pre-pass in `main()` flags such
    # entries with the synthetic `_atk_def_equal` key so we render the
    # right text instead of silently dropping the condition.
    if e.get("_atk_def_equal"):
        parts.append("Atk = Def")
    else:
        rps = e.get("relative_physical_stats")
        try:
            v = int(rps) if rps not in ("", None) else 0
        except (TypeError, ValueError):
            v = 0
        if v > 0:
            parts.append("Atk > Def")
        elif v < 0:
            parts.append("Def > Atk")
    if e.get("happiness"):
        parts.append("high friendship")
    if e.get("beauty"):
        parts.append("high beauty")
    if e.get("affection"):
        parts.append("high affection")
    if e.get("location"):
        parts.append(f"near {e['location']}")
    return ", ".join(parts) or trigger.replace("_", " ").title()


def yaml_quote(s: str) -> str:
    """Single-quote a string for inline YAML, escaping any embedded
    single quotes by doubling them (the YAML 1.1 convention)."""
    return "'" + str(s).replace("'", "''") + "'"


def render_evo_block(entries: list[dict]) -> str:
    """Render the `evolution_family:` block as YAML lines for the
    form-level frontmatter (4-space indent matching surrounding fields)."""
    if not entries:
        return ""
    out = ["    evolution_family:"]
    for e in entries:
        out.append(f"      - species: {yaml_quote(e['species'])}")
        out.append(f"        slug: {yaml_quote(e['slug'])}")
        out.append(f"        depth: {e['depth']}")
        out.append(f"        method: {yaml_quote(e['method'])}")
    return "\n".join(out) + "\n"


def remove_existing_evo_blocks(form_block: str) -> str:
    """Strip any pre-existing evolution YAML blocks (legacy `evolves_to:` /
    `evolves_from:` and the new `evolution_family:`) from a form-level
    block. Catches both shapes so re-running cleanly replaces older
    output rather than appending."""
    return re.sub(
        r"^    (?:evolves_to|evolves_from|evolution_family):\n(?:      .*\n)*",
        "",
        form_block,
        flags=re.M,
    )


def build_family(start: str, edges_to: dict[str, list[dict]],
                 reverse: dict[str, list[str]]) -> list[dict]:
    """Compute the full DFS-ordered evolution tree containing `start`.

    Walks both directions of the evolution graph (treating it as
    undirected for connectivity), finds the component's root (no incoming
    edges from within the component), then DFS-traverses out from the
    root annotating each node with its depth and the trigger method
    inherited from its parent."""
    # 1) Find every member of the connected component (BFS, undirected).
    members: set[str] = set()
    queue: list[str] = [start]
    while queue:
        slug = queue.pop()
        if slug in members:
            continue
        members.add(slug)
        for child in edges_to.get(slug, []):
            queue.append(child["slug"])
        for parent in reverse.get(slug, []):
            queue.append(parent)
    # 2) Pick a root: a node in the component with no incoming edges from
    #    within the component. Multiple roots are unusual but possible —
    #    fall back alphabetically.
    roots = sorted(
        m for m in members
        if not any(p in members for p in reverse.get(m, []))
    )
    if not roots:
        roots = sorted(members)
    root = roots[0]
    # 3) DFS, annotating each node with depth + method from its parent.
    out: list[dict] = []
    visited: set[str] = set()

    def visit(slug: str, parent_slug: str | None, depth: int, method: str):
        if slug in visited:
            return
        visited.add(slug)
        # Find the canonical display name from any in-edge or out-edge.
        name = None
        for entry in edges_to.get(slug, []):
            # When this slug was a *source*, its display name lives on
            # the `from_species` we recorded into reverse — fall through.
            pass
        for entry in edges_to.get(parent_slug, []) if parent_slug else []:
            if entry["slug"] == slug:
                name = entry["species"]
                break
        if name is None:
            # Root or no parent edge — pick a name from any out-edge target,
            # or fall back to the slug.
            for entry in edges_to.get(slug, []):
                # Prefer the source species's own name from `from_names[slug]`
                pass
            name = display_names.get(slug) or slug.replace("-", " ").title()
        out.append({
            "species": name,
            "slug":    slug,
            "depth":   depth,
            "method":  method,
        })
        # Visit children (out-edges) in their declared order.
        for child in edges_to.get(slug, []):
            if child["slug"] not in visited and child["slug"] in members:
                visit(child["slug"], slug, depth + 1, child["method"])

    # Expose `display_names` to the inner function via closure.
    visit(root, None, 0, "")
    # 4) If any members weren't reached (disconnected sub-trees / cycles),
    #    append them at depth 0 with no method so we never silently lose
    #    a Pokémon from its own family page.
    for m in sorted(members - visited):
        out.append({
            "species": display_names.get(m) or m.replace("-", " ").title(),
            "slug":    m,
            "depth":   0,
            "method":  "",
        })
    return out


# Module-level — populated in `main()` and read by `build_family`.
display_names: dict[str, str] = {}


def main() -> int:
    if not EVOL_JSON.exists():
        print(f"missing: {EVOL_JSON}", file=sys.stderr)
        return 1
    raw = json.loads(EVOL_JSON.read_text())
    name_to_slug = build_name_to_slug()

    def slug_of(name: str) -> str | None:
        return name_to_slug.get(normalize(name))

    # Pre-pass: detect "Atk == Def" branches. The source JSON encodes
    # Tyrogue → Hitmontop as a level-up entry without an explicit
    # `relative_physical_stats` value (it defaults to 0); meaning is
    # only inferable from the sibling branches Tyrogue → Hitmonlee (+1)
    # and Tyrogue → Hitmonchan (-1). For every source species whose
    # evolutions split on a non-zero rps value, mark the matching
    # zero-or-missing rps entry as the equal-stats path.
    def rps_int(e):
        v = e.get("relative_physical_stats")
        if v in ("", None):
            return 0
        try:
            return int(v)
        except (TypeError, ValueError):
            return 0
    by_source: dict[str, list[dict]] = {}
    for e in raw:
        by_source.setdefault(e.get("species", ""), []).append(e)
    for entries in by_source.values():
        if any(rps_int(e) != 0 for e in entries):
            for e in entries:
                if rps_int(e) == 0:
                    e["_atk_def_equal"] = True

    # Build the evolution graph (out-edges + reverse adjacency for
    # connectivity walking). Skip entries where either side has no wiki
    # page — those would dangle as broken links in the rendered family.
    edges_to: dict[str, list[dict]] = {}
    reverse: dict[str, list[str]] = {}
    global display_names
    skipped = 0
    for e in raw:
        s_name = e.get("species") or ""
        t_name = e.get("to") or ""
        s_slug = slug_of(s_name)
        t_slug = slug_of(t_name)
        if not s_slug or not t_slug:
            skipped += 1
            continue
        method = format_method(e)
        edges_to.setdefault(s_slug, []).append(
            {"species": t_name, "slug": t_slug, "method": method})
        reverse.setdefault(t_slug, []).append(s_slug)
        # Record canonical display names for both sides — used by
        # `build_family` when emitting nodes that have no incoming edge
        # in the slice.
        display_names.setdefault(s_slug, s_name)
        display_names.setdefault(t_slug, t_name)

    # Compute one family tree per connected component, share it across
    # every member's page.
    species_with_pages = set(edges_to) | set(reverse)
    families: dict[str, list[dict]] = {}     # slug -> family list
    for slug in species_with_pages:
        if slug in families:
            continue
        family = build_family(slug, edges_to, reverse)
        for entry in family:
            families[entry["slug"]] = family

    # Sanity stats for the report.
    component_sizes = {}
    for slug, fam in families.items():
        component_sizes.setdefault(id(fam), len(fam))
    sizes_hist = sorted(component_sizes.values())

    written = 0
    skipped_no_form = 0
    for slug in sorted(families):
        md = POKEDEX_DIR / f"{slug}.md"
        if not md.exists():
            continue
        text = md.read_text()
        m = re.search(r"^  - name: '[^']+'\n((?:    [^\n]*\n)*)", text, re.M)
        if not m:
            skipped_no_form += 1
            continue
        block_start, block_end = m.start(), m.end()
        form_block = m.group(0)
        cleaned = remove_existing_evo_blocks(form_block)
        new_block = cleaned + render_evo_block(families[slug])
        if new_block == form_block:
            continue
        md.write_text(text[:block_start] + new_block + text[block_end:])
        written += 1

    print(f"Source entries:       {len(raw)}")
    print(f"Skipped (no wiki page on either end): {skipped}")
    print(f"Connected families:   {len(set(id(f) for f in families.values()))}")
    print(f"Family-size histogram: min={min(sizes_hist) if sizes_hist else 0}, "
          f"max={max(sizes_hist) if sizes_hist else 0}")
    print(f"Markdown files updated: {written}")
    if skipped_no_form:
        print(f"  pages with no form block:  {skipped_no_form}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
