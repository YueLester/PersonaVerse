"""
Agent Service - 入口文件
基于多层架构的 AI 服务
端口: 8001
"""

import sys
import os

# 将当前目录加入路径，支持直接运行 python main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Agent Service",
    description="基于多层架构的 AI 服务",
    version="0.1.0"
)

# 注册路由
app.include_router(router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Agent Service", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    
    ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    model = os.environ.get("DEFAULT_MODEL", "qwen:2.5")
    
    print("=" * 60)
    print("Agent Service Starting")
    print("=" * 60)
    print(f"Ollama: {ollama_url}")
    print(f"Model: {model}")
    print(f"\nEndpoints:")
    print(f"  POST /v1/geo/province   - 查省份")
    print(f"  GET  /v1/geo/province   - 查省份(GET)")
    print(f"  POST /v1/chat          - 通用对话")
    print(f"  GET  /v1/health        - 健康检查")
    print(f"\nAPI Docs: http://localhost:8001/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
