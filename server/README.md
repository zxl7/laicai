# Laicai 股票分析后台服务

## 快速开始
- 创建虚拟环境并安装依赖：
```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

- 启动服务：
```
.venv/bin/uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload
```

或一键启动：
```
bash server/start.sh
```

若不使用虚拟环境，可直接：
```
python3 -m pip install "fastapi==0.95.2" "pydantic==1.10.13" "uvicorn==0.22.0" "starlette==0.27.0" "requests"
python3 -m uvicorn server.app:app --host 0.0.0.0 --port 8000
```

## 第三方数据源配置
- 通过环境变量启用第三方接口：
```
export THIRD_PARTY_BASE_URL="https://api.biyingapi.com/hsstock/instrument"
export THIRD_PARTY_API_KEY="<你的 token>"
```
- 行为：
  - `limit-status` 会调用上述 instrument 接口，结合最新行情计算涨跌停状态
  - `quote` 仍使用新浪行情（第三方未提供统一 quote 端点时自动回退）

## 接口说明
- `GET /quote?symbol=...`
  - 支持 `600000`、`sh600000`、`sz000001`、`000547.SZ`
  - 返回：`code,name,price,change_percent,change_amount,open,high,low,prev_close,time`

- `GET /limit-status?symbol=...`
  - 返回：`limit_up_price,limit_down_price,is_limit_up,is_limit_down,limit_rate`

- `WS /ws/quote?symbol=...`
  - 每秒推送一次行情 JSON

## 示例
- `curl "http://localhost:8000/quote?symbol=600000"`
- `curl "http://localhost:8000/limit-status?symbol=000547"`
- `curl "http://localhost:8000/limit-status?symbol=000547.SZ"`
- `wscat -c "ws://localhost:8000/ws/quote?symbol=sh600000"`

## 目录结构与代码位置
- FastAPI 应用与端点：`server/app.py`
  - 根路径与端点列表：`server/app.py:24`
  - 行情查询：`server/app.py:27`
  - 涨跌停状态：`server/app.py:36`
  - 涨停股池：`server/app.py:45`
  - WebSocket 行情：`server/app.py:54`
- 适配层（对外统一接口）：`server/data_provider.py`
  - 委托至业务层：`get_quote`、`get_limit_status`、`get_limit_up_pool`
- 业务逻辑（services）
  - 行情：`server/services/quote_service.py`
  - 涨跌停：`server/services/limit_service.py`
  - 涨停股池：`server/services/pool_service.py`
- 公共方法（common）
  - 代码归一化/交易所转换/价格保留/时间格式化/涨跌停比例：`server/common/utils.py`
- 启动脚本：`server/start.sh`

## API 文档（Apifox）
- 打开 Apifox → 导入 OpenAPI → 地址：`http://localhost:8000/openapi.json`
- 标签与说明：
  - `pool`：涨停股池 `/limit-up-pool`
  - `quote`：行情 `/quote`
  - `status`：涨跌停状态 `/limit-status`

## 注意事项
- 若出现 `uvicorn` 不在 PATH，可使用 `python3 -m uvicorn` 或通过 `.venv/bin/uvicorn`
- 当前环境为 Python 3.7，已固定兼容版本的 `fastapi/pydantic/starlette/uvicorn`
