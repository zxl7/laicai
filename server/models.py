from pydantic import BaseModel


class QuoteResponse(BaseModel):
    code: str
    name: str
    price: float
    change_percent: float
    change_amount: float
    open: float
    high: float
    low: float
    prev_close: float
    time: str


class LimitStatusResponse(BaseModel):
    code: str
    name: str
    price: float
    limit_up_price: float
    limit_down_price: float
    is_limit_up: bool
    is_limit_down: bool
    limit_rate: float


class ErrorResponse(BaseModel):
    error: str


class LimitUpItem(BaseModel):
    code: str
    name: str
    price: float
    change_percent: float
    amount: float
    float_market_cap: float
    total_market_cap: float
    turnover_rate: float
    consecutive_boards: int
    first_board_time: str
    last_board_time: str
    seal_funds: float
    broken_boards: int
    stat: str


class RealTimePublicItem(BaseModel):
    fm: float
    h: float
    hs: float
    lb: float
    l: float
    lt: float
    o: float
    pe: float
    pc: float
    p: float
    sz: float
    cje: float
    ud: float
    v: float
    yc: float
    zf: float
    zs: float
    sjl: float
    zdf60: float
    zdfnc: float
    t: str


class RealTimeBrokerItem(BaseModel):
    p: float
    o: float
    h: float
    l: float
    yc: float
    cje: float
    v: float
    pv: float
    t: str
    ud: float
    pc: float
    zf: float
    pe: float
    tr: float
    pb_ratio: float
    tv: float


class RealTimePublicBatchItem(BaseModel):
    dm: str
    p: float
    o: float
    h: float
    l: float
    yc: float
    cje: float
    v: float
    pv: float
    t: str
    ud: float
    pc: float
    zf: float
    pe: float
    tr: float
    pb_ratio: float
    tv: float


class LimitDownItem(BaseModel):
    dm: str
    mc: str
    p: float
    zf: float
    cje: float
    lt: float
    zsz: float
    pe: float
    hs: float
    lbc: int
    lbt: str
    zj: float
    fba: float
    zbc: int


class BreakPoolItem(BaseModel):
    dm: str
    mc: str
    p: float
    ztp: float
    zf: float
    cje: float
    lt: float
    zsz: float
    zs: float
    hs: float
    tj: str
    fbt: str
    zbc: int


class StrongPoolItem(BaseModel):
    dm: str
    mc: str
    p: float
    ztp: float
    zf: float
    cje: float
    lt: float
    zsz: float
    zs: float
    nh: int
    lb: float
    hs: float
    tj: str
