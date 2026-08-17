"""Panel 11 - closing CTA. SURVIVING, unmodified."""
ID, TITLE = "cta", "Closing CTA"
SOURCE_INDEX = 12


def html(ctx):
    return ctx["section"](SOURCE_INDEX)
