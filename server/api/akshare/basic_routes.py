from typing import Dict, Any
from fastapi import APIRouter, Query
from models.schemas import ErrorResponse
from services.api_service import handle_akshare_request

# 创建Akshare基本信息相关路由
router = APIRouter(
    prefix="",
    tags=["Akshare基本信息接口"]
)

@router.get(
    "/stock/basic/info",
    summary="个股基本信息查询",
    description="通过Akshare数据源查询指定股票的基本信息",
    response_model=Dict[str, Any],
    responses={400: {"model": ErrorResponse}}
)
def akshare_stock_basic_info(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    """
    Akshare 个股基本信息查询接口
    
    Args:
        symbol: 股票代码，如 600000 或 sz000001
        
    Returns:
        Dict[str, Any]: 包含个股基本信息的数据字典
    """
    from akshareData.provider import get_stock_individual_basic_info_xq
    return handle_akshare_request(get_stock_individual_basic_info_xq, symbol)
