# 股票数据服务项目结构文档

## 项目概述

这是一个股票数据服务项目，提供股票行情查询、涨跌停状态查询、板块概念查询等功能，支持多种数据源包括第三方API和Akshare爬虫数据。

## 目录结构

```
/Users/zxl/Desktop/laicai/server/
├── api/                      # API路由层
│   ├── akshare_routes.py     # Akshare数据接口路由
│   └── routes.py             # 基础接口路由
├── akshareData/              # Akshare数据源实现
│   └── provider.py           # Akshare数据提供函数
├── core/                     # 核心工具和配置
│   ├── http_client.py        # HTTP客户端工具
│   └── utils.py              # 通用工具函数
├── models/                   # 数据模型和响应结构
│   └── schemas.py            # Pydantic数据模型定义
├── services/                 # 业务逻辑层
│   ├── api_service.py        # API请求处理服务
│   ├── limit_service.py      # 涨跌停服务
│   ├── pool_service.py       # 股票池服务
│   ├── quote_service.py      # 行情服务
│   └── realtime_service.py   # 实时数据服务
├── __init__.py               # 项目初始化文件
├── .gitignore                # Git忽略配置
├── config.py                 # 项目配置文件
├── main.py                   # 项目主入口
├── README.md                 # 项目说明文档
├── requirements.txt          # 依赖包列表
└── start.sh                  # 服务启动脚本
```

## 接口分类

### 1. 基础接口（第三方API）

这些接口主要使用第三方API或直接从公开数据源获取数据：

| 接口路径 | 功能描述 | 数据源 | 文件位置 |
|---------|---------|-------|---------|
| `/quote` | 股票行情查询 | 新浪财经 | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |
| `/hsstock/instrument/{instrument}` | 股票涨跌停状态查询 | 第三方API（可配置） | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |
| `/hslt/ztgc` | 涨停股池查询 | 第三方API | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |
| `/hslt/dtgc` | 跌停股池查询 | 第三方API | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |
| `/hslt/zbgc` | 炸板股池查询 | 第三方API | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |
| `/hslt/qsgc` | 强势股池查询 | 第三方API | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |
| `/hsrl/ssjy` | 实时交易数据查询 | 第三方API | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |
| `/hsstock/real/time` | 股票实时数据查询 | 第三方API | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |
| `/hsrl/ssjy_more` | 更多实时交易数据查询 | 第三方API | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |
| `/ws/quote` | WebSocket行情推送 | 第三方API | <mcfile name="routes.py" path="/Users/zxl/Desktop/laicai/server/api/routes.py"></mcfile> |

### 2. Akshare爬虫数据接口

这些接口使用Akshare库爬取东方财富、同花顺等网站的数据：

| 接口路径 | 功能描述 | Akshare函数 | 文件位置 |
|---------|---------|------------|---------|
| `/akshare/api/quote` | Akshare股票行情查询 | `stock_zh_a_spot_em` | <mcfile name="akshare_routes.py" path="/Users/zxl/Desktop/laicai/server/api/akshare_routes.py"></mcfile> |
| `/akshare/api/board/concept/info` | 板块概念信息查询 | `stock_board_concept_info_ths` | <mcfile name="akshare_routes.py" path="/Users/zxl/Desktop/laicai/server/api/akshare_routes.py"></mcfile> |
| `/akshare/api/board/concept/list` | 板块概念列表查询 | `stock_board_concept_name_ths` | <mcfile name="akshare_routes.py" path="/Users/zxl/Desktop/laicai/server/api/akshare_routes.py"></mcfile> |
| `/akshare/api/market/activity/legu` | 市场活跃度查询 | `stock_market_activity_legu` | <mcfile name="akshare_routes.py" path="/Users/zxl/Desktop/laicai/server/api/akshare_routes.py"></mcfile> |
| `/akshare/api/stock/basic/info` | 个股基本信息查询 | `stock_individual_basic_info_xq`/`stock_basic_info_em` | <mcfile name="akshare_routes.py" path="/Users/zxl/Desktop/laicai/server/api/akshare_routes.py"></mcfile> |
| `/akshare/api/stock/spot/all` | 所有A股实时行情查询 | `stock_zh_a_spot_em` | <mcfile name="akshare_routes.py" path="/Users/zxl/Desktop/laicai/server/api/akshare_routes.py"></mcfile> |

## 核心组件说明

### 1. API服务层

- **api_service.py**: 封装API请求的公共逻辑，包括错误处理和响应模型转换
  - `handle_api_request`: 处理基础API请求
  - `handle_akshare_request`: 处理Akshare数据请求
  - `handle_ws_quote`: 处理WebSocket行情请求

### 2. 数据源实现

- **quote_service.py**: 提供股票行情查询服务，使用新浪财经作为数据源
- **limit_service.py**: 提供涨跌停状态查询服务，优先使用第三方API，失败时回退到本地计算
- **pool_service.py**: 提供股票池查询服务，包括涨停股池、跌停股池、炸板股池和强势股池
- **realtime_service.py**: 提供实时交易数据查询服务
- **akshareData/provider.py**: 提供Akshare数据源的实现，包括以下函数：
  - `get_quote_by_akshare`: 使用Akshare获取股票行情
  - `get_board_concept_info_ths`: 获取板块概念信息
  - `get_board_concept_list_ths`: 获取板块概念列表
  - `get_stock_market_activity_legu`: 获取市场活跃度数据
  - `get_stock_individual_basic_info_xq`: 获取个股基本信息
  - `get_stock_zh_a_spot_em`: 获取所有A股实时行情

### 3. 核心工具

- **http_client.py**: 封装HTTP请求，提供get_text和get_json函数
- **utils.py**: 提供通用工具函数，如股票代码归一化、价格四舍五入等

## 技术栈

- **Python**: 主要开发语言
- **FastAPI**: Web框架，用于构建API接口
- **Akshare**: 股票数据爬虫库
- **Pydantic**: 数据模型验证和序列化
- **WebSocket**: 实时数据推送
- **Requests**: HTTP客户端库

## 数据流程

1. **客户端请求** → **API路由层**（routes.py或akshare_routes.py）
2. **API路由层** → **API服务层**（api_service.py）
3. **API服务层** → **业务逻辑层**（quote_service.py等）或 **Akshare数据源**（akshareData/provider.py）
4. **业务逻辑层** → **第三方API**或**本地计算**
5. **Akshare数据源** → **Akshare库** → **目标网站**
6. **响应数据** → **客户端**

## 配置说明

项目支持通过环境变量或配置文件进行配置：

- `THIRD_PARTY_BASE_URL`: 第三方API基础URL
- `THIRD_PARTY_API_KEY`: 第三方API密钥

## 启动方式

使用以下命令启动服务：

```bash
bash start.sh
```

服务默认运行在 `http://0.0.0.0:8000`。

## 接口文档

启动服务后，可以通过以下地址访问API文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
