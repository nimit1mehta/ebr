"""Panel 07 - NEW copy. Six core capabilities.

Icons are lifted from the iconoir set already baked into the original page as
inline SVG, so they stay offline-safe. ctx["icon"] does the extraction.
"""
ID, TITLE = "capabilities", "Core capabilities (6, iconoir)"

HEADING = "Core capabilities"

CAPABILITIES = [
    dict(icon="iconoir:cube", name="A single layer, independent of source",
         body="One context layer that no single system owns. Your meaning lives above the "
              "warehouse, the catalog and the lake, so it survives every migration "
              "underneath it."),
    dict(icon="iconoir:share-android", name="Open standards",
         body="Modelled on open W3C standards, RDF, OWL, SPARQL, SHACL and SKOS, several of "
              "which our team helped author. Your context is yours: export it and go."),
    dict(icon="iconoir:network", name="Semantic model-backed",
         body="Meaning is native, not bolted on. Concepts, relationships and constraints are "
              "modelled as a graph, so an agent can traverse your business rather than guess "
              "at it."),
    dict(icon="iconoir:shield-check", name="Centralized governance",
         body="Update once, disseminate everywhere. Every change propagates to every connected "
              "system, with full version history and time-travel to the context behind any "
              "past decision."),
    dict(icon="iconoir:brain-electricity", name="Agent-enabled",
         body="Serve governed context to your agents, copilots and apps through MCP, a Python "
              "SDK and REST. Dynamic, machine-readable, always current."),
    dict(icon="iconoir:bookmark-book", name="Marketplace",
         body="Prebuilt ontologies, taxonomies and industry standards, ready to reuse. Start "
              "from proven context packages by domain and use case instead of a blank page."),
]


def html(ctx):
    cards = "".join(f'''
      <article class="nv-cap">
        <span class="nv-cap-ic">{ctx["icon"](c["icon"])}</span>
        <h3 class="nv-h3">{c['name']}</h3>
        <p>{c['body']}</p>
      </article>''' for c in CAPABILITIES)
    return f'''
<section class="nv nv-light nv-block" id="nv-capabilities">
  <div class="nv-container">
    <div class="nv-head-full">
      <h2 class="nv-h2">{HEADING}</h2>
    </div>
    <div class="nv-capgrid">{cards}</div>
  </div>
</section>'''


CSS = """
.nv-capgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
  border-top:1px solid var(--nv-line);border-left:1px solid var(--nv-line)}
.nv-cap{padding:38px 32px;border-right:1px solid var(--nv-line);
  border-bottom:1px solid var(--nv-line)}
/* solid ink tile, white glyph - reads sharply against the cream page */
.nv-cap-ic{display:grid;place-items:center;width:58px;height:58px;margin-bottom:24px;
  background:var(--nv-ink);color:#fff;transition:background .2s ease}
.nv-cap-ic svg{width:30px;height:30px;display:block}
/* iconoir strokes are hairline by default - thicken and snap them to the pixel grid */
.nv-cap-ic svg *{stroke-width:1.9px;vector-effect:non-scaling-stroke;
  shape-rendering:geometricPrecision}
.nv-cap:hover .nv-cap-ic{background:var(--nv-accent)}
.nv-cap .nv-h3{margin:0 0 12px}
.nv-cap p{font-family:var(--nv-body);font-size:.97rem;line-height:1.6;color:var(--nv-muted);
  margin:0}
@media (max-width:1040px){.nv-capgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:720px){.nv-capgrid{grid-template-columns:1fr}}
"""
