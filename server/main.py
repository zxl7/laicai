from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入路由入口
from api import main_router

# 创建FastAPI应用
app = FastAPI(
    title="股票数据服务",
    description="提供股票行情、涨跌停、实时交易等数据接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(main_router)
