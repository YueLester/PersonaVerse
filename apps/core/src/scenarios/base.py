"""场景基类"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class ScenarioStatus(str, Enum):
    """场景状态"""
    PENDING = "pending"        # 等待开始
    RUNNING = "running"        # 进行中
    WAITING = "waiting"        # 等待决策
    RESOLVED = "resolved"      # 已结算
    COMPLETED = "completed"    # 已完成


@dataclass
class Choice:
    """可选项"""
    id: str
    description: str
    impacts: dict[str, Any] = field(default_factory=dict)  # 额外影响参数


@dataclass
class ChoiceNode:
    """选择节点"""
    id: str
    description: str
    choices: list[Choice]
    timeout: Optional[float] = 30.0  # 决策超时（秒）


@dataclass
class Scenario:
    """场景实例"""
    id: str
    name: str
    
    # 参与者
    participant_ids: list[str]
    
    # 当前状态
    status: ScenarioStatus = ScenarioStatus.PENDING
    current_node: Optional[ChoiceNode] = None
    
    # 决策记录
    decisions: dict[str, str] = field(default_factory=dict)  # agent_id -> choice_id
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # 结果
    results: list[dict] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "participants": self.participant_ids,
            "current_node": {
                "id": self.current_node.id,
                "description": self.current_node.description,
                "choices": [
                    {"id": c.id, "description": c.description}
                    for c in self.current_node.choices
                ]
            } if self.current_node else None,
            "decisions": self.decisions,
        }
