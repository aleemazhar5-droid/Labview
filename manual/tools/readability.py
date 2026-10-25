#!/usr/bin/env python3
"""Plain-language metrics per chapter: words, mean sentence length, share of long sentences,
Flesch reading ease (prose only — tables, maths, captions, code and callout titles removed).

  python3 tools/readability.py            # all chapters
  python3 tools/readability.py 43 --long  # one chapter, list sentences longer than 35 words
"""
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src/chapters"


def prose(md):
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)
    md = re.sub(r"\$\$.*?\$\$", " ", md, flags=re.S)
    md = re.sub(r"\$[^$\n]+\$", "X", md)
    out = []
    for line in md.splitlines():
        s = line.strip()
        if not s or s.startswith(("|", ":::", "!", "#", ": ", "```", "<")):
            continue
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"\{#[^}]*\}|@(fig|tbl|sec|eq):\w+", "", s)
        s = re.sub(r"[*_`]", "", s)
        s = re.sub(r"^\d+\.\s+|^[-•]\s+", "", s)
        out.append(s)
    return " ".join(out)


def sentences(text):
    text = re.sub(r"\b(e\.g|i\.e|etc|approx|vs|Fig|No|Dr|St|Mt|al)\.", r"\1", text)
    text = re.sub(r"(\d)\.(\d)", r"\1,\2", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"(])", text) if len(s.split()) >= 3]


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 1
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups) - (1 if w.endswith("e") and len(groups) > 1 and not w.endswith("le") else 0)
    return max(1, n)


def stats(md):
    sents = sentences(prose(md))
    words = [w for s in sents for w in s.split()]
    nw, ns = len(words), max(1, len(sents))
    syl = sum(syllables(w) for w in words)
    lens = [len(s.split()) for s in sents]
    flesch = 206.835 - 1.015 * nw / ns - 84.6 * syl / max(1, nw)
    return dict(words=nw, sents=ns, mean=nw / ns, long30=sum(l > 30 for l in lens) / ns,
                long40=sum(l > 40 for l in lens), flesch=flesch, sentlist=sents)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = sorted(SRC.glob("*.md"))
    if args:
        files = [f for f in files if f.name.split("-")[0] in args]
    print(f"{'ch':>3} {'words':>6} {'mean':>5} {'>30w%':>6} {'>40w':>5} {'Flesch':>6}")
    for f in files:
        st = stats(f.read_text(encoding="utf-8"))
        print(f"{f.name.split('-')[0]:>3} {st['words']:>6} {st['mean']:5.1f} {100*st['long30']:6.1f} "
              f"{st['long40']:>5} {st['flesch']:6.1f}")
        if "--long" in sys.argv:
            for s in st["sentlist"]:
                if len(s.split()) > 35:
                    print(f"   [{len(s.split())}] {s}")
