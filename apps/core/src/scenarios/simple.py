"""
简化场景 - MVP 版本

一个单一选择节点，用于演示闭环
"""

import uuid
from typing import Optional

from .base import Choice, ChoiceNode, Scenario, ScenarioStatus


class SimpleDilemmaScenario:
    """
    简单两难困境
    
    经典电车难题变种，用于演示人格探测
    """
    
    SCENARIOS = [
        {
            "name": "资源分配",
            "description": "你和另一个幸存者被困在荒岛，发现的食物只够一人支撑到救援。你会：",
            "choices": [
                Choice(
                    id="share_fair",
                    description="平分食物，两人都可能撑不到救援",
                    impacts={"altruism": 10, "fairness": 10, "thinking": -5}
                ),
                Choice(
                    id="take_all",
                    description="拿走全部食物，确保自己存活",
                    impacts={"altruism": -15, "dominance": 10, "thinking": 5}
                ),
                Choice(
                    id="negotiate",
                    description="提议通过游戏公平决定归属",
                    impacts={"fairness": 10, "sociability": 5, "thinking": 5}
                ),
                Choice(
                    id="sacrifice",
                    description="把食物让给对方，自己等待命运",
                    impacts={"altruism": 20, "authenticity": 10, "thinking": -10}
                ),
            ]
        },
        {
            "name": "信任测试",
            "description": "你发现队友私藏了关键情报，而你们正在竞争同一个目标。你会：",
            "choices": [
                Choice(
                    id="confront_direct",
                    description="当场揭穿，要求公开情报",
                    impacts={"dominance": 10, "fairness": 10, "sociability": -5}
                ),
                Choice(
                    id="negotiate_private",
                    description="私下谈判，寻求交易",
                    impacts={"sociability": 10, "thinking": 10, "authenticity": -5}
                ),
                Choice(
                    id="ignore",
                    description="假装不知道，自己寻找其他途径",
                    impacts={"authenticity": -10, "intuition": 10}
                ),
                Choice(
                    id="counter_hide",
                    description="也隐藏自己的情报，互相制衡",
                    impacts={"authenticity": -5, "thinking": 10, "fairness": -5}
                ),
            ]
        },
        {
            "name": "领导困境",
            "description": "团队陷入困境，需要有人做出不受欢迎的决定。你会：",
            "choices": [
                Choice(
                    id="step_up",
                    description="主动承担领导责任，做出决定",
                    impacts={"dominance": 15, "sociability": 5, "thinking": 5}
                ),
                Choice(
                    id="suggest_vote",
                    description="提议投票，让大家共同决定",
                    impacts={"fairness": 10, "dominance": -5, "sociability": 10}
                ),
                Choice(
                    id="wait",
                    description="等待他人先行动",
                    impacts={"dominance": -10, "authenticity": 5}
                ),
                Choice(
                    id="avoid",
                    description="保持距离，这不关你的事",
                    impacts={"sociability": -10, "authenticity": -5}
                ),
            ]
        }
    ]
    
    @classmethod
    def create(
        cls,
        participant_ids: list[str],
        scenario_index: int = 0
    ) -> Scenario:
        """创建场景"""
        template = cls.SCENARIOS[scenario_index % len(cls.SCENARIOS)]
        
        scenario_id = f"scenario_{uuid.uuid4().hex[:8]}"
        
        return Scenario(
            id=scenario_id,
            name=template["name"],
            participant_ids=participant_ids,
            status=ScenarioStatus.PENDING,
            current_node=ChoiceNode(
                id="initial",
                description=template["description"],
                choices=template["choices"],
                timeout=60.0
            )
        )
    
    @classmethod
    def get_all_templates(cls) -> list[dict]:
        """获取所有场景模板"""
        return [
            {
                "name": s["name"],
                "description": s["description"],
                "choice_count": len(s["choices"])
            }
            for s in cls.SCENARIOS
        ]
