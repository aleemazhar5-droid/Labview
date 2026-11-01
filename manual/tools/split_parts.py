#!/usr/bin/env python3
"""Split the complete manual into one stand-alone PDF per Part.

  python3 tools/split_parts.py            # after a full build (output/…Reference_Manual.pdf)

Each Part file gets its own cover, the book's title and copyright pages, a contents page for the Part,
then the Part's pages exactly as in the complete book (same page numbers, via PDF page labels).
Bookmarks are rebuilt for the Part; links inside the Part are kept, links to other Parts are removed.
"""
import asyncio
import html as htmlmod
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, TextStringObject

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
from structure import PARTS  # noqa: E402

FULL = build.OUT_PDF
OUTDIR = build.OUT_DIR / "parts"
ROMAN = {p["num"]: i + 1 for i, p in enumerate(PARTS)}
esc = htmlmod.escape


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")


# ------------------------------------------------------------------ outline of the complete book
def read_structure(reader):
    """Return parts [(num, title, start_idx, [(chap_title, idx, [(sec_title, idx)])])] and index page idx."""
    parts, index_idx = [], None
    ol = reader.outline
    i = 0
    while i < len(ol):
        it = ol[i]
        if isinstance(it, list):
            i += 1
            continue
        title = it.title
        idx = reader.get_destination_page_number(it)
        kids = ol[i + 1] if i + 1 < len(ol) and isinstance(ol[i + 1], list) else []
        m = re.match(r"Part ([IVXL]+) — (.+)", title)
        if m:
            chaps = []
            j = 0
            while j < len(kids):
                c = kids[j]
                if isinstance(c, list):
                    j += 1
                    continue
                secs = kids[j + 1] if j + 1 < len(kids) and isinstance(kids[j + 1], list) else []
                chaps.append((c.title, reader.get_destination_page_number(c),
                              [(s.title, reader.get_destination_page_number(s)) for s in secs
                               if not isinstance(s, list)]))
                j += 1
            parts.append((m.group(1), m.group(2), idx, chaps))
        elif title == "Index":
            index_idx = idx
        i += 1
    return parts, index_idx


# ------------------------------------------------------------------ front pages for one Part
def cover_html(part, first_label, last_label, chap_range):
    photo = f"figures/photos/{part['photo']}.jpg"
    n = ROMAN[part["num"]]
    return build.page_html(f"Part {part['num']} cover", f"""
<style>@page {{ margin: 0 }} body {{ margin: 0 }}
.cv {{ width: 210mm; height: 297mm; position: relative; overflow: hidden; color: #fff; font-family: Inter, sans-serif; }}
.cv .bg {{ position: absolute; inset: 0; background: url({photo}) center/cover; }}
.cv .sh {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(4,14,30,0.94) 0%, rgba(4,14,30,0.62) 38%,
          rgba(4,14,30,0.22) 62%, rgba(4,14,30,0.9) 100%); }}
.cv .top {{ position: absolute; top: 24mm; left: 20mm; right: 20mm; }}
.cv .kick {{ font-size: 9.5pt; letter-spacing: 0.3em; text-transform: uppercase; color: #F2A65A; font-weight: 700; }}
.cv .book {{ font-size: 15pt; font-weight: 700; margin-top: 4mm; color: #DCE6F0; }}
.cv .pn {{ font-size: 64pt; font-weight: 800; color: #D9772B; line-height: 1; margin-top: 12mm; }}
.cv h1 {{ color: #fff; font-size: 34pt; line-height: 1.06; font-weight: 800; margin: 3mm 0 5mm; letter-spacing: -0.01em; }}
.cv .sub {{ font-size: 12pt; line-height: 1.5; color: #DCE6F0; max-width: 160mm; font-weight: 400; }}
.cv .bar {{ width: 36mm; height: 3pt; background: #D9772B; margin-top: 8mm; }}
.cv .bot {{ position: absolute; bottom: 18mm; left: 20mm; right: 20mm; display: flex; justify-content: space-between;
           align-items: flex-end; }}
.cv .ed {{ font-size: 10pt; color: #E7EEF5; line-height: 1.55; }}
.cv .ed b {{ color: #F2A65A; }}
</style>
<div class="cv"><div class="bg"></div><div class="sh"></div>
<div class="top"><div class="kick">Engineering Reference Manual · Part {n} of {len(PARTS)}</div>
<div class="book">Space Exploration &amp; Aerospace Engineering</div>
<div class="pn">Part {esc(part['num'])}</div>
<h1>{esc(part['title'])}</h1>
<div class="sub">{esc(part['desc'])}</div><div class="bar"></div></div>
<div class="bot"><div class="ed"><b>{esc(chap_range)}</b> · pages {first_label}–{last_label} of the complete manual<br>
First Edition · Current to October 2026 · Written in plain language with deep technical detail</div></div></div>""")


def contents_html(part, chaps, label_of):
    rows = [f'<div class="part">Part {esc(part["num"])} · {esc(part["title"])}</div>']
    for ctitle, cidx, secs in chaps:
        m = re.match(r"(Chapter|Appendix) ([0-9A-Z]+)\. (.+)", ctitle)
        num, t = (m.group(2), m.group(3)) if m else ("", ctitle)
        p = label_of(cidx)
        rows.append(f'<div class="row l1"><span class="n">{esc(num)}</span><span class="t">'
                    f'<a href="{build.REF}p/{p}">{esc(t)}</a></span><span class="dots"></span>'
                    f'<span class="p">{p}</span></div>')
        for stitle, sidx in secs:
            m2 = re.match(r"([0-9A-Z]+\.[0-9]+) (.+)", stitle)
            sn, st = (m2.group(1), m2.group(2)) if m2 else ("", stitle)
            sp = label_of(sidx)
            rows.append(f'<div class="row l2"><span class="n">{esc(sn)}</span><span class="t">'
                        f'<a href="{build.REF}p/{sp}">{esc(st)}</a></span><span class="dots"></span>'
                        f'<span class="p">{sp}</span></div>')
    note = ("<p class=\"smallprint\" style=\"margin-top:6mm\">This volume is one Part of <i>Space Exploration &amp; "
            "Aerospace Engineering — An Engineering Reference Manual</i>. Page numbers, chapter numbers and figure "
            "numbers are the same as in the complete manual, so cross-references to other chapters (for example "
            "“Chapter 24”) and to the appendices refer to the complete book.</p>")
    return build.page_html(f"Contents of Part {part['num']}",
                           f'<div class="toc-title">Contents of Part {esc(part["num"])}</div>'
                           f'<div class="toc">{"".join(rows)}</div>{note}')


# ------------------------------------------------------------------ assembly
def main():
    reader = PdfReader(str(FULL))
    labels = reader.page_labels
    front_n = labels.index("1")
    parts, index_idx = read_structure(reader)
    end_main = index_idx if index_idx is not None else len(reader.pages)
    ref_to_idx = {p.indirect_reference.idnum: i for i, p in enumerate(reader.pages)}
    by_num = {p["num"]: p for p in PARTS}
    title_pdf = build.PDF_DIR / "front_title.pdf"
    OUTDIR.mkdir(parents=True, exist_ok=True)

    jobs = []
    for k, (num, ptitle, start, chaps) in enumerate(parts):
        end = parts[k + 1][2] if k + 1 < len(parts) else end_main
        part = by_num[num]
        keys = part["chapters"]
        kind = "Appendices" if not keys[0].isdigit() else "Chapters"
        rng = f"{kind} {int(keys[0]) if keys[0].isdigit() else keys[0]}–{int(keys[-1]) if keys[-1].isdigit() else keys[-1]}" \
            if len(keys) > 1 else f"{kind[:-1]} {keys[0]}"
        jobs.append((part, start, end, chaps, rng))

    async def render_fronts():
        async with build.Renderer() as R:
            for part, start, end, chaps, rng in jobs:
                tag = f"part{ROMAN[part['num']]:02d}"
                hc = build.HTML_DIR / f"{tag}_cover.html"
                hc.write_text(cover_html(part, labels[start], labels[end - 1], rng), encoding="utf-8")
                await R.render(hc, build.PDF_DIR / f"{tag}_cover.pdf")
                ht = build.HTML_DIR / f"{tag}_contents.html"
                ht.write_text(contents_html(part, chaps, lambda i: labels[i]), encoding="utf-8")
                await R.render(ht, build.PDF_DIR / f"{tag}_contents.pdf")

    asyncio.run(render_fronts())

    for part, start, end, chaps, rng in jobs:
        n = ROMAN[part["num"]]
        tag = f"part{n:02d}"
        src = PdfReader(str(FULL))          # fresh reader: annotations are edited in place before copying
        s_ref = {p.indirect_reference.idnum: i for i, p in enumerate(src.pages)}
        w = PdfWriter()
        fronts = [PdfReader(str(build.PDF_DIR / f"{tag}_cover.pdf")), PdfReader(str(title_pdf)),
                  PdfReader(str(build.PDF_DIR / f"{tag}_contents.pdf"))]
        for fr in fronts:
            for p in fr.pages:
                w.add_page(p)
        nfront = len(w.pages)
        # mark links before copying: in-part GoTo -> placeholder URI; other GoTo removed
        pending = []
        for i in range(start, end):
            page = src.pages[i]
            annots = page.get("/Annots")
            if not annots:
                continue
            keep = ArrayObject()
            for a in annots:
                ao = a.get_object()
                act = ao.get("/A")
                act = act.get_object() if act is not None else None
                if act is not None and act.get("/S") == "/GoTo":
                    d = act.get("/D")
                    tgt = s_ref.get(d[0].idnum) if isinstance(d, ArrayObject) and len(d) else None
                    if tgt is None or not (start <= tgt < end):
                        continue
                    ao[NameObject("/A")] = DictionaryObject({
                        NameObject("/S"): NameObject("/URI"),
                        NameObject("/URI"): TextStringObject(f"part://{tgt - start}")})
                keep.append(a)
            page[NameObject("/Annots")] = keep
        for i in range(start, end):
            w.add_page(src.pages[i])
        # resolve placeholders and the contents-page links (book page labels)
        label_to_new = {labels[i]: nfront + (i - start) for i in range(start, end)}
        for page in w.pages:
            for a in page.get("/Annots") or []:
                ao = a.get_object()
                act = ao.get("/A")
                if act is None:
                    continue
                act = act.get_object()
                uri = str(act.get("/URI", ""))
                target = None
                if uri.startswith("part://"):
                    target = nfront + int(uri[7:])
                elif uri.startswith(build.REF + "p/"):
                    target = label_to_new.get(uri[len(build.REF) + 2:])
                else:
                    continue
                if target is None:
                    del ao["/A"]
                    continue
                ao[NameObject("/A")] = DictionaryObject({
                    NameObject("/S"): NameObject("/GoTo"),
                    NameObject("/D"): ArrayObject([w.pages[target].indirect_reference, NameObject("/Fit")])})
        # page labels: front matter roman, the Part keeps the book's page numbers
        w.set_page_label(0, nfront - 1, style="/r")
        w.set_page_label(nfront, len(w.pages) - 1, style="/D", start=int(labels[start]))
        # bookmarks
        w.add_outline_item("Cover", 0)
        w.add_outline_item("Title Page", 1)
        w.add_outline_item(f"Contents of Part {part['num']}", len(fronts[0].pages) + len(fronts[1].pages))
        top = w.add_outline_item(f"Part {part['num']} — {part['title']}", nfront)
        for ctitle, cidx, secs in chaps:
            c = w.add_outline_item(ctitle, nfront + cidx - start, parent=top)
            for stitle, sidx in secs:
                w.add_outline_item(stitle, nfront + sidx - start, parent=c)
        w.add_metadata({"/Title": f"Space Exploration & Aerospace Engineering — Part {part['num']}: {part['title']}",
                        "/Author": "Space & Aerospace Engineering Reference Manual project",
                        "/Subject": f"Part {part['num']} of an illustrated engineering reference on the space "
                                    f"ecosystem (First Edition, October 2026)",
                        "/Creator": "Markdown, pandoc, Chromium and pypdf"})
        w.page_mode = "/UseOutlines"
        out = OUTDIR / f"Part_{n:02d}_{part['num']}_{slug(part['title'])}.pdf"
        with open(out, "wb") as f:
            w.write(f)
        try:
            import pikepdf
            tmp = out.with_suffix(".tmp.pdf")
            with pikepdf.open(out) as pdf:
                pdf.save(tmp, object_stream_mode=pikepdf.ObjectStreamMode.generate, compress_streams=True,
                         recompress_flate=True)
            tmp.replace(out)
        except ImportError:
            pass
        print(f"{out.name}: {len(w.pages)} pages ({nfront} front + {end - start}), "
              f"{out.stat().st_size / 1e6:.1f} MB, book pages {labels[start]}–{labels[end - 1]}")


if __name__ == "__main__":
    main()
