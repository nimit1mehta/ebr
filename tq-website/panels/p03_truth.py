"""Panel 03 - NEW. Replaces "Context built one app at a time".

The truth definition on the left, the effect of making it machine-readable on the
right. No Judgement card - the figures occupy that space instead, unboxed, so the
definition stays the only object on the page here.

Also the origin of the spine: a line leaves the definition and runs down into panel
04, where it resolves into the numbered 1-2-3-4 axis of the four assets.
"""
ID, TITLE = "truth", "Limit agent guesswork (truth + impact figures)"

HEADING = "Limit agent guesswork with your ground truth"

# Effect of giving an agent machine-readable truth instead of leaving it to infer.
# THESE ARE PLACEHOLDERS, not measured results - the panel carries an "Illustrative"
# marker while they are. Replace the values and set ILLUSTRATIVE = False when you
# have real figures.
ILLUSTRATIVE = True

METRICS = [
    dict(dir="up",   value="+34%", label="Accuracy",
         note="Answers resolve against a governed definition instead of the model's best guess."),
    dict(dir="down", value="−41%", label="Token cost",
         note="The rule is retrieved once, not re-derived from raw context on every call."),
    dict(dir="up",   value="+58%", label="Repeatability",
         note="The same question returns the same answer, run to run and team to team."),
]
ARROW = {"up": "&#9650;", "down": "&#9660;"}


def html(ctx):
    figures = "".join(f'''
        <div class="nv-figure" data-dir="{m['dir']}">
          <div class="nv-figure-top">
            <span class="nv-figure-arrow">{ARROW[m['dir']]}</span>
            <span class="nv-figure-value">{m['value']}</span>
            <span class="nv-figure-label">{m['label']}</span>
          </div>
          <p class="nv-figure-note">{m['note']}</p>
        </div>''' for m in METRICS)

    illus = '<span class="nv-illus">Illustrative</span>' if ILLUSTRATIVE else ''

    return f'''
<section class="nv nv-light nv-block nv-truth-sec" id="nv-truth">
  <div class="nv-container">
    <div class="nv-head-full">
      <h2 class="nv-h2">{HEADING}</h2>
      <p class="nv-lede nv-lede-full">Every answer an agent gives is two things at once &mdash;
        what it took to be true, and the leap it made from there. Settle the first and the
        second stops being a guess.</p>
    </div>

    <div class="nv-truthgrid">
      <div class="nv-halfcard nv-halfcard-origin">
        <h3 class="nv-h3">What you know to be true</h3>
        <p>What a customer is. What a contract commits you to. Which offers someone actually
          qualifies for. The things everyone in the business has to be able to rely on &mdash;
          agreed once by the people accountable for them, then used by everyone and
          everything downstream.</p>
        <p class="nv-note">Settled by your experts &middot; Same answer every time</p>
      </div>

      <div class="nv-figures">
        <div class="nv-figures-head">
          <span class="nv-kicker">Impact</span>{illus}
        </div>
        {figures}
      </div>
    </div>

    <span class="nv-flow" aria-hidden="true">
      <span class="nv-flow-track"><span class="nv-flow-fill"></span></span>
    </span>
  </div>
</section>'''


CSS = """
.nv-lede-full{max-width:none}
.nv-truth-sec{position:relative}

.nv-truthgrid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
  gap:48px;margin-top:36px;align-items:stretch}
.nv-figures{display:flex;flex-direction:column}
.nv-figure:last-child{flex:1}

/* the definition stays the one object on the page here */
.nv-halfcard{border:1px solid var(--nv-line);background:#fff;padding:30px;height:100%}
.nv-halfcard .nv-h3{margin:0 0 12px}
.nv-halfcard p{font-family:var(--nv-body);font-size:.99rem;line-height:1.6;
  color:var(--nv-muted);margin:0 0 10px}
.nv-kicker{color:var(--nv-accent)}
.nv-note{font-family:var(--nv-mono)!important;font-size:11px!important;letter-spacing:.04em;
  color:var(--nv-ink)!important;margin:16px 0 0!important}

/* figures sit on the page itself - no cards, hairlines only */
.nv-figures{padding-top:4px}
.nv-figures-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  padding-bottom:18px}
.nv-illus{font-family:var(--nv-mono);font-size:9px;font-weight:600;letter-spacing:.12em;
  text-transform:uppercase;color:var(--nv-muted);border:1px solid var(--nv-line);
  padding:3px 7px}
.nv-figure{padding:22px 0;border-top:1px solid var(--nv-line)}
.nv-figure:last-child{padding-bottom:0}
.nv-figure-top{display:flex;align-items:baseline;gap:10px}
.nv-figure-arrow{font-size:11px;line-height:1;color:var(--nv-accent)}
.nv-figure[data-dir="down"] .nv-figure-arrow{color:#1f9d55}
.nv-figure-value{font-family:var(--nv-display);font-size:clamp(1.9rem,3.1vw,2.6rem);
  font-weight:700;letter-spacing:-.02em;color:var(--nv-ink);line-height:1}
.nv-figure-label{font-family:var(--nv-mono);font-size:10px;font-weight:600;
  letter-spacing:.13em;text-transform:uppercase;color:var(--nv-muted)}
.nv-figure-note{font-family:var(--nv-body);font-size:.93rem;line-height:1.55;
  color:var(--nv-muted);margin:10px 0 0;max-width:46ch}

/* spine: leaves the definition and carries down into the four assets */
.nv-flow{position:absolute;left:0;top:0;width:1px;height:0}
.nv-flow-track{position:absolute;inset:0;background:var(--nv-line)}
.nv-flow-fill{position:absolute;top:0;left:0;width:1px;height:0;background:var(--nv-accent);
  transition:height .2s linear}

@media (max-width:1040px){
  .nv-truthgrid{grid-template-columns:1fr;gap:32px}
  .nv-flow{display:none}
}
"""

JS = """
(function () {
  var sec  = document.getElementById('nv-truth');
  var flow = sec && sec.querySelector('.nv-flow');
  var fill = flow && flow.querySelector('.nv-flow-fill');
  var card = sec && sec.querySelector('.nv-halfcard-origin');
  if (!fill || !card) return;

  // span from the bottom of the definition to the bottom of the section, so the
  // line visibly carries truth into the four assets below
  var box = sec.querySelector('.nv-container');

  function size() {
    var sr = sec.getBoundingClientRect(), cr = card.getBoundingClientRect();
    flow.style.top = (cr.bottom - sr.top) + 'px';
    flow.style.height = Math.max(0, sr.bottom - cr.bottom) + 'px';
    // The pillars axis sits at (container content left + --nv-axis). Measure the
    // same origin here rather than recomputing it from viewport maths, so the two
    // segments read as one line at any width.
    var cs = getComputedStyle(box);
    var axis = parseFloat(getComputedStyle(document.documentElement)
                 .getPropertyValue('--nv-axis')) || 32;
    var contentLeft = box.getBoundingClientRect().left + parseFloat(cs.paddingLeft);
    flow.style.left = (contentLeft - sr.left + axis) + 'px';
  }
  function draw() {
    var r = flow.getBoundingClientRect();
    var p = (window.innerHeight * 0.72 - r.top) / Math.max(r.height, 1);
    fill.style.height = (Math.max(0, Math.min(1, p)) * 100) + '%';
  }
  function update() { size(); draw(); }

  if (window.nvReduce) { size(); fill.style.height = '100%'; return; }
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
  setTimeout(update, 600);
})();
"""
