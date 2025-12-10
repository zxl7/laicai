"""
测试API客户端封装
验证模型错误是否会影响整体输出
"""

from datetime import datetime
from pydantic import BaseModel
from typing import Union
from src.utils.api_client import ApiClient

# 定义测试模型
class TestModel(BaseModel):
    id: int
    name: str
    value: Union[float, str]  # 支持多种类型
    created_at: datetime

# 创建API客户端实例
api_client = ApiClient(timeout=5)

# 模拟第三方API返回的数据（包含错误数据）
simulated_api_data = [
    {"id": 1, "name": "正常数据1", "value": 100.5, "created_at": "2023-01-01T12:00:00"},
    {"id": 2, "name": "正常数据2", "value": "200.75", "created_at": "2023-01-02T13:30:00"},
    {"id": "3", "name": "类型错误数据", "value": 300.25, "created_at": "2023-01-03T14:45:00"},  # id应该是int
    {"id": 4, "name": "缺少字段数据", "created_at": "2023-01-04T15:15:00"},  # 缺少value字段
    {"id": 5, "name": "正常数据3", "value": 500.0, "created_at": "2023-01-05T16:30:00"}
]

print("=== 测试API客户端模型映射功能 ===")
print("模拟API响应数据:")
for i, item in enumerate(simulated_api_data):
    print(f"  数据 {i+1}: {item}")

# 测试模型映射功能
result = api_client.map_to_model(simulated_api_data, TestModel)

print("\n映射结果:")
for i, model in enumerate(result):
    print(f"  模型 {i+1}: {model}")

print(f"\n总结: 共 {len(simulated_api_data)} 条数据，成功映射 {len(result)} 条，失败 {len(simulated_api_data) - len(result)} 条")

# 验证即使有错误数据，正确的数据仍然会被输出
assert len(result) > 0, "应该至少有一条数据映射成功"
assert len(result) < len(simulated_api_data), "应该有部分数据映射失败"

print("\n=== 测试通过! 模型错误不会影响整体输出 ===")

# 关闭API客户端
api_client.close()
