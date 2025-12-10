"""
JSON文件操作工具类
提供读取、写入、更新本地JSON文件的功能
"""

import json
from typing import Dict, Any, Optional


class JsonFileHandler:
    """
    JSON文件处理类
    提供读取、写入、更新本地JSON文件的方法
    """
    
    def __init__(self, file_path: str):
        """
        初始化JSON文件处理器
        
        Args:
            file_path: JSON文件的绝对路径
        """
        self.file_path = file_path
    
    def read(self) -> Dict[str, Any]:
        """
        读取JSON文件内容
        
        Returns:
            Dict[str, Any]: JSON文件的内容，如果文件不存在则返回空字典
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"文件不存在: {self.file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"JSON文件格式错误: {self.file_path}")
            return {}
        except Exception as e:
            print(f"读取JSON文件失败: {str(e)}")
            return {}
    
    def write(self, data: Dict[str, Any]) -> bool:
        """
        写入JSON文件内容
        
        Args:
            data: 要写入的JSON数据
            
        Returns:
            bool: 写入成功返回True，失败返回False
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"写入JSON文件失败: {str(e)}")
            return False
    
    def update(self, new_data: Dict[str, Any]) -> bool:
        """
        更新JSON文件内容
        将新数据添加到现有数据中（如果键已存在则覆盖）
        
        Args:
            new_data: 要添加或更新的数据
            
        Returns:
            bool: 更新成功返回True，失败返回False
        """
        try:
            # 读取现有数据
            existing_data = self.read()
            
            # 更新数据（如果键已存在则覆盖）
            existing_data.update(new_data)
            
            # 写入更新后的数据
            return self.write(existing_data)
        except Exception as e:
            print(f"更新JSON文件失败: {str(e)}")
            return False
    
    def append(self, key: str, value: Any) -> bool:
        """
        向JSON文件追加新的键值对
        如果键已存在，则不会覆盖
        
        Args:
            key: 要添加的键
            value: 要添加的值
            
        Returns:
            bool: 添加成功返回True，键已存在或失败返回False
        """
        try:
            # 读取现有数据
            existing_data = self.read()
            
            # 检查键是否已存在
            if key in existing_data:
                print(f"键 '{key}' 已存在，不会覆盖")
                return False
            
            # 添加新键值对
            existing_data[key] = value
            
            # 写入更新后的数据
            return self.write(existing_data)
        except Exception as e:
            print(f"追加JSON数据失败: {str(e)}")
            return False


# 示例用法
if __name__ == "__main__":
    """
    示例：从接口获取数据并添加到本地JSON文件
    """
    import requests
    from datetime import datetime
    
    # JSON文件路径
    json_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
    
    # 初始化JSON文件处理器
    json_handler = JsonFileHandler(json_file_path)
    
    # 模拟从接口获取数据
    def get_data_from_api():
        """模拟从第三方接口获取股票数据"""
        # 实际项目中，这里应该是调用真实的API
        # response = requests.get("https://api.example.com/stocks")
        # return response.json()
        
        # 模拟数据
        return {
            "600000": {
                "code": "600000",
                "list": {
                    "dm": "600000",
                    "mc": "浦发银行",
                    "zf": 1.23,
                    "p": 8.25,
                    "ztp": 8.99,
                    "cje": 1500000000,
                    "lt": 350000000000,
                    "zsz": 480000000000,
                    "hs": 2.1,
                    "zs": 0,
                    "nh": "否",
                    "lb": 0.8,
                    "tj": "1/1",
                    "rx": "",
                    "hy": "银行"
                },
                "dm": "600000",
                "mc": "浦发银行",
                "zf": 1.23,
                "p": 8.25,
                "ztp": 8.99,
                "cje": 1500000000,
                "lt": 350000000000,
                "zsz": 480000000000,
                "hs": 2.1,
                "zs": 0,
                "nh": "否",
                "lb": 0.8,
                "tj": "1/1",
                "rx": "",
                "hy": "银行",
                "lastUpdated": datetime.now().isoformat() + "Z"
            },
            "600001": {
                "code": "600001",
                "list": {
                    "dm": "600001",
                    "mc": "邯郸钢铁",
                    "zf": -0.56,
                    "p": 3.58,
                    "ztp": 3.89,
                    "cje": 800000000,
                    "lt": 120000000000,
                    "zsz": 150000000000,
                    "hs": 1.8,
                    "zs": 0,
                    "nh": "否",
                    "lb": 0.5,
                    "tj": "1/0",
                    "rx": "",
                    "hy": "钢铁"
                },
                "dm": "600001",
                "mc": "邯郸钢铁",
                "zf": -0.56,
                "p": 3.58,
                "ztp": 3.89,
                "cje": 800000000,
                "lt": 120000000000,
                "zsz": 150000000000,
                "hs": 1.8,
                "zs": 0,
                "nh": "否",
                "lb": 0.5,
                "tj": "1/0",
                "rx": "",
                "hy": "钢铁",
                "lastUpdated": datetime.now().isoformat() + "Z"
            }
        }
    
    # 从接口获取数据
    print("从接口获取数据...")
    api_data = get_data_from_api()
    
    # 将数据添加到本地JSON文件
    print("将数据添加到本地JSON文件...")
    success = json_handler.update(api_data)
    
    if success:
        print("数据添加成功!")
    else:
        print("数据添加失败!")
    
    # 验证数据是否已添加
    updated_data = json_handler.read()
    print(f"更新后的数据总条目数: {len(updated_data)}")