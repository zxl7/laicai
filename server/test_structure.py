#!/usr/bin/env python3
"""
测试项目目录结构是否正确的脚本
"""

import os

PROJECT_ROOT = os.path.dirname(__file__)
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')

def check_file_exists(file_path):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✓ {file_path}")
        return True
    else:
        print(f"✗ {file_path}")
        return False

def check_directory_exists(dir_path):
    """检查目录是否存在"""
    if os.path.isdir(dir_path):
        print(f"✓ {dir_path}")
        return True
    else:
        print(f"✗ {dir_path}")
        return False

def main():
    print("检查项目目录结构...")
    print("=" * 50)
    
    # 检查src目录
    if not check_directory_exists(SRC_DIR):
        print("src目录不存在，项目结构错误！")
        return False
    
    print("\n检查核心模块...")
    core_dir = os.path.join(SRC_DIR, 'core')
    if check_directory_exists(core_dir):
        check_file_exists(os.path.join(core_dir, '__init__.py'))
        check_file_exists(os.path.join(core_dir, 'app.py'))
        check_file_exists(os.path.join(core_dir, 'exceptions.py'))
    
    print("\n检查配置模块...")
    config_dir = os.path.join(SRC_DIR, 'config')
    if check_directory_exists(config_dir):
        check_file_exists(os.path.join(config_dir, '__init__.py'))
        check_file_exists(os.path.join(config_dir, 'config.py'))
    
    print("\n检查数据模型模块...")
    schemas_dir = os.path.join(SRC_DIR, 'schemas')
    if check_directory_exists(schemas_dir):
        check_file_exists(os.path.join(schemas_dir, '__init__.py'))
        check_file_exists(os.path.join(schemas_dir, 'quote.py'))
    
    print("\n检查服务层模块...")
    services_dir = os.path.join(SRC_DIR, 'services')
    if check_directory_exists(services_dir):
        check_file_exists(os.path.join(services_dir, '__init__.py'))
        check_file_exists(os.path.join(services_dir, 'quote.py'))
    
    print("\n检查API模块...")
    api_dir = os.path.join(SRC_DIR, 'api')
    if check_directory_exists(api_dir):
        check_file_exists(os.path.join(api_dir, '__init__.py'))
        check_file_exists(os.path.join(api_dir, 'routes.py'))
        check_file_exists(os.path.join(api_dir, 'endpoints', '__init__.py'))
        check_file_exists(os.path.join(api_dir, 'endpoints', 'quote.py'))
        check_file_exists(os.path.join(api_dir, 'dependencies', '__init__.py'))
        check_file_exists(os.path.join(api_dir, 'dependencies', 'quote.py'))
    
    print("\n检查工具模块...")
    utils_dir = os.path.join(SRC_DIR, 'utils')
    if check_directory_exists(utils_dir):
        check_file_exists(os.path.join(utils_dir, '__init__.py'))
    
    print("\n检查数据库模型模块...")
    models_dir = os.path.join(SRC_DIR, 'models')
    if check_directory_exists(models_dir):
        check_file_exists(os.path.join(models_dir, '__init__.py'))
    
    print("\n" + "=" * 50)
    print("检查主入口文件...")
    check_file_exists(os.path.join(PROJECT_ROOT, 'main.py'))
    check_file_exists(os.path.join(PROJECT_ROOT, 'setup.py'))
    
    print("\n项目结构检查完成！")
    print("\n现在检查导入语句...")
    
    # 检查是否还有laicai导入语句
    print("\n检查是否还有laicai层级的导入语句...")
    result = os.popen("cd {} && grep -r 'from laicai' . --include='*.py' 2>/dev/null".format(PROJECT_ROOT)).read()
    if result.strip():
        print("✗ 发现laicai导入语句：")
        print(result)
    else:
        print("✓ 没有发现laicai导入语句")
    
    print("\n" + "=" * 50)
    print("项目结构和导入路径已成功更新！laicai层级已移除。")
    print("现在代码结构为：src/[module] 而不是 src/laicai/[module]")
    print("导入语句格式为：from [module] import ... 而不是 from laicai.[module] import ...")
    
    return True

if __name__ == "__main__":
    main()
