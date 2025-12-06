# Laicai 股票分析后台服务（重构版）

## 快速开始
- 安装依赖：
```
python3 -m pip install -r requirements.txt
```

- 启动服务：
```
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- 或一键启动脚本：
```
bash server/start.sh
```

若你没有全局安装 uvicorn，可先执行：
```
python3 -m pip install "fastapi==0.95.2" "pydantic==1.10.13" "uvicorn==0.22.0" "starlette==0.27.0" "requests"
```

## 目录结构
```
server/
 ├── api/              # API 路由
 ├── core/             # 核心工具/环境读取
 ├── models/           # 数据模型
 ├── services/         # 服务层
 ├── config.py         # 配置
 └── main.py           # 应用入口
└── requirements.txt   # 依赖
└── .env               # 环境变量（可选）
```

## 第三方数据源配置
- 环境变量（或 `.env` 文件）
```
export THIRD_PARTY_API_KEY="<你的 licence>"
export THIRD_PARTY_BASE_URL="https://api.biyingapi.com/hsstock/instrument"
export THIRD_PARTY_SSJY_BASE_URL="http://api.biyingapi.com/hsrl/ssjy"
export THIRD_PARTY_REALTIME_BASE_URL="https://api.biyingapi.com/hsstock/real/time"
export THIRD_PARTY_SSJY_MORE_BASE_URL="http://api.biyingapi.com/hsrl/ssjy_more"
export THIRD_PARTY_ZTGC_BASE_URL="https://api.biyingapi.com/hslt/ztgc"
export THIRD_PARTY_DTGC_BASE_URL="http://api.biyingapi.com/hslt/dtgc"
export THIRD_PARTY_ZBGC_BASE_URL="http://api.biyingapi.com/hslt/zbgc"
export THIRD_PARTY_QSGC_BASE_URL="http://api.biyingapi.com/hslt/qsgc"
```
- 也可在请求中传入 `licence`（Query 或 Header）覆盖环境变量

## 接口说明
- `GET /quote?symbol=...` 基础行情（新浪源）
- `GET /limit-status?symbol=...` 涨跌停状态（支持第三方 instrument 源）
- `GET /limit-up-pool?date=...&licence=...` 涨停股池（默认当天）
- `GET /limit-down-pool?date=...&licence=...` 跌停股池（默认当天）
- `GET /break-pool?date=...&licence=...` 炸板股池（默认当天）
- `GET /strong-pool?date=...&licence=...` 强势股池（默认当天）
- `GET /realtime/public?symbol=...&licence=...` 实时交易（公开源）
- `GET /realtime/broker?symbol=...&licence=...` 实时交易（券商源）
- `GET /realtime/public/batch?symbols=...&licence=...` 批量实时交易（公开源，≤20支）
- `WS /ws/quote?symbol=...` WebSocket 每秒推送一次行情 JSON

## 示例
- `curl "http://localhost:8000/quote?symbol=600000"`
- `curl "http://localhost:8000/limit-status?symbol=000547"`
- `curl "http://localhost:8000/realtime/broker?symbol=000547&licence=<LICENCE>"`
- `curl -H "licence: <LICENCE>" "http://localhost:8000/limit-up-pool?date=2025-12-05"`

## API 文档（Apifox）
- Apifox → 导入 OpenAPI → 地址：`http://localhost:8000/openapi.json`
- 已包含中文字段描述、示例与 `licence` 参数（Query/Head）

## 迁移说明（清理旧入口与重复逻辑）
- 旧入口与重复实现已清理：`server/app.py`、`server/simple_server.py`、`server/sentiment_monitor/*`、`server/common/*`、`server/data_provider.py`、`server/models.py`
- 统一入口为 `main.py`，统一路由位于 `api/routes.py`

## 注意事项
- 若出现 `uvicorn` 不在 PATH，可使用 `python3 -m uvicorn`
- 当前环境为 Python 3.7，已固定兼容版本的 `fastapi/pydantic/starlette/uvicorn`
