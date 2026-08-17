"""Panel modules for the TQ Data Foundation page.

Each panel is self-contained and exposes:
    ID     short slug, used in the build manifest and as the section's DOM id
    TITLE  human label, printed in the build report
    html(ctx)  -> markup string
    CSS    (optional) styles scoped to this panel
    JS     (optional) behaviour for this panel

`ctx` carries shared helpers and the sections extracted from the original page,
so panels that survive from the live site can reuse their original markup
instead of being re-authored.
"""
