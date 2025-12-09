#!/bin/bash

# 运行测试脚本

# 设置环境变量
export PYTHONPATH=$(pwd)/src
export APP_ENV=test

# 默认参数
TEST_PATH="tests"
REPORT_FORMAT="verbose"
TEST_ARGS=""

# 显示帮助信息
show_help() {
    echo "===== laicai-stock 测试运行脚本 ====="
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -p, --path <路径>    指定测试路径或文件 (默认: tests)"
    echo "  -f, --format <格式>  指定测试报告格式 (默认: verbose)"
    echo "                       可选值: verbose, simple, json, html"
    echo "  -h, --help           显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                    # 运行所有测试"
    echo "  $0 -p tests/unit      # 只运行单元测试"
    echo "  $0 -f simple          # 使用简单格式报告"
    echo "======================================"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--path)
            TEST_PATH="$2"
            shift
            shift
            ;;
        -f|--format)
            REPORT_FORMAT="$2"
            shift
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            TEST_ARGS="$TEST_ARGS $1"
            shift
            ;;
    esac
done

# 根据报告格式设置pytest参数
case $REPORT_FORMAT in
    verbose)
        PYTEST_ARGS="-v"
        ;;
    simple)
        PYTEST_ARGS="-q"
        ;;
    json)
        PYTEST_ARGS="--json-report"
        ;;
    html)
        PYTEST_ARGS="--html=test_report.html"
        ;;
    *)
        echo "警告: 未知的报告格式 '$REPORT_FORMAT'，使用默认格式"
        PYTEST_ARGS="-v"
        ;;
esac

# 显示当前环境信息
echo "===== laicai-stock 测试运行脚本 ====="
echo "当前工作目录: $(pwd)"
echo "Python路径: $PYTHONPATH"
echo "应用环境: $APP_ENV"
echo "测试路径: $TEST_PATH"
echo "报告格式: $REPORT_FORMAT"
echo "======================================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未安装Python 3"
    exit 1
fi

# 检查pytest是否安装
if ! command -v pytest &> /dev/null; then
    echo "警告: pytest未安装，正在安装..."
    pip install pytest pytest-asyncio pytest-cov pytest-html pytest-json-report
    if [ $? -ne 0 ]; then
        echo "错误: pytest安装失败"
        exit 1
    fi
fi

# 运行测试
echo "正在运行测试..."
pytest $PYTEST_ARGS $TEST_ARGS $TEST_PATH

test_exit_code=$?

# 显示测试结果总结
echo "======================================"
if [ $test_exit_code -eq 0 ]; then
    echo "✓ 所有测试通过！"
else
    echo "✗ 测试失败，退出码: $test_exit_code"
fi
echo "======================================"

exit $test_exit_code