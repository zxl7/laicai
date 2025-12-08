import asyncio
from typing import Optional, List

from fastapi import APIRouter, Query, WebSocket, Header
from fastapi.responses import JSONResponse

from models.schemas import (
    QuoteResponse,
    LimitStatusResponse,
    LimitUpItem,
    RealTimePublicItem,
    RealTimeBrokerItem,
    RealTimePublicBatchItem,
    LimitDownItem,
    BreakPoolItem,
    StrongPoolItem,
    ErrorResponse,
)
from services.api_service import handle_api_request, handle_ws_quote


# 路由容器：统一注册所有 HTTP 和 WebSocket 接口，供 main.py 挂载
router = APIRouter()


# 根路径：返回服务名称与端点列表，便于前端发现可用接口
@router.get("/", response_model=dict)
def root():
    """
    根路径接口，返回服务信息和可用端点列表
    
    Returns:
        dict: 包含服务名称和端点列表的字典
            - service: 服务名称，固定为 "laicai-stock"
            - endpoints: 可用接口端点列表
    """
    return {"service": "laicai-stock", "endpoints": [
        "/quote",
        "/hsstock/instrument",
        "/hslt/ztgc",
        "/hslt/dtgc",
        "/hslt/zbgc",
        "/hslt/qsgc",
        "/hsrl/ssjy",
        "/hsstock/real/time",
        "/hsrl/ssjy_more",
        "/ws/quote",
    ]}


# 行情查询：入参 symbol（支持 600000 / sh600000 / 000547.SZ 等）
# 返回最新价格、涨跌幅、开高低收、时间等基础行情
@router.get(
    "/quote",
    response_model=QuoteResponse,
    responses={400: {"model": ErrorResponse}},
)
def quote(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    """
    股票行情查询接口
    
    Args:
        symbol: 股票代码，支持多种格式（如 600000、sh600000、000547.SZ 等）
        
    Returns:
        QuoteResponse: 包含股票行情信息的响应对象
            - code: 股票代码
            - name: 股票名称
            - price: 当前价格
            - change_percent: 涨跌幅百分比
            - change_amount: 涨跌额
            - open: 开盘价
            - high: 最高价
            - low: 最低价
            - prev_close: 前收盘价
            - time: 行情时间
    
    Raises:
        HTTPException: 当请求失败或参数错误时，返回 400 状态码和错误信息
    """
    from services.quote_service import get_quote
    return handle_api_request(get_quote, QuoteResponse, symbol)


# 涨跌停状态：入参 symbol，优先 instrument 源；失败回退新浪计算
# 返回涨停价/跌停价与是否触及、涨跌停幅度
@router.get(
    "/hsstock/instrument/{instrument}",
    response_model=LimitStatusResponse,
    responses={400: {"model": ErrorResponse}},
)
def limit_status(instrument: str, api_key: Optional[str] = None, licence_header: Optional[str] = Header(None, alias="licence")):
    """
    股票涨跌停状态查询接口
    
    Args:
        instrument: 股票代码或工具标识符
        api_key: API 密钥（可选）
        licence_header: 授权头（可选），通过 HTTP Header 传递
        
    Returns:
        LimitStatusResponse: 包含涨跌停状态信息的响应对象
            - symbol: 股票代码
            - limit_up_price: 涨停价
            - limit_down_price: 跌停价
            - is_limit_up: 是否涨停
            - is_limit_down: 是否跌停
            - limit_up_rate: 涨停幅度
            - limit_down_rate: 跌停幅度
    
    Raises:
        HTTPException: 当请求失败或参数错误时，返回 400 状态码和错误信息
    """
    from services.limit_service import get_limit_status
    symbol = instrument
    return handle_api_request(get_limit_status, LimitStatusResponse, symbol, api_key)


# 涨停股池：入参 date（默认当天）；可传 licence（Query/Header）覆盖环境变量
# 返回按字段映射后的列表项，字段见 models.LimitUpItem
@router.get(
    "/hslt/ztgc/{date}/{api_key}",
    response_model=List[LimitUpItem],
    responses={400: {"model": ErrorResponse}},
)
def limit_up_pool(date: str, api_key: str):
    """
    涨停股池查询接口
    
    Args:
        date: 查询日期，格式为 YYYY-MM-DD
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[LimitUpItem]: 涨停股票列表
            每个元素包含涨停股票的详细信息，如股票代码、名称、涨停时间等
    
    Raises:
        HTTPException: 当请求失败或参数错误时，返回 400 状态码和错误信息
    """
    from services.pool_service import get_limit_up_pool
    return handle_api_request(get_limit_up_pool, LimitUpItem, date, api_key)


# 跌停股池：入参同上；字段见 models.LimitDownItem
@router.get(
    "/hslt/dtgc/{date}/{api_key}",
    response_model=List[LimitDownItem],
    responses={400: {"model": ErrorResponse}},
)
def limit_down_pool(date: str, api_key: str):
    """
    跌停股池查询接口
    
    Args:
        date: 查询日期，格式为 YYYY-MM-DD
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[LimitDownItem]: 跌停股票列表
            每个元素包含跌停股票的详细信息，如股票代码、名称、跌停时间等
    
    Raises:
        HTTPException: 当请求失败或参数错误时，返回 400 状态码和错误信息
    """
    from services.pool_service import get_limit_down_pool
    return handle_api_request(get_limit_down_pool, LimitDownItem, date, api_key)


# 炸板股池：入参同上；字段见 models.BreakPoolItem
@router.get(
    "/hslt/zbgc/{date}/{api_key}",
    response_model=List[BreakPoolItem],
    responses={400: {"model": ErrorResponse}},
)
def break_pool(date: str, api_key: str):
    """
    炸板股池查询接口
    
    Args:
        date: 查询日期，格式为 YYYY-MM-DD
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[BreakPoolItem]: 炸板股票列表
            每个元素包含炸板股票的详细信息，如股票代码、名称、炸板时间等
    
    Raises:
        HTTPException: 当请求失败或参数错误时，返回 400 状态码和错误信息
    """
    from services.pool_service import get_break_pool
    return handle_api_request(get_break_pool, BreakPoolItem, date, api_key)


# 强势股池：入参同上；字段见 models.StrongPoolItem
@router.get(
    "/hslt/qsgc/{date}/{api_key}",
    response_model=List[StrongPoolItem],
    responses={400: {"model": ErrorResponse}},
)
def strong_pool(date: str, api_key: str):
    """
    强势股池查询接口
    
    Args:
        date: 查询日期，格式为 YYYY-MM-DD
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[StrongPoolItem]: 强势股票列表
            每个元素包含强势股票的详细信息，如股票代码、名称、涨跌幅等
    
    Raises:
        HTTPException: 当请求失败或参数错误时，返回 400 状态码和错误信息
    """
    from services.pool_service import get_strong_pool
    return handle_api_request(get_strong_pool, StrongPoolItem, date, api_key)


# 实时交易（公开源）：入参 symbol；可传 licence 覆盖；返回公开源字段集合
@router.get(
    "/hsrl/ssjy/{code}/{api_key}",
    response_model=List[RealTimePublicItem],
    responses={400: {"model": ErrorResponse}},
)
def realtime_public(code: str, api_key: str):
    """
    公开源实时交易数据查询接口
    
    Args:
        code: 股票代码
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[RealTimePublicItem]: 实时交易数据列表
            每个元素包含公开源提供的实时交易信息，如最新价、成交量、成交额等
    
    Raises:
        HTTPException: 当请求失败或参数错误时，返回 400 状态码和错误信息
    """
    from services.realtime_service import get_realtime_public
    symbol = code
    return handle_api_request(get_realtime_public, RealTimePublicItem, symbol, api_key)


# 实时交易（券商源）：入参 symbol；可传 licence 覆盖；返回券商源字段集合
@router.get(
    "/hsstock/real/time/{code}/{api_key}",
    response_model=List[RealTimeBrokerItem],
    responses={400: {"model": ErrorResponse}},
)
def realtime_broker(code: str, api_key: str):
    """
    券商源实时交易数据查询接口
    
    Args:
        code: 股票代码
        api_key: API 密钥，用于访问第三方服务
        
    Returns:
        List[RealTimeBrokerItem]: 实时交易数据列表
            每个元素包含券商源提供的实时交易信息，如最新价、开盘价、最高价、最低价等
    
    Raises:
        HTTPException: 当请求失败或参数错误时，返回 400 状态码和错误信息
    """
    from services.realtime_service import get_realtime_broker
    symbol = code
    return handle_api_request(get_realtime_broker, RealTimeBrokerItem, symbol, api_key)


# 实时交易（公开-多股）：入参 symbols（逗号分隔 ≤20）；可传 licence 覆盖
@router.get(
    "/hsrl/ssjy_more/{api_key}",
    response_model=List[RealTimePublicBatchItem],
    responses={400: {"model": ErrorResponse}},
)
def realtime_public_batch(api_key: str, stock_codes: str = Query(..., description="逗号分隔的股票代码列表，如 000001,600000")):
    """
    公开源批量实时交易数据查询接口
    
    Args:
        api_key: API 密钥，用于访问第三方服务
        stock_codes: 逗号分隔的股票代码列表，如 "000001,600000"，最多支持 20 只股票
        
    Returns:
        List[RealTimePublicBatchItem]: 批量实时交易数据列表
            每个元素包含一只股票的实时交易信息，如股票代码、最新价、成交量等
    
    Raises:
        HTTPException: 当请求失败或参数错误时，返回 400 状态码和错误信息
    """
    from services.realtime_service import get_realtime_public_batch
    symbol_list = [s.strip() for s in stock_codes.split(",") if s.strip()]
    return handle_api_request(get_realtime_public_batch, RealTimePublicBatchItem, symbol_list, api_key)


# WebSocket 行情：query 参数 `symbol`；每秒推送一次行情 JSON
@router.websocket("/ws/quote")
async def quote_ws(websocket: WebSocket):
    """
    WebSocket 实时行情推送接口
    
    Args:
        websocket: WebSocket 连接对象
        
    Query Parameters:
        symbol: 股票代码，如 "600000" 或 "sz000001"
        
    Behavior:
        - 连接建立后，每秒推送一次指定股票的实时行情数据
        - 如果缺少 symbol 参数，返回错误信息并关闭连接
        - 连接异常时，返回错误信息并关闭连接
    """
    await websocket.accept()
    symbol: Optional[str] = websocket.query_params.get("symbol")
    if not symbol:
        await websocket.send_json({"error": "缺少symbol参数"})
        await websocket.close()
        return
    try:
        while True:
            data = handle_ws_quote(symbol)
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()
