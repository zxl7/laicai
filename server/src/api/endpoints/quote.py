"""
股票行情全部股票
"""

from fastapi import APIRouter
from services.quote import QuoteService
from schemas.quote import StockPool, APIResponse

router = APIRouter()
quote_service = QuoteService()


@router.get("/stock-pool", response_model=APIResponse)
def get_stock_pool():
    """
    获取股票池数据
    """
    data = quote_service.get_stock_pool()
    return APIResponse(code=200, message="获取股票池数据成功", data=data)