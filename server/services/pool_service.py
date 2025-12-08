import os
import time
from typing import Dict, Any, List, Optional

from core.utils import round_price, format_hms, read_env_from_file
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


def _to_int(v: Any) -> int:
    """
    将任意值转换为整数的辅助函数
    
    支持处理字符串、布尔值、数字等各种类型的输入，并进行适当的格式化和转换。
    特别支持中文的"是/否"、英文的"Y/N"、布尔值的"true/false"等表示方式。
    
    Args:
        v: 需要转换为整数的任意值
        
    Returns:
        int: 转换后的整数，如果转换失败则返回 0
    """
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


def get_limit_up_pool(date: str, api_key: str) -> List[Dict[str, Any]]:
    """
    获取指定日期的涨停股池数据
    
    从第三方API获取涨停股池数据，并进行格式化处理后返回。
    数据包括股票代码、名称、价格、涨跌幅、成交量、成交额等信息。
    
    Args:
        date: 查询日期，格式为 YYYY-MM-DD
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[Dict[str, Any]]: 涨停股池数据列表
            每个字典包含一只涨停股票的详细信息，如：
            - code: 股票代码
            - name: 股票名称
            - price: 当前价格
            - change_percent: 涨跌幅百分比
            - amount: 成交额
            - float_market_cap: 流通市值
            - total_market_cap: 总市值
            - turnover_rate: 换手率
            - consecutive_boards: 连续涨停板数
            - first_board_time: 首次涨停时间
            - last_board_time: 最后涨停时间
            - seal_funds: 封单资金
            - broken_boards: 炸板次数
            - stat: 统计信息
    
    Raises:
        ValueError: 当缺少 API 密钥、请求失败或返回格式错误时抛出
    """
    base = os.environ.get("THIRD_PARTY_ZTGC_BASE_URL") or "https://api.biyingapi.com/hslt/ztgc"
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    url = base.rstrip("/") + "/" + date + "/" + api_key
    try:
        data = get_json(url, timeout=10, referer="https://api.biyingapi.com/")
    except Exception as e:
        raise ValueError("涨停股池接口请求失败")
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


def get_limit_down_pool(date: str, api_key: str) -> List[Dict[str, Any]]:
    """
    获取指定日期的跌停股池数据
    
    从第三方API获取跌停股池数据，并进行格式化处理后返回。
    数据包括股票代码、名称、价格、涨跌幅、成交量、成交额等信息。
    
    Args:
        date: 查询日期，格式为 YYYY-MM-DD
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[Dict[str, Any]]: 跌停股池数据列表
            每个字典包含一只跌停股票的详细信息，如：
            - dm: 股票代码
            - mc: 股票名称
            - p: 当前价格
            - zf: 涨跌幅百分比
            - cje: 成交额
            - lt: 流通市值
            - zsz: 总市值
            - pe: 市盈率
            - hs: 换手率
            - lbc: 连续跌停板数
            - lbt: 最后跌停时间
            - zj: 封单资金
            - fba: 封板金额
            - zbc: 炸板次数
    
    Raises:
        ValueError: 当缺少 API 密钥、请求失败或返回格式错误时抛出
    """
    base = os.environ.get("THIRD_PARTY_DTGC_BASE_URL") or "http://api.biyingapi.com/hslt/dtgc"
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    url = base.rstrip("/") + "/" + date + "/" + api_key
    try:
        data = get_json(url, timeout=10, referer="https://api.biyingapi.com/")
    except Exception:
        raise ValueError("跌停股池接口请求失败")
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


def get_break_pool(date: str, api_key: str) -> List[Dict[str, Any]]:
    """
    获取指定日期的炸板股池数据
    
    从第三方API获取炸板股池数据，并进行格式化处理后返回。
    数据包括股票代码、名称、价格、涨停价、涨跌幅、成交量、成交额等信息。
    
    Args:
        date: 查询日期，格式为 YYYY-MM-DD
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[Dict[str, Any]]: 炸板股池数据列表
            每个字典包含一只炸板股票的详细信息，如：
            - dm: 股票代码
            - mc: 股票名称
            - p: 当前价格
            - ztp: 涨停价
            - zf: 涨跌幅百分比
            - cje: 成交额
            - lt: 流通市值
            - zsz: 总市值
            - zs: 总手数
            - hs: 换手率
            - tj: 统计信息
            - fbt: 首次封板时间
            - zbc: 炸板次数
    
    Raises:
        ValueError: 当缺少 API 密钥、请求失败或返回格式错误时抛出
    """
    base = os.environ.get("THIRD_PARTY_ZBGC_BASE_URL") or "http://api.biyingapi.com/hslt/zbgc"
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    url = base.rstrip("/") + "/" + date + "/" + api_key
    try:
        data = get_json(url, timeout=10, referer="https://api.biyingapi.com/")
    except Exception:
        raise ValueError("炸板股池接口请求失败")
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


def get_strong_pool(date: str, api_key: str) -> List[Dict[str, Any]]:
    """
    获取指定日期的强势股池数据
    
    从第三方API获取强势股池数据，并进行格式化处理后返回。
    如果HTTPS请求失败，会自动尝试HTTP请求。
    数据包括股票代码、名称、价格、涨停价、涨跌幅、成交量、成交额等信息。
    
    Args:
        date: 查询日期，格式为 YYYY-MM-DD
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[Dict[str, Any]]: 强势股池数据列表
            每个字典包含一只强势股票的详细信息，如：
            - dm: 股票代码
            - mc: 股票名称
            - p: 当前价格
            - ztp: 涨停价
            - zf: 涨跌幅百分比
            - cje: 成交额
            - lt: 流通市值
            - zsz: 总市值
            - zs: 总手数
            - nh: 内在价值
            - lb: 连板数
            - hs: 换手率
            - tj: 统计信息
    
    Raises:
        ValueError: 当缺少 API 密钥、请求失败或返回格式错误时抛出
    """
    base = os.environ.get("THIRD_PARTY_QSGC_BASE_URL") or "https://api.biyingapi.com/hslt/qsgc"
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    url = base.rstrip("/") + "/" + date + "/" + api_key
    try:
        data = get_json(url, timeout=10, referer="https://api.biyingapi.com/")
    except Exception:
        if base.startswith("https://"):
            alt = "http://" + base[len("https://"):]
            url = alt.rstrip("/") + "/" + date + "/" + api_key
            data = get_json(url, timeout=10, referer="https://api.biyingapi.com/")
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
