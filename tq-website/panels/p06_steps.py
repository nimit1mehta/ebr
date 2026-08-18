"""Panel 06 - NEW. The five steps, with the architecture building beside them.

One scroll-driven section: step text on the left, the three-tier diagram pinned on
the right, lighting up cumulatively as each step comes into view.
"""
from . import arch

ID, TITLE = "steps", "Platform built for the challenge (steps + arch build)"

HEADING = "A platform that makes your context authoritative"

STEPS = [
    dict(n="01", title="Point at your data", lede="Start from what you already know.",
         body="Point the Foundation at your databases, catalogs, repos, and documents. It "
              "surfaces the models, terms, and relationships already living inside them.",
         stage="data"),
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
         stage="agentic"),
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
      <div class="nv-stepvis">{arch.render("nv-arch-steps", mode="build")}</div>
    </div>
  </div>
</section>'''


CSS = """
.nv-steps-sec{padding-bottom:0}
.nv-steps-sec .nv-head-full{margin-bottom:0}
.nv-steps{display:grid;grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr);gap:56px;
  align-items:start}
/* Lead-in and run-out. A sticky frame is not pinned at the very start or end of
   its container, which left step 1's diagram low and step 5's clipped. Padding
   the step list means the frame is already pinned by the time step 1 is read,
   and still pinned through step 5. */
.nv-steplist{display:flex;flex-direction:column;padding-top:16vh;padding-bottom:20vh}
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
/* The diagram follows the step you are reading. The stack builds bottom-up, so
   the active layer is slid to the reader's eye line rather than making them hunt
   for it at the bottom. It moves on its own easing, slower than the scroll. */
.nv-stepvis{position:sticky;top:0;height:100vh;display:flex;align-items:center;
  overflow:hidden;
  -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 5%,#000 95%,transparent 100%);
  mask-image:linear-gradient(180deg,transparent 0,#000 5%,#000 95%,transparent 100%)}
.nv-stepvis .nv-arch{width:100%}
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
  var frame = document.querySelector('.nv-stepvis');
  if (!steps.length || !box) return;

  // Which slots exist, and which one is blown out, at each step.
  var PLAN = [
    { stage: 'data',          present: ['data'],                                        open: 'data' },
    { stage: 'inferred',      present: ['data', 'context', 'inferred', 'authoritative'], open: 'inferred' },
    { stage: 'authoritative', present: ['data', 'context', 'inferred', 'authoritative'], open: 'authoritative' },
    { stage: 'agentic',       present: ['data', 'context', 'inferred', 'authoritative', 'agentic'], open: 'agentic' },
    { stage: 'governed',      present: ['data', 'context', 'inferred', 'authoritative', 'agentic'], open: null }
  ];

  var slots = {};
  [].slice.call(box.querySelectorAll('[data-slot]')).forEach(function (el) {
    slots[el.dataset.slot] = el;
  });

  // The frame is centred in the viewport and nvTrack activates whichever step is
  // nearest the viewport centre, so the active step's text is already at centre.
  // All that is left is to bring the OPEN layer to the centre of the stack, so it
  // lands level with that text instead of wherever it happens to sit in the pile.
  // Bounded by the stack's own height, so it can never wander out of frame.
  var shift = 0;

  function align() {
    var openSlot = box.querySelector('.nv-slot.is-open');
    // step 5 has nothing open: leave the whole stack centred, which lines it up
    if (!openSlot) { shift = 0; box.style.transform = ''; return; }
    var target = openSlot.querySelector('.nv-layer');
    if (!target) return;

    var br = box.getBoundingClientRect(), tr = target.getBoundingClientRect();
    // rect differences within one transformed element are transform-invariant,
    // so this is correct even mid-animation
    var offsetInBox = (tr.top - br.top) + tr.height / 2;
    shift = (br.height / 2) - offsetInBox;
    box.style.transform = 'translateY(' + shift + 'px)';
  }

  window.nvTrack(steps, function (idx) {
    steps.forEach(function (s, i) { s.classList.toggle('is-on', i === idx); });

    var plan = PLAN[idx] || PLAN[0];
    box.setAttribute('data-stage', plan.stage);

    Object.keys(slots).forEach(function (k) {
      slots[k].classList.toggle('is-present', plan.present.indexOf(k) !== -1);
      slots[k].classList.toggle('is-open', k === plan.open);
    });

    // let the slot heights settle, then bring the open layer to centre
    setTimeout(align, 200);
    setTimeout(align, 700);
    setTimeout(align, 1100);
  });
})();
"""
