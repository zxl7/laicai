from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query
from models.schemas import ErrorResponse
from services.api_service import handle_akshare_request

# 创建Akshare板块概念相关路由
router = APIRouter(
    prefix="",
    tags=["Akshare板块概念接口"]
)

@router.get(
    "/board/concept/info",
    summary="板块概念信息查询",
    description="查询指定板块概念的详细信息，包括板块内的股票列表及相关数据",
    response_model=List[Dict[str, Any]],
    responses={400: {"model": ErrorResponse}}
)
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

@router.get(
    "/board/concept/list",
    summary="板块概念列表查询",
    description="查询所有可用的板块概念列表",
    response_model=List[Dict[str, Any]],
    responses={400: {"model": ErrorResponse}}
)
def akshare_board_concept_list():
    """
    Akshare 板块概念列表查询接口
    
    Returns:
        List[Dict[str, Any]]: 板块概念列表
    """
    from akshareData.provider import get_board_concept_list_ths
    return handle_akshare_request(get_board_concept_list_ths)
