#!/usr/bin/env python3
"""Fetch public-domain photographs from the NASA Image and Video Library.

  python3 tools/fetch_photos.py --search "space shuttle launch"   # list candidates
  python3 tools/fetch_photos.py                                    # download everything in photo_list.json
  python3 tools/fetch_photos.py --only key1,key2 --force

photo_list.json:  { "key": {"id": "NASA_ID"} | {"q": "query", "pick": 0}, ... }
Images are resized (max 1500 px), saved as figures/photos/<key>.jpg; credits go to figures/photos/credits.json.
"""
import argparse
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "figures/photos"
LIST = ROOT / "figures/photo_list.json"
CRED = PHOTOS / "credits.json"
API = "https://images-api.nasa.gov"
UA = {"User-Agent": "aerospace-manual-builder/1.0 (educational reference manual)"}


def get(url, tries=4):
    url = url.replace("http://", "https://")
    sp = urllib.parse.urlsplit(url)
    url = urllib.parse.urlunsplit((sp.scheme, sp.netloc, urllib.parse.quote(sp.path), sp.query, sp.fragment))
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            if k == tries - 1:
                raise
            time.sleep(2 ** (k + 1))
            print("   retry", url, e, file=sys.stderr)


def search(q, n=15, year_start=None):
    params = {"q": q, "media_type": "image"}
    if year_start:
        params["year_start"] = str(year_start)
    data = json.loads(get(f"{API}/search?{urllib.parse.urlencode(params)}"))
    items = data["collection"]["items"][:n]
    out = []
    for it in items:
        d = it["data"][0]
        out.append({"id": d.get("nasa_id"), "title": d.get("title", ""), "center": d.get("center", ""),
                    "date": d.get("date_created", "")[:10], "photographer": d.get("photographer", ""),
                    "desc": (d.get("description", "") or "")[:200]})
    return out


def meta_for(nasa_id):
    data = json.loads(get(f"{API}/search?{urllib.parse.urlencode({'nasa_id': nasa_id})}"))
    items = data["collection"]["items"]
    if not items:
        return {}
    d = items[0]["data"][0]
    return d


def best_asset(nasa_id):
    data = json.loads(get(f"{API}/asset/{nasa_id}"))
    hrefs = [i["href"] for i in data["collection"]["items"]]
    for suf in ("~large.jpg", "~orig.jpg", "~medium.jpg", "~large.png", "~orig.png", "~orig.tif", "~small.jpg"):
        for h in hrefs:
            if h.lower().endswith(suf.lower()):
                return h
    for h in hrefs:
        if h.lower().endswith((".jpg", ".jpeg", ".png")):
            return h
    return None


def process(key, spec, credits, force=False):
    out = PHOTOS / f"{key}.jpg"
    if out.exists() and not force and key in credits:
        return
    nasa_id = spec.get("id")
    if not nasa_id:
        res = search(spec["q"], n=30, year_start=spec.get("year"))
        must = [m.lower() for m in spec.get("must", [])]
        res = [r for r in res if all(m in (r["title"] + " " + r["desc"]).lower() for m in must)] or res
        if not res:
            print(f"!! {key}: no results for {spec['q']}")
            return
        nasa_id = res[min(spec.get("pick", 0), len(res) - 1)]["id"]
    href = best_asset(nasa_id)
    if not href:
        print(f"!! {key}: no asset for {nasa_id}")
        return
    raw = get(href)
    im = Image.open(io.BytesIO(raw))
    im = im.convert("RGB")
    if spec.get("crop"):
        l, t, r, b = spec["crop"]          # fractions
        W, H = im.size
        im = im.crop((int(l * W), int(t * H), int(r * W), int(b * H)))
    maxd = spec.get("max", 1500)
    im.thumbnail((maxd, maxd), Image.LANCZOS)
    im.save(out, "JPEG", quality=spec.get("q_jpeg", 78), optimize=True, progressive=True)
    d = meta_for(nasa_id)
    center = d.get("center", "")
    who = d.get("photographer") or d.get("secondary_creator") or ""
    credit = "Image: NASA" + (f"/{center}" if center and center not in ("HQ",) else "")
    if who and len(who) < 60:
        credit += f" ({who})"
    credits[key] = {"nasa_id": nasa_id, "title": d.get("title", ""), "date": d.get("date_created", "")[:10],
                    "center": center, "credit": credit, "source": f"https://images.nasa.gov/details/{nasa_id}",
                    "desc": (d.get("description", "") or "")[:300]}
    print(f"ok {key:24s} {nasa_id:30s} {im.size} {out.stat().st_size // 1024} KB  {d.get('title', '')[:60]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--search")
    ap.add_argument("--year", type=int)
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.search:
        for r in search(a.search, n=20, year_start=a.year):
            print(f"{r['id']:34s} {r['date']} {r['center']:5s} {r['title'][:80]}")
        return
    PHOTOS.mkdir(parents=True, exist_ok=True)
    spec = json.loads(LIST.read_text())
    credits = json.loads(CRED.read_text()) if CRED.exists() else {}
    only = set(x for x in a.only.split(",") if x)
    for key, s in spec.items():
        if only and key not in only:
            continue
        try:
            process(key, s, credits, force=a.force or bool(only))
        except Exception as e:  # noqa: BLE001
            print(f"!! {key}: {e}")
        CRED.write_text(json.dumps(credits, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
