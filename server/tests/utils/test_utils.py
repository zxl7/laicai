"""
测试工具函数
"""

from unittest.mock import MagicMock, patch
from typing import Dict, Any


def mock_akshare_stock_data(stock_data: Dict[str, Any]):
    """
    模拟akshare的股票数据返回
    
    Args:
        stock_data: 模拟的股票数据
    
    Returns:
        MagicMock: 模拟的DataFrame对象
    """
    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.iloc = MagicMock(return_value=MagicMock(to_dict=MagicMock(return_value=stock_data)))
    mock_df.__getitem__.return_value = mock_df
    mock_df['代码'] = [stock_data['代码']]
    return mock_df


def patch_akshare(func_name: str, return_value=None, side_effect=None):
    """
    补丁akshare的指定函数
    
    Args:
        func_name: 要补丁的函数名，如"stock_zh_a_spot_em"
        return_value: 返回值
        side_effect: 副作用
    
    Returns:
        patch: 补丁对象
    """
    return patch(f"akshare.{func_name}", return_value=return_value, side_effect=side_effect)


def assert_response_success(response, expected_data=None):
    """
    断言响应成功
    
    Args:
        response: FastAPI响应对象
        expected_data: 期望的数据
    """
    assert response.status_code == 200
    response_data = response.json()
    assert "code" in response_data
    assert "message" in response_data
    assert "data" in response_data
    
    if expected_data:
        assert response_data["data"] == expected_data


def assert_response_error(response, expected_status_code=400, expected_code=None):
    """
    断言响应错误
    
    Args:
        response: FastAPI响应对象
        expected_status_code: 期望的状态码
        expected_code: 期望的错误代码
    """
    assert response.status_code == expected_status_code
    response_data = response.json()
    assert "code" in response_data
    assert "message" in response_data
    
    if expected_code:
        assert response_data["code"] == expected_code