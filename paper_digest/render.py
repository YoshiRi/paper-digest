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
  --good: #1a7f37; --warn: #9a6700; --danger: #cf222e;
}
@media (prefers-color-scheme: dark) {
  :root { --bg:#12151a; --card:#1a1f27; --fg:#e6e9ef; --muted:#9aa4b2;
          --line:#2a313c; --accent:#6ea8fe; --chip:#232a34;
          --good:#56d364; --warn:#d29922; --danger:#ff7b72; }
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
input[type=search], input[type=number], input[type=text], select, textarea {
  font:inherit; font-size:13px; padding:7px 10px; border:1px solid var(--line);
  border-radius:8px; background:var(--card); color:var(--fg); }
input[type=search] { flex:1 1 260px; min-width:200px; }
textarea { width:100%; min-height:68px; resize:vertical; display:block; }
button, .file-btn {
  font:inherit; font-size:12px; line-height:1; padding:8px 10px; border:1px solid var(--line);
  border-radius:8px; background:var(--card); color:var(--fg); cursor:pointer; }
button:hover, .file-btn:hover { border-color:var(--accent); color:var(--accent); }
button.active { border-color:var(--accent); color:var(--accent); background:var(--chip); }
button.good.active { border-color:var(--good); color:var(--good); }
button.warn.active { border-color:var(--warn); color:var(--warn); }
button.danger.active { border-color:var(--danger); color:var(--danger); }
#count, #savedCount { color:var(--muted); font-size:12px; white-space:nowrap; }
#count { margin-left:auto; }
main { max-width:1240px; margin:0 auto; padding:18px 20px 60px;
  display:grid; grid-template-columns:minmax(260px, 330px) minmax(0, 1fr); gap:16px; align-items:start; }
.workspace { position:sticky; top:105px; display:flex; flex-direction:column; gap:12px; }
.panel { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:14px; }
.panel h2 { margin:0 0 10px; font-size:14px; }
.panel-row { display:flex; gap:8px; align-items:center; margin-top:8px; }
.panel-row > * { flex:1 1 auto; min-width:0; }
.panel-actions { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
.panel small { color:var(--muted); display:block; line-height:1.5; margin-top:8px; }
.survey-list { display:flex; flex-direction:column; gap:8px; margin-top:10px; }
.survey-item { border-top:1px solid var(--line); padding-top:8px; font-size:12px; }
.survey-item b { display:block; font-size:12px; line-height:1.4; }
.survey-item span { color:var(--muted); }
.feed { min-width:0; }
article { background:var(--card); border:1px solid var(--line); border-radius:8px;
  padding:16px 18px; margin-bottom:14px; }
article h2 { margin:0 0 8px; font-size:16px; line-height:1.5; }
article h2 a { color:var(--fg); text-decoration:none; }
article h2 a:hover { color:var(--accent); text-decoration:underline; }
.quick { display:flex; flex-wrap:wrap; gap:6px; margin:10px 0; }
.chips { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }
.chip { font-size:11px; padding:2px 9px; border-radius:999px;
  background:var(--chip); color:var(--muted); border:1px solid var(--line); }
.chip.venue { color:var(--accent); border-color:var(--accent); }
.chip.state { color:var(--good); border-color:var(--good); }
.sec { margin:8px 0; }
.sec b { display:block; font-size:12px; color:var(--muted); font-weight:600;
  letter-spacing:.04em; margin-bottom:1px; }
.links { margin-top:10px; font-size:13px; display:flex; gap:14px; flex-wrap:wrap; }
.links a { color:var(--accent); }
details.abs { margin-top:8px; font-size:13px; color:var(--muted); }
details.abs summary { cursor:pointer; font-size:12px; }
.reader-notes { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:10px; }
.reader-notes label { display:block; font-size:11px; color:var(--muted); }
.reader-notes textarea { margin-top:4px; min-height:58px; }
.empty { text-align:center; color:var(--muted); padding:60px 0; }
@media (max-width: 880px) {
  header { position:static; }
  .controls { align-items:stretch; }
  .controls input[type=search], .controls select {
    flex:1 1 100%; min-width:0; width:100%;
  }
  .controls button, .controls .file-btn { flex:0 0 auto; }
  #count, #savedCount { flex:1 1 100%; }
  main { display:block; padding:12px 12px 48px; }
  .workspace { position:static; margin-bottom:14px; }
  .reader-notes { grid-template-columns:1fr; }
  #count { margin-left:0; }
}
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
    <select id="state">
      <option value="">状態 (すべて)</option>
      <option value="favorite">お気に入り</option>
      <option value="later">あとで読む</option>
      <option value="reading">読んでる</option>
      <option value="read">読んだ</option>
      <option value="skip">見送り</option>
    </select>
    <select id="sort">
      <option value="new">新しい順</option>
      <option value="old">古い順</option>
      <option value="rel">関連度順</option>
      <option value="marked">マーク優先</option>
      <option value="title">タイトル順</option>
    </select>
    <button id="exportState" title="読書状態をJSONで保存">Export</button>
    <label class="file-btn" title="読書状態JSONを読み込む">Import<input type="file" id="importState" accept="application/json" hidden></label>
    <span id="count"></span>
    <span id="savedCount"></span>
  </div>
</header>
<main>
  <section class="workspace">
    <div class="panel">
      <h2>Ask</h2>
      <textarea id="askInput" placeholder="質問"></textarea>
      <div class="panel-row">
        <select id="askLimit">
          <option value="8">上位8件</option>
          <option value="15">上位15件</option>
          <option value="30">上位30件</option>
        </select>
      </div>
      <div class="panel-actions">
        <button id="buildAsk">Prompt</button>
        <button id="copyAsk">Copy</button>
      </div>
      <textarea id="askOutput" readonly placeholder="LLMに渡す文脈"></textarea>
    </div>
    <div class="panel">
      <h2>Survey</h2>
      <textarea id="surveyQuery" placeholder="query"></textarea>
      <div class="panel-row">
        <input type="number" id="surveySince" min="2010" max="2100" value="2025" title="since">
        <input type="number" id="surveyLimit" min="1" max="500" value="150" title="limit">
      </div>
      <div class="panel-row">
        <select id="surveySources">
          <option value="arxiv,cvf">arxiv,cvf</option>
          <option value="arxiv">arxiv</option>
          <option value="cvf">cvf</option>
          <option value="arxiv,cvf,semanticscholar">arxiv,cvf,semanticscholar</option>
        </select>
      </div>
      <div class="panel-row">
        <input type="text" id="surveyVenues" value="CVPR,ICCV,ECCV" title="venues">
      </div>
      <div class="panel-actions">
        <button id="saveSurvey">Queue</button>
        <button id="exportSurveys">Export</button>
      </div>
      <div class="survey-list" id="surveyList"></div>
    </div>
  </section>
  <section class="feed" id="list"></section>
</main>
<script type="application/json" id="data">__DATA__</script>
<script>
const PAPERS = JSON.parse(document.getElementById("data").textContent);
const $ = (id) => document.getElementById(id);
const esc = (s) => (s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const STATE_KEY = "paper-digest-reader-state-v1";
const SURVEY_KEY = "paper-digest-survey-requests-v1";
const STATE_LABELS = { later:"あとで読む", reading:"読んでる", read:"読んだ", skip:"見送り" };
let paperState = loadJson(STATE_KEY, {});
let surveyRequests = loadJson(SURVEY_KEY, []);
let currentRows = [];

function loadJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function saveJson(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch {}
}

function paperKey(p) { return p.key || p.paper_url || p.title; }
function getState(key) { return paperState[key] || {}; }
function hasSavedState(s) { return !!(s.favorite || s.status || s.memo || s.questions); }
function savePaperState() { saveJson(STATE_KEY, paperState); updateStateSummary(); }

function setPaperState(key, patch, rerender = true) {
  const next = { ...getState(key), ...patch };
  Object.keys(next).forEach(k => {
    if (next[k] === "" || next[k] === false || next[k] == null) delete next[k];
  });
  if (hasSavedState(next)) paperState[key] = next;
  else delete paperState[key];
  savePaperState();
  if (rerender) render();
}

function downloadJson(name, value) {
  const blob = new Blob([JSON.stringify(value, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = name; a.click();
  URL.revokeObjectURL(url);
}

async function copyText(text) {
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const tmp = document.createElement("textarea");
    tmp.value = text; document.body.appendChild(tmp); tmp.select();
    document.execCommand("copy"); tmp.remove();
  }
}

function fillSelect(el, label, values) {
  el.innerHTML = `<option value="">${label} (すべて)</option>` +
    values.map(v => `<option value="${esc(v)}">${esc(v)}</option>`).join("");
}
const uniq = (key) => [...new Set(PAPERS.map(p => p[key]).filter(Boolean))].sort();
fillSelect($("venue"), "発表先", uniq("venue"));
fillSelect($("topic"), "トピック", uniq("topic"));

function sortKey(p) { return p.published || (p.year ? String(p.year) : ""); }

function filteredRows() {
  const q = $("q").value.trim().toLowerCase();
  const venue = $("venue").value, topic = $("topic").value;
  const state = $("state").value;
  return PAPERS.filter(p => {
    const saved = getState(paperKey(p));
    if (venue && p.venue !== venue) return false;
    if (topic && p.topic !== topic) return false;
    if (state === "favorite" && !saved.favorite) return false;
    if (state && state !== "favorite" && saved.status !== state) return false;
    if (!q) return true;
    return (p.title + " " + p.summary_ja + " " + p.novelty_ja + " " + p.why_read_ja +
            " " + p.abstract + " " + (p.topics || []).join(" ") + " " +
            (saved.memo || "") + " " + (saved.questions || "")
           ).toLowerCase().includes(q);
  });
}

function render() {
  const sort = $("sort").value;
  let rows = filteredRows();
  rows.sort((a, b) => {
    if (sort === "title") return a.title.localeCompare(b.title);
    if (sort === "rel") return (b.relevance || 0) - (a.relevance || 0);
    if (sort === "marked") {
      const sa = getState(paperKey(a)), sb = getState(paperKey(b));
      const wa = (sa.favorite ? 8 : 0) + (sa.status ? 4 : 0) + (sa.memo ? 2 : 0) + (sa.questions ? 1 : 0);
      const wb = (sb.favorite ? 8 : 0) + (sb.status ? 4 : 0) + (sb.memo ? 2 : 0) + (sb.questions ? 1 : 0);
      if (wa !== wb) return wb - wa;
    }
    const c = sortKey(a) < sortKey(b) ? -1 : sortKey(a) > sortKey(b) ? 1 : 0;
    return sort === "old" ? c : -c;
  });
  currentRows = rows;
  $("count").textContent = `${rows.length} / ${PAPERS.length} 件`;
  $("list").innerHTML = rows.length ? rows.map(card).join("") :
    '<div class="empty">該当する論文がありません</div>';
  hydrateTextareas();
  updateStateSummary();
}

function card(p) {
  const key = paperKey(p);
  const saved = getState(key);
  const sec = (label, text) => text ? `<div class="sec"><b>${label}</b>${esc(text)}</div>` : "";
  const stateChip = saved.status ? `<span class="chip state">${esc(STATE_LABELS[saved.status])}</span>` : "";
  const chips = [
    p.venue ? `<span class="chip venue">${esc(p.venue)}</span>` : "",
    p.topic ? `<span class="chip">${esc(p.topic)}</span>` : "",
    stateChip,
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
  return `<article data-key="${esc(key)}"><h2>${title}</h2><div class="chips">${chips}</div>
    <div class="quick">
      <button data-action="favorite" data-key="${esc(key)}" class="${saved.favorite ? "active" : ""}" title="お気に入り">★</button>
      <button data-status="later" data-key="${esc(key)}" class="${saved.status === "later" ? "active warn" : ""}">あとで読む</button>
      <button data-status="reading" data-key="${esc(key)}" class="${saved.status === "reading" ? "active" : ""}">読んでる</button>
      <button data-status="read" data-key="${esc(key)}" class="${saved.status === "read" ? "active good" : ""}">読んだ</button>
      <button data-status="skip" data-key="${esc(key)}" class="${saved.status === "skip" ? "active danger" : ""}">見送り</button>
    </div>
    ${body}
    <div class="links">${links}</div>${abs}
    <div class="reader-notes">
      <label>Memo<textarea data-field="memo" data-key="${esc(key)}"></textarea></label>
      <label>Questions<textarea data-field="questions" data-key="${esc(key)}"></textarea></label>
    </div>
  </article>`;
}

function hydrateTextareas() {
  document.querySelectorAll("textarea[data-field]").forEach(el => {
    el.value = getState(el.dataset.key)[el.dataset.field] || "";
  });
}

function updateStateSummary() {
  const values = Object.values(paperState);
  const saved = values.filter(hasSavedState).length;
  const fav = values.filter(v => v.favorite).length;
  const later = values.filter(v => v.status === "later").length;
  const read = values.filter(v => v.status === "read").length;
  $("savedCount").textContent = `保存 ${saved} / fav ${fav} / later ${later} / read ${read}`;
}

function paperBrief(p) {
  const s = getState(paperKey(p));
  const notes = [
    s.favorite ? "favorite: true" : "",
    s.status ? `status: ${STATE_LABELS[s.status]}` : "",
    s.memo ? `memo: ${s.memo}` : "",
    s.questions ? `questions: ${s.questions}` : "",
  ].filter(Boolean).join("\\n  ");
  return [
    `- title: ${p.title}`,
    `  venue: ${p.venue || ""}`,
    `  topic: ${p.topic || ""}`,
    `  paper: ${p.paper_url || ""}`,
    `  summary: ${p.summary_ja || "(日本語要約なし)"}`,
    `  novelty: ${p.novelty_ja || ""}`,
    `  why_read: ${p.why_read_ja || ""}`,
    notes ? `  local_notes:\\n  ${notes}` : "",
    `  abstract: ${p.abstract || ""}`,
  ].filter(Boolean).join("\\n");
}

function buildAskPrompt() {
  const question = $("askInput").value.trim() || "この論文群の位置づけを整理して";
  const limit = Number($("askLimit").value || 8);
  const rows = currentRows.slice(0, limit);
  return [
    "あなたは自動運転の環境認識・地図生成分野のリサーチアシスタントです。",
    "以下の論文一覧と自分の読書メモを根拠に、質問へ日本語で答えてください。",
    "abstractに書かれていない事実は推測として明示してください。",
    "",
    `質問: ${question}`,
    "",
    `対象論文: ${rows.length}件（現在の検索・フィルタ結果の先頭）`,
    rows.map(paperBrief).join("\\n\\n"),
  ].join("\\n");
}

function renderSurveys() {
  $("surveyList").innerHTML = surveyRequests.slice(0, 8).map((r, i) => `
    <div class="survey-item">
      <b>${esc(r.query)}</b>
      <span>since ${esc(String(r.since))} / ${esc(r.sources)} / ${esc(r.venues || "CVPR,ICCV,ECCV")} / limit ${esc(String(r.limit))} / ${esc(r.created_at)}</span>
      <div class="panel-actions"><button data-survey-copy="${i}">Copy JSON</button></div>
    </div>
  `).join("");
}

function saveSurvey() {
  const query = $("surveyQuery").value.trim();
  if (!query) return;
  surveyRequests.unshift({
    query,
    since: Number($("surveySince").value || 2025),
    limit: Number($("surveyLimit").value || 150),
    sources: $("surveySources").value,
    venues: $("surveyVenues").value.trim() || "CVPR,ICCV,ECCV",
    created_at: new Date().toISOString(),
    status: "queued",
  });
  saveJson(SURVEY_KEY, surveyRequests);
  $("surveyQuery").value = "";
  renderSurveys();
}

["q", "venue", "topic", "state", "sort"].forEach(id => {
  $(id).addEventListener(id === "q" ? "input" : "change", render);
});
$("list").addEventListener("click", (ev) => {
  const status = ev.target.closest("button[data-status]");
  if (status) {
    const cur = getState(status.dataset.key).status;
    setPaperState(status.dataset.key, { status: cur === status.dataset.status ? "" : status.dataset.status });
    return;
  }
  const action = ev.target.closest("button[data-action='favorite']");
  if (action) {
    setPaperState(action.dataset.key, { favorite: !getState(action.dataset.key).favorite });
  }
});
$("list").addEventListener("input", (ev) => {
  const field = ev.target.closest("textarea[data-field]");
  if (!field) return;
  setPaperState(field.dataset.key, { [field.dataset.field]: field.value }, false);
});
$("exportState").addEventListener("click", () => {
  downloadJson("paper-digest-reader-state.json", {
    version: 1,
    exported_at: new Date().toISOString(),
    state: paperState,
    surveys: surveyRequests,
  });
});
$("importState").addEventListener("change", async (ev) => {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const payload = JSON.parse(await file.text());
  paperState = { ...paperState, ...(payload.state || {}) };
  surveyRequests = [...(payload.surveys || []), ...surveyRequests];
  savePaperState(); saveJson(SURVEY_KEY, surveyRequests);
  renderSurveys(); render();
  ev.target.value = "";
});
$("buildAsk").addEventListener("click", () => { $("askOutput").value = buildAskPrompt(); });
$("copyAsk").addEventListener("click", () => {
  if (!$("askOutput").value) $("askOutput").value = buildAskPrompt();
  copyText($("askOutput").value);
});
$("saveSurvey").addEventListener("click", saveSurvey);
$("exportSurveys").addEventListener("click", () => {
  downloadJson("paper-digest-survey-requests.json", {
    version: 1,
    exported_at: new Date().toISOString(),
    surveys: surveyRequests,
  });
});
$("surveyList").addEventListener("click", (ev) => {
  const btn = ev.target.closest("button[data-survey-copy]");
  if (!btn) return;
  copyText(JSON.stringify(surveyRequests[Number(btn.dataset.surveyCopy)], null, 2));
});
renderSurveys();
render();
</script>
</body>
</html>
"""


def render_html(papers: list[Paper], path: Path, *, title: str = "論文ダイジェスト") -> None:
    payload = [
        {
            "key": p.key,
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
