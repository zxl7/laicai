from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from api.akshare_routes import router as ak_router


app = FastAPI(
    title="菜菜股票分析服务",
    description="提供股票行情查询、涨跌停状态查询、股池查询、实时交易数据查询等功能的股票分析服务API接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(ak_router)
