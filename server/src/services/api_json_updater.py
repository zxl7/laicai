"""
API数据更新服务
从第三方接口获取数据并更新本地JSON文件
"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime
from src.utils.json_utils import JsonFileHandler


class ApiJsonUpdater:
    """
    API数据更新服务类
    从第三方接口获取数据并更新本地JSON文件
    """
    
    def __init__(self, api_url: str, json_file_path: str):
        """
        初始化API数据更新服务
        
        Args:
            api_url: 第三方API的URL
            json_file_path: 本地JSON文件的绝对路径
        """
        self.api_url = api_url
        self.json_handler = JsonFileHandler(json_file_path)
    
    def fetch_data_from_api(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        从第三方接口获取数据
        
        Args:
            params: API请求参数
            
        Returns:
            Dict[str, Any]: 从API获取的数据，如果获取失败则返回空字典
        """
        try:
            # 发送GET请求
            response = requests.get(self.api_url, params=params, timeout=30)
            
            # 检查响应状态码
            if response.status_code != 200:
                print(f"API请求失败，状态码: {response.status_code}")
                return {}
            
            # 解析JSON响应
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API请求异常: {str(e)}")
            return {}
        except ValueError as e:
            print(f"API响应解析失败: {str(e)}")
            return {}
    
    def transform_data(self, api_data: Dict[str, Any], existing_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        转换API数据格式以匹配本地JSON文件的格式
        
        Args:
            api_data: 从API获取的原始数据
            existing_data: 本地已有的数据，用于比较是否发生变化
            
        Returns:
            Dict[str, Any]: 转换后的数据，符合本地JSON文件格式
        """
        transformed_data = {}
        
        # 根据实际API返回的数据格式进行转换
        # 这里假设API返回的数据格式为 {'data': {'stocks': {...}}}
        # 实际项目中需要根据真实API响应格式进行调整
        if 'data' in api_data and 'stocks' in api_data['data']:
            for code, stock_info in api_data['data']['stocks'].items():
                # 构造符合本地JSON格式的数据
                stock_data = {
                    "code": code,
                    "list": {
                        "dm": stock_info.get("dm", code),
                        "mc": stock_info.get("mc", ""),
                        "zf": stock_info.get("zf", 0.0),
                        "p": stock_info.get("p", 0.0),
                        "ztp": stock_info.get("ztp", 0.0),
                        "cje": stock_info.get("cje", 0),
                        "lt": stock_info.get("lt", 0),
                        "zsz": stock_info.get("zsz", 0),
                        "hs": stock_info.get("hs", 0.0),
                        "zs": stock_info.get("zs", 0),
                        "nh": stock_info.get("nh", "否"),
                        "lb": stock_info.get("lb", 0.0),
                        "tj": stock_info.get("tj", "0/0"),
                        "rx": stock_info.get("rx", ""),
                        "hy": stock_info.get("hy", "")
                    },
                    "dm": stock_info.get("dm", code),
                    "mc": stock_info.get("mc", ""),
                    "zf": stock_info.get("zf", 0.0),
                    "p": stock_info.get("p", 0.0),
                    "ztp": stock_info.get("ztp", 0.0),
                    "cje": stock_info.get("cje", 0),
                    "lt": stock_info.get("lt", 0),
                    "zsz": stock_info.get("zsz", 0),
                    "hs": stock_info.get("hs", 0.0),
                    "zs": stock_info.get("zs", 0),
                    "nh": stock_info.get("nh", "否"),
                    "lb": stock_info.get("lb", 0.0),
                    "tj": stock_info.get("tj", "0/0"),
                    "rx": stock_info.get("rx", ""),
                    "hy": stock_info.get("hy", "")
                }
                
                # 比较数据是否发生变化，只有变化时才更新时间字段
                if existing_data and code in existing_data:
                    # 移除lastUpdated字段后比较
                    existing_copy = existing_data[code].copy()
                    existing_copy.pop('lastUpdated', None)
                    
                    if existing_copy == stock_data:
                        # 数据未变化，保持原有时间字段
                        stock_data['lastUpdated'] = existing_data[code].get('lastUpdated', datetime.now().isoformat() + "Z")
                        print(f"{code} 的数据未发生变化，保持原有时间字段")
                    else:
                        # 数据发生变化，更新时间字段
                        stock_data['lastUpdated'] = datetime.now().isoformat() + "Z"
                        print(f"{code} 的数据发生变化，更新时间字段")
                else:
                    # 新数据，添加时间字段
                    stock_data['lastUpdated'] = datetime.now().isoformat() + "Z"
                    print(f"添加新数据 {code}，设置时间字段")
                
                transformed_data[code] = stock_data
        
        return transformed_data
    
    def update_json_file(self, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        从API获取数据并更新本地JSON文件
        
        Args:
            params: API请求参数
            
        Returns:
            bool: 更新成功返回True，失败返回False
        """
        try:
            # 从API获取数据
            print("正在从API获取数据...")
            api_data = self.fetch_data_from_api(params)
            
            if not api_data:
                print("从API获取数据失败")
                return False
            
            # 读取现有数据用于比较
            existing_data = self.json_handler.read()
            
            # 转换数据格式，传入现有数据进行比较
            print("正在转换数据格式...")
            transformed_data = self.transform_data(api_data, existing_data)
            
            if not transformed_data:
                print("数据转换失败")
                return False
            
            # 更新本地JSON文件
            print("正在更新本地JSON文件...")
            success = self.json_handler.update(transformed_data)
            
            if success:
                print(f"成功更新 {len(transformed_data)} 条数据到本地JSON文件")
            else:
                print("更新本地JSON文件失败")
            
            return success
        except Exception as e:
            print(f"更新过程异常: {str(e)}")
            return False


# 示例用法
if __name__ == "__main__":
    """
    示例：使用ApiJsonUpdater从接口获取数据并更新本地JSON文件
    """
    # API URL (实际项目中替换为真实URL)
    api_url = "https://api.example.com/stocks"
    
    # 本地JSON文件路径
    json_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
    
    # 初始化API数据更新服务
    updater = ApiJsonUpdater(api_url, json_file_path)
    
    # API请求参数（可选）
    params = {
        "type": "stock",
        "limit": 10
    }
    
    # 更新本地JSON文件
    updater.update_json_file(params)
