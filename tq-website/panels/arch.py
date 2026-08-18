"""The layered architecture, shared by the hero and the five-step build.

Four layers, sandwiched flush. Bottom to top:

    DATA                      your source systems, shown as logos
    CONTEXT { INFERRED
            { AUTHORITATIVE
    AGENTIC                   what consumes the context

Each layer lives in a "slot" that animates its own height, so appearing and
expanding are gradual rather than discrete. Three states per slot:

    absent   - not there yet (height 0)
    present  - name only, no detail
    open     - detail blown out

The hero renders every layer present with only AUTHORITATIVE open.
The five-step build brings slots in and opens them one at a time.
"""

F = "./TQ Data Foundation — Power the Context Your AI Needs _ TopQuadrant_files/"

SEQUENCE = ["data", "inferred", "authoritative", "agentic"]

# Category names stay put; the logos blow out underneath them.
# (label, asset). Asset is a saved-page file, "logos/x.svg" for a mark sourced
# from npm, or None where no open-licensed mark exists - those render as a
# monogram tile of the same size so the grid still lines up.
DATA_GROUPS = [
    ("Lakes",     [("Snowflake", "logos_snowflake-icon.svg"),
                   ("Databricks", "logos/databricks.svg")]),
    ("Catalogs",  [("Collibra", None), ("Informatica", "logos/informatica.svg"),
                   ("Alation", None)]),
    ("Cloud",     [("AWS", "logos_aws.svg"), ("Azure", "logos_microsoft-azure.svg"),
                   ("Google Cloud", "logos_google-cloud.svg")]),
    ("Databases", [("Neo4j", "logos_neo4j.svg"),
                   ("PostgreSQL", "logos_postgresql.svg")]),
    ("Analytics", [("Tableau", "logos_tableau-icon.svg"),
                   ("Power BI", "logos_microsoft-power-bi.svg")]),
]

INFERRED = ["Decision traces", "Trends", "ML insights", "Problems & suggestions"]
AUTHORITATIVE = ["References", "Ontologies", "Rules", "Processes"]
AGENTIC = ["Agents", "AI applications", "Machine learning", "BI & reporting"]


def _chips(items, extra=""):
    return "".join(
        f'<span class="nv-chip {extra}"><span class="nv-chip-dot" aria-hidden="true"></span>'
        f'<span>{i}</span></span>' for i in items)


def _mark(label, asset):
    """One 34px tile. Same footprint whether it holds a logo or a monogram."""
    if asset is None:
        mono = "".join(w[0] for w in label.split())[:2].upper()
        return (f'<span class="nv-logo nv-logo-mono" title="{label}">'
                f'<span>{mono}</span></span>')
    src = asset if asset.startswith("logos/") else F + asset
    src = "./" + src if asset.startswith("logos/") else src
    return f'<span class="nv-logo" title="{label}"><img src="{src}" alt="{label}"></span>'


def _data_body():
    """Category names always visible; logo marks expand beneath each."""
    return '<div class="nv-datagrid">' + "".join(
        f'<div class="nv-datagroup"><span class="nv-grouplabel">{name}</span>'
        f'<div class="nv-logos">' + "".join(_mark(l, i) for l, i in items)
        + '</div></div>'
        for name, items in DATA_GROUPS) + "</div>"


def _layer(key, title, body, always=""):
    """`always` renders outside the collapsible body, so it never moves."""
    return f'''
      <div class="nv-layer" data-layer="{key}">
        <span class="nv-layer-name">{title}</span>
        {always}
        <div class="nv-layer-body">{body}</div>
      </div>'''


def _seam():
    return '<div class="nv-seam" aria-hidden="true">' + "<span></span>" * 5 + "</div>"


def render(scope, mode="static"):
    # hero: everything present, only authoritative open
    p = " is-present" if mode == "static" else ""
    open_auth = " is-open" if mode == "static" else ""

    agentic = f'''
  <div class="nv-slot{p}" data-slot="agentic">
    {_layer("agentic", "Agentic", _chips(AGENTIC, "nv-chip-agentic"))}
    {_seam()}
  </div>'''

    context = f'''
  <div class="nv-slot{p}" data-slot="context">
    <div class="nv-context">
      <span class="nv-context-label">Context</span>
      <div class="nv-slot{p}{open_auth}" data-slot="authoritative">
        {_layer("authoritative", "Authoritative", _chips(AUTHORITATIVE, "nv-chip-auth"))}
        {_seam()}
      </div>
      <div class="nv-slot{p}" data-slot="inferred">
        {_layer("inferred", "Inferred", _chips(INFERRED))}
      </div>
    </div>
    {_seam()}
  </div>'''

    data = f'''
  <div class="nv-slot{p}" data-slot="data">
    {_layer("data", "Data", _data_body())}
  </div>'''

    return f'''
<div class="nv-arch nv-arch-{mode}" id="{scope}" data-stage="data">
  <div class="nv-arch-glow" aria-hidden="true"></div>
  {agentic}
  {context}
  {data}
</div>'''


CSS = """
.nv-arch{position:relative;display:flex;flex-direction:column;
  border:1px solid var(--nv-d-line);background:rgba(8,15,26,.72);padding:14px;
  transition:transform .9s cubic-bezier(.22,.61,.36,1)}
.nv-arch-glow{position:absolute;inset:-1px;pointer-events:none;opacity:0;
  transition:opacity 1s ease;
  background:radial-gradient(70% 60% at 50% 50%,rgba(241,90,34,.18),transparent 70%)}
.nv-arch[data-stage="governed"] .nv-arch-glow{opacity:1}

/* ---- slots: gradual appear / disappear ---- */
.nv-slot{overflow:hidden;max-height:0;opacity:0;
  transition:max-height .9s cubic-bezier(.2,.7,.2,1),opacity .6s ease}
.nv-slot.is-present{max-height:760px;opacity:1}

/* ---- layers: flush stack, name pinned ---- */
.nv-layer{position:relative;border:1px solid var(--nv-d-line);background:var(--nv-d-panel);
  padding:12px 14px;transition:border-color .5s ease,background .5s ease}
.nv-layer-name{display:block;font-family:var(--nv-mono);font-size:10.5px;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:#fff}
/* the collapsible part; the name above it never moves */
.nv-layer-body{overflow:hidden;max-height:0;opacity:0;
  display:flex;flex-wrap:wrap;gap:8px;
  transition:max-height .85s cubic-bezier(.2,.7,.2,1),opacity .55s ease,
             margin-top .85s cubic-bezier(.2,.7,.2,1)}
.nv-slot.is-open > .nv-layer > .nv-layer-body{max-height:420px;opacity:1;margin-top:11px}

/* ---- context group: neutral, no accent box ---- */
.nv-context{position:relative;border:1px solid var(--nv-d-line);background:rgba(13,22,36,.5);
  padding:24px 10px 10px;margin:-1px 0}
.nv-context-label{position:absolute;top:7px;left:12px;font-family:var(--nv-mono);
  font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
  color:var(--nv-d-muted)}
.nv-context .nv-layer{background:rgba(18,29,46,.92)}

/* ---- chips ---- */
.nv-chip{display:inline-flex;align-items:center;gap:7px;background:var(--nv-d-node);
  border:1px solid rgba(255,255,255,.22);padding:8px 12px;font-family:var(--nv-body);
  font-size:12.5px;font-weight:500;color:#fff;white-space:nowrap}
.nv-chip-dot{width:5px;height:5px;background:var(--nv-accent);flex:none}
.nv-chip-auth{border-color:rgba(241,90,34,.5)}

/* ---- data: names fixed, logos blow out ---- */
.nv-datagrid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;width:100%}
.nv-datagroup{display:flex;flex-direction:column;gap:8px}
.nv-grouplabel{font-family:var(--nv-mono);font-size:9px;font-weight:600;letter-spacing:.1em;
  text-transform:uppercase;color:var(--nv-d-muted)}
/* fixed 3-up grid: every category's tiles occupy the same slots, so the
   rows across all five categories line up regardless of how many marks each has */
.nv-logos{display:grid;grid-template-columns:repeat(3,34px);gap:6px;justify-content:start}
.nv-logo{display:grid;place-items:center;width:34px;height:34px;background:var(--nv-d-node);
  border:1px solid rgba(255,255,255,.22)}
.nv-logo img{width:19px;height:19px;display:block}
/* no open-licensed mark available - same tile, brand initials */
.nv-logo-mono span{font-family:var(--nv-mono);font-size:10px;font-weight:700;
  letter-spacing:.04em;color:var(--nv-d-muted)}

/* the category names stay visible even when the layer is closed */
.nv-slot[data-slot="data"] .nv-layer-body{max-height:34px;opacity:1;margin-top:11px}
.nv-slot[data-slot="data"] .nv-logos{max-height:0;overflow:hidden;opacity:0;
  transition:max-height .85s cubic-bezier(.2,.7,.2,1),opacity .55s ease}
.nv-slot[data-slot="data"].is-open .nv-layer-body{max-height:420px}
.nv-slot[data-slot="data"].is-open .nv-logos{max-height:120px;opacity:1}

/* ---- seams, lit at step 5 ---- */
.nv-seam{display:grid;grid-template-columns:repeat(5,1fr);height:14px;padding:0 12%;
  position:relative;z-index:1}
.nv-seam span{width:1px;margin:0 auto;background:rgba(255,255,255,.2);
  transition:background .7s ease,box-shadow .7s ease}
/* step 5: the connections pulse, and the rim of the whole plane breathes with them */
@keyframes nv-seam-pulse{
  0%,100%{opacity:.3;box-shadow:0 0 0 rgba(241,90,34,0)}
  50%    {opacity:1;box-shadow:0 0 9px rgba(241,90,34,.95)}}
@keyframes nv-rim-pulse{
  0%,100%{box-shadow:0 0 0 1px rgba(241,90,34,.28),0 0 20px rgba(241,90,34,.08)}
  50%    {box-shadow:0 0 0 1px rgba(241,90,34,.85),0 0 40px rgba(241,90,34,.28)}}
.nv-arch[data-stage="governed"] .nv-seam span{background:var(--nv-accent);
  animation:nv-seam-pulse 2.4s ease-in-out infinite}
.nv-arch[data-stage="governed"] .nv-seam span:nth-child(2){animation-delay:.12s}
.nv-arch[data-stage="governed"] .nv-seam span:nth-child(3){animation-delay:.24s}
.nv-arch[data-stage="governed"] .nv-seam span:nth-child(4){animation-delay:.36s}
.nv-arch[data-stage="governed"] .nv-seam span:nth-child(5){animation-delay:.48s}
.nv-arch[data-stage="governed"]{border-color:rgba(241,90,34,.5);
  animation:nv-rim-pulse 2.4s ease-in-out infinite}

/* ---- build: dim what is not the current step ---- */
.nv-arch-build .nv-layer{opacity:.42;transition:opacity .6s ease,border-color .5s ease}
.nv-arch-build .nv-slot.is-open > .nv-layer{opacity:1;border-color:rgba(241,90,34,.55)}
.nv-arch-build[data-stage="governed"] .nv-layer{opacity:.92}

@media (max-width:720px){.nv-datagrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
"""
