"""
人格引擎 - 计算维度变化

MVP 版本：硬编码映射规则，后续可替换为配置/ML
"""

from typing import Any

from .models import PersonalityDimensions, PersonalityProfile


class PersonalityEngine:
    """
    人格计算引擎
    
    当前实现：简单的硬编码规则
    未来：可配置规则、机器学习模型
    """
    
    # 选择 ID 到维度变化的映射（MVP 简化版）
    # 规则：选择 ID 包含维度关键词时，该维度变化
    CHOICE_IMPACTS = {
        # 理性选择
        "analyze": {"thinking": +5, "intuition": -2},
        "calculate": {"thinking": +8},
        "logic": {"thinking": +10, "fairness": +3},
        
        # 感性选择
        "feel": {"thinking": -5, "intuition": +5},
        "intuition": {"intuition": +10},
        "emotion": {"thinking": -8, "altruism": +5},
        
        # 利他选择
        "help": {"altruism": +10, "thinking": -3},
        "sacrifice": {"altruism": +15, "authenticity": +5},
        "share": {"altruism": +8, "fairness": +5},
        
        # 利己选择
        "self": {"altruism": -10, "authenticity": -3},
        "take": {"altruism": -8, "dominance": +5},
        "compete": {"altruism": -5, "dominance": +10},
        
        # 社交选择
        "talk": {"sociability": +8},
        "lead": {"dominance": +10, "sociability": +5},
        "follow": {"dominance": -8, "sociability": +3},
        "alone": {"sociability": -10, "authenticity": +3},
        
        # 公平选择
        "fair": {"fairness": +10, "altruism": +3},
        "equal": {"fairness": +12},
        "cheat": {"fairness": -15, "authenticity": -10},
        
        # 真实选择
        "honest": {"authenticity": +10},
        "lie": {"authenticity": -15, "fairness": -5},
        "pretend": {"authenticity": -10, "sociability": +3},
    }
    
    def __init__(self):
        # 内存存储（MVP 版本）
        self._profiles: dict[str, PersonalityProfile] = {}
    
    def get_or_create_profile(self, agent_id: str) -> PersonalityProfile:
        """获取或创建档案"""
        if agent_id not in self._profiles:
            self._profiles[agent_id] = PersonalityProfile(agent_id=agent_id)
        return self._profiles[agent_id]
    
    def calculate_impact(
        self,
        agent_id: str,
        choice_id: str,
        context: dict[str, Any]
    ) -> dict[str, int]:
        """
        计算选择对人格维度的影响
        
        MVP：基于关键词匹配
        未来：基于情境复杂规则
        """
        changes: dict[str, int] = {}
        
        # 1. 直接匹配选择 ID
        if choice_id in self.CHOICE_IMPACTS:
            changes.update(self.CHOICE_IMPACTS[choice_id])
        else:
            # 2. 尝试部分匹配
            for key, impact in self.CHOICE_IMPACTS.items():
                if key in choice_id or choice_id in key:
                    changes.update(impact)
                    break
        
        # 3. 如果没有匹配，给一个微小的变化（避免完全无变化）
        if not changes:
            changes = {"authenticity": +1}  # 默认：做出选择就是真实的
        
        return changes
    
    def apply_choice(
        self,
        agent_id: str,
        choice_id: str,
        context: dict[str, Any]
    ) -> PersonalityProfile:
        """
        应用选择，更新人格档案
        
        Returns:
            更新后的档案
        """
        profile = self.get_or_create_profile(agent_id)
        
        # 计算影响
        changes = self.calculate_impact(agent_id, choice_id, context)
        
        # 应用变化
        profile.dimensions.apply_changes(changes)
        
        # 记录历史
        profile.record_change(
            context=context.get("description", "unknown"),
            changes=changes
        )
        
        # 更新标签（MVP 简化版）
        self._update_tags(profile)
        
        return profile
    
    def _update_tags(self, profile: PersonalityProfile) -> None:
        """
        根据维度值更新标签
        MVP 简化版标签系统
        """
        dims = profile.dimensions
        tags = []
        
        # 极端值标签
        if dims.thinking > 60:
            tags.append("理性主导")
        elif dims.thinking < -60:
            tags.append("感性主导")
        
        if dims.altruism > 60:
            tags.append("利他主义者")
        elif dims.altruism < -60:
            tags.append("利己主义者")
        
        if dims.dominance > 60:
            tags.append("领导者倾向")
        elif dims.dominance < -60:
            tags.append("跟随者倾向")
        
        if dims.authenticity > 60:
            tags.append("高度真实")
        elif dims.authenticity < -40:
            tags.append("表演型人格")
        
        if dims.sociability > 60:
            tags.append("社交活跃")
        elif dims.sociability < -60:
            tags.append("独处偏好")
        
        profile.tags = tags
    
    def get_profile(self, agent_id: str) -> PersonalityProfile | None:
        """获取档案"""
        return self._profiles.get(agent_id)


# 全局引擎实例
personality_engine = PersonalityEngine()
