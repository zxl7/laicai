"""
股票行情数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class StockQuote(BaseModel):
    """
    股票实时行情数据模型
    """
    symbol: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌幅(%)")
    change_amount: float = Field(..., description="涨跌额")
    volume: float = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额")
    turnover: float = Field(..., description="换手率(%)")
    amplitude: float = Field(..., description="振幅(%)")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    open: float = Field(..., description="今开价")
    prev_close: float = Field(..., description="昨收价")
    market_cap: float = Field(..., description="总市值")
    circulating_cap: float = Field(..., description="流通市值")
    pe: Optional[float] = Field(None, description="市盈率")
    pb: Optional[float] = Field(None, description="市净率")


class LimitUpStock(BaseModel):
    """
    涨停股票数据模型
    """
    symbol: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌幅(%)")
    change_amount: float = Field(..., description="涨跌额")
    volume: float = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额")
    open_time: Optional[str] = Field(None, description="涨停时间")


class LimitUpStocks(BaseModel):
    """
    涨停股票列表数据模型
    """
    total: int = Field(..., description="涨停股票总数")
    stocks: List[LimitUpStock] = Field(..., description="涨停股票列表")


class LimitDownStock(BaseModel):
    """
    跌停股票数据模型
    """
    symbol: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌幅(%)")
    change_amount: float = Field(..., description="涨跌额")
    volume: float = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额")


class LimitDownStocks(BaseModel):
    """
    跌停股票列表数据模型
    """
    total: int = Field(..., description="跌停股票总数")
    stocks: List[LimitDownStock] = Field(..., description="跌停股票列表")


class FailedLimitUpStock(BaseModel):
    """
    炸板股票数据模型
    """
    symbol: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌幅(%)")
    change_amount: float = Field(..., description="涨跌额")
    volume: float = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额")
    high: float = Field(..., description="最高价")
    limit_up_time: Optional[int] = Field(None, description="开板次数")


class FailedLimitUpStocks(BaseModel):
    """
    炸板股票列表数据模型
    """
    total: int = Field(..., description="炸板股票总数")
    stocks: List[FailedLimitUpStock] = Field(..., description="炸板股票列表")


class StrongStock(BaseModel):
    """
    强势股票数据模型
    """
    symbol: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价")
    change: float = Field(..., description="涨跌幅(%)")
    change_amount: float = Field(..., description="涨跌额")
    volume: float = Field(..., description="成交量(手)")
    amount: float = Field(..., description="成交额")


class StrongStocks(BaseModel):
    """
    强势股票列表数据模型
    """
    total: int = Field(..., description="强势股票总数")
    stocks: List[StrongStock] = Field(..., description="强势股票列表")


class APIResponse(BaseModel):
    """
    API统一响应数据模型
    """
    code: str = Field(..., description="响应代码")
    message: str = Field(..., description="响应消息")
    data: Optional[Dict[str, Any]] = Field(None, description="响应数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间戳")


class ErrorResponse(BaseModel):
    """
    错误响应数据模型
    """
    code: str = Field(..., description="错误代码")
    message: str = Field(..., description="错误消息")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详情")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间戳")