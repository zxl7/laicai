import os
from typing import Dict, Any, List, Optional

from core.utils import normalize_symbol, round_price, read_env_from_file
from core.http_client import get_json


def _to_float(v: Any) -> float:
    """
    将任意值转换为浮点数的辅助函数
    
    支持处理字符串、百分比值、空值等各种类型的输入，并进行适当的格式化和转换。
    
    Args:
        v: 需要转换为浮点数的任意值
        
    Returns:
        float: 转换后的浮点数，如果转换失败则返回 0.0
    """
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
    """
    将公开源实时交易数据映射为标准格式的辅助函数
    
    从第三方API返回的原始数据中提取并格式化所需字段，转换为统一的数据结构。
    
    Args:
        it: 原始实时交易数据字典
        
    Returns:
        Dict[str, Any]: 格式化后的实时交易数据字典
            - fm: 浮筹
            - h: 最高价
            - hs: 换手率
            - lb: 连板
            - l: 最低价
            - lt: 流通市值
            - o: 开盘价
            - pe: 市盈率
            - pc: 成交量
            - p: 当前价格
            - sz: 总市值
            - cje: 成交额
            - ud: 涨跌额
            - v: 成交量
            - yc: 昨收
            - zf: 涨跌幅
            - zs: 总手
            - sjl: 净流入
            - zdf60: 60分钟涨跌幅
            - zdfnc: 年内涨跌幅
            - t: 更新时间
    """
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


def get_realtime_public(symbol: str, api_key: str) -> List[Dict[str, Any]]:
    """
    获取公开源实时交易数据
    
    从第三方API获取单只股票的公开源实时交易数据，并进行格式化处理后返回。
    数据包括价格、涨跌、成交量、成交额、市值、更新时间等信息。
    
    Args:
        symbol: 股票代码，支持多种格式（如 600000、sh600000、000547.SZ 等）
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[Dict[str, Any]]: 实时交易数据列表
            每个字典包含一只股票的实时交易信息，字段包括：
            - fm: 浮筹
            - h: 最高价
            - hs: 换手率
            - lb: 连板
            - l: 最低价
            - lt: 流通市值
            - o: 开盘价
            - pe: 市盈率
            - pc: 成交量
            - p: 当前价格
            - sz: 总市值
            - cje: 成交额
            - ud: 涨跌额
            - v: 成交量
            - yc: 昨收
            - zf: 涨跌幅
            - zs: 总手
            - sjl: 净流入
            - zdf60: 60分钟涨跌幅
            - zdfnc: 年内涨跌幅
            - t: 更新时间
    
    Raises:
        ValueError: 当缺少 API 密钥、请求失败或返回格式错误时抛出
    """
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


def get_realtime_broker(symbol: str, api_key: str) -> List[Dict[str, Any]]:
    """
    获取券商源实时交易数据
    
    从第三方API获取单只股票的券商源实时交易数据，并进行格式化处理后返回。
    数据包括最新价、开盘价、最高价、最低价、前收盘价、成交量、成交额、市盈率、换手率、市净率等信息。
    
    Args:
        symbol: 股票代码，支持多种格式（如 600000、sh600000、000547.SZ 等）
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[Dict[str, Any]]: 实时交易数据列表
            每个字典包含一只股票的实时交易信息，字段包括：
            - p: 当前价格
            - o: 开盘价
            - h: 最高价
            - l: 最低价
            - yc: 昨收
            - cje: 成交额
            - v: 成交量
            - pv: 前成交量
            - t: 更新时间
            - ud: 涨跌额
            - pc: 成交量
            - zf: 涨跌幅
            - pe: 市盈率
            - tr: 换手率
            - pb_ratio: 市净率
            - tv: 总市值
    
    Raises:
        ValueError: 当缺少 API 密钥、请求失败或返回格式错误时抛出
    """
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


def get_realtime_public_batch(symbols: List[str], api_key: str) -> List[Dict[str, Any]]:
    """
    获取公开源批量实时交易数据
    
    从第三方API获取多只股票的公开源实时交易数据，并进行格式化处理后返回。
    数据包括股票代码、价格、涨跌、成交量、成交额、市值、更新时间等信息。
    
    Args:
        symbols: 股票代码列表，支持多种格式（如 ["600000", "000001"] 等）
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[Dict[str, Any]]: 批量实时交易数据列表
            每个字典包含一只股票的实时交易信息，字段包括：
            - dm: 股票代码
            - p: 当前价格
            - o: 开盘价
            - h: 最高价
            - l: 最低价
            - yc: 昨收
            - cje: 成交额
            - v: 成交量
            - pv: 前成交量
            - t: 更新时间
            - ud: 涨跌额
            - pc: 成交量
            - zf: 涨跌幅
            - pe: 市盈率
            - tr: 换手率
            - pb_ratio: 市净率
            - tv: 总市值
    
    Raises:
        ValueError: 当缺少 API 密钥、请求失败或返回格式错误时抛出
    """
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
