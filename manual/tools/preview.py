#!/usr/bin/env python3
"""Render figures (svg/png) into a contact-sheet PNG via Chromium for visual QA.
   preview.py out.png pattern [cols]   e.g. preview.py /tmp/x.png 'ch01_*' 2"""
import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parent.parent
out, pat = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 2
files = sorted((ROOT / "figures/out").glob(pat + ".*"))
cells = "".join(f'<div class="c"><img src="{f.as_uri()}"><div class="n">{f.name}</div></div>' for f in files)
html = f"""<html><head><style>body{{margin:0;background:#fff;font-family:Inter}}
.g{{display:grid;grid-template-columns:repeat({cols},1fr);gap:8px;padding:8px;width:{cols*560}px}}
.c{{border:1px solid #ddd;padding:4px}} img{{width:100%}} .n{{font-size:11px;color:#555}}</style></head>
<body><div class="g">{cells}</div></body></html>"""
p = ROOT / "build/preview.html"; p.parent.mkdir(exist_ok=True); p.write_text(html)
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page(viewport={"width": cols*560+16, "height": 800})
        await pg.goto(p.as_uri()); await pg.wait_for_timeout(300)
        await pg.screenshot(path=out, full_page=True); await b.close()
asyncio.run(main()); print(out, len(files))
