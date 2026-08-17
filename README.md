# paper-digest

CVPR / ICCV / ECCV / arXiv から **地図生成・自動運転の環境認識** 関連の論文を集めて、
日本語で短く要約した一覧 (Markdown / HTML) を生成する CLI。

CLI を一度実行すると、その時点で読むべき論文の日本語インデックスができる状態を目指しています。

**公開ページ: https://yoshiri.github.io/paper-digest/**
(`docs/index.html` をそのまま GitHub Pages でホストしています。`papers.md` は
[こちら](papers.md)。)

## セットアップ

```bash
cd paper-digest
uv sync                 # 依存は requests のみ
# ANTHROPIC_API_KEY がある場合はこちら (SDK 経由になる)
uv sync --extra api
```

LLM は次の順で自動選択されます (`--llm-backend` で固定も可能)。

| backend | 条件 | 備考 |
|---|---|---|
| `anthropic` | `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` / `ant auth login` のプロファイルがある | Structured Outputs を使うので出力が安定 |
| `claude-cli` | `claude` コマンドがある | Claude Code の認証をそのまま使える。APIキー不要 |

どちらも無い場合は `--no-llm` を付ければ収集・出力だけ実行できます。

## 使い方

```bash
# 収集 → 日本語要約 → papers.json / papers.md / papers.html を生成
uv run paper-digest collect \
  --query "HD map, occupancy, 3D perception, autonomous driving" \
  --since 2025 \
  --output papers.html

# 定期更新: 前回の設定を引き継いで新着だけ追加する
uv run paper-digest update

# 収集済みで未要約のものだけ要約する
uv run paper-digest summarize

# LLM もネットワークも使わず、JSON から出力だけ作り直す
uv run paper-digest render --output papers.md --output papers.html

# 収集状況
uv run paper-digest stats
```

`--query` を省略すると、`paper_digest/topics.py` に定義した重点テーマの
検索フレーズが自動的に使われます。

### 主なオプション

| オプション | 既定値 | 説明 |
|---|---|---|
| `--data` | `papers.json` | 中間形式 JSON のパス |
| `--output` | `papers.md` と `papers.html` | 出力先。拡張子で形式判定。複数回指定可 |
| `--since` | 今年 | この年以降の論文を対象にする |
| `--sources` | `arxiv,cvf` | `arxiv` / `cvf` / `semanticscholar` から選択 |
| `--venues` | `CVPR,ICCV,ECCV` | CVF・Semantic Scholar で対象にする会議 |
| `--limit` | 200 | 1ソースあたりの取得上限 |
| `--min-score` | 4.0 | キーワード一次フィルタの閾値 |
| `--cvf-detail-limit` | 80 | CVF で abstract を取りに行く上限 (会議・年ごと) |
| `--model` | `claude-opus-5` | 要約に使うモデル。`claude-sonnet-5` / `claude-haiku-4-5` にすると安い |
| `--max-summaries` | なし | 1回の実行で要約する件数の上限 (関連度の高い順) |
| `--concurrency` | 3 | 要約の並列数 |
| `--no-llm` | — | 要約せず収集と出力だけ行う |

## 動作

1. **検索** — arXiv API (Atom)、CVF Open Access の採択一覧、
   任意で Semantic Scholar Graph API から論文を取得
2. **一次フィルタ** — `topics.py` のキーワード辞書でスコアリングし、
   明らかに無関係なものを落とす (LLM 呼び出し回数を抑えるため)
3. **重複排除** — arXiv ID / URL / 正規化タイトルで名寄せ。
   複数ソースで見つかった場合は会議名や Code URL を補完し合う
4. **LLM 判定 + 要約** — 1回の呼び出しで「テーマ該当かどうか」と
   「概要 / 新規性 / 読む理由」の日本語を同時に生成。
   キーワードが当たっていても文脈が違うもの (屋内専用・医用画像など) はここで除外される
5. **出力** — Markdown と HTML

### 出力形式

Markdown はトピック別に、論文ごとに次の形で並びます。

```markdown
### 論文タイトル

CVPR 2026 / Mapping

**概要**
何を解こうとしている論文なのかを日本語で2〜4文。

**新規性**
従来手法との違いを1〜2文。

**読む理由**
地図生成・環境認識の研究動向を追ううえで、なぜ重要かを1〜2文。

- Paper: URL
- Code: URL
```

HTML は外部依存なしの1ファイルで、キーワード検索・Conference フィルタ・
Topic フィルタ・並び替え (新しい順 / 古い順 / 関連度順 / タイトル順) ができます。
ライト/ダークテーマに追従します。

### 中間形式 (papers.json)

```json
{
  "version": 1,
  "updated_at": "2026-08-17T00:00:00+00:00",
  "config": { "since": 2025, "sources": ["arxiv", "cvf"], "...": "..." },
  "papers": [
    {
      "title": "...",
      "venue": "CVPR 2026",
      "year": 2026,
      "topic": "Occupancy",
      "abstract": "...",
      "summary_ja": "...",
      "novelty_ja": "...",
      "why_read_ja": "...",
      "paper_url": "...",
      "code_url": "..."
    }
  ]
}
```

実際にはこれに加えて `topics` / `authors` / `source` / `published` /
`relevance` / `llm_relevant` / `llm_reason` / `added_at` を持ちます。

## 増分更新

`update` (と `collect`) は既存 JSON を読み込み、

- 新しい論文だけを追加
- URL (arXiv ID 正規化込み) またはタイトルで重複排除
- **既存の日本語要約は再生成しない**

という動作をします。cron や `claude` の schedule から `paper-digest update` を
定期実行すれば、日本語インデックスが育っていきます。

```cron
0 9 * * 1 cd /path/to/paper-digest && uv run paper-digest update
```

## GitHub Pages と自動更新

このリポジトリは 2 段構えで運用します。

| どこで | 何をするか | LLM |
|---|---|---|
| GitHub Actions (毎週月曜 09:00 JST) | `paper-digest update --no-llm` で新着を収集し、`papers.json` / `papers.md` / `docs/index.html` を更新して push | 使わない (API キー不要) |
| ローカル | `paper-digest summarize` で未要約の論文に日本語要約を付けて push | 使う |

Actions は新着が無ければコミットしません (生成時刻だけの差分は捨てます)。
`main` に push されると Pages (`main` ブランチの `/docs`) が自動で再デプロイされます。
手動実行は Actions タブの **update-digest** → Run workflow から。

ローカルでの要約 → 公開までの流れ:

```bash
git pull
uv run paper-digest summarize            # 未要約のものだけ要約 (件数を絞るなら --max-summaries 20)
git add papers.json papers.md docs/index.html
git commit -m "docs: 日本語要約を追加"
git push
```

Actions 側でも要約まで自動化したい場合は、リポジトリの Secrets に `ANTHROPIC_API_KEY` を
登録したうえで、`.github/workflows/update.yml` の `--no-llm` を外して
`env: ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}` と
`--max-summaries 20` 程度を足してください (実行ごとに API 課金が発生します)。

## テーマを変える

`paper_digest/topics.py` の `TOPICS` を編集します。1トピックは

- `strong`: それ単体で該当と見なせる語 (重み大)
- `weak`: 補助的な語
- `queries`: arXiv / Semantic Scholar に投げる検索フレーズ

の3つで定義されており、`summarize.py` の `SYSTEM` プロンプトにある
対象テーマの記述と揃えておくと LLM 判定もぶれません。

## 制限

- CVF は一覧ページにタイトルしか無いため、タイトルで絞ってから abstract を
  1件ずつ取りに行きます (`--cvf-detail-limit` で上限を制御)。ヒットしすぎる場合は
  一次フィルタで落ちた論文の abstract は見ていないことになります。
- Semantic Scholar は API キー無しだとレート制限が厳しく、失敗することがあります
  (失敗しても他ソースの処理は続行します)。`S2_API_KEY` を設定すると安定します。
- Code URL は abstract / arXiv コメント / CVF ページ中の GitHub リンクから
  拾っているだけなので、取りこぼしがあります。
