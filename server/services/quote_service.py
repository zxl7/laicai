import re
from typing import Dict, Any, Optional

from core.utils import normalize_symbol, round_price
from core.http_client import get_text


def _fetch_sina(sym: str) -> Dict[str, Any]:
    """
    从新浪财经获取股票行情数据的私有函数
    
    通过调用新浪财经的接口获取股票行情数据，并进行解析和格式化处理。
    新浪接口返回的数据格式为特定的字符串，需要进行正则匹配和分割处理。
    
    Args:
        sym: 归一化后的股票代码，如 "sh600000"（上海）或 "sz000001"（深圳）
        
    Returns:
        Dict[str, Any]: 包含股票行情信息的字典
            - code: 股票代码（不含市场前缀）
            - name: 股票名称
            - price: 当前价格
            - change_percent: 涨跌幅百分比
            - change_amount: 涨跌额
            - open: 开盘价
            - high: 最高价
            - low: 最低价
            - prev_close: 前收盘价
            - time: 行情时间
    
    Raises:
        ValueError: 当未获取到行情数据或数据格式错误时抛出
    """
    txt = get_text("http://hq.sinajs.cn/list=" + sym, timeout=5, referer="https://finance.sina.com.cn/")
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
    """
    获取股票行情数据的公共函数
    
    对外提供的行情查询接口，首先对股票代码进行归一化处理，然后调用新浪财经接口获取数据。
    
    Args:
        symbol: 股票代码，支持多种格式（如 600000、sh600000、000547.SZ 等）
        
    Returns:
        Dict[str, Any]: 包含股票行情信息的字典
            - code: 股票代码（不含市场前缀）
            - name: 股票名称
            - price: 当前价格
            - change_percent: 涨跌幅百分比
            - change_amount: 涨跌额
            - open: 开盘价
            - high: 最高价
            - low: 最低价
            - prev_close: 前收盘价
            - time: 行情时间
    
    Raises:
        ValueError: 当未获取到行情数据或数据格式错误时抛出
    """
    sym = normalize_symbol(symbol)
    return _fetch_sina(sym)


def get_quote_price(symbol: str) -> float:
    """
    获取股票当前价格的便捷函数
    
    是 get_quote 函数的简化版本，只返回股票的当前价格。
    
    Args:
        symbol: 股票代码，支持多种格式（如 600000、sh600000、000547.SZ 等）
        
    Returns:
        float: 股票的当前价格，如果获取失败则返回 0.0
    
    Raises:
        ValueError: 当未获取到行情数据或数据格式错误时抛出
    """
    return float(get_quote(symbol).get("price", 0.0))
