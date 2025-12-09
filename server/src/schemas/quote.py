"""
股票行情数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class StockPool(BaseModel):
    """
    股票池数据模型
    """
    total: int = Field(..., description="股票总数")
    stocks: Dict[str, Any] = Field(..., description="股票池数据，以股票代码为键，存储原始数据")


class APIResponse(BaseModel):
    """
    API响应通用数据模型
    """
    code: int = Field(..., description="响应代码")
    message: str = Field(..., description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间戳")


class ErrorResponse(BaseModel):
    """
    错误响应数据模型
    """
    code: str = Field(..., description="错误代码")
    message: str = Field(..., description="错误消息")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详情")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间戳")
