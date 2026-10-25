#!/usr/bin/env python3
"""Plain-language pass: extract over-long sentences from chapters and apply rewritten versions safely.

  python3 tools/plain_pass.py extract OUT.json NN [NN ...]   # sentences > 35 words (raw Markdown)
  python3 tools/plain_pass.py apply EDITS.json               # [{"id", "new"}] -> chapters

Each extracted item keeps the exact Markdown text so it can be replaced verbatim. A rewrite is applied
only if it keeps every cross-reference (@fig:…), maths span ($…$), link and number of the original,
and the original text occurs exactly once in its chapter.
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src/chapters"
LIMIT = 35


def plain_words(s):
    s = re.sub(r"\$[^$]+\$", "X", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\{#[^}]*\}|@(fig|tbl|sec|eq):[\w-]+", "ref", s)
    return len(re.sub(r"[*_`]", "", s).split())


def split_raw(line):
    """Split a raw Markdown line into sentences without touching maths or abbreviations."""
    protect = {}

    def keep(m):
        k = f"\x00{len(protect)}\x00"
        protect[k] = m.group(0)
        return k
    t = re.sub(r"\$[^$]+\$|\[[^\]]*\]\([^)]*\)|\b(?:e\.g|i\.e|etc|approx|vs|Fig|No|Dr|St|Mt|al|Inc|Ltd|Co)\.|\d\.\d",
               keep, line)
    parts = re.split(r"(?<=[.!?])(?:\*\*|\*|\)|”|\")?\s+(?=[A-Z0-9“\"(*\[])", t)
    out, pos = [], 0
    for p in parts:
        for k, v in protect.items():
            p = p.replace(k, v)
        out.append(p)
    return out


def extract(out, keys):
    items = []
    for f in sorted(SRC.glob("*.md")):
        key = f.name.split("-")[0]
        if keys and key not in keys:
            continue
        text = f.read_text(encoding="utf-8")
        body = re.sub(r"^---\n.*?\n---\n", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
        fence = False
        for ln, line in enumerate(body.splitlines(), 1):
            s = line.strip()
            if s.startswith("$$"):
                fence = not fence if s.count("$$") == 1 else fence
                continue
            if fence or not s or s.startswith(("|", ":::", "!", "#", ": ", "```", "<", "**Example", "**Key", "**Review")):
                continue
            for sent in split_raw(line):
                n = plain_words(sent)
                if n > LIMIT and text.count(sent) == 1:
                    items.append({"id": f"{key}:{ln}:{len(items)}", "file": f.name, "line": ln, "words": n,
                                  "text": sent.strip()})
    Path(out).write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    c = collections.Counter(i["file"].split("-")[0] for i in items)
    print(out, len(items), "sentences;", " ".join(f"{k}:{v}" for k, v in sorted(c.items())))


def tokens(s):
    s = re.sub(r"(?<=[A-Z])\$", "§", s)          # currency such as US$ 500 is not maths
    refs = re.findall(r"@(?:fig|tbl|sec|eq):[\w-]+", s)
    maths = re.findall(r"\$[^$]+\$", s)
    links = re.findall(r"\]\([^)]*\)", s)
    nums = re.findall(r"\d+(?:[.,]\d+)?", re.sub(r"\$[^$]+\$", "", s))
    return sorted(refs), sorted(maths), sorted(links), sorted(nums)


def apply(edits_file):
    src = {i["id"]: i for i in json.loads(Path(edits_file.replace("edits", "items")).read_text())} \
        if Path(edits_file.replace("edits", "items")).exists() else None
    edits = json.loads(Path(edits_file).read_text(encoding="utf-8"))
    files, ok, bad = {}, 0, []
    for e in edits:
        it = e if "text" in e and "file" in e else (src or {}).get(e["id"])
        if not it:
            bad.append((e.get("id"), "unknown id"))
            continue
        old, new = it["text"], e["new"].strip()
        if old == new:
            continue
        f = SRC / it["file"]
        txt = files.get(f) or f.read_text(encoding="utf-8")
        if txt.count(old) != 1:
            bad.append((e["id"], "original not found exactly once"))
            continue
        to, tn = tokens(old), tokens(new)
        if to[0] != tn[0] or to[1] != tn[1] or to[2] != tn[2]:
            bad.append((e["id"], "refs/maths/links changed"))
            continue
        if collections.Counter(to[3]) - collections.Counter(tn[3]):
            bad.append((e["id"], f"numbers lost: {list((collections.Counter(to[3]) - collections.Counter(tn[3])).elements())}"))
            continue
        if max(plain_words(x) for x in split_raw(new)) > LIMIT + 5:
            bad.append((e["id"], "still too long"))
            continue
        files[f] = txt.replace(old, new)
        ok += 1
    for f, txt in files.items():
        f.write_text(txt, encoding="utf-8")
    print(f"applied {ok}, rejected {len(bad)}")
    for b in bad:
        print("  ", *b)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "extract":
        extract(sys.argv[2], set(sys.argv[3:]))
    elif cmd == "apply":
        apply(sys.argv[2])
