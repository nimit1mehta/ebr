"""Panel 09 - webinar CTA. SURVIVING, unmodified.

Note: its background image is an inline-style URL Chrome never saved, so it only
appears when online. A fallback tint is applied in inline_build.py.
"""
ID, TITLE = "webinar", "Webinar CTA"
SOURCE_INDEX = 10


def html(ctx):
    return ctx["section"](SOURCE_INDEX)
