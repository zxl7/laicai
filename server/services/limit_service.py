import os
import json
from typing import Dict, Any
from urllib.request import Request, urlopen

from core.utils import normalize_symbol, round_price, limit_rate, symbol_to_instrument, read_env_from_file
from services.quote_service import get_quote, get_quote_price


def get_limit_status(symbol: str) -> Dict[str, Any]:
    base = os.environ.get("THIRD_PARTY_BASE_URL")
    api_key = os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
    if base and ("biyingapi.com" in base or base.rstrip("/").endswith("/hsstock/instrument")):
        try:
            instrument = symbol_to_instrument(symbol)
            url = base.rstrip("/") + "/" + instrument + ("/" + api_key if api_key else "")
            req = Request(url, headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json, */*;q=0.1",
                "Connection": "keep-alive",
                "Referer": "https://api.biyingapi.com/",
            })
            with urlopen(req, timeout=10) as resp:
                if resp.status != 200:
                    raise ValueError("第三方接口请求失败")
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
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

