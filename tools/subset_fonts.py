#!/usr/bin/env python3
"""Subset the self-hosted variable fonts to the characters the site renders.

The full Playfair Display and Inter releases carry ~230 glyphs each covering
Latin Extended, Vietnamese and Cyrillic ranges we never use. This site is
English-only, so the shipped files are cut down to Basic Latin plus the
punctuation, currency and arrow marks that appear in the copy — about a third
of the original weight, with the variable weight axis left intact.

Run it after adding copy that introduces a new character:

    .venv/bin/python tools/subset_fonts.py

Source (unsubset) fonts live in tools/fonts_src/. If that directory is absent
the script refuses to run rather than subsetting an already-subset file, which
would silently compound losses on every invocation.

Two subsetter defaults are deliberately NOT used:

  --no-hinting     drops the `prep` table, which shifts rendered text advance
                   widths by up to 0.5%. That is invisible per glyph but it
                   reflows headlines and moved ~2800 elements when measured.
  --layout-features=<list>
                   keeping only a hand-picked feature list has the same effect
                   through GPOS. `*` keeps them all.

With both left alone the subset is metric-identical to the original: verified
by measuring rendered string widths at 200px for both faces before and after.

Requires: fonttools, brotli  (pip install fonttools brotli)
"""

from __future__ import annotations

import glob
import html
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "fonts_src")
DEST = os.path.join(ROOT, "assets", "fonts")

# Faces to ship. Inter italic is deliberately absent: every italic on the site
# is display type set in Playfair, so an Inter italic face would never load.
FACES = ["inter-normal", "playfair-normal", "playfair-italic"]

# Marks that never appear as literal text in the HTML but can still be rendered
# (injected by JS, produced by CSS content, or simply worth keeping as a safety
# margin so a small copy edit does not silently fall back to a system font).
EXTRA = (
    "©®™°±×÷–—―‘’‚“”„†‡•…‰‹›€£¥₹→←↑↓✓✔★☆·‑"
    "\u00a0\u2009\u202f"
)

LAYOUT_FEATURES = "*"


def charset() -> str:
    """Every character the site can render, from markup and JS string literals."""
    chars: set[str] = set()

    for path in glob.glob(os.path.join(ROOT, "*.html")):
        text = open(path, encoding="utf-8").read()
        text = re.sub(r"<script[\s\S]*?</script>", " ", text)
        text = re.sub(r"<style[\s\S]*?</style>", " ", text)
        text = re.sub(r"<[^>]+>", " ", text)
        chars |= set(html.unescape(text))

    for path in glob.glob(os.path.join(ROOT, "assets", "js", "*.js")):
        for match in re.finditer(r"'([^'\n]*)'|\"([^\"\n]*)\"", open(path, encoding="utf-8").read()):
            chars |= set(match.group(1) or match.group(2) or "")

    chars |= set(chr(c) for c in range(0x20, 0x7F))  # full printable ASCII
    chars |= set(EXTRA)
    chars = {c for c in chars if ord(c) > 31}
    return "".join(sorted(chars))


def main() -> int:
    if not os.path.isdir(SRC):
        print(f"error: {SRC} not found.", file=sys.stderr)
        print("Put the original (unsubset) .woff2 files there first — subsetting an", file=sys.stderr)
        print("already-subset font would compound the glyph loss.", file=sys.stderr)
        return 1

    text = charset()
    listing = os.path.join(SRC, "charset.txt")
    open(listing, "w", encoding="utf-8").write(text)
    print(f"charset: {len(text)} codepoints -> {listing}")

    total_before = total_after = 0
    for face in FACES:
        src = os.path.join(SRC, f"{face}.woff2")
        dst = os.path.join(DEST, f"{face}.woff2")
        if not os.path.exists(src):
            print(f"  skip {face}: no source at {src}")
            continue
        subprocess.run(
            [
                sys.executable, "-m", "fontTools.subset", src,
                f"--output-file={dst}",
                "--flavor=woff2",
                f"--text-file={listing}",
                f"--layout-features={LAYOUT_FEATURES}",
            ],
            check=True,
        )
        before, after = os.path.getsize(src), os.path.getsize(dst)
        total_before += before
        total_after += after
        print(f"  {face:22} {before:7} -> {after:7} bytes  (-{100 - 100 * after // before}%)")

    if total_before:
        print(f"  {'TOTAL':22} {total_before:7} -> {total_after:7} bytes"
              f"  (-{100 - 100 * total_after // total_before}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
