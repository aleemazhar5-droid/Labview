# Authoring guide for chapters of the space-engineering reference manual

This manual is a ~1 000-page illustrated engineering reference ("in simple words, with deep technical
accuracy") built from Markdown with pandoc + Chromium. Chapters 01–29 are finished; read one or two of the
recent ones (e.g. `src/chapters/26-space-probes-flybys.md`, `27-landers-edl.md`, `29-sample-return.md`)
before writing, and match their tone, density and structure exactly.

All paths below are relative to `/home/user/Labview/manual`. The current date is **October 2026**.

## 1. Deliverables for one chapter NN

| File | What |
|---|---|
| `src/chapters/NN-short-slug.md` | Chapter text (Markdown + pandoc-crossref syntax) |
| `figures/src/chNN.py` | Script that draws all computed/diagram figures for the chapter → `figures/out/chNN_*.svg` |
| `figures/photos/chNN_*.jpg` | Public-domain photos fetched with `tools/fetch_photos.py --add` (never hand-copied) |
| `notes/currency/chNN.md` | Bullet list of every post-2023 fact you used, each with its source URL and the date checked |

Do **not** edit other chapters, `PLAN.md`, `tools/build.py`, `tools/figlib.py`, `styles/`, or
`notes/currency_2026.md` (read it — it is the shared fact sheet). Do **not** run git commands that change
state (no add/commit/push/checkout/stash). Put temporary files in your scratchpad directory.

## 2. Size and composition targets (per chapter)

- **6 500–7 500 words** of Markdown (check with `wc -w`), giving **18–22 PDF pages**.
- **7–9 figures drawn by `figures/src/chNN.py`** — prefer *computed* figures (physics models, real data,
  parameter sweeps, simulations) over decorative ones; plus 1–3 clear schematic diagrams.
- **7–10 photographs** from the NASA Image and Video Library (real hardware, crews, missions).
- **4–6 tables** (comparisons, specifications, timelines, budgets).
- **2–3 worked examples** (`::: example`) with real numbers that you have computed in Python first.
- One **AI callout** (`::: ai`) linking the topic to the AI chapters of Part XIII: 43 AI foundations; 44 deep learning,
  foundation models and generative AI; 45 data, computing hardware and edge AI in orbit; 46 AI for Earth observation;
  47 AI for weather, climate and space weather; 48 AI for autonomy, navigation and robotics; 49 AI for mission operations,
  communications and networks; 50 AI for SSA, defence and security; 51 AI for space science, planetary exploration and
  human spaceflight; 52 AI in design, manufacturing, launch and the space business; 53 trustworthy AI (assurance,
  security, governance, outlook).
- **Key takeaways** (`::: key`, 5–7 bullets) then **Review questions** (`::: questions`, 8–10 numbered).
- The chapter's hero image `figures/photos/chNN.jpg` already exists (shown under the title). Do not replace it.

## 3. Writing style

- Audience: engineering students and professionals; explain every technical term in plain words at first use,
  then use it precisely. Short paragraphs, active voice, concrete numbers. No hype, no filler.
- British spelling (metre, colour, analyse, programme — but "computer program"), SI units with a space
  ("5.4 km/s", "1 300 °C", "29.6 kPa"); thousands separated by a space ("1 935 g", "17 000"); en dash for
  ranges ("2025–26", "11–13 km/s"); spaced em dash for asides (" — ").
- Never invent facts, quotes, numbers or dates. If unsure after checking, say less or phrase cautiously
  ("about", "reported", "planned"). Prefer figures from agency sources, peer-reviewed papers, or reputable
  space press. Write the status of programmes **as of October 2026**, and state uncertainty where it exists.
- Use **WebSearch / WebFetch** to verify anything that may have changed after 2024 (launches, programme
  status, records, budgets, cancellations, new vehicles) and any number you are not sure of. Record each in
  `notes/currency/chNN.md`. Read `notes/currency_2026.md` first — it already holds many verified 2025–26 facts.
- Never mention AI model names or identifiers anywhere.
- Refer to other chapters as "(Chapter 24)". Avoid repeating material other chapters cover — check their
  headings with `grep -n '^##' src/chapters/*.md` and cross-reference instead.

## 4. Markdown conventions

Front matter (exact keys):

```
---
title: Crewed Spacecraft
hero: ch31
abstract: One paragraph (90–130 words) summarising the chapter.
---
```

- Start with 1–3 intro paragraphs (no heading), then `##` sections (5–8) and `###` subsections. Headings are
  numbered automatically — never type numbers.
- **Figures** (each alone in its own paragraph, caption = full sentence(s)):
  `![Caption text.](figures/out/ch31_entry.svg){#fig:capsuleentry width=94%}`
  `![Caption text.](figures/photos/ch31_dragon.jpg){#fig:dragonphoto width=62%}`
  Widths: data plots 88–100 %, photos 45–75 %, tall photos 35–50 %. Side-by-side photos:

  ```
  ::: figrow
  ![Caption A.](figures/photos/ch31_a.jpg){#fig:a}

  ![Caption B.](figures/photos/ch31_b.jpg){#fig:b}
  :::
  ```
- **Labels must be unique across the whole book**: before using `fig:xyz` / `tbl:xyz`, check with
  `grep -rn '#fig:xyz' src/chapters/`. Use distinctive names (e.g. `fig:eclssloop`, `tbl:crewvehicles`).
- Reference figures/tables in the text *before* they appear: "(@fig:eclssloop)", "@tbl:crewvehicles shows".
- **Tables**: pipe tables with a caption line after a blank line: `: Caption text. {#tbl:crewvehicles}`.
  Keep cells short; 4–7 columns maximum.
- **Maths**: inline `$\Delta v = v_e \ln(m_0/m_f)$`, display `$$ ... $$` (MathJax). Use Unicode for simple
  values in prose (10⁻³, ×, °, ≈).
- **Callouts** (fenced divs): `::: example`, `::: ai`, `::: key`, `::: questions`, also available
  `::: note`, `::: warning`, `::: data`, `::: history`, `::: formula`. First line is a bold title, e.g.
  `**Example: sizing a CO₂ scrubber**`, `**Key takeaways**`, `**Review questions**`. Example steps are a
  numbered list; questions are a numbered list.

## 5. Figures (`figures/src/chNN.py`)

Template:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge


def dose():
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ...
    fig.text(0.99, 0.01, "Model/assumption footnote.", ha="right", va="bottom", fontsize=6.0, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch30_dose")          # -> figures/out/ch30_dose.svg ; save(fig, name, raster=True) for PNG


if __name__ == "__main__":
    fns = [dose]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
```

- Palette constants: NAVY, BLUE, SKY, ORANGE, GOLD, GREEN, RED, VIOLET, GREY, LIGHT, INK, EARTH, LAND, SPACE.
- Helpers in `tools/figlib.py` (read it): `canvas(w,h,xlim,ylim)` blank diagram axes; `box`, `title_box`,
  `arrow`, `darrow`, `label`, `earth`, `planet`, `satellite`, `rocket`, `orbit_ellipse`, `timeline`, `hbar`,
  `stack`, `table_fig`, `world_axes` (cartopy), `ground_track`, `plot_track`, `note`.
- Figure width 6.4–7.0 in; font sizes ≥ 5.8 pt; label lines never overlap each other, data, or titles.
- Put long footnotes in `fig.text(...)` + `tight_layout(rect=(0, 0.06, 1, 1))` — **not** `note()` under an
  axes (long text there makes the whole figure shrink).
- Every computed figure must rest on stated equations/data; write the assumptions in the footnote and make
  the numbers in the text agree with the figure.
- Run `python3 figures/src/chNN.py` then preview: `python3 tools/preview.py <scratch>/f.png 'chNN_*' 2` and
  **look at the PNG with the Read tool**. Fix overlaps, clipping, empty space, illegible labels. Iterate.

## 6. Photos (NASA Image and Video Library — public domain)

```
python3 tools/fetch_photos.py --search "Crew Dragon docking"          # list candidates (id, date, centre, title)
python3 tools/fetch_photos.py --add ch31_dragon=iss068e012345,ch31_soyuz=iss071e000999
python3 tools/contact_sheet.py <scratch>/cs.jpg ch31_dragon ch31_soyuz  # then Read the jpg to inspect
python3 tools/fetch_photos.py --remove ch31_soyuz                      # drop a bad one completely
```

- `--add` registers the key in `figures/photo_list.json` and records the credit in
  `figures/photos/credits.json` (both lock-protected; safe with other agents running).
- Key names: `chNN_<short>`. Reject images that are irrelevant, misleading, tiny (< 600 px), mostly text,
  artist's concepts when real photos exist, or duplicates of photos used in other chapters
  (`ls figures/photos/`).
- Captions must describe what the image really shows; check the title/description stored in `credits.json`.
  Credits are added to the caption automatically by the build — do not type them.

## 7. Build and visual QA

```
sh tools/build_locked.sh NN                     # builds only chapter NN (serialised with a lock)
python3 tools/page_sheet.py NN <scratch>/p.png  # contact sheet of all pages; Read it
python3 tools/page_sheet.py NN <scratch>/q.png 5 6   # pages 5–6 at readable resolution
```

The build prints pages/figures/tables and `WARN` lines (duplicate labels, unresolved references) — fix all
warnings. Look at the pages: no figure larger than needed, no near-empty pages caused by an oversized figure,
tables not overflowing, captions correct, maths rendered, callouts formatted. Iterate until clean.

## 8. Quality bar

Accurate, current (October 2026), quantitative, well illustrated, clearly explained. Every chapter should leave
a reader able to *do* something: estimate a number, size a subsystem, compare designs, read a mission plan.
