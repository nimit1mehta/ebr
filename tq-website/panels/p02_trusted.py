"""Panel 02 - Trusted by. SURVIVING markup, modified.

Changes: two-column head-split becomes one full row, and the
"Global banks, pharma, media and government..." lede is deleted.
Logo wall, six story cards and the 50-70% stat are kept as-is.
"""
import re

ID, TITLE = "trusted", "Trusted by (full row, blurb removed)"
SOURCE_INDEX = 2          # top-level <section> in the original page


def html(ctx):
    s = ctx["section"](SOURCE_INDEX)
    # delete the lede paragraph
    s, n_lede = re.subn(r'<p class="lede">.*?</p>', "", s, count=1, flags=re.S)
    # collapse the two-column header to a single full-width row
    s, n_split = re.subn(r'class="head-split reveal"', 'class="nv-head-row reveal"', s, count=1)
    ctx["note"](ID, f"lede removed: {bool(n_lede)}, head-split collapsed: {bool(n_split)}")
    return s


CSS = """
/* full row header, replacing the original two-column head-split */
.nv-head-row{display:block!important;grid-template-columns:none!important;
  max-width:none!important;margin-bottom:36px}
.nv-head-row .section-title{max-width:34ch}
"""
