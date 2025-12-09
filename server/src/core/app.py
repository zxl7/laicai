"""
核心应用配置文件
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import settings
from core.exceptions import setup_exception_handlers
from api.routes import api_router


def create_app() -> FastAPI:
    """
    创建FastAPI应用实例
    
    Returns:
        FastAPI: 配置好的FastAPI应用实例
    """
    # 创建FastAPI应用
    app = FastAPI(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        openapi_url=settings.OPENAPI_URL,
    )
    
    # 配置CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    
    # 注册API路由
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    # 设置异常处理器
    setup_exception_handlers(app)
    
    return app