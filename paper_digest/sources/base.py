"""ソース共通のHTTPユーティリティ。"""

from __future__ import annotations

import logging
import time

import requests

log = logging.getLogger("paper_digest")

USER_AGENT = "paper-digest/0.1 (research paper digest CLI; +https://github.com/)"

_session: requests.Session | None = None
_last_request_at: dict[str, float] = {}


def session() -> requests.Session:
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({"User-Agent": USER_AGENT})
    return _session


def polite_get(url: str, *, host_key: str, min_interval: float = 1.0,
               timeout: float = 30.0, **kwargs) -> requests.Response | None:
    """ホスト毎に最低間隔を空けて GET する。失敗時は None(全体は止めない)。"""
    last = _last_request_at.get(host_key, 0.0)
    wait = min_interval - (time.monotonic() - last)
    if wait > 0:
        time.sleep(wait)
    try:
        resp = session().get(url, timeout=timeout, **kwargs)
    except requests.RequestException as e:
        log.warning("GET failed %s: %s", url, e)
        _last_request_at[host_key] = time.monotonic()
        return None
    _last_request_at[host_key] = time.monotonic()
    if resp.status_code != 200:
        log.warning("GET %s -> HTTP %s", url, resp.status_code)
        return None
    return resp
