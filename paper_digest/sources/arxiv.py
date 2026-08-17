"""arXiv API (Atom) から論文を取得する。"""

from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

from ..models import Paper
from .base import polite_get

log = logging.getLogger("paper_digest")

API = "http://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

# arXiv は 3 秒間隔を推奨している
MIN_INTERVAL = 3.0

GITHUB_RE = re.compile(r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+", re.I)


def _batch_queries(queries: list[str], max_len: int = 1200) -> list[str]:
    """フレーズ群を `all:"..." OR all:"..."` にまとめる。長すぎる場合は分割。"""
    terms = [f'all:"{q}"' for q in queries]
    batches, cur = [], ""
    for t in terms:
        cand = f"{cur} OR {t}" if cur else t
        if len(cand) > max_len and cur:
            batches.append(cur)
            cur = t
        else:
            cur = cand
    if cur:
        batches.append(cur)
    return batches


def _text(el: ET.Element | None) -> str:
    return re.sub(r"\s+", " ", (el.text or "").strip()) if el is not None else ""


def _parse_entry(entry: ET.Element) -> Paper | None:
    title = _text(entry.find("a:title", NS))
    if not title:
        return None
    abstract = _text(entry.find("a:summary", NS))
    published = _text(entry.find("a:published", NS))
    updated = _text(entry.find("a:updated", NS))
    year = 0
    for stamp in (published, updated):
        m = re.match(r"(\d{4})", stamp or "")
        if m:
            year = int(m.group(1))
            break

    abs_url = ""
    for link in entry.findall("a:link", NS):
        if link.get("rel") == "alternate" or link.get("type") == "text/html":
            abs_url = link.get("href", "")
            break
    if not abs_url:
        abs_url = _text(entry.find("a:id", NS))
    abs_url = re.sub(r"v\d+$", "", abs_url)

    authors = [_text(a.find("a:name", NS)) for a in entry.findall("a:author", NS)]
    comment = _text(entry.find("arxiv:comment", NS))
    journal_ref = _text(entry.find("arxiv:journal_ref", NS))

    # コメント欄によく "Accepted to CVPR 2025" / GitHub リンクが書かれている
    venue = f"arXiv {year}" if year else "arXiv"
    m = re.search(r"\b(CVPR|ICCV|ECCV|NeurIPS|ICLR|ICML|IROS|ICRA|RAL|WACV|BMVC|AAAI|CoRL)\b"
                  r"[^0-9]{0,12}(20\d{2})?", f"{comment} {journal_ref}", re.I)
    if m:
        conf = m.group(1).upper()
        conf_year = m.group(2) or (str(year) if year else "")
        venue = f"{conf} {conf_year}".strip()

    code_url = ""
    gm = GITHUB_RE.search(f"{comment} {abstract}")
    if gm:
        code_url = gm.group(0).rstrip(".,);")

    return Paper(
        title=title,
        abstract=abstract,
        paper_url=abs_url,
        code_url=code_url,
        venue=venue,
        year=year,
        authors=authors,
        source="arxiv",
        published=published or updated,
    )


def fetch(queries: list[str], *, since: int, limit: int = 200,
          categories: tuple[str, ...] = ("cs.CV", "cs.RO")) -> list[Paper]:
    """検索フレーズ群にマッチする arXiv 論文を新しい順に取得する。"""
    cat_clause = " OR ".join(f"cat:{c}" for c in categories)
    papers: list[Paper] = []
    seen: set[str] = set()

    batches = _batch_queries(queries)
    per_batch = max(25, -(-limit // max(1, len(batches))))  # 切り上げ

    for i, batch in enumerate(batches, 1):
        if len(papers) >= limit:
            break
        search = f"({cat_clause}) AND ({batch})"
        fetched, start, stale = 0, 0, False
        while fetched < per_batch and not stale:
            params = {
                "search_query": search,
                "start": start,
                "max_results": min(100, per_batch - fetched),
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
            url = f"{API}?{urlencode(params)}"
            log.info("arXiv query %d/%d (start=%d)", i, len(batches), start)
            resp = polite_get(url, host_key="arxiv", min_interval=MIN_INTERVAL)
            if resp is None:
                break
            try:
                root = ET.fromstring(resp.content)
            except ET.ParseError as e:
                log.warning("arXiv XML parse error: %s", e)
                break
            entries = root.findall("a:entry", NS)
            if not entries:
                break
            for entry in entries:
                p = _parse_entry(entry)
                if p is None:
                    continue
                if p.year and p.year < since:
                    # 新しい順なので、以降はすべて対象年より古い
                    stale = True
                    continue
                if p.key in seen:
                    continue
                seen.add(p.key)
                papers.append(p)
            fetched += len(entries)
            start += len(entries)
            if len(entries) < params["max_results"]:
                break

    papers = papers[:limit]
    log.info("arXiv: %d 件取得", len(papers))
    return papers
