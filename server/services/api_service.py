"""API服务层，封装接口调用的公共逻辑"""
from typing import List, Dict, Any, Optional, Type, TypeVar, Callable
from fastapi import Query, Header
from fastapi.responses import JSONResponse

import os
from models.schemas import ErrorResponse
from services.third_party_api import ThirdPartyAPI
from akshareData.provider import (
    get_quote_by_akshare,
    get_board_concept_info_ths,
    get_board_concept_list_ths,
    get_stock_market_activity_legu,
    get_stock_individual_basic_info_xq,
    get_stock_zh_a_spot_em,
)

# 保持向后兼容的函数别名
get_quote = ThirdPartyAPI.get_stock_quote  # 兼容原get_quote函数
get_limit_status = ThirdPartyAPI.get_limit_status
get_limit_up_pool = ThirdPartyAPI.get_limit_up_pool
get_limit_down_pool = ThirdPartyAPI.get_limit_down_pool
get_break_pool = ThirdPartyAPI.get_break_pool
get_strong_pool = ThirdPartyAPI.get_strong_pool
get_realtime_public = ThirdPartyAPI.get_realtime_public
get_realtime_broker = ThirdPartyAPI.get_realtime_broker
get_realtime_public_batch = ThirdPartyAPI.get_realtime_public_batch
handle_api_request = ThirdPartyAPI.handle_api_request

# 类型变量，用于响应模型的泛型支持
T = TypeVar('T')


def handle_akshare_request(
    func: Callable,
    *args,
    **kwargs
) -> List[Dict[str, Any]] | Dict[str, Any] | JSONResponse:
    """
    处理Akshare API请求的通用函数，封装错误处理
    
    Args:
        func: 要调用的业务逻辑函数
        *args: 传递给业务逻辑函数的位置参数
        **kwargs: 传递给业务逻辑函数的关键字参数
        
    Returns:
        响应数据或错误响应
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


def handle_ws_quote(symbol: str) -> Dict[str, Any]:
    """
    处理WebSocket行情请求的函数
    
    Args:
        symbol: 股票代码
        
    Returns:
        行情数据
    """
    return get_quote(symbol)
