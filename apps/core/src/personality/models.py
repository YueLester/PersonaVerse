"""人格维度数据模型（简化版 MVP）"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PersonalityDimensions:
    """
    人格维度 - MVP 简化版
    只保留最核心的维度，便于演示
    """
    
    # 认知层（简化）
    thinking: int = 0        # -100 感性 ~ +100 理性
    intuition: int = 0       # -100 实感 ~ +100 直觉
    
    # 道德层（简化）
    altruism: int = 0        # -100 利己 ~ +100 利他
    fairness: int = 0        # -100 灵活 ~ +100 公平
    
    # 社交层（简化）
    sociability: int = 0     # -100 独处 ~ +100 社交
    dominance: int = 0       # -100 服从 ~ +100 主导
    
    # 表象层（简化）
    authenticity: int = 0    # -100 表演 ~ +100 真实
    
    def apply_changes(self, changes: dict[str, int]) -> "PersonalityDimensions":
        """应用维度变化"""
        for dim, delta in changes.items():
            if hasattr(self, dim):
                current = getattr(self, dim)
                new_val = max(-100, min(100, current + delta))
                setattr(self, dim, new_val)
        return self
    
    def to_dict(self) -> dict:
        return {
            "thinking": self.thinking,
            "intuition": self.intuition,
            "altruism": self.altruism,
            "fairness": self.fairness,
            "sociability": self.sociability,
            "dominance": self.dominance,
            "authenticity": self.authenticity,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PersonalityDimensions":
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


@dataclass
class PersonalityProfile:
    """人格档案"""
    agent_id: str
    dimensions: PersonalityDimensions = field(default_factory=PersonalityDimensions)
    
    # 标签（由系统推导）
    tags: list[str] = field(default_factory=list)
    
    # 变化历史
    history: list[dict] = field(default_factory=list)
    
    def record_change(self, context: str, changes: dict[str, int]) -> None:
        """记录变化"""
        self.history.append({
            "context": context,
            "changes": changes,
            "result": self.dimensions.to_dict()
        })
    
    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "dimensions": self.dimensions.to_dict(),
            "tags": self.tags,
            "history_count": len(self.history)
        }
