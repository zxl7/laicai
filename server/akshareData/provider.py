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

def get_stock_zh_a_spot_em() -> List[Dict[str, Any]]:
    """
    获取所有A股实时行情数据
    
    Returns:
        List[Dict[str, Any]]: 所有A股的实时行情数据列表
    """
    try:
        import akshare as ak
        import requests
        
        # 检查缓存
        c = _ak_cache.get("stock_zh_a_spot_em")
        if c and c[0] > time.time():
            return c[1]
        
        # 调用akshare获取数据，最多重试3次
        max_retries = 3
        for attempt in range(max_retries):
            try:
                df = ak.stock_zh_a_spot_em()
                if df is None or df.empty:
                    raise ValueError("akshare stock_zh_a_spot_em 未返回数据")
                break
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError) as e:
                if attempt == max_retries - 1:
                    raise ValueError(f"网络连接错误，已重试 {max_retries} 次: {str(e)}")
                # 等待一段时间后重试
                time.sleep(1)
            except Exception as e:
                raise ValueError(str(e))
        
        # 转换数据并返回
        data = df.fillna(0).to_dict(orient="records")
        
        # 设置缓存（有效期30秒）
        _ak_cache["stock_zh_a_spot_em"] = (time.time() + 30, data)
        
        return data
    except Exception as e:
        raise ValueError(str(e))


_ak_cache: Dict[str, Any] = {}


def get_stock_market_activity_legu() -> List[Dict[str, Any]]:
    try:
        import akshare as ak
        c = _ak_cache.get("market_activity_legu")
        if c and c[0] > time.time():
            return c[1]
        df = ak.stock_market_activity_legu()
        if df is None or df.empty:
            raise ValueError("乐咕乐股-赚钱情绪数据为空")
        data = df.fillna(0).to_dict(orient="records")
        _ak_cache["market_activity_legu"] = (time.time() + 300, data)
        return data
    except Exception as e:
        raise ValueError(str(e))


def get_stock_individual_basic_info_xq(symbol: str) -> Dict[str, Any]:
    """
    获取个股基本信息
    
    Args:
        symbol: 股票代码，如 600000 或 sz000001
    
    Returns:
        Dict[str, Any]: 个股基本信息（英文key）
    """
    try:
        import akshare as ak
        code = normalize_symbol(symbol)
        
        # 清除旧的缓存（如果存在的话）
        if f"stock_basic:{code}" in _ak_cache:
            del _ak_cache[f"stock_basic:{code}"]
        
        # 尝试使用akshare获取真实数据
        df = None
        try:
            # 尝试使用stock_individual_basic_info_xq函数
            df = ak.stock_individual_basic_info_xq(symbol=code)
        except Exception as e:
            # 如果失败，尝试其他可能的函数
            try:
                # 尝试使用stock_basic_info_em函数
                df = ak.stock_basic_info_em(symbol=code)
            except Exception as e2:
                # 如果都失败，使用stock_zh_a_info_em函数
                df = ak.stock_zh_a_info_em(symbol=code)
        
        # 直接构造英文key的数据结构
        data = {
            "stock_code": code,
            "stock_name": "",
            "current_price": "",
            "change_percent": "",
            "industry": "",
            "pe_ratio": "",
            "pb_ratio": "",
            "total_market_value": "",
            "circulating_market_value": ""
        }
        
        if df is not None and not df.empty:
            # 将DataFrame转换为字典
            raw_data = df.fillna("").to_dict(orient="records")[0]
            
            # 映射中文key到英文key
            key_mapping = {
                "股票代码": "stock_code",
                "股票名称": "stock_name",
                "最新价": "current_price",
                "涨跌幅": "change_percent",
                "所属行业": "industry",
                "行业": "industry",
                "市盈率": "pe_ratio",
                "PE": "pe_ratio",
                "市净率": "pb_ratio",
                "PB": "pb_ratio",
                "总市值": "total_market_value",
                "流通市值": "circulating_market_value"
            }
            
            # 填充数据
            for zh_key, en_key in key_mapping.items():
                if zh_key in raw_data:
                    data[en_key] = raw_data[zh_key]
            
            # 不保留原始数据中的其他字段，只返回我们明确指定的字段
        
        # 保存到缓存
        _ak_cache[f"stock_basic:{code}"] = (time.time() + 300, data)
        return data
    except Exception as e:
        # 发生错误时，返回一个默认的基本信息结构（英文key）
        return {
            "stock_code": normalize_symbol(symbol),
            "stock_name": "",
            "current_price": "",
            "change_percent": "",
            "industry": "",
            "pe_ratio": "",
            "pb_ratio": "",
            "total_market_value": "",
            "circulating_market_value": "",
            "error_message": f"获取数据失败: {str(e)}"
        }
