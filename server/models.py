from pydantic import BaseModel, Field


class QuoteResponse(BaseModel):
    code: str = Field(..., description="股票代码，如 000001")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="最新价格（元）")
    change_percent: float = Field(..., description="涨跌幅（%）")
    change_amount: float = Field(..., description="涨跌额（元）")
    open: float = Field(..., description="开盘价（元）")
    high: float = Field(..., description="最高价（元）")
    low: float = Field(..., description="最低价（元）")
    prev_close: float = Field(..., description="昨日收盘价（元）")
    time: str = Field(..., description="数据时间 yyyy-MM-dd HH:mm:ss")


class LimitStatusResponse(BaseModel):
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="当前价格（元）")
    limit_up_price: float = Field(..., description="涨停价（元）")
    limit_down_price: float = Field(..., description="跌停价（元）")
    is_limit_up: bool = Field(..., description="是否触及涨停")
    is_limit_down: bool = Field(..., description="是否触及跌停")
    limit_rate: float = Field(..., description="涨跌停幅度（%），如主板10%、科创20%、ST5%")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="错误信息")


class LimitUpItem(BaseModel):
    code: str = Field(..., description="代码")
    name: str = Field(..., description="名称")
    price: float = Field(..., description="价格（元）")
    change_percent: float = Field(..., description="涨幅（%）")
    amount: float = Field(..., description="成交额（元）")
    float_market_cap: float = Field(..., description="流通市值（元）")
    total_market_cap: float = Field(..., description="总市值（元）")
    turnover_rate: float = Field(..., description="换手率（%）")
    consecutive_boards: int = Field(..., description="连板数")
    first_board_time: str = Field(..., description="首次封板时间（HH:mm:ss）")
    last_board_time: str = Field(..., description="最后封板时间（HH:mm:ss）")
    seal_funds: float = Field(..., description="封板资金（元）")
    broken_boards: int = Field(..., description="炸板次数")
    stat: str = Field(..., description="涨停统计（x天/y板）")


class RealTimePublicItem(BaseModel):
    fm: float = Field(..., description="五分钟涨跌幅（%）")
    h: float = Field(..., description="最高价（元）")
    hs: float = Field(..., description="换手（%）")
    lb: float = Field(..., description="量比（%）")
    l: float = Field(..., description="最低价（元）")
    lt: float = Field(..., description="流通市值（元）")
    o: float = Field(..., description="开盘价（元）")
    pe: float = Field(..., description="市盈率（动态）")
    pc: float = Field(..., description="涨跌幅（%）")
    p: float = Field(..., description="当前价格（元）")
    sz: float = Field(..., description="总市值（元）")
    cje: float = Field(..., description="成交额（元）")
    ud: float = Field(..., description="涨跌额（元）")
    v: float = Field(..., description="成交量（手）")
    yc: float = Field(..., description="昨日收盘价（元）")
    zf: float = Field(..., description="振幅（%）")
    zs: float = Field(..., description="涨速（%）")
    sjl: float = Field(..., description="市净率")
    zdf60: float = Field(..., description="60日涨跌幅（%）")
    zdfnc: float = Field(..., description="年初至今涨跌幅（%）")
    t: str = Field(..., description="更新时间 yyyy-MM-ddHH:mm:ss")


class RealTimeBrokerItem(BaseModel):
    p: float = Field(..., description="最新价")
    o: float = Field(..., description="开盘价")
    h: float = Field(..., description="最高价")
    l: float = Field(..., description="最低价")
    yc: float = Field(..., description="前收盘价")
    cje: float = Field(..., description="成交总额")
    v: float = Field(..., description="成交总量")
    pv: float = Field(..., description="原始成交总量")
    t: str = Field(..., description="更新时间")
    ud: float = Field(..., description="涨跌额")
    pc: float = Field(..., description="涨跌幅")
    zf: float = Field(..., description="振幅")
    pe: float = Field(..., description="市盈率")
    tr: float = Field(..., description="换手率")
    pb_ratio: float = Field(..., description="市净率")
    tv: float = Field(..., description="成交量")


class RealTimePublicBatchItem(BaseModel):
    dm: str = Field(..., description="股票代码")
    p: float = Field(..., description="最新价")
    o: float = Field(..., description="开盘价")
    h: float = Field(..., description="最高价")
    l: float = Field(..., description="最低价")
    yc: float = Field(..., description="前收盘价")
    cje: float = Field(..., description="成交总额")
    v: float = Field(..., description="成交总量")
    pv: float = Field(..., description="原始成交总量")
    t: str = Field(..., description="更新时间")
    ud: float = Field(..., description="涨跌额")
    pc: float = Field(..., description="涨跌幅")
    zf: float = Field(..., description="振幅")
    pe: float = Field(..., description="市盈率")
    tr: float = Field(..., description="换手率")
    pb_ratio: float = Field(..., description="市净率")
    tv: float = Field(..., description="成交量")


class LimitDownItem(BaseModel):
    dm: str = Field(..., description="代码")
    mc: str = Field(..., description="名称")
    p: float = Field(..., description="价格（元）")
    zf: float = Field(..., description="跌幅（%）")
    cje: float = Field(..., description="成交额（元）")
    lt: float = Field(..., description="流通市值（元）")
    zsz: float = Field(..., description="总市值（元）")
    pe: float = Field(..., description="动态市盈率")
    hs: float = Field(..., description="换手率（%）")
    lbc: int = Field(..., description="连续跌停次数")
    lbt: str = Field(..., description="最后封板时间（HH:mm:ss）")
    zj: float = Field(..., description="封单资金（元）")
    fba: float = Field(..., description="板上成交额（元）")
    zbc: int = Field(..., description="开板次数")


class BreakPoolItem(BaseModel):
    dm: str = Field(..., description="代码")
    mc: str = Field(..., description="名称")
    p: float = Field(..., description="价格（元）")
    ztp: float = Field(..., description="涨停价（元）")
    zf: float = Field(..., description="涨跌幅（%）")
    cje: float = Field(..., description="成交额（元）")
    lt: float = Field(..., description="流通市值（元）")
    zsz: float = Field(..., description="总市值（元）")
    zs: float = Field(..., description="涨速（%）")
    hs: float = Field(..., description="转手率（%）")
    tj: str = Field(..., description="涨停统计（x天/y板）")
    fbt: str = Field(..., description="首次封板时间（HH:mm:ss）")
    zbc: int = Field(..., description="炸板次数")


class StrongPoolItem(BaseModel):
    dm: str = Field(..., description="代码")
    mc: str = Field(..., description="名称")
    p: float = Field(..., description="价格（元）")
    ztp: float = Field(..., description="涨停价（元）")
    zf: float = Field(..., description="涨幅（%）")
    cje: float = Field(..., description="成交额（元）")
    lt: float = Field(..., description="流通市值（元）")
    zsz: float = Field(..., description="总市值（元）")
    zs: float = Field(..., description="涨速（%）")
    nh: int = Field(..., description="是否新高（0：否，1：是）")
    lb: float = Field(..., description="量比")
    hs: float = Field(..., description="换手率（%）")
    tj: str = Field(..., description="涨停统计（x天/y板）")
