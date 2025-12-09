import os
import time
from typing import Dict, Any, List, Optional

from core.utils import round_price, format_hms, read_env_from_file, normalize_symbol
from core.http_client import get_json


class ThirdPartyAPI:
    """
    第三方接口服务统一封装类
    
    整合所有第三方API调用，提供统一的接口访问方式，并封装共用逻辑
    """
    
    @staticmethod
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
    
    @staticmethod
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
    
    @staticmethod
    def handle_api_request(base_url: str, endpoint: str = "", api_key: str = None, 
                         timeout: int = 10, referer: str = None, params: Dict[str, Any] = None) -> Any:
        """
        统一处理API请求的方法
        
        Args:
            base_url: API基础URL
            endpoint: API端点路径
            api_key: API密钥
            timeout: 请求超时时间
            referer: 请求Referer头
            params: 请求参数
            
        Returns:
            Any: API响应数据
            
        Raises:
            ValueError: 当请求失败或返回格式错误时抛出
        """
        # 构建完整URL
        url = base_url.rstrip("/")
        if endpoint:
            url += f"/{endpoint}"
        
        try:
            return get_json(url, timeout=timeout, referer=referer, params=params)
        except Exception as e:
            raise ValueError(f"API请求失败: {str(e)}")
    
    # 行情数据接口
    @classmethod
    def get_stock_quote(cls, symbol: str) -> Dict[str, Any]:
        """
        获取股票行情数据
        
        Args:
            symbol: 股票代码
            
        Returns:
            Dict[str, Any]: 格式化后的股票行情数据
        """
        code = symbol
        if not code.startswith(('sh', 'sz')):
            if code.startswith('6'):
                code = 'sh' + code
            else:
                code = 'sz' + code
        
        base = os.environ.get("SINA_FINANCE_BASE_URL") or "https://hq.sinajs.cn"
        endpoint = f"/list={code}"
        data = cls.handle_api_request(base, endpoint)
        
        # 解析新浪财经返回的数据
        if isinstance(data, str):
            # 新浪财经返回的是类似 "var hq_str_sh600000="浦发银行,10.00,10.10,..."" 的字符串
            parts = data.split(",")
            if len(parts) < 32:
                raise ValueError("行情数据格式错误")
            
            return {
                "code": symbol,
                "name": parts[0].split("=")[1].strip('"'),
                "price": round_price(cls._to_float(parts[1])),
                "open": round_price(cls._to_float(parts[2])),
                "pre_close": round_price(cls._to_float(parts[3])),
                "high": round_price(cls._to_float(parts[4])),
                "low": round_price(cls._to_float(parts[5])),
                "volume": cls._to_int(parts[8]),
                "amount": round_price(cls._to_float(parts[9]) / 10000),
                "time": parts[31].strip('"')
            }
        else:
            raise ValueError("行情数据格式错误")
    
    # 涨跌停相关接口
    @classmethod
    def get_limit_up_info(cls, symbol: str, api_key: str) -> Dict[str, Any]:
        """
        获取股票涨停信息
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            Dict[str, Any]: 股票涨停信息
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        code = normalize_symbol(symbol)[2:]
        base = os.environ.get("THIRD_PARTY_LIMIT_UP_BASE_URL") or "https://api.biyingapi.com/hsstock/limit_up"
        endpoint = f"/{code}/{api_key}"
        
        data = cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
        if not isinstance(data, dict):
            raise ValueError("涨停接口返回格式错误")
        
        return {
            "code": symbol,
            "name": str(data.get("name", "")),
            "price": round_price(cls._to_float(data.get("price", "0"))),
            "limit_up_price": round_price(cls._to_float(data.get("limit_up_price", "0"))),
            "limit_down_price": round_price(cls._to_float(data.get("limit_down_price", "0"))),
            "is_limit_up": bool(data.get("is_limit_up", 0)),
            "is_limit_down": bool(data.get("is_limit_down", 0)),
            "limit_range": 10.0  # 默认涨跌幅限制
        }
    
    @classmethod
    def calculate_limit_prices(cls, symbol: str, price: float) -> Dict[str, Any]:
        """
        计算股票涨跌停价格（备用方法）
        
        Args:
            symbol: 股票代码
            price: 当前价格
            
        Returns:
            Dict[str, Any]: 计算得到的涨跌停价格
        """
        # 科创板股票涨跌幅限制为20%
        if symbol.startswith(('sh68', 'sh688', 'sz30', 'sz300')):
            limit_range = 20.0
        else:
            limit_range = 10.0
        
        # 四舍五入到分
        limit_up_price = round(price * (1 + limit_range / 100), 2)
        limit_down_price = round(price * (1 - limit_range / 100), 2)
        
        return {
            "code": symbol,
            "price": price,
            "limit_up_price": limit_up_price,
            "limit_down_price": limit_down_price,
            "is_limit_up": abs(price - limit_up_price) < 0.01,
            "is_limit_down": abs(price - limit_down_price) < 0.01,
            "limit_range": limit_range
        }
    
    @classmethod
    def get_limit_status(cls, symbol: str, api_key: str = None) -> Dict[str, Any]:
        """
        获取股票涨跌停状态（优先使用第三方接口，失败则本地计算）
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            Dict[str, Any]: 股票涨跌停状态
        """
        try:
            if api_key:
                return cls.get_limit_up_info(symbol, api_key)
            else:
                raise ValueError("API密钥未提供，将使用本地计算")
        except Exception as e:
            # 回退到本地计算
            quote = cls.get_stock_quote(symbol)
            return cls.calculate_limit_prices(symbol, quote['price'])
    
    # 股池接口
    @classmethod
    def get_limit_up_pool(cls, date: str, api_key: str) -> List[Dict[str, Any]]:
        """
        获取涨停股池数据
        
        Args:
            date: 查询日期，格式为 YYYY-MM-DD
            api_key: API密钥
            
        Returns:
            List[Dict[str, Any]]: 涨停股池数据列表
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        base = os.environ.get("THIRD_PARTY_ZTGC_BASE_URL") or "https://api.biyingapi.com/hslt/ztgc"
        endpoint = f"{date}/{api_key}"
        
        data = cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
        if not isinstance(data, list):
            raise ValueError("涨停股池返回格式错误")
        
        items: List[Dict[str, Any]] = []
        for it in data:
            items.append({
                "code": str(it.get("dm") or ""),
                "name": str(it.get("mc") or ""),
                "price": round_price(cls._to_float(it.get("p"))),
                "change_percent": round_price(cls._to_float(it.get("zf"))),
                "amount": round_price(cls._to_float(it.get("cje"))),
                "float_market_cap": round_price(cls._to_float(it.get("lt"))),
                "total_market_cap": round_price(cls._to_float(it.get("zsz"))),
                "turnover_rate": round_price(cls._to_float(it.get("hs"))),
                "consecutive_boards": cls._to_int(it.get("lbc")),
                "first_board_time": format_hms(str(it.get("fbt") or "")),
                "last_board_time": format_hms(str(it.get("lbt") or "")),
                "seal_funds": round_price(cls._to_float(it.get("zj"))),
                "broken_boards": cls._to_int(it.get("zbc")),
                "stat": str(it.get("tj") or ""),
            })
        return items
    
    @classmethod
    def get_limit_down_pool(cls, date: str, api_key: str) -> List[Dict[str, Any]]:
        """
        获取跌停股池数据
        
        Args:
            date: 查询日期，格式为 YYYY-MM-DD
            api_key: API密钥
            
        Returns:
            List[Dict[str, Any]]: 跌停股池数据列表
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        base = os.environ.get("THIRD_PARTY_DTGC_BASE_URL") or "http://api.biyingapi.com/hslt/dtgc"
        endpoint = f"{date}/{api_key}"
        
        data = cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
        if not isinstance(data, list):
            raise ValueError("跌停股池返回格式错误")
        
        items: List[Dict[str, Any]] = []
        for it in data:
            items.append({
                "dm": str(it.get("dm") or ""),
                "mc": str(it.get("mc") or ""),
                "p": round_price(cls._to_float(it.get("p"))),
                "zf": round_price(cls._to_float(it.get("zf"))),
                "cje": round_price(cls._to_float(it.get("cje"))),
                "lt": round_price(cls._to_float(it.get("lt"))),
                "zsz": round_price(cls._to_float(it.get("zsz"))),
                "pe": round_price(cls._to_float(it.get("pe"))),
                "hs": round_price(cls._to_float(it.get("hs"))),
                "lbc": cls._to_int(it.get("lbc")),
                "lbt": str(it.get("lbt") or ""),
                "zj": round_price(cls._to_float(it.get("zj"))),
                "fba": round_price(cls._to_float(it.get("fba"))),
                "zbc": cls._to_int(it.get("zbc")),
            })
        return items
    
    @classmethod
    def get_break_pool(cls, date: str, api_key: str) -> List[Dict[str, Any]]:
        """
        获取炸板股池数据
        
        Args:
            date: 查询日期，格式为 YYYY-MM-DD
            api_key: API密钥
            
        Returns:
            List[Dict[str, Any]]: 炸板股池数据列表
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        base = os.environ.get("THIRD_PARTY_ZBGC_BASE_URL") or "http://api.biyingapi.com/hslt/zbgc"
        endpoint = f"{date}/{api_key}"
        
        data = cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
        if not isinstance(data, list):
            raise ValueError("炸板股池返回格式错误")
        
        items: List[Dict[str, Any]] = []
        for it in data:
            items.append({
                "dm": str(it.get("dm") or ""),
                "mc": str(it.get("mc") or ""),
                "p": round_price(cls._to_float(it.get("p"))),
                "ztp": round_price(cls._to_float(it.get("ztp"))),
                "zf": round_price(cls._to_float(it.get("zf"))),
                "cje": round_price(cls._to_float(it.get("cje"))),
                "lt": round_price(cls._to_float(it.get("lt"))),
                "zsz": round_price(cls._to_float(it.get("zsz"))),
                "zs": round_price(cls._to_float(it.get("zs"))),
                "hs": round_price(cls._to_float(it.get("hs"))),
                "tj": str(it.get("tj") or ""),
                "fbt": str(it.get("fbt") or ""),
                "zbc": cls._to_int(it.get("zbc")),
            })
        return items
    
    @classmethod
    def get_strong_pool(cls, date: str, api_key: str) -> List[Dict[str, Any]]:
        """
        获取强势股池数据
        
        Args:
            date: 查询日期，格式为 YYYY-MM-DD
            api_key: API密钥
            
        Returns:
            List[Dict[str, Any]]: 强势股池数据列表
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        base = os.environ.get("THIRD_PARTY_QSGC_BASE_URL") or "https://api.biyingapi.com/hslt/qsgc"
        endpoint = f"{date}/{api_key}"
        
        try:
            data = cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
        except Exception:
            # 如果HTTPS请求失败，尝试HTTP
            if base.startswith("https://"):
                alt_base = "http://" + base[len("https://"):]
                data = cls.handle_api_request(alt_base, endpoint, referer="https://api.biyingapi.com/")
            else:
                raise
        
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
                "p": round_price(cls._to_float(it.get("p"))),
                "ztp": round_price(cls._to_float(it.get("ztp"))),
                "zf": round_price(cls._to_float(it.get("zf"))),
                "cje": round_price(cls._to_float(it.get("cje"))),
                "lt": round_price(cls._to_float(it.get("lt"))),
                "zsz": round_price(cls._to_float(it.get("zsz"))),
                "zs": round_price(cls._to_float(it.get("zs"))),
                "nh": cls._to_int(it.get("nh")),
                "lb": round_price(cls._to_float(it.get("lb"))),
                "hs": round_price(cls._to_float(it.get("hs"))),
                "tj": str(it.get("tj") or ""),
            })
        return items
    
    # 实时交易数据接口
    @classmethod
    def _map_public_item(cls, it: Dict[str, Any]) -> Dict[str, Any]:
        """
        映射公开源实时交易数据
        """
        return {
            "fm": round_price(cls._to_float(it.get("fm"))),
            "h": round_price(cls._to_float(it.get("h"))),
            "hs": round_price(cls._to_float(it.get("hs"))),
            "lb": round_price(cls._to_float(it.get("lb"))),
            "l": round_price(cls._to_float(it.get("l"))),
            "lt": round_price(cls._to_float(it.get("lt"))),
            "o": round_price(cls._to_float(it.get("o"))),
            "pe": round_price(cls._to_float(it.get("pe"))),
            "pc": round_price(cls._to_float(it.get("pc"))),
            "p": round_price(cls._to_float(it.get("p"))),
            "sz": round_price(cls._to_float(it.get("sz"))),
            "cje": round_price(cls._to_float(it.get("cje"))),
            "ud": round_price(cls._to_float(it.get("ud"))),
            "v": round_price(cls._to_float(it.get("v"))),
            "yc": round_price(cls._to_float(it.get("yc"))),
            "zf": round_price(cls._to_float(it.get("zf"))),
            "zs": round_price(cls._to_float(it.get("zs"))),
            "sjl": round_price(cls._to_float(it.get("sjl"))),
            "zdf60": round_price(cls._to_float(it.get("zdf60"))),
            "zdfnc": round_price(cls._to_float(it.get("zdfnc"))),
            "t": str(it.get("t") or ""),
        }
    
    @classmethod
    def get_realtime_public(cls, symbol: str, api_key: str) -> List[Dict[str, Any]]:
        """
        获取公开源实时交易数据
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            List[Dict[str, Any]]: 实时交易数据列表
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        code = normalize_symbol(symbol)[2:]
        base = os.environ.get("THIRD_PARTY_SSJY_BASE_URL") or "http://api.biyingapi.com/hsrl/ssjy"
        endpoint = f"{code}/{api_key}"
        
        data = cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
        
        if not isinstance(data, list):
            if isinstance(data, dict):
                for k in ("data", "list", "items", "result"):
                    v = data.get(k)
                    if isinstance(v, list):
                        data = v
                        break
                else:
                    # 兼容单条记录返回为对象的情况
                    return [cls._map_public_item(data)]
            else:
                raise ValueError("实时交易(公开)返回格式错误")
        
        return [cls._map_public_item(it) for it in data]
    
    @classmethod
    def _map_broker_item(cls, it: Dict[str, Any]) -> Dict[str, Any]:
        """
        映射券商源实时交易数据
        """
        return {
            "p": round_price(cls._to_float(it.get("p"))),
            "o": round_price(cls._to_float(it.get("o"))),
            "h": round_price(cls._to_float(it.get("h"))),
            "l": round_price(cls._to_float(it.get("l"))),
            "yc": round_price(cls._to_float(it.get("yc"))),
            "cje": round_price(cls._to_float(it.get("cje"))),
            "v": round_price(cls._to_float(it.get("v"))),
            "pv": round_price(cls._to_float(it.get("pv"))),
            "t": str(it.get("t") or ""),
            "ud": round_price(cls._to_float(it.get("ud"))),
            "pc": round_price(cls._to_float(it.get("pc"))),
            "zf": round_price(cls._to_float(it.get("zf"))),
            "pe": round_price(cls._to_float(it.get("pe"))),
            "tr": round_price(cls._to_float(it.get("tr"))),
            "pb_ratio": round_price(cls._to_float(it.get("pb_ratio"))),
            "tv": round_price(cls._to_float(it.get("tv"))),
        }
    
    @classmethod
    def get_realtime_broker(cls, symbol: str, api_key: str) -> List[Dict[str, Any]]:
        """
        获取券商源实时交易数据
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            List[Dict[str, Any]]: 实时交易数据列表
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        code = normalize_symbol(symbol)[2:]
        base = os.environ.get("THIRD_PARTY_REALTIME_BASE_URL") or "https://api.biyingapi.com/hsstock/real/time"
        endpoint = f"{code}/{api_key}"
        
        data = cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
        
        if isinstance(data, list):
            return [cls._map_broker_item(it) for it in data]
        if isinstance(data, dict):
            for k in ("data", "list", "items", "result"):
                v = data.get(k)
                if isinstance(v, list):
                    return [cls._map_broker_item(it) for it in v]
            return [cls._map_broker_item(data)]
        
        raise ValueError("实时交易(券商)返回格式错误")
    
    @classmethod
    def get_realtime_public_batch(cls, symbols: List[str], api_key: str) -> List[Dict[str, Any]]:
        """
        获取公开源批量实时交易数据
        
        Args:
            symbols: 股票代码列表
            api_key: API密钥
            
        Returns:
            List[Dict[str, Any]]: 批量实时交易数据列表
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        codes: List[str] = [normalize_symbol(s)[2:] for s in symbols]
        base = os.environ.get("THIRD_PARTY_SSJY_MORE_BASE_URL") or "http://api.biyingapi.com/hsrl/ssjy_more"
        endpoint = f"{api_key}"
        params = {"stock_codes": ",".join(codes)}
        
        data = cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/", params=params)
        
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
