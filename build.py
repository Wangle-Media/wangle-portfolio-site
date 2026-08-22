#!/usr/bin/env python3
"""Build docs/index.html from template.html plus the brand logo.

Single-file output on purpose: the page must be publishable as a self-contained
artifact for review AND servable from GitHub Pages, and keeping one artifact
kills the drift risk of maintaining two copies.

The logo is injected as a CSS mask data URI rather than an <img>, so it takes its
colour from `currentColor` and works in both themes without an invert hack.
"""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
LOGO = ROOT / "docs" / "assets" / "wangle-w.png"
TPL = ROOT / "template.html"
OUT = ROOT / "docs" / "index.html"


def logo_data_uri() -> str:
    """The full-colour gradient mark, embedded so the page stays self-contained.

    Sourced from Company/Branding/logos/wangle W.png, cropped to the mark's own
    bounds (the original carries a wide transparent margin that throws off optical
    alignment against type) and resized for web.
    """
    b64 = base64.b64encode(LOGO.read_bytes()).decode("ascii")
    return "data:image/png;base64," + b64


def main() -> int:
    if not TPL.exists():
        sys.stderr.write("missing template.html\n")
        return 1
    html = TPL.read_text(encoding="utf-8")
    html = html.replace("__LOGO_URI__", logo_data_uri())
    if "__LOGO_URI__" in html:
        sys.stderr.write("logo placeholder not substituted\n")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

    # Fleet hard rule: no em-dash character, ever. Fail the build rather than ship one.
    bad = [i + 1 for i, line in enumerate(html.splitlines()) if "—" in line]
    if bad:
        sys.stderr.write("EM-DASH found on lines: %s\n" % bad)
        return 1

    print("built %s (%d bytes), em-dash check clean" % (OUT, len(html)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
