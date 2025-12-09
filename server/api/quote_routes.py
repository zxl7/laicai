from typing import Optional
from fastapi import APIRouter, Query
from models.schemas import QuoteResponse, ErrorResponse
from services.api_service import handle_api_request
from services.quote_service import get_quote

# 创建行情相关路由
router = APIRouter(
    prefix="",
    tags=["行情接口"]
)

@router.get(
    "/quote",
    summary="股票行情查询",
    description="查询指定股票的最新行情信息，包括最新价格、涨跌幅、开高低收等数据",
    response_model=QuoteResponse,
    responses={400: {"model": ErrorResponse}},
)
def quote(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    """
    股票行情查询接口
    
    Args:
        symbol: 股票代码，支持多种格式（如 600000、sh600000、000547.SZ 等）
        
    Returns:
        QuoteResponse: 包含股票行情信息的响应对象
    """
    return handle_api_request(get_quote, QuoteResponse, symbol)
