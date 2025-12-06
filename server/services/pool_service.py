import os
import requests
import time
from typing import Dict, Any, List, Optional

from core.utils import round_price, format_hms, read_env_from_file


def _to_float(v: Any) -> float:
    s = str(v or "").strip()
    if not s:
        return 0.0
    s = s.replace(",", "")
    if s.endswith("%"):
        s = s[:-1]
    try:
        return float(s)
    except Exception:
        return 0.0


def _to_int(v: Any) -> int:
    s = str(v or "").strip()
    if not s:
        return 0
    if s in ("是", "Y", "y", "true", "True", "1"):
        return 1
    if s in ("否", "N", "n", "false", "False", "0"):
        return 0
    s = s.replace(",", "")
    try:
        return int(float(s))
    except Exception:
        return 0


def get_limit_up_pool(date: Optional[str] = None, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    base = os.environ.get("THIRD_PARTY_ZTGC_BASE_URL") or "https://api.biyingapi.com/hslt/ztgc"
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
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
    def _float(v: Any) -> float:
        s = str(v or "").strip()
        if not s:
            return 0.0
        s = s.replace(",", "")
        if s.endswith("%"):
            s = s[:-1]
        try:
            return float(s)
        except Exception:
            return 0.0

    def _int(v: Any) -> int:
        s = str(v or "").strip()
        if not s:
            return 0
        if s in ("是", "Y", "y", "true", "True", "1"):
            return 1
        if s in ("否", "N", "n", "false", "False", "0"):
            return 0
        s = s.replace(",", "")
        try:
            return int(float(s))
        except Exception:
            return 0

    items: List[Dict[str, Any]] = []
    for it in data:
        items.append({
            "code": str(it.get("dm") or ""),
            "name": str(it.get("mc") or ""),
            "price": round_price(_to_float(it.get("p"))),
            "change_percent": round_price(_to_float(it.get("zf"))),
            "amount": round_price(_to_float(it.get("cje"))),
            "float_market_cap": round_price(_to_float(it.get("lt"))),
            "total_market_cap": round_price(_to_float(it.get("zsz"))),
            "turnover_rate": round_price(_to_float(it.get("hs"))),
            "consecutive_boards": _to_int(it.get("lbc")),
            "first_board_time": format_hms(str(it.get("fbt") or "")),
            "last_board_time": format_hms(str(it.get("lbt") or "")),
            "seal_funds": round_price(_to_float(it.get("zj"))),
            "broken_boards": _to_int(it.get("zbc")),
            "stat": str(it.get("tj") or ""),
        })
    return items


def get_limit_down_pool(date: Optional[str] = None, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    base = os.environ.get("THIRD_PARTY_DTGC_BASE_URL") or "http://api.biyingapi.com/hslt/dtgc"
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
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
        raise ValueError("跌停股池接口请求失败")
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("跌停股池返回格式错误")
    items: List[Dict[str, Any]] = []
    for it in data:
        items.append({
            "dm": str(it.get("dm") or ""),
            "mc": str(it.get("mc") or ""),
            "p": round_price(_to_float(it.get("p"))),
            "zf": round_price(_to_float(it.get("zf"))),
            "cje": round_price(_to_float(it.get("cje"))),
            "lt": round_price(_to_float(it.get("lt"))),
            "zsz": round_price(_to_float(it.get("zsz"))),
            "pe": round_price(_to_float(it.get("pe"))),
            "hs": round_price(_to_float(it.get("hs"))),
            "lbc": _to_int(it.get("lbc")),
            "lbt": str(it.get("lbt") or ""),
            "zj": round_price(_to_float(it.get("zj"))),
            "fba": round_price(_to_float(it.get("fba"))),
            "zbc": _to_int(it.get("zbc")),
        })
    return items


def get_break_pool(date: Optional[str] = None, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    base = os.environ.get("THIRD_PARTY_ZBGC_BASE_URL") or "http://api.biyingapi.com/hslt/zbgc"
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
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
        raise ValueError("炸板股池接口请求失败")
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("炸板股池返回格式错误")
    items: List[Dict[str, Any]] = []
    for it in data:
        items.append({
            "dm": str(it.get("dm") or ""),
            "mc": str(it.get("mc") or ""),
            "p": round_price(_to_float(it.get("p"))),
            "ztp": round_price(_to_float(it.get("ztp"))),
            "zf": round_price(_to_float(it.get("zf"))),
            "cje": round_price(_to_float(it.get("cje"))),
            "lt": round_price(_to_float(it.get("lt"))),
            "zsz": round_price(_to_float(it.get("zsz"))),
            "zs": round_price(_to_float(it.get("zs"))),
            "hs": round_price(_to_float(it.get("hs"))),
            "tj": str(it.get("tj") or ""),
            "fbt": str(it.get("fbt") or ""),
            "zbc": _to_int(it.get("zbc")),
        })
    return items


def get_strong_pool(date: Optional[str] = None, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    base = os.environ.get("THIRD_PARTY_QSGC_BASE_URL") or "https://api.biyingapi.com/hslt/qsgc"
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
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
        # 协议回退 https->http
        if base.startswith("https://"):
            alt = "http://" + base[len("https://"):]
            url = alt.rstrip("/") + "/" + date + "/" + api_key
            resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            # 尝试读取错误详情
            try:
                err = resp.json()
            except Exception:
                err = resp.text
            raise ValueError(f"强势股池接口请求失败: {err}")
    try:
        data = resp.json()
    except Exception:
        # 若解析失败再尝试协议回退
        if base.startswith("https://"):
            alt = "http://" + base[len("https://"):]
            url = alt.rstrip("/") + "/" + date + "/" + api_key
            resp = requests.get(url, headers=headers, timeout=10)
            try:
                data = resp.json()
            except Exception:
                raise ValueError("强势股池返回格式错误")
    if not isinstance(data, list):
        # 有时返回错误对象，提取信息提示
        msg = ""
        if isinstance(data, dict):
            msg = data.get("error") or data.get("msg") or data.get("message") or ""
        raise ValueError(f"强势股池返回格式错误{(': ' + msg) if msg else ''}")
    items: List[Dict[str, Any]] = []
    for it in data:
        items.append({
            "dm": str(it.get("dm") or ""),
            "mc": str(it.get("mc") or ""),
            "p": round_price(_to_float(it.get("p"))),
            "ztp": round_price(_to_float(it.get("ztp"))),
            "zf": round_price(_to_float(it.get("zf"))),
            "cje": round_price(_to_float(it.get("cje"))),
            "lt": round_price(_to_float(it.get("lt"))),
            "zsz": round_price(_to_float(it.get("zsz"))),
            "zs": round_price(_to_float(it.get("zs"))),
            "nh": _to_int(it.get("nh")),
            "lb": round_price(_to_float(it.get("lb"))),
            "hs": round_price(_to_float(it.get("hs"))),
            "tj": str(it.get("tj") or ""),
        })
    return items
