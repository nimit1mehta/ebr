"""Panel 03 - NEW. Replaces "Context built one app at a time".

A decision is two things: what the agent held true, and what it chose to do.

Origin of the flow line: a connector leaves the bottom of the TRUTH card and
descends out of the section. Panel 04 picks it up at the same x (--nv-axis) and
resolves it into the numbered 1-2-3-4 axis, so truth visibly flows into its four
components.
"""
ID, TITLE = "truth", "Agents need truth (Truth + Judgement)"

HEADING = "Your agents need truth so you can evaluate their judgement"


def html(ctx):
    return f'''
<section class="nv nv-light nv-block nv-truth-sec" id="nv-truth">
  <div class="nv-container">
    <div class="nv-head-full">
      <h2 class="nv-h2">{HEADING}</h2>
      <p class="nv-lede nv-lede-wide">Every decision an agent makes is two things at once.
        What it held to be true, and what it chose to do about it. Confuse the two and you
        cannot review either.</p>
    </div>

    <div class="nv-split">
      <div class="nv-halfcard nv-halfcard-origin">
        <span class="nv-kicker">Truth</span>
        <h3 class="nv-h3">What is so</h3>
        <p>The concepts, relationships, rules and processes of your business, governed by
          the people accountable for them. It does not vary by prompt, by model, or by
          which team happened to build the agent.</p>
        <p class="nv-note">Owned by your experts &middot; Versioned &middot; Citable</p>

        <span class="nv-flow" aria-hidden="true">
          <span class="nv-flow-track"><span class="nv-flow-fill"></span></span>
        </span>
      </div>

      <div class="nv-halfcard">
        <span class="nv-kicker">Judgement</span>
        <h3 class="nv-h3">What it decided</h3>
        <p>The reasoning: what the agent weighed, what it prioritised, the call it made.
          This is the part you actually want to assess, coach and improve.</p>
        <p class="nv-note">Owned by the model &middot; Variable by design</p>
      </div>
    </div>
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
.nv-halfcard-origin{position:relative;overflow:visible}
.nv-flow{position:absolute;left:var(--nv-axis,32px);top:100%;width:1px;
  height:var(--nv-flow-drop,104px)}
.nv-flow-track{position:absolute;inset:0;background:var(--nv-line)}
.nv-flow-fill{position:absolute;top:0;left:0;width:1px;height:0;background:var(--nv-accent);
  transition:height .2s linear}

@media (max-width:1040px){.nv-flow{display:none}}
@media (max-width:720px){.nv-split{grid-template-columns:1fr}}
"""

JS = """
(function () {
  var flow = document.querySelector('.nv-flow');
  var fill = flow && flow.querySelector('.nv-flow-fill');
  if (!fill) return;
  if (window.nvReduce) { fill.style.height = '100%'; return; }

  function onScroll() {
    var r = flow.getBoundingClientRect();
    // fills as the connector crosses the lower half of the viewport
    var p = (window.innerHeight * 0.72 - r.top) / Math.max(r.height, 1);
    fill.style.height = (Math.max(0, Math.min(1, p)) * 100) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();
"""
