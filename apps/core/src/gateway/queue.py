"""
离线消息队列
Agent 离线时缓存消息，重连后推送
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class QueuedMessage:
    """队列中的消息"""
    msg_id: str
    payload: dict
    queued_at: datetime
    ttl_seconds: int
    
    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.queued_at + timedelta(seconds=self.ttl_seconds)


class OfflineQueue:
    """
    离线消息队列（基于 Redis 实现）
    
    职责：
    1. Agent 离线时缓存消息
    2. Agent 重连后按序推送
    3. 过期清理
    4. 队列长度限制
    """
    
    def __init__(
        self,
        redis_client: Optional["Redis"] = None,
        max_per_agent: int = 100,
        default_ttl: int = 3600,
    ):
        self.redis = redis_client
        self.max_per_agent = max_per_agent
        self.default_ttl = default_ttl
        
    async def enqueue(self, agent_id: str, message: dict) -> bool:
        """消息入队"""
        pass
    
    async def dequeue_all(self, agent_id: str) -> List[QueuedMessage]:
        """取出所有待处理消息（Agent 重连时调用）"""
        pass
    
    async def clear(self, agent_id: str):
        """清空队列"""
        pass
