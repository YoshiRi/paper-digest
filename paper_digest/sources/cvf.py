"""CVF Open Access (CVPR / ICCV / ECCV) の採択論文一覧から取得する。

一覧ページにはタイトルしか無いため、
  1. 一覧を取ってタイトルでざっくり絞る(無料)
  2. 残った候補だけ詳細ページを叩いて abstract を取る(1リクエスト/件)
という二段構えにしている。
"""

from __future__ import annotations

import html
import logging
import re

from ..models import Paper
from ..topics import contains_phrase, keywords_for_prefilter, score_paper
from .base import polite_get

log = logging.getLogger("paper_digest")

BASE = "https://openaccess.thecvf.com"
MIN_INTERVAL = 0.7

PTITLE_RE = re.compile(
    r'class="ptitle"[^>]*>.*?<a\s+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>',
    re.I | re.S,
)
ABSTRACT_RE = re.compile(r'id="abstract"[^>]*>(?P<abs>.*?)</div>', re.I | re.S)
ARXIV_RE = re.compile(r"arxiv\.org/abs/([0-9]+\.[0-9]+)", re.I)
GITHUB_RE = re.compile(r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+", re.I)


def _strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def _listing_urls(venue: str, year: int) -> list[str]:
    v = venue.upper()
    return [f"{BASE}/{v}{year}?day=all", f"{BASE}/{v}{year}"]


def _title_looks_relevant(title: str, keywords: list[str]) -> bool:
    t = title.lower()
    return any(contains_phrase(t, kw) for kw in keywords)


def fetch(venues: list[str], years: list[int], *, detail_limit: int = 80) -> list[Paper]:
    keywords = keywords_for_prefilter()
    papers: list[Paper] = []

    for venue in venues:
        for year in years:
            listing = None
            for url in _listing_urls(venue, year):
                resp = polite_get(url, host_key="cvf", min_interval=MIN_INTERVAL)
                if resp is not None and "ptitle" in resp.text:
                    listing = resp.text
                    break
            if listing is None:
                log.info("CVF: %s %s は一覧を取得できず(未開催/未公開)", venue, year)
                continue

            entries: list[tuple[str, str]] = []
            seen_href: set[str] = set()
            for m in PTITLE_RE.finditer(listing):
                href, title = m.group("href"), _strip_tags(m.group("title"))
                if not title or href in seen_href:
                    continue
                seen_href.add(href)
                entries.append((href, title))

            # タイトルだけでスコアリングし、見込みの高い順に abstract を取りに行く
            candidates = [(h, t) for h, t in entries if _title_looks_relevant(t, keywords)]
            candidates.sort(key=lambda ht: -score_paper(ht[1], "")[0])
            log.info("CVF %s %d: 全 %d 件 → タイトル一致 %d 件 (詳細取得は最大 %d 件)",
                     venue.upper(), year, len(entries), len(candidates), detail_limit)

            for href, title in candidates[:detail_limit]:
                url = href if href.startswith("http") else f"{BASE}{href}"
                p = Paper(
                    title=title,
                    paper_url=url,
                    venue=f"{venue.upper()} {year}",
                    year=year,
                    source="cvf",
                )
                detail = polite_get(url, host_key="cvf", min_interval=MIN_INTERVAL)
                if detail is not None:
                    body = detail.text
                    am = ABSTRACT_RE.search(body)
                    if am:
                        p.abstract = _strip_tags(am.group("abs"))
                    ax = ARXIV_RE.search(body)
                    if ax:
                        # arXiv 版があるならそちらを正とする(他ソースと重複排除できる)
                        p.paper_url = f"https://arxiv.org/abs/{ax.group(1)}"
                    gm = GITHUB_RE.search(body)
                    if gm:
                        p.code_url = gm.group(0).rstrip(".,);")
                papers.append(p)

    log.info("CVF: %d 件取得", len(papers))
    return papers
