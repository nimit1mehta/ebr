"""Panel 08 - pharma quote + the 40+ / Weeks / 419+ stat tiles. SURVIVING, unmodified."""
ID, TITLE = "quote-stats", "Customer quote + stat tiles"
SOURCE_INDEX = 9


def html(ctx):
    return ctx["section"](SOURCE_INDEX)
