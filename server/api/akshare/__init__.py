from fastapi import APIRouter

# 创建Akshare主路由
router = APIRouter(
    prefix="/akshare/api",
    tags=["Akshare数据接口"]
)

# 导入并注册各个Akshare子路由
from api.akshare.quote_routes import router as quote_router
from api.akshare.concept_routes import router as concept_router
from api.akshare.market_routes import router as market_router
from api.akshare.basic_routes import router as basic_router

router.include_router(quote_router)
router.include_router(concept_router)
router.include_router(market_router)
router.include_router(basic_router)
