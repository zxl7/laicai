#!/bin/bash

# 启动生产服务器脚本

# 设置环境变量
export PYTHONPATH=$(pwd)/src
export APP_ENV=production

# 显示当前环境信息
echo "===== laicai-stock 生产服务器启动脚本 ====="
echo "当前工作目录: $(pwd)"
echo "Python路径: $PYTHONPATH"
echo "应用环境: $APP_ENV"
echo "======================================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未安装Python 3"
    exit 1
fi

# 检查依赖是否安装
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "警告: 依赖未安装，正在安装..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi

# 检查是否存在.env文件
if [ ! -f ".env" ]; then
    echo "错误: .env文件不存在，请从.env.example复制并配置"
    exit 1
fi

# 启动生产服务器
echo "正在启动生产服务器..."
echo "按 Ctrl+C 停止服务器"
echo "======================================"

# 使用gunicorn作为生产服务器
gunicorn -w 4 -k uvicorn.workers.UvicornWorker laicai.main:app --bind 0.0.0.0:8000