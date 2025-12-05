import os
import requests
from typing import Dict, Any, List, Optional

from ..common.utils import normalize_symbol, round_price, read_env_from_file


def get_realtime_public(symbol: str, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    公开源实时交易数据
    - 入参: 股票代码(支持 600000 / sh600000 / 000547.SZ 等)
    - 数据源: http://api.biyingapi.com/hsrl/ssjy/{code}/{licence}
    - 更新频率: 交易时段每 ~1 分钟
    - 需环境变量: THIRD_PARTY_API_KEY (licence)
    - 返回: List[dict]，包含 fm/h/hs/lb/l/lt/o/pe/pc/p/sz/cje/ud/v/yc/zf/zs/sjl/zdf60/zdfnc/t
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
    券商源实时交易数据
    - 入参: 股票代码(支持多种格式)
    - 数据源: https://api.biyingapi.com/hsstock/real/time/{code}/{licence}
    - 更新频率: 实时
    - 需环境变量: THIRD_PARTY_API_KEY (licence)
    - 返回: List[dict]，包含 p/o/h/l/yc/cje/v/pv/t/ud/pc/zf/pe/tr/pb_ratio/tv
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
    公开源批量实时交易数据
    - 入参: 股票代码列表(最多20支)
    - 数据源: http://api.biyingapi.com/hsrl/ssjy_more/{licence}?stock_codes=code1,code2,...
    - 更新频率: 实时
    - 需环境变量: THIRD_PARTY_API_KEY (licence)
    - 返回: List[dict]，字段与公开源单股类似，包含 dm 表示股票代码
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


def get_limit_down_pool(date: Optional[str] = None, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    跌停股池
    - 入参: 日期(yyyy-MM-dd，默认当天)
    - 数据源: http://api.biyingapi.com/hslt/dtgc/{date}/{licence}
    - 更新频率: 交易时间段每 ~10 分钟
    - 返回: List[dict]，包含 dm/mc/p/zf/cje/lt/zsz/pe/hs/lbc/lbt/zj/fba/zbc
    """
    base = os.environ.get("THIRD_PARTY_DTGC_BASE_URL") or "http://api.biyingapi.com/hslt/dtgc"
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    import time
    if not date:
        date = time.strftime("%Y-%m-%d", time.localtime())
    url = base.rstrip("/") + f"/{date}/{api_key}"
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
            "p": round_price(float(it.get("p") or 0.0)),
            "zf": round_price(float(it.get("zf") or 0.0)),
            "cje": round_price(float(it.get("cje") or 0.0)),
            "lt": round_price(float(it.get("lt") or 0.0)),
            "zsz": round_price(float(it.get("zsz") or 0.0)),
            "pe": round_price(float(it.get("pe") or 0.0)),
            "hs": round_price(float(it.get("hs") or 0.0)),
            "lbc": int(it.get("lbc") or 0),
            "lbt": str(it.get("lbt") or ""),
            "zj": round_price(float(it.get("zj") or 0.0)),
            "fba": round_price(float(it.get("fba") or 0.0)),
            "zbc": int(it.get("zbc") or 0),
        })
    return items


def get_break_pool(date: Optional[str] = None, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    炸板股池
    - 入参: 日期(yyyy-MM-dd，默认当天)
    - 数据源: http://api.biyingapi.com/hslt/zbgc/{date}/{licence}
    - 更新频率: 交易时间段每 ~10 分钟
    - 返回: List[dict]，包含 dm/mc/p/ztp/zf/cje/lt/zsz/zs/hs/tj/fbt/zbc
    """
    base = os.environ.get("THIRD_PARTY_ZBGC_BASE_URL") or "http://api.biyingapi.com/hslt/zbgc"
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    import time
    if not date:
        date = time.strftime("%Y-%m-%d", time.localtime())
    url = base.rstrip("/") + f"/{date}/{api_key}"
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
            "p": round_price(float(it.get("p") or 0.0)),
            "ztp": round_price(float(it.get("ztp") or 0.0)),
            "zf": round_price(float(it.get("zf") or 0.0)),
            "cje": round_price(float(it.get("cje") or 0.0)),
            "lt": round_price(float(it.get("lt") or 0.0)),
            "zsz": round_price(float(it.get("zsz") or 0.0)),
            "zs": round_price(float(it.get("zs") or 0.0)),
            "hs": round_price(float(it.get("hs") or 0.0)),
            "tj": str(it.get("tj") or ""),
            "fbt": str(it.get("fbt") or ""),
            "zbc": int(it.get("zbc") or 0),
        })
    return items


def get_strong_pool(date: Optional[str] = None, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    强势股池
    - 入参: 日期(yyyy-MM-dd，默认当天)
    - 数据源: http://api.biyingapi.com/hslt/qsgc/{date}/{licence}
    - 更新频率: 交易时间段每 ~10 分钟
    - 返回: List[dict]，包含 dm/mc/p/ztp/zf/cje/lt/zsz/zs/nh/lb/hs/tj
    """
    base = os.environ.get("THIRD_PARTY_QSGC_BASE_URL") or "http://api.biyingapi.com/hslt/qsgc"
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    import time
    if not date:
        date = time.strftime("%Y-%m-%d", time.localtime())
    url = base.rstrip("/") + f"/{date}/{api_key}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, */*;q=0.1",
        "Connection": "keep-alive",
        "Referer": "https://api.biyingapi.com/",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise ValueError("强势股池接口请求失败")
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("强势股池返回格式错误")
    items: List[Dict[str, Any]] = []
    for it in data:
        items.append({
            "dm": str(it.get("dm") or ""),
            "mc": str(it.get("mc") or ""),
            "p": round_price(float(it.get("p") or 0.0)),
            "ztp": round_price(float(it.get("ztp") or 0.0)),
            "zf": round_price(float(it.get("zf") or 0.0)),
            "cje": round_price(float(it.get("cje") or 0.0)),
            "lt": round_price(float(it.get("lt") or 0.0)),
            "zsz": round_price(float(it.get("zsz") or 0.0)),
            "zs": round_price(float(it.get("zs") or 0.0)),
            "nh": int(it.get("nh") or 0),
            "lb": round_price(float(it.get("lb") or 0.0)),
            "hs": round_price(float(it.get("hs") or 0.0)),
            "tj": str(it.get("tj") or ""),
        })
    return items
