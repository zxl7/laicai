from fastapi import APIRouter
from api.routes import router as base_router
from api.quote_routes import router as quote_router
from api.limit_routes import router as limit_router
from api.pool_routes import router as pool_router
from api.realtime_routes import router as realtime_router
from api.akshare import router as akshare_router

# 创建主路由
main_router = APIRouter()

# 注册所有子路由
main_router.include_router(base_router)
main_router.include_router(quote_router)
main_router.include_router(limit_router)
main_router.include_router(pool_router)
main_router.include_router(realtime_router)
main_router.include_router(akshare_router)
