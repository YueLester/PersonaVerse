"""人格引擎测试"""

import pytest

from apps.core.src.personality.engine import PersonalityEngine
from apps.core.src.personality.models import PersonalityDimensions


class TestPersonalityEngine:
    """测试人格引擎"""
    
    def test_create_profile(self):
        """测试创建档案"""
        engine = PersonalityEngine()
        profile = engine.get_or_create_profile("test_agent")
        
        assert profile.agent_id == "test_agent"
        assert profile.dimensions.thinking == 0
        assert profile.dimensions.altruism == 0
    
    def test_calculate_impact_direct_match(self):
        """测试直接匹配选择影响"""
        engine = PersonalityEngine()
        
        changes = engine.calculate_impact("test", "help", {})
        
        assert "altruism" in changes
        assert changes["altruism"] > 0
    
    def test_apply_choice(self):
        """测试应用选择"""
        engine = PersonalityEngine()
        
        profile = engine.apply_choice(
            agent_id="test",
            choice_id="sacrifice",
            context={"description": "测试"}
        )
        
        assert profile.dimensions.altruism > 0
        assert len(profile.history) == 1
        assert len(profile.tags) > 0
    
    def test_dimension_bounds(self):
        """测试维度边界"""
        dims = PersonalityDimensions()
        
        # 应用超大变化
        dims.apply_changes({"thinking": 200})
        
        # 应该被限制在 100
        assert dims.thinking == 100
        
        dims.apply_changes({"thinking": -500})
        
        # 应该被限制在 -100
        assert dims.thinking == -100
