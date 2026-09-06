#!/usr/bin/env python3
"""Assemble dist/ — exactly the files that should be public on Cloudflare.

Serving the repository root directly would mean the deploy contains .git,
tools/, the Python virtualenv and node_modules, kept out only by an ignore
file. One typo there and private material goes live. An explicit allowlist is
safer: anything not named here simply is not published.

Usage:
    python3 tools/build_dist.py

Then deploy the result:
    npx wrangler deploy
"""

from __future__ import annotations

import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

# Whole directories copied as-is.
DIRS = ["assets"]

# Individual files. Anything absent is reported and skipped rather than
# failing the build, so a partially built site still deploys.
FILES = [
    "index.html",
    "about.html",
    "products.html",
    "product-1.html",
    "product-2.html",
    "product-3.html",
    "product-4.html",
    "product-5.html",
    "contact.html",
    "order.html",
    "privacy-policy.html",
    "terms.html",
    "shipping-returns.html",
    "disclaimer.html",
    "404.html",
    "sitemap.xml",
    "robots.txt",
    "site.webmanifest",
    # Cloudflare reads these as configuration; they are never served.
    "_headers",
    "_redirects",
]


def main() -> int:
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    missing = []
    total = 0

    for d in DIRS:
        src = os.path.join(ROOT, d)
        if not os.path.isdir(src):
            missing.append(d + "/")
            continue
        shutil.copytree(src, os.path.join(DIST, d))
        total += sum(len(f) for _, _, f in os.walk(src))

    for f in FILES:
        src = os.path.join(ROOT, f)
        if not os.path.exists(src):
            missing.append(f)
            continue
        shutil.copy2(src, os.path.join(DIST, f))
        total += 1

    size = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, _, fs in os.walk(DIST)
        for f in fs
    )

    print(f"dist/ built: {total} files, {size / 1024 / 1024:.1f} MB")

    # Guard against ever shipping development material.
    leaked = []
    for dirpath, dirnames, filenames in os.walk(DIST):
        for name in list(dirnames):
            if name in {".git", "tools", ".venv", "node_modules", "__pycache__"}:
                leaked.append(os.path.join(dirpath, name))
        for name in filenames:
            if name.endswith((".py", ".pyc")) or name == ".htaccess":
                leaked.append(os.path.join(dirpath, name))

    if leaked:
        print("\nERROR: development files found in dist/:", file=sys.stderr)
        for p in leaked:
            print("   " + os.path.relpath(p, ROOT), file=sys.stderr)
        return 1

    if missing:
        print("\nnot found (skipped):")
        for m in missing:
            print("   " + m)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
