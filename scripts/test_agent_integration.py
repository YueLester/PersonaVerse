#!/usr/bin/env python3
"""
测试 Core 与 Agent 服务的集成

运行方式:
1. 先启动 Agent 服务: python apps/agent/src/main.py
2. 再运行此脚本: python scripts/test_agent_integration.py
"""

import asyncio

from src.config import settings

# 强制启用 Agent 服务
settings.AGENT_SERVICE_ENABLED = True
settings.AGENT_SERVICE_URL = "http://localhost:8001"

from src.main import demo


async def test_with_agent_service():
    """测试通过 Agent 服务运行"""
    print("=" * 60)
    print("测试 Core + Agent 服务集成")
    print("=" * 60)
    print(f"Agent 服务地址: {settings.AGENT_SERVICE_URL}")
    print(f"Agent 服务启用: {settings.AGENT_SERVICE_ENABLED}")
    print()
    
    # 运行标准 demo
    await demo()


if __name__ == "__main__":
    try:
        asyncio.run(test_with_agent_service())
    except Exception as e:
        print(f"\n[错误] {e}")
        print("\n请确保 Agent 服务已启动:")
        print("  conda activate personiverse")
        print("  python apps/agent/src/main.py")
