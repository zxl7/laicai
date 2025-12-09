from typing import Optional
from fastapi import APIRouter, Query, Header
from models.schemas import LimitStatusResponse, ErrorResponse
from services.api_service import handle_api_request
from services.limit_service import get_limit_status

# 创建涨跌停相关路由
router = APIRouter(
    prefix="",
    tags=["涨跌停接口"]
)

@router.get(
    "/hsstock/instrument/{instrument}",
    summary="股票涨跌停状态查询",
    description="查询指定股票的涨跌停状态，包括涨停价、跌停价、是否触及涨跌停等信息",
    response_model=LimitStatusResponse,
    responses={400: {"model": ErrorResponse}},
)
def limit_status(instrument: str, api_key: Optional[str] = Query(None, description="API密钥"), licence_header: Optional[str] = Header(None, alias="licence", description="许可证头")):
    """
    股票涨跌停状态查询接口
    
    Args:
        instrument: 股票代码（通常是归一化后的格式）
        api_key: API密钥（可选），用于访问第三方服务
        licence_header: 许可证头（可选），用于访问第三方服务
        
    Returns:
        LimitStatusResponse: 包含涨跌停状态信息的响应对象
    """
    # 优先使用api_key参数，如果没有则使用licence_header
    final_api_key = api_key or licence_header
    return handle_api_request(get_limit_status, LimitStatusResponse, instrument, final_api_key)
