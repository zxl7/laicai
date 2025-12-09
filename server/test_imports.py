#!/usr/bin/env python3
"""
测试导入路径是否正确的脚本
"""

import sys
import os

# 设置PYTHONPATH为src目录
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # 测试核心模块导入
    from core.app import create_app
    print("✓ 成功导入 core.app")
    
    from config import settings
    print("✓ 成功导入 config")
    
    from schemas.quote import StockQuote
    print("✓ 成功导入 schemas.quote")
    
    print("\n所有导入测试通过！")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    import traceback
    traceback.print_exc()
