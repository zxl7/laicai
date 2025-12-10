"""
测试quote模块的功能
"""

import pytest
import json
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from core.app import create_app
from services.quote import QuoteService
from config import settings


@pytest.fixture
def test_client():
    """
    创建测试客户端
    """
    app = create_app()
    with TestClient(app) as client:
        yield client


@pytest.fixture
def quote_service():
    """
    创建QuoteService实例
    """
    return QuoteService()


@pytest.fixture
def mock_company_profile_data():
    """
    模拟上市公司简介数据
    """
    return {
        "name": "平安银行",
        "ename": "PING AN BANK CO., LTD.",
        "market": "SZ",
        "idea": "银行,深成500,深圳综指,MSCI中国,深证100R,融资融券,深圳特区,深证成指,转融券标的,富时罗素,MSCI中国A股,标普道琼斯A股,养老金持股,QFII持股",
        "ldate": "1991-04-03",
        "sprice": "11.80",
        "principal": "平安证券有限责任公司",
        "rdate": "1987-12-22",
        "rprice": "1940591.0000000002",
        "instype": "股份有限公司",
        "organ": "有限责任公司",
        "secre": "周强",
        "phone": "0755-82080387",
        "sphone": "0755-82080387",
        "fax": "0755-82080323",
        "sfax": "0755-82080323",
        "email": "pab@pingan.com.cn",
        "semail": "pab@pingan.com.cn",
        "site": "http://bank.pingan.com",
        "post": "518026",
        "infosite": "http://www.cninfo.com.cn",
        "oname": "深发展A->平安银行",
        "addr": "深圳市罗湖区深南东路5047号",
        "oaddr": "深圳市罗湖区深南东路5047号",
        "desc": "平安银行股份有限公司是中国第一家面向社会公众公开发行股票并上市的商业银行。",
        "bscope": "吸收公众存款;发放短期、中期和长期贷款;办理国内外结算;办理票据承兑与贴现;发行金融债券;代理发行、代理兑付、承销政府债券;买卖政府债券、金融债券;从事同业拆借;买卖、代理买卖外汇;从事银行卡业务;提供信用证服务及担保;代理收付款项及代理保险业务;提供保管箱服务;结汇、售汇;从事离岸银行业务;资产托管业务;办理黄金业务;财务顾问、资信调查、咨询、见证业务;经国务院银行业监督管理机构等监管部门批准的其他业务。",
        "printype": "包销",
        "referrer": "平安证券有限责任公司",
        "putype": "上网定价发行",
        "pe": "12.00",
        "firgu": "45000.0",
        "lastgu": "55000.0",
        "realgu": "10000.0",
        "planm": "11800.0",
        "realm": "11800.0",
        "pubfee": "1600.0",
        "collect": "10200.0",
        "signfee": "1200.0",
        "pdate": "1991-03-26"
    }


@patch('services.quote.requests.get')
def test_get_company_profile_success(mock_get, quote_service, mock_company_profile_data):
    """
    测试成功获取上市公司简介数据
    """
    # 配置mock响应
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [mock_company_profile_data]
    mock_get.return_value = mock_response
    
    # 调用服务方法
    result = quote_service.get_company_profile("000001")
    
    # 验证结果
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].name == mock_company_profile_data["name"]
    assert result[0].ename == mock_company_profile_data["ename"]
    assert result[0].market == mock_company_profile_data["market"]
    
    # 验证请求
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert settings.BIYING_API_HOST in args[0]
    assert settings.BIYING_API_TOKEN in args[0]
    assert "000001" in args[0]


@patch('services.quote.requests.get')
def test_get_company_profile_api_error(mock_get, quote_service):
    """
    测试API请求失败的情况
    """
    # 配置mock响应
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response
    
    # 调用服务方法，应该返回空列表
    result = quote_service.get_company_profile("000001")
    assert result == []


@patch('services.quote.requests.get')
def test_get_company_profile_empty_response(mock_get, quote_service):
    """
    测试API返回空响应的情况
    """
    # 配置mock响应
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response
    
    # 调用服务方法，应该返回空列表
    result = quote_service.get_company_profile("000001")
    assert result == []


@patch('services.quote.QuoteService.get_company_profile')
def test_company_profile_endpoint(mock_get_company_profile, test_client, mock_company_profile_data):
    """
    测试公司简介API端点
    """
    from schemas.quote import CompanyProfile
    
    # 配置mock响应
    mock_get_company_profile.return_value = [CompanyProfile(**mock_company_profile_data)]
    
    # 发送请求
    response = test_client.get("/api/quote/company-profile/000001")
    
    # 验证响应
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "获取上市公司简介数据成功"
    assert json_response["data"] is not None
    assert isinstance(json_response["data"], list)
    assert len(json_response["data"]) == 1
    assert json_response["data"][0]["name"] == mock_company_profile_data["name"]
    
    # 验证服务方法被调用
    mock_get_company_profile.assert_called_once_with("000001")
