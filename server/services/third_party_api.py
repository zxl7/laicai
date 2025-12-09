import os
import time
from typing import Dict, Any, List, Optional

from core.utils import normalize_symbol
from core.http_client import get_json


class ThirdPartyAPI:
    """
    第三方接口服务统一封装类
    
    整合所有第三方API调用，提供统一的接口访问方式，并封装共用逻辑
    """
    
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
    
    # 新浪财经 - 行情数据接口
    @classmethod
    def hq_sinajs(cls, symbol: str) -> Any:
        """
        获取股票行情数据 (新浪财经)
        
        Args:
            symbol: 股票代码
            
        Returns:
            Any: 新浪财经返回的原始行情数据
        """
        code = symbol
        if not code.startswith(('sh', 'sz')):
            if code.startswith('6'):
                code = 'sh' + code
            else:
                code = 'sz' + code
        
        base = os.environ.get("SINA_FINANCE_BASE_URL") or "https://hq.sinajs.cn"
        endpoint = f"/list={code}"
        return cls.handle_api_request(base, endpoint)
    
    # 第三方接口 - 涨跌停信息
    @classmethod
    def hsstock_limit_up(cls, symbol: str, api_key: str) -> Any:
        """
        获取股票涨停信息
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            Any: 第三方接口返回的原始涨跌停信息
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        code = normalize_symbol(symbol)[2:]
        base = os.environ.get("THIRD_PARTY_LIMIT_UP_BASE_URL") or "https://api.biyingapi.com/hsstock/limit_up"
        endpoint = f"/{code}/{api_key}"
        
        return cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
    
    # 第三方接口 - 涨停股池
    @classmethod
    def hslt_ztgc(cls, date: str, api_key: str) -> Any:
        """
        获取涨停股池数据
        
        Args:
            date: 查询日期，格式为 YYYY-MM-DD
            api_key: API密钥
            
        Returns:
            Any: 第三方接口返回的原始涨停股池数据
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        base = os.environ.get("THIRD_PARTY_ZTGC_BASE_URL") or "https://api.biyingapi.com/hslt/ztgc"
        endpoint = f"{date}/{api_key}"
        
        return cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
    
    # 第三方接口 - 跌停股池
    @classmethod
    def hslt_dtgc(cls, date: str, api_key: str) -> Any:
        """
        获取跌停股池数据
        
        Args:
            date: 查询日期，格式为 YYYY-MM-DD
            api_key: API密钥
            
        Returns:
            Any: 第三方接口返回的原始跌停股池数据
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        base = os.environ.get("THIRD_PARTY_DTGC_BASE_URL") or "http://api.biyingapi.com/hslt/dtgc"
        endpoint = f"{date}/{api_key}"
        
        return cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
    
    # 第三方接口 - 炸板股池
    @classmethod
    def hslt_zbgc(cls, date: str, api_key: str) -> Any:
        """
        获取炸板股池数据
        
        Args:
            date: 查询日期，格式为 YYYY-MM-DD
            api_key: API密钥
            
        Returns:
            Any: 第三方接口返回的原始炸板股池数据
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        base = os.environ.get("THIRD_PARTY_ZBGC_BASE_URL") or "http://api.biyingapi.com/hslt/zbgc"
        endpoint = f"{date}/{api_key}"
        
        return cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
    
    # 第三方接口 - 强势股池
    @classmethod
    def hslt_qsgc(cls, date: str, api_key: str) -> Any:
        """
        获取强势股池数据
        
        Args:
            date: 查询日期，格式为 YYYY-MM-DD
            api_key: API密钥
            
        Returns:
            Any: 第三方接口返回的原始强势股池数据
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        base = os.environ.get("THIRD_PARTY_QSGC_BASE_URL") or "https://api.biyingapi.com/hslt/qsgc"
        endpoint = f"{date}/{api_key}"
        
        try:
            return cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
        except Exception:
            # 如果HTTPS请求失败，尝试HTTP
            if base.startswith("https://"):
                alt_base = "http://" + base[len("https://"):]
                return cls.handle_api_request(alt_base, endpoint, referer="https://api.biyingapi.com/")
            else:
                raise
    
    # 第三方接口 - 公开源实时交易数据
    @classmethod
    def hsrl_ssjy(cls, symbol: str, api_key: str) -> Any:
        """
        获取公开源实时交易数据
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            Any: 第三方接口返回的原始公开源实时交易数据
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        code = normalize_symbol(symbol)[2:]
        base = os.environ.get("THIRD_PARTY_SSJY_BASE_URL") or "http://api.biyingapi.com/hsrl/ssjy"
        endpoint = f"{code}/{api_key}"
        
        return cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
    
    # 第三方接口 - 券商源实时交易数据
    @classmethod
    def hsstock_real_time(cls, symbol: str, api_key: str) -> Any:
        """
        获取券商源实时交易数据
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            Any: 第三方接口返回的原始券商源实时交易数据
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        code = normalize_symbol(symbol)[2:]
        base = os.environ.get("THIRD_PARTY_REALTIME_BASE_URL") or "https://api.biyingapi.com/hsstock/real/time"
        endpoint = f"/{code}/{api_key}"
        
        return cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/")
    
    # 第三方接口 - 批量公开源实时交易数据
    @classmethod
    def hsrl_ssjy_more(cls, symbols: List[str], api_key: str) -> Any:
        """
        获取公开源批量实时交易数据
        
        Args:
            symbols: 股票代码列表
            api_key: API密钥
            
        Returns:
            Any: 第三方接口返回的原始批量实时交易数据
        """
        if not api_key:
            raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
        
        codes: List[str] = [normalize_symbol(s)[2:] for s in symbols]
        base = os.environ.get("THIRD_PARTY_SSJY_MORE_BASE_URL") or "http://api.biyingapi.com/hsrl/ssjy_more"
        endpoint = f"{api_key}"
        params = {"stock_codes": ",".join(codes)}
        
        return cls.handle_api_request(base, endpoint, referer="https://api.biyingapi.com/", params=params)
    
    # 兼容性方法 - 保持原有接口名称可用
    @classmethod
    def get_stock_quote(cls, symbol: str) -> Any:
        """
        获取股票行情数据 (兼容原有接口)
        
        Args:
            symbol: 股票代码
            
        Returns:
            Any: 行情数据
        """
        return cls.hq_sinajs(symbol)
    
    @classmethod
    def get_limit_up_info(cls, symbol: str, api_key: str) -> Any:
        """
        获取股票涨跌停信息 (兼容原有接口)
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            Any: 涨跌停信息
        """
        return cls.hsstock_limit_up(symbol, api_key)
    
    @classmethod
    def get_limit_status(cls, symbol: str, api_key: str) -> Any:
        """
        获取股票涨跌停状态 (兼容原有接口)
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            Any: 涨跌停状态
        """
        return cls.hsstock_limit_up(symbol, api_key)
    
    @classmethod
    def get_limit_up_pool(cls, date: str, api_key: str) -> Any:
        """
        获取涨停股池数据 (兼容原有接口)
        
        Args:
            date: 查询日期
            api_key: API密钥
            
        Returns:
            Any: 涨停股池数据
        """
        return cls.hslt_ztgc(date, api_key)
    
    @classmethod
    def get_limit_down_pool(cls, date: str, api_key: str) -> Any:
        """
        获取跌停股池数据 (兼容原有接口)
        
        Args:
            date: 查询日期
            api_key: API密钥
            
        Returns:
            Any: 跌停股池数据
        """
        return cls.hslt_dtgc(date, api_key)
    
    @classmethod
    def get_break_pool(cls, date: str, api_key: str) -> Any:
        """
        获取炸板股池数据 (兼容原有接口)
        
        Args:
            date: 查询日期
            api_key: API密钥
            
        Returns:
            Any: 炸板股池数据
        """
        return cls.hslt_zbgc(date, api_key)
    
    @classmethod
    def get_strong_pool(cls, date: str, api_key: str) -> Any:
        """
        获取强势股池数据 (兼容原有接口)
        
        Args:
            date: 查询日期
            api_key: API密钥
            
        Returns:
            Any: 强势股池数据
        """
        return cls.hslt_qsgc(date, api_key)
    
    @classmethod
    def get_realtime_public(cls, symbol: str, api_key: str) -> Any:
        """
        获取公开源实时交易数据 (兼容原有接口)
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            Any: 公开源实时交易数据
        """
        return cls.hsrl_ssjy(symbol, api_key)
    
    @classmethod
    def get_realtime_broker(cls, symbol: str, api_key: str) -> Any:
        """
        获取券商源实时交易数据 (兼容原有接口)
        
        Args:
            symbol: 股票代码
            api_key: API密钥
            
        Returns:
            Any: 券商源实时交易数据
        """
        return cls.hsstock_real_time(symbol, api_key)
    
    @classmethod
    def get_realtime_public_batch(cls, symbols: List[str], api_key: str) -> Any:
        """
        获取批量实时交易数据 (兼容原有接口)
        
        Args:
            symbols: 股票代码列表
            api_key: API密钥
            
        Returns:
            Any: 批量实时交易数据
        """
        return cls.hsrl_ssjy_more(symbols, api_key)
