# laicai-stock

企业级股票数据服务项目

## 项目简介

这是一个基于FastAPI开发的企业级股票数据服务项目，提供股票行情查询、涨跌停状态查询、股票池查询等功能。

## 主要功能

- 股票行情查询
- 涨跌停状态查询
- 涨停股池查询
- 跌停股池查询
- 炸板股池查询
- 强势股池查询
- 实时交易数据查询

## 技术栈

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- AkShare

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

## 项目结构

```
laicai-stock/
├── src/                    # 主源码目录
│   ├── app/                # 应用核心
│   ├── api/                # API路由
│   ├── services/           # 业务逻辑层
│   ├── models/             # 数据模型
│   ├── schemas/            # 数据验证和序列化
│   ├── utils/              # 工具函数
│   └── config/             # 配置文件
├── tests/                  # 测试目录
├── docs/                   # 文档目录
├── scripts/                # 脚本目录
├── main.py                 # 应用入口
├── requirements.txt        # 项目依赖
├── setup.py                # 安装脚本
├── README.md               # 项目说明
├── LICENSE                 # 许可证
└── CHANGELOG.md            # 变更日志
```

## 开发指南

### 代码规范

- 遵循PEP 8编码规范
- 使用类型注解
- 编写单元测试
- 保持代码简洁和可维护性

### 提交规范

- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试用例更新
- chore: 构建或依赖更新

## 许可证

MIT License