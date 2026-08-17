"""中間形式 JSON の読み書きと、URL/タイトルによる重複排除・増分マージ。"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .models import Paper

log = logging.getLogger("paper_digest")

VERSION = 1


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class Store:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.papers: list[Paper] = []
        self.config: dict[str, Any] = {}
        self.updated_at: str = ""
        self._by_key: dict[str, Paper] = {}
        self._by_title: dict[str, Paper] = {}

    # ---- I/O ----
    @classmethod
    def load(cls, path: Path) -> "Store":
        s = cls(path)
        if s.path.exists():
            try:
                data = json.loads(s.path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                raise SystemExit(f"既存の {s.path} を読み込めませんでした: {e}")
            raw = data.get("papers", data if isinstance(data, list) else [])
            s.papers = [Paper.from_dict(d) for d in raw]
            s.config = data.get("config", {}) if isinstance(data, dict) else {}
            s.updated_at = data.get("updated_at", "") if isinstance(data, dict) else ""
            s._reindex()
            log.info("既存データ %d 件を読み込み: %s", len(s.papers), s.path)
        return s

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": VERSION,
            "updated_at": now_iso(),
            "config": self.config,
            "papers": [p.to_dict() for p in self.papers],
        }
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)
        log.info("保存: %s (%d 件)", self.path, len(self.papers))

    # ---- インデックス ----
    def _reindex(self) -> None:
        self._by_key.clear()
        self._by_title.clear()
        for p in self.papers:
            self._by_key[p.key] = p
            self._by_title.setdefault(p.title_key, p)

    def find(self, paper: Paper) -> Paper | None:
        return self._by_key.get(paper.key) or self._by_title.get(paper.title_key)

    def _index(self, paper: Paper) -> None:
        self._by_key[paper.key] = paper
        self._by_title.setdefault(paper.title_key, paper)

    # ---- マージ ----
    def merge(self, incoming: Iterable[Paper]) -> tuple[int, int]:
        """新規追加と既存更新を行う。戻り値は (新規件数, 更新件数)。

        既存論文の日本語要約は保持され、再生成されない。
        """
        added = updated = 0
        for p in incoming:
            existing = self.find(p)
            if existing is None:
                p.added_at = p.added_at or now_iso()
                self.papers.append(p)
                self._index(p)
                added += 1
            else:
                if existing.merge_from(p):
                    updated += 1
        return added, updated

    # ---- 抽出 ----
    def needs_summary(self) -> list[Paper]:
        return [p for p in self.papers if not p.has_summary and not p.excluded]

    def visible(self) -> list[Paper]:
        """出力対象(LLM が非該当と判定したものを除く)。新しい順。"""
        vis = [p for p in self.papers if not p.excluded]
        vis.sort(key=lambda p: (p.published or "", p.year, p.relevance), reverse=True)
        return vis
