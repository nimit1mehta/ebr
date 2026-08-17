"""The three-tier architecture graphic, shared by the hero and the five-step build.

Mirrors the homepage diagram: consumers on top, CONTEXT in the middle split into
Inferred vs Authoritative, your systems underneath.

Two instances, two modes:
  hero  (simple=True)  category labels only, no vendor names - a silhouette
  steps (simple=False) full detail, and it grows tier by tier as the reader
                       scrolls the five steps ("blobs out and creates itself")
"""

F = "./TQ Data Foundation — Power the Context Your AI Needs _ TopQuadrant_files/"

# Full detail, used by the scroll-driven instance.
SOURCE_GROUPS = [
    ("Data lakes", [("Snowflake", "logos_snowflake-icon.svg"), ("Databricks", None)]),
    ("Catalogs",   [("Collibra", None), ("Informatica", None), ("Alation", None)]),
    ("Cloud",      [("AWS", "logos_aws.svg"), ("Azure", "logos_microsoft-azure.svg"),
                    ("Google Cloud", "logos_google-cloud.svg")]),
    ("Databases",  [("Neo4j", "logos_neo4j.svg"), ("PostgreSQL", "logos_postgresql.svg")]),
    ("Analytics",  [("Tableau", "logos_tableau-icon.svg"),
                    ("Power BI", "logos_microsoft-power-bi.svg")]),
]
# Silhouette: categories only, no named systems.
SOURCE_CATEGORIES = ["Lakes", "Catalogs", "Cloud", "Databases", "Analytics"]

CONSUMERS = ["AI applications", "Machine learning", "Data science", "BI & reporting"]
PILLAR_NAMES = ["References", "Ontologies", "Rules", "Processes"]
INFERRED = ["Decision traces", "Trends", "ML insights", "Problems & suggestions"]

# Cumulative build order. "governed" is not a tier - it lights the backdrop once
# everything else is on.
STAGES = ["sources", "inferred", "authoritative", "consumers", "governed"]


def chip(label, icon=None):
    ic = (f'<img src="{F}{icon}" alt="" class="nv-chip-ic">' if icon
          else '<span class="nv-chip-dot" aria-hidden="true"></span>')
    return f'<span class="nv-chip">{ic}<span>{label}</span></span>'


def _sources(simple):
    if simple:
        return ('<div class="nv-srcgrid nv-srcgrid-simple">'
                + "".join(f'<span class="nv-srccat">{c}</span>' for c in SOURCE_CATEGORIES)
                + "</div>")
    return ('<div class="nv-srcgrid">' + "".join(
        f'<div class="nv-srcgroup"><span class="nv-srclabel">{name}</span>'
        f'<div class="nv-srcrow">{"".join(chip(l, i) for l, i in items)}</div></div>'
        for name, items in SOURCE_GROUPS) + "</div>")


def render(scope, simple=False):
    consumers = "".join(f'<span class="nv-node">{c}</span>' for c in CONSUMERS)
    pillars = "".join(f'<span class="nv-pill">{p}</span>' for p in PILLAR_NAMES)
    inferred = "".join(chip(i) for i in INFERRED)
    wires = '<div class="nv-wires" aria-hidden="true">' + "<span></span>" * 4 + "</div>"

    return f'''
<div class="nv-arch{' nv-arch-simple' if simple else ''}" id="{scope}" data-stage="sources">
  <div class="nv-arch-glow" aria-hidden="true"></div>

  <div class="nv-tier nv-tier-consumers" data-tier="consumers">
    <span class="nv-tierlabel">Agents &amp; applications</span>
    <div class="nv-tierbody"><div class="nv-noderow">{consumers}</div></div>
  </div>
  {wires}

  <div class="nv-core">
    <span class="nv-tierlabel">Context</span>
    <div class="nv-corebody">
      <div class="nv-box nv-box-inferred" data-tier="inferred">
        <span class="nv-boxlabel">Inferred context</span>
        <div class="nv-tierbody"><div class="nv-boxrow">{inferred}</div></div>
      </div>
      <div class="nv-box nv-box-auth" data-tier="authoritative">
        <span class="nv-boxlabel nv-boxlabel-auth">Authoritative context</span>
        <div class="nv-tierbody"><div class="nv-boxrow">{pillars}</div></div>
      </div>
    </div>
  </div>
  {wires}

  <div class="nv-tier nv-tier-sources" data-tier="sources">
    <span class="nv-tierlabel">Your systems</span>
    <div class="nv-tierbody">{_sources(simple)}</div>
  </div>
</div>'''


CSS = """
.nv-arch{position:relative;display:flex;flex-direction:column;gap:9px;
  border:1px solid var(--nv-d-line);background:rgba(10,18,30,.55);padding:18px}
.nv-arch-glow{position:absolute;inset:-1px;pointer-events:none;opacity:0;
  transition:opacity .8s ease;
  background:radial-gradient(70% 60% at 50% 50%,rgba(241,90,34,.20),transparent 70%)}
.nv-arch[data-stage="governed"] .nv-arch-glow{opacity:1}
.nv-tier,.nv-core{position:relative;border:1px solid var(--nv-d-line);
  background:var(--nv-d-panel);padding:13px 15px}
.nv-core{border-width:1.5px}
.nv-tierlabel,.nv-boxlabel,.nv-srclabel{display:block;color:var(--nv-d-muted);
  margin-bottom:10px}
.nv-boxlabel-auth{color:var(--nv-accent)}
.nv-noderow,.nv-boxrow,.nv-srcrow{display:flex;flex-wrap:wrap;gap:8px}
.nv-node,.nv-chip,.nv-pill{display:inline-flex;align-items:center;gap:7px;
  background:var(--nv-d-node);border:1px solid var(--nv-d-line);padding:8px 12px;
  font-family:var(--nv-body);font-size:12.5px;font-weight:500;color:var(--nv-d-text);
  white-space:nowrap}
.nv-chip-ic{width:15px;height:15px;flex:none}
.nv-chip-dot{width:5px;height:5px;background:var(--nv-d-muted);flex:none}
.nv-corebody{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}
.nv-box{border:1px solid var(--nv-d-line);background:rgba(13,22,36,.72);padding:12px 13px}
.nv-box-auth{border-color:rgba(241,90,34,.55);
  background:radial-gradient(120% 180% at 12% 0%,rgba(241,90,34,.13),transparent 60%),
             rgba(13,22,36,.72)}
.nv-srcgrid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.nv-srcgroup{display:flex;flex-direction:column;gap:8px}
.nv-srcgroup .nv-srclabel{margin-bottom:0;font-size:9px}
.nv-srcrow{flex-direction:column;gap:6px}
.nv-srcrow .nv-chip{font-size:11.5px;padding:6px 9px}
.nv-wires{display:grid;grid-template-columns:repeat(4,1fr);height:16px;padding:0 18%;
  opacity:.5;transition:height .5s ease,opacity .5s ease}
.nv-wires span{border-left:1px solid var(--nv-d-line);margin:0 auto}

/* ---- silhouette: categories only ---- */
.nv-srcgrid-simple{grid-template-columns:repeat(5,minmax(0,1fr))}
.nv-srccat{display:flex;align-items:center;justify-content:center;text-align:center;
  background:var(--nv-d-node);border:1px solid var(--nv-d-line);padding:12px 8px;
  font-family:var(--nv-mono);font-size:10px;font-weight:600;letter-spacing:.09em;
  text-transform:uppercase;color:var(--nv-d-muted)}
.nv-arch-simple .nv-node,.nv-arch-simple .nv-chip,.nv-arch-simple .nv-pill{font-size:11.5px;
  padding:7px 10px}

@media (max-width:720px){
  .nv-corebody{grid-template-columns:1fr}
  .nv-srcgrid,.nv-srcgrid-simple{grid-template-columns:repeat(2,minmax(0,1fr))}
}
"""
