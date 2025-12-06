from typing import Dict, Any, List, Optional
import time

from core.utils import normalize_symbol, round_price


def get_quote_by_akshare(symbol: str) -> Dict[str, float]:
    code = normalize_symbol(symbol)[2:]
    _c = _ak_cache.get(f"quote:{code}")
    if _c and _c[0] > time.time():
        return _c[1]
    try:
        import akshare as ak
        df = ak.stock_zh_a_spot_em()
        if df is None or df.empty:
            raise ValueError("akshare未返回数据")
        row = df.loc[df["代码"].astype(str) == code]
        if row.empty:
            raise ValueError("未找到该代码的akshare数据")
        r = row.iloc[0]
        price = float(r.get("最新价") or 0.0)
        prev_close = float(r.get("昨收") or price)
        change_amount = price - prev_close
        change_percent = (change_amount / prev_close * 100.0) if prev_close else 0.0
        data = {
            "code": str(r.get("代码") or code),
            "name": str(r.get("名称") or ""),
            "price": round_price(price),
            "change_percent": round_price(change_percent),
            "change_amount": round_price(change_amount),
            "open": round_price(float(r.get("今开") or 0.0)),
            "high": round_price(float(r.get("最高") or price)),
            "low": round_price(float(r.get("最低") or price)),
            "prev_close": round_price(prev_close),
            "time": str(r.get("最新交易日") or r.get("更新时间") or ""),
        }
        _ak_cache[f"quote:{code}"] = (time.time() + 30, data)
        return data
    except Exception:
        from services.quote_service import get_quote
        return get_quote(symbol)


def get_board_concept_info_ths(concept: Optional[str] = None, code: Optional[str] = None, date: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        import akshare as ak
        symbol = concept or code or ""
        if not symbol:
            raise ValueError("缺少板块概念名称或代码")
        df = ak.stock_board_concept_info_ths(symbol=symbol, date=date)
        if df is None or df.empty:
            raise ValueError("板块概念数据为空")
        data = df.fillna(0).to_dict(orient="records")
        _ak_cache[f"concept_info:{symbol}:{date or ''}"] = (time.time() + 30, data)
        return data
    except Exception as e:
        raise ValueError(str(e))


def get_board_concept_list_ths() -> List[Dict[str, Any]]:
    try:
        import akshare as ak
        df = ak.stock_board_concept_name_ths()
        if df is None or df.empty:
            raise ValueError("板块概念列表为空")
        data = df.fillna(0).to_dict(orient="records")
        _ak_cache["concept_list"] = (time.time() + 300, data)
        return data
    except Exception as e:
        raise ValueError(str(e))

_ak_cache: Dict[str, Any] = {}
