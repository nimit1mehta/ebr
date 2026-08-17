"""Panel 05 - the truth quote. Attribution retained from the section it replaces."""
ID, TITLE = "quote-truth", "Quote (same truth)"

QUOTE = ("Only when we could give our agents the same truth "
         "could we select those who were effective.")
NAME, ORG = "Chief Data Officer", "Global banking group"


def html(ctx):
    return f'''
<section class="nv nv-light nv-quote-sec" id="nv-quote-truth">
  <div class="nv-container">
    <blockquote class="nv-quote">
      <p>&ldquo;{QUOTE}&rdquo;</p>
      <footer><span class="nv-qname">{NAME}</span>
        <span class="nv-qorg">{ORG}</span></footer>
    </blockquote>
  </div>
</section>'''


CSS = """
.nv-quote-sec{padding:88px 0}
.nv-quote{margin:0;text-align:center}
.nv-quote p{font-family:var(--nv-display);font-weight:500;font-size:clamp(1.5rem,3vw,2.3rem);
  line-height:1.28;letter-spacing:-.012em;color:var(--nv-ink);margin:0 auto;max-width:26ch}
.nv-quote footer{margin-top:26px;display:flex;flex-direction:column;gap:3px}
.nv-qname{font-family:var(--nv-body);font-size:.94rem;font-weight:600}
.nv-qorg{font-family:var(--nv-mono);font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--nv-muted)}
"""
