"""Panel 06 - NEW. The five steps, with the architecture building beside them.

One scroll-driven section: step text on the left, the three-tier diagram pinned on
the right, lighting up cumulatively as each step comes into view.
"""
from . import arch

ID, TITLE = "steps", "Platform built for the challenge (steps + arch build)"

HEADING = "A platform custom built for the challenge"

STEPS = [
    dict(n="01", title="Point at your data", lede="Start from what you already know.",
         body="Point the Foundation at your databases, catalogs, repos, and documents. It "
              "surfaces the models, terms, and relationships already living inside them.",
         stage="sources"),
    dict(n="02", title="Generate with AI", lede="Let the platform propose the first version.",
         body="AI turns what it found into draft models and definitions your team can react "
              "to. The hard part, a first structure, is already done.",
         stage="inferred"),
    dict(n="03", title="Make it authoritative", lede="Your experts make it authoritative.",
         body="Stakeholders collaborate; subject-matter experts review, refine, and sign off. "
              "Human approval turns the draft into governed, authoritative context.",
         stage="authoritative"),
    dict(n="04", title="Wire it into agents", lede="Serve it where AI is built.",
         body="Deliver approved context to your agents, copilots, and apps through MCP, SDKs, "
              "and your existing stack, living context, not a static export.",
         stage="consumers"),
    dict(n="05", title="Keep it true, automatically", lede="Authoritative stays authoritative.",
         body="The Foundation watches for drift and new context across your systems, flags "
              "what changed, and proposes updates.",
         stage="governed"),
]


def html(ctx):
    steps = "".join(f'''
      <article class="nv-step" data-track data-stage="{s['stage']}">
        <span class="nv-stepnum">Step {s['n']}</span>
        <h3 class="nv-h3">{s['title']}</h3>
        <p class="nv-steplede">{s['lede']}</p>
        <p class="nv-stepbody">{s['body']}</p>
      </article>''' for s in STEPS)

    return f'''
<section class="nv nv-dark nv-block nv-steps-sec" id="nv-steps">
  <div class="nv-container">
    <div class="nv-head-full">
      <h2 class="nv-h2">{HEADING}</h2>
    </div>
    <div class="nv-steps">
      <div class="nv-steplist">{steps}</div>
      <div class="nv-stepvis">{arch.render("nv-arch-steps", simple=False)}</div>
    </div>
  </div>
</section>'''


CSS = """
.nv-steps{display:grid;grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr);gap:56px;
  align-items:start}
.nv-steplist{display:flex;flex-direction:column}
.nv-step{padding:56px 0;border-top:1px solid var(--nv-d-line);opacity:.3;
  transition:opacity .45s ease}
.nv-step:first-child{border-top:0;padding-top:8px}
.nv-step.is-on{opacity:1}
.nv-stepnum{color:var(--nv-accent)}
.nv-step .nv-h3{margin:11px 0 8px;font-size:1.6rem;color:#fff}
.nv-steplede{font-family:var(--nv-body);font-size:1.02rem;font-weight:500;
  color:var(--nv-d-text);margin:0 0 10px}
.nv-stepbody{font-family:var(--nv-body);font-size:.99rem;line-height:1.6;
  color:var(--nv-d-muted);margin:0;max-width:52ch}
.nv-stepvis{position:sticky;top:96px;height:max-content}
/* The architecture builds itself: each tier starts as a collapsed sliver and
   grows to full size as its step arrives, so the diagram assembles on scroll. */
.nv-steps-sec .nv-arch [data-tier]{opacity:.2;filter:saturate(.25);
  transition:opacity .55s ease,filter .55s ease,border-color .55s ease,
             padding .6s cubic-bezier(.2,.7,.2,1)}
.nv-steps-sec .nv-arch [data-tier]{padding-top:9px;padding-bottom:9px}
.nv-steps-sec .nv-arch [data-tier] .nv-tierlabel{margin-bottom:0;
  transition:margin-bottom .6s cubic-bezier(.2,.7,.2,1)}
.nv-steps-sec .nv-arch [data-tier] .nv-tierbody{max-height:0;overflow:hidden;opacity:0;
  transform:translateY(-6px);
  transition:max-height .65s cubic-bezier(.2,.7,.2,1),opacity .45s ease .1s,
             transform .5s ease .1s}
.nv-steps-sec .nv-arch [data-tier].is-on{opacity:1;filter:none;
  padding-top:13px;padding-bottom:13px}
.nv-steps-sec .nv-arch [data-tier].is-on .nv-tierlabel{margin-bottom:10px}
.nv-steps-sec .nv-arch [data-tier].is-on .nv-tierbody{max-height:420px;opacity:1;
  transform:none}
.nv-steps-sec .nv-arch [data-tier].is-focus{border-color:var(--nv-accent)}
/* connectors draw themselves once both ends exist */
.nv-steps-sec .nv-arch .nv-wires{height:0;opacity:0}
.nv-steps-sec .nv-arch[data-stage="authoritative"] .nv-wires,
.nv-steps-sec .nv-arch[data-stage="consumers"] .nv-wires,
.nv-steps-sec .nv-arch[data-stage="governed"] .nv-wires{height:16px;opacity:.5}
@media (max-width:1040px){
  .nv-steps{grid-template-columns:1fr;gap:40px}
  .nv-stepvis{position:static;order:-1}
  .nv-step{padding:34px 0}
}
"""

JS = """
(function () {
  var steps = [].slice.call(document.querySelectorAll('.nv-step'));
  var box   = document.getElementById('nv-arch-steps');
  if (!steps.length || !box) return;
  var ORDER = ['sources', 'inferred', 'authoritative', 'consumers', 'governed'];

  window.nvTrack(steps, function (idx) {
    steps.forEach(function (s, i) { s.classList.toggle('is-on', i === idx); });

    var stage = ORDER[idx] || ORDER[0];
    var upto  = ORDER.indexOf(stage);
    box.setAttribute('data-stage', stage);

    ORDER.forEach(function (name, i) {
      if (name === 'governed') return;          // backdrop glow, not a tier
      var el = box.querySelector('[data-tier="' + name + '"]');
      if (!el) return;
      el.classList.toggle('is-on', i <= upto || stage === 'governed');
      el.classList.toggle('is-focus', name === stage);
    });
  });
})();
"""
