# 股票行情API

## 获取单个股票的实时行情

### 接口说明

获取单个股票的实时行情数据，包括最新价、涨跌幅、成交量等信息。

### 请求

```
GET /api/quote/current
```

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| symbol | string | 是 | 股票代码，如"000001.SZ" |

### 响应

```json
{
    "symbol": "000001.SZ",
    "name": "平安银行",
    "price": 15.80,
    "change": 10.03,
    "change_amount": 1.44,
    "volume": 150000000,
    "amount": 2370000000,
    "turnover": 1.5,
    "amplitude": 8.32,
    "high": 15.80,
    "low": 14.36,
    "open": 14.70,
    "prev_close": 14.36,
    "market_cap": 350000000000,
    "circulating_cap": 350000000000,
    "pe": 7.8,
    "pb": 0.85
}
```

## 获取所有涨停股票

### 接口说明

获取所有涨停股票的列表，包括股票代码、名称、涨停价格等信息。

### 请求

```
GET /api/quote/limit-up
```

### 响应

```json
{
    "total": 2,
    "stocks": [
        {
            "symbol": "000001.SZ",
            "name": "平安银行",
            "price": 15.80,
            "change": 10.03,
            "change_amount": 1.44,
            "volume": 150000000,
            "amount": 2370000000,
            "open_time": "09:30:00"
        },
        {
            "symbol": "600036.SH",
            "name": "招商银行",
            "price": 38.90,
            "change": 10.01,
            "change_amount": 3.54,
            "volume": 80000000,
            "amount": 3112000000,
            "open_time": "09:35:20"
        }
    ]
}
```

## 获取所有跌停股票

### 接口说明

获取所有跌停股票的列表，包括股票代码、名称、跌停价格等信息。

### 请求

```
GET /api/quote/limit-down
```

### 响应

```json
{
    "total": 2,
    "stocks": [
        {
            "symbol": "002007.SZ",
            "name": "华兰生物",
            "price": 28.50,
            "change": -9.98,
            "change_amount": -3.17,
            "volume": 30000000,
            "amount": 855000000
        },
        {
            "symbol": "600519.SH",
            "name": "贵州茅台",
            "price": 1780.00,
            "change": -4.99,
            "change_amount": -93.50,
            "volume": 1200000,
            "amount": 2136000000
        }
    ]
}
```

## 获取所有炸板股票

### 接口说明

获取所有炸板股票的列表，包括股票代码、名称、炸板价格等信息。

### 请求

```
GET /api/quote/failed-limit-up
```

### 响应

```json
{
    "total": 2,
    "stocks": [
        {
            "symbol": "000002.SZ",
            "name": "万科A",
            "price": 14.20,
            "change": 8.23,
            "change_amount": 1.08,
            "volume": 120000000,
            "amount": 1704000000,
            "high": 14.58,
            "limit_up_time": 3
        },
        {
            "symbol": "600048.SH",
            "name": "保利发展",
            "price": 15.80,
            "change": 7.52,
            "change_amount": 1.11,
            "volume": 90000000,
            "amount": 1422000000,
            "high": 16.23,
            "limit_up_time": 2
        }
    ]
}
```

## 获取强势股票池

### 接口说明

获取强势股票池的列表，包括股票代码、名称、价格等信息。

### 请求

```
GET /api/quote/strong
```

### 响应

```json
{
    "total": 2,
    "stocks": [
        {
            "symbol": "000858.SZ",
            "name": "五粮液",
            "price": 185.00,
            "change": 7.89,
            "change_amount": 13.50,
            "volume": 15000000,
            "amount": 2775000000
        },
        {
            "symbol": "002415.SZ",
            "name": "海康威视",
            "price": 38.90,
            "change": 6.23,
            "change_amount": 2.25,
            "volume": 25000000,
            "amount": 972500000
        }
    ]
}
```