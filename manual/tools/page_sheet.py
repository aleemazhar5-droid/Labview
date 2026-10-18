#!/usr/bin/env python3
"""Render a chapter PDF's pages for visual QA.
   page_sheet.py NN OUT.png            -> contact sheet of all pages (40 dpi, 7 per row)
   page_sheet.py NN OUT.png 5 6        -> pages 5 and 6 side by side at 75 dpi (for close reading)"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
nn, out = sys.argv[1], sys.argv[2]
pages = [int(p) for p in sys.argv[3:]]
pdf = ROOT / f"build/pdf/ch{int(nn):02d}.pdf"
with tempfile.TemporaryDirectory() as td:
    if pages:
        for p in pages:
            subprocess.run(["pdftoppm", "-r", "75", "-png", "-f", str(p), "-l", str(p), str(pdf), f"{td}/q{p:03d}"], check=True)
    else:
        subprocess.run(["pdftoppm", "-r", "40", "-png", str(pdf), f"{td}/p"], check=True)
    ims = [Image.open(f) for f in sorted(Path(td).glob("*.png"))]
    cols = len(ims) if pages else 7
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(out)
    print(out, len(ims), "pages")
