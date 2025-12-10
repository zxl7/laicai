"""
项目配置文件
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """
    项目配置类
    """
    # 应用基本信息
    APP_TITLE: str = "laicai-stock"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "企业级股票数据服务项目"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    WORKERS: int = 1
    
    # API配置
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./laicai-stock.db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 第三方API配置
    AK_SHARE_TIMEOUT: int = 30
    AK_SHARE_RETRY: int = 3
    
    # 必应API配置
    BIYING_API_HOST: str = "http://api.biyingapi.com"
    BIYING_API_TOKEN: str = "60D084A7-FF4A-4B42-9E1C-45F0B719F33C"
    
    class Config:
        """
        配置类的配置
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置实例（单例模式）
    
    Returns:
        Settings: 配置实例
    """
    return Settings()


# 创建配置实例
settings = get_settings()