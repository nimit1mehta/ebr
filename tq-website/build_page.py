#!/usr/bin/env python3
"""
Assemble the restructured TQ Data Foundation page from panel modules.

    python3 build_page.py            -> restructured.html
    python3 inline_build.py restructured.html   -> self-contained single file

To reorder the page, reorder MANIFEST. To drop a panel, comment it out.
To edit one panel's copy or styling, edit only that module in panels/.
"""
import importlib
import re
import sys

from panels import base

# --------------------------------------------------------------------------
# Page order. This is the whole spec - everything else follows from it.
# --------------------------------------------------------------------------
MANIFEST = [
    "p01_hero",           # NEW  dark, category headline, no explainer
    "p02_trusted",        #      surviving, full row, blurb removed
    "p03_truth",          # NEW  agents need truth / truth + judgement
    "p04_pillars",        # NEW  four components, scroll tracked
    "p05_quote_truth",    # NEW  "the same truth" quote
    "p06_steps",          # NEW  five steps + architecture build
    "p07_capabilities",   # NEW  six core capabilities
    "p08_quote_stats",    #      surviving, quote + stat tiles
    "p09_webinar",        #      surviving
    "p10_faq",            #      surviving
    "p11_cta",            #      surviving
]

# Sections present in the original that no longer appear anywhere.
RETIRED = {
    3: 'Context built one app at a time  ->  replaced by p03_truth',
    4: 'Five moves from scattered data   ->  replaced by p06_steps',
    5: 'Four things sitting between...   ->  replaced by p04_pillars',
    6: 'Same question, two answers (WY)  ->  cut',
    7: 'CDO quote                        ->  replaced by p05_quote_truth',
    8: 'What an agent needs (old caps)   ->  replaced by p07_capabilities',
}

SRC = "original.html"
OUT = "restructured.html"


def top_level_sections(body):
    """Return [(start, end)] for each top-level <section>, honouring nesting."""
    spans, depth, start = [], 0, None
    for m in re.finditer(r'<(/?)section\b[^>]*>', body):
        if not m.group(1):
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                spans.append((start, m.end()))
    return spans


def main():
    src = open(SRC, encoding="utf-8").read()
    root = src.find('<div id="tqdf-root"')
    if root < 0:
        sys.exit("could not locate #tqdf-root in " + SRC)

    head, body = src[:root], src[root:]
    spans = top_level_sections(body)
    if len(spans) != 12:
        print(f"  ! expected 12 top-level sections, found {len(spans)}")

    notes = []

    def icon(name):
        """Lift an iconoir SVG that Iconify already baked into the original page.
        Size is stripped so CSS controls it; keeps everything offline-safe."""
        # search the whole document: several icons live in the nav, above #tqdf-root
        m = re.search(r'<svg[^>]*data-icon="' + re.escape(name) + r'"[^>]*>[\s\S]*?</svg>',
                      src)
        if not m:
            notes.append(("icon", f"MISSING {name}"))
            return ""
        svg = m.group(0)
        svg = re.sub(r'\s(?:width|height|style)="[^"]*"', "", svg)
        svg = re.sub(r'\sclass="[^"]*"', ' class="nv-ic"', svg, count=1)
        return svg

    ctx = {
        # 1-based, matching the section map
        "section": lambda i: body[spans[i - 1][0]:spans[i - 1][1]],
        "note": lambda pid, msg: notes.append((pid, msg)),
        "icon": icon,
    }

    panels = [importlib.import_module("panels." + name) for name in MANIFEST]

    html_parts, css_parts, js_parts = [], [base.CSS], [base.JS]
    for name, p in zip(MANIFEST, panels):
        html_parts.append(f"\n<!-- ===== panel: {p.ID} - {p.TITLE} ===== -->")
        html_parts.append(p.html(ctx))
        if getattr(p, "CSS", None):
            css_parts.append(f"/* ---- {p.ID} ---- */\n{p.CSS}")
        if getattr(p, "JS", None):
            js_parts.append(f"/* ---- {p.ID} ---- */\n{p.JS}")

    # arch.py is shared by hero + steps, so its CSS is added once, up front
    from panels import arch
    css_parts.insert(1, f"/* ---- arch (shared) ---- */\n{arch.CSS}")

    # Everything between #tqdf-root's opening tag and the first section is
    # scaffolding (nav embeds, style blocks) - keep it. Same for the tail.
    pre = body[:spans[0][0]]
    tail = body[spans[-1][1]:]

    page = (head + pre
            + "\n".join(html_parts)
            + "\n<style id=\"nv-styles\">" + "\n".join(css_parts) + "</style>"
            + "\n<script id=\"nv-behaviour\">" + "\n".join(js_parts) + "</script>\n"
            + tail)

    open(OUT, "w", encoding="utf-8").write(page)

    # ---------------- report ----------------
    print(f"\n  {len(panels)} panels assembled -> {OUT}  ({len(page)/1024:.0f} KB)\n")
    for i, (name, p) in enumerate(zip(MANIFEST, panels), 1):
        kind = "reuse" if hasattr(p, "SOURCE_INDEX") else "NEW  "
        print(f"   {i:2d}. [{kind}] {p.TITLE}")
    print("\n  retired from the original:")
    for i, why in sorted(RETIRED.items()):
        print(f"      section {i}: {why}")
    if notes:
        print("\n  panel notes:")
        for pid, msg in notes:
            print(f"      {pid}: {msg}")

    # sanity: every panel id should appear exactly once in the output
    print()
    for p in panels:
        n = page.count(f"panel: {p.ID} ")
        flag = "ok" if n == 1 else f"!! {n}"
        print(f"      {flag:5s} {p.ID}")


if __name__ == "__main__":
    main()
