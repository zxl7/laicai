#!/usr/bin/env python3
"""
简单测试导入路径是否正确的脚本
"""

import sys
import os

# 设置PYTHONPATH为src目录
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # 测试模块路径
    print("测试核心模块路径...")
    import core
    print(f"✓ core模块存在: {core.__file__}")
    
    import core.app
    print(f"✓ core.app模块存在: {core.app.__file__}")
    
    print("\n测试配置模块路径...")
    import config
    print(f"✓ config模块存在: {config.__file__}")
    
    print("\n测试数据模型模块路径...")
    import schemas
    print(f"✓ schemas模块存在: {schemas.__file__}")
    
    import schemas.quote
    print(f"✓ schemas.quote模块存在: {schemas.quote.__file__}")
    
    print("\n测试服务层模块路径...")
    import services
    print(f"✓ services模块存在: {services.__file__}")
    
    import services.quote
    print(f"✓ services.quote模块存在: {services.quote.__file__}")
    
    print("\n所有模块路径测试通过！导入路径已正确设置。")
    
    print("\n当前项目结构:")
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'src')):
        level = root.replace(os.path.join(os.path.dirname(__file__), 'src'), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:10]:  # 只显示前10个文件
            print(f"{subindent}{file}")
        if len(files) > 10:
            print(f"{subindent}... and {len(files) - 10} more files")
            
except Exception as e:
    print(f"✗ 模块测试失败: {e}")
    import traceback
    traceback.print_exc()
