"""Shared design tokens, layout primitives and the scroll-tracking runtime.

Palette is lifted from the live homepage architecture so the new dark sections
match the design system rather than approximating it:
  hero gradient  #00040a -> #00090f -> #01141f
  panel          #232F3E      node       #1A2531
  hairline       rgba(255,255,255,.16)   accent     #f15a22
"""

CSS = """
.nv{
  --nv-accent:#f15a22; --nv-ink:#0e1a2e; --nv-muted:#5c6b7f;
  --nv-line:#e6e3db; --nv-paper:#fdfcf9;
  --nv-d-panel:#232f3e; --nv-d-node:#1a2531; --nv-d-line:rgba(255,255,255,.16);
  --nv-d-text:#ebeff2; --nv-d-muted:#8fa3b8;
  --nv-gutter:210px; --nv-axis:32px;
  --nv-mono:'JetBrains Mono',ui-monospace,monospace;
  --nv-display:'Hanken Grotesk','Inter',sans-serif;
  --nv-body:'Inter',sans-serif;
}
.nv,.nv *{box-sizing:border-box}
.nv-container{width:100%;max-width:1180px;margin:0 auto;padding:0 32px}
.nv-block{padding:104px 0}
.nv-light{background:var(--nv-paper);color:var(--nv-ink)}
.nv-dark{background:linear-gradient(180deg,#00040a 0%,#00090f 50%,#01141f 100%);
  color:var(--nv-d-text)}

.nv-h1{font-family:var(--nv-display);font-weight:700;font-size:clamp(2.4rem,4.4vw,4rem);
  line-height:1.04;letter-spacing:-.02em;margin:.18em 0 0}
.nv-h2{font-family:var(--nv-display);font-weight:700;font-size:clamp(1.8rem,2.9vw,2.7rem);
  line-height:1.1;letter-spacing:-.015em;margin:0}
.nv-h3{font-family:var(--nv-display);font-weight:600;font-size:1.22rem;line-height:1.25;margin:0}
.nv-accent{color:var(--nv-accent)}
/* Webflow styles h1/h2/h3 directly, so inheriting from .nv-dark loses.
   Set the colour explicitly per scope or dark sections render dark-on-dark. */
.nv-light .nv-h1,.nv-light .nv-h2,.nv-light .nv-h3{color:var(--nv-ink)}
.nv-dark .nv-h1,.nv-dark .nv-h2,.nv-dark .nv-h3{color:#fff}
.nv-dark .nv-h1 .nv-accent,.nv-dark .nv-h2 .nv-accent{color:var(--nv-accent)}
.nv-dark p,.nv-dark li{color:var(--nv-d-text)}
.nv-eyebrow,.nv-kicker,.nv-tierlabel,.nv-boxlabel,.nv-srclabel,.nv-stepnum{
  font-family:var(--nv-mono);font-size:10.5px;font-weight:600;letter-spacing:.13em;
  text-transform:uppercase}
.nv-eyebrow{color:var(--nv-accent)}
.nv-lede{font-family:var(--nv-body);font-size:1.06rem;line-height:1.62;
  color:var(--nv-muted);margin:0}
.nv-dark .nv-lede{color:var(--nv-d-muted)}
.nv-lede-wide{max-width:62ch}
.nv-head-full{margin-bottom:34px}
.nv-head-full .nv-lede{margin-top:16px}

.nv-btn{display:inline-flex;align-items:center;font-family:var(--nv-body);font-size:.94rem;
  font-weight:600;padding:14px 24px;text-decoration:none;border:1px solid transparent;
  transition:background .18s,border-color .18s,color .18s}
.nv-btn-primary{background:var(--nv-accent);color:#fff}
.nv-btn-primary:hover{background:#d94e19}
.nv-btn-ghost{border-color:var(--nv-d-line);color:var(--nv-d-text)}
.nv-btn-ghost:hover{border-color:var(--nv-accent);color:var(--nv-accent)}

@media (max-width:720px){
  .nv-block{padding:68px 0}
  .nv-container{padding:0 20px}
}
/* Surviving Webflow sections use .reveal (opacity:0 until an observer fires).
   If it never fires you get tall empty bands, so force them visible. */
.reveal{opacity:1!important;transform:none!important}

@media (prefers-reduced-motion:reduce){
  .nv [data-track],.nv [data-tier]{opacity:1!important;transform:none!important;
    filter:none!important}
  .nv *{transition:none!important;animation:none!important}
}
"""

# Generic "which of these is nearest the middle of the viewport" tracker.
# Panels opt in by calling nvTrack(items, applyFn).
JS = """
window.nvReduce = window.matchMedia &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

window.nvTrack = function (items, apply) {
  if (!items.length) return;
  if (window.nvReduce) { apply(items.length - 1); return; }
  var active = -1;
  function onScroll() {
    var mid = window.innerHeight * 0.5, best = 0, bestD = Infinity;
    items.forEach(function (el, i) {
      var r = el.getBoundingClientRect();
      var d = Math.abs((r.top + r.height / 2) - mid);
      if (d < bestD) { bestD = d; best = i; }
    });
    if (best !== active) { active = best; apply(best); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
  // Failsafe: never leave a tracked group fully dimmed.
  setTimeout(function () { if (active < 0) apply(0); }, 2000);
};
"""
