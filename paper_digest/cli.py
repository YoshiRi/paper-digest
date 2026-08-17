"""paper-digest の CLI エントリポイント。"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from . import render as render_mod
from .llm import DEFAULT_MODEL, LLMError, make_backend
from .models import Paper
from .sources import arxiv, cvf, semantic_scholar
from .store import Store
from .summarize import summarize_papers
from .topics import DEFAULT_THRESHOLD, default_queries, score_paper

log = logging.getLogger("paper_digest")

DEFAULT_SOURCES = ["arxiv", "cvf"]
DEFAULT_VENUES = ["CVPR", "ICCV", "ECCV"]
DEFAULT_DATA = "papers.json"
DEFAULT_OUTPUTS = ["papers.md", "papers.html"]


# ------------------------------------------------------------------ helpers
def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        stream=sys.stderr,
    )


def _split(value: str | None) -> list[str]:
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


def _resolve_config(args: argparse.Namespace, store: Store) -> dict:
    """CLI 引数 > 前回保存した設定 > 既定値 の順で解決する。"""
    saved = store.config or {}

    def pick(name: str, cli_value, default):
        if cli_value not in (None, [], ""):
            return cli_value
        if name in saved and saved[name] not in (None, [], ""):
            return saved[name]
        return default

    queries = _split(getattr(args, "query", None))
    since = getattr(args, "since", None)
    cfg = {
        "query": pick("query", queries, []),
        "since": pick("since", since, datetime.now().year),
        "sources": pick("sources", _split(getattr(args, "sources", None)), DEFAULT_SOURCES),
        "venues": pick("venues", _split(getattr(args, "venues", None)), DEFAULT_VENUES),
        "limit": pick("limit", getattr(args, "limit", None), 200),
        "min_score": pick("min_score", getattr(args, "min_score", None), DEFAULT_THRESHOLD),
        "cvf_detail_limit": pick("cvf_detail_limit",
                                 getattr(args, "cvf_detail_limit", None), 80),
        "model": pick("model", getattr(args, "model", None), DEFAULT_MODEL),
        "outputs": pick("outputs", getattr(args, "output", None), DEFAULT_OUTPUTS),
        "title": pick("title", getattr(args, "title", None), "論文ダイジェスト"),
    }
    return cfg


def _score_and_filter(papers: list[Paper], min_score: float) -> list[Paper]:
    kept: list[Paper] = []
    for p in papers:
        score, topics = score_paper(p.title, p.abstract)
        p.relevance, p.topics = score, topics
        p.topic = topics[0] if topics else ""
        if score >= min_score:
            kept.append(p)
    log.info("キーワード一次フィルタ: %d 件中 %d 件が閾値 %.1f 以上",
             len(papers), len(kept), min_score)
    return kept


def _collect_from_sources(cfg: dict) -> list[Paper]:
    queries = cfg["query"] or default_queries()
    sources = cfg["sources"]
    since = int(cfg["since"])
    found: list[Paper] = []

    if "arxiv" in sources:
        found += arxiv.fetch(queries, since=since, limit=int(cfg["limit"]))
    if "cvf" in sources:
        years = list(range(since, datetime.now().year + 2))
        found += cvf.fetch(cfg["venues"], years, detail_limit=int(cfg["cvf_detail_limit"]))
    if "semanticscholar" in sources:
        found += semantic_scholar.fetch(queries, since=since, venues=cfg["venues"],
                                        limit=int(cfg["limit"]))
    return found


def _run_summaries(args: argparse.Namespace, store: Store, cfg: dict) -> None:
    if getattr(args, "no_llm", False):
        log.info("--no-llm のため日本語要約はスキップします")
        return
    pending = store.needs_summary()
    if not pending:
        log.info("要約が必要な論文はありません")
        return
    limit = getattr(args, "max_summaries", None)
    if limit:
        pending = sorted(pending, key=lambda p: -p.relevance)[: int(limit)]
    log.info("日本語要約を生成します: %d 件", len(pending))
    try:
        backend = make_backend(getattr(args, "llm_backend", "auto"), cfg["model"],
                               getattr(args, "effort", "low"))
    except LLMError as e:
        log.error("LLM を初期化できませんでした: %s", e)
        return
    ok, dropped, failed = summarize_papers(
        pending, backend, concurrency=int(getattr(args, "concurrency", 3)))
    log.info("要約完了: 生成 %d / テーマ非該当として除外 %d / 失敗 %d", ok, dropped, failed)


def _write_outputs(store: Store, cfg: dict) -> None:
    papers = store.visible()
    for out in cfg["outputs"]:
        render_mod.render_output(papers, Path(out), title=cfg["title"])
    if papers:
        log.info("%s", render_mod.summarize_counts(papers))


# ----------------------------------------------------------------- commands
def cmd_collect(args: argparse.Namespace) -> int:
    store = Store.load(Path(args.data))
    cfg = _resolve_config(args, store)
    log.info("設定: since=%s sources=%s venues=%s",
             cfg["since"], ",".join(cfg["sources"]), ",".join(cfg["venues"]))

    found = _collect_from_sources(cfg)
    kept = _score_and_filter(found, float(cfg["min_score"]))
    added, updated = store.merge(kept)
    log.info("マージ結果: 新規 %d 件 / 既存更新 %d 件 (総計 %d 件)",
             added, updated, len(store.papers))

    store.config = cfg
    store.save()
    _run_summaries(args, store, cfg)
    store.save()
    _write_outputs(store, cfg)
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """前回の設定を引き継いで、新着だけを追加する。"""
    if not Path(args.data).exists():
        log.error("%s がありません。まず `paper-digest collect` を実行してください。", args.data)
        return 1
    return cmd_collect(args)


def cmd_summarize(args: argparse.Namespace) -> int:
    """収集済みで要約が無いものだけを要約する。"""
    store = Store.load(Path(args.data))
    if not store.papers:
        log.error("%s にデータがありません", args.data)
        return 1
    cfg = _resolve_config(args, store)
    _run_summaries(args, store, cfg)
    store.config = cfg
    store.save()
    _write_outputs(store, cfg)
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    """LLM もネットワークも使わず、既存 JSON から出力だけ作り直す。"""
    store = Store.load(Path(args.data))
    if not store.papers:
        log.error("%s にデータがありません", args.data)
        return 1
    cfg = _resolve_config(args, store)
    _write_outputs(store, cfg)
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    store = Store.load(Path(args.data))
    vis = store.visible()
    print(f"総数: {len(store.papers)} 件 (表示対象 {len(vis)} / 除外 {len(store.papers) - len(vis)})")
    print(f"要約済み: {sum(1 for p in vis if p.has_summary)} 件")
    print(f"最終更新: {store.updated_at or '-'}")
    if vis:
        print(render_mod.summarize_counts(vis))
    return 0


# ------------------------------------------------------------------- parser
def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--data", default=DEFAULT_DATA, help="中間形式 JSON のパス (既定: papers.json)")
    p.add_argument("--output", action="append", metavar="FILE",
                   help="出力ファイル。拡張子で md/html を判定。複数回指定可 "
                        "(既定: papers.md と papers.html)")
    p.add_argument("--title", help="出力のタイトル")
    p.add_argument("-v", "--verbose", action="store_true", help="デバッグログを出す")


def _add_llm(p: argparse.ArgumentParser) -> None:
    p.add_argument("--no-llm", action="store_true", help="日本語要約を生成しない")
    p.add_argument("--llm-backend", choices=["auto", "anthropic", "claude-cli"],
                   default="auto", help="LLM の呼び出し方 (既定: auto)")
    p.add_argument("--model", help=f"使用モデル (既定: {DEFAULT_MODEL})")
    p.add_argument("--effort", choices=["low", "medium", "high"], default="low",
                   help="anthropic backend の effort (既定: low)")
    p.add_argument("--concurrency", type=int, default=3, help="要約の並列数 (既定: 3)")
    p.add_argument("--max-summaries", type=int,
                   help="1回の実行で要約する最大件数 (関連度の高い順)")


def _add_collect(p: argparse.ArgumentParser) -> None:
    p.add_argument("--query", help='検索フレーズをカンマ区切りで指定 '
                                   '(例: "HD map, occupancy, 3D perception")')
    p.add_argument("--since", type=int, help="この年以降の論文を対象にする (既定: 今年)")
    p.add_argument("--sources", help=f"使用ソース (既定: {','.join(DEFAULT_SOURCES)}。"
                                     "arxiv,cvf,semanticscholar から選択)")
    p.add_argument("--venues", help=f"会議名 (既定: {','.join(DEFAULT_VENUES)})")
    p.add_argument("--limit", type=int, help="1ソースあたりの取得上限 (既定: 200)")
    p.add_argument("--min-score", type=float,
                   help=f"キーワード一次フィルタの閾値 (既定: {DEFAULT_THRESHOLD})")
    p.add_argument("--cvf-detail-limit", type=int,
                   help="CVF で abstract を取りに行く最大件数 / 会議・年 (既定: 80)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="paper-digest",
        description="地図生成・自動運転の環境認識に関する最新論文を集めて日本語で要約する",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    c = sub.add_parser("collect", help="論文を検索して収集し、要約して出力する")
    _add_common(c); _add_collect(c); _add_llm(c)
    c.set_defaults(func=cmd_collect)

    u = sub.add_parser("update", help="前回の設定で新着だけを追加する (定期実行用)")
    _add_common(u); _add_collect(u); _add_llm(u)
    u.set_defaults(func=cmd_update)

    s = sub.add_parser("summarize", help="収集済みで未要約のものだけ要約する")
    _add_common(s); _add_llm(s)
    s.set_defaults(func=cmd_summarize)

    r = sub.add_parser("render", help="既存 JSON から Markdown/HTML を作り直す")
    _add_common(r)
    r.set_defaults(func=cmd_render)

    st = sub.add_parser("stats", help="収集状況を表示する")
    _add_common(st)
    st.set_defaults(func=cmd_stats)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _setup_logging(getattr(args, "verbose", False))
    try:
        return args.func(args)
    except KeyboardInterrupt:
        log.warning("中断しました")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
