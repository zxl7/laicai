"""
股票行情服务
"""

import json
import requests
from datetime import datetime
from typing import Dict, Any, List
from schemas.quote import StockPool, CompanyProfile, StrongStock, StrongStockPool
from src.config.config import settings


class QuoteService:
    """
    股票行情服务类
    """
    
    def get_stock_pool(self) -> StockPool:
        """
        从本地文件获取股票池数据
        
        Returns:
            StockPool: 股票池数据
        """
        try:
            # 使用绝对路径
            file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
            
            # 调试：打印文件路径
            print(f"股票池文件路径: {file_path}")
            
            # 读取JSON文件
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 调试：打印数据结构
            print(f"数据条目数: {len(data)}")
            
            # 直接返回所有原始数据，不做任何过滤或限制，保证数据的完整性
            stocks = {}
            for code, item in data.items():
                # 直接返回item的所有字段，包括code、list、lastUpdated等所有信息
                stocks[code] = item
            
            print(f"返回全部 {len(stocks)} 个股票的完整数据")
            return StockPool(total=len(stocks), stocks=stocks)
        except FileNotFoundError:
            # 如果文件不存在，返回空数据
            print(f"文件不存在: {file_path}")
            return StockPool(total=0, stocks={})
        except Exception as e:
            # 处理其他异常
            print(f"读取股票池数据失败: {e}")
            import traceback
            traceback.print_exc()
            return StockPool(total=0, stocks={})
    
    def get_company_profile(self, stock_code: str) -> List[CompanyProfile]:
        """
        根据股票代码获取上市公司简介数据
        
        Args:
            stock_code: 股票代码
            
        Returns:
            List[CompanyProfile]: 上市公司简介数据列表
        """
        try:
            # 构建API请求URL
            api_url = f"{settings.BIYING_API_HOST}/hscp/gsjj/{stock_code}/{settings.BIYING_API_TOKEN}"
            
            # 调试：打印API请求URL
            print(f"请求API URL: {api_url}")
            
            # 发送API请求
            response = requests.get(api_url, timeout=30)
            
            # 检查响应状态码
            if response.status_code != 200:
                print(f"API请求失败，状态码: {response.status_code}")
                return []
            
            # 解析JSON响应
            data = response.json()
            
            # 调试：打印API响应数据
            print(f"API响应数据: {data}")
            
            # 转换为CompanyProfile模型列表
            profiles = []
            
            # 检查API响应数据的结构
            if isinstance(data, list):
                # 情况1: data是列表
                for item in data:
                    if isinstance(item, dict):
                        try:
                            # 尝试转换为模型，处理增量兼容
                            profile = CompanyProfile(**item)
                            profiles.append(profile)
                        except TypeError as e:
                            # 处理字段不匹配的情况，跳过当前项但继续处理其他数据
                            print(f"数据转换失败，跳过该项: {e}")
                            continue
                        except Exception as e:
                            # 处理其他异常，跳过当前项但继续处理其他数据
                            print(f"处理数据时发生异常，跳过该项: {e}")
                            continue
            elif isinstance(data, dict):
                # 情况2: data是字典
                try:
                    # 尝试转换为模型，处理增量兼容
                    profile = CompanyProfile(**data)
                    profiles.append(profile)
                except TypeError as e:
                    # 处理字段不匹配的情况
                    print(f"数据转换失败: {e}")
                except Exception as e:
                    # 处理其他异常
                    print(f"处理数据时发生异常: {e}")
            
            print(f"成功获取 {len(profiles)} 条上市公司简介数据")
            
            # 更新或添加数据到stockCompanyPool.json文件
            if profiles:
                try:
                    # 读取stockCompanyPool.json文件
                    pool_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
                    with open(pool_file_path, 'r', encoding='utf-8') as f:
                        pool_data = json.load(f)
                    
                    # 使用stock_code作为键来更新或添加数据
                    for profile in profiles:
                        # 将CompanyProfile模型转换为字典
                        profile_dict = profile.dict()
                        
                        if stock_code in pool_data:
                            # 更新现有数据，保留原有字段（如list、lastUpdated等）
                            existing_data = pool_data[stock_code]
                            # 只更新CompanyProfile模型中存在的字段，不覆盖原有字段
                            for key, value in profile_dict.items():
                                if value is not None:  # 只更新非空值
                                    existing_data[key] = value
                            pool_data[stock_code] = existing_data
                            print(f"增量更新了 {stock_code} 的公司简介数据")
                        else:
                            # 添加新数据
                            pool_data[stock_code] = profile_dict
                            # 添加code字段，保持与现有数据结构一致
                            pool_data[stock_code]['code'] = stock_code
                            print(f"添加了 {stock_code} 的公司简介数据")
                    
                    # 保存更新后的数据到文件
                    with open(pool_file_path, 'w', encoding='utf-8') as f:
                        json.dump(pool_data, f, ensure_ascii=False, indent=4)
                    
                    print(f"成功更新stockCompanyPool.json文件")
                except Exception as e:
                    print(f"更新stockCompanyPool.json文件失败: {e}")
                    # 不影响正常返回，只记录错误
            
            return profiles
        except requests.exceptions.RequestException as e:
            print(f"API请求异常: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"API响应解析失败: {e}")
            return []
        except Exception as e:
            print(f"获取上市公司简介数据失败: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_strong_stock_pool(self, date: str) -> StrongStockPool:
        """
        根据日期获取强势股票池数据
        
        Args:
            date: 日期（格式yyyy-MM-dd）
            
        Returns:
            StrongStockPool: 强势股池数据
        """
        try:
            # 构建API请求URL
            api_url = f"http://api.biyingapi.com/hslt/qsgc/{date}/{settings.BIYING_API_TOKEN}"
            print(f"请求URL: {api_url}")
            
            # 发送API请求
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            
            # 解析JSON响应
            data = response.json()
            print(f"API响应数据: {data}")
            
            # 转换为StrongStock模型列表 - 保持原始数据类型
            stocks = []
            for i, item in enumerate(data):
                try:
                    # 直接使用模型转换，保持原始数据类型
                    stock = StrongStock(**item)
                    stocks.append(stock)
                except Exception as e:
                    # 记录异常但不进行过度转换
                    print(f"第 {i+1} 条数据转换失败: {e}")
                    print(f"原始数据: {item}")
                    continue
            
            print(f"成功获取 {len(stocks)} 条强势股数据")
            
            # 更新或添加数据到stockCompanyPool.json文件
            if stocks:
                try:
                    # 读取stockCompanyPool.json文件
                    pool_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
                    with open(pool_file_path, 'r', encoding='utf-8') as f:
                        pool_data = json.load(f)
                    
                    # 遍历强势股数据，更新或添加到stockCompanyPool.json
                    for stock in stocks:
                        # 将StrongStock模型转换为字典
                        stock_dict = stock.dict()
                        
                        # 从dm字段提取纯数字股票代码（去掉市场前缀如sz、sh）
                        stock_code = stock_dict['dm'][2:] if stock_dict['dm'].startswith(('sz', 'sh')) else stock_dict['dm']
                        
                        if stock_code in pool_data:
                            # 更新现有数据，保留原有字段（如list、lastUpdated等）
                            existing_data = pool_data[stock_code]
                            
                            # 更新list字段（如果存在的话）
                            if 'list' in existing_data:
                                for key, value in stock_dict.items():
                                    if value is not None:  # 只更新非空值
                                        existing_data['list'][key] = value
                            else:
                                # 如果list字段不存在，则创建它
                                existing_data['list'] = stock_dict.copy()
                            
                            # 同时更新根级字段（保持数据一致性）
                            for key, value in stock_dict.items():
                                if value is not None:  # 只更新非空值
                                    existing_data[key] = value
                            
                            # 更新lastUpdated字段
                            existing_data['lastUpdated'] = datetime.now().isoformat()
                            
                            pool_data[stock_code] = existing_data
                            print(f"增量更新了 {stock_code} 的强势股数据")
                        else:
                            # 添加新数据
                            new_data = stock_dict.copy()
                            new_data['code'] = stock_code  # 添加code字段
                            new_data['list'] = stock_dict.copy()  # 创建list字段
                            new_data['lastUpdated'] = datetime.now().isoformat()  # 添加更新时间
                            
                            pool_data[stock_code] = new_data
                            print(f"添加了 {stock_code} 的强势股数据")
                    
                    # 保存更新后的数据到文件
                    with open(pool_file_path, 'w', encoding='utf-8') as f:
                        json.dump(pool_data, f, ensure_ascii=False, indent=4)
                    
                    print(f"成功更新stockCompanyPool.json文件")
                except Exception as e:
                    print(f"更新stockCompanyPool.json文件失败: {e}")
                    import traceback
                    traceback.print_exc()
                    # 不影响正常返回，只记录错误
            
            # 构建并返回StrongStockPool对象
            return StrongStockPool(
                date=date,
                total=len(stocks),
                stocks=stocks
            )
            
        except requests.exceptions.RequestException as e:
            print(f"API请求异常: {e}")
            # 返回空的股票池，不阻拦输出
            return StrongStockPool(date=date, total=0, stocks=[])
        except json.JSONDecodeError as e:
            print(f"API响应解析失败: {e}")
            # 返回空的股票池，不阻拦输出
            return StrongStockPool(date=date, total=0, stocks=[])
        except Exception as e:
            print(f"获取强势股池数据失败: {e}")
            import traceback
            traceback.print_exc()
            # 返回空的股票池，不阻拦输出
            return StrongStockPool(date=date, total=0, stocks=[])
