#!/usr/bin/env python3
"""
Build a fully self-contained single-file copy of the TQ Data Foundation page.

Everything the page needs to render is embedded: CSS, JS, fonts, images.
Zero network requests, so it renders inside the network-sandboxed Cowork
artifact panel.
"""
import base64, io, os, re, sys
from PIL import Image

D    = "/sessions/keen-magical-turing/mnt/TQ Data Foundation — Power the Context Your AI Needs _ TopQuadrant_files"
SRC  = sys.argv[1] if len(sys.argv) > 1 else "original.html"
OUT  = sys.argv[2] if len(sys.argv) > 2 else "tq-data-foundation-selfcontained.html"
FONT = "fonts"
LOGOS = "logos"   # brand marks sourced from npm, embedded like any other asset
F    = "./TQ Data Foundation — Power the Context Your AI Needs _ TopQuadrant_files/"

# JS that actually drives rendering / interaction. Everything else is dropped.
KEEP_JS = {
    "jquery-3.5.1.min.dc5e7f18c8.js",
    "webflow.schunk.7321a5097fb66f41.js",
    "webflow.751e0867.148dc658e77a3916.js",
    "6a78489be1dd29d210549a5a_tqdf-tqd.js",
    "6a72ddcba29eccb88244f4c8_tqdf-foundation.js",
    "6a72ddcba29eccb88244f4ec_tqdf-kga.js",
}
# Story-card covers: shipped at 1260x1260, displayed far smaller.
JPG_MAX, JPG_Q = 640, 74

MIME = {".svg": "image/svg+xml", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"}

log = {"css": [], "js_kept": [], "js_dropped": [], "img": 0, "img_bytes": 0, "missing": []}

# 1x1 transparent GIF, for stubbing out images we deliberately do not want fetched.
PIXEL = ("data:image/gif;base64,"
         "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")


def disk(name):
    """Resolve a saved-page reference to a real file, tolerating Chrome's .download suffix."""
    for cand in (name, name + ".download"):
        p = os.path.join(D, cand)
        if os.path.isfile(p):
            return p
    return None


def local_logo(name):
    p = os.path.join(LOGOS, name)
    return p if os.path.isfile(p) else None


def read_text(name):
    p = disk(name)
    if not p:
        log["missing"].append(name)
        return None
    return open(p, encoding="utf-8", errors="replace").read()


def data_uri(name):
    p = disk(name)
    if not p:
        log["missing"].append(name)
        return None
    ext = os.path.splitext(name)[1].lower()
    raw = open(p, "rb").read()
    if ext in (".jpg", ".jpeg"):
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if max(im.size) > JPG_MAX:
            im.thumbnail((JPG_MAX, JPG_MAX), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=JPG_Q, optimize=True, progressive=True)
        raw = buf.getvalue()
    log["img"] += 1
    log["img_bytes"] += len(raw)
    return "data:%s;base64,%s" % (MIME.get(ext, "application/octet-stream"),
                                  base64.b64encode(raw).decode())


def build_font_css():
    """Replace the Google Fonts stylesheet (147 gstatic @font-face rules) with
    embedded latin woff2 for only the three families and five weights in use."""
    fams = [("Hanken Grotesk", "hanken-grotesk"), ("Inter", "inter"),
            ("JetBrains Mono", "jetbrains-mono")]
    out, n = [], 0
    for family, pkg in fams:
        for w in (300, 400, 500, 600, 700):
            p = os.path.join(FONT, pkg, "files", f"{pkg}-latin-{w}-normal.woff2")
            if not os.path.isfile(p):
                log["missing"].append(p)
                continue
            b64 = base64.b64encode(open(p, "rb").read()).decode()
            out.append(
                "@font-face{font-family:'%s';font-style:normal;font-weight:%d;"
                "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}"
                % (family, w, b64))
            n += 1
    print(f"  fonts embedded : {n} faces")
    return "\n".join(out)


def main():
    s = open(SRC, encoding="utf-8").read()
    orig_len = len(s)

    # ---- 1. strip tracking, consent, chat, and browser-extension cruft ----------
    def kill_script(m):
        t = m.group(0)
        src = re.search(re.escape(F) + r'([^"]*)', t)
        name = (src.group(1) if src else "").replace(".download", "")
        if name in KEEP_JS:
            return t
        log["js_dropped"].append(name or "inline/remote")
        return ""

    s = re.sub(r'<script\b[^>]*\bsrc="\./TQ Data Foundation[^"]*"[^>]*>\s*</script>',
               kill_script, s)
    s = re.sub(r'<script\b[^>]*\bsrc="https?://[^"]*"[^>]*>\s*</script>', "", s)
    s = re.sub(r'<iframe\b[^>]*saved_resource\.html[^>]*>\s*</iframe>', "", s)
    s = re.sub(r'<script\b[^>]*>(?:(?!</script>)[\s\S])*?'
               r'(?:googletagmanager|_linkedin_partner_id|_hsq|cookieyes|CookieYes|hs-scripts)'
               r'(?:(?!</script>)[\s\S])*?</script>', "", s, flags=re.I)
    s = re.sub(r'<div id="chrome-extension-pull-out-tab-host">[\s\S]*?</div>\s*(?=</body>|$)', "", s)
    # webfont.js is gone (it would fetch Google Fonts); the wf-*-active classes it
    # sets are already baked into <html>, so just remove the orphaned loader call.
    s = re.sub(r'<script[^>]*>\s*WebFont\.load\((?:(?!</script>)[\s\S])*?</script>', "", s)
    # icons are already baked in as inline <svg>; drop favicon/webclip requests
    s = re.sub(r'<link[^>]*rel="(?:shortcut )?icon"[^>]*>', "", s)
    s = re.sub(r'<link[^>]*rel="apple-touch-icon"[^>]*>', "", s)
    # no network at all: drop connection hints to hosts we no longer use
    s = re.sub(r'<link[^>]*rel="(?:preconnect|dns-prefetch|preload)"[^>]*>', "", s)

    # ---- 2. inline every stylesheet ---------------------------------------------
    def inline_css(m):
        name = m.group(1)
        if name == "css":                      # the Google Fonts sheet
            log["css"].append("google-fonts -> embedded woff2")
            return "<style>\n" + build_font_css() + "\n</style>"
        css = read_text(name)
        if css is None:
            return ""
        log["css"].append(f"{name} ({len(css)//1024} KB)")
        return "<style>\n" + css + "\n</style>"

    s = re.sub(r'<link[^>]*href="' + re.escape(F) + r'([^"]*)"[^>]*>', inline_css, s)

    # ---- 3. inline the render-critical JS ---------------------------------------
    def inline_js(m):
        name = m.group(1).replace(".download", "")
        js = read_text(name)
        if js is None:
            return ""
        # The Webflow runtime builds a "Made in Webflow" badge and fetches its two
        # icons from cloudfront. We hide the badge in CSS; neutralise the URLs so it
        # does not fire blocked requests either.
        js = re.sub(r'https://d3e54v103j8qbb\.cloudfront\.net/img/webflow-badge[^"\')]*',
                    PIXEL, js)
        log["js_kept"].append(f"{name} ({len(js)//1024} KB)")
        return "<script>\n" + js + "\n</script>"

    s = re.sub(r'<script\b[^>]*\bsrc="' + re.escape(F) + r'([^"]*)"[^>]*>\s*</script>',
               inline_js, s)

    # ---- 4. every image becomes a data: URI -------------------------------------
    def inline_img(m):
        uri = data_uri(m.group(2))
        return m.group(1) + (uri or "") + '"'

    s = re.sub(r'(<img[^>]*\bsrc=")' + re.escape(F) + r'([^"]*)"', inline_img, s)
    s = re.sub(r'(\bposter=")' + re.escape(F) + r'([^"]*)"', inline_img, s)

    def inline_logo(m):
        p = local_logo(m.group(2))
        if not p:
            log["missing"].append("logos/" + m.group(2))
            return m.group(1) + '"'
        raw = open(p, "rb").read()
        log["img"] += 1; log["img_bytes"] += len(raw)
        return (m.group(1) + "data:image/svg+xml;base64,"
                + base64.b64encode(raw).decode() + '"')

    s = re.sub(r'(<img[^>]*\bsrc=")\./logos/([^"]*)"', inline_logo, s)

    # Webflow ships responsive variants (-p-500/-p-800...) via srcset, pointing at
    # absolute CDN URLs that Chrome never saved. The browser prefers srcset over
    # src, so these MUST go or the embedded data: images are ignored.
    n_srcset = len(re.findall(r'\ssrcset="', s))
    s = re.sub(r'\ssrcset="[^"]*"', "", s)
    s = re.sub(r'\ssizes="[^"]*"', "", s)
    log["srcset_stripped"] = n_srcset

    # ---- 5. artifact-panel hardening -------------------------------------------
    # light mode, plus a failsafe so scroll-reveal sections can never stay invisible
    inject = """
<style id="tq-artifact-fix">
:root { color-scheme: light; }
html, body { background:#fdfcf9; }
/* Injected by webflow.schunk.js on webflow.io hosts - not part of the design. */
.w-webflow-badge { display:none !important; }
/* The webinar card's background image is an inline-style URL Chrome never saved.
   Keep the real URL (correct in a browser) and tint behind it for offline views. */
a.w-fig { background-color:#e8e4dc; }
</style>
<style id="tq-local-edit">/* local working copy - add overrides below */</style>
</head>"""
    s = s.replace("</head>", inject, 1)

    failsafe = """
<script id="tq-reveal-failsafe">
// Scroll-reveal elements start at opacity:0 and rely on an observer firing.
// Inside a panel that can silently not happen, so guarantee visibility.
(function () {
  function showAll() {
    document.querySelectorAll('.reveal:not(.in)').forEach(function (el) {
      el.classList.add('in');
    });
  }
  window.addEventListener('load', function () { setTimeout(showAll, 1500); });
  setTimeout(showAll, 4000);
})();
</script>
</body>"""
    s = s.replace("</body>", failsafe, 1)

    open(OUT, "w", encoding="utf-8").write(s)

    # ---- report -----------------------------------------------------------------
    leftover = re.findall(r'(?:src|href)="(?:\.|https?:)[^"]*"', s)
    remote = [x for x in leftover if "http" in x and "data:" not in x]
    print(f"\n  source         : {orig_len/1024:.0f} KB  ->  output {len(s)/1024:.0f} KB")
    print(f"  stylesheets    : {len(log['css'])}")
    for c in log["css"]:
        print("     +", c)
    print(f"  scripts kept   : {len(log['js_kept'])}")
    for j in log["js_kept"]:
        print("     +", j)
    print(f"  scripts dropped: {len(log['js_dropped'])} -> {', '.join(sorted(set(log['js_dropped'])))}")
    print(f"  images inlined : {log['img']}  ({log['img_bytes']/1024:.0f} KB raw before base64)")
    print(f"  local refs left: {s.count(F)}")
    print(f"  missing files  : {log['missing'] or 'none'}")
    print(f"  remote refs    : {len(remote)}")
    for r in sorted(set(remote))[:12]:
        print("     ?", r[:110])


if __name__ == "__main__":
    main()
