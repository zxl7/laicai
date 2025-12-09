import asyncio
from typing import Optional, List
from fastapi import APIRouter, Query, WebSocket, Header
from models.schemas import (
    RealTimePublicItem, RealTimeBrokerItem, RealTimePublicBatchItem, ErrorResponse
)
from services.api_service import handle_api_request, handle_ws_quote
from services.third_party_api import ThirdPartyAPI

# 使用统一的第三方API服务
get_realtime_public = ThirdPartyAPI.get_realtime_public
get_realtime_broker = ThirdPartyAPI.get_realtime_broker
get_realtime_public_batch = ThirdPartyAPI.get_realtime_public_batch

# 创建实时数据相关路由
router = APIRouter(
    prefix="",
    tags=["实时数据接口"]
)

@router.get(
    "/hsrl/ssjy",
    summary="实时交易数据查询",
    description="查询实时交易数据",
    response_model=List[RealTimePublicItem],
    responses={400: {"model": ErrorResponse}},
)
def realtime_public(symbol: str = Query(..., description="股票代码")):
    """
    实时交易数据查询接口
    
    Args:
        symbol: 股票代码
        
    Returns:
        List[RealTimePublicItem]: 实时交易数据列表
    """
    return handle_api_request(get_realtime_public, List[RealTimePublicItem], symbol)

@router.get(
    "/hsstock/real/time",
    summary="股票实时数据查询",
    description="查询股票的实时交易数据",
    response_model=List[RealTimeBrokerItem],
    responses={400: {"model": ErrorResponse}},
)
def realtime_broker(symbol: str = Query(..., description="股票代码")):
    """
    股票实时数据查询接口
    
    Args:
        symbol: 股票代码
        
    Returns:
        List[RealTimeBrokerItem]: 实时交易数据列表
    """
    return handle_api_request(get_realtime_broker, List[RealTimeBrokerItem], symbol)

@router.get(
    "/hsrl/ssjy_more",
    summary="更多实时交易数据查询",
    description="查询更多的实时交易数据",
    response_model=List[RealTimePublicBatchItem],
    responses={400: {"model": ErrorResponse}},
)
def realtime_public_batch(symbol: str = Query(..., description="股票代码")):
    """
    更多实时交易数据查询接口
    
    Args:
        symbol: 股票代码
        
    Returns:
        List[RealTimePublicBatchItem]: 更多实时交易数据列表
    """
    return handle_api_request(get_realtime_public_batch, List[RealTimePublicBatchItem], symbol)

@router.websocket("/ws/quote")
async def quote_ws(websocket: WebSocket):
    """
    WebSocket行情推送接口
    
    Args:
        websocket: WebSocket连接对象
    """
    await handle_ws_quote(websocket)
