import asyncio
from typing import Optional, List

from fastapi import FastAPI, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .data_provider import get_quote, get_limit_status, get_limit_up_pool
from .models import QuoteResponse, LimitStatusResponse, ErrorResponse, LimitUpItem


app = FastAPI(title="Laicai Stock Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict)
def root():
    return {"service": "laicai-stock", "endpoints": ["/quote", "/limit-status", "/limit-up-pool", "/ws/quote"]}


@app.get("/quote", response_model=QuoteResponse, responses={400: {"model": ErrorResponse}})
def quote(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    try:
        data = get_quote(symbol)
        return QuoteResponse(**data)
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


@app.get("/limit-status", response_model=LimitStatusResponse, responses={400: {"model": ErrorResponse}})
def limit_status(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    try:
        data = get_limit_status(symbol)
        return LimitStatusResponse(**data)
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


@app.get("/limit-up-pool", response_model=List[LimitUpItem], responses={400: {"model": ErrorResponse}}, summary="涨停股池", description="根据日期返回当天涨停股池，默认当天", tags=["pool"])
def limit_up_pool(date: Optional[str] = Query(None, description="日期，格式yyyy-MM-dd；默认当天")):
    try:
        items = get_limit_up_pool(date)
        return [LimitUpItem(**x) for x in items]
    except Exception as e:
        return JSONResponse(status_code=400, content=ErrorResponse(error=str(e)).dict())


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
