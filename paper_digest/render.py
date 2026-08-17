"""Markdown / HTML の一覧を書き出す。"""

from __future__ import annotations

import html
import json
import logging
from collections import Counter
from datetime import datetime
from pathlib import Path

from .models import Paper

log = logging.getLogger("paper_digest")


def _venue_group(paper: Paper) -> str:
    return paper.venue or (f"arXiv {paper.year}" if paper.year else "unknown")


# ---------------------------------------------------------------- Markdown
def render_markdown(papers: list[Paper], path: Path, *, title: str = "論文ダイジェスト") -> None:
    lines: list[str] = []
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"生成日時: {stamp} / 収録 {len(papers)} 件")
    lines.append("")

    by_topic: dict[str, list[Paper]] = {}
    for p in papers:
        by_topic.setdefault(p.topic or "Other", []).append(p)
    order = sorted(by_topic, key=lambda t: (-len(by_topic[t]), t))

    lines.append("## トピック")
    lines.append("")
    for t in order:
        anchor = t.lower().replace(" ", "-").replace("/", "")
        lines.append(f"- [{t}](#{anchor}) — {len(by_topic[t])} 件")
    lines.append("")

    for t in order:
        lines.append(f"## {t}")
        lines.append("")
        for p in by_topic[t]:
            lines.append(f"### {p.title}")
            lines.append("")
            lines.append(f"{_venue_group(p)} / {p.topic or 'Other'}")
            lines.append("")
            if p.summary_ja:
                lines.append("**概要**")
                lines.append("")
                lines.append(p.summary_ja)
                lines.append("")
            if p.novelty_ja:
                lines.append("**新規性**")
                lines.append("")
                lines.append(p.novelty_ja)
                lines.append("")
            if p.why_read_ja:
                lines.append("**読む理由**")
                lines.append("")
                lines.append(p.why_read_ja)
                lines.append("")
            if not p.summary_ja:
                lines.append("*(日本語要約は未生成。`paper-digest summarize` を実行してください)*")
                lines.append("")
            lines.append(f"- Paper: {p.paper_url or '-'}")
            lines.append(f"- Code: {p.code_url or '-'}")
            lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Markdown を書き出しました: %s", path)


# -------------------------------------------------------------------- HTML
_HTML_TEMPLATE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  color-scheme: light dark;
  --bg: #f6f7f9; --card: #ffffff; --fg: #14171a; --muted: #5b6570;
  --line: #dfe3e8; --accent: #1f6feb; --chip: #eef2f7;
}
@media (prefers-color-scheme: dark) {
  :root { --bg:#12151a; --card:#1a1f27; --fg:#e6e9ef; --muted:#9aa4b2;
          --line:#2a313c; --accent:#6ea8fe; --chip:#232a34; }
}
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Noto Sans JP",
               "Yu Gothic UI", Meiryo, sans-serif; line-height:1.7; }
header { position:sticky; top:0; z-index:10; background:var(--bg);
  border-bottom:1px solid var(--line); padding:14px 20px 12px; }
h1 { margin:0 0 2px; font-size:19px; }
.meta { color:var(--muted); font-size:12px; margin-bottom:10px; }
.controls { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
input[type=search], select {
  font:inherit; font-size:13px; padding:7px 10px; border:1px solid var(--line);
  border-radius:8px; background:var(--card); color:var(--fg); }
input[type=search] { flex:1 1 260px; min-width:200px; }
#count { color:var(--muted); font-size:12px; margin-left:auto; white-space:nowrap; }
main { max-width:960px; margin:0 auto; padding:18px 20px 60px; }
article { background:var(--card); border:1px solid var(--line); border-radius:12px;
  padding:16px 18px; margin-bottom:14px; }
article h2 { margin:0 0 8px; font-size:16px; line-height:1.5; }
article h2 a { color:var(--fg); text-decoration:none; }
article h2 a:hover { color:var(--accent); text-decoration:underline; }
.chips { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }
.chip { font-size:11px; padding:2px 9px; border-radius:999px;
  background:var(--chip); color:var(--muted); border:1px solid var(--line); }
.chip.venue { color:var(--accent); border-color:var(--accent); }
.sec { margin:8px 0; }
.sec b { display:block; font-size:12px; color:var(--muted); font-weight:600;
  letter-spacing:.04em; margin-bottom:1px; }
.links { margin-top:10px; font-size:13px; display:flex; gap:14px; flex-wrap:wrap; }
.links a { color:var(--accent); }
details.abs { margin-top:8px; font-size:13px; color:var(--muted); }
details.abs summary { cursor:pointer; font-size:12px; }
.empty { text-align:center; color:var(--muted); padding:60px 0; }
</style>
</head>
<body>
<header>
  <h1>__TITLE__</h1>
  <div class="meta">生成日時: __STAMP__ / 収録 __TOTAL__ 件</div>
  <div class="controls">
    <input type="search" id="q" placeholder="キーワード検索 (タイトル・要約・abstract)">
    <select id="venue"></select>
    <select id="topic"></select>
    <select id="sort">
      <option value="new">新しい順</option>
      <option value="old">古い順</option>
      <option value="rel">関連度順</option>
      <option value="title">タイトル順</option>
    </select>
    <span id="count"></span>
  </div>
</header>
<main id="list"></main>
<script type="application/json" id="data">__DATA__</script>
<script>
const PAPERS = JSON.parse(document.getElementById("data").textContent);
const $ = (id) => document.getElementById(id);
const esc = (s) => (s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

function fillSelect(el, label, values) {
  el.innerHTML = `<option value="">${label} (すべて)</option>` +
    values.map(v => `<option value="${esc(v)}">${esc(v)}</option>`).join("");
}
const uniq = (key) => [...new Set(PAPERS.map(p => p[key]).filter(Boolean))].sort();
fillSelect($("venue"), "発表先", uniq("venue"));
fillSelect($("topic"), "トピック", uniq("topic"));

function sortKey(p) { return p.published || (p.year ? String(p.year) : ""); }

function render() {
  const q = $("q").value.trim().toLowerCase();
  const venue = $("venue").value, topic = $("topic").value, sort = $("sort").value;
  let rows = PAPERS.filter(p => {
    if (venue && p.venue !== venue) return false;
    if (topic && p.topic !== topic) return false;
    if (!q) return true;
    return (p.title + " " + p.summary_ja + " " + p.novelty_ja + " " +
            p.why_read_ja + " " + p.abstract + " " + (p.topics || []).join(" ")
           ).toLowerCase().includes(q);
  });
  rows.sort((a, b) => {
    if (sort === "title") return a.title.localeCompare(b.title);
    if (sort === "rel") return (b.relevance || 0) - (a.relevance || 0);
    const c = sortKey(a) < sortKey(b) ? -1 : sortKey(a) > sortKey(b) ? 1 : 0;
    return sort === "old" ? c : -c;
  });
  $("count").textContent = `${rows.length} / ${PAPERS.length} 件`;
  $("list").innerHTML = rows.length ? rows.map(card).join("") :
    '<div class="empty">該当する論文がありません</div>';
}

function card(p) {
  const sec = (label, text) => text ? `<div class="sec"><b>${label}</b>${esc(text)}</div>` : "";
  const chips = [
    p.venue ? `<span class="chip venue">${esc(p.venue)}</span>` : "",
    p.topic ? `<span class="chip">${esc(p.topic)}</span>` : "",
    ...(p.topics || []).filter(t => t !== p.topic).map(t => `<span class="chip">${esc(t)}</span>`),
  ].join("");
  const links = [
    p.paper_url ? `<a href="${esc(p.paper_url)}" target="_blank" rel="noopener">Paper</a>` : "",
    p.code_url ? `<a href="${esc(p.code_url)}" target="_blank" rel="noopener">Code</a>` : "",
  ].filter(Boolean).join("");
  const abs = p.abstract
    ? `<details class="abs"><summary>Abstract (原文)</summary>${esc(p.abstract)}</details>` : "";
  const title = p.paper_url
    ? `<a href="${esc(p.paper_url)}" target="_blank" rel="noopener">${esc(p.title)}</a>`
    : esc(p.title);
  const body = p.summary_ja
    ? sec("概要", p.summary_ja) + sec("新規性", p.novelty_ja) + sec("読む理由", p.why_read_ja)
    : `<div class="sec"><b>概要</b>(日本語要約は未生成)</div>`;
  return `<article><h2>${title}</h2><div class="chips">${chips}</div>${body}
    <div class="links">${links}</div>${abs}</article>`;
}

["q", "venue", "topic", "sort"].forEach(id => {
  $(id).addEventListener(id === "q" ? "input" : "change", render);
});
render();
</script>
</body>
</html>
"""


def render_html(papers: list[Paper], path: Path, *, title: str = "論文ダイジェスト") -> None:
    payload = [
        {
            "title": p.title,
            "venue": _venue_group(p),
            "year": p.year,
            "topic": p.topic or "Other",
            "topics": p.topics,
            "abstract": p.abstract,
            "summary_ja": p.summary_ja,
            "novelty_ja": p.novelty_ja,
            "why_read_ja": p.why_read_ja,
            "paper_url": p.paper_url,
            "code_url": p.code_url,
            "published": p.published,
            "relevance": p.relevance,
        }
        for p in papers
    ]
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    doc = (_HTML_TEMPLATE
           .replace("__TITLE__", html.escape(title))
           .replace("__STAMP__", datetime.now().strftime("%Y-%m-%d %H:%M"))
           .replace("__TOTAL__", str(len(payload)))
           .replace("__DATA__", data))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")
    log.info("HTML を書き出しました: %s", path)


def render_output(papers: list[Paper], out: Path, *, title: str = "論文ダイジェスト") -> None:
    """拡張子で md / html を振り分ける。"""
    suffix = out.suffix.lower()
    if suffix in (".html", ".htm"):
        render_html(papers, out, title=title)
    elif suffix in (".md", ".markdown", ""):
        render_markdown(papers, out, title=title)
    else:
        raise SystemExit(f"未対応の出力形式です: {out.suffix} (.md か .html を指定してください)")


def summarize_counts(papers: list[Paper]) -> str:
    venues = Counter(_venue_group(p) for p in papers)
    topics = Counter(p.topic or "Other" for p in papers)
    top_v = ", ".join(f"{k} {v}" for k, v in venues.most_common(5))
    top_t = ", ".join(f"{k} {v}" for k, v in topics.most_common(5))
    return f"発表先: {top_v}\nトピック: {top_t}"
