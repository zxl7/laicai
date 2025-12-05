import asyncio
from typing import Optional, List

from fastapi import FastAPI, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .data_provider import get_quote, get_limit_status, get_limit_up_pool
from .models import QuoteResponse, LimitStatusResponse, ErrorResponse, LimitUpItem, RealTimePublicItem, RealTimeBrokerItem, RealTimePublicBatchItem, LimitDownItem, BreakPoolItem, StrongPoolItem
from .services.realtime_service import (
    get_realtime_public,
    get_realtime_broker,
    get_realtime_public_batch,
    get_limit_down_pool,
    get_break_pool,
    get_strong_pool,
)


app = FastAPI(title="Laicai Stock Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 根路径：返回服务名称与可用端点列表，便于前端查看有哪些接口
@app.get("/", response_model=dict)
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


# 行情查询：入参为股票代码，自动兼容 600000 / sh600000 / 000547.SZ 等格式
# 返回最新价格、涨跌幅、开高低收、时间等基础行情数据
@app.get(
    "/quote",
    response_model=QuoteResponse,
    responses={
        200: {
            "description": "基础行情数据",
            "content": {
                "application/json": {
                    "example": {
                        "code": "000547",
                        "name": "航天发展",
                        "price": 12.34,
                        "change_percent": 1.23,
                        "change_amount": 0.15,
                        "open": 12.10,
                        "high": 12.50,
                        "low": 12.00,
                        "prev_close": 12.19,
                        "time": "2025-12-05 14:02:00",
                    }
                }
            },
        },
        400: {"model": ErrorResponse},
    },
    summary="行情",
    tags=["quote"],
)
def quote(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    try:
        data = get_quote(symbol)
        return QuoteResponse(**data)
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 涨跌停状态：入参为股票代码，结合第三方/新浪行情计算涨停价、跌停价与是否触及
@app.get(
    "/limit-status",
    response_model=LimitStatusResponse,
    responses={
        200: {
            "description": "涨跌停状态",
            "content": {
                "application/json": {
                    "example": {
                        "code": "000547",
                        "name": "航天发展",
                        "price": 12.34,
                        "limit_up_price": 13.41,
                        "limit_down_price": 10.97,
                        "is_limit_up": False,
                        "is_limit_down": False,
                        "limit_rate": 0.10,
                    }
                }
            },
        },
        400: {"model": ErrorResponse},
    },
    summary="涨跌停状态",
    tags=["status"],
)
def limit_status(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    try:
        data = get_limit_status(symbol)
        return LimitStatusResponse(**data)
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 涨停股池：入参为日期(可选，默认当天)，数据源为 biyingapi，对应字段已在模型中定义
@app.get(
    "/limit-up-pool",
    response_model=List[LimitUpItem],
    responses={
        200: {
            "description": "涨停股池列表",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "code": "000547",
                            "name": "航天发展",
                            "price": 12.34,
                            "change_percent": 10.0,
                            "amount": 123456789.0,
                            "float_market_cap": 4567890000.0,
                            "total_market_cap": 7890000000.0,
                            "turnover_rate": 5.67,
                            "consecutive_boards": 2,
                            "first_board_time": "09:45:12",
                            "last_board_time": "13:22:31",
                            "seal_funds": 34500000.0,
                            "broken_boards": 1,
                            "stat": "3天/2板",
                        }
                    ]
                }
            },
        },
        400: {"model": ErrorResponse},
    },
    summary="涨停股池",
    description="根据日期返回当天涨停股池，默认当天",
    tags=["pool"],
)
def limit_up_pool(date: Optional[str] = Query(None, description="日期，格式yyyy-MM-dd；默认当天")):
    try:
        items = get_limit_up_pool(date)
        return [LimitUpItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 跌停股池：入参为日期(可选，默认当天)，数据源为 biyingapi，包含封单资金、连续跌停等信息
@app.get(
    "/limit-down-pool",
    response_model=List[LimitDownItem],
    responses={
        200: {
            "description": "跌停股池列表",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "dm": "000001",
                            "mc": "平安银行",
                            "p": 10.01,
                            "zf": -10.0,
                            "cje": 234567890.0,
                            "lt": 3456000000.0,
                            "zsz": 4567000000.0,
                            "pe": 15.2,
                            "hs": 3.21,
                            "lbc": 1,
                            "lbt": "10:45:12",
                            "zj": 12000000.0,
                            "fba": 8000000.0,
                            "zbc": 0
                        }
                    ]
                }
            },
        },
        400: {"model": ErrorResponse},
    },
    summary="跌停股池",
    description="根据日期返回当天跌停股池，默认当天",
    tags=["pool"],
)
def limit_down_pool(date: Optional[str] = Query(None, description="日期，格式yyyy-MM-dd；默认当天")):
    try:
        items = get_limit_down_pool(date)
        return [LimitDownItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 炸板股池：入参为日期(可选，默认当天)，包含涨停价、炸板次数、首次封板时间等
@app.get(
    "/break-pool",
    response_model=List[BreakPoolItem],
    responses={
        200: {
            "description": "炸板股池列表",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "dm": "000547",
                            "mc": "航天发展",
                            "p": 12.34,
                            "ztp": 13.41,
                            "zf": 8.65,
                            "cje": 156789000.0,
                            "lt": 4567890000.0,
                            "zsz": 7890000000.0,
                            "zs": 2.10,
                            "hs": 4.56,
                            "tj": "近3天/2板",
                            "fbt": "10:12:33",
                            "zbc": 1
                        }
                    ]
                }
            },
        },
        400: {"model": ErrorResponse},
    },
    summary="炸板股池",
    description="根据日期返回当天炸板股池，默认当天",
    tags=["pool"],
)
def break_pool(date: Optional[str] = Query(None, description="日期，格式yyyy-MM-dd；默认当天")):
    try:
        items = get_break_pool(date)
        return [BreakPoolItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 强势股池：入参为日期(可选，默认当天)，根据涨幅倒序，含是否新高、量比、换手等
@app.get(
    "/strong-pool",
    response_model=List[StrongPoolItem],
    responses={
        200: {
            "description": "强势股池列表",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "dm": "000547",
                            "mc": "航天发展",
                            "p": 12.34,
                            "ztp": 13.41,
                            "zf": 8.65,
                            "cje": 156789000.0,
                            "lt": 4567890000.0,
                            "zsz": 7890000000.0,
                            "zs": 2.10,
                            "nh": 1,
                            "lb": 1.23,
                            "hs": 4.56,
                            "tj": "近3天/2板"
                        }
                    ]
                }
            },
        },
        400: {"model": ErrorResponse},
    },
    summary="强势股池",
    description="根据日期返回当天强势股池，默认当天",
    tags=["pool"],
)
def strong_pool(date: Optional[str] = Query(None, description="日期，格式yyyy-MM-dd；默认当天")):
    try:
        items = get_strong_pool(date)
        return [StrongPoolItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 实时交易(公开)：入参为股票代码；调用 `hsrl/ssjy` 接口返回列表，每条含价、涨跌、量额、市值、更新时间等
# 需设置 `THIRD_PARTY_API_KEY` 作为 licence；交易时段约每1分钟更新
@app.get(
    "/realtime/public",
    response_model=List[RealTimePublicItem],
    responses={
        200: {
            "description": "公开源实时交易数据列表",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "fm": 0.52,
                            "h": 12.50,
                            "hs": 3.21,
                            "lb": 1.05,
                            "l": 12.00,
                            "lt": 4567890000.0,
                            "o": 12.10,
                            "pe": 18.3,
                            "pc": 1.23,
                            "p": 12.34,
                            "sz": 7890000000.0,
                            "cje": 156789000.0,
                            "ud": 0.15,
                            "v": 123456.0,
                            "yc": 12.19,
                            "zf": 4.02,
                            "zs": 2.10,
                            "sjl": 2.12,
                            "zdf60": 12.3,
                            "zdfnc": 35.6,
                            "t": "2025-12-05 14:02:00"
                        }
                    ]
                }
            },
        },
        400: {"model": ErrorResponse},
    },
    summary="实时交易(公开)",
    description="根据股票代码获取实时交易数据（公开数据源）",
    tags=["realtime"],
)
def realtime_public(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    try:
        items = get_realtime_public(symbol)
        return [RealTimePublicItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 实时交易(券商)：入参为股票代码；调用 `hsstock/real/time` 接口返回列表，数据为券商源，实时刷新频率更高
# 字段包含最新价、开高低、前收、量额、市盈率、换手、市净率等
@app.get(
    "/realtime/broker",
    response_model=List[RealTimeBrokerItem],
    responses={
        200: {
            "description": "券商源实时交易数据列表",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "p": 12.34,
                            "o": 12.10,
                            "h": 12.50,
                            "l": 12.00,
                            "yc": 12.19,
                            "cje": 156789000.0,
                            "v": 123456.0,
                            "pv": 123456.0,
                            "t": "2025-12-05 14:02:00",
                            "ud": 0.15,
                            "pc": 1.23,
                            "zf": 4.02,
                            "pe": 18.3,
                            "tr": 3.21,
                            "pb_ratio": 2.12,
                            "tv": 23456.0
                        }
                    ]
                }
            },
        },
        400: {"model": ErrorResponse},
    },
    summary="实时交易(券商)",
    description="根据股票代码获取实时交易数据（券商数据源）",
    tags=["realtime"],
)
def realtime_broker(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    try:
        items = get_realtime_broker(symbol)
        return [RealTimeBrokerItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# 实时交易(公开-多股)：入参为逗号分隔的代码列表(最多20)，返回对应股票的实时数据列表
# 字段与单股公开源基本一致，并包含 `dm` 表示股票代码
@app.get(
    "/realtime/public/batch",
    response_model=List[RealTimePublicBatchItem],
    responses={
        200: {
            "description": "公开源批量实时交易数据列表",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "dm": "000547",
                            "p": 12.34,
                            "o": 12.10,
                            "h": 12.50,
                            "l": 12.00,
                            "yc": 12.19,
                            "cje": 156789000.0,
                            "v": 123456.0,
                            "pv": 123456.0,
                            "t": "2025-12-05 14:02:00",
                            "ud": 0.15,
                            "pc": 1.23,
                            "zf": 4.02,
                            "pe": 18.3,
                            "tr": 3.21,
                            "pb_ratio": 2.12,
                            "tv": 23456.0
                        }
                    ]
                }
            },
        },
        400: {"model": ErrorResponse},
    },
    summary="实时交易(公开-多股)",
    description="一次性获取不超过20支股票的实时交易数据（公开数据源）",
    tags=["realtime"],
)
def realtime_public_batch(symbols: str = Query(..., description="逗号分隔的股票代码列表，如 000001,600000")):
    try:
        symbol_list = [s.strip() for s in symbols.split(",") if s.strip()]
        items = get_realtime_public_batch(symbol_list)
        return [RealTimePublicBatchItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


# WebSocket 行情：入参为 `?symbol=`；每秒推送一次 JSON 行情，便于前端做实时展示
@app.websocket("/ws/quote")
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
