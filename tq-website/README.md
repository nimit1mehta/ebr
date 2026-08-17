# TQ Data Foundation — product page (restructured)

Working copy of the TQ Data Foundation product page, rebuilt from modular panels.
Source page: `topquadrant-spring.webflow.io/tq-data-foundation`.

**Live preview:** https://nimit1mehta.github.io/ebr/tq-website/
Marked `noindex` — reachable by link, kept out of search results.

## Structure

| File | Purpose |
|---|---|
| `index.html` | Built page. Fully self-contained: CSS, JS, fonts and all images embedded. No network calls. |
| `build_page.py` | Assembles the page from panels. `MANIFEST` is the page order. |
| `inline_build.py` | Embeds every asset, strips tracking, produces the standalone file. |
| `panels/` | One module per section — markup, copy, CSS and JS together. |
| `original.html` | The unmodified saved source page, used as input. |

## Rebuild

```bash
python3 build_page.py                              # -> restructured.html
python3 inline_build.py restructured.html index.html
```

Two inputs are not committed (they are large and re-derivable):

- **Saved page assets.** Open the source page in Chrome, Ctrl+S, "Webpage, Complete".
  Point `D` in `inline_build.py` at the resulting `..._files` folder.
- **Fonts.** `npm pack @fontsource/hanken-grotesk @fontsource/inter @fontsource/jetbrains-mono`,
  extract into `fonts/<pkg>/files/`. Only latin subsets at weights 300–700 are used.

## Editing

Change one section by editing only its module. Reorder or drop sections by editing
`MANIFEST` in `build_page.py`. Both hero and the five-step build share `panels/arch.py`
(`simple=True` renders the hero silhouette).

## Page order

1. Hero — dark, category headline
2. Trusted by — full row
3. Agents need truth — truth vs. judgement
4. Truth is built from four components — scroll-tracked axis
5. Quote
6. A platform custom built for the challenge — five steps drive the architecture build
7. Core capabilities
8. Customer quote + stat tiles
9. Webinar CTA
10. FAQ
11. Closing CTA

Retired from the original: "Context built one app at a time", "Five moves from
scattered data", "Four things sitting between…", the Weyland-Yutani comparison,
the CDO quote, and the previous capabilities grid.

## Notes

- Tracking, consent and chat tags are stripped (HubSpot, LinkedIn, GTM, CookieYes, Finsweet).
- The webinar card's background image is an inline-style URL Chrome never saved; it loads
  when online, with a fallback tint otherwise.
- `.reveal` elements are forced visible — they start at `opacity:0` awaiting an observer
  and leave blank bands when it does not fire.
