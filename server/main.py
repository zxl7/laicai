#!/usr/bin/env python3
"""
主应用入口文件
"""

import uvicorn
import os
import sys

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.app import create_app
from config import settings

# 创建FastAPI应用实例
app = create_app()


def main() -> None:
    """
    应用主函数，用于启动服务器
    """
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS,
    )


if __name__ == "__main__":
    main()