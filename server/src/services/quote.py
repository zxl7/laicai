"""
股票行情服务
"""

import akshare as ak
import json
import os
from typing import List, Dict, Any
from schemas.quote import StockQuote, LimitUpStocks, LimitDownStocks, FailedLimitUpStocks, StrongStocks, StockPool, StockPoolItem


class QuoteService:
    """
    股票行情服务类
    """
    
    def get_current_quote(self, symbol: str) -> StockQuote:
        """
        获取单个股票的实时行情数据
        
        Args:
            symbol: 股票代码，如"000001.SZ"
        
        Returns:
            StockQuote: 股票实时行情数据
        """
        # 使用akshare获取股票实时行情
        stock_zh_a_spot_df = ak.stock_zh_a_spot_em()
        
        # 查找指定股票代码的数据
        stock_data = stock_zh_a_spot_df[stock_zh_a_spot_df['代码'] == symbol]
        
        if stock_data.empty:
            # 如果找不到数据，返回模拟数据
            return self._get_mock_quote(symbol)
        
        # 转换为字典
        data = stock_data.iloc[0].to_dict()
        
        # 构建返回数据
        return StockQuote(
            symbol=data['代码'],
            name=data['名称'],
            price=data['最新价'],
            change=data['涨跌幅'],
            change_amount=data['涨跌额'],
            volume=data['成交量'],
            amount=data['成交额'],
            turnover=data['换手率'],
            amplitude=data['振幅'],
            high=data['最高'],
            low=data['最低'],
            open=data['今开'],
            prev_close=data['昨收'],
            market_cap=data['总市值'],
            circulating_cap=data['流通市值'],
            pe=data['市盈率-动态'],
            pb=data['市净率']
        )
    
    def get_limit_up_stocks(self) -> LimitUpStocks:
        """
        获取所有涨停股票
        
        Returns:
            LimitUpStocks: 涨停股票列表
        """
        # 使用akshare获取涨停股票数据
        try:
            limit_up_stocks_df = ak.stock_zt_pool_em()
        except Exception:
            # 如果API调用失败，返回模拟数据
            return self._get_mock_limit_up_stocks()
        
        # 转换为列表
        stocks = []
        for _, row in limit_up_stocks_df.iterrows():
            stocks.append({
                "symbol": row['代码'],
                "name": row['名称'],
                "price": row['最新价'],
                "change": row['涨跌幅'],
                "change_amount": row['涨跌额'],
                "volume": row['成交量'],
                "amount": row['成交额'],
                "open_time": row['涨停时间']
            })
        
        return LimitUpStocks(total=len(stocks), stocks=stocks)
    
    def get_limit_down_stocks(self) -> LimitDownStocks:
        """
        获取所有跌停股票
        
        Returns:
            LimitDownStocks: 跌停股票列表
        """
        # 使用akshare获取股票数据并筛选跌停股票
        try:
            stock_zh_a_spot_df = ak.stock_zh_a_spot_em()
            # 筛选跌幅接近或等于10%的股票（考虑ST股票5%的涨跌幅限制）
            limit_down_stocks_df = stock_zh_a_spot_df[(stock_zh_a_spot_df['涨跌幅'] <= -9.9) | \
                                                    (stock_zh_a_spot_df['涨跌幅'] <= -4.9) & \
                                                    (stock_zh_a_spot_df['名称'].str.contains('ST'))]
        except Exception:
            # 如果API调用失败，返回模拟数据
            return self._get_mock_limit_down_stocks()
        
        # 转换为列表
        stocks = []
        for _, row in limit_down_stocks_df.iterrows():
            stocks.append({
                "symbol": row['代码'],
                "name": row['名称'],
                "price": row['最新价'],
                "change": row['涨跌幅'],
                "change_amount": row['涨跌额'],
                "volume": row['成交量'],
                "amount": row['成交额']
            })
        
        return LimitDownStocks(total=len(stocks), stocks=stocks)
    
    def get_failed_limit_up_stocks(self) -> FailedLimitUpStocks:
        """
        获取所有炸板股票
        
        Returns:
            FailedLimitUpStocks: 炸板股票列表
        """
        # 使用akshare获取炸板股票数据
        try:
            failed_limit_up_stocks_df = ak.stock_zb_pool_em()
        except Exception:
            # 如果API调用失败，返回模拟数据
            return self._get_mock_failed_limit_up_stocks()
        
        # 转换为列表
        stocks = []
        for _, row in failed_limit_up_stocks_df.iterrows():
            stocks.append({
                "symbol": row['代码'],
                "name": row['名称'],
                "price": row['最新价'],
                "change": row['涨跌幅'],
                "change_amount": row['涨跌额'],
                "volume": row['成交量'],
                "amount": row['成交额'],
                "high": row['最高'],
                "limit_up_time": row['开板次数']
            })
        
        return FailedLimitUpStocks(total=len(stocks), stocks=stocks)
    
    def get_strong_stocks(self) -> StrongStocks:
        """
        获取强势股票池
        
        Returns:
            StrongStocks: 强势股票列表
        """
        # 使用akshare获取强势股票数据
        try:
            strong_stocks_df = ak.stock_qsgc_strong_pool_em()
        except Exception:
            # 如果API调用失败，返回模拟数据
            return self._get_mock_strong_stocks()
        
        # 转换为列表
        stocks = []
        for _, row in strong_stocks_df.iterrows():
            stocks.append({
                "symbol": row['代码'],
                "name": row['名称'],
                "price": row['最新价'],
                "change": row['涨跌幅'],
                "change_amount": row['涨跌额'],
                "volume": row['成交量'],
                "amount": row['成交额']
            })
        
        return StrongStocks(total=len(stocks), stocks=stocks)
    
    def _get_mock_quote(self, symbol: str) -> StockQuote:
        """
        获取模拟的股票行情数据
        
        Args:
            symbol: 股票代码
        
        Returns:
            StockQuote: 模拟的股票行情数据
        """
        return StockQuote(
            symbol=symbol,
            name="模拟股票",
            price=10.00,
            change=5.23,
            change_amount=0.50,
            volume=1000000,
            amount=10000000,
            turnover=1.5,
            amplitude=8.32,
            high=10.50,
            low=9.68,
            open=9.80,
            prev_close=9.50,
            market_cap=1000000000,
            circulating_cap=800000000,
            pe=20.5,
            pb=2.1
        )
    
    def _get_mock_limit_up_stocks(self) -> LimitUpStocks:
        """
        获取模拟的涨停股票数据
        
        Returns:
            LimitUpStocks: 模拟的涨停股票列表
        """
        stocks = [
            {
                "symbol": "000001.SZ",
                "name": "平安银行",
                "price": 15.80,
                "change": 10.03,
                "change_amount": 1.44,
                "volume": 150000000,
                "amount": 2370000000,
                "open_time": "09:30:00"
            },
            {
                "symbol": "600036.SH",
                "name": "招商银行",
                "price": 38.90,
                "change": 10.01,
                "change_amount": 3.54,
                "volume": 80000000,
                "amount": 3112000000,
                "open_time": "09:35:20"
            }
        ]
        return LimitUpStocks(total=2, stocks=stocks)
    
    def _get_mock_limit_down_stocks(self) -> LimitDownStocks:
        """
        获取模拟的跌停股票数据
        
        Returns:
            LimitDownStocks: 模拟的跌停股票列表
        """
        stocks = [
            {
                "symbol": "002007.SZ",
                "name": "华兰生物",
                "price": 28.50,
                "change": -9.98,
                "change_amount": -3.17,
                "volume": 30000000,
                "amount": 855000000
            },
            {
                "symbol": "600519.SH",
                "name": "贵州茅台",
                "price": 1780.00,
                "change": -4.99,
                "change_amount": -93.50,
                "volume": 1200000,
                "amount": 2136000000
            }
        ]
        return LimitDownStocks(total=2, stocks=stocks)
    
    def _get_mock_failed_limit_up_stocks(self) -> FailedLimitUpStocks:
        """
        获取模拟的炸板股票数据
        
        Returns:
            FailedLimitUpStocks: 模拟的炸板股票列表
        """
        stocks = [
            {
                "symbol": "000002.SZ",
                "name": "万科A",
                "price": 14.20,
                "change": 8.23,
                "change_amount": 1.08,
                "volume": 120000000,
                "amount": 1704000000,
                "high": 14.58,
                "limit_up_time": 3
            },
            {
                "symbol": "600048.SH",
                "name": "保利发展",
                "price": 15.80,
                "change": 7.52,
                "change_amount": 1.11,
                "volume": 90000000,
                "amount": 1422000000,
                "high": 16.23,
                "limit_up_time": 2
            }
        ]
        return FailedLimitUpStocks(total=2, stocks=stocks)
    
    def _get_mock_strong_stocks(self) -> StrongStocks:
        """
        获取模拟的强势股票数据
        
        Returns:
            StrongStocks: 模拟的强势股票列表
        """
        stocks = [
            {
                "symbol": "000858.SZ",
                "name": "五粮液",
                "price": 185.00,
                "change": 7.89,
                "change_amount": 13.50,
                "volume": 15000000,
                "amount": 2775000000
            },
            {
                "symbol": "002415.SZ",
                "name": "海康威视",
                "price": 38.90,
                "change": 6.23,
                "change_amount": 2.25,
                "volume": 25000000,
                "amount": 972500000
            }
        ]
        return StrongStocks(total=2, stocks=stocks)
    
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
            
            # 直接返回所有原始数据，不做模型验证，保证不丢失任何数据
            stocks = {}
            for code, item in data.items():
                # 直接使用原始数据，即使没有'list'字段
                stocks[code] = item.get("list", {})
            
            print(f"返回全部 {len(stocks)} 个股票数据")
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