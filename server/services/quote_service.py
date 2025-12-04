import os
import re
from typing import Dict, Any, Optional

import requests

from ..common.utils import normalize_symbol, round_price


def _fetch_sina(sym: str) -> Dict[str, Any]:
    resp = requests.get("http://hq.sinajs.cn/list=" + sym, timeout=5, headers={"Referer": "https://finance.sina.com.cn/"})
    if resp.status_code != 200:
        raise ValueError("行情接口请求失败")
    txt = resp.text
    m = re.search(r'"([^"]*)"\s*;', txt)
    if not m:
        raise ValueError("未获取到行情数据")
    parts = m.group(1).split(",")
    if len(parts) < 32:
        raise ValueError("行情数据格式错误")
    name = parts[0]
    open_price = float(parts[1]) if parts[1] else 0.0
    prev_close = float(parts[2]) if parts[2] else open_price
    price = float(parts[3]) if parts[3] else prev_close
    high = float(parts[4]) if parts[4] else price
    low = float(parts[5]) if parts[5] else price
    dt = parts[30] + " " + parts[31]
    change_amount = price - prev_close
    change_percent = (change_amount / prev_close * 100) if prev_close else 0.0
    code = sym[2:]
    return {
        "code": code,
        "name": name,
        "price": round_price(price),
        "change_percent": round_price(change_percent),
        "change_amount": round_price(change_amount),
        "open": round_price(open_price),
        "high": round_price(high),
        "low": round_price(low),
        "prev_close": round_price(prev_close),
        "time": dt,
    }


def _fetch_third_party(symbol: str) -> Optional[Dict[str, Any]]:
    base = os.environ.get("THIRD_PARTY_BASE_URL")
    api_key = os.environ.get("THIRD_PARTY_API_KEY")
    if not base:
        return None
    if "biyingapi.com" in base or base.rstrip("/").endswith("/hsstock/instrument"):
        return None
    params = {"symbol": symbol}
    if api_key:
        params["api_key"] = api_key
    url = base.rstrip("/") + "/quote"
    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        return None
    data = resp.json()
    if not isinstance(data, dict):
        return None
    required = ["code", "name", "price", "prev_close", "open", "high", "low", "time"]
    if not all(k in data for k in required):
        return None
    price = float(data["price"]) if data["price"] is not None else 0.0
    prev_close = float(data["prev_close"]) if data["prev_close"] is not None else price
    change_amount = price - prev_close
    change_percent = (change_amount / prev_close * 100) if prev_close else 0.0
    return {
        "code": str(data["code"]),
        "name": str(data["name"]),
        "price": round_price(price),
        "change_percent": round_price(change_percent),
        "change_amount": round_price(change_amount),
        "open": round_price(float(data["open"])) if data["open"] is not None else round_price(price),
        "high": round_price(float(data["high"])) if data["high"] is not None else round_price(price),
        "low": round_price(float(data["low"])) if data["low"] is not None else round_price(price),
        "prev_close": round_price(prev_close),
        "time": str(data["time"]),
    }


def get_quote(symbol: str) -> Dict[str, Any]:
    sym = normalize_symbol(symbol)
    third = _fetch_third_party(symbol)
    if third is not None:
        return third
    return _fetch_sina(sym)


def get_quote_price(symbol: str) -> float:
    q = get_quote(symbol)
    return float(q.get("price", 0.0))
