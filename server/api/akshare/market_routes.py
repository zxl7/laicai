from typing import List, Dict, Any
from fastapi import APIRouter
from models.schemas import ErrorResponse
from services.api_service import handle_akshare_request

# 创建Akshare市场相关路由
router = APIRouter(
    prefix="",
    tags=["Akshare市场数据接口"]
)

@router.get(
    "/market/activity/legu",
    summary="市场活跃度（乐股）查询",
    description="查询市场活跃度相关数据",
    response_model=List[Dict[str, Any]],
    responses={400: {"model": ErrorResponse}}
)
def akshare_market_activity_legu():
    """
    Akshare 市场活跃度（乐股）查询接口
    
    Returns:
        List[Dict[str, Any]]: 市场活跃度数据列表
    """
    from akshareData.provider import get_stock_market_activity_legu
    return handle_akshare_request(get_stock_market_activity_legu)

@router.get(
    "/stock/spot/all",
    summary="所有A股实时行情查询",
    description="通过Akshare数据源查询所有A股的实时行情数据",
    response_model=List[Dict[str, Any]],
    responses={400: {"model": ErrorResponse}}
)
def akshare_stock_spot_all():
    """
    Akshare 所有A股实时行情查询接口
    
    Returns:
        List[Dict[str, Any]]: 包含所有A股实时行情数据的列表
    """
    from akshareData.provider import get_stock_zh_a_spot_em
    return handle_akshare_request(get_stock_zh_a_spot_em)
