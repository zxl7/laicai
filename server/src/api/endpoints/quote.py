"""
股票行情API
"""

from fastapi import APIRouter
from services.quote import QuoteService
from schemas.quote import StockPool, APIResponse, CompanyProfile

router = APIRouter()
quote_service = QuoteService()


@router.get("/stock-pool", response_model=APIResponse)
def get_stock_pool():
    """
    获取股票池数据
    """
    data = quote_service.get_stock_pool()
    return APIResponse(code=200, message="获取股票池数据成功", data=data)


@router.get("/company-profile/{stock_code}", response_model=APIResponse)
def get_company_profile(stock_code: str):
    """
    根据股票代码获取上市公司简介数据
    
    Args:
        stock_code: 股票代码（如000001）
        
    Returns:
        APIResponse: 包含上市公司简介数据的响应
    """
    data = quote_service.get_company_profile(stock_code)
    return APIResponse(code=200, message="获取上市公司简介数据成功", data=data)