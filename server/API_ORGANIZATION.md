# API接口组织方案

## 当前接口组织方式分析

目前项目的接口组织方式是：
1. `api/routes.py` - 包含所有基础接口的路由定义
2. `api/akshare_routes.py` - 包含所有Akshare数据接口的路由定义

每个文件中包含多个接口路由，业务逻辑主要在services目录下实现。这种方式已经初步实现了路由和业务逻辑的分离，但还可以进一步优化。

## 优化方案：更清晰的路由与业务逻辑分离

### 1. 按功能模块组织路由文件

**不是必须一个接口一个py文件**，但可以按功能模块拆分路由文件，实现更好的模块化：

```
/api/
├── __init__.py           # 路由注册入口
├── routes.py             # 基础路由（根路径等）
├── realtime_routes.py    # 实时数据相关接口
└── akshare/
    ├── __init__.py       # Akshare路由注册
    ├── quote_routes.py   # Akshare行情接口
    ├── concept_routes.py # 板块概念接口
    └── market_routes.py  # 市场数据接口
```

### 2. 实现路由与业务逻辑的完全分离

**核心思想：路由文件只负责：**
- 定义接口地址
- 定义请求参数
- 定义响应模型
- 调用业务逻辑函数

**业务逻辑文件只负责：**
- 实现具体的业务功能
- 处理数据
- 与数据源交互

### 3. 代码示例

#### 优化后的路由文件（quote_routes.py）

```python
from fastapi import APIRouter, Query
from models.schemas import QuoteResponse, ErrorResponse
from services.api_service import handle_api_request
from services.quote_service import get_quote

router = APIRouter(
    prefix="",
    tags=["行情接口"],
)

@router.get(
    "/quote",
    summary="股票行情查询",
    description="查询指定股票的最新行情信息，包括最新价格、涨跌幅、开高低收等数据",
    response_model=QuoteResponse,
    responses={400: {"model": ErrorResponse}},
)
def quote(symbol: str = Query(..., description="股票代码，如 600000 或 sz000001")):
    """股票行情查询接口"""
    return handle_api_request(get_quote, symbol)
```

#### 业务逻辑文件（quote_service.py）

```python
from typing import Dict, Any
from core.utils import normalize_symbol, round_price
from core.http_client import get_text

def get_quote(symbol: str) -> Dict[str, Any]:
    """
    获取股票行情信息
    
    Args:
        symbol: 股票代码
        
    Returns:
        Dict[str, Any]: 股票行情数据
    """
    # 实现具体的行情获取逻辑
    # ...
    pass
```

#### 路由注册入口（__init__.py）

```python
from fastapi import APIRouter
from api.routes import router as base_router
from api.quote_routes import router as quote_router
from api.limit_routes import router as limit_router
from api.pool_routes import router as pool_router
from api.realtime_routes import router as realtime_router
from api.akshare import router as akshare_router

# 创建主路由
main_router = APIRouter()

# 注册所有子路由
main_router.include_router(base_router)
main_router.include_router(quote_router)
main_router.include_router(limit_router)
main_router.include_router(pool_router)
main_router.include_router(realtime_router)
main_router.include_router(akshare_router, prefix="/akshare", tags=["Akshare数据接口"])
```

### 4. 实现步骤

1. **创建新的路由目录结构**
2. **按功能模块拆分现有路由**
3. **创建路由注册入口文件**
4. **更新main.py中的路由注册**
5. **测试所有接口**

### 5. 优势

- **更好的模块化**：每个文件职责单一，便于维护
- **更清晰的代码结构**：路由定义和业务逻辑完全分离
- **更容易扩展**：新增功能只需添加新的路由文件和业务逻辑文件
- **更好的团队协作**：不同模块可以由不同开发人员负责

## 总结

可以实现"逻辑是逻辑，地址是地址"的分离，不需要一个接口一个py文件，而是按功能模块组织路由文件，每个路由文件只负责定义接口地址和参数，业务逻辑完全封装在services目录下。这种方式可以实现更好的代码组织和维护性。