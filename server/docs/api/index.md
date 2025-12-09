# API文档

laicai-stock 提供了一系列RESTful API接口，用于获取股票行情数据和股票池信息。

## API列表

### 股票行情

- **[获取单个股票的实时行情](/api/quote.md#获取单个股票的实时行情)**
- **[获取所有涨停股票](/api/quote.md#获取所有涨停股票)**
- **[获取所有跌停股票](/api/quote.md#获取所有跌停股票)**
- **[获取所有炸板股票](/api/quote.md#获取所有炸板股票)**
- **[获取强势股票池](/api/quote.md#获取强势股票池)**

### 系统

- **[健康检查](/api/system.md#健康检查)**

## API调用示例

### 获取单个股票的实时行情

```bash
curl http://localhost:8000/api/quote/current?symbol=000001.SZ
```

### 获取所有涨停股票

```bash
curl http://localhost:8000/api/quote/limit-up
```

## 响应格式

所有API接口都返回统一的JSON格式响应：

```json
{
    "code": "SUCCESS",
    "message": "操作成功",
    "data": {
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
    },
    "timestamp": "2024-01-01T12:00:00"
}
```