"""Abstract をもとに、関連度判定と日本語要約を LLM で生成する。

1回の呼び出しで「テーマ該当かどうか」と「日本語要約」を同時に出させる。
非該当なら要約は捨てられるが、呼び出し回数が倍にならないので結果的に安い。
"""

from __future__ import annotations

import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from .llm import Backend, LLMError
from .models import Paper
from .topics import TOPIC_NAMES

log = logging.getLogger("paper_digest")

SYSTEM = """\
あなたは自動運転の環境認識・地図生成分野に詳しいリサーチアシスタントです。
与えられた論文の情報を読み、(1) 指定テーマに関連するかの判定と、(2) 日本語の短い解説を作ります。

# 対象テーマ
Online HD Map / Vector Map、Lane / Road Topology、Map Reconstruction / Map Update、
3D Object Detection、3D Scene Understanding、Occupancy Prediction、Occupancy Forecasting、
Gaussian Splatting、3D / 4D Reconstruction、Open-world Perception、World Model、
Autonomous Driving Perception。

# 関連度の判定基準
- 自動運転・車載/屋外シーンの認識や地図生成に、手法または応用先として直接つながるなら relevant = true。
- キーワードが一致していても、対象が屋内専用・医用画像・純粋な2D画像生成・NLP など、
  上記の文脈に接続しないものは relevant = false。
- 汎用的な3D表現やシーン再構成の研究でも、屋外大規模シーンや動的シーンを扱っていて
  自動運転に転用できるなら relevant = true としてよい。
- 判断に迷う場合は、その理由を reason に日本語で一文書くこと。

# 日本語解説の書き方
- Abstract の逐語訳をしない。何を課題としてどう解いたのかを自分の言葉で書く。
- summary_ja: 何を解こうとしている論文なのかを2〜4文。
- novelty_ja: 従来手法との違いを1〜2文。
- why_read_ja: 地図生成・環境認識の研究動向を追ううえでなぜ重要かを1〜2文。
- occupancy / BEV / topology / Gaussian Splatting / world model などの専門用語は
  無理に日本語化せず英語表記のままでよい。
- 誇張しない。Abstract に書かれていない性能や事実を足さない。
- relevant = false の場合でも、上の3項目は簡潔に埋めること(出力には使われない)。

# topic
最も中心的なトピックを1つだけ選ぶ。どれにも当てはまらない場合のみ "Other"。
"""

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "relevant": {"type": "boolean", "description": "対象テーマに関連するか"},
        "reason": {"type": "string", "description": "判定理由を日本語で一文"},
        "topic": {"type": "string", "enum": TOPIC_NAMES + ["Other"]},
        "summary_ja": {"type": "string"},
        "novelty_ja": {"type": "string"},
        "why_read_ja": {"type": "string"},
    },
    "required": ["relevant", "reason", "topic", "summary_ja", "novelty_ja", "why_read_ja"],
    "additionalProperties": False,
}


def _prompt(paper: Paper) -> str:
    parts = [
        f"Title: {paper.title}",
        f"Venue: {paper.venue or '不明'}",
        f"Year: {paper.year or '不明'}",
    ]
    if paper.topics:
        parts.append(f"キーワード一致トピック: {', '.join(paper.topics)}")
    abstract = paper.abstract.strip() or "(abstract を取得できませんでした。タイトルから判断してください)"
    parts.append(f"Abstract:\n{abstract}")
    return "\n".join(parts)


def _apply(paper: Paper, result: dict[str, Any]) -> None:
    paper.llm_relevant = bool(result.get("relevant", True))
    paper.llm_reason = (result.get("reason") or "").strip()
    topic = (result.get("topic") or "").strip()
    if topic and topic != "Other":
        paper.topic = topic
        if topic not in paper.topics:
            paper.topics.insert(0, topic)
    elif not paper.topic:
        paper.topic = paper.topics[0] if paper.topics else "Other"
    if paper.llm_relevant:
        paper.summary_ja = (result.get("summary_ja") or "").strip()
        paper.novelty_ja = (result.get("novelty_ja") or "").strip()
        paper.why_read_ja = (result.get("why_read_ja") or "").strip()


def summarize_papers(papers: list[Paper], backend: Backend, *,
                     concurrency: int = 3) -> tuple[int, int, int]:
    """要約を生成する。戻り値は (成功, 非該当として除外, 失敗)。"""
    if not papers:
        return (0, 0, 0)

    done = ok = dropped = failed = 0
    total = len(papers)

    def work(p: Paper) -> tuple[Paper, dict[str, Any] | None, str]:
        try:
            return p, backend.complete_json(SYSTEM, _prompt(p), SCHEMA), ""
        except (LLMError, ValueError) as e:
            return p, None, str(e)

    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        futures = [pool.submit(work, p) for p in papers]
        for fut in as_completed(futures):
            paper, result, err = fut.result()
            done += 1
            if result is None:
                failed += 1
                log.warning("要約失敗: %s (%s)", paper.title[:60], err)
            else:
                _apply(paper, result)
                if paper.llm_relevant:
                    ok += 1
                else:
                    dropped += 1
            print(f"\r  要約 {done}/{total} (生成 {ok} / 除外 {dropped} / 失敗 {failed})",
                  end="", file=sys.stderr, flush=True)
    print("", file=sys.stderr)
    return ok, dropped, failed
