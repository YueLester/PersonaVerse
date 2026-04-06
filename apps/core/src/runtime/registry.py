"""Agent 注册管理"""

import asyncio
from typing import Optional

from .models import Agent, AgentStatus


class AgentRegistry:
    """Agent 注册表 - 内存存储（MVP 版本）"""
    
    def __init__(self):
        self._agents: dict[str, Agent] = {}
        self._lock = asyncio.Lock()
    
    async def register(self, agent: Agent) -> Agent:
        """注册新 Agent"""
        async with self._lock:
            self._agents[agent.id] = agent
            agent.status = AgentStatus.ACTIVE
            return agent
    
    async def get(self, agent_id: str) -> Optional[Agent]:
        """获取 Agent"""
        return self._agents.get(agent_id)
    
    async def update_status(self, agent_id: str, status: AgentStatus) -> Optional[Agent]:
        """更新状态"""
        async with self._lock:
            if agent := self._agents.get(agent_id):
                agent.status = status
                return agent
            return None
    
    async def list_active(self) -> list[Agent]:
        """列出活跃 Agent"""
        return [
            a for a in self._agents.values()
            if a.status in (AgentStatus.ACTIVE, AgentStatus.DECIDING)
        ]
    
    async def unregister(self, agent_id: str) -> bool:
        """注销 Agent"""
        async with self._lock:
            if agent_id in self._agents:
                del self._agents[agent_id]
                return True
            return False


# 全局单例
registry = AgentRegistry()
