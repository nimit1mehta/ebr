"""Panel 04 - NEW. The four components of truth, on a scroll-tracked axis.

Continues the flow line from panel 03 at the same x (--nv-axis): the line runs the
full height of this section and carries four numbered stops. The number lives only
on the axis, never on the card.

Copy carried over verbatim from the retired "Four things sitting between your data
and your agents" panel.
"""
ID, TITLE = "pillars", "Truth is built from four components (scroll axis)"

HEADING = "Truth is built from four components"

PILLARS = [
    dict(n="1", name="References", q="What are the core things?",
         body="The concepts your business runs on (customers, products, suppliers, country "
              "and currency codes) each given one canonical identifier, so the same thing is "
              "recognized the same way across every system.",
         tags=["Taxonomies", "Reference data", "Glossaries", "Code lists"]),
    dict(n="2", name="Ontologies", q="How do they connect?",
         body="How those entities relate (a customer places an order, a supplier ships a "
              "product, an employee owns an account) modeled so AI captures how your business "
              "actually thinks, not just what sits in a table.",
         tags=["Ontologies", "Conceptual models", "RDF / OWL", "Linked data"]),
    dict(n="3", name="Rules", q="What's allowed?",
         body="The policies that make context trustworthy (validation, access permissions, "
              "retention, and compliance mappings like GDPR and HIPAA) enforced directly in "
              "the data, so AI stays governed and explainable by design.",
         tags=["Policy-as-code", "SHACL constraints", "Validation rules", "Access controls"]),
    dict(n="4", name="Processes", q="How does work get done?",
         body="A machine-understandable map of how work actually flows (order-to-cash, "
              "onboarding, approval chains) so AI understands the sequences, states, and "
              "decisions your business runs on, not just data at rest.",
         tags=["Process models", "Workflows", "Lineage"]),
]


def html(ctx):
    cards = "".join(f'''
      <article class="nv-pcard" data-track>
        <h3 class="nv-h3">{p['name']}</h3>
        <p class="nv-pq">{p['q']}</p>
        <p class="nv-pbody">{p['body']}</p>
        <div class="nv-ptags">{''.join(f'<span>{t}</span>' for t in p['tags'])}</div>
      </article>''' for p in PILLARS)

    stops = "".join(f'''
      <li class="nv-stop">
        <span class="nv-stopnum">{p['n']}</span>
        <span class="nv-stopname">{p['name']}</span>
      </li>''' for p in PILLARS)

    return f'''
<section class="nv nv-light nv-block nv-pillars-sec" id="nv-pillars">
  <div class="nv-container nv-axis-grid">

    <aside class="nv-axis" aria-hidden="true">
      <div class="nv-axis-line"><span class="nv-axis-fill"></span></div>
      <ol class="nv-stops">{stops}</ol>
    </aside>

    <div class="nv-axis-body">
      <div class="nv-head-full">
        <h2 class="nv-h2">{HEADING}</h2>
      </div>
      <div class="nv-pcards">{cards}</div>
    </div>
  </div>
</section>'''


CSS = """
.nv-axis-grid{display:grid;grid-template-columns:var(--nv-gutter,210px) minmax(0,1fr);
  gap:44px;align-items:start;position:relative}
/* the line spans the whole section, so it reads as one continuous run from panel 03 */
.nv-axis{position:relative;align-self:stretch}
.nv-axis-line{position:absolute;top:calc(-1 * var(--nv-block-pad,104px));bottom:0;
  left:var(--nv-axis,32px);width:1px;background:var(--nv-line)}
.nv-axis-fill{position:absolute;top:0;left:0;width:1px;height:0;background:var(--nv-accent);
  transition:height .45s cubic-bezier(.2,.7,.2,1)}
.nv-stops{list-style:none;margin:0;padding:0;position:sticky;top:150px;
  display:flex;flex-direction:column;gap:28px}
.nv-stop{position:relative;display:flex;align-items:center;gap:14px}
.nv-stopnum{position:relative;z-index:1;flex:none;width:28px;height:28px;
  margin-left:calc(var(--nv-axis,32px) - 14px);display:grid;place-items:center;
  border:1px solid var(--nv-line);border-radius:50%;background:var(--nv-paper);
  font-family:var(--nv-mono);font-size:11px;font-weight:600;color:var(--nv-muted);
  transition:border-color .3s ease,color .3s ease,background .3s ease,transform .3s ease}
.nv-stopname{font-family:var(--nv-display);font-size:1rem;font-weight:600;
  color:var(--nv-muted);opacity:.45;transition:opacity .3s ease,color .3s ease}
.nv-stop.is-done .nv-stopnum{border-color:var(--nv-accent);color:var(--nv-accent)}
.nv-stop.is-on .nv-stopnum{border-color:var(--nv-accent);background:var(--nv-accent);
  color:#fff;transform:scale(1.16)}
.nv-stop.is-on .nv-stopname,.nv-stop.is-done .nv-stopname{opacity:1;color:var(--nv-ink)}

.nv-pcards{display:flex;flex-direction:column;gap:18px}
.nv-pcard{border:1px solid var(--nv-line);background:#fff;padding:32px 34px;opacity:.5;
  transform:translateY(14px);
  transition:opacity .5s ease,transform .5s ease,border-color .5s ease}
.nv-pcard.is-on{opacity:1;transform:none;border-color:#d9d4c8}
.nv-pcard .nv-h3{margin:0 0 4px;font-size:1.5rem}
.nv-pq{font-family:var(--nv-body);font-size:1rem;color:var(--nv-accent);margin:0 0 14px}
.nv-pbody{font-family:var(--nv-body);font-size:1.02rem;line-height:1.62;color:var(--nv-muted);
  margin:0;max-width:66ch}
.nv-ptags{display:flex;flex-wrap:wrap;gap:7px;margin-top:20px}
.nv-ptags span{font-family:var(--nv-mono);font-size:10px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--nv-muted);border:1px solid var(--nv-line);padding:6px 10px}

@media (max-width:1040px){
  .nv-axis-grid{grid-template-columns:1fr;gap:0}
  .nv-axis{display:none}
}
"""

JS = """
(function () {
  var cards = [].slice.call(document.querySelectorAll('.nv-pcard'));
  var stops = [].slice.call(document.querySelectorAll('.nv-stop'));
  var fill  = document.querySelector('.nv-axis-fill');
  if (!cards.length) return;

  window.nvTrack(cards, function (idx) {
    // cards accumulate, so component 1 stays readable when you reach 4
    cards.forEach(function (c, i) { c.classList.toggle('is-on', i <= idx); });
    stops.forEach(function (s, i) {
      s.classList.toggle('is-on', i === idx);
      s.classList.toggle('is-done', i < idx);
    });
    if (fill && stops.length > 1) {
      fill.style.height = (((idx + 1) / stops.length) * 100) + '%';
    }
  });
})();
"""
