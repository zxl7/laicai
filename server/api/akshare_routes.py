from typing import Optional, List, Dict, Any

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from models.schemas import QuoteResponse, ErrorResponse
from services.api_service import handle_akshare_request


router = APIRouter()


@router.get("/akshare/api/quote", response_model=QuoteResponse, responses={400: {"model": ErrorResponse}})
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


@router.get("/akshare/api/board/concept/info", response_model=List[Dict[str, Any]], responses={400: {"model": ErrorResponse}})
def akshare_board_concept_info(concept: Optional[str] = Query(None, description="板块概念名称，如 AI概念"), code: Optional[str] = Query(None, description="板块概念代码，如 BKXXXX"), date: Optional[str] = Query(None, description="日期，格式YYYY-MM-DD，可选")):
    """
    Akshare 板块概念信息查询接口
    
    Args:
        concept: 板块概念名称，如 AI概念
        code: 板块概念代码，如 BKXXXX
        date: 日期，格式YYYY-MM-DD，可选
        
    Returns:
        List[Dict[str, Any]]: 板块概念信息列表
    """
    from akshareData.provider import get_board_concept_info_ths
    return handle_akshare_request(get_board_concept_info_ths, concept=concept, code=code, date=date)


@router.get("/akshare/api/board/concept/list", response_model=List[Dict[str, Any]], responses={400: {"model": ErrorResponse}})
def akshare_board_concept_list():
    """
    Akshare 板块概念列表查询接口
    
    Returns:
        List[Dict[str, Any]]: 板块概念列表
    """
    from akshareData.provider import get_board_concept_list_ths
    return handle_akshare_request(get_board_concept_list_ths)


@router.get("/akshare/api/market/activity/legu", response_model=List[Dict[str, Any]], responses={400: {"model": ErrorResponse}})
def akshare_market_activity_legu():
    """
    Akshare 市场活跃度（乐股）查询接口
    
    Returns:
        List[Dict[str, Any]]: 市场活跃度数据列表
    """
    from akshareData.provider import get_stock_market_activity_legu
    return handle_akshare_request(get_stock_market_activity_legu)
