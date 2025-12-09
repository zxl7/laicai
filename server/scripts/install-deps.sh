#!/bin/bash

# 安装依赖脚本

# 默认环境
env="all"

# 显示帮助信息
show_help() {
    echo "===== laicai-stock 依赖安装脚本 ====="
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -e, --env <环境>     指定安装环境 (默认: all)"
    echo "                       可选值: all, dev, prod, test"
    echo "  -h, --help           显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                    # 安装所有环境依赖"
    echo "  $0 -e dev             # 只安装开发环境依赖"
    echo "  $0 -e prod            # 只安装生产环境依赖"
    echo "======================================"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            env="$2"
            shift
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 显示当前环境信息
echo "===== laicai-stock 依赖安装脚本 ====="
echo "当前工作目录: $(pwd)"
echo "安装环境: $env"
echo "======================================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未安装Python 3"
    exit 1
fi

# 检查pip是否安装
if ! command -v pip &> /dev/null; then
    echo "错误: 未安装pip"
    exit 1
fi

# 更新pip
echo "正在更新pip..."
pip install --upgrade pip

# 根据环境安装依赖
case $env in
    all)
        echo "正在安装所有环境依赖..."
        pip install -r requirements.txt
        if [ -f "requirements-dev.txt" ]; then
            pip install -r requirements-dev.txt
        fi
        if [ -f "requirements-test.txt" ]; then
            pip install -r requirements-test.txt
        fi
        ;;
    dev)
        echo "正在安装开发环境依赖..."
        pip install -r requirements.txt
        if [ -f "requirements-dev.txt" ]; then
            pip install -r requirements-dev.txt
        fi
        ;;
    prod)
        echo "正在安装生产环境依赖..."
        pip install -r requirements.txt
        ;;
    test)
        echo "正在安装测试环境依赖..."
        pip install -r requirements.txt
        if [ -f "requirements-test.txt" ]; then
            pip install -r requirements-test.txt
        fi
        ;;
    *)
        echo "错误: 未知的环境 '$env'"
        show_help
        exit 1
        ;;
esac

if [ $? -eq 0 ]; then
    echo "======================================"
    echo "✓ 依赖安装成功！"
    echo "======================================"
else
    echo "======================================"
    echo "✗ 依赖安装失败！"
    echo "======================================"
    exit 1
fi