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


class CompanyProfile(BaseModel):
    """
    上市公司简介数据模型
    """
    name: str = Field(..., description="公司名称")
    ename: Optional[str] = Field(None, description="公司英文名称")
    market: Optional[str] = Field(None, description="上市市场")
    idea: Optional[str] = Field(None, description="概念及板块，多个概念由英文逗号分隔")
    ldate: Optional[str] = Field(None, description="上市日期，格式yyyy-MM-dd")
    sprice: Optional[str] = Field(None, description="发行价格（元）")
    principal: Optional[str] = Field(None, description="主承销商")
    rdate: Optional[str] = Field(None, description="成立日期")
    rprice: Optional[str] = Field(None, description="注册资本")
    instype: Optional[str] = Field(None, description="机构类型")
    organ: Optional[str] = Field(None, description="组织形式")
    secre: Optional[str] = Field(None, description="董事会秘书")
    phone: Optional[str] = Field(None, description="公司电话")
    sphone: Optional[str] = Field(None, description="董秘电话")
    fax: Optional[str] = Field(None, description="公司传真")
    sfax: Optional[str] = Field(None, description="董秘传真")
    email: Optional[str] = Field(None, description="公司电子邮箱")
    semail: Optional[str] = Field(None, description="董秘电子邮箱")
    site: Optional[str] = Field(None, description="公司网站")
    post: Optional[str] = Field(None, description="邮政编码")
    infosite: Optional[str] = Field(None, description="信息披露网址")
    oname: Optional[str] = Field(None, description="证券简称更名历史")
    addr: Optional[str] = Field(None, description="注册地址")
    oaddr: Optional[str] = Field(None, description="办公地址")
    desc: Optional[str] = Field(None, description="公司简介")
    bscope: Optional[str] = Field(None, description="经营范围")
    printype: Optional[str] = Field(None, description="承销方式")
    referrer: Optional[str] = Field(None, description="上市推荐人")
    putype: Optional[str] = Field(None, description="发行方式")
    pe: Optional[str] = Field(None, description="发行市盈率（按发行后总股本）")
    firgu: Optional[str] = Field(None, description="首发前总股本（万股）")
    lastgu: Optional[str] = Field(None, description="首发后总股本（万股）")
    realgu: Optional[str] = Field(None, description="实际发行量（万股）")
    planm: Optional[str] = Field(None, description="预计募集资金（万元）")
    realm: Optional[str] = Field(None, description="实际募集资金合计（万元）")
    pubfee: Optional[str] = Field(None, description="发行费用总额（万元）")
    collect: Optional[str] = Field(None, description="募集资金净额（万元）")
    signfee: Optional[str] = Field(None, description="承销费用（万元）")
    pdate: Optional[str] = Field(None, description="招股公告日")


class ErrorResponse(BaseModel):
    """
    错误响应数据模型
    """
    code: str = Field(..., description="错误代码")
    message: str = Field(..., description="错误消息")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详情")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间戳")
