"""
测试配置文件
"""

import pytest
from fastapi.testclient import TestClient
from laicai.core.app import create_app
from laicai.core.config import settings


@pytest.fixture(scope="session")
def test_client():
    """
    创建测试客户端
    
    Returns:
        TestClient: FastAPI测试客户端
    """
    app = create_app()
    return TestClient(app)


@pytest.fixture(scope="session")
def mock_quote_data():
    """
    模拟股票行情数据
    
    Returns:
        dict: 模拟的股票行情数据
    """
    return {
        "symbol": "000001.SZ",
        "name": "平安银行",
        "price": 15.80,
        "change": 10.03,
        "change_amount": 1.44,
        "volume": 150000000,
        "amount": 2370000000,
        "turnover": 1.5,
        "amplitude": 8.32,
        "high": 15.80,
        "low": 14.36,
        "open": 14.70,
        "prev_close": 14.36,
        "market_cap": 350000000000,
        "circulating_cap": 350000000000,
        "pe": 7.8,
        "pb": 0.85
    }


@pytest.fixture(scope="session")
def mock_limit_up_stocks():
    """
    模拟涨停股票数据
    
    Returns:
        dict: 模拟的涨停股票数据
    """
    return {
        "total": 2,
        "stocks": [
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
    }