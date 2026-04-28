#!/usr/bin/env python3
"""
Walk the WarriorToxic channel's uploads playlist and dump every video as
TSV (videoId<TAB>title) to scripts/youtube_videos.tsv.

Strategy: load the public playlist page (uploads playlist = UC channel id
with the UC prefix swapped to UU), extract the initial 100 videos and the
continuation token, then POST to /youtubei/v1/browse to paginate through
the rest until no more continuation token is returned.

Re-run this whenever the user wants a fresh video list. The output file is
checked into the wiki and consumed by build_questlog.py.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from pathlib import Path

CHANNEL_ID = "UCafGqNUr5lkGEnYql5QCNjQ"
UPLOADS_ID = "UU" + CHANNEL_ID[2:]
PLAYLIST_URL = f"https://www.youtube.com/playlist?list={UPLOADS_ID}"
BROWSE_URL = "https://www.youtube.com/youtubei/v1/browse"

WIKI_ROOT = Path(__file__).resolve().parent.parent
OUT_TSV = WIKI_ROOT / "scripts/youtube_videos.tsv"

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"


def http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def http_post_json(url: str, body: dict, headers: dict) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    for k, v in headers.items():
        req.add_header(k, v)
    req.add_header("User-Agent", UA)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def extract_videos_positional(text: str) -> list[tuple[str, str]]:
    """Extract (videoId, title) pairs by walking forward through the text:
    every videoId picks up the next title that follows it."""
    # YouTube's web embeds use compact JSON ("key":"v"); the API returns
    # indented JSON ("key": "v"). Allow optional whitespace around the colon.
    ids = [(m.start(), m.group(1)) for m in re.finditer(
        r'"videoId"\s*:\s*"([A-Za-z0-9_-]{11})"', text)]
    titles = [(m.start(), m.group(1)) for m in re.finditer(
        r'"title"\s*:\s*\{\s*"runs"\s*:\s*\[\s*\{\s*"text"\s*:\s*"((?:[^"\\]|\\.)+)"', text)]
    titles += [(m.start(), m.group(1)) for m in re.finditer(
        r'"title"\s*:\s*\{\s*"simpleText"\s*:\s*"((?:[^"\\]|\\.)+)"', text)]
    titles.sort()
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    t_iter = iter(titles)
    titles_remaining = list(titles)
    for id_pos, vid in ids:
        if vid in seen:
            continue
        # Find first title with position > id_pos
        nearest = None
        for t_pos, t_text in titles_remaining:
            if t_pos > id_pos:
                nearest = (t_pos, t_text)
                break
        if nearest:
            title = nearest[1].encode().decode("unicode_escape", errors="replace")
            out.append((vid, title))
            seen.add(vid)
    return out


def extract_initial(text: str) -> tuple[list[tuple[str, str]], dict, dict, str]:
    """Return (videos, ytcfg, context, continuation_token)."""
    videos = extract_videos_positional(text)
    api_key_m = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', text)
    client_name_m = re.search(r'"INNERTUBE_CLIENT_NAME":"([^"]+)"', text)
    client_ver_m = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', text)
    cont_m = re.search(r'"continuationCommand":\{"token":"([^"]+)"', text)
    ytcfg = {
        "api_key": api_key_m.group(1) if api_key_m else "",
        "client_name": client_name_m.group(1) if client_name_m else "WEB",
        "client_version": client_ver_m.group(1) if client_ver_m else "2.20240101.00.00",
    }
    context = {
        "client": {
            "clientName": ytcfg["client_name"],
            "clientVersion": ytcfg["client_version"],
            "hl": "en",
            "gl": "US",
        },
    }
    return videos, ytcfg, context, (cont_m.group(1) if cont_m else "")


def fetch_continuation(token: str, ytcfg: dict, context: dict) -> tuple[list[tuple[str, str]], str]:
    body = {
        "context": context,
        "continuation": token,
    }
    url = f"{BROWSE_URL}?key={ytcfg['api_key']}"
    headers = {
        "X-YouTube-Client-Name": "1",
        "X-YouTube-Client-Version": ytcfg["client_version"],
        "Origin": "https://www.youtube.com",
        "Referer": PLAYLIST_URL,
    }
    data = http_post_json(url, body, headers)
    raw = json.dumps(data, ensure_ascii=False)
    videos = extract_videos_positional(raw)
    next_token = ""
    cm = re.search(r'"continuationCommand":\{"token":"([^"]+)"', raw)
    if cm:
        next_token = cm.group(1)
    return videos, next_token


def main() -> int:
    print(f"Fetching {PLAYLIST_URL}", file=sys.stderr)
    html = http_get(PLAYLIST_URL)
    videos, ytcfg, context, token = extract_initial(html)
    print(f"  initial: {len(videos)} videos; api_key={ytcfg['api_key'][:10]}…  next_token={'yes' if token else 'no'}",
          file=sys.stderr)

    seen = {v: t for v, t in videos}
    page = 1
    while token and page < 50:
        time.sleep(0.5)
        page += 1
        try:
            new_videos, token = fetch_continuation(token, ytcfg, context)
        except Exception as e:
            print(f"  page {page}: {e}", file=sys.stderr)
            break
        added = 0
        for v, t in new_videos:
            if v not in seen:
                seen[v] = t
                added += 1
        print(f"  page {page}: +{added} videos (total {len(seen)})", file=sys.stderr)
        if added == 0:
            break

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TSV.open("w", encoding="utf-8") as f:
        for vid, title in seen.items():
            f.write(f"{vid}\t{title}\n")
    print(f"Wrote {len(seen)} videos → {OUT_TSV}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
