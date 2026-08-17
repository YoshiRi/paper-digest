"""中間形式(JSON)に落とす論文データの定義。"""

from __future__ import annotations

import dataclasses
import re
from dataclasses import dataclass, field
from typing import Any


def normalize_title(title: str) -> str:
    """重複排除用のタイトル正規化(小文字英数字のみ)。"""
    return re.sub(r"[^a-z0-9]+", "", (title or "").lower())


def normalize_url(url: str | None) -> str:
    if not url:
        return ""
    u = url.strip().lower()
    u = re.sub(r"^https?://(www\.)?", "", u)
    u = re.sub(r"[#?].*$", "", u).rstrip("/")
    # arXiv の abs/pdf とバージョン差を吸収する
    m = re.search(r"arxiv\.org/(abs|pdf)/([0-9]+\.[0-9]+)", u)
    if m:
        return f"arxiv:{m.group(2)}"
    return u


@dataclass
class Paper:
    title: str
    abstract: str = ""
    paper_url: str = ""
    code_url: str = ""
    venue: str = ""           # 例: "CVPR 2026", "arXiv 2025"
    year: int = 0
    topic: str = ""           # 主トピック(1つ)
    topics: list[str] = field(default_factory=list)  # 該当トピック全て
    authors: list[str] = field(default_factory=list)
    source: str = ""          # arxiv / cvf / semanticscholar
    published: str = ""       # ISO8601 (取得できた場合)
    summary_ja: str = ""
    novelty_ja: str = ""
    why_read_ja: str = ""
    relevance: float = 0.0    # キーワードベースのスコア
    llm_relevant: bool | None = None   # LLM 判定 (None = 未判定)
    llm_reason: str = ""
    added_at: str = ""        # このツールが最初に取り込んだ日時

    # ---- 同一性 ----
    @property
    def key(self) -> str:
        """重複排除キー。URL 優先、無ければ正規化タイトル。"""
        u = normalize_url(self.paper_url)
        return u or f"title:{normalize_title(self.title)}"

    @property
    def title_key(self) -> str:
        return f"title:{normalize_title(self.title)}"

    @property
    def has_summary(self) -> bool:
        return bool(self.summary_ja)

    @property
    def excluded(self) -> bool:
        """LLM がテーマ非該当と判断したもの。"""
        return self.llm_relevant is False

    # ---- シリアライズ ----
    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Paper":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})

    def merge_from(self, other: "Paper") -> bool:
        """別ソースで見つかった同一論文の情報で欠けている項目を埋める。

        既存の日本語要約は上書きしない(仕様: 再生成しない)。
        戻り値は変更があったかどうか。
        """
        changed = False
        for f in ("abstract", "code_url", "published"):
            if not getattr(self, f) and getattr(other, f):
                setattr(self, f, getattr(other, f))
                changed = True
        if not self.authors and other.authors:
            self.authors = other.authors
            changed = True
        # 会議名は arXiv より査読会議側を優先する
        if other.venue and not other.venue.startswith("arXiv") and self.venue.startswith("arXiv"):
            self.venue, self.year, self.source = other.venue, other.year or self.year, other.source
            changed = True
        if other.relevance > self.relevance:
            self.relevance = other.relevance
            changed = True
        for t in other.topics:
            if t not in self.topics:
                self.topics.append(t)
                changed = True
        if not self.topic and self.topics:
            self.topic = self.topics[0]
            changed = True
        return changed
