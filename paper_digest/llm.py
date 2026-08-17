"""LLM バックエンド。

- anthropic  : Anthropic SDK を直接叩く (ANTHROPIC_API_KEY か `ant auth login` が必要)
- claude-cli : `claude -p` を subprocess で呼ぶ (Claude Code の認証をそのまま使える)
- auto       : 使えるものを自動選択 (SDK → CLI の順)
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

log = logging.getLogger("paper_digest")

DEFAULT_MODEL = "claude-opus-5"


class LLMError(RuntimeError):
    pass


def _extract_json(text: str) -> dict[str, Any]:
    """テキスト中の最初の JSON オブジェクトを取り出す。"""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    start = text.find("{")
    if start == -1:
        raise LLMError(f"JSON が見つかりません: {text[:200]!r}")
    depth, in_str, esc = 0, False, False
    for i, ch in enumerate(text[start:], start):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise LLMError(f"JSON が閉じていません: {text[:200]!r}")


class Backend:
    name = "base"

    def complete_json(self, system: str, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class AnthropicBackend(Backend):
    name = "anthropic"

    def __init__(self, model: str = DEFAULT_MODEL, effort: str = "low"):
        try:
            import anthropic  # noqa: F401
        except ImportError as e:
            raise LLMError("anthropic パッケージが必要です (uv sync --extra api)") from e
        import anthropic as _a
        self._client = _a.Anthropic()
        self.model = model
        self.effort = effort

    def complete_json(self, system: str, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        resp = self._client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            output_config={
                "effort": self.effort,
                "format": {"type": "json_schema", "schema": schema},
            },
            messages=[{"role": "user", "content": prompt}],
        )
        if resp.stop_reason == "refusal":
            raise LLMError("モデルが応答を拒否しました")
        text = next((b.text for b in resp.content if b.type == "text"), "")
        if not text:
            raise LLMError(f"空の応答 (stop_reason={resp.stop_reason})")
        return json.loads(text)


class ClaudeCLIBackend(Backend):
    """`claude -p` 経由。API キーが無くても Claude Code の認証で動く。"""

    name = "claude-cli"

    def __init__(self, model: str = DEFAULT_MODEL, timeout: float = 300.0):
        exe = shutil.which("claude")
        if not exe:
            raise LLMError("claude CLI が見つかりません")
        self.exe = exe
        self.model = model
        self.timeout = timeout

    def complete_json(self, system: str, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        full = (
            f"{system}\n\n---\n\n{prompt}\n\n---\n\n"
            "上記を踏まえ、次の JSON Schema に厳密に従う JSON オブジェクトだけを出力してください。"
            "前置き・後書き・コードフェンスは一切書かないこと。\n"
            f"{json.dumps(schema, ensure_ascii=False)}"
        )
        cmd = [self.exe, "-p", full, "--output-format", "json", "--model", self.model]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.timeout,
                cwd=str(Path.home()),
            )
        except subprocess.TimeoutExpired as e:
            raise LLMError(f"claude CLI がタイムアウトしました ({self.timeout}s)") from e
        if proc.returncode != 0:
            raise LLMError(f"claude CLI 失敗 (rc={proc.returncode}): {proc.stderr[:300]}")
        out = proc.stdout.strip()
        try:
            envelope = json.loads(out)
            text = envelope.get("result", out) if isinstance(envelope, dict) else out
        except ValueError:
            text = out
        if isinstance(text, dict):
            return text
        return _extract_json(text)


def _has_anthropic_credentials() -> bool:
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        return True
    cfg = Path(os.environ.get("ANTHROPIC_CONFIG_DIR", Path.home() / ".config" / "anthropic"))
    return (cfg / "credentials").is_dir() and any((cfg / "credentials").glob("*.json"))


def make_backend(kind: str = "auto", model: str = DEFAULT_MODEL,
                 effort: str = "low") -> Backend:
    if kind == "anthropic":
        return AnthropicBackend(model, effort)
    if kind == "claude-cli":
        return ClaudeCLIBackend(model)
    if kind != "auto":
        raise LLMError(f"未知の backend: {kind}")

    if _has_anthropic_credentials():
        try:
            b = AnthropicBackend(model, effort)
            log.info("LLM backend: anthropic SDK (%s)", model)
            return b
        except LLMError as e:
            log.info("anthropic SDK を使えませんでした (%s) — claude CLI を試します", e)
    try:
        b = ClaudeCLIBackend(model)
        log.info("LLM backend: claude CLI (%s)", model)
        return b
    except LLMError:
        pass
    raise LLMError(
        "LLM を呼べません。ANTHROPIC_API_KEY を設定するか `ant auth login` するか、"
        "claude CLI をインストールしてください。要約なしで良ければ --no-llm を付けてください。"
    )
