import re
import requests
from typing import Dict, Any, Optional

from core.utils import normalize_symbol, round_price


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


def get_quote(symbol: str) -> Dict[str, Any]:
    sym = normalize_symbol(symbol)
    return _fetch_sina(sym)


def get_quote_price(symbol: str) -> float:
    return float(get_quote(symbol).get("price", 0.0))

