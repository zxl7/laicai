from typing import Optional, Dict, Any
from fastapi import APIRouter, Query
from models.schemas import QuoteResponse, ErrorResponse
from services.api_service import handle_akshare_request

# 创建Akshare行情相关路由
router = APIRouter(
    prefix="",
    tags=["Akshare行情接口"]
)

@router.get(
    "/quote",
    summary="Akshare股票行情查询",
    description="通过Akshare数据源查询指定股票的最新行情信息",
    response_model=QuoteResponse,
    responses={400: {"model": ErrorResponse}}
)
def akshare_quote(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001"), fallback: Optional[bool] = Query(False, description="为true时强制使用备用数据源")):
    """
    Akshare 股票行情查询接口
    
    Args:
        symbol: 股票代码，如 600000 或 sz000001
        fallback: 是否强制使用备用数据源，默认为 False
        
    Returns:
        QuoteResponse: 包含股票行情信息的响应对象
    """
    def _get_quote(symbol: str, fallback: bool) -> Dict[str, Any]:
        if fallback:
            from services.quote_service import get_quote
            return get_quote(symbol)
        else:
            from akshareData.provider import get_quote_by_akshare
            return get_quote_by_akshare(symbol)
    
    return handle_akshare_request(_get_quote, symbol, fallback)
