"""Agent 客户端 - 供其他服务调用"""

import httpx
from typing import AsyncIterator, Optional

from .api.models import (
    GenerateConfig,
    GenerateRequest,
    GenerationResult,
    Message,
    StreamChunk,
)


class AgentClient:
    """
    Agent Service 客户端
    
    供 Core、Theater 等模块调用
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:8001",
        api_key: Optional[str] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=60.0,
            headers={
                "Authorization": f"Bearer {api_key}" if api_key else None
            }
        )
    
    async def generate(
        self,
        tenant_id: str,
        agent_type: str,
        messages: list[dict],
        config: Optional[dict] = None
    ) -> GenerationResult:
        """
        调用 Agent 生成
        
        Args:
            tenant_id: 租户标识
            agent_type: Agent 类型
            messages: 消息列表 [{"role": "user", "content": "..."}]
            config: 生成配置
        
        Returns:
            生成结果
        """
        request = GenerateRequest(
            tenant_id=tenant_id,
            agent_type=agent_type,
            messages=[Message(**m) for m in messages],
            config=GenerateConfig(**(config or {}))
        )
        
        response = await self.client.post(
            "/generate",
            json=request.model_dump()
        )
        response.raise_for_status()
        
        return GenerationResult(**response.json())
    
    async def generate_stream(
        self,
        tenant_id: str,
        agent_type: str,
        messages: list[dict],
        config: Optional[dict] = None
    ) -> AsyncIterator[StreamChunk]:
        """
        流式生成
        
        Yields:
            StreamChunk 流式块
        """
        request = GenerateRequest(
            tenant_id=tenant_id,
            agent_type=agent_type,
            messages=[Message(**m) for m in messages],
            config=GenerateConfig(**(config or {}), stream=True)
        )
        
        async with self.client.stream(
            "POST",
            "/generate/stream",
            json=request.model_dump()
        ) as response:
            response.raise_for_status()
            
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    
                    try:
                        import json
                        chunk_data = json.loads(data)
                        yield StreamChunk(**chunk_data)
                    except:
                        pass
    
    async def health(self) -> dict:
        """检查服务健康"""
        response = await self.client.get("/health")
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()


# 便捷函数：快速创建客户端
def create_agent_client(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None
) -> AgentClient:
    """
    创建 Agent 客户端
    
    从环境变量读取配置（如果未提供）
    """
    import os
    
    base_url = base_url or os.environ.get(
        "AGENT_SERVICE_URL",
        "http://localhost:8001"
    )
    api_key = api_key or os.environ.get("AGENT_SERVICE_API_KEY")
    
    return AgentClient(base_url, api_key)
