"""
股票行情API端点
"""

from fastapi import APIRouter
from services.quote import QuoteService
from schemas.quote import StockPool, APIResponse

router = APIRouter()
quote_service = QuoteService()


@router.get("/strong", response_model=APIResponse)
def get_strong_stocks():
    """
    获取强势股票列表
    """
    data = quote_service.get_strong_stocks()
    return APIResponse(code=200, message="获取强势股票列表成功", data=data)


@router.get("/stock-pool", response_model=APIResponse)
def get_stock_pool():
    """
    获取股票池数据
    """
    data = quote_service.get_stock_pool()
    return APIResponse(code=200, message="获取股票池数据成功", data=data)