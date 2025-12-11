"""
股票行情服务
"""

import json
import requests
from datetime import datetime
from typing import Dict, Any, List
from src.schemas.quote import StockPool, CompanyProfile, StrongStock, StrongStockPool
from src.config.config import settings
from src.utils.api_client import api_client, ApiClient


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
            stock_code: 股票代码（支持带市场前缀如sz000016或纯数字如000016）
            
        Returns:
            List[CompanyProfile]: 上市公司简介数据列表
        """
        try:
            # 处理股票代码，去掉市场前缀（如sz、sh）
            clean_stock_code = stock_code[2:] if stock_code.startswith(('sz', 'sh')) else stock_code
            
            # 构建API请求URL
            api_url = f"{settings.BIYING_API_HOST}/hscp/gsjj/{clean_stock_code}/{settings.BIYING_API_TOKEN}"
            
            # 使用API客户端发送请求
            data = api_client.get(api_url)
            
            # 使用API客户端的模型映射功能，确保单个模型错误不影响整体输出
            profiles = api_client.map_to_model(data, CompanyProfile)
            
            print(f"成功获取 {len(profiles)} 条上市公司简介数据")
            
            # 更新或添加数据到stockCompanyPool.json文件
            if profiles:
                try:
                    # 读取stockCompanyPool.json文件
                    pool_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
                    with open(pool_file_path, 'r', encoding='utf-8') as f:
                        pool_data = json.load(f)
                    
                    # 使用clean_stock_code作为键来更新或添加数据，保持与股票池数据格式一致
                    for profile in profiles:
                        # 将CompanyProfile模型转换为字典
                        profile_dict = profile.dict()
                        
                        if clean_stock_code in pool_data:
                            # 更新现有数据，保留原有字段（如list、lastUpdated等）
                            existing_data = pool_data[clean_stock_code]
                            # 只更新CompanyProfile模型中存在的字段，不覆盖原有字段
                            for key, value in profile_dict.items():
                                if value is not None:  # 只更新非空值
                                    existing_data[key] = value
                            pool_data[clean_stock_code] = existing_data
                            print(f"增量更新了 {clean_stock_code} 的公司简介数据")
                        else:
                            # 添加新数据
                            pool_data[clean_stock_code] = profile_dict
                            # 添加code字段，保持与现有数据结构一致
                            pool_data[clean_stock_code]['code'] = clean_stock_code
                            print(f"添加了 {clean_stock_code} 的公司简介数据")
                    
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
            
            # 使用API客户端发送请求
            data = api_client.get(api_url)
            
            # 使用API客户端的模型映射功能，确保单个模型错误不影响整体输出
            stocks = api_client.map_to_model(data, StrongStock)
            
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
                            
                            # 创建现有数据的副本，用于比较是否发生变化
                            original_data = existing_data.copy()
                            if 'list' in original_data:
                                original_data['list'] = original_data['list'].copy()
                            
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
                            
                            # 比较数据是否发生变化，只有变化时才更新时间字段
                            if existing_data != original_data:
                                existing_data['lastUpdated'] = datetime.now().isoformat()
                                pool_data[stock_code] = existing_data
                                print(f"增量更新了 {stock_code} 的强势股数据")
                            else:
                                print(f"{stock_code} 的强势股数据未发生变化，不更新时间字段")
                        else:
                            # 添加新数据
                            new_data = stock_dict.copy()
                            new_data['code'] = stock_code  # 添加code字段
                            # 创建list字段，排除lastUpdated以避免重复设置
                            new_data['list'] = {k: v for k, v in stock_dict.items() if k != 'lastUpdated'}
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
