from typing import Optional
from fastapi import APIRouter, Query
from models.schemas import (
    LimitUpItem, LimitDownItem, BreakPoolItem, StrongPoolItem, ErrorResponse
)
from services.api_service import handle_api_request
from services.third_party_api import ThirdPartyAPI

# 使用统一的第三方API服务
get_limit_up_pool = ThirdPartyAPI.get_limit_up_pool
get_limit_down_pool = ThirdPartyAPI.get_limit_down_pool
get_break_pool = ThirdPartyAPI.get_break_pool
get_strong_pool = ThirdPartyAPI.get_strong_pool

# 创建股票池相关路由
router = APIRouter(
    prefix="",
    tags=["股票池接口"]
)

@router.get(
    "/hslt/ztgc",
    summary="涨停股池查询",
    description="查询当前涨停的股票列表",
    response_model=list[LimitUpItem],
    responses={400: {"model": ErrorResponse}},
)
def limit_up_pool(page: Optional[int] = Query(None, description="页码"), limit: Optional[int] = Query(None, description="每页数量")):
    """
    涨停股池查询接口
    
    Args:
        page: 页码（可选）
        limit: 每页数量（可选）
        
    Returns:
        List[LimitUpItem]: 涨停股票列表
    """
    return handle_api_request(get_limit_up_pool, list[LimitUpItem], page, limit)

@router.get(
    "/hslt/dtgc",
    summary="跌停股池查询",
    description="查询当前跌停的股票列表",
    response_model=list[LimitDownItem],
    responses={400: {"model": ErrorResponse}},
)
def limit_down_pool(page: Optional[int] = Query(None, description="页码"), limit: Optional[int] = Query(None, description="每页数量")):
    """
    跌停股池查询接口
    
    Args:
        page: 页码（可选）
        limit: 每页数量（可选）
        
    Returns:
        List[LimitDownItem]: 跌停股票列表
    """
    return handle_api_request(get_limit_down_pool, list[LimitDownItem], page, limit)

@router.get(
    "/hslt/zbgc",
    summary="炸板股池查询",
    description="查询当前炸板的股票列表",
    response_model=list[BreakPoolItem],
    responses={400: {"model": ErrorResponse}},
)
def break_pool(page: Optional[int] = Query(None, description="页码"), limit: Optional[int] = Query(None, description="每页数量")):
    """
    炸板股池查询接口
    
    Args:
        page: 页码（可选）
        limit: 每页数量（可选）
        
    Returns:
        List[BreakPoolItem]: 炸板股票列表
    """
    return handle_api_request(get_break_pool, list[BreakPoolItem], page, limit)

@router.get(
    "/hslt/qsgc",
    summary="强势股池查询",
    description="查询当前强势的股票列表",
    response_model=list[StrongPoolItem],
    responses={400: {"model": ErrorResponse}},
)
def strong_pool(page: Optional[int] = Query(None, description="页码"), limit: Optional[int] = Query(None, description="每页数量")):
    """
    强势股池查询接口
    
    Args:
        page: 页码（可选）
        limit: 每页数量（可选）
        
    Returns:
        List[StrongPoolItem]: 强势股票列表
    """
    return handle_api_request(get_strong_pool, list[StrongPoolItem], page, limit)
