"""Panel 03 - NEW. Replaces "Context built one app at a time".

A decision is two things: what the agent held true, and what it chose to do.

Origin of the flow line: a connector leaves the bottom of the TRUTH card and
descends out of the section. Panel 04 picks it up at the same x (--nv-axis) and
resolves it into the numbered 1-2-3-4 axis, so truth visibly flows into its four
components.
"""
ID, TITLE = "truth", "Agents need truth (Truth + Judgement)"

HEADING = "Limit agent guesswork with your ground truth"

# Effect of giving an agent machine-readable truth instead of leaving it to infer.
# THESE ARE PLACEHOLDERS, not measured results - the band carries an "Illustrative"
# marker while they are. Replace the values and delete ILLUSTRATIVE when you have
# real figures.
ILLUSTRATIVE = True
METRICS = [
    dict(key="accuracy",      dir="up",   value="+34%", label="Accuracy",
         note="Answers resolve against a governed definition instead of the model's best guess."),
    dict(key="token-cost",    dir="down", value="\u221241%", label="Token cost",
         note="The rule is retrieved once, not re-derived from raw context on every call."),
    dict(key="repeatability", dir="up",   value="+58%", label="Repeatability",
         note="The same question returns the same answer, run to run and team to team."),
]
ARROW = {"up": "&#9650;", "down": "&#9660;"}


def html(ctx):
    metrics = "".join(f'''
        <div class="nv-metric" data-dir="{m['dir']}">
          <span class="nv-metric-arrow">{ARROW[m['dir']]}</span>
          <span class="nv-metric-value">{m['value'] or ''}</span>
          <span class="nv-metric-label">{m['label']}</span>
          <p class="nv-metric-note">{m['note']}</p>
        </div>''' for m in METRICS)

    return f'''
<section class="nv nv-light nv-block nv-truth-sec" id="nv-truth">
  <div class="nv-container">
    <div class="nv-head-full">
      <h2 class="nv-h2">{HEADING}</h2>
      <p class="nv-lede nv-lede-full">Every answer an agent gives is two things at once &mdash;
        what it took to be true, and the leap it made from there. Confuse the two and you can
        review neither.</p>
    </div>

    <div class="nv-split">
      <div class="nv-halfcard nv-halfcard-origin">
        <span class="nv-kicker">Truth</span>
        <h3 class="nv-h3">What you know to be true</h3>
        <p>What a customer is. What a contract commits you to. Which offers someone actually
          qualifies for. The things everyone in the business has to be able to rely on &mdash;
          agreed once by the people accountable for them, then used by everyone and
          everything downstream.</p>
        <p class="nv-note">Settled by your experts &middot; Same answer every time</p>

      </div>

      <div class="nv-halfcard">
        <span class="nv-kicker">Judgement</span>
        <h3 class="nv-h3">Educated guesses</h3>
        <p>Everything the agent infers on top of that &mdash; what it weighs, what it
          prioritises, the call it makes when the answer is not written down anywhere. This is
          the part worth reviewing and coaching, and it is allowed to vary.</p>
        <p class="nv-note">Made by the model &middot; Only as good as what it started from</p>
      </div>
    </div>

    <div class="nv-metrics">
      <div class="nv-metrics-head">
        <span class="nv-kicker">With machine-readable truth</span>
        {'<span class="nv-illus">Illustrative</span>' if ILLUSTRATIVE else ''}
        <p class="nv-metrics-lede">The same model, given context it can resolve against
          rather than infer.</p>
      </div>
      <div class="nv-metricgrid">{metrics}</div>
    </div>

    <span class="nv-flow" aria-hidden="true">
      <span class="nv-flow-track"><span class="nv-flow-fill"></span></span>
    </span>
  </div>
</section>'''


CSS = """
.nv-split{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:36px}
.nv-halfcard{border:1px solid var(--nv-line);background:#fff;padding:28px}
.nv-halfcard .nv-h3{margin:10px 0 12px}
.nv-halfcard p{font-family:var(--nv-body);font-size:.99rem;line-height:1.6;
  color:var(--nv-muted);margin:0 0 10px}
.nv-kicker{color:var(--nv-accent)}
.nv-note{font-family:var(--nv-mono)!important;font-size:11px!important;letter-spacing:.04em;
  color:var(--nv-ink)!important;margin:16px 0 0!important}

/* the flow line leaves the bottom of the TRUTH card and exits the section */
.nv-halfcard-origin{position:relative}
.nv-flow{position:absolute;left:var(--nv-axis,32px);top:100%;width:1px;
  height:var(--nv-flow-drop,104px)}
.nv-flow-track{position:absolute;inset:0;background:var(--nv-line)}
.nv-flow-fill{position:absolute;top:0;left:0;width:1px;height:0;background:var(--nv-accent);
  transition:height .2s linear}

.nv-lede-full{max-width:none}

/* the spine runs the full height of the panel, from the truth cards down into
   the four pillars; the band is indented so the line passes to its left */
.nv-truth-sec{position:relative}
.nv-flow{position:absolute;left:calc((100% - 1180px) / 2 + 32px);top:0;width:1px;height:0}
.nv-metrics{margin:44px 0 0 72px;border-top:1px solid var(--nv-line);padding-top:28px}
.nv-metrics-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.nv-metrics-lede{font-family:var(--nv-body);font-size:.95rem;color:var(--nv-muted);
  margin:0;flex:1 1 320px}
.nv-illus{font-family:var(--nv-mono);font-size:9px;font-weight:600;letter-spacing:.12em;
  text-transform:uppercase;color:var(--nv-muted);border:1px solid var(--nv-line);
  padding:3px 7px}
.nv-metricgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;
  background:var(--nv-line);border:1px solid var(--nv-line);margin-top:24px}
.nv-metric{background:#fff;padding:26px 24px}
.nv-metric-arrow{font-size:12px;line-height:1;color:var(--nv-accent);margin-right:6px}
.nv-metric[data-dir="down"] .nv-metric-arrow{color:#1f9d55}
.nv-metric-value{font-family:var(--nv-display);font-size:clamp(1.8rem,3vw,2.5rem);
  font-weight:700;letter-spacing:-.02em;color:var(--nv-ink)}
.nv-metric-label{display:block;font-family:var(--nv-mono);font-size:10px;font-weight:600;
  letter-spacing:.13em;text-transform:uppercase;color:var(--nv-muted);margin-top:8px}
.nv-metric-note{font-family:var(--nv-body);font-size:.9rem;line-height:1.55;
  color:var(--nv-muted);margin:12px 0 0}

@media (max-width:1040px){.nv-metricgrid{grid-template-columns:1fr}
  .nv-metrics{margin-left:0}}

@media (max-width:1040px){.nv-flow{display:none}}
@media (max-width:720px){.nv-split{grid-template-columns:1fr}}
"""

JS = """
(function () {
  var sec  = document.getElementById('nv-truth');
  var flow = sec && sec.querySelector('.nv-flow');
  var fill = flow && flow.querySelector('.nv-flow-fill');
  var card = sec && sec.querySelector('.nv-halfcard-origin');
  if (!fill || !card) return;

  // span from the bottom of the TRUTH card to the bottom of the section, so the
  // line visibly carries truth past the metrics and into the four pillars
  function size() {
    var sr = sec.getBoundingClientRect(), cr = card.getBoundingClientRect();
    flow.style.top = (cr.bottom - sr.top) + 'px';
    flow.style.height = (sr.bottom - cr.bottom) + 'px';
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
