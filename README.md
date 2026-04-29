# Pokéfind Companion

Static reference wiki for the Pokéfind Minecraft server, built with Hugo and
deployed to Cloudflare Pages. Companion to the WarriorToxic YouTube channel.

## Local development

Requires Hugo extended ≥ 0.123.

```bash
hugo server          # local dev server with live reload at :1313
hugo --minify        # production build → public/
```

## Cloudflare Pages build settings

| Setting | Value |
|---|---|
| Framework preset | Hugo |
| Build command | `hugo --minify` |
| Build output directory | `public` |
| Environment variable | `HUGO_VERSION = 0.123.7` |

## Updating content

The `content/` tree is a mix of editorial markdown and auto-generated pages
produced by the Python scripts in `scripts/`. The scripts read from local
data sources (the server's quest JSON exports, the resource pack, etc.) and
emit markdown into `content/`. Re-run them when the underlying data changes:

```bash
python3 scripts/ingest_pokédex.py        # rebuild Pokédex from species.json
python3 scripts/build_pokédex_extras.py  # spawn-region towns + Smogon sets
python3 scripts/populate_moves.py        # Moves & Abilities tab
python3 scripts/build_questlog.py        # Quest log + per-quest walkthroughs
python3 scripts/build_gym_teams.py       # Gym leader / Elite Four rosters
python3 scripts/build_skins.py           # Skin variants from the resource pack
python3 scripts/fetch_youtube_videos.py  # Refresh the YouTube video cache
```

Generated markdown is committed so Cloudflare Pages can build without
needing the source data.

## Project layout

```
content/   markdown pages (mostly auto-generated, some editorial)
layouts/   Hugo templates per section
static/    CSS, JS, images
scripts/   Python build scripts + cached data files
hugo.toml  site config
```
