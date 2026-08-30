# Interactive research assistant plan

`paper-digest` を「静的な論文一覧」から「論文タイムライン + 読書管理 + 追加サーベイ依頼」に伸ばすための方針。

## Goal

- URL を開けば、どこでも最新の論文一覧を読める。
- 論文ごとに `favorite` / `later` / `reading` / `read` / `skip` を付けられる。
- 論文ごとに memo と questions を残せる。
- 現在の検索・フィルタ結果を文脈にして、LLM へ投げる質問プロンプトを作れる。
- 追加サーベイの query を queue として残せる。
- 将来的には backend/API で Ask と Survey をその場で実行する。

## Phase 1: static-first

GitHub Pages のまま完結させる。

- `docs/index.html` に読書状態 UI を持たせる。
- 状態は browser `localStorage` に保存する。
- export/import JSON で、端末間の手動移行とバックアップを可能にする。
- Ask は回答までは行わず、現在の検索・フィルタ結果から LLM 用 prompt を生成する。
- Survey は実行せず、query / since / sources / limit を request JSON として queue する。

この段階は認証も backend も不要。公開ページとして壊れにくい。

## Phase 2: sync state

複数端末で読書状態を共有したくなったら、保存先だけを追加する。

候補:

- Supabase
- Cloudflare Workers + D1/KV
- private GitHub repository の JSON

保持する最小 schema:

```json
{
  "paper_key": "arxiv:2608.26951",
  "status": "later",
  "favorite": true,
  "memo": "...",
  "questions": "...",
  "updated_at": "2026-08-30T00:00:00Z"
}
```

`paper_key` は `papers.json` から生成している key を使う。`paper_url` がある場合は URL 正規化、無い場合は title 正規化。

## Phase 3: Ask API

静的 page から小さい API を呼ぶ。

最小 endpoint:

```text
POST /ask
```

入力:

```json
{
  "question": "HD Map系で実装コストが低いものはどれ？",
  "paper_keys": ["arxiv:2608.26951"],
  "reader_state": {}
}
```

処理:

1. `papers.json` から対象論文を取り出す。
2. title / venue / topic / abstract / summary_ja / novelty_ja / why_read_ja / memo / questions を context にする。
3. LLM に渡して日本語回答を返す。

最初は RAG 用 DB を持たず、`papers.json` の filter 結果をそのまま context に入れる。

## Phase 4: Survey API

追加サーベイは同期処理にしない。外部 API と LLM 要約で時間がかかるため job にする。

最小 endpoint:

```text
POST /survey
GET /jobs/:id
```

処理:

1. query / since / sources / limit を受け取る。
2. GitHub Actions `workflow_dispatch` か worker job を起動する。
3. `paper-digest collect` または `update` を実行する。
4. `papers.json` / `papers.md` / `docs/index.html` を更新して push する。
5. GitHub Pages が再公開する。

LLM 要約を自動実行する場合は API 課金が発生するので、最初は `--no-llm` の追加収集だけにする。

## Not doing yet

- public X/Twitter bot を読書状態の正本にしない。
- ブラウザに GitHub token を保存して workflow dispatch する設計はまだ採用しない。
- RAG DB や認証付き multi-user backend は、localStorage 運用で痛みが見えてから入れる。
