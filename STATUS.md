# 開発・運用ステータス

2026-08-17 時点。PoC として作ったところから、GitHub Pages で公開して
週次で自動更新が回るところまでの記録。

## 現状

| 項目 | 値 |
|---|---|
| リポジトリ | https://github.com/YoshiRi/paper-digest (public) |
| 公開ページ | https://yoshiri.github.io/paper-digest/ |
| Pages ソース | `main` ブランチの `/docs` (`docs/index.html`) |
| 収録論文 | 234 件 (arXiv 145 / CVF 89) |
| 日本語要約済み | 15 件 (残り 219 件は未生成) |
| Code URL 取得済み | 48 件 |
| データ最終更新 | 2026-08-17 |

### 収録内訳

発表先: arXiv 2026 (60) / arXiv 2025 (57) / CVPR 2026 (32) / ICCV 2025 (32) /
CVPR 2025 (31) / ECCV 2026 (5) / IROS 2026 (4) / ICRA 2026 (4) ほか
(年別: 2025 が 131 件、2026 が 103 件)

トピック: Occupancy (62) / Gaussian Splatting (36) / HD Map (35) /
AD Perception (32) / 3D Detection (25) / Reconstruction (11) / Open-world (10) /
Scene Understanding (9) / World Model (8) / Topology (3) / Occupancy Forecasting (3)

Topology と Occupancy Forecasting が少ないのは、キーワード辞書がまだ薄いのが原因と思われる。
`paper_digest/topics.py` の `strong` / `queries` を足すと拾えるようになるはず。

## できていること

当初の PoC 手順 (1. 論文取得 → 2. JSON 保存 → 3. LLM 要約 → 4. Markdown →
5. HTML → 6. 増分更新) は一通り実装済み。

### コマンド

| コマンド | 動作 |
|---|---|
| `collect` | 検索 → 一次フィルタ → 重複排除 → JSON 保存 → LLM 判定/要約 → md/html 出力 |
| `update` | 前回設定を JSON から引き継いで新着だけ追加 (CI / cron 向け) |
| `summarize` | 未要約のものだけ要約 |
| `render` | ネットも LLM も使わず JSON から出力だけ作り直し |
| `stats` | 収集状況の表示 |

### 関連度判定の 2 段構え

1. **キーワード一次フィルタ** (`topics.py`) — トピック辞書でスコアリングし、
   自動運転 / 3D の文脈が皆無なものは減点。閾値 (既定 4.0) 未満を落とす。
   LLM 呼び出し数を抑えるのが目的。
2. **LLM 判定 + 要約** (`summarize.py`) — 1 回の呼び出しで
   「テーマ該当か」と「概要 / 新規性 / 読む理由」を同時に生成。
   キーワードは当たっているが文脈が違うもの (屋内専用・医用画像など) はここで落ちる。

### LLM バックエンド

`ANTHROPIC_API_KEY` / `ant` プロファイルがあれば Anthropic SDK (Structured Outputs)、
無ければ `claude -p` を叩く CLI バックエンドに自動フォールバックする。
開発環境には API キーが無かったため、実際の要約生成は CLI バックエンド (claude-opus-5) で行った。

## 検証したこと

| 対象 | 方法 | 結果 |
|---|---|---|
| 重複排除 | `abs`/`pdf`/バージョン付き/http の URL 表記ゆれ + タイトル表記ゆれを投入 | 1 件に統合。会議名は arXiv より CVPR 等を優先、Code URL / abstract は相互補完、既存の日本語要約は保持 |
| 増分更新 | 同一条件の `update` を 2 回連続実行 | 2 回目は「新規 0 件」。既存要約も維持 |
| 関連度フィルタ | 屋内限定 occupancy 論文 / 医用画像 3D 再構成論文を投入 | 両方 `relevant=false` で理由付きで除外。屋内外統合の occupancy 論文は残った |
| HTML の挙動 | Node で DOM をスタブし描画ロジックを実行 | キーワード検索・Conference フィルタ・Topic フィルタ・4 種のソート・0 件表示すべて動作 |
| HTML の自己完結性 | 生成物と公開ページの外部参照を確認 | 外部リソース参照ゼロ |
| Semantic Scholar | ライブ API に対して実行 | 動作 (会議名は ICCV 等の略称に正規化)。未認証だと 429 が頻発するため既定ソースからは外した |
| CI | Actions を手動実行 | 新規 43 件を収集してコミット・push、Pages 自動再デプロイまで成功 |

## 運用フロー

| どこで | 何をするか | LLM |
|---|---|---|
| GitHub Actions (毎週月曜 09:00 JST) | `update --no-llm` で新着収集 → 差分があればコミット → Pages 更新 | 使わない (API キー不要) |
| ローカル | `summarize` で未要約分に日本語要約を付けて push | 使う |

新着ゼロのときは生成時刻だけの差分を捨てるので、空コミットで履歴が汚れない。
未要約の件数は毎回 Actions のサマリに notice として出る。

## 既知の制限

- **CVF は 2 段階取得**。一覧ページにタイトルしか無いため、タイトルでスコアリングして
  上位だけ abstract を取りに行く (`--cvf-detail-limit`)。ここで落ちた論文の abstract は見ていない。
- **Semantic Scholar は未認証だとレート制限が厳しい**。失敗しても他ソースは続行するが、
  常用するなら `S2_API_KEY` が要る。既定ソースからは外してある。
- **Code URL は best effort**。abstract / arXiv コメント / CVF ページ中の GitHub リンクを
  拾っているだけで、Papers with Code 連携は入れていない (API が不安定なため)。現状 234 件中 48 件。
- **要約が 15/234 件**。残りは課金が発生するためローカルで順次実行する想定。
- GitHub の仕様上、リポジトリが 60 日間無活動だとスケジュール実行が自動停止する。
  週次で新着コミットが入るうちは問題にならない。

## 次にやるとしたら

- 残り 219 件の日本語要約 (`summarize --max-summaries 50 --model claude-sonnet-5` で小分け)
- Topology / Occupancy Forecasting のキーワード辞書の拡充
- Papers with Code もしくは GitHub 検索による Code URL の補完
- 一次フィルタの閾値 (現状 4.0) の調整 — 現状 240 件中 237 件が通過しており、ほぼ素通し状態
