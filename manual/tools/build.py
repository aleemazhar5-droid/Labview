#!/usr/bin/env python3
"""Build the Space & Aerospace Engineering Reference Manual.

Pipeline: Markdown (pandoc) -> numbered HTML (BeautifulSoup) -> per-chapter PDF (Chromium via
Playwright, MathJax SVG) -> page map (pypdf) -> front matter / TOC / lists / index -> header/footer
overlay -> merged PDF with bookmarks, page labels and resolved internal links.

Usage:
  python3 tools/build.py                 # full build (cached per chapter)
  python3 tools/build.py --only 03,04    # render only some chapters (quick preview PDFs in build/pdf)
  python3 tools/build.py --force         # ignore cache
"""
import argparse
import asyncio
import hashlib
import html as htmlmod
import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, DictionaryObject, NameObject, NumberObject, FloatObject)

ROOT = Path(__file__).resolve().parent.parent          # manual/
REPO = ROOT.parent
SRC = ROOT / "src"
CH_DIR = SRC / "chapters"
BUILD = ROOT / "build"
HTML_DIR = BUILD / "html"
PDF_DIR = BUILD / "pdf"
OUT_DIR = REPO / "output"
OUT_PDF = OUT_DIR / "Space_and_Aerospace_Engineering_Reference_Manual.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
MATHJAX = ROOT / "tools/node_modules/mathjax-full/es5/tex-svg-full.js"
BOOK_TITLE = "Space & Aerospace Engineering Reference Manual"
REF = "https://ref.local/"

sys.path.insert(0, str(ROOT / "tools"))
from structure import PARTS, FRONT, chapter_part  # noqa: E402


# --------------------------------------------------------------------------------------------
# Markdown -> HTML
# --------------------------------------------------------------------------------------------
def read_chapter(path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    if text.startswith("---\n"):
        end = text.index("\n---", 4)
        for line in text[4:end].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        text = text[end + 4:]
    return meta, text


def pandoc(md):
    r = subprocess.run(
        ["pandoc", "-f", "markdown+smart+pipe_tables+grid_tables+fenced_divs+bracketed_spans+"
         "implicit_figures+tex_math_dollars+superscript+subscript+definition_lists+raw_html",
         "-t", "html5", "--mathjax", "--wrap=none"],
        input=md.encode("utf-8"), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode())
    if r.stderr:
        sys.stderr.write(r.stderr.decode())
    return r.stdout.decode("utf-8")


def chap_key(path):
    return path.stem.split("-")[0]           # "03" or "A"


def chap_label(key):
    return str(int(key)) if key.isdigit() else key


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())


class Chapter:
    def __init__(self, path):
        self.path = path
        self.key = chap_key(path)
        self.num = chap_label(self.key)
        self.is_appendix = not self.key.isdigit()
        self.meta, self.md = read_chapter(path)
        self.title = self.meta.get("title", path.stem)
        self.labels = {}     # id -> (kind, label)
        self.sections = []   # (level, id, number, title)
        self.figs = []       # (id, label, caption-short)
        self.tbls = []
        self.soup = None

    def digest(self, extra=""):
        h = hashlib.sha1(self.md.encode())
        h.update(json.dumps(self.meta, sort_keys=True).encode())
        h.update(extra.encode())
        # include referenced figure files' mtimes
        for m in re.findall(r"\((figures/[^)\s]+)\)", self.md):
            p = ROOT / m
            if p.exists():
                h.update(f"{m}:{p.stat().st_mtime_ns}".encode())
        hero = self.meta.get("hero")
        if hero:
            p = ROOT / "figures/photos" / f"{hero}.jpg"
            if p.exists():
                h.update(f"{hero}:{p.stat().st_mtime_ns}".encode())
        return h.hexdigest()

    def first_pass(self):
        soup = BeautifulSoup(pandoc(self.md), "lxml")
        body = soup.body
        for h1 in body.find_all("h1"):
            h1.decompose()
        n2 = n3 = 0
        for h in body.find_all(["h2", "h3"]):
            unnumbered = "unnumbered" in (h.get("class") or [])
            if not h.get("id"):
                h["id"] = f"s{self.key}-{len(self.sections)}"
            if h.name == "h2":
                if not unnumbered:
                    n2 += 1
                    n3 = 0
                    num = f"{self.num}.{n2}"
                else:
                    num = ""
            else:
                if not unnumbered:
                    n3 += 1
                    num = f"{self.num}.{n2}.{n3}"
                else:
                    num = ""
            title = h.get_text(" ", strip=True)
            if num:
                span = soup.new_tag("span", attrs={"class": "secnum"})
                span.string = num
                h.insert(0, span)
            self.sections.append((2 if h.name == "h2" else 3, h["id"], num, title))
            self.labels[h["id"]] = ("Section", num or title)
        # figures
        fi = 0
        for fig in body.find_all("figure"):
            fi += 1
            label = f"{self.num}.{fi}"
            fid = fig.get("id") or f"fig{self.key}-{fi}"
            fig["id"] = fid
            img = fig.find("img")
            if img is not None:
                src = img.get("src", "")
                if "photos/" in src:
                    fig["class"] = (fig.get("class") or []) + ["photo"]
                img.attrs.pop("alt", None)
            cap = fig.find("figcaption")
            if cap is None:
                cap = soup.new_tag("figcaption")
                fig.append(cap)
            cap.attrs.pop("aria-hidden", None)
            short = short_caption(cap)
            if img is not None and "photos/" in img.get("src", "") and not cap.find(class_="credit"):
                key = Path(img["src"]).stem
                cr = soup.new_tag("span", attrs={"class": "credit"})
                cr.string = " " + photo_credit(key) + "."
                cap.append(cr)
            lab = soup.new_tag("span", attrs={"class": "fig-label"})
            lab.string = f"FIGURE {label}"
            cap.insert(0, lab)
            self.labels[fid] = ("Figure", label)
            self.figs.append((fid, label, short))
        # tables
        ti = 0
        for tbl in body.find_all("table"):
            cap = tbl.find("caption")
            if cap is None:
                continue
            ti += 1
            label = f"{self.num}.{ti}"
            tid = None
            for s in cap.find_all(string=re.compile(r"\{#tbl:[^}]+\}")):
                m = re.search(r"\{#(tbl:[^}]+)\}", s)
                tid = m.group(1)
                s.replace_with(re.sub(r"\s*\{#tbl:[^}]+\}", "", s))
            tid = tid or f"tbl{self.key}-{ti}"
            tbl["id"] = tid
            short = short_caption(cap)
            lab = soup.new_tag("span", attrs={"class": "tbl-label"})
            lab.string = f"TABLE {label}"
            cap.insert(0, lab)
            self.labels[tid] = ("Table", label)
            self.tbls.append((tid, label, short))
        self.soup = soup

    def second_pass(self, all_labels):
        soup = self.soup
        for sp in soup.find_all("span", class_="citation"):
            cites = sp.get("data-cites", "").split()
            parts = []
            for c in cites:
                if c in all_labels:
                    kind, label = all_labels[c]
                    parts.append((kind, label, c))
                else:
                    print(f"  WARN [{self.key}] unresolved ref @{c}", file=sys.stderr)
                    parts.append(("??", c, c))
            new = soup.new_tag("span", attrs={"class": "xref"})
            for i, (kind, label, c) in enumerate(parts):
                if i:
                    new.append(", ")
                a = soup.new_tag("a", href=f"{REF}id/{c}")
                a.string = f"{kind} {label}" if kind != "??" else f"[{label}]"
                new.append(a)
            sp.replace_with(new)

    def html(self, part):
        body_html = "".join(str(c) for c in self.soup.body.contents)
        hero = self.meta.get("hero")
        hero_html = ""
        if hero:
            credit = photo_credit(hero)
            hero_html = (f'<div class="ch-hero"><img src="figures/photos/{hero}.jpg">'
                         f'<div class="credit">{htmlmod.escape(credit)}</div></div>')
        abstract = self.meta.get("abstract", "")
        abs_html = f'<div class="ch-abstract">{htmlmod.escape(abstract)}</div>' if abstract else ""
        rows = "".join(
            f'<div class="e"><b>{num}</b><a href="{REF}id/{sid}">{htmlmod.escape(t)}</a></div>'
            for lvl, sid, num, t in self.sections if lvl == 2)
        contents = f'<div class="ch-contents"><div class="t">In this chapter</div>{rows}</div>' if rows else ""
        label = "Appendix" if self.is_appendix else "Chapter"
        pname = f"Part {part['num']} · {part['title']}" if part else ""
        opener = (f'<section class="chapter-opener"><div class="part-name">{htmlmod.escape(pname)}</div>'
                  f'<div class="ch-band"><div class="ch-num">{self.num}</div><div>'
                  f'<div class="ch-label">{label}</div><h1 id="top">{htmlmod.escape(self.title)}</h1></div></div>'
                  f'{hero_html}{abs_html}{contents}</section>')
        return page_html(self.title, opener + body_html)


def short_caption(tag):
    txt = tag.get_text(" ", strip=True)
    txt = re.sub(r"\s+", " ", txt)
    txt = re.sub(r"\s*\{#tbl:[^}]+\}", "", txt)
    m = re.match(r"(.+?[.!?])(\s|$)", txt)
    s = m.group(1) if m else txt
    if len(s) > 150:
        s = s[:147].rsplit(" ", 1)[0] + "…"
    return s


_credits = None


def photo_credit(key):
    global _credits
    if _credits is None:
        p = ROOT / "figures/photos/credits.json"
        _credits = json.loads(p.read_text()) if p.exists() else {}
    c = _credits.get(key, {})
    return c.get("credit", "Image: NASA")


def page_html(title, inner, extra_css=""):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<base href="{ROOT.as_uri()}/">
<title>{htmlmod.escape(title)}</title>
<link rel="stylesheet" href="styles/manual.css">
<style>{extra_css}</style>
<script>
window.MathJax = {{ tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']], tags: 'none' }},
  svg: {{ fontCache: 'global', scale: 1.0 }}, options: {{ enableMenu: false }},
  startup: {{ typeset: true }} }};
</script>
<script src="{MATHJAX.as_uri()}"></script>
</head><body>{inner}</body></html>"""


# --------------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------------
class Renderer:
    async def __aenter__(self):
        from playwright.async_api import async_playwright
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(
            executable_path=CHROME,
            args=["--disable-background-networking", "--disable-component-update",
                  "--no-first-run", "--disable-sync", "--font-render-hinting=none"])
        return self

    async def __aexit__(self, *a):
        await self.browser.close()
        await self.pw.stop()

    async def render(self, html_path, pdf_path, margins=True):
        page = await self.browser.new_page()
        await page.goto(html_path.as_uri(), wait_until="load", timeout=180000)
        await page.evaluate("document.fonts.ready")
        try:
            if await page.evaluate("!!window.MathJax"):
                await page.wait_for_function("window.MathJax && MathJax.startup && MathJax.startup.promise",
                                             timeout=60000)
                await page.evaluate("MathJax.startup.promise")
        except Exception as e:  # noqa: BLE001
            print("  mathjax wait failed:", e, file=sys.stderr)
        await page.evaluate("""Promise.all(Array.from(document.images).filter(i => !i.complete)
                               .map(i => new Promise(r => { i.onload = i.onerror = r; })))""")
        await page.pdf(path=str(pdf_path), prefer_css_page_size=True, outline=True, tagged=False,
                       print_background=True)
        await page.close()


# --------------------------------------------------------------------------------------------
# PDF analysis
# --------------------------------------------------------------------------------------------
def outline_entries(reader):
    out = []

    def walk(items, depth):
        for it in items:
            if isinstance(it, list):
                walk(it, depth + 1)
            else:
                try:
                    out.append((depth, it.title, reader.get_destination_page_number(it)))
                except Exception:  # noqa: BLE001
                    pass
    walk(reader.outline, 0)
    return out


def page_texts(reader):
    texts = []
    for p in reader.pages:
        try:
            texts.append(p.extract_text() or "")
        except Exception:  # noqa: BLE001
            texts.append("")
    return texts


def analyze_chapter(ch, pdf_path):
    reader = PdfReader(str(pdf_path))
    n = len(reader.pages)
    ol = outline_entries(reader)
    # map sections by normalized title order
    sec_pages = {}
    oi = 0
    ol_norm = [(d, norm(t), p) for d, t, p in ol]
    for lvl, sid, num, title in ch.sections:
        target = norm((num or "") + title)
        target2 = norm(title)
        found = None
        for j in range(oi, len(ol_norm)):
            if ol_norm[j][1] in (target, target2) or ol_norm[j][1].endswith(target2):
                found = j
                break
        if found is None:
            sec_pages[sid] = sec_pages.get(sid, None)
            continue
        sec_pages[sid] = ol_norm[found][2]
        oi = found + 1
    texts = page_texts(reader)
    fig_pages, tbl_pages = {}, {}
    for i, t in enumerate(texts):
        for m in re.finditer(r"FIGURE\s+([0-9A-Z]+\.\d+)", t):
            fig_pages.setdefault(m.group(1), i)
        for m in re.finditer(r"TABLE\s+([0-9A-Z]+\.\d+)", t):
            tbl_pages.setdefault(m.group(1), i)
    # fill missing section pages from neighbours
    last = 0
    for lvl, sid, num, title in ch.sections:
        if sec_pages.get(sid) is None:
            sec_pages[sid] = last
        last = sec_pages[sid]
    return {"pages": n, "sec_pages": sec_pages, "fig_pages": fig_pages, "tbl_pages": tbl_pages,
            "texts": texts}


# --------------------------------------------------------------------------------------------
# Front matter, TOC, lists, index
# --------------------------------------------------------------------------------------------
def esc(s):
    return htmlmod.escape(s)


def toc_html(chapters, info, start):
    rows = []
    for item in FRONT_TOC_ITEMS:
        rows.append(item)
    by_key = {c.key: c for c in chapters}
    for part in PARTS:
        pkey = f"part{part['num']}"
        if pkey in start:
            rows.append(f'<div class="part">Part {part["num"]} · {esc(part["title"])}</div>')
        for k in part["chapters"]:
            ch = by_key.get(k)
            if not ch:
                continue
            s = start[ch.key]
            lab = ch.num
            rows.append(f'<div class="row l1"><span class="n">{lab}</span><span class="t">'
                        f'<a href="{REF}p/{s}">{esc(ch.title)}</a></span><span class="dots"></span>'
                        f'<span class="p">{s}</span></div>')
            for lvl, sid, num, title in ch.sections:
                p = s + info[ch.key]["sec_pages"].get(sid, 0)
                cls = "l2" if lvl == 2 else "l3"
                if lvl == 3 and not TOC_LEVEL3:
                    continue
                rows.append(f'<div class="row {cls}"><span class="n">{num}</span><span class="t">'
                            f'<a href="{REF}p/{p}">{esc(title)}</a></span><span class="dots"></span>'
                            f'<span class="p">{p}</span></div>')
    for name, key in BACK_TOC_ITEMS:
        if key in start:
            rows.append(f'<div class="row l1"><span class="n"></span><span class="t">'
                        f'<a href="{REF}p/{start[key]}">{name}</a></span><span class="dots"></span>'
                        f'<span class="p">{start[key]}</span></div>')
    return page_html("Contents", f'<div class="toc-title">Contents</div><div class="toc">{"".join(rows)}</div>')


TOC_LEVEL3 = False
FRONT_TOC_ITEMS = []
BACK_TOC_ITEMS = [("Index", "index")]


def lof_html(chapters, info, start, kind):
    rows = []
    for ch in chapters:
        items = ch.figs if kind == "fig" else ch.tbls
        if not items:
            continue
        rows.append(f'<div class="chap">{"Appendix" if ch.is_appendix else "Chapter"} {ch.num} · {esc(ch.title)}</div>')
        pages = info[ch.key]["fig_pages" if kind == "fig" else "tbl_pages"]
        for fid, label, short in items:
            p = start[ch.key] + pages.get(label, 0)
            rows.append(f'<div class="row"><span class="n">{label}</span><span class="t">'
                        f'<a href="{REF}p/{p}">{esc(short)}</a></span><span class="dots"></span>'
                        f'<span class="p">{p}</span></div>')
    title = "List of Figures" if kind == "fig" else "List of Tables"
    return page_html(title, f'<div class="toc-title">{title}</div><div class="toc lof">{"".join(rows)}</div>')


def index_html(chapters, info, start):
    terms_file = SRC / "index_terms.txt"
    if not terms_file.exists():
        return None
    entries = []
    pages_text = []   # (abs page, normalized text)
    for ch in chapters:
        for i, t in enumerate(info[ch.key]["texts"]):
            tt = re.sub(r"-\s*\n\s*", "", t)
            tt = re.sub(r"\s+", " ", tt).lower()
            pages_text.append((start[ch.key] + i, tt))
    for line in terms_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [x.strip() for x in line.split("|")]
        head = parts[0]
        variants = [v.lower() for v in (parts[1:] or [head])]
        pats = [re.compile(r"(?<![a-z0-9])" + re.escape(v) + r"(?![a-z0-9])") for v in variants]
        hits = []
        for p, tt in pages_text:
            if any(pt.search(tt) for pt in pats):
                hits.append(p)
        if not hits:
            continue
        if len(hits) > 14:
            hits = hits[:14]
        entries.append((head, hits))
    entries.sort(key=lambda e: e[0].lower().lstrip("'\""))
    out, letter = [], None
    for head, hits in entries:
        L = head[0].upper()
        L = L if L.isalpha() else "#"
        if L != letter:
            letter = L
            out.append(f'<div class="letter">{L}</div>')
        links = ", ".join(f'<a href="{REF}p/{p}">{p}</a>' for p in compress_pages(hits))
        out.append(f'<div class="ie">{esc(head)}, {links}</div>')
    return page_html("Index", f'<div class="toc-title">Index</div><div class="index">{"".join(out)}</div>')


def compress_pages(hits):
    return sorted(set(hits))


def part_html(part):
    img = part.get("photo")
    bg = f'<div class="bg" style="background-image:url(figures/photos/{img}.jpg)"></div>' if img else ""
    credit = f'<div class="credit">{esc(photo_credit(img))}</div>' if img else ""
    chap_rows = "".join(f'<div><b>{chap_label(k)}</b>{esc(t)}</div>' for k, t in part.get("chapter_titles", []))
    return page_html(f"Part {part['num']}", f"""<div class="part-page">{bg}<div class="shade"></div>
      <div class="content"><div class="pn">Part {part['num']}</div><div class="pt">{esc(part['title'])}</div>
      <div class="pd">{esc(part['desc'])}</div><div class="pc">{chap_rows}</div>{credit}</div></div>""",
                     extra_css="@page { margin: 0 } body { margin: 0 }")


# --------------------------------------------------------------------------------------------
# Header / footer overlay
# --------------------------------------------------------------------------------------------
def overlay_html(page_specs):
    """page_specs: list of dicts {num: str|None, left: str, right: str, header: bool}"""
    css = """@page { size: A4; margin: 0 }
      body { margin:0; font-family: Inter, sans-serif; }
      .pg { width: 210mm; height: 297mm; position: relative; break-after: page; overflow: hidden; }
      .hd { position: absolute; top: 10.5mm; left: 19mm; right: 19mm; font-size: 7.6pt; color: #5B6670;
            border-bottom: 0.5pt solid #C9D3DD; padding-bottom: 1.6mm; display: flex; justify-content: space-between;
            letter-spacing: 0.02em; }
      .hd b { color: #0B2E4F; font-weight: 700; }
      .ft { position: absolute; bottom: 9mm; font-size: 8.4pt; font-weight: 700; color: #0B2E4F; }
      .ft.o { right: 19mm; } .ft.e { left: 19mm; }
      .ft .bar { display:inline-block; width: 6mm; height: 1.4pt; background:#D9772B; vertical-align: middle; margin: 0 2mm; }
      .tag { position: absolute; bottom: 9.4mm; left: 0; right: 0; text-align: center; font-size: 6.6pt; color: #9AA5B1;
             letter-spacing: 0.12em; text-transform: uppercase; }"""
    pages = []
    for i, s in enumerate(page_specs):
        inner = ""
        odd = (s.get("seq", i) % 2 == 0)
        if s.get("header"):
            if odd:
                inner += f'<div class="hd"><span>{esc(BOOK_TITLE)}</span><span><b>{esc(s["right"])}</b></span></div>'
            else:
                inner += f'<div class="hd"><span><b>{esc(s["left"])}</b></span><span>{esc(BOOK_TITLE)}</span></div>'
        if s.get("num"):
            if odd:
                inner += f'<div class="ft o"><span class="bar"></span>{esc(s["num"])}</div>'
            else:
                inner += f'<div class="ft e">{esc(s["num"])}<span class="bar"></span></div>'
        pages.append(f'<div class="pg">{inner}</div>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head>
      <body>{''.join(pages)}</body></html>"""


def roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
            (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    s = ""
    for v, r in vals:
        while n >= v:
            s += r
            n -= v
    return s


# --------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------
async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-final", action="store_true")
    args = ap.parse_args()
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    paths = sorted(CH_DIR.glob("*.md"), key=lambda p: (not chap_key(p).isdigit(), chap_key(p)))
    chapters = [Chapter(p) for p in paths]
    only = set(x.strip() for x in args.only.split(",") if x.strip())
    print(f"{len(chapters)} chapter files")
    all_labels = {}
    for ch in chapters:
        ch.first_pass()
        for k, v in ch.labels.items():
            if k in all_labels and not k.startswith("s"):
                print(f"  WARN duplicate label {k}", file=sys.stderr)
            all_labels[k] = v
    label_json = json.dumps(all_labels, sort_keys=True)
    cache_file = BUILD / "cache.json"
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    css_digest = hashlib.sha1((ROOT / "styles/manual.css").read_bytes()).hexdigest()

    async with Renderer() as R:
        info = {}
        for ch in chapters:
            if only and ch.key not in only:
                continue
            ch.second_pass(all_labels)
            part = chapter_part(ch.key)
            # cache key includes labels referenced (cheap approximation: all labels)
            dg = ch.digest(css_digest + hashlib.sha1(label_json.encode()).hexdigest())
            hp = HTML_DIR / f"ch{ch.key}.html"
            pp = PDF_DIR / f"ch{ch.key}.pdf"
            ip = PDF_DIR / f"ch{ch.key}.json"
            if not args.force and cache.get(ch.key) == dg and pp.exists() and ip.exists():
                info[ch.key] = json.loads(ip.read_text())
                continue
            hp.write_text(ch.html(part), encoding="utf-8")
            print(f"  render {ch.key} {ch.title}")
            await R.render(hp, pp)
            info[ch.key] = analyze_chapter(ch, pp)
            ip.write_text(json.dumps(info[ch.key]))
            cache[ch.key] = dg
            cache_file.write_text(json.dumps(cache, indent=1))
            print(f"    {info[ch.key]['pages']} pages, {len(ch.figs)} figs, {len(ch.tbls)} tables")
        if only or args.no_final:
            tot = sum(v["pages"] for v in info.values())
            print(f"rendered subset: {tot} pages")
            return

        # ---- layout of main matter ----
        seq = []   # list of (key, kind, pdf_path, pages)
        for part in PARTS:
            ptitles = [(k, next((c.title for c in chapters if c.key == k), "")) for k in part["chapters"]
                       if any(c.key == k for c in chapters)]
            if not ptitles:
                continue
            part["chapter_titles"] = ptitles
            pk = f"part{part['num']}"
            hp = HTML_DIR / f"{pk}.html"
            pp = PDF_DIR / f"{pk}.pdf"
            hp.write_text(part_html(part), encoding="utf-8")
            await R.render(hp, pp)
            seq.append((pk, "part", pp, len(PdfReader(str(pp)).pages)))
            for k in part["chapters"]:
                ch = next((c for c in chapters if c.key == k), None)
                if ch:
                    seq.append((ch.key, "chapter", PDF_DIR / f"ch{ch.key}.pdf", info[ch.key]["pages"]))
        start = {}
        page = 1
        for key, kind, pp, n in seq:
            start[key] = page
            page += n
        # index (needs page numbers of main matter); render to know its length
        idx = index_html(chapters, info, start)
        if idx:
            hp = HTML_DIR / "index.html"
            pp = PDF_DIR / "index.pdf"
            hp.write_text(idx, encoding="utf-8")
            await R.render(hp, pp)
            n = len(PdfReader(str(pp)).pages)
            start["index"] = page
            seq.append(("index", "back", pp, n))
            page += n
        main_pages = page - 1

        # ---- front matter ----
        front = []
        for name, builder in FRONT:
            hp = HTML_DIR / f"front_{name}.html"
            pp = PDF_DIR / f"front_{name}.pdf"
            hp.write_text(builder(page_html, ROOT), encoding="utf-8")
            await R.render(hp, pp)
            front.append((name, pp))
        for name, html_text in (("toc", toc_html(chapters, info, start)),
                                ("lof", lof_html(chapters, info, start, "fig")),
                                ("lot", lof_html(chapters, info, start, "tbl"))):
            hp = HTML_DIR / f"front_{name}.html"
            pp = PDF_DIR / f"front_{name}.pdf"
            hp.write_text(html_text, encoding="utf-8")
            await R.render(hp, pp)
            front.append((name, pp))

        # ---- overlay specs ----
        specs = []
        front_pages = 0
        for name, pp in front:
            n = len(PdfReader(str(pp)).pages)
            for i in range(n):
                fp = front_pages + i
                specs.append({"num": roman(fp + 1) if name not in ("cover", "title") else None,
                              "header": False, "seq": fp})
            front_pages += n
        by_key = {c.key: c for c in chapters}
        for key, kind, pp, n in seq:
            for i in range(n):
                absn = start[key] + i
                spec = {"num": str(absn), "seq": front_pages + absn - 1, "header": False}
                if kind == "chapter":
                    ch = by_key[key]
                    if i > 0:
                        spec["header"] = True
                        spec["left"] = f"{'Appendix' if ch.is_appendix else 'Chapter'} {ch.num}  ·  {ch.title}"
                        cur = ""
                        for lvl, sid, num, title in ch.sections:
                            if lvl == 2 and info[key]["sec_pages"].get(sid, 99999) <= i:
                                cur = f"{num}  {title}"
                        spec["right"] = cur or ch.title
                elif kind == "part":
                    spec["num"] = None
                elif kind == "back":
                    spec["header"] = i > 0
                    spec["left"] = spec["right"] = "Index"
                specs.append(spec)
        ov_html = HTML_DIR / "overlay.html"
        ov_pdf = PDF_DIR / "overlay.pdf"
        ov_html.write_text(overlay_html(specs), encoding="utf-8")
        await R.render(ov_html, ov_pdf)

    # ---- merge ----
    print("merging…")
    overlay = PdfReader(str(ov_pdf))
    writer = PdfWriter()
    docs = [(name, "front", pp) for name, pp in front] + [(k, kind, pp) for k, kind, pp, n in seq]
    offsets = {}
    gi = 0
    for name, kind, pp in docs:
        r = PdfReader(str(pp))
        offsets[name] = gi
        for p in r.pages:
            p.merge_page(overlay.pages[gi])
            writer.add_page(p)
            gi += 1
    total = gi
    # page labels
    writer.set_page_label(0, front_pages - 1, style="/r")
    writer.set_page_label(front_pages, total - 1, style="/D")
    # targets
    def abs_index(page_number):
        return front_pages + page_number - 1
    id_pages = {}
    for ch in chapters:
        s = start.get(ch.key)
        if s is None:
            continue
        for lvl, sid, num, title in ch.sections:
            id_pages[sid] = s + info[ch.key]["sec_pages"].get(sid, 0)
        for fid, label, short in ch.figs:
            id_pages[fid] = s + info[ch.key]["fig_pages"].get(label, 0)
        for tid, label, short in ch.tbls:
            id_pages[tid] = s + info[ch.key]["tbl_pages"].get(label, 0)
    # resolve links
    nlinks = 0
    for pi, page in enumerate(writer.pages):
        annots = page.get("/Annots")
        if not annots:
            continue
        for a in annots:
            a = a.get_object()
            act = a.get("/A")
            if not act:
                continue
            act = act.get_object()
            uri = act.get("/URI")
            if not uri or not str(uri).startswith(REF):
                continue
            tail = str(uri)[len(REF):]
            target = None
            if tail.startswith("p/"):
                target = abs_index(int(tail[2:]))
            elif tail.startswith("id/"):
                pid = tail[3:]
                if pid == "top":
                    target = None
                elif pid in id_pages:
                    target = abs_index(id_pages[pid])
            if target is None or target >= total:
                del a["/A"]
                continue
            dest = ArrayObject([writer.pages[target].indirect_reference, NameObject("/Fit")])
            newact = DictionaryObject({NameObject("/S"): NameObject("/GoTo"), NameObject("/D"): dest})
            a[NameObject("/A")] = newact
            nlinks += 1
    print(f"  resolved {nlinks} internal links")
    # bookmarks
    fr_titles = {"cover": "Cover", "title": "Title Page", "preface": "Preface and How to Use This Manual",
                 "toc": "Contents", "lof": "List of Figures", "lot": "List of Tables"}
    for name, pp in front:
        if name in fr_titles:
            writer.add_outline_item(fr_titles[name], offsets[name])
    for part in PARTS:
        pk = f"part{part['num']}"
        if pk not in offsets:
            continue
        pitem = writer.add_outline_item(f"Part {part['num']} — {part['title']}", offsets[pk])
        for k in part["chapters"]:
            ch = by_key.get(k)
            if not ch or ch.key not in offsets:
                continue
            citem = writer.add_outline_item(
                f"{'Appendix' if ch.is_appendix else 'Chapter'} {ch.num}. {ch.title}", offsets[ch.key], parent=pitem)
            for lvl, sid, num, title in ch.sections:
                if lvl == 2:
                    writer.add_outline_item(f"{num} {title}", abs_index(id_pages[sid]), parent=citem)
    if "index" in offsets:
        writer.add_outline_item("Index", offsets["index"])
    writer.add_metadata({"/Title": BOOK_TITLE, "/Author": "Space & Aerospace Engineering Reference Manual project",
                         "/Subject": "Engineering reference manual on space exploration and aerospace systems",
                         "/Keywords": "space, aerospace, satellites, launch vehicles, remote sensing, AI"})
    writer.page_mode = "/UseOutlines"
    try:
        writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    except Exception as e:  # noqa: BLE001
        print("  compress skipped:", e)
    with open(OUT_PDF, "wb") as f:
        writer.write(f)
    print(f"wrote {OUT_PDF} — {total} pages ({front_pages} front + {main_pages} main)")


if __name__ == "__main__":
    asyncio.run(main())
