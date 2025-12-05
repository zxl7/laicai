import os
import requests
from typing import Dict, Any, List, Optional

from core.utils import normalize_symbol, round_price, read_env_from_file


def get_realtime_public(symbol: str, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    公开源实时交易
    - 数据源: http://api.biyingapi.com/hsrl/ssjy/{code}/{licence}
    - 返回: 列表，包含价、涨跌、量额、市值、更新时间等
    """
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    code = normalize_symbol(symbol)[2:]
    base = os.environ.get("THIRD_PARTY_SSJY_BASE_URL") or "http://api.biyingapi.com/hsrl/ssjy"
    url = base.rstrip("/") + f"/{code}/{api_key}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, */*;q=0.1",
        "Connection": "keep-alive",
        "Referer": "https://api.biyingapi.com/",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise ValueError("实时交易(公开)接口请求失败")
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("实时交易(公开)返回格式错误")
    items: List[Dict[str, Any]] = []
    for it in data:
        items.append({
            "fm": round_price(float(it.get("fm") or 0.0)),
            "h": round_price(float(it.get("h") or 0.0)),
            "hs": round_price(float(it.get("hs") or 0.0)),
            "lb": round_price(float(it.get("lb") or 0.0)),
            "l": round_price(float(it.get("l") or 0.0)),
            "lt": round_price(float(it.get("lt") or 0.0)),
            "o": round_price(float(it.get("o") or 0.0)),
            "pe": round_price(float(it.get("pe") or 0.0)),
            "pc": round_price(float(it.get("pc") or 0.0)),
            "p": round_price(float(it.get("p") or 0.0)),
            "sz": round_price(float(it.get("sz") or 0.0)),
            "cje": round_price(float(it.get("cje") or 0.0)),
            "ud": round_price(float(it.get("ud") or 0.0)),
            "v": round_price(float(it.get("v") or 0.0)),
            "yc": round_price(float(it.get("yc") or 0.0)),
            "zf": round_price(float(it.get("zf") or 0.0)),
            "zs": round_price(float(it.get("zs") or 0.0)),
            "sjl": round_price(float(it.get("sjl") or 0.0)),
            "zdf60": round_price(float(it.get("zdf60") or 0.0)),
            "zdfnc": round_price(float(it.get("zdfnc") or 0.0)),
            "t": str(it.get("t") or ""),
        })
    return items


def get_realtime_broker(symbol: str, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    券商源实时交易
    - 数据源: https://api.biyingapi.com/hsstock/real/time/{code}/{licence}
    - 返回: 列表，包含最新价、开高低、前收、量额、市盈率、换手、市净率等
    """
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    code = normalize_symbol(symbol)[2:]
    base = os.environ.get("THIRD_PARTY_REALTIME_BASE_URL") or "https://api.biyingapi.com/hsstock/real/time"
    url = base.rstrip("/") + f"/{code}/{api_key}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, */*;q=0.1",
        "Connection": "keep-alive",
        "Referer": "https://api.biyingapi.com/",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise ValueError("实时交易(券商)接口请求失败")
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("实时交易(券商)返回格式错误")
    items: List[Dict[str, Any]] = []
    for it in data:
        items.append({
            "p": round_price(float(it.get("p") or 0.0)),
            "o": round_price(float(it.get("o") or 0.0)),
            "h": round_price(float(it.get("h") or 0.0)),
            "l": round_price(float(it.get("l") or 0.0)),
            "yc": round_price(float(it.get("yc") or 0.0)),
            "cje": round_price(float(it.get("cje") or 0.0)),
            "v": round_price(float(it.get("v") or 0.0)),
            "pv": round_price(float(it.get("pv") or 0.0)),
            "t": str(it.get("t") or ""),
            "ud": round_price(float(it.get("ud") or 0.0)),
            "pc": round_price(float(it.get("pc") or 0.0)),
            "zf": round_price(float(it.get("zf") or 0.0)),
            "pe": round_price(float(it.get("pe") or 0.0)),
            "tr": round_price(float(it.get("tr") or 0.0)),
            "pb_ratio": round_price(float(it.get("pb_ratio") or 0.0)),
            "tv": round_price(float(it.get("tv") or 0.0)),
        })
    return items


def get_realtime_public_batch(symbols: List[str], api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    公开源批量实时交易
    - 数据源: http://api.biyingapi.com/hsrl/ssjy_more/{licence}?stock_codes=code1,...
    - 返回: 列表，字段与公开源单股类似，包含 dm 表示股票代码
    """
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    codes: List[str] = [normalize_symbol(s)[2:] for s in symbols]
    base = os.environ.get("THIRD_PARTY_SSJY_MORE_BASE_URL") or "http://api.biyingapi.com/hsrl/ssjy_more"
    url = base.rstrip("/") + f"/{api_key}"
    params = {"stock_codes": ",".join(codes)}
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, */*;q=0.1",
        "Connection": "keep-alive",
        "Referer": "https://api.biyingapi.com/",
    }
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise ValueError("实时交易(公开-多股)接口请求失败")
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("实时交易(公开-多股)返回格式错误")
    items: List[Dict[str, Any]] = []
    for it in data:
        items.append({
            "dm": str(it.get("dm") or ""),
            "p": round_price(float(it.get("p") or 0.0)),
            "o": round_price(float(it.get("o") or 0.0)),
            "h": round_price(float(it.get("h") or 0.0)),
            "l": round_price(float(it.get("l") or 0.0)),
            "yc": round_price(float(it.get("yc") or 0.0)),
            "cje": round_price(float(it.get("cje") or 0.0)),
            "v": round_price(float(it.get("v") or 0.0)),
            "pv": round_price(float(it.get("pv") or 0.0)),
            "t": str(it.get("t") or ""),
            "ud": round_price(float(it.get("ud") or 0.0)),
            "pc": round_price(float(it.get("pc") or 0.0)),
            "zf": round_price(float(it.get("zf") or 0.0)),
            "pe": round_price(float(it.get("pe") or 0.0)),
            "tr": round_price(float(it.get("tr") or 0.0)),
            "pb_ratio": round_price(float(it.get("pb_ratio") or 0.0)),
            "tv": round_price(float(it.get("tv") or 0.0)),
        })
    return items

