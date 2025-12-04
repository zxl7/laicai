import re
import time
import os
from typing import Dict, Any, Optional, List

import requests


def _normalize_symbol(symbol: str) -> str:
    s = symbol.strip().lower()
    m = re.match(r"^(\d{6})\.(sh|sz)$", s)
    if m:
        return f"{m.group(2)}{m.group(1)}"
    m = re.match(r"^(sh|sz)\d{6}$", s)
    if m:
        return s
    m = re.match(r"^(\d{6})$", s)
    if m:
        code = m.group(1)
        prefix = "sh" if code.startswith("6") or code.startswith("9") else "sz"
        return f"{prefix}{code}"
    raise ValueError("symbol格式不正确")


def _round_price(v: float) -> float:
    return float(f"{v:.2f}")


def _limit_rate(code: str, name: str) -> float:
    n = name.upper()
    if n.startswith("*ST") or n.startswith("ST"):
        return 0.05
    if code.startswith("300") or code.startswith("301") or code.startswith("688"):
        return 0.20
    return 0.10


def _symbol_to_instrument(symbol: str) -> str:
    s = symbol.strip().lower()
    m = re.match(r"^(sh|sz)(\d{6})$", s)
    if m:
        exch = m.group(1).upper()
        code = m.group(2)
        return f"{code}.{exch}"
    m = re.match(r"^(\d{6})$", s)
    if m:
        code = m.group(1)
        exch = "SH" if code.startswith("6") or code.startswith("9") else "SZ"
        return f"{code}.{exch}"
    m = re.match(r"^(\d{6})\.(sh|sz)$", s)
    if m:
        return f"{m.group(1)}.{m.group(2).upper()}"
    raise ValueError("symbol格式不正确")


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
        "price": _round_price(price),
        "change_percent": _round_price(change_percent),
        "change_amount": _round_price(change_amount),
        "open": _round_price(open_price),
        "high": _round_price(high),
        "low": _round_price(low),
        "prev_close": _round_price(prev_close),
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
        "price": _round_price(price),
        "change_percent": _round_price(change_percent),
        "change_amount": _round_price(change_amount),
        "open": _round_price(float(data["open"])) if data["open"] is not None else _round_price(price),
        "high": _round_price(float(data["high"])) if data["high"] is not None else _round_price(price),
        "low": _round_price(float(data["low"])) if data["low"] is not None else _round_price(price),
        "prev_close": _round_price(prev_close),
        "time": str(data["time"]),
    }

def get_quote(symbol: str) -> Dict[str, Any]:
    sym = _normalize_symbol(symbol)
    third = _fetch_third_party(symbol)
    if third is not None:
        return third
    return _fetch_sina(sym)


def get_limit_status(symbol: str) -> Dict[str, Any]:
    base = os.environ.get("THIRD_PARTY_BASE_URL")
    api_key = os.environ.get("THIRD_PARTY_API_KEY")
    if base and ("biyingapi.com" in base or base.rstrip("/").endswith("/hsstock/instrument")):
        try:
            instrument = _symbol_to_instrument(symbol)
            url = base.rstrip("/") + "/" + instrument + ("/" + api_key if api_key else "")
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json, */*;q=0.1",
                "Connection": "keep-alive",
                "Referer": "https://api.biyingapi.com/",
            }
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                raise ValueError("第三方接口请求失败")
            data = resp.json()
            if not isinstance(data, dict):
                raise ValueError("第三方接口返回格式错误")
            code_tp = str(data.get("ii") or "")
            name_tp = str(data.get("name") or "")
            prev_close = float(data.get("pc") or 0.0)
            up = float(data.get("up") or 0.0)
            down = float(data.get("dp") or 0.0)
            sina = _fetch_sina(_normalize_symbol(symbol))
            price = sina.get("price", 0.0)
            is_flag = int(data.get("is") or 0)
            is_up = bool(is_flag == 1 or (price >= up - 1e-6))
            is_down = bool(is_flag == -1 or (price <= down + 1e-6))
            rate = 0.0
            if prev_close:
                rate = _round_price((up / prev_close) - 1.0) if up else _limit_rate(code_tp or sina.get("code", ""), name_tp or sina.get("name", ""))
            return {
                "code": code_tp or sina.get("code", ""),
                "name": name_tp or sina.get("name", ""),
                "price": price,
                "limit_up_price": _round_price(up) if up else _round_price(prev_close * (1 + rate)),
                "limit_down_price": _round_price(down) if down else _round_price(prev_close * (1 - rate)),
                "is_limit_up": bool(is_up),
                "is_limit_down": bool(is_down),
                "limit_rate": _round_price(rate if rate else _limit_rate(code_tp or sina.get("code", ""), name_tp or sina.get("name", ""))),
            }
        except Exception:
            pass
    q = get_quote(symbol)
    rate = _limit_rate(q["code"], q["name"])
    up = _round_price(q["prev_close"] * (1 + rate))
    down = _round_price(q["prev_close"] * (1 - rate))
    is_up = q["price"] >= up - 1e-6
    is_down = q["price"] <= down + 1e-6
    return {
        "code": q["code"],
        "name": q["name"],
        "price": q["price"],
        "limit_up_price": up,
        "limit_down_price": down,
        "is_limit_up": bool(is_up),
        "is_limit_down": bool(is_down),
        "limit_rate": rate,
    }


def get_limit_up_pool(date: Optional[str] = None) -> List[Dict[str, Any]]:
    base = os.environ.get("THIRD_PARTY_ZTGC_BASE_URL") or "https://api.biyingapi.com/hslt/ztgc"
    api_key = os.environ.get("THIRD_PARTY_API_KEY")
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    if not date:
        date = time.strftime("%Y-%m-%d", time.localtime())
    url = base.rstrip("/") + "/" + date + "/" + api_key
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, */*;q=0.1",
        "Connection": "keep-alive",
        "Referer": "https://api.biyingapi.com/",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise ValueError("涨停股池接口请求失败")
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("涨停股池返回格式错误")
    items: List[Dict[str, Any]] = []
    for it in data:
        dm = str(it.get("dm") or "")
        mc = str(it.get("mc") or "")
        price = float(it.get("p") or 0.0)
        zf = float(it.get("zf") or 0.0)
        cje = float(it.get("cje") or 0.0)
        lt = float(it.get("lt") or 0.0)
        zsz = float(it.get("zsz") or 0.0)
        hs = float(it.get("hs") or 0.0)
        lbc = int(it.get("lbc") or 0)
        fbt_raw = str(it.get("fbt") or "")
        lbt_raw = str(it.get("lbt") or "")
        def _fmt_hms(s: str) -> str:
            s = s.strip()
            if len(s) == 6 and s.isdigit():
                return f"{s[0:2]}:{s[2:4]}:{s[4:6]}"
            return s
        fbt = _fmt_hms(fbt_raw)
        lbt = _fmt_hms(lbt_raw)
        zj = float(it.get("zj") or 0.0)
        zbc = int(it.get("zbc") or 0)
        tj = str(it.get("tj") or "")
        items.append({
            "code": dm,
            "name": mc,
            "price": _round_price(price),
            "change_percent": _round_price(zf),
            "amount": _round_price(cje),
            "float_market_cap": _round_price(lt),
            "total_market_cap": _round_price(zsz),
            "turnover_rate": _round_price(hs),
            "consecutive_boards": lbc,
            "first_board_time": fbt,
            "last_board_time": lbt,
            "seal_funds": _round_price(zj),
            "broken_boards": zbc,
            "stat": tj,
        })
    return items

from .services.quote_service import get_quote as __svc_get_quote
from .services.limit_service import get_limit_status as __svc_get_limit_status
from .services.pool_service import get_limit_up_pool as __svc_get_limit_up_pool

def get_quote(symbol: str) -> Dict[str, Any]:
    return __svc_get_quote(symbol)

def get_limit_status(symbol: str) -> Dict[str, Any]:
    return __svc_get_limit_status(symbol)

def get_limit_up_pool(date: Optional[str] = None) -> List[Dict[str, Any]]:
    return __svc_get_limit_up_pool(date)
