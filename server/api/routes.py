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


router = APIRouter()


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

