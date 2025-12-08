import os
from typing import Dict, Any, Optional

from core.utils import normalize_symbol, round_price, limit_rate, symbol_to_instrument, read_env_from_file
from core.http_client import get_json
from services.quote_service import get_quote, get_quote_price


def get_limit_status(symbol: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    获取股票涨跌停状态信息
    
    优先使用第三方接口获取涨跌停数据，失败时回退到本地计算方式。
    返回股票的涨停价、跌停价、是否涨停、是否跌停等状态信息。
    
    Args:
        symbol: 股票代码，支持多种格式（如 600000、sh600000、000547.SZ 等）
        api_key: API 密钥（可选），用于访问第三方服务
        
    Returns:
        Dict[str, Any]: 包含涨跌停状态信息的字典
            - code: 归一化后的股票代码
            - name: 股票名称
            - price: 当前价格
            - limit_up_price: 涨停价
            - limit_down_price: 跌停价
            - is_limit_up: 是否涨停
            - is_limit_down: 是否跌停
            - limit_rate: 涨跌停幅度
            
    Raises:
        Exception: 当本地计算也失败时，可能抛出各种异常
    """
    base = os.environ.get("THIRD_PARTY_BASE_URL")
    api_key = api_key or os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
    if base and ("biyingapi.com" in base or base.rstrip("/").endswith("/hsstock/instrument")):
        try:
            instrument = symbol_to_instrument(symbol)
            url = base.rstrip("/") + "/" + instrument + ("/" + api_key if api_key else "")
            data = get_json(url, timeout=10, referer="https://api.biyingapi.com/")
            if not isinstance(data, dict):
                raise ValueError("第三方接口返回格式错误")
            code_tp = str(data.get("ii") or "")
            name_tp = str(data.get("name") or "")
            prev_close = float(data.get("pc") or 0.0)
            up = float(data.get("up") or 0.0)
            down = float(data.get("dp") or 0.0)
            price = get_quote_price(symbol)
            is_flag = int(data.get("is") or 0)
            is_up = bool(is_flag == 1 or (price >= up - 1e-6))
            is_down = bool(is_flag == -1 or (price <= down + 1e-6))
            rate = 0.0
            if prev_close:
                rate = round_price((up / prev_close) - 1.0) if up else limit_rate(code_tp or code_tp, name_tp or name_tp)
            return {
                "code": code_tp or normalize_symbol(symbol)[2:],
                "name": name_tp,
                "price": price,
                "limit_up_price": round_price(up) if up else round_price(prev_close * (1 + rate)),
                "limit_down_price": round_price(down) if down else round_price(prev_close * (1 - rate)),
                "is_limit_up": bool(is_up),
                "is_limit_down": bool(is_down),
                "limit_rate": round_price(rate if rate else limit_rate(code_tp or normalize_symbol(symbol)[2:], name_tp or "")),
            }
        except Exception:
            pass
    q = get_quote(symbol)
    rate = limit_rate(q["code"], q["name"])
    up = round_price(q["prev_close"] * (1 + rate))
    down = round_price(q["prev_close"] * (1 - rate))
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
