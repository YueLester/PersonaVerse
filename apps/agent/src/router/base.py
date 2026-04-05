"""路由策略基类"""

from abc import ABC, abstractmethod
from typing import Optional

from ..adapters.base import AgentAdapter
from ..adapters.registry import AdapterRegistry


class RouterStrategy(ABC):
    """路由策略基类"""
    
    def __init__(self, registry: AdapterRegistry):
        self.registry = registry
    
    @abstractmethod
    async def select(
        self,
        agent_type: str,
        preference: str = "balanced"
    ) -> Optional[AgentAdapter]:
        """选择适配器"""
        pass


class RoundRobinRouter(RouterStrategy):
    """轮询路由"""
    
    def __init__(self, registry: AdapterRegistry):
        super().__init__(registry)
        self._index = 0
    
    async def select(
        self,
        agent_type: str,
        preference: str = "balanced"
    ) -> Optional[AgentAdapter]:
        adapters = self.registry.get_healthy_adapters()
        if not adapters:
            return None
        
        adapter = adapters[self._index % len(adapters)][1]
        self._index += 1
        return adapter


class CostBasedRouter(RouterStrategy):
    """成本优先路由"""
    
    async def select(
        self,
        agent_type: str,
        preference: str = "balanced"
    ) -> Optional[AgentAdapter]:
        adapters = self.registry.get_healthy_adapters()
        if not adapters:
            return None
        
        if preference == "cheap":
            # 选择最便宜的
            return min(adapters, key=lambda x: x[1].cost_per_1k_tokens[0])[1]
        elif preference == "quality":
            # 选择最贵的（通常质量更好）
            return max(adapters, key=lambda x: x[1].cost_per_1k_tokens[0])[1]
        else:
            # balanced: 选择中等的
            sorted_adapters = sorted(adapters, key=lambda x: x[1].cost_per_1k_tokens[0])
            return sorted_adapters[len(sorted_adapters) // 2][1]


class FallbackRouter(RouterStrategy):
    """带故障转移的路由"""
    
    def __init__(self, registry: AdapterRegistry, primary: str, fallback: str):
        super().__init__(registry)
        self.primary = primary
        self.fallback = fallback
    
    async def select(
        self,
        agent_type: str,
        preference: str = "balanced"
    ) -> Optional[AgentAdapter]:
        # 先尝试主适配器
        primary = self.registry.get(self.primary)
        if primary:
            health = await primary.health_check()
            if health.status == "healthy":
                return primary
        
        # 主适配器故障，使用备用
        return self.registry.get(self.fallback)
