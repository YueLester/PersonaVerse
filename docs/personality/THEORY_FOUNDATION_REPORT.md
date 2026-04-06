# PersonaVerse 人格理论基础与应用报告

> **调研范围**：经典性格理论、认知心理学、社会心理学、动机与情绪理论、进化与跨文化心理学  
> **调研时间**：2026年4月5日  
> **核心产出**：60+ 本核心理论书籍、40+ 维度建模框架、系统化应用建议

---

## 📋 目录

1. [执行摘要](#执行摘要)
2. [核心理论体系](#核心理论体系)
3. [完整书单与理论详解](#完整书单与理论详解)
4. [PersonaVerse 应用框架](#personaverse-应用框架)
5. [选择分叉树设计指南](#选择分叉树设计指南)
6. [实施路线图](#实施路线图)

---

## 执行摘要

### 调研目标

为 PersonaVerse AI 人格模拟系统寻找科学、系统、全面的心理学理论基础，特别关注：
- 可用于**选择分叉树**设计的性格-行为预测模型
- **五层维度系统**（认知、星象、道德、社交、表象）的理论支撑
- **40+ 人格维度**的科学定义与测量方法

### 核心发现

| 领域 | 核心理论 | 关键贡献 |
|------|----------|----------|
| **性格结构** | Big Five + HEXACO H | 6维度核心骨架，30个facets细分特质 |
| **认知机制** | 双过程理论 + 前景理论 | System 1/2 决策权重、损失厌恶参数 |
| **社会行为** | 依恋理论 + 社会认同 + Goffman拟剧论 | 关系动态、群体行为、印象管理 |
| **动机驱动** | 自我决定理论 (SDT) | 自主、胜任、关联三需求 |
| **情绪调节** | Gross过程模型 + Ekman基本情绪 | 5种调节策略 × 7种基本情绪 |
| **道德判断** | Haidt道德基础理论 | 6大道德基础（与现有设计完全对应） |
| **进化基础** | 生命史理论 + Buss择偶策略 | 快-慢策略、性别差异、情感功能 |
| **文化维度** | Nisbett思维地理学 + Ubuntu | 分析/整体认知、关系主义自我 |

### 推荐核心框架

```python
persona_vector = {
    # === 核心特质层 (Big Five + HEXACO) ===
    "openness": 75,           # 开放性：幻想、美学、思想、价值观
    "conscientiousness": 60,  # 尽责性：胜任、秩序、成就追求、自律
    "extraversion": 80,       # 外向性：热情、合群、果断、活跃
    "agreeableness": 45,      # 宜人性：信任、坦诚、利他、同理心
    "neuroticism": 30,        # 神经质：焦虑、抑郁、冲动、脆弱
    "honesty_humility": 70,   # 诚实-谦逊：真诚、贪婪规避、谦虚
    
    # === 认知风格层 ===
    "system1_weight": 0.65,       # System 1 (直觉) 权重
    "field_independence": 0.7,    # 场独立性 (0=依存, 1=独立)
    "loss_aversion": 2.25,        # 损失厌恶系数 (λ)
    "cognitive_capacity": 5,      # 工作记忆容量 (chunks)
    
    # === 动机驱动层 (SDT) ===
    "autonomy_need": 0.8,         # 自主需求
    "competence_need": 0.7,       # 胜任需求
    "relatedness_need": 0.6,      # 关联需求
    
    # === 情绪特质层 ===
    "emotion_regulation_style": "cognitive_reappraisal",  # 认知重评/表达抑制
    "empathy_perspective_taking": 75,  # 观点采择能力
    "empathy_concern": 80,             # 共情关怀
    
    # === 道德基础层 (Haidt) ===
    "care_harm": 80,              # 关怀/伤害
    "fairness_cheating": 75,      # 公平/欺骗
    "loyalty_betrayal": 60,       # 忠诚/背叛
    "authority_subversion": 50,   # 权威/颠覆
    "sanctity_degradation": 45,   # 神圣/堕落
    "liberty_oppression": 70,     # 自由/压迫
    
    # === 社交策略层 ===
    "attachment_style": "secure",     # 安全/焦虑/回避
    "conflict_mode": "collaborate",   # 竞争/协作/妥协/回避/迁就
    "social_style": "expressive",     # 驱动/和蔼/表达/分析
    "face_concern": 65,               # 面子关注度
    
    # === 表象管理层 ===
    "self_monitoring": 70,        # 自我监控（印象管理能力）
    "authenticity": 55,           # 真实性（前台vs后台一致性）
    
    # === 进化参数层 ===
    "life_history_strategy": "slow",  # 快/慢生命史策略
    "sensory_processing_sensitivity": 30,  # 感觉处理敏感度 (HSP)
    "empathizing": 75,            # 共情能力 (E-S理论)
    "systemizing": 45,            # 系统化能力
    
    # === 文化背景层 ===
    "cultural_cognition": "holistic",   # 整体/分析性思维
    "individualism_collectivism": "horizontal_individualism",
    "power_distance": 40,
}
```

---

## 核心理论体系

### 五层架构理论映射

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PersonaVerse 五层维度架构                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ★ 表象层 (Presentation)                                                    │
│  ├── Goffman 拟剧论 - 前台/后台行为分离                                      │
│  ├── 自我监控理论 (Snyder) - 印象管理能力                                    │
│  ├── 面子理论 (Brown & Levinson) - 礼貌策略                                  │
│  └── 沟通风格模型 - 直接/间接、表达/分析                                      │
│                                                                             │
│  ★ 社交层 (Social)                                                          │
│  ├── 依恋理论 (Bowlby/Ainsworth) - 关系底层架构                              │
│  ├── 社会交换理论 (Thibaut & Kelley) - 成本收益决策                          │
│  ├── 关系模型理论 (Fiske) - CS/AR/EM/MP 四种关系                             │
│  ├── 社会认同理论 (Tajfel & Turner) - 群体归属                               │
│  ├── Thomas-Kilmann 冲突模式 - 五种冲突处理                                   │
│  └── Davis 同理心模型 - 观点采择/共情关怀                                    │
│                                                                             │
│  ★ 道德层 (Moral)                                                           │
│  ├── 道德基础理论 (Haidt) - 六大道德基础 ✓ (已对应)                          │
│  ├── Schwartz 价值观理论 - 10种基本价值观                                    │
│  ├── Kohlberg 道德发展 - 三水平六阶段                                        │
│  └── Dark/Light Triad - 道德极性                                            │
│                                                                             │
│  ★ 星象层 (Energy/Archetype)                                                │
│  ├── 生命史理论 (Del Giudice) - 快/慢策略                                    │
│  ├── 感觉处理敏感度 (Aron) - HSP特质                                        │
│  ├── 心理韧性 (Masten) - 应对与恢复                                         │
│  └── 九型人格 (Riso & Hudson) - 核心恐惧与欲望                               │
│                                                                             │
│  ★ 认知层 (Cognitive)                                                       │
│  ├── Big Five + 30 Facets - 核心特质                                        │
│  ├── 双过程理论 (Kahneman) - System 1/2                                     │
│  ├── 前景理论 (Kahneman & Tversky) - 风险态度                               │
│  ├── 场依存/场独立 (Witkin) - 认知风格                                      │
│  ├── 工作记忆模型 (Baddeley) - 信息处理容量                                  │
│  └── 共情-系统化 (Baron-Cohen) - E-S认知风格                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 核心理论网络图

```
                            ┌─────────────────────┐
                            │    进化基础层        │
                            │ (Buss, Trivers,     │
                            │  Del Giudice)       │
                            └──────────┬──────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    ↓                  ↓                  ↓
           ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
           │   性格结构    │   │   动机驱动    │   │   认知机制    │
           │ (Big Five    │   │ (SDT, Maslow, │   │ (Dual Process│
           │  + HEXACO)   │   │  McClelland) │   │  Prospect)   │
           └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
                  │                  │                  │
                  └──────────────────┼──────────────────┘
                                     ↓
                           ┌──────────────────┐
                           │   行为输出层      │
                           │ (决策/社交/情绪  │
                           │  /道德表达)      │
                           └────────┬─────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           ↓                        ↓                        ↓
    ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
    │   情境响应    │        │   文化调节    │        │   叙事整合    │
    │ (Gross情绪    │        │ (Hofstede,   │        │ (McAdams生命  │
    │  调节, TKI)   │        │  Nisbett)    │        │  故事)       │
    └──────────────┘        └──────────────┘        └──────────────┘
```

---

## 完整书单与理论详解

### 第一优先级：必读核心（15本）

#### 性格结构与特质

| # | 书名 | 作者 | 年份 | 核心理论 | AI适用性 |
|---|------|------|------|----------|----------|
| 1 | *Personality in Adulthood* | Costa & McCrae | 2003 | Big Five 毕生发展 | ⭐⭐⭐⭐⭐ |
| 2 | *The H Factor of Personality* | Lee & Ashton | 2012 | HEXACO 第六维度 | ⭐⭐⭐⭐⭐ |
| 3 | *Handbook of Personality* (3rd Ed.) | John et al. (Eds.) | 2008 | 综合参考手册 | ⭐⭐⭐⭐⭐ |

#### 认知与决策

| # | 书名 | 作者 | 年份 | 核心理论 | AI适用性 |
|---|------|------|------|----------|----------|
| 4 | *Thinking, Fast and Slow* | Daniel Kahneman | 2011 | 双过程理论 | ⭐⭐⭐⭐⭐ |
| 5 | *Judgment under Uncertainty* | Kahneman, Tversky, Slovic | 1982 | 启发式与偏差 | ⭐⭐⭐⭐⭐ |
| 6 | *Administrative Behavior* | Herbert Simon | 1947/1997 | 有限理性 | ⭐⭐⭐⭐⭐ |

#### 社会与关系

| # | 书名 | 作者 | 年份 | 核心理论 | AI适用性 |
|---|------|------|------|----------|----------|
| 7 | *The Presentation of Self in Everyday Life* | Erving Goffman | 1959 | 拟剧论/印象管理 | ⭐⭐⭐⭐⭐ |
| 8 | *Attachment and Loss* (Vol.1) | John Bowlby | 1969 | 依恋理论 | ⭐⭐⭐⭐⭐ |
| 9 | *Social Psychology of Groups* | Thibaut & Kelley | 1959 | 社会交换理论 | ⭐⭐⭐⭐⭐ |

#### 动机与道德

| # | 书名 | 作者 | 年份 | 核心理论 | AI适用性 |
|---|------|------|------|----------|----------|
| 10 | *Self-Determination Theory* | Deci & Ryan | 1985/2017 | 自我决定理论 | ⭐⭐⭐⭐⭐ |
| 11 | *The Righteous Mind* | Jonathan Haidt | 2012 | 道德基础理论 | ⭐⭐⭐⭐⭐ |
| 12 | *Handbook of Emotion Regulation* | James Gross (Ed.) | 2007/2014 | 情绪调节 | ⭐⭐⭐⭐⭐ |

#### 进化与多样性

| # | 书名 | 作者 | 年份 | 核心理论 | AI适用性 |
|---|------|------|------|----------|----------|
| 13 | *The Evolution of Desire* | David Buss | 1994/2016 | 择偶策略 | ⭐⭐⭐⭐⭐ |
| 14 | *Evolutionary Psychopathology* | Marco Del Giudice | 2018 | 生命史理论 | ⭐⭐⭐⭐⭐ |
| 15 | *The Geography of Thought* | Richard Nisbett | 2003 | 思维地理学 | ⭐⭐⭐⭐⭐ |

---

### 第二优先级：深度扩展（25本）

#### 性格理论扩展

| 书名 | 作者 | 核心理论 |
|------|------|----------|
| *The Wisdom of the Enneagram* | Riso & Hudson | 九型人格 |
| *Essentials of 16PF Assessment* | Cattell & Schuerger | 16PF特质 |
| *The Dark Side of Personality* | Zeigler-Hill & Marcus | Dark Triad |
| *The Highly Sensitive Person* | Elaine Aron | HSP特质 |
| *The Essential Difference* | Simon Baron-Cohen | E-S理论 |

#### 认知心理学

| 书名 | 作者 | 核心理论 |
|------|------|----------|
| *Working Memory, Thought, and Action* | Alan Baddeley | 工作记忆模型 |
| *Cognitive Styles: Essence and Origins* | Witkin & Goodenough | FDI认知风格 |
| *The Psychology of Personal Constructs* | George Kelly | 个人建构理论 |
| *Prospect Theory: For Risk and Ambiguity* | Peter Wakker | 前景理论数学 |
| *Cognitive Load Theory* | John Sweller | 认知负荷理论 |

#### 社会心理学

| 书名 | 作者 | 核心理论 |
|------|------|----------|
| *Structures of Social Life* | Alan Fiske | 关系模型理论 |
| *Obedience to Authority* | Stanley Milgram | 服从研究 |
| *The Social Psychology of Intergroup Relations* | Tajfel & Turner | 社会认同理论 |
| *Politeness* | Brown & Levinson | 礼貌理论 |
| *Interaction Ritual* | Erving Goffman | 面子与互动 |

#### 动机与情绪

| 书名 | 作者 | 核心理论 |
|------|------|----------|
| *Drive: The Surprising Truth* | Daniel Pink | 驱动力3.0 |
| *Emotions Revealed* | Paul Ekman | 基本情绪理论 |
| *Descartes' Error* | Antonio Damasio | 躯体标记假说 |
| *The Achieving Society* | David McClelland | 成就动机理论 |
| *A Theory of Goal Setting* | Locke & Latham | 目标设置理论 |

#### 进化与跨文化

| 书名 | 作者 | 核心理论 |
|------|------|----------|
| *The Selfish Gene* | Richard Dawkins | 基因选择论 |
| *The Evolution of Reciprocal Altruism* | Robert Trivers | 互惠利他 |
| *Culture's Consequences* | Geert Hofstede | 文化维度 |
| *Individualism and Collectivism* | Harry Triandis | 个体/集体主义 |
| *The Stories We Live By* | Dan McAdams | 叙事身份理论 |

---

### 第三优先级：专业参考（20+本）

- *The Personality Puzzle* (Funder, 2019) - 综合教材
- *Me, Myself, and Us* (Little, 2014) - 通俗科学
- *Social Style/Management Style* (Bolton & Bolton, 1984) - 沟通风格
- *Thomas-Kilmann Conflict Mode Instrument* (Thomas & Kilmann, 1974) - 冲突处理
- *The Power of Habit* (Duhigg, 2012) / *Atomic Habits* (Clear, 2018) - 习惯形成
- *Bowling Alone* (Putnam, 2000) - 社会资本
- *Ubuntu* (Mbiti, Tutu) - 非洲哲学
- 杨国枢 *中国人的心理与行为* - 本土心理学
- *Ordinary Magic* (Masten, 2014) - 心理韧性
- *Posttraumatic Growth* (Tedeschi & Calhoun, 2014) - 创伤后成长
- *Emotional Intelligence* (Goleman, 1995) - 情绪智力
- *The Feeling of What Happens* (Damasio, 1999) - 意识与情绪
- *Mindset* (Dweck, 2006) - 成长型思维
- *Grit* (Duckworth, 2016) - 坚毅理论
- *Flow* (Csikszentmihalyi, 1990) - 心流体验

---

## PersonaVerse 应用框架

### 人格向量模型 v2.0

基于调研结果，建议采用以下**可量化参数体系**：

```python
@dataclass
class PersonaProfile:
    """PersonaVerse 人格配置完整模型"""
    
    # ===== 基础特质层 (Big Five + HEXACO) =====
    # 范围: 0-100，50为人群平均水平
    openness: int                    # 开放性
    conscientiousness: int           # 尽责性
    extraversion: int                # 外向性
    agreeableness: int               # 宜人性
    neuroticism: int                 # 神经质
    honesty_humility: int            # 诚实-谦逊 (HEXACO新增)
    
    # 30个Facets细分 (可选，用于精细建模)
    facets: Dict[str, int] = field(default_factory=dict)
    
    # ===== 认知处理层 =====
    system1_dominance: float         # System 1权重 (0-1)
    field_independence: float        # 场独立性 (0-1)
    loss_aversion_coefficient: float # 损失厌恶λ (1.0-3.0)
    working_memory_capacity: int     # 工作记忆容量 (3-7)
    need_for_cognition: int          # 认知需求 (0-100)
    
    # ===== 动机驱动层 (SDT) =====
    autonomy_need: float             # 自主需求 (0-1)
    competence_need: float           # 胜任需求 (0-1)
    relatedness_need: float          # 关联需求 (0-1)
    
    # 成就动机 (McClelland)
    need_achievement: int            # 成就需要 (0-100)
    need_power: int                  # 权力需要 (0-100)
    need_affiliation: int            # 亲和需要 (0-100)
    
    # ===== 情绪特质层 =====
    emotion_regulation_strategy: str  # "cognitive_reappraisal" / "expressive_suppression"
    emotional_stability: int         # 情绪稳定性 (0-100)
    sensory_processing_sensitivity: int  # HSP敏感度 (0-100)
    
    # 同理心四维度 (Davis IRI)
    empathy_perspective_taking: int  # 观点采择 (0-100)
    empathy_empathic_concern: int    # 共情关怀 (0-100)
    empathy_personal_distress: int   # 个人痛苦 (0-100)
    empathy_fantasy: int             # 幻想倾向 (0-100)
    
    # 共情-系统化 (Baron-Cohen)
    empathizing_quotient: int        # 共情商数 (0-100)
    systemizing_quotient: int        # 系统商数 (0-100)
    
    # ===== 道德基础层 (Haidt) =====
    # 范围: -100 到 +100，正值表示重视该基础
    care_harm: int                   # 关怀/伤害
    fairness_cheating: int           # 公平/欺骗
    loyalty_betrayal: int            # 忠诚/背叛
    authority_subversion: int        # 权威/颠覆
    sanctity_degradation: int        # 神圣/堕落
    liberty_oppression: int          # 自由/压迫
    
    # 道德极性
    dark_triad_score: int            # 黑暗三联征 (-100 到 100)
    light_triad_score: int           # 光明三联征 (-100 到 100)
    
    # ===== 社交策略层 =====
    # 依恋风格
    attachment_anxiety: int          # 依恋焦虑 (0-100)
    attachment_avoidance: int        # 依恋回避 (0-100)
    
    # 冲突处理模式 (TKI)
    conflict_competing: int          # 竞争倾向 (0-100)
    conflict_collaborating: int      # 协作倾向 (0-100)
    conflict_compromising: int       # 妥协倾向 (0-100)
    conflict_avoiding: int           # 回避倾向 (0-100)
    conflict_accommodating: int      # 迁就倾向 (0-100)
    
    # 社交风格 (DISC-based)
    dominance_style: int             # 支配型倾向 (0-100)
    influence_style: int             # 影响型倾向 (0-100)
    steadiness_style: int            # 稳健型倾向 (0-100)
    compliance_style: int            # 谨慎型倾向 (0-100)
    
    # 面子关注 (跨文化)
    face_concern_self: int           # 自我面子关注 (0-100)
    face_concern_other: int          # 他人面子关注 (0-100)
    
    # ===== 表象管理层 =====
    self_monitoring: int             # 自我监控 (0-100)
    public_self_consciousness: int   # 公众自我意识 (0-100)
    authenticity: int                # 真实性 (0-100)
    
    # ===== 进化与适应层 =====
    life_history_strategy: str       # "fast" / "slow" / "balanced"
    life_history_speed_score: int    # 生命史速度 (0-100)
    
    # 韧性
    resilience: int                  # 心理韧性 (0-100)
    post_traumatic_growth: int       # 创伤后成长倾向 (0-100)
    
    # ===== 文化背景层 =====
    # 认知风格
    cognitive_style: str             # "analytic" / "holistic"
    
    # 个体主义-集体主义 (Triandis)
    ic_orientation: str              # "HI" / "VI" / "HC" / "VC"
    
    # 霍夫斯泰德维度
    power_distance: int              # 权力距离 (0-100)
    uncertainty_avoidance: int       # 不确定性规避 (0-100)
    long_term_orientation: int       # 长期导向 (0-100)
    indulgence: int                  # 放纵 (0-100)
    
    # ===== 叙事与身份层 =====
    narrative_coherence: int         # 叙事连贯性 (0-100)
    self_continuity: int             # 自我连续性 (0-100)
    
    # 九型人格 (可选)
    enneagram_type: Optional[int]    # 1-9
    enneagram_wing: Optional[int]    # 侧翼
    enneagram_level: Optional[int]   # 健康层级 1-9
```

### 情境-反应映射示例

```python
# 示例：面对"同事抢功"情境的反应预测
def respond_to_credit_stealing(persona: PersonaProfile, context: Context):
    
    # Step 1: 认知评估 (双过程理论)
    if random.random() < persona.system1_dominance:
        # System 1: 直觉/情绪反应
        initial_reaction = "emotional"
    else:
        # System 2: 分析/理性评估
        initial_reaction = "analytical"
    
    # Step 2: 冲突处理模式选择 (TKI)
    conflict_scores = {
        "compete": persona.conflict_competing,
        "collaborate": persona.conflict_collaborating,
        "compromise": persona.conflict_compromising,
        "avoid": persona.conflict_avoiding,
        "accommodate": persona.conflict_accommodating
    }
    chosen_strategy = max(conflict_scores, key=conflict_scores.get)
    
    # Step 3: 道德基础权重 (Haidt)
    moral_weights = {
        "fairness": abs(persona.fairness_cheating),
        "authority": abs(persona.authority_subversion),
        "care": abs(persona.care_harm)
    }
    
    # Step 4: 情绪调节 (Gross)
    if persona.emotion_regulation_strategy == "cognitive_reappraisal":
        # 重新解读情境
        interpretation = reframe_situation(context)
    else:  # expressive_suppression
        # 抑制情绪表达
        interpretation = suppress_emotion(context)
    
    # Step 5: 面子考虑 (跨文化)
    if persona.face_concern_other > 70:
        # 保护对方面子
        approach = "indirect"
    else:
        approach = "direct"
    
    # 综合生成反应
    return generate_response(
        strategy=chosen_strategy,
        approach=approach,
        moral_salience=moral_weights,
        emotional_tone=interpretation
    )
```

---

## 选择分叉树设计指南

### 设计原则

基于调研的理论体系，选择分叉树应遵循以下原则：

```
1. 多维度触发：每个选择点应考虑 3-5 个相关人格维度
2. 权重差异：不同人格维度对选择的贡献不同
3. 情境调节：文化、社会压力等情境因素可调节人格表达
4. 非线性映射：人格参数与选择之间不是简单线性关系
5. 个体差异：保留随机性以模拟真实的人类不可预测性
```

### 情境设计模板

```python
class ChoiceNode:
    """选择分叉树节点"""
    
    def __init__(self, scenario: str, choices: List[Choice]):
        self.scenario = scenario
        self.choices = choices
    
    def predict_choice(self, persona: PersonaProfile) -> Choice:
        """基于人格预测选择"""
        scores = []
        
        for choice in self.choices:
            score = 0
            
            # 遍历该选择关联的人格维度
            for dimension, weight in choice.dimension_weights.items():
                persona_value = getattr(persona, dimension)
                
                # 计算匹配度
                if choice.target_range:
                    # 目标范围匹配
                    if choice.target_range[0] <= persona_value <= choice.target_range[1]:
                        match = 1.0
                    else:
                        distance = min(
                            abs(persona_value - choice.target_range[0]),
                            abs(persona_value - choice.target_range[1])
                        )
                        match = max(0, 1 - distance / 50)
                else:
                    # 线性相关
                    match = persona_value / 100
                
                score += match * weight
            
            scores.append((choice, score))
        
        # 基于分数概率选择
        total = sum(s for _, s in scores)
        probabilities = [s/total for _, s in scores]
        
        return random.choices(
            [c for c, _ in scores],
            weights=probabilities,
            k=1
        )[0]


# 示例：设计一个"项目失败责任归属"情境
project_failure_scenario = ChoiceNode(
    scenario="你负责的项目失败了，在团队会议上...",
    choices=[
        Choice(
            text="主动承担责任，分析自己的失误",
            dimension_weights={
                "honesty_humility": 0.3,
                "conscientiousness": 0.25,
                "conflict_accommodating": 0.2,
                "self_monitoring": 0.15
            },
            target_range=None,
            impacts={"trust": +10, "leadership": -5}
        ),
        Choice(
            text="指出团队成员的问题",
            dimension_weights={
                "dark_triad_score": 0.3,
                "conflict_competing": 0.25,
                "neuroticism": 0.2,
                "loyalty_betrayal": -0.15  # 负相关
            },
            target_range=None,
            impacts={"team_morale": -15, "accountability": +5}
        ),
        Choice(
            text="强调外部不可控因素",
            dimension_weights={
                "neuroticism": 0.25,
                "external_locus": 0.3,
                "conflict_avoiding": 0.2,
                "system1_dominance": 0.15
            },
            target_range=None,
            impacts={"credibility": -10, "stress": -5}
        ),
        Choice(
            text="提出系统性的改进方案",
            dimension_weights={
                "conscientiousness": 0.3,
                "need_achievement": 0.25,
                "systemizing_quotient": 0.2,
                "system2_dominance": 0.2  # 需要System 2
            },
            target_range=None,
            impacts={"trust": +15, "competence_perceived": +20}
        )
    ]
)
```

### 五层维度对应的情境类型

| 维度层 | 典型情境类型 | 关键触发因素 |
|--------|-------------|-------------|
| **认知层** | 信息处理、决策制定、问题解决 | 时间压力、信息复杂度、认知负荷 |
| **星象层** | 能量管理、压力应对、长期规划 | 生命事件、资源可用性、时间视角 |
| **道德层** | 伦理困境、价值冲突、正义判断 | 涉及他人利益、道德基础冲突 |
| **社交层** | 群体互动、关系维护、冲突处理 | 群体压力、关系亲疏、社会资本 |
| **表象层** | 自我呈现、印象管理、身份表达 | 观众存在、角色期望、面子威胁 |

---

## 实施路线图

### 阶段一：核心框架搭建（1-2月）

- [ ] 实现 Big Five + HEXACO H 六维度核心模型
- [ ] 集成双过程理论决策机制
- [ ] 建立基础选择分叉树结构
- [ ] 设计人格向量存储方案

### 阶段二：五层维度扩展（2-3月）

- [ ] 实现 30 Facets 细分特质
- [ ] 集成 SDT 动机驱动模型
- [ ] 实现 Haidt 道德基础判断
- [ ] 集成 Gross 情绪调节策略

### 阶段三：社会与文化层（3-4月）

- [ ] 实现依恋风格与关系动态
- [ ] 集成 Thomas-Kilmann 冲突处理
- [ ] 实现 Goffman 印象管理机制
- [ ] 添加文化背景参数

### 阶段四：高级特性（4-6月）

- [ ] 实现生命史策略动态调整
- [ ] 集成叙事身份与自我连续性
- [ ] 添加 HSP、E-S 等特殊人格模型
- [ ] 实现习惯形成与学习机制

---

## 附录

### A. 快速参考卡片

```
Big Five 速记：
O = Openness      开放/传统
C = Conscientiousness 尽责/自发  
E = Extraversion  外向/内向
A = Agreeableness 宜人/竞争
N = Neuroticism   神经质/稳定

SDT 三需求：
A = Autonomy     自主
C = Competence   胜任
R = Relatedness  关联

Haidt 六道德：
Care, Fairness, Loyalty, Authority, Sanctity, Liberty
```

### B. 推荐学习路径

1. **入门者**：Pink《Drive》→ Goleman《Emotional Intelligence》→ Haidt《The Righteous Mind》
2. **进阶者**：Kahneman《Thinking, Fast and Slow》→ Bowlby《Attachment》→ Goffman《Presentation of Self》
3. **专业者**：Costa & McCrae《Personality in Adulthood》→ Deci & Ryan《SDT》→ Buss《Evolution of Desire》

---

**报告完成时间**：2026年4月5日  
**调研团队**：多 Agent 并行调研系统  
**理论覆盖**：6大领域、60+ 本核心文献、40+ 可量化维度
