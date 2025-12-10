"""
第三方API客户端封装
提供统一的API调用接口，确保模型错误不影响整体输出
"""

import requests
import logging
from typing import Any, List, TypeVar, Generic, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 泛型类型变量
T = TypeVar('T', bound=BaseModel)

class ApiClient:
    """
    第三方API客户端封装类
    提供统一的API调用接口，确保模型错误不影响整体输出
    """
    
    def __init__(self, base_url: Optional[str] = None, timeout: int = 10):
        """
        初始化API客户端
        
        Args:
            base_url: 基础API URL
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """
        发送GET请求
        
        Args:
            endpoint: API端点
            params: 请求参数
            **kwargs: 其他请求参数
            
        Returns:
            Any: API响应数据
        """
        url = f"{self.base_url}/{endpoint}" if self.base_url else endpoint
        try:
            response = self.session.get(url, params=params, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {e}")
            logger.error(f"请求URL: {url}")
            return []
        except Exception as e:
            logger.error(f"API响应处理失败: {e}")
            logger.error(f"请求URL: {url}")
            return []
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """
        发送POST请求
        
        Args:
            endpoint: API端点
            data: 表单数据
            json: JSON数据
            **kwargs: 其他请求参数
            
        Returns:
            Any: API响应数据
        """
        url = f"{self.base_url}/{endpoint}" if self.base_url else endpoint
        try:
            response = self.session.post(url, data=data, json=json, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {e}")
            logger.error(f"请求URL: {url}")
            return {}
        except Exception as e:
            logger.error(f"API响应处理失败: {e}")
            logger.error(f"请求URL: {url}")
            return {}
    
    def map_to_model(self, data: Any, model_class: Generic[T]) -> List[T]:
        """
        将API响应数据映射到Pydantic模型列表
        单个模型错误不会影响整体输出
        
        Args:
            data: API响应数据
            model_class: Pydantic模型类
            
        Returns:
            List[T]: 模型列表
        """
        models = []
        
        # 确保数据是可迭代的
        if not isinstance(data, (list, tuple)):
            data = [data]
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                logger.warning(f"第 {i+1} 项数据不是字典类型: {type(item).__name__}")
                continue
            
            try:
                # 尝试创建模型实例，保持原始数据类型
                model_instance = model_class(**item)
                models.append(model_instance)
            except Exception as e:
                # 记录详细错误信息但不中断处理
                logger.error(f"第 {i+1} 条数据转换失败: {e}")
                logger.debug(f"原始数据: {item}")
                # 不要中断处理，继续转换其他数据
                continue
        
        logger.info(f"成功转换 {len(models)} 条数据，失败 {len(data) - len(models)} 条")
        return models
    
    def close(self):
        """
        关闭会话
        """
        self.session.close()

# 创建全局API客户端实例
api_client = ApiClient()
