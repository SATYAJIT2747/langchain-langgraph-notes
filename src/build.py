"""Build index.html from the content files.  Run:  python src/build.py"""
import ast, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content_langchain import LANGCHAIN
from content_langgraph import LANGGRAPH
from content_extras import EXTRAS
from easy import EASY

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTS = [
    ("langchain", "Part I", "LangChain", LANGCHAIN, "PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0"),
    ("langgraph", "Part II", "LangGraph & Agentic AI", LANGGRAPH, "PLKnIA16_RmvYsvB8qkUQuJmJNuiCUJFPL"),
    ("extras", "Part III", "Interview Extras", EXTRAS, None),
]
esc = html.escape


def section(v, n, part_name):
    yt = (f'<a class="yt" href="https://www.youtube.com/watch?v={v["yt"]}" target="_blank" rel="noopener">Watch ↗</a>'
          if v.get("yt") else "")
    dl = "".join(f'<div class="c"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in v["concepts"])
    def lang(c):
        try:
            ast.parse(c); return "python"
        except SyntaxError:
            return "bash"
    def blocks(items):
        return "".join(
            f'<figure class="code"><figcaption><span>{esc(t)}</span><button class="copy" type="button">Copy</button></figcaption>'
            f'<pre><code class="language-{lang(c)}">{esc(c)}</code></pre></figure>' for t, c in items)
    e = EASY.get(v["id"], {})
    keys = "".join(f'<tr><td><code>{esc(k)}</code></td><td>{esc(m)}</td></tr>' for k, m in e.get("keys", []))
    keys = f'<table class="keys"><thead><tr><th>Function / argument</th><th>Means</th></tr></thead><tbody>{keys}</tbody></table>' if keys else ""
    easy = blocks(e.get("easy", []))
    easy_h = (f'<h3 class="sub">Easy example <span class="tag">standalone · copy &amp; run</span></h3>{keys}{easy}'
              if (keys or easy) else "")
    code = blocks(v["code"])
    rem = "".join(f"<li>{r}</li>" for r in v.get("remember", []))
    rem = f'<aside class="remember"><h4>Remember</h4><ul>{rem}</ul></aside>' if rem else ""
    code_h = easy_h + (f'<h3 class="sub">From the lecture <span class="tag">course / project code</span></h3>{code}' if code else "")
    return f'''
<section class="video" id="{v["id"]}" data-title="{esc(v["title"].lower())}">
  <header>
    <p class="kicker">{part_name} · {n:02d}</p>
    <h2>{esc(v["title"])}</h2>
    <p class="meta"><span>{esc(v["dur"])}</span>{yt}
      <label class="done"><input type="checkbox" data-id="{v["id"]}"> Revised</label></p>
  </header>
  <h3 class="sub">Key concepts</h3>
  <dl class="concepts">{dl}</dl>
  {code_h}
  {rem}
</section>'''


nav, body = [], []
total = 0
for pid, plabel, pname, vids, pl in PARTS:
    total += len(vids)
    items = "".join(
        f'<li><a href="#{v["id"]}" data-id="{v["id"]}"><span class="n">{i:02d}</span>{esc(v["title"])}</a></li>'
        for i, v in enumerate(vids, 1))
    nav.append(f'<div class="navpart"><p class="navhead">{plabel} — {esc(pname)}</p><ol>{items}</ol></div>')
    pl_link = (f' <a href="https://www.youtube.com/playlist?list={pl}" target="_blank" rel="noopener">Playlist ↗</a>'
               if pl else "")
    body.append(f'<div class="part" id="{pid}"><p class="kicker">{plabel}</p><h1 class="parttitle">{esc(pname)}</h1>'
                f'<p class="partmeta">{len(vids)} sections{pl_link}</p></div>')
    body += [section(v, i, pname.split(" ")[0]) for i, v in enumerate(vids, 1)]

template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
out = (template.replace("{{NAV}}", "".join(nav))
               .replace("{{BODY}}", "".join(body))
               .replace("{{TOTAL}}", str(total))
               .replace("{{LC}}", str(len(LANGCHAIN)))
               .replace("{{LG}}", str(len(LANGGRAPH)))
               .replace("{{EX}}", str(len(EXTRAS))))
(ROOT / "index.html").write_text(out, encoding="utf-8")
print("built index.html with", total, "sections")
