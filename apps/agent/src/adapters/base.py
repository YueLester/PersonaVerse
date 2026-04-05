"""适配器基类"""

from abc import ABC, abstractmethod
from typing import AsyncIterator

from ..api.models import (
    GenerateConfig,
    GenerationResult,
    HealthStatus,
    Message,
    StreamChunk,
)


class AgentAdapter(ABC):
    """Agent 适配器基类"""
    
    name: str = "base"
    capabilities: list[str] = []
    
    @abstractmethod
    async def generate(
        self,
        messages: list[Message],
        config: GenerateConfig
    ) -> GenerationResult:
        """同步生成"""
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: list[Message],
        config: GenerateConfig
    ) -> AsyncIterator[StreamChunk]:
        """流式生成"""
        pass
    
    @abstractmethod
    async def health_check(self) -> HealthStatus:
        """健康检查"""
        pass
    
    @property
    @abstractmethod
    def cost_per_1k_tokens(self) -> tuple[float, float]:
        """
        成本 (input_cost, output_cost) USD per 1K tokens
        """
        pass
