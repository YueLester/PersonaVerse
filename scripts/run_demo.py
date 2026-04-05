#!/usr/bin/env python3
"""运行最小闭环演示"""

import asyncio

# 如果安装包后可以直接导入
# pip install -e apps/core
from src.main import demo

if __name__ == "__main__":
    asyncio.run(demo())
