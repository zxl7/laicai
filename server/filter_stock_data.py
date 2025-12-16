#!/usr/bin/env python3
"""
脚本功能：删除stockCompanyPool.json文件中成交额(cje)小于5亿的数据
"""

import json
import os

# 文件路径
FILE_PATH = "/Users/zxl/Desktop/laicai/server/DataBase/stockCompanyPool.json"

# 读取stockCompanyPool.json文件内容
def read_stock_data():
    """
    读取stockCompanyPool.json文件内容
    
    Returns:
        dict: 股票数据字典
    """
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件不存在: {FILE_PATH}")
        return {}
    except json.JSONDecodeError:
        print(f"JSON文件格式错误: {FILE_PATH}")
        return {}
    except Exception as e:
        print(f"读取文件失败: {e}")
        return {}

# 过滤股票数据，保留成交额大于等于5亿的数据
def filter_stock_data(stock_data):
    """
    过滤股票数据，保留成交额大于等于5亿的数据
    
    Args:
        stock_data (dict): 原始股票数据字典
        
    Returns:
        tuple: (过滤后的数据字典, 被删除的股票数量)
    """
    filtered_data = {}
    deleted_count = 0
    
    for code, stock_info in stock_data.items():
        # 获取成交额，优先直接获取，其次从list.cje获取
        cje = stock_info.get('cje', 0)
        if cje == 0:
            cje = stock_info.get('list', {}).get('cje', 0)
        
        if cje >= 500000000:  # 5亿
            filtered_data[code] = stock_info
        else:
            deleted_count += 1
            print(f"删除股票 {code}({stock_info.get('mc', '')}): 成交额 {cje} < 5亿")
    
    return filtered_data, deleted_count

# 将过滤后的数据写回文件
def write_filtered_data(filtered_data):
    """
    将过滤后的数据写回stockCompanyPool.json文件
    
    Args:
        filtered_data (dict): 过滤后的股票数据字典
        
    Returns:
        bool: 写入成功返回True，失败返回False
    """
    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"写入文件失败: {e}")
        return False

# 验证过滤结果
def verify_filtered_data(filtered_data):
    """
    验证过滤结果，确保所有股票的成交额都大于等于5亿
    
    Args:
        filtered_data (dict): 过滤后的股票数据字典
        
    Returns:
        bool: 验证通过返回True，否则返回False
    """
    for code, stock_info in filtered_data.items():
        cje = stock_info.get('cje', 0)
        if cje == 0:
            cje = stock_info.get('list', {}).get('cje', 0)
        
        if cje < 500000000:
            print(f"验证失败: 股票 {code} 成交额 {cje} < 5亿")
            return False
    
    print("验证通过: 所有股票的成交额都大于等于5亿")
    return True

# 主函数
def main():
    """
    主函数，执行删除成交额小于5亿数据的流程
    """
    print("开始处理stockCompanyPool.json文件...")
    
    # 步骤1: 读取股票数据
    stock_data = read_stock_data()
    if not stock_data:
        print("没有读取到股票数据，退出程序")
        return
    
    print(f"共读取到 {len(stock_data)} 条股票数据")
    
    # 步骤2: 过滤股票数据
    filtered_data, deleted_count = filter_stock_data(stock_data)
    
    print(f"过滤后剩余 {len(filtered_data)} 条股票数据")
    print(f"共删除 {deleted_count} 条成交额小于5亿的股票数据")
    
    # 步骤3: 将过滤后的数据写回文件
    if write_filtered_data(filtered_data):
        print("成功将过滤后的数据写回文件")
        
        # 步骤4: 验证过滤结果
        verify_filtered_data(filtered_data)
    else:
        print("写入文件失败，操作未完成")

if __name__ == "__main__":
    main()
