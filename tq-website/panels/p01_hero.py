"""Panel 01 - Hero. NEW: dark, left-aligned, category headline, explainer removed."""
from . import arch

ID, TITLE = "hero", "Hero (dark, category message)"

HEADLINE_LEAD = "The Context Management Platform for mastering your"
HEADLINE_ACCENT = "ground truth"


def html(ctx):
    return f'''
<section class="nv nv-dark nv-hero" id="nv-hero">
  <div class="nv-container nv-hero-grid">
    <div class="nv-hero-copy">
      <span class="nv-eyebrow">TQ Data Foundation</span>
      <h1 class="nv-h1">{HEADLINE_LEAD}
        <span class="nv-accent">{HEADLINE_ACCENT}</span></h1>
      <div class="nv-actions">
        <a href="https://topquadrant-spring.webflow.io/contact"
           class="nv-btn nv-btn-primary">Request a Demo</a>
        <a href="#nv-truth" class="nv-btn nv-btn-ghost">See what it answers</a>
      </div>
      <p class="nv-standards">Built entirely on open knowledge-graph standards
        <span>&middot;</span> RDF <span>&middot;</span> OWL <span>&middot;</span> SHACL</p>
    </div>
    <div class="nv-hero-vis" aria-hidden="true">{arch.render("nv-arch-hero", simple=True)}</div>
  </div>
</section>'''


CSS = """
.nv-hero{padding:96px 0 88px;overflow:hidden}
.nv-hero-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.04fr);
  gap:56px;align-items:center}
.nv-hero-copy{max-width:35ch}
.nv-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}
.nv-standards{font-family:var(--nv-mono);font-size:10px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--nv-d-muted);margin:34px 0 0}
.nv-standards span{color:var(--nv-accent);margin:0 2px}
/* the hero instance reads as a silhouette, not a working control */
.nv-hero-vis .nv-arch{transform:scale(.93);transform-origin:center right}
.nv-hero-vis .nv-chip,.nv-hero-vis .nv-node,.nv-hero-vis .nv-pill{color:var(--nv-d-muted)}
@media (max-width:1040px){
  .nv-hero-grid{grid-template-columns:1fr;gap:44px}
  .nv-hero-copy{max-width:none}
  .nv-hero-vis .nv-arch{transform:none}
}
"""
