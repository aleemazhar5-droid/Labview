#!/usr/bin/env python3
"""Generate the data-driven appendix sections.

  python3 tools/make_appendices.py launches   -> src/appendix_data/E-launches.md  (GCAT launch tables)
  python3 tools/make_appendices.py credits    -> src/chapters/J-image-credits.md  (from credits.json + usage)
  python3 tools/make_appendices.py acronyms   -> src/chapters/G-acronyms.md       (extracted + appendix_data/G-acronyms-extra.tsv)
  python3 tools/make_appendices.py index      -> src/index_terms.txt              (glossary headwords + appendix_data/index-extra.txt)

Launch data: Jonathan McDowell's GCAT (planet4589.org/space/gcat, CC-BY 4.0), raw TSVs in data/raw.
"""
import collections
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw"
SRC = ROOT / "src"


def load(name):
    with open(RAW / name, encoding="utf-8", errors="replace") as f:
        hdr = f.readline().lstrip("#").rstrip("\n").split("\t")
        rows = []
        for r in csv.reader(f, delimiter="\t"):
            if not r or r[0].startswith("#"):
                continue
            rows.append({h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(hdr)})
    return rows


def esc(s):
    return s.replace("|", "/")


# ---------------------------------------------------------------- launch tables
GROUPS = {"US": "USA", "SU": "USSR/Russia", "RU": "USSR/Russia", "CN": "China", "F": "Europe",
          "I-ESA": "Europe", "I-ARIANE": "Europe", "J": "Japan", "IN": "India", "KZ": "USSR/Russia"}
COLS = ["USA", "USSR/Russia", "China", "Europe", "Japan", "India", "Other"]
SITE_EN = {"Baykonur": "Baikonur", "Canaveral": "Cape Canaveral", "Kennedy": "Kennedy Space Center",
           "Vostochniy": "Vostochny", "Kirimati": "Pacific Ocean (Sea Launch)", "Huang Hai": "Yellow Sea (sea launch)",
           "Hainan CLS": "Hainan commercial site (Wenchang)", "Pt Arguello": "Point Arguello", "Kagoshima": "Uchinoura (Kagoshima)",
           "Wallops MARS": "Wallops (MARS)", "Wallops I": "Wallops Island", "Mahia": "Mahia (Rocket Lab LC-1)"}
RENAME = [("Chang Zheng", "Long March"), ("Kuaizhou", "Kuaizhou"), ("Zhuque", "Zhuque")]


def family(lv):
    lv = lv.strip()
    for a, b in RENAME:
        lv = lv.replace(a, b)
    m = re.match(r"(Long March \d+)", lv)
    if m:
        return m.group(1)
    for key in ("Space Shuttle", "Falcon 9", "Falcon Heavy", "Starship", "Electron", "Soyuz", "Atlas V", "Ariane 6", "Ariane 5",
                "Vega", "H-3", "H3", "H-IIA", "PSLV", "GSLV", "LVM3", "Proton", "Angara", "Delta IV", "Vulcan",
                "New Glenn", "Kuaizhou", "Ceres", "Zhuque", "Kinetica", "Gravity", "Tianlong", "Jielong",
                "Firefly Alpha", "Alpha", "Minotaur", "Pegasus", "Antares", "Nuri", "Epsilon", "Kairos"):
        if lv.startswith(key):
            return key
    return lv.split()[0] if lv else "?"


def launches_md():
    orgs = {o["Code"]: o for o in load("orgs.tsv")}
    sites = {s["Site"]: s for s in load("sites.tsv")}
    L = load("launch.tsv")

    def agency_state(code):
        o = orgs.get(code.split("/")[0])
        return o["StateCode"] if o else "?"

    def group(row):
        if row["Agency"].startswith("RLAB"):
            return "USA"
        st = agency_state(row["Agency"])
        g = GROUPS.get(st)
        if g:
            return g
        if st.startswith("I-") or st in ("F", "D", "I", "UK", "GB", "E", "S", "N"):
            return "Europe"
        return "Other"

    def site_name(row):
        s = sites.get(row["Launch_Site"])
        nm = (s.get("ShortName") or s.get("Name") or row["Launch_Site"]) if s else row["Launch_Site"]
        return SITE_EN.get(nm, nm)

    def site_short(row):
        s = sites.get(row["Launch_Site"])
        nm = (s.get("ShortName") or row["Launch_Site"]) if s else row["Launch_Site"]
        return {"Baykonur": "Baikonur", "Vostochniy": "Vostochny", "Huang Hai": "Yellow Sea",
                "Hainan CLS": "Hainan (comm.)"}.get(nm, nm)

    orb = [r for r in L if r["LaunchCode"][:1] in ("O", "D") and r["Launch_Date"][:4].isdigit()]
    by_year = collections.defaultdict(collections.Counter)
    fails = collections.Counter()
    fam_all = collections.Counter()
    fam_fail = collections.Counter()
    fam_first = {}
    site_all = collections.Counter()
    for r in orb:
        y = int(r["Launch_Date"][:4])
        g = group(r)
        by_year[y][g] += 1
        f = r["LaunchCode"][1:2] == "F"
        if f:
            fails[y] += 1
        fam = family(r["LV_Type"])
        fam_all[fam] += 1
        fam_fail[fam] += f
        fam_first.setdefault(fam, y)
        site_all[site_name(r)] += 1
    updated = "13 October 2026"
    out = []
    out.append("## Orbital Launch Attempts by Year\n")
    out.append(f"Orbital launch attempts (successful or not) by the country or region of the launching organisation, "
               f"1957 to {updated}. Rocket Lab's launches from New Zealand count as US. Source: GCAT (J. McDowell, "
               f"CC-BY 4.0).\n")
    out.append("| Year | " + " | ".join(COLS) + " | Total | Failures |")
    out.append("|" + "---|" * (len(COLS) + 3))
    for y in sorted(by_year):
        c = by_year[y]
        tot = sum(c.values())
        out.append(f"| {y}{'*' if y == 2026 else ''} | " + " | ".join(str(c.get(k, 0) or "–") for k in COLS) +
                   f" | {tot} | {fails.get(y, 0) or '–'} |")
    out.append("\n: Orbital launch attempts per year, 1957–2026 (* 2026 to 13 October). {#tbl:apxlaunchyears}\n")

    out.append("## Most-Launched Vehicle Families\n")
    out.append("| Family | First orbital attempt | Attempts | Failures | Success rate |")
    out.append("|---|---|---|---|---|")
    for fam, n in fam_all.most_common(30):
        rate = 100 * (n - fam_fail[fam]) / n
        out.append(f"| {esc(fam)} | {fam_first[fam]} | {n:,} | {fam_fail[fam]} | {rate:.1f} % |".replace(",", " "))
    out.append("\n: The thirty most-launched orbital vehicle families (to 13 October 2026). {#tbl:apxfamilies}\n")

    out.append("## Busiest Launch Sites\n")
    out.append("| Launch site | Orbital launch attempts |")
    out.append("|---|---|")
    for s, n in site_all.most_common(25):
        out.append(f"| {esc(s)} | {n:,} |".replace(",", " "))
    out.append("\n: The twenty-five busiest orbital launch sites of all time (to 13 October 2026). {#tbl:apxsites}\n")

    for year, tag in [(2025, "2025"), (2026, "2026, to 13 October")]:
        rows = [r for r in orb if r["Launch_Date"].startswith(str(year))]
        out.append(f"## Orbital Launch Log: {tag}\n")
        out.append(f"All {len(rows)} orbital launch attempts. ✗ marks a failure to reach orbit. Times are UTC.\n")
        out.append("::: small\n")
        out.append("| No. | Date (UTC) | Vehicle | Site | Mission / payload | |")
        out.append("|---|---|---|---|---|---|")
        for i, r in enumerate(rows, 1):
            d = r["Launch_Date"][5:11].strip()
            lv = r["LV_Type"]
            for a, b in RENAME:
                lv = lv.replace(a, b)
            mission = r["Mission"] if r["Mission"] not in ("-", "") else r["Flight"]
            mission = mission[:42]
            mark = "✗" if r["LaunchCode"][1:2] == "F" else ""
            out.append(f"| {i} | {d} | {esc(lv)} | {esc(site_short(r))} | {esc(mission)} | {mark} |")
        out.append(f"\n: Orbital launch attempts in {tag}. {{#tbl:apxlog{year}}}\n")
        out.append(":::\n")
    (SRC / "appendix_data").mkdir(exist_ok=True)
    p = SRC / "appendix_data/E-launches.md"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(p, sum(len(by_year[y]) for y in by_year), "years")
    # assemble the appendix: curated head + curated tables (if any) + generated launch tables
    head = SRC / "appendix_data/E-head.md"
    cur = SRC / "appendix_data/E-curated.md"
    parts = [head.read_text(encoding="utf-8")] if head.exists() else []
    if cur.exists():
        parts.append(cur.read_text(encoding="utf-8"))
    parts.append(p.read_text(encoding="utf-8"))
    dst = SRC / "chapters/E-mission-vehicle-databases.md"
    dst.write_text("\n\n".join(parts), encoding="utf-8")
    print(dst)


# ---------------------------------------------------------------- image credits
def credits_md():
    cred = json.loads((ROOT / "figures/photos/credits.json").read_text())
    from structure import PARTS  # noqa: E402
    used = collections.OrderedDict()
    titles = {}
    for f in sorted((SRC / "chapters").glob("*.md")):
        key = f.name.split("-")[0]
        if not key[0].isdigit():
            continue
        txt = f.read_text(encoding="utf-8")
        m = re.search(r"^title:\s*(.+)$", txt, re.M)
        titles[key] = m.group(1).strip().strip('"') if m else key
        keys = [f"ch{key}"] if (ROOT / f"figures/photos/ch{key}.jpg").exists() else []
        keys += re.findall(r"figures/photos/([A-Za-z0-9_\-]+)\.jpg", txt)
        used[key] = list(dict.fromkeys(keys))
    out = ["---", "title: Image Credits", "abstract: Sources of the photographs and images reproduced in this manual.",
           "---", "",
           "All photographs in this manual come from the NASA Image and Video Library (images.nasa.gov) and are in "
           "the public domain in the United States, unless stated otherwise in the caption. NASA does not endorse "
           "this publication. Images are listed by chapter in order of appearance, with the NASA identifier, title "
           "and date; the full record can be found at https://images.nasa.gov/details/ followed by the identifier. "
           "All charts and diagrams were drawn for this manual from the sources cited in their captions.", ""]
    parts = [p for p in PARTS if p.get("photo")]
    out.append("## Part Opening Images\n")
    out.append("| Part | NASA ID | Title | Date |")
    out.append("|---|---|---|---|")
    for p in parts:
        c = cred.get(p["photo"], {})
        out.append(f"| {p['num']} | {esc(c.get('nasa_id', '–'))} | {esc(c.get('title', '')[:70])} | {c.get('date', '')} |")
    out.append("\n: Part opening images. {#tbl:apxcreditparts}\n")
    for key, keys in used.items():
        if not keys:
            continue
        out.append(f"## Chapter {int(key)}: {titles[key]}\n")
        out.append("| Image | NASA ID | Title | Date |")
        out.append("|---|---|---|---|")
        for k in keys:
            c = cred.get(k, {})
            label = "Chapter opening" if k == f"ch{key}" else k.split("_", 1)[-1]
            out.append(f"| {esc(label)} | {esc(c.get('nasa_id', '–'))} | {esc((c.get('title') or '')[:70])} | "
                       f"{c.get('date', '')} |")
        out.append(f"\n: Images in Chapter {int(key)}. {{#tbl:apxcredit{key}}}\n")
    p = SRC / "chapters/J-image-credits.md"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(p, sum(len(v) for v in used.values()), "images")


# ---------------------------------------------------------------- acronyms
SMALL = {"of", "and", "the", "for", "in", "on", "to", "a", "an", "de", "du", "des", "la", "le", "et", "with", "by",
         "at", "&", "from", "or", "per", "für", "di", "del", "y", "da", "e"}


def _spell(words, acr):
    """Return n if the last n words spell the acronym (initials, word prefixes, hyphen parts, small words skipped)."""
    A = "".join(c for c in acr if c.isalnum()).lower()

    def rec(ws, i, j):
        if j == len(A):
            return i == len(ws)
        if i == len(ws):
            return False
        w = ws[i]
        wl = w.lower()
        if wl in SMALL and rec(ws, i + 1, j):
            return True
        parts = [p for p in re.split(r"[-/]", wl) if p]
        if len(parts) > 1:                    # hyphenated: each part may give its initial, or be skipped if small
            def hp(k, jj):
                if k == len(parts):
                    return rec(ws, i + 1, jj)
                p = parts[k]
                if jj < len(A) and p[0] == A[jj] and hp(k + 1, jj + 1):
                    return True
                return p in SMALL and hp(k + 1, jj)
            if hp(0, j):
                return True
        k = 0
        while k < len(wl) and j + k < len(A) and wl[k] == A[j + k]:
            k += 1
            if rec(ws, i + 1, j + k):
                return True
        return False

    for n in range(1, min(len(words), 12) + 1):
        ws = words[-n:]
        if ws[0].lower() in SMALL:
            continue
        if rec(ws, 0, 0):
            return n
    return None


def acronyms_md():
    found = collections.defaultdict(collections.Counter)
    where = collections.defaultdict(list)
    files = sorted((SRC / "chapters").glob("*.md"))
    for f in files:
        key = f.name.split("-")[0]
        if key in ("G", "H", "J"):
            continue
        t = f.read_text(encoding="utf-8")
        t = re.sub(r"!\[.*?\]\(.*?\)\{.*?\}", " ", t)
        t = re.sub(r"[*_`]", "", t)
        for m in re.finditer(r"\(([A-Z][A-Za-z0-9\-/&]{1,11})[,;)]", t):
            acr = m.group(1)
            if sum(c.isupper() for c in acr) < 2:
                continue
            seg = t[max(0, m.start() - 220):m.start()]
            seg = re.split(r"[.;:()\n\[\]|—–!?]", seg)[-1]
            toks = list(re.finditer(r"[\w’'\-/&]+", seg))
            if not toks:
                continue
            words = [x.group(0) for x in toks]
            a2 = acr[:-1] if acr.endswith("s") and acr[-2:-1].isupper() else acr
            n = _spell(words, a2)
            if not n:
                continue
            exp = seg[toks[-n].start():].strip().rstrip(",")
            exp = re.sub(r"\s+", " ", exp)
            if a2 != acr and exp.endswith("s"):
                exp = exp[:-1]
            found[a2][exp] += 1
            if key not in where[a2]:
                where[a2].append(key)
    extra = {}
    xf = SRC / "appendix_data/G-acronyms-extra.tsv"
    if xf.exists():
        for line in xf.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                a, e = line.split("\t", 1)
                extra[a.strip()] = e.strip()

    def tidy(variants):
        # prefer a variant that is written in lower case somewhere (a common noun); else the most common one
        lower = [v for v in variants if v[:1].islower()]
        e = lower[0] if lower else variants[0]
        w = e.split()
        if len(w) > 1 and e[:1].isupper() and e[1:2].islower() and all(x[:1].islower() or x.lower() in SMALL for x in w[1:]):
            e = e[:1].lower() + e[1:]
        return e

    rows = {}
    for a, c in found.items():
        rows[a] = (tidy([v for v, _ in c.most_common()]), where[a])
    for a, e in extra.items():
        if e == "-":
            rows.pop(a, None)
        else:
            rows[a] = (e, rows.get(a, ("", []))[1])

    def ch(keys):
        nums = [str(int(k)) if k.isdigit() else k for k in keys]
        return ", ".join(nums[:4]) + (" …" if len(nums) > 4 else "")

    out = ["---", "title: Acronyms and Abbreviations",
           "abstract: The acronyms and abbreviations used in this manual, with their meanings and the chapters in which "
           "they are defined or mainly used.", "---", "",
           "Space engineering is notoriously rich in acronyms. This list gives every acronym that is spelled out in the "
           "chapters, together with common ones used without definition. The last column gives the chapters where each "
           "is defined or mainly used (letters denote appendices). Acronyms in other languages are followed by the "
           "English meaning where helpful. Units and chemical formulae are not listed; see Appendix A.", ""]
    groups = collections.OrderedDict()
    for a in sorted(rows, key=lambda x: (x.upper(), x)):
        first = a[0].upper()
        groups.setdefault(first if first.isalpha() else "#", []).append(a)
    for g, items in groups.items():
        out.append(f"## {g}\n")
        out.append("::: small")
        out.append("| Acronym | Meaning | Chapters |")
        out.append("|------|----------------------|----|")
        for a in items:
            e, k = rows[a]
            out.append(f"| **{esc(a)}** | {esc(e)} | {ch(k)} |")
        out.append(":::\n")
    p = SRC / "chapters/G-acronyms.md"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(p, len(rows), "acronyms")


# ---------------------------------------------------------------- index terms
def index_terms():
    """src/index_terms.txt = glossary headwords (H) + curated appendix_data/index-extra.txt."""
    seen, lines = set(), ["# Generated by tools/make_appendices.py index — edit appendix_data/index-extra.txt or the glossary"]
    gl = (SRC / "chapters/H-glossary.md").read_text(encoding="utf-8")
    for m in re.finditer(r"^\*\*(.+?)\.\*\*", gl, re.M):
        raw = m.group(1)
        for part in raw.split(" / "):
            part = part.strip()
            base = re.sub(r"\s*\(.*?\)", "", part).strip()
            paren = re.findall(r"\((.*?)\)", part)
            if not base:
                continue
            head = base if (base[:2].isupper() or base.split()[0][0].isupper() and base.split()[0][1:2].isupper()) else base[0].lower() + base[1:]
            if any(c.isupper() for c in base[1:]) or base.split()[0] in ("Kepler's", "Kármán", "Lagrange", "Hohmann", "Oberth",
                                                                   "Planck's", "Kessler", "Airy", "Hall-effect", "Doppler", "Whipple",
                                                                   "Molniya", "Bond"):
                head = base
            variants = [base.lower()] + [p.lower() for p in paren if len(p) > 1 and not re.fullmatch(r"[α-ωΑ-Ω*\\]+", p)]
            key = head.lower()
            if key in seen or key == "gateway":
                continue
            seen.add(key)
            lines.append(" | ".join([head] + variants))
    for line in (SRC / "appendix_data/index-extra.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        key = line.split("|")[0].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        lines.append(line.strip())
    (SRC / "index_terms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(SRC / "index_terms.txt", len(lines) - 1, "terms")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools"))
    what = sys.argv[1:] or ["launches", "credits"]
    if "launches" in what:
        launches_md()
    if "credits" in what:
        credits_md()
    if "acronyms" in what:
        acronyms_md()
    if "index" in what:
        index_terms()
