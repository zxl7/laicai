from typing import Optional, List, Dict, Any

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from models.schemas import QuoteResponse, ErrorResponse
from akshareData.provider import get_quote_by_akshare, get_board_concept_info_ths, get_board_concept_list_ths


router = APIRouter()


@router.get("/akshare/api/quote", response_model=QuoteResponse, responses={400: {"model": ErrorResponse}})
def akshare_quote(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001"), fallback: Optional[bool] = Query(False, description="为true时强制使用备用数据源")):
    try:
        if fallback:
            from services.quote_service import get_quote
            data = get_quote(symbol)
        else:
            data = get_quote_by_akshare(symbol)
        return QuoteResponse(**data)
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


@router.get("/akshare/api/board/concept/info", response_model=List[Dict[str, Any]], responses={400: {"model": ErrorResponse}})
def akshare_board_concept_info(concept: Optional[str] = Query(None, description="板块概念名称，如 AI概念"), code: Optional[str] = Query(None, description="板块概念代码，如 BKXXXX"), date: Optional[str] = Query(None, description="日期，格式YYYY-MM-DD，可选")):
    try:
        data = get_board_concept_info_ths(concept=concept, code=code, date=date)
        return data
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


@router.get("/akshare/api/board/concept/list", response_model=List[Dict[str, Any]], responses={400: {"model": ErrorResponse}})
def akshare_board_concept_list():
    try:
        data = get_board_concept_list_ths()

        return data
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())
