# laicai-stock 文档

欢迎使用 laicai-stock 企业级股票数据服务项目文档！

## 项目简介

laicai-stock 是一个基于 FastAPI 开发的企业级股票数据服务项目，提供股票行情查询、涨跌停状态查询、股票池查询等功能。

## 文档结构

- **[API文档](api/index.md)**：详细介绍项目提供的所有API接口
- **[用户指南](guides/index.md)**：如何使用 laicai-stock 服务
- **[部署指南](deployment/index.md)**：如何部署 laicai-stock 服务
- **[开发指南](development/index.md)**：如何参与 laicai-stock 项目开发

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 访问API文档

```
http://localhost:8000/docs
http://localhost:8000/redoc
```

## 联系我们

如果您有任何问题或建议，请随时联系我们。