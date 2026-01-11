"""
股票行情服务
"""

import json
import requests
from datetime import datetime, timedelta, time
from typing import Dict, Any, List, Type
from src.schemas.quote import StockPool, CompanyProfile, StrongStock, StrongStockPool, ZTStock, DTStock, ZTStockPool, DTStockPool
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
                    
                    # 删除成交额小于5亿的数据
                    filtered_data = {}
                    for code, stock in pool_data.items():
                        # 检查股票数据中是否有成交额字段，且是否大于等于5亿
                        cje = stock.get('cje', 0) or stock.get('list', {}).get('cje', 0)
                        if cje >= 500000000:  # 5亿 = 500,000,000
                            filtered_data[code] = stock
                        else:
                            print(f"删除 {code} ({stock.get('mc', '')})：成交额 {cje} 小于5亿")
                    
                    # 保存过滤后的数据到文件
                    with open(pool_file_path, 'w', encoding='utf-8') as f:
                        json.dump(filtered_data, f, ensure_ascii=False, indent=4)
                    
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
            today = datetime.now().strftime("%Y-%m-%d")
            api_url = f"http://api.biyingapi.com/hslt/qsgc/{date}/{settings.BIYING_API_TOKEN}"
            print(f"请求URL: {api_url}")
            data = api_client.get(api_url)
            stocks = api_client.map_to_model(data, StrongStock)
            print(f"成功获取 {len(stocks)} 条强势股数据")
            if stocks:
                # 仅当请求当天数据时更新stockCompanyPool.json，避免历史数据污染
                if date == today:
                    try:
                        pool_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
                        with open(pool_file_path, 'r', encoding='utf-8') as f:
                            pool_data = json.load(f)
                        for stock in stocks:
                            stock_dict = stock.dict()
                            stock_code = stock_dict['dm'][2:] if stock_dict['dm'].startswith(('sz', 'sh')) else stock_dict['dm']
                            if stock_code in pool_data:
                                existing_data = pool_data[stock_code]
                                original_data = existing_data.copy()
                                if 'list' in original_data:
                                    original_data['list'] = original_data['list'].copy()
                                if 'list' in existing_data:
                                    for key, value in stock_dict.items():
                                        if value is not None:
                                            existing_data['list'][key] = value
                                else:
                                    existing_data['list'] = stock_dict.copy()
                                for key, value in stock_dict.items():
                                    if value is not None:
                                        existing_data[key] = value
                                if existing_data != original_data:
                                    existing_data['lastUpdated'] = datetime.now().isoformat()
                                    pool_data[stock_code] = existing_data
                                    print(f"增量更新了 {stock_code} 的强势股数据")
                                else:
                                    print(f"{stock_code} 的强势股数据未发生变化，不更新时间字段")
                            else:
                                new_data = stock_dict.copy()
                                new_data['code'] = stock_code
                                new_data['list'] = {k: v for k, v in stock_dict.items() if k != 'lastUpdated'}
                                new_data['lastUpdated'] = datetime.now().isoformat()
                                pool_data[stock_code] = new_data
                                print(f"添加了 {stock_code} 的强势股数据")
                        filtered_data = {}
                        for code, stock in pool_data.items():
                            cje = stock.get('cje', 0) or stock.get('list', {}).get('cje', 0)
                            if cje >= 500000000:
                                filtered_data[code] = stock
                            else:
                                print(f"删除 {code} ({stock.get('mc', '')})：成交额 {cje} 小于5亿")
                        with open(pool_file_path, 'w', encoding='utf-8') as f:
                            json.dump(filtered_data, f, ensure_ascii=False, indent=4)
                        print(f"成功更新stockCompanyPool.json文件")
                    except Exception as e:
                        print(f"更新stockCompanyPool.json文件失败: {e}")
                        import traceback
                        traceback.print_exc()
            
            if stocks:
                try:
                        qsgc_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/QSGC.json"
                        qsgc_data = {}
                        try:
                            with open(qsgc_file_path, 'r', encoding='utf-8') as f:
                                qsgc_data = json.load(f)
                        except FileNotFoundError:
                            pass
                        
                        # 使用请求的日期作为key保存数据
                        qsgc_data[date] = {
                            "total": len(stocks),
                            "stocks": [stock.dict() for stock in stocks],
                            "updateTime": datetime.now().isoformat()
                        }
                        
                        # 仅当请求当天数据时清理过期数据
                        if date == today:
                            try:
                                today_dt = datetime.strptime(today, "%Y-%m-%d")
                                dates_to_keep = []
                                for data_date in qsgc_data.keys():
                                    try:
                                        date_obj = datetime.strptime(data_date, "%Y-%m-%d")
                                        if 0 <= (today_dt - date_obj).days < 3:
                                            dates_to_keep.append(data_date)
                                    except ValueError:
                                        continue
                                cleaned_qsgc_data = {d: qsgc_data[d] for d in dates_to_keep}
                                with open(qsgc_file_path, 'w', encoding='utf-8') as f:
                                    json.dump(cleaned_qsgc_data, f, ensure_ascii=False, indent=4)
                                print(f"成功更新QSGC.json文件，保留了 {len(cleaned_qsgc_data)} 天的数据")
                            except Exception as e:
                                print(f"清理过期数据失败: {e}")
                                with open(qsgc_file_path, 'w', encoding='utf-8') as f:
                                    json.dump(qsgc_data, f, ensure_ascii=False, indent=4)
                        else:
                            # 非当天数据，直接保存，不清理
                            with open(qsgc_file_path, 'w', encoding='utf-8') as f:
                                json.dump(qsgc_data, f, ensure_ascii=False, indent=4)
                            print(f"成功更新QSGC.json文件，保存了 {date} 的数据")
                            
                except Exception as e:
                    print(f"更新QSGC.json文件失败: {e}")
                    import traceback
                    traceback.print_exc()
                return StrongStockPool(date=date, total=len(stocks), stocks=stocks)
            
            # API失败，降级逻辑
            file_path = "/Users/zxl/Desktop/laicai/server/DataBase/QSGC.json"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    qsgc_data = json.load(f)
                if date in qsgc_data:
                    entry = qsgc_data[date]
                    stocks = [StrongStock(**s) for s in entry.get("stocks", [])]
                    return StrongStockPool(date=date, total=entry.get("total", len(stocks)), stocks=stocks)
                else:
                    keys = []
                    for d in qsgc_data.keys():
                        try:
                            keys.append(datetime.strptime(d, "%Y-%m-%d"))
                        except ValueError:
                            continue
                    if not keys:
                        return StrongStockPool(date=date, total=0, stocks=[])
                    latest = max(keys).strftime("%Y-%m-%d")
                    entry = qsgc_data.get(latest, {"stocks": [], "total": 0})
                    stocks = [StrongStock(**s) for s in entry.get("stocks", [])]
                    return StrongStockPool(date=latest, total=entry.get("total", len(stocks)), stocks=stocks)
            except FileNotFoundError:
                print(f"文件不存在: {file_path}")
                return StrongStockPool(date=date, total=0, stocks=[])
        except requests.exceptions.RequestException as e:
            print(f"API请求异常: {e}")
            return StrongStockPool(date=date, total=0, stocks=[])
        
        
    
    def get_zt_stock_pool(self, date: str) -> ZTStockPool:
        """
        根据日期获取涨停股票池数据
        
        Args:
            date: 日期（格式yyyy-MM-dd）
            
        Returns:
            ZTStockPool: 涨停股池数据
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            api_url = f"http://api.biyingapi.com/hslt/ztgc/{date}/{settings.BIYING_API_TOKEN}"
            print(f"请求URL: {api_url}")
            data = api_client.get(api_url)
            stocks = api_client.map_to_model(data, ZTStock)
            print(f"成功获取 {len(stocks)} 条涨停股数据")
            if stocks:
                # 仅当请求当天数据时更新stockCompanyPool.json
                if date == today:
                    try:
                        pool_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
                        with open(pool_file_path, 'r', encoding='utf-8') as f:
                            pool_data = json.load(f)
                        for stock in stocks:
                            stock_dict = stock.dict()
                            stock_code = stock_dict['dm'][2:] if stock_dict['dm'].startswith(('sz', 'sh')) else stock_dict['dm']
                            if stock_code in pool_data:
                                existing_data = pool_data[stock_code]
                                original_data = existing_data.copy()
                                if 'list' in original_data:
                                    original_data['list'] = original_data['list'].copy()
                                if 'list' in existing_data:
                                    for key, value in stock_dict.items():
                                        if value is not None:
                                            existing_data['list'][key] = value
                                else:
                                    existing_data['list'] = stock_dict.copy()
                                for key, value in stock_dict.items():
                                    if value is not None:
                                        existing_data[key] = value
                                if existing_data != original_data:
                                    existing_data['lastUpdated'] = datetime.now().isoformat()
                                    pool_data[stock_code] = existing_data
                                    print(f"增量更新了 {stock_code} 的涨停股数据")
                                else:
                                    print(f"{stock_code} 的涨停股数据未发生变化，不更新时间字段")
                            else:
                                new_data = stock_dict.copy()
                                new_data['code'] = stock_code
                                new_data['list'] = {k: v for k, v in stock_dict.items() if k != 'lastUpdated'}
                                new_data['lastUpdated'] = datetime.now().isoformat()
                                pool_data[stock_code] = new_data
                                print(f"添加了 {stock_code} 的涨停股数据")
                        filtered_data = {}
                        for code, stock in pool_data.items():
                            cje = stock.get('cje', 0) or stock.get('list', {}).get('cje', 0)
                            if cje >= 500000000:
                                filtered_data[code] = stock
                            else:
                                print(f"删除 {code} ({stock.get('mc', '')})：成交额 {cje} 小于5亿")
                        with open(pool_file_path, 'w', encoding='utf-8') as f:
                            json.dump(filtered_data, f, ensure_ascii=False, indent=4)
                        print(f"成功更新stockCompanyPool.json文件")
                    except Exception as e:
                        print(f"更新stockCompanyPool.json文件失败: {e}")
                        import traceback
                        traceback.print_exc()
            
            if stocks:
                try:
                        ztgc_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/ZTGC.json"
                        ztgc_data = {}
                        try:
                            with open(ztgc_file_path, 'r', encoding='utf-8') as f:
                                ztgc_data = json.load(f)
                        except FileNotFoundError:
                            pass
                        
                        # 使用请求的日期作为key
                        ztgc_data[date] = {
                            "total": len(stocks),
                            "stocks": [stock.dict() for stock in stocks],
                            "updateTime": datetime.now().isoformat()
                        }
                        
                        # 仅当请求当天数据时清理过期数据
                        if date == today:
                            today_dt = datetime.strptime(today, "%Y-%m-%d")
                            cutoff_date = today_dt - timedelta(days=5)
                            dates_to_keep = []
                            for data_date in ztgc_data.keys():
                                try:
                                    date_obj = datetime.strptime(data_date, "%Y-%m-%d")
                                    if date_obj >= cutoff_date:
                                        dates_to_keep.append(data_date)
                                except ValueError:
                                    continue
                            cleaned_ztgc_data = {d: ztgc_data[d] for d in dates_to_keep}
                            with open(ztgc_file_path, 'w', encoding='utf-8') as f:
                                json.dump(cleaned_ztgc_data, f, ensure_ascii=False, indent=4)
                            print(f"成功更新ZTGC.json文件，保留了 {len(cleaned_ztgc_data)} 天的数据")
                        else:
                            with open(ztgc_file_path, 'w', encoding='utf-8') as f:
                                json.dump(ztgc_data, f, ensure_ascii=False, indent=4)
                            print(f"成功更新ZTGC.json文件，保存了 {date} 的数据")
                            
                except Exception as e:
                    print(f"更新ZTGC.json文件失败: {e}")
                    import traceback
                    traceback.print_exc()
                return ZTStockPool(date=date, total=len(stocks), stocks=stocks)
            
            # API失败，降级逻辑
            file_path = "/Users/zxl/Desktop/laicai/server/DataBase/ZTGC.json"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    ztgc_data = json.load(f)
                if date in ztgc_data:
                    entry = ztgc_data[date]
                    stocks = [ZTStock(**s) for s in entry.get("stocks", [])]
                    return ZTStockPool(date=date, total=entry.get("total", len(stocks)), stocks=stocks)
                else:
                    keys = []
                    for d in ztgc_data.keys():
                        try:
                            keys.append(datetime.strptime(d, "%Y-%m-%d"))
                        except ValueError:
                            continue
                    if not keys:
                        return ZTStockPool(date=date, total=0, stocks=[])
                    latest = max(keys).strftime("%Y-%m-%d")
                    entry = ztgc_data.get(latest, {"stocks": [], "total": 0})
                    stocks = [ZTStock(**s) for s in entry.get("stocks", [])]
                    return ZTStockPool(date=latest, total=entry.get("total", len(stocks)), stocks=stocks)
            except FileNotFoundError:
                print(f"文件不存在: {file_path}")
                return ZTStockPool(date=date, total=0, stocks=[])
        except requests.exceptions.RequestException as e:
            print(f"API请求异常: {e}")
            return ZTStockPool(date=date, total=0, stocks=[])
        except json.JSONDecodeError as e:
            print(f"API响应解析失败: {e}")
            return ZTStockPool(date=date, total=0, stocks=[])
        except Exception as e:
            print(f"获取涨停股池数据失败: {e}")
            import traceback
            traceback.print_exc()
            return ZTStockPool(date=date, total=0, stocks=[])
    
    def get_dt_stock_pool(self, date: str) -> DTStockPool:
        """
        根据日期获取跌停股票池数据
        
        Args:
            date: 日期（格式yyyy-MM-dd）
            
        Returns:
            DTStockPool: 跌停股池数据
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            api_url = f"http://api.biyingapi.com/hslt/dtgc/{date}/{settings.BIYING_API_TOKEN}"
            print(f"请求URL: {api_url}")
            data = api_client.get(api_url)
            stocks = api_client.map_to_model(data, DTStock)
            print(f"成功获取 {len(stocks)} 条跌停股数据")
            if stocks:
                # 仅当请求当天数据时更新stockCompanyPool.json
                if date == today:
                    try:
                        pool_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"
                        with open(pool_file_path, 'r', encoding='utf-8') as f:
                            pool_data = json.load(f)
                        for stock in stocks:
                            stock_dict = stock.dict()
                            stock_code = stock_dict['dm'][2:] if stock_dict['dm'].startswith(('sz', 'sh')) else stock_dict['dm']
                            if stock_code in pool_data:
                                existing_data = pool_data[stock_code]
                                original_data = existing_data.copy()
                                if 'list' in original_data:
                                    original_data['list'] = original_data['list'].copy()
                                if 'list' in existing_data:
                                    for key, value in stock_dict.items():
                                        if value is not None:
                                            existing_data['list'][key] = value
                                else:
                                    existing_data['list'] = stock_dict.copy()
                                for key, value in stock_dict.items():
                                    if value is not None:
                                        existing_data[key] = value
                                if existing_data != original_data:
                                    existing_data['lastUpdated'] = datetime.now().isoformat()
                                    pool_data[stock_code] = existing_data
                                    print(f"增量更新了 {stock_code} 的跌停股数据")
                                else:
                                    print(f"{stock_code} 的跌停股数据未发生变化，不更新时间字段")
                            else:
                                new_data = stock_dict.copy()
                                new_data['code'] = stock_code
                                new_data['list'] = {k: v for k, v in stock_dict.items() if k != 'lastUpdated'}
                                new_data['lastUpdated'] = datetime.now().isoformat()
                                pool_data[stock_code] = new_data
                                print(f"添加了 {stock_code} 的跌停股数据")
                        filtered_data = {}
                        for code, stock in pool_data.items():
                            cje = stock.get('cje', 0) or stock.get('list', {}).get('cje', 0)
                            if cje >= 500000000:
                                filtered_data[code] = stock
                            else:
                                print(f"删除 {code} ({stock.get('mc', '')})：成交额 {cje} 小于5亿")
                        with open(pool_file_path, 'w', encoding='utf-8') as f:
                            json.dump(filtered_data, f, ensure_ascii=False, indent=4)
                        print(f"成功更新stockCompanyPool.json文件")
                    except Exception as e:
                        print(f"更新stockCompanyPool.json文件失败: {e}")
                        import traceback
                        traceback.print_exc()
            
            if stocks:
                try:
                        dtgc_file_path = "/Users/zxl/Desktop/laicai/server/DataBase/DTGC.json"
                        dtgc_data = {}
                        try:
                            with open(dtgc_file_path, 'r', encoding='utf-8') as f:
                                dtgc_data = json.load(f)
                        except FileNotFoundError:
                            pass
                        
                        # 使用请求的日期作为key
                        dtgc_data[date] = {
                            "total": len(stocks),
                            "stocks": [stock.dict() for stock in stocks],
                            "updateTime": datetime.now().isoformat()
                        }
                        
                        # 仅当请求当天数据时清理过期数据
                        if date == today:
                            today_dt = datetime.strptime(today, "%Y-%m-%d")
                            cutoff_date = today_dt - timedelta(days=5)
                            dates_to_keep = []
                            for data_date in dtgc_data.keys():
                                try:
                                    date_obj = datetime.strptime(data_date, "%Y-%m-%d")
                                    if date_obj >= cutoff_date:
                                        dates_to_keep.append(data_date)
                                except ValueError:
                                    continue
                            cleaned_dtgc_data = {d: dtgc_data[d] for d in dates_to_keep}
                            with open(dtgc_file_path, 'w', encoding='utf-8') as f:
                                json.dump(cleaned_dtgc_data, f, ensure_ascii=False, indent=4)
                            print(f"成功更新DTGC.json文件，保留了 {len(cleaned_dtgc_data)} 天的数据")
                        else:
                            with open(dtgc_file_path, 'w', encoding='utf-8') as f:
                                json.dump(dtgc_data, f, ensure_ascii=False, indent=4)
                            print(f"成功更新DTGC.json文件，保存了 {date} 的数据")
                            
                except Exception as e:
                    print(f"更新DTGC.json文件失败: {e}")
                    import traceback
                    traceback.print_exc()
                return DTStockPool(date=date, total=len(stocks), stocks=stocks)
            
            # API失败或无数据，降级逻辑
            file_path = "/Users/zxl/Desktop/laicai/server/DataBase/DTGC.json"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    dtgc_data = json.load(f)
                if date in dtgc_data:
                    entry = dtgc_data[date]
                    stocks = [DTStock(**s) for s in entry.get("stocks", [])]
                    return DTStockPool(date=date, total=entry.get("total", len(stocks)), stocks=stocks)
                else:
                    keys = []
                    for d in dtgc_data.keys():
                        try:
                            keys.append(datetime.strptime(d, "%Y-%m-%d"))
                        except ValueError:
                            continue
                    if not keys:
                        return DTStockPool(date=date, total=0, stocks=[])
                    latest = max(keys).strftime("%Y-%m-%d")
                    entry = dtgc_data.get(latest, {"stocks": [], "total": 0})
                    stocks = [DTStock(**s) for s in entry.get("stocks", [])]
                    return DTStockPool(date=latest, total=entry.get("total", len(stocks)), stocks=stocks)
            except FileNotFoundError:
                print(f"文件不存在: {file_path}")
                return DTStockPool(date=date, total=0, stocks=[])
                
        except requests.exceptions.RequestException as e:
            print(f"API请求异常: {e}")
            return DTStockPool(date=date, total=0, stocks=[])
        except json.JSONDecodeError as e:
            print(f"API响应解析失败: {e}")
            return DTStockPool(date=date, total=0, stocks=[])
        except Exception as e:
            print(f"获取跌停股池数据失败: {e}")
            import traceback
            traceback.print_exc()
            return DTStockPool(date=date, total=0, stocks=[])

    def is_trading_time(self) -> bool:
        now = datetime.now()
        if now.weekday() >= 5:
            return False
        morning_start = time(9, 30)
        morning_end = time(11, 30)
        afternoon_start = time(13, 0)
        afternoon_end = time(15, 0)
        t = now.time()
        return (morning_start <= t < morning_end) or (afternoon_start <= t < afternoon_end)
