import os
from typing import Dict, Any, List, Optional

from core.utils import normalize_symbol, round_price, read_env_from_file
from core.http_client import get_json


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


def _map_public_item(it: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "fm": round_price(_to_float(it.get("fm"))),
        "h": round_price(_to_float(it.get("h"))),
        "hs": round_price(_to_float(it.get("hs"))),
        "lb": round_price(_to_float(it.get("lb"))),
        "l": round_price(_to_float(it.get("l"))),
        "lt": round_price(_to_float(it.get("lt"))),
        "o": round_price(_to_float(it.get("o"))),
        "pe": round_price(_to_float(it.get("pe"))),
        "pc": round_price(_to_float(it.get("pc"))),
        "p": round_price(_to_float(it.get("p"))),
        "sz": round_price(_to_float(it.get("sz"))),
        "cje": round_price(_to_float(it.get("cje"))),
        "ud": round_price(_to_float(it.get("ud"))),
        "v": round_price(_to_float(it.get("v"))),
        "yc": round_price(_to_float(it.get("yc"))),
        "zf": round_price(_to_float(it.get("zf"))),
        "zs": round_price(_to_float(it.get("zs"))),
        "sjl": round_price(_to_float(it.get("sjl"))),
        "zdf60": round_price(_to_float(it.get("zdf60"))),
        "zdfnc": round_price(_to_float(it.get("zdfnc"))),
        "t": str(it.get("t") or ""),
    }


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
    try:
        data = get_json(url, timeout=10, referer="https://api.biyingapi.com/")
    except Exception:
        raise ValueError("实时交易(公开)接口请求失败")
    if not isinstance(data, list):
        if isinstance(data, dict):
            for k in ("data", "list", "items", "result"):
                v = data.get(k)
                if isinstance(v, list):
                    data = v
                    break
            else:
                # 兼容单条记录返回为对象的情况
                return [_map_public_item(data)]
        else:
            raise ValueError("实时交易(公开)返回格式错误")
    items: List[Dict[str, Any]] = []
    for it in data:
        items.append(_map_public_item(it))
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
    try:
        data = get_json(url, timeout=10, referer="https://api.biyingapi.com/")
    except Exception:
        raise ValueError("实时交易(券商)接口请求失败")
    def _map_broker_item(it: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "p": round_price(_to_float(it.get("p"))),
            "o": round_price(_to_float(it.get("o"))),
            "h": round_price(_to_float(it.get("h"))),
            "l": round_price(_to_float(it.get("l"))),
            "yc": round_price(_to_float(it.get("yc"))),
            "cje": round_price(_to_float(it.get("cje"))),
            "v": round_price(_to_float(it.get("v"))),
            "pv": round_price(_to_float(it.get("pv"))),
            "t": str(it.get("t") or ""),
            "ud": round_price(_to_float(it.get("ud"))),
            "pc": round_price(_to_float(it.get("pc"))),
            "zf": round_price(_to_float(it.get("zf"))),
            "pe": round_price(_to_float(it.get("pe"))),
            "tr": round_price(_to_float(it.get("tr"))),
            "pb_ratio": round_price(_to_float(it.get("pb_ratio"))),
            "tv": round_price(_to_float(it.get("tv"))),
        }
    if isinstance(data, list):
        return [_map_broker_item(it) for it in data]
    if isinstance(data, dict):
        for k in ("data", "list", "items", "result"):
            v = data.get(k)
            if isinstance(v, list):
                return [_map_broker_item(it) for it in v]
        return [_map_broker_item(data)]
    raise ValueError("实时交易(券商)返回格式错误")


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
    try:
        data = get_json(url, params=params, timeout=10, referer="https://api.biyingapi.com/")
    except Exception:
        raise ValueError("实时交易(公开-多股)接口请求失败")
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
