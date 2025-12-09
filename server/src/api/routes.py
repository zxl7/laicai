"""
API路由定义
"""

from fastapi import APIRouter
from api.endpoints import quote

# 创建API路由
api_router = APIRouter()

# 注册股票行情相关路由
api_router.include_router(quote.router, prefix="/quote", tags=["股票行情"])

