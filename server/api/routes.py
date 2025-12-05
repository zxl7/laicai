import asyncio
from typing import Optional, List

from fastapi import APIRouter, Query, WebSocket, Header
from fastapi.responses import JSONResponse

from models.schemas import (
    QuoteResponse,
    LimitStatusResponse,
    ErrorResponse,
    LimitUpItem,
    RealTimePublicItem,
    RealTimeBrokerItem,
    RealTimePublicBatchItem,
    LimitDownItem,
    BreakPoolItem,
    StrongPoolItem,
)
from services.quote_service import get_quote
from services.limit_service import get_limit_status
from services.pool_service import get_limit_up_pool, get_limit_down_pool, get_break_pool, get_strong_pool
from services.realtime_service import (
    get_realtime_public,
    get_realtime_broker,
    get_realtime_public_batch,
)


# 路由容器：统一注册所有 HTTP 和 WebSocket 接口，供 main.py 挂载
router = APIRouter()


# 根路径：返回服务名称与端点列表，便于前端发现可用接口
@router.get("/", response_model=dict)
def root():
    return {"service": "laicai-stock", "endpoints": [
        "/quote",
        "/limit-status",
        "/limit-up-pool",
        "/limit-down-pool",
        "/break-pool",
        "/strong-pool",
        "/realtime/public",
        "/realtime/broker",
        "/realtime/public/batch",
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
    try:
        data = get_quote(symbol)
        return QuoteResponse(**data)
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 涨跌停状态：入参 symbol，优先 instrument 源；失败回退新浪计算
# 返回涨停价/跌停价与是否触及、涨跌停幅度
@router.get(
    "/limit-status",
    response_model=LimitStatusResponse,
    responses={400: {"model": ErrorResponse}},
)
def limit_status(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    try:
        data = get_limit_status(symbol)
        return LimitStatusResponse(**data)
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 涨停股池：入参 date（默认当天）；可传 licence（Query/Header）覆盖环境变量
# 返回按字段映射后的列表项，字段见 models.LimitUpItem
@router.get(
    "/limit-up-pool",
    response_model=List[LimitUpItem],
    responses={400: {"model": ErrorResponse}},
)
def limit_up_pool(date: Optional[str] = Query(None, description="日期，格式yyyy-MM-dd；默认当天"), licence: Optional[str] = Query(None), licence_header: Optional[str] = Header(None, alias="licence")):
    try:
        items = get_limit_up_pool(date, api_key=licence or licence_header)
        return [LimitUpItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 跌停股池：入参同上；字段见 models.LimitDownItem
@router.get(
    "/limit-down-pool",
    response_model=List[LimitDownItem],
    responses={400: {"model": ErrorResponse}},
)
def limit_down_pool(date: Optional[str] = Query(None, description="日期，格式yyyy-MM-dd；默认当天"), licence: Optional[str] = Query(None), licence_header: Optional[str] = Header(None, alias="licence")):
    try:
        items = get_limit_down_pool(date, api_key=licence or licence_header)
        return [LimitDownItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 炸板股池：入参同上；字段见 models.BreakPoolItem
@router.get(
    "/break-pool",
    response_model=List[BreakPoolItem],
    responses={400: {"model": ErrorResponse}},
)
def break_pool(date: Optional[str] = Query(None, description="日期，格式yyyy-MM-dd；默认当天"), licence: Optional[str] = Query(None), licence_header: Optional[str] = Header(None, alias="licence")):
    try:
        items = get_break_pool(date, api_key=licence or licence_header)
        return [BreakPoolItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 强势股池：入参同上；字段见 models.StrongPoolItem
@router.get(
    "/strong-pool",
    response_model=List[StrongPoolItem],
    responses={400: {"model": ErrorResponse}},
)
def strong_pool(date: Optional[str] = Query(None, description="日期，格式yyyy-MM-dd；默认当天"), licence: Optional[str] = Query(None), licence_header: Optional[str] = Header(None, alias="licence")):
    try:
        items = get_strong_pool(date, api_key=licence or licence_header)
        return [StrongPoolItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 实时交易（公开源）：入参 symbol；可传 licence 覆盖；返回公开源字段集合
@router.get(
    "/realtime/public",
    response_model=List[RealTimePublicItem],
    responses={400: {"model": ErrorResponse}},
)
def realtime_public(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001"), licence: Optional[str] = Query(None), licence_header: Optional[str] = Header(None, alias="licence")):
    try:
        items = get_realtime_public(symbol, api_key=licence or licence_header)
        return [RealTimePublicItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 实时交易（券商源）：入参 symbol；可传 licence 覆盖；返回券商源字段集合
@router.get(
    "/realtime/broker",
    response_model=List[RealTimeBrokerItem],
    responses={400: {"model": ErrorResponse}},
)
def realtime_broker(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001"), licence: Optional[str] = Query(None), licence_header: Optional[str] = Header(None, alias="licence")):
    try:
        items = get_realtime_broker(symbol, api_key=licence or licence_header)
        return [RealTimeBrokerItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 实时交易（公开-多股）：入参 symbols（逗号分隔 ≤20）；可传 licence 覆盖
@router.get(
    "/realtime/public/batch",
    response_model=List[RealTimePublicBatchItem],
    responses={400: {"model": ErrorResponse}},
)
def realtime_public_batch(symbols: str = Query(..., description="逗号分隔的股票代码列表，如 000001,600000"), licence: Optional[str] = Query(None), licence_header: Optional[str] = Header(None, alias="licence")):
    try:
        symbol_list = [s.strip() for s in symbols.split(",") if s.strip()]
        items = get_realtime_public_batch(symbol_list, api_key=licence or licence_header)
        return [RealTimePublicBatchItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# WebSocket 行情：query 参数 `symbol`；每秒推送一次行情 JSON
@router.websocket("/ws/quote")
async def quote_ws(websocket: WebSocket):
    await websocket.accept()
    symbol: Optional[str] = websocket.query_params.get("symbol")
    if not symbol:
        await websocket.send_json({"error": "缺少symbol参数"})
        await websocket.close()
        return
    try:
        while True:
            data = get_quote(symbol)
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()
