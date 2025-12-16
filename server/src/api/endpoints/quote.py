"""
股票行情API
"""

from fastapi import APIRouter
from services.quote import QuoteService
from schemas.quote import StockPool, APIResponse, CompanyProfile, StrongStockPool, ZTStockPool, DTStockPool

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


@router.get("/strong-stock-pool/{date}", response_model=APIResponse)
def get_strong_stock_pool(date: str):
    """
    根据日期获取强势股票池数据
    
    Args:
        date: 日期（格式yyyy-MM-dd，如2020-01-15）
        
    Returns:
        APIResponse: 包含强势股池数据的响应
    """
    data = quote_service.get_strong_stock_pool(date)
    return APIResponse(code=200, message="获取强势股票池数据成功", data=data)


@router.get("/zt-stock-pool/{date}", response_model=APIResponse)
def get_zt_stock_pool(date: str):
    """
    根据日期获取涨停股票池数据
    
    Args:
        date: 日期（格式yyyy-MM-dd，如2020-01-15）
        
    Returns:
        APIResponse: 包含涨停股池数据的响应
    """
    data = quote_service.get_zt_stock_pool(date)
    return APIResponse(code=200, message="获取涨停股票池数据成功", data=data)


@router.get("/dt-stock-pool/{date}", response_model=APIResponse)
def get_dt_stock_pool(date: str):
    """
    根据日期获取跌停股票池数据
    
    Args:
        date: 日期（格式yyyy-MM-dd，如2020-01-15）
        
    Returns:
        APIResponse: 包含跌停股池数据的响应
    """
    data = quote_service.get_dt_stock_pool(date)
    return APIResponse(code=200, message="获取跌停股票池数据成功", data=data)