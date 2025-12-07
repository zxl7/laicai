import os
import time
import random
from typing import Dict, Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


_session = requests.Session()
_retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET", "POST"])  # type: ignore
_adapter = HTTPAdapter(max_retries=_retry)
_session.mount("http://", _adapter)
_session.mount("https://", _adapter)

_last_ts: float = 0.0
_cache: Dict[str, Any] = {}


def _default_headers(ref: Optional[str] = None) -> Dict[str, str]:
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept": "application/json, */*;q=0.1",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": ref or "https://quote.eastmoney.com/",
    }


def _proxies() -> Dict[str, str]:
    p: Dict[str, str] = {}
    hp = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    sp = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if hp:
        p["http"] = hp
    if sp:
        p["https"] = sp
    return p


def _rate_limit():
    global _last_ts
    qps = float(os.environ.get("HTTP_RATE_LIMIT_QPS", "10"))
    min_interval = 1.0 / max(qps, 0.1)
    now = time.time()
    wait = _last_ts + min_interval - now
    if wait > 0:
        time.sleep(wait + random.uniform(0.05, 0.25))
    _last_ts = time.time()


def _cache_key(url: str, params: Optional[Dict[str, Any]]) -> str:
    if not params:
        return url
    items = sorted([(k, str(v)) for k, v in params.items()])
    return url + "?" + "&".join([f"{k}={v}" for k, v in items])


def get_json(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: float = 10.0, referer: Optional[str] = None) -> Any:
    _rate_limit()
    ttl = int(os.environ.get("HTTP_CACHE_TTL", "30"))
    key = _cache_key(url, params)
    c = _cache.get(key)
    if c and c[0] > time.time():
        return c[1]
    h = _default_headers(ref=referer)
    if headers:
        h.update(headers)
    r = _session.get(url, params=params, headers=h, timeout=timeout, proxies=_proxies())
    r.raise_for_status()
    data = r.json()
    _cache[key] = (time.time() + ttl, data)
    return data


def get_text(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: float = 10.0, referer: Optional[str] = None) -> str:
    _rate_limit()
    ttl = int(os.environ.get("HTTP_CACHE_TTL", "30"))
    key = _cache_key(url, params)
    c = _cache.get(key)
    if c and c[0] > time.time():
        return c[1]
    h = _default_headers(ref=referer)
    if headers:
        h.update(headers)
    r = _session.get(url, params=params, headers=h, timeout=timeout, proxies=_proxies())
    r.raise_for_status()
    text = r.text
    _cache[key] = (time.time() + ttl, text)
    return text
