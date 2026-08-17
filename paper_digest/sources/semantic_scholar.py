"""Semantic Scholar Graph API (bulk search) から取得する。

会議名 (CVPR/ICCV/ECCV など) で絞り込めるのが利点。
API キー無しでも動くが共用レート制限がきついので、失敗しても全体は止めない。
S2_API_KEY 環境変数があればヘッダに載せる。
"""

from __future__ import annotations

import logging
import os
import re

from ..models import Paper
from .base import polite_get

log = logging.getLogger("paper_digest")

API = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
FIELDS = "title,abstract,venue,year,externalIds,openAccessPdf,publicationDate,authors.name"
MIN_INTERVAL = 3.0

GITHUB_RE = re.compile(r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+", re.I)


def _build_query(queries: list[str]) -> str:
    """bulk search のクエリ構文に変換する。

    "..." は完全一致になってしまい長いフレーズではほぼヒットしないので、
    フレーズ内は + (AND)、フレーズ間は | (OR) に展開する。
    """
    parts = []
    for q in queries:
        words = [w for w in re.split(r"[^A-Za-z0-9]+", q) if w]
        if words:
            parts.append("(" + "+".join(words) + ")")
    return " | ".join(parts)


# S2 は正式名称を返すので、他ソース(CVF/arXiv)と揃うよう略称に直す
VENUE_ALIASES = [
    ("international conference on computer vision", "ICCV"),
    ("computer vision and pattern recognition", "CVPR"),
    ("european conference on computer vision", "ECCV"),
    ("winter conference on applications of computer vision", "WACV"),
    ("neural information processing systems", "NeurIPS"),
    ("international conference on learning representations", "ICLR"),
    ("international conference on machine learning", "ICML"),
    ("international conference on robotics and automation", "ICRA"),
    ("intelligent robots and systems", "IROS"),
    ("conference on robot learning", "CoRL"),
    ("robotics and automation letters", "RA-L"),
    ("arxiv", "arXiv"),
]


def _short_venue(venue: str) -> str:
    v = venue.lower()
    for needle, short in VENUE_ALIASES:
        if needle in v:
            return short
    return venue


def _to_paper(item: dict) -> Paper | None:
    title = (item.get("title") or "").strip()
    if not title:
        return None
    ext = item.get("externalIds") or {}
    arxiv_id = ext.get("ArXiv")
    if arxiv_id:
        url = f"https://arxiv.org/abs/{arxiv_id}"
    elif ext.get("DOI"):
        url = f"https://doi.org/{ext['DOI']}"
    else:
        oa = item.get("openAccessPdf") or {}
        url = oa.get("url") or ""

    year = item.get("year") or 0
    raw_venue = _short_venue((item.get("venue") or "").strip())
    venue = f"{raw_venue} {year}".strip() if raw_venue else (f"arXiv {year}" if year else "")

    abstract = (item.get("abstract") or "").strip()
    code = ""
    gm = GITHUB_RE.search(abstract)
    if gm:
        code = gm.group(0).rstrip(".,);")

    return Paper(
        title=title,
        abstract=abstract,
        paper_url=url,
        code_url=code,
        venue=venue,
        year=int(year) if year else 0,
        authors=[a.get("name", "") for a in (item.get("authors") or [])][:12],
        source="semanticscholar",
        published=item.get("publicationDate") or "",
    )


def fetch(queries: list[str], *, since: int, venues: list[str] | None = None,
          limit: int = 200) -> list[Paper]:
    params = {
        "query": _build_query(queries),
        "fields": FIELDS,
        "year": f"{since}-",
        "sort": "publicationDate:desc",
    }
    if venues:
        params["venue"] = ",".join(venues)

    headers = {}
    if os.environ.get("S2_API_KEY"):
        headers["x-api-key"] = os.environ["S2_API_KEY"]

    papers: list[Paper] = []
    token: str | None = None
    while len(papers) < limit:
        p = dict(params)
        if token:
            p["token"] = token
        resp = polite_get(API, host_key="s2", min_interval=MIN_INTERVAL,
                          params=p, headers=headers)
        if resp is None:
            log.warning("Semantic Scholar: 取得に失敗したためスキップします")
            break
        try:
            data = resp.json()
        except ValueError:
            log.warning("Semantic Scholar: JSON parse に失敗")
            break
        for item in data.get("data") or []:
            paper = _to_paper(item)
            if paper is not None:
                papers.append(paper)
        token = data.get("token")
        if not token or not data.get("data"):
            break

    papers = papers[:limit]
    log.info("Semantic Scholar: %d 件取得", len(papers))
    return papers
