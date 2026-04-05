"""Agent Service 入口"""

import os
import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from .api.models import (
    GenerateRequest,
    GenerationResult,
    HealthStatus,
    StreamChunk,
)
from .adapters.registry import init_adapters, registry
from .router.base import CostBasedRouter


# 全局状态
router = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """服务生命周期"""
    global router
    
    # 启动时初始化适配器
    init_adapters({
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "OPENAI_MODEL": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
    })
    
    # 初始化路由
    router = CostBasedRouter(registry)
    
    print(f"[Agent] 服务启动，可用适配器: {registry.list_adapters()}")
    
    yield
    
    # 关闭时清理
    print("[Agent] 服务关闭")


app = FastAPI(
    title="PersonaVerse Agent Service",
    description="AI 接入网关",
    version="0.1.0",
    lifespan=lifespan
)


@app.post("/generate", response_model=GenerationResult)
async def generate(request: GenerateRequest) -> GenerationResult:
    """
    同步生成接口
    
    - 智能选择模型
    - 自动故障转移
    - 成本优化
    """
    # 选择适配器
    adapter = await router.select(
        request.agent_type,
        request.config.cost_preference
    )
    
    if not adapter:
        raise HTTPException(503, "No available AI adapter")
    
    try:
        result = await adapter.generate(
            request.messages,
            request.config
        )
        return result
    except Exception as e:
        raise HTTPException(500, f"Generation failed: {str(e)}")


@app.post("/generate/stream")
async def generate_stream(request: GenerateRequest) -> StreamingResponse:
    """
    流式生成接口
    
    使用 SSE (Server-Sent Events) 返回流式响应
    """
    adapter = await router.select(
        request.agent_type,
        request.config.cost_preference
    )
    
    if not adapter:
        raise HTTPException(503, "No available AI adapter")
    
    async def event_stream() -> AsyncIterator[str]:
        """生成 SSE 流"""
        try:
            async for chunk in adapter.generate_stream(
                request.messages,
                request.config
            ):
                data = chunk.model_dump_json()
                yield f"data: {data}\n\n"
                
                if chunk.is_finished:
                    yield "data: [DONE]\n\n"
                    break
                    
        except Exception as e:
            error_chunk = StreamChunk(content=f"Error: {str(e)}", is_finished=True)
            yield f"data: {error_chunk.model_dump_json()}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )


@app.get("/health", response_model=dict)
async def health() -> dict:
    """服务健康检查"""
    adapters = registry.list_adapters()
    
    # 检查每个适配器的健康状态
    health_checks = {}
    for name in adapters:
        adapter = registry.get(name)
        if adapter:
            try:
                status = await adapter.health_check()
                health_checks[name] = status.model_dump()
            except Exception as e:
                health_checks[name] = {
                    "status": "error",
                    "error": str(e)
                }
    
    return {
        "service": "healthy",
        "adapters": health_checks
    }


@app.get("/adapters")
async def list_adapters() -> dict:
    """列出可用适配器"""
    adapters = registry.list_adapters()
    details = []
    
    for name in adapters:
        adapter = registry.get(name)
        if adapter:
            details.append({
                "name": name,
                "capabilities": adapter.capabilities,
                "cost_per_1k": adapter.cost_per_1k_tokens
            })
    
    return {"adapters": details}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
