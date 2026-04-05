"""
人格维度数据模型
五大模块：认知、星象、道德、社交、表象
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ============ 模块一：认知层（荣格八维） ============

class CognitiveFunction(str, Enum):
    """八维认知功能"""
    SE = "Se"  # 外倾感觉
    SI = "Si"  # 内倾感觉
    NE = "Ne"  # 外倾直觉
    NI = "Ni"  # 内倾直觉
    TE = "Te"  # 外倾思维
    TI = "Ti"  # 内倾思维
    FE = "Fe"  # 外倾情感
    FI = "Fi"  # 内倾情感


class CognitiveProfile(BaseModel):
    """认知层档案"""
    Se: int = Field(0, ge=-100, le=100, description="外倾感觉")
    Si: int = Field(0, ge=-100, le=100, description="内倾感觉")
    Ne: int = Field(0, ge=-100, le=100, description="外倾直觉")
    Ni: int = Field(0, ge=-100, le=100, description="内倾直觉")
    Te: int = Field(0, ge=-100, le=100, description="外倾思维")
    Ti: int = Field(0, ge=-100, le=100, description="内倾思维")
    Fe: int = Field(0, ge=-100, le=100, description="外倾情感")
    Fi: int = Field(0, ge=-100, le=100, description="内倾情感")
    
    def get_dominant(self) -> tuple[CognitiveFunction, int]:
        """返回主导功能及其分数"""
        values = {
            CognitiveFunction.SE: self.Se,
            CognitiveFunction.SI: self.Si,
            CognitiveFunction.NE: self.Ne,
            CognitiveFunction.NI: self.Ni,
            CognitiveFunction.TE: self.Te,
            CognitiveFunction.TI: self.Ti,
            CognitiveFunction.FE: self.Fe,
            CognitiveFunction.FI: self.Fi,
        }
        dominant = max(values, key=values.get)
        return dominant, values[dominant]


# ============ 模块二：星象层 ============

class SolarExpression(str, Enum):
    FIRE = "fire"      # 日火：主动扩张
    EARTH = "earth"    # 日土：稳定构建
    AIR = "air"        # 日风：社交连接
    WATER = "water"    # 日水：情感沉浸


class LunarResponse(str, Enum):
    CARDINAL = "cardinal"    # 月创：情绪驱动行动
    FIXED = "fixed"          # 月固：情绪持久深刻
    MUTABLE = "mutable"      # 月变：情绪流动适应


class AscendantMask(str, Enum):
    WARRIOR = "warrior"       # 升战：强势果决
    DIPLOMAT = "diplomat"     # 升使：和谐圆融
    SAGE = "sage"             # 升贤：智慧超然
    ARTIST = "artist"         # 升艺：独特魅力
    BUILDER = "builder"       # 升筑：可靠务实


class AstroProfile(BaseModel):
    """星象层档案"""
    solar: SolarExpression = Field(..., description="太阳星座：核心自我表达")
    lunar: LunarResponse = Field(..., description="月亮星座：情感反应模式")
    ascendant: AscendantMask = Field(..., description="上升星座：对外第一印象")
    mercury: str = Field("direct", description="水星：沟通模式")
    mars: str = Field("strategic", description="火星：冲突/欲望模式")
    venus: str = Field("exchange", description="金星：价值/关系模式")


# ============ 模块三：道德层 ============

class MoralProfile(BaseModel):
    """道德层档案"""
    care_harm: int = Field(0, ge=-100, le=100, description="关怀-伤害维度")
    fairness_cheating: int = Field(0, ge=-100, le=100, description="公平-欺骗维度")
    loyalty_betrayal: int = Field(0, ge=-100, le=100, description="忠诚-背叛维度")
    authority_subversion: int = Field(0, ge=-100, le=100, description="权威-颠覆维度")
    sanctity_degradation: int = Field(0, ge=-100, le=100, description="纯洁-堕落维度")
    liberty_oppression: int = Field(0, ge=-100, le=100, description="自由-压迫维度")
    
    # 衍生维度
    flexibility: str = Field("pragmatic", description="道德灵活性：principled/pragmatic/situational")
    attribution: str = Field("systemic", description="归因风格：internal/external/systemic")


# ============ 模块四：社交层 ============

class SocialEnergy(str, Enum):
    GIVER = "giver"
    TAKER = "taker"
    EXCHANGE = "exchange"
    SELF = "self"


class TeamRole(str, Enum):
    SHAPER = "shaper"
    IMPLEMENTER = "implementer"
    COMPLETER = "completer"
    PLANT = "plant"
    RESOURCE_INVESTIGATOR = "resource_investigator"
    COORDINATOR = "coordinator"
    TEAMWORKER = "teamworker"
    MONITOR_EVALUATOR = "monitor_evaluator"
    SPECIALIST = "specialist"


class AttachmentStyle(str, Enum):
    SECURE = "secure"
    ANXIOUS = "anxious"
    AVOIDANT = "avoidant"
    DISORGANIZED = "disorganized"


class SocialStrategy(str, Enum):
    """社交策略：黑暗三角 vs 光明三角"""
    DARK_MACHIAVELLIAN = "dark_machiavellianism"
    DARK_NARCISSISM = "dark_narcissism"
    DARK_PSYCHOPATHY = "dark_psychopathy"
    LIGHT_KANTIAN = "light_kantianism"
    LIGHT_HUMANISM = "light_humanism"
    LIGHT_FAITH = "light_faith"
    NEUTRAL_RECIPROCITY = "neutral_reciprocity"


class ConflictStyle(str, Enum):
    COMPETING = "competing"
    COLLABORATING = "collaborating"
    COMPROMISING = "compromising"
    AVOIDING = "avoiding"
    ACCOMMODATING = "accommodating"


class SocialProfile(BaseModel):
    """社交层档案"""
    energy: SocialEnergy = Field(..., description="社交能量")
    team_role: TeamRole = Field(..., description="团队角色")
    attachment: AttachmentStyle = Field(..., description="依恋模式")
    strategy: SocialStrategy = Field(..., description="社交策略")
    conflict_style: ConflictStyle = Field(..., description="冲突处理风格")


# ============ 模块五：表象层 ============

class SurfaceProfile(BaseModel):
    """表象层档案"""
    impression_management: str = Field("strategic", description="印象管理")
    authenticity_gap: str = Field("strategic", description="真实-表演差距")
    social_comparison: str = Field("lateral", description="社会比较倾向")
    reputation_sensitivity: str = Field("vigilant", description="声誉敏感度")
    power_perception: str = Field("indifferent", description="权力感知")
    shame_guilt: str = Field("guilt_prone", description="羞耻-内疚倾向")


# ============ 完整人格档案 ============

class PersonalityProfile(BaseModel):
    """完整人格档案：五大模块聚合"""
    agent_id: str = Field(..., description="关联的Agent ID")
    
    # 五大模块
    cognitive: CognitiveProfile = Field(default_factory=CognitiveProfile)
    astro: AstroProfile = Field(default_factory=lambda: AstroProfile(
        solar=SolarExpression.FIRE,
        lunar=LunarResponse.CARDINAL,
        ascendant=AscendantMask.WARRIOR
    ))
    moral: MoralProfile = Field(default_factory=MoralProfile)
    social: SocialProfile = Field(default_factory=lambda: SocialProfile(
        energy=SocialEnergy.EXCHANGE,
        team_role=TeamRole.TEAMWORKER,
        attachment=AttachmentStyle.SECURE,
        strategy=SocialStrategy.NEUTRAL_RECIPROCITY,
        conflict_style=ConflictStyle.COMPROMISING
    ))
    surface: SurfaceProfile = Field(default_factory=SurfaceProfile)
    
    # 衍生标签
    computed_tags: list[str] = Field(default_factory=list, description="系统计算的标签")
    
    # 演化历史
    evolution_history: list[dict] = Field(default_factory=list, description="属性变化历史")
    
    def get_dimension(self, module: str, dimension: str) -> Optional[int]:
        """获取特定维度值"""
        mod = getattr(self, module, None)
        if mod:
            return getattr(mod, dimension, None)
        return None
    
    def update_dimension(self, module: str, dimension: str, delta: int) -> None:
        """更新维度值（带边界检查）"""
        mod = getattr(self, module, None)
        if mod and hasattr(mod, dimension):
            current = getattr(mod, dimension)
            if isinstance(current, int):
                new_val = max(-100, min(100, current + delta))
                setattr(mod, dimension, new_val)
                # 记录历史
                self.evolution_history.append({
                    "module": module,
                    "dimension": dimension,
                    "from": current,
                    "to": new_val,
                    "delta": delta
                })
