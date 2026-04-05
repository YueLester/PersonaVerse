"""适配器注册表"""

from typing import Optional

from .base import AgentAdapter
from .openai import OpenAIAdapter


class AdapterRegistry:
    """适配器注册表"""
    
    def __init__(self):
        self._adapters: dict[str, AgentAdapter] = {}
    
    def register(self, name: str, adapter: AgentAdapter) -> None:
        """注册适配器"""
        self._adapters[name] = adapter
    
    def get(self, name: str) -> Optional[AgentAdapter]:
        """获取适配器"""
        return self._adapters.get(name)
    
    def list_adapters(self) -> list[str]:
        """列出所有适配器"""
        return list(self._adapters.keys())
    
    def get_healthy_adapters(self) -> list[tuple[str, AgentAdapter]]:
        """获取健康的适配器"""
        # TODO: 实际检查健康状态
        return list(self._adapters.items())


# 全局注册表
registry = AdapterRegistry()


def init_adapters(config: dict):
    """初始化适配器"""
    # OpenAI
    if api_key := config.get("OPENAI_API_KEY"):
        registry.register(
            "openai",
            OpenAIAdapter(api_key, config.get("OPENAI_MODEL", "gpt-4o-mini"))
        )
    
    # TODO: Claude, Gemini, etc.
