"""Panel 10 - FAQ accordion. SURVIVING, unmodified (Webflow JS drives the toggles)."""
ID, TITLE = "faq", "FAQ"
SOURCE_INDEX = 11


def html(ctx):
    return ctx["section"](SOURCE_INDEX)
