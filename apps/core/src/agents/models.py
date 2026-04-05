"""Agent 数据模型"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class AgentStatus(str, Enum):
    """Agent 状态"""
    CONNECTING = "connecting"      # 连接中
    ACTIVE = "active"              # 活跃
    DECIDING = "deciding"          # 正在决策
    INACTIVE = "inactive"          # 离线
    ERROR = "error"                # 错误


@dataclass
class Agent:
    """Agent 实体"""
    id: str
    name: str
    
    # 接入配置
    connector_type: str           # "openai", "anthropic", "mock"
    connector_config: dict = field(default_factory=dict)
    
    # 状态
    status: AgentStatus = AgentStatus.CONNECTING
    connected_at: datetime = field(default_factory=datetime.now)
    last_active: Optional[datetime] = None
    
    # 当前情境
    current_scenario_id: Optional[str] = None
    
    # 元数据
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "connector_type": self.connector_type,
            "current_scenario_id": self.current_scenario_id,
            "connected_at": self.connected_at.isoformat(),
        }
