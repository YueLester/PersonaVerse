"""OpenAI 适配器"""

import time
from datetime import datetime
from typing import AsyncIterator

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

from .base import AgentAdapter
from ..api.models import (
    GenerateConfig,
    GenerationResult,
    HealthStatus,
    Message,
    StreamChunk,
    TokenUsage,
)


class OpenAIAdapter(AgentAdapter):
    """OpenAI GPT 适配器"""
    
    name = "openai"
    capabilities = ["chat", "streaming", "function_calling"]
    
    # 模型成本 (input, output) per 1K tokens
    COSTS = {
        "gpt-4o": (0.005, 0.015),
        "gpt-4o-mini": (0.00015, 0.0006),
        "gpt-4-turbo": (0.01, 0.03),
        "gpt-3.5-turbo": (0.0005, 0.0015),
    }
    
    def __init__(self, api_key: str, default_model: str = "gpt-4o-mini"):
        if not HAS_HTTPX:
            raise ImportError("httpx is required")
        
        self.api_key = api_key
        self.default_model = default_model
        self.client = httpx.AsyncClient(
            base_url="https://api.openai.com/v1",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0
        )
    
    def _map_messages(self, messages: list[Message]) -> list[dict]:
        """转换消息格式"""
        return [
            {"role": m.role, "content": m.content, **({"name": m.name} if m.name else {})}
            for m in messages
        ]
    
    def _calculate_cost(self, model: str, usage: TokenUsage) -> float:
        """计算成本"""
        input_cost, output_cost = self.COSTS.get(model, (0.01, 0.03))
        
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        
        cost = (input_tokens / 1000 * input_cost) + (output_tokens / 1000 * output_cost)
        return round(cost, 6)
    
    async def generate(
        self,
        messages: list[Message],
        config: GenerateConfig
    ) -> GenerationResult:
        """同步生成"""
        start_time = time.time()
        model = config.model or self.default_model
        
        try:
            response = await self.client.post(
                "/chat/completions",
                json={
                    "model": model,
                    "messages": self._map_messages(messages),
                    "temperature": config.temperature,
                    "max_tokens": config.max_tokens,
                }
            )
            
            result = response.json()
            
            # 解析响应
            content = result["choices"][0]["message"]["content"]
            finish_reason = result["choices"][0].get("finish_reason", "stop")
            
            # Token 使用
            usage_data = result.get("usage", {})
            usage = TokenUsage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0)
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            return GenerationResult(
                content=content,
                model=model,
                usage=usage,
                latency_ms=latency_ms,
                cost_usd=self._calculate_cost(model, usage),
                request_id=result.get("id", "unknown"),
                finish_reason=finish_reason
            )
            
        except Exception as e:
            raise AdapterError(f"OpenAI generation failed: {e}")
    
    async def generate_stream(
        self,
        messages: list[Message],
        config: GenerateConfig
    ) -> AsyncIterator[StreamChunk]:
        """流式生成"""
        model = config.model or self.default_model
        
        try:
            async with self.client.stream(
                "POST",
                "/chat/completions",
                json={
                    "model": model,
                    "messages": self._map_messages(messages),
                    "temperature": config.temperature,
                    "max_tokens": config.max_tokens,
                    "stream": True
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            yield StreamChunk(content="", is_finished=True)
                            break
                        
                        try:
                            import json
                            chunk = json.loads(data)
                            delta = chunk["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            
                            if content:
                                yield StreamChunk(content=content)
                        except:
                            pass
                            
        except Exception as e:
            raise AdapterError(f"OpenAI stream failed: {e}")
    
    async def health_check(self) -> HealthStatus:
        """健康检查"""
        start_time = time.time()
        
        try:
            # 简单请求检查
            response = await self.client.get("/models", timeout=5.0)
            latency_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                return HealthStatus(
                    status="healthy",
                    latency_ms=latency_ms,
                    last_checked=datetime.now().isoformat()
                )
            else:
                return HealthStatus(
                    status="degraded",
                    latency_ms=latency_ms,
                    last_checked=datetime.now().isoformat(),
                    error_count=1
                )
                
        except Exception as e:
            return HealthStatus(
                status="unhealthy",
                latency_ms=(time.time() - start_time) * 1000,
                last_checked=datetime.now().isoformat(),
                error_count=1
            )
    
    @property
    def cost_per_1k_tokens(self) -> tuple[float, float]:
        """成本"""
        return self.COSTS.get(self.default_model, (0.01, 0.03))


class AdapterError(Exception):
    """适配器错误"""
    pass
