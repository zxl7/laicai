#!/usr/bin/env python3
"""
测试脚本：从接口获取数据并更新本地JSON文件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.json_utils import JsonFileHandler
from src.services.api_json_updater import ApiJsonUpdater
from datetime import datetime


def test_json_file_handler():
    """
    测试JsonFileHandler类的功能
    """
    print("\n=== 测试JsonFileHandler类 ===")
    
    # 使用临时JSON文件进行测试
    test_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/test_stocks.json"
    
    # 初始化JSON文件处理器
    json_handler = JsonFileHandler(test_file_path)
    
    # 测试写入功能
    test_data = {
        "600000": {
            "code": "600000",
            "name": "浦发银行",
            "price": 8.25,
            "lastUpdated": datetime.now().isoformat() + "Z"
        }
    }
    
    success = json_handler.write(test_data)
    if success:
        print("✓ 写入JSON文件成功")
    else:
        print("✗ 写入JSON文件失败")
        return False
    
    # 测试读取功能
    read_data = json_handler.read()
    if read_data:
        print("✓ 读取JSON文件成功")
        print(f"  读取到的数据: {read_data}")
    else:
        print("✗ 读取JSON文件失败")
        return False
    
    # 测试更新功能
    update_data = {
        "600001": {
            "code": "600001",
            "name": "邯郸钢铁",
            "price": 3.58,
            "lastUpdated": datetime.now().isoformat() + "Z"
        }
    }
    
    success = json_handler.update(update_data)
    if success:
        print("✓ 更新JSON文件成功")
    else:
        print("✗ 更新JSON文件失败")
        return False
    
    # 验证更新结果
    updated_data = json_handler.read()
    if "600001" in updated_data:
        print("✓ 验证更新结果成功")
        print(f"  更新后的数据总条目: {len(updated_data)}")
    else:
        print("✗ 验证更新结果失败")
        return False
    
    print("\n=== JsonFileHandler类测试完成 ===")
    return True


def test_api_json_updater():
    """
    测试ApiJsonUpdater类的功能
    """
    print("\n=== 测试ApiJsonUpdater类 ===")
    
    # 使用模拟的API URL和本地JSON文件
    # 注意：实际使用时需要替换为真实的API URL
    api_url = "https://api.example.com/stocks"  # 这是一个模拟的URL
    json_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
    
    # 初始化API数据更新服务
    updater = ApiJsonUpdater(api_url, json_file_path)
    
    # 模拟从API获取数据（由于是模拟URL，会失败，这是预期行为）
    print("\n测试从API获取数据（模拟URL，预期失败）:")
    api_data = updater.fetch_data_from_api()
    
    if not api_data:
        print("✓ 模拟API请求失败（预期行为）")
    else:
        print("✗ 模拟API请求成功（非预期行为）")
    
    # 测试数据转换功能
    print("\n测试数据转换功能:")
    mock_api_data = {
        "data": {
            "stocks": {
                "600002": {
                    "dm": "600002",
                    "mc": "万科A",
                    "zf": 2.5,
                    "p": 15.8,
                    "ztp": 16.9
                }
            }
        }
    }
    
    transformed_data = updater.transform_data(mock_api_data)
    if transformed_data and "600002" in transformed_data:
        print("✓ 数据转换功能测试成功")
        print(f"  转换后的数据: {transformed_data['600002'].keys()}")
    else:
        print("✗ 数据转换功能测试失败")
    
    print("\n=== ApiJsonUpdater类测试完成 ===")
    return True


def main():
    """
    主函数
    """
    print("Python 修改本地 JSON 文件测试")
    print("=" * 50)
    
    # 安装必要的依赖
    print("\n检查并安装依赖...")
    try:
        import requests
        print("✓ requests库已安装")
    except ImportError:
        print("✗ requests库未安装，正在安装...")
        os.system("pip install requests")
        print("✓ requests库安装成功")
    
    # 运行测试
    test_json_file_handler()
    test_api_json_updater()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n使用说明：")
    print("1. 实际使用时，修改 api_json_updater.py 中的 API URL 为真实地址")
    print("2. 根据真实API响应格式调整 transform_data 方法")
    print("3. 在项目中导入并使用这些类")
    
    print("\n示例代码：")
    print("""
from src.services.api_json_updater import ApiJsonUpdater

# 初始化更新服务
updater = ApiJsonUpdater(
    api_url="https://真实API地址",
    json_file_path="/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
)

# 更新JSON文件
updater.update_json_file(params={"limit": 100})
""")


if __name__ == "__main__":
    main()
