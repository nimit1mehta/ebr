"""The layered architecture, shared by the hero and the five-step build.

Four layers, sandwiched flush against each other. Bottom to top:

    DATA            your source systems
    CONTEXT   { INFERRED       what the machine derives
              { AUTHORITATIVE  what your experts govern
    AGENTS          what consumes it

Every layer has two levels of detail:
  detail  - everything (Data shows named technologies with logos)
  summary - the condensed form (Data shows its five categories)

The hero renders every layer at summary level, statically.
The five-step build expands the active layer to detail and collapses the ones
you have scrolled past back to summary, so the diagram tells the story of the
step you are reading.
"""

F = "./TQ Data Foundation — Power the Context Your AI Needs _ TopQuadrant_files/"

# Layer order, bottom to top. Also the animation sequence.
SEQUENCE = ["data", "inferred", "authoritative", "agents"]

DATA_GROUPS = [
    ("Lakes",     [("Snowflake", "logos_snowflake-icon.svg"), ("Databricks", None)]),
    ("Catalogs",  [("Collibra", None), ("Informatica", None), ("Alation", None)]),
    ("Cloud",     [("AWS", "logos_aws.svg"), ("Azure", "logos_microsoft-azure.svg"),
                   ("Google Cloud", "logos_google-cloud.svg")]),
    ("Databases", [("Neo4j", "logos_neo4j.svg"), ("PostgreSQL", "logos_postgresql.svg")]),
    ("Analytics", [("Tableau", "logos_tableau-icon.svg"),
                   ("Power BI", "logos_microsoft-power-bi.svg")]),
]
DATA_CATEGORIES = [g[0] for g in DATA_GROUPS]

INFERRED = ["Decision traces", "Trends", "ML insights", "Problems & suggestions"]
AUTHORITATIVE = ["References", "Ontologies", "Rules", "Processes"]
AGENTS = ["AI applications", "Machine learning", "Data science", "BI & reporting"]

SUMMARIES = {
    "data": "5 system categories",
    "inferred": "Derived by the machine",
    "authoritative": "Governed by your experts",
    "agents": "Everything that consumes context",
}


def _chip(label, icon=None, cls="nv-chip"):
    ic = (f'<img src="{F}{icon}" alt="" class="nv-chip-ic">' if icon
          else '<span class="nv-chip-dot" aria-hidden="true"></span>')
    return f'<span class="{cls}">{ic}<span>{label}</span></span>'


def _chips(items, cls="nv-chip"):
    return "".join(_chip(i, None, cls) for i in items)


def _data_detail():
    return '<div class="nv-datagrid">' + "".join(
        f'<div class="nv-datagroup"><span class="nv-grouplabel">{name}</span>'
        f'<div class="nv-groupchips">{"".join(_chip(l, i) for l, i in items)}</div></div>'
        for name, items in DATA_GROUPS) + "</div>"


def _data_summary():
    return ('<div class="nv-catrow">'
            + "".join(f'<span class="nv-cat">{c}</span>' for c in DATA_CATEGORIES)
            + "</div>")


def _layer(key, title, detail, summary):
    return f'''
    <div class="nv-layer" data-layer="{key}">
      <div class="nv-layer-head">
        <span class="nv-layer-name">{title}</span>
        <span class="nv-layer-sum">{SUMMARIES[key]}</span>
      </div>
      <div class="nv-layer-detail">{detail}</div>
      <div class="nv-layer-summary">{summary}</div>
    </div>'''


def _seam():
    """The join between two layers. Lit up at step 5."""
    return ('<div class="nv-seam" aria-hidden="true">'
            + "<span></span>" * 5 + "</div>")


def render(scope, mode="static"):
    agents = _layer("agents", "Agents", _chips(AGENTS, "nv-chip nv-chip-agent"),
                    _chips(AGENTS, "nv-chip nv-chip-agent"))
    auth = _layer("authoritative", "Authoritative",
                  _chips(AUTHORITATIVE, "nv-chip nv-chip-auth"),
                  _chips(AUTHORITATIVE, "nv-chip nv-chip-auth"))
    inferred = _layer("inferred", "Inferred", _chips(INFERRED), _chips(INFERRED))
    data = _layer("data", "Data", _data_detail(), _data_summary())

    return f'''
<div class="nv-arch nv-arch-{mode}" id="{scope}" data-stage="data">
  <div class="nv-arch-glow" aria-hidden="true"></div>

  {agents}
  {_seam()}

  <div class="nv-context">
    <span class="nv-context-label">Context</span>
    {auth}
    {_seam()}
    {inferred}
  </div>

  {_seam()}
  {data}
</div>'''


CSS = """
.nv-arch{position:relative;display:flex;flex-direction:column;
  border:1px solid var(--nv-d-line);background:rgba(8,15,26,.72);padding:14px}
.nv-arch-glow{position:absolute;inset:-1px;pointer-events:none;opacity:0;
  transition:opacity .8s ease;
  background:radial-gradient(70% 60% at 50% 50%,rgba(241,90,34,.22),transparent 70%)}
.nv-arch[data-stage="governed"] .nv-arch-glow{opacity:1}

/* ---- layers stack flush: shared hairlines, no gaps ---- */
.nv-layer{position:relative;border:1px solid var(--nv-d-line);background:var(--nv-d-panel);
  padding:12px 14px;transition:background .4s ease,border-color .4s ease}
.nv-layer + .nv-layer,.nv-context + .nv-layer,.nv-layer + .nv-context{margin-top:-1px}
.nv-layer-head{display:flex;align-items:baseline;gap:12px;margin-bottom:10px}
.nv-layer-name{font-family:var(--nv-mono);font-size:10.5px;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:#fff}
.nv-layer-sum{font-family:var(--nv-body);font-size:11.5px;color:var(--nv-d-muted);
  opacity:0;transition:opacity .4s ease}

/* Context wraps Authoritative + Inferred */
.nv-context{position:relative;border:1.5px solid rgba(241,90,34,.45);
  background:radial-gradient(120% 140% at 50% 0%,rgba(241,90,34,.10),transparent 62%),
             rgba(10,18,30,.55);
  padding:26px 12px 12px;margin:-1px 0}
.nv-context-label{position:absolute;top:8px;left:14px;font-family:var(--nv-mono);
  font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
  color:var(--nv-accent)}
.nv-context .nv-layer{background:rgba(16,26,42,.9)}

/* ---- chips: full contrast, never muted ---- */
.nv-chip{display:inline-flex;align-items:center;gap:7px;background:var(--nv-d-node);
  border:1px solid rgba(255,255,255,.22);padding:8px 12px;font-family:var(--nv-body);
  font-size:12.5px;font-weight:500;color:#fff;white-space:nowrap}
.nv-chip-auth{border-color:rgba(241,90,34,.55);color:#fff}
.nv-chip-agent{border-color:rgba(255,255,255,.3)}
.nv-chip-ic{width:15px;height:15px;flex:none}
.nv-chip-dot{width:5px;height:5px;background:var(--nv-accent);flex:none}
.nv-layer-detail,.nv-layer-summary{display:flex;flex-wrap:wrap;gap:8px}

/* data layer */
.nv-datagrid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;width:100%}
.nv-datagroup{display:flex;flex-direction:column;gap:7px}
.nv-grouplabel{font-family:var(--nv-mono);font-size:9px;font-weight:600;letter-spacing:.1em;
  text-transform:uppercase;color:var(--nv-d-muted)}
.nv-groupchips{display:flex;flex-direction:column;gap:6px}
.nv-groupchips .nv-chip{font-size:11.5px;padding:6px 9px}
.nv-catrow{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;width:100%}
.nv-cat{display:flex;align-items:center;justify-content:center;background:var(--nv-d-node);
  border:1px solid rgba(255,255,255,.22);padding:10px 8px;font-family:var(--nv-mono);
  font-size:10px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:#fff}

/* ---- seams: the joins, lit at step 5 ---- */
.nv-seam{display:grid;grid-template-columns:repeat(5,1fr);height:14px;padding:0 12%;
  position:relative;z-index:1}
.nv-seam span{width:1px;margin:0 auto;background:rgba(255,255,255,.22);
  transition:background .5s ease,box-shadow .5s ease}
.nv-arch[data-stage="governed"] .nv-seam span{background:var(--nv-accent);
  box-shadow:0 0 7px rgba(241,90,34,.85)}

/* ---- static (hero): every layer at summary level ---- */
.nv-arch-static .nv-layer-detail{display:none}

/* ---- build (steps): detail on the active layer, summary once passed ---- */
.nv-arch-build .nv-layer-detail,.nv-arch-build .nv-layer-summary{
  overflow:hidden;transition:max-height .6s cubic-bezier(.2,.7,.2,1),opacity .4s ease}
.nv-arch-build .nv-layer{opacity:.3;transition:opacity .5s ease,border-color .5s ease}
.nv-arch-build .nv-layer.is-live{opacity:1}
.nv-arch-build .nv-layer.is-active{border-color:var(--nv-accent)}
.nv-arch-build .nv-layer.is-active .nv-layer-summary{display:none}
.nv-arch-build .nv-layer:not(.is-active) .nv-layer-detail{display:none}
.nv-arch-build .nv-layer:not(.is-active) .nv-layer-sum{opacity:1}

@media (max-width:720px){
  .nv-datagrid,.nv-catrow{grid-template-columns:repeat(2,minmax(0,1fr))}
}
"""
