# Theater 模块编码规范

> 剧场编排器 - 创造体验，讲述故事，放大冲突

---

## 模块定位

**Theater 是 PersonaVerse 的体验层。**

它把 Core 的"物理法则"包装成"游戏体验"：
- 设计有意义的选择情境
- 编排戏剧化的节奏
- 计算模式特定的评分
- 生成可回放的叙事

**Theater 理解人性（或机性），它创造让人想看的故事。**

---

## 核心原则

### 1. 体验优先（Experience-First）

```python
# ✅ 正确：设计有意义的冲突
class MBTIFurnace:
    def setup_stages(self):
        return [
            # 压力测试：资源 vs 道德
            ResourceDilemma(resources=3, people=5),
            # 信任测试：合作 vs 背叛
            PrisonerVariant(rounds=5),
            # 危机测试：个人 vs 群体
            SacrificeScenario(time_limit=60),
        ]

# ❌ 错误：随机的选择集合
class RandomMode:
    def setup(self):
        return [random_scenario() for _ in range(5)]  # 没有叙事意义
```

**规则**：每个情境都要服务于"揭示人格"这一目标。

### 2. 灵活编排（Flexible Orchestration）

```python
# ✅ 正确：支持动态调整
class TheaterOrchestrator:
    async def adapt_if_needed(self, theater: Theater):
        """根据进展调整节奏"""
        if theater.engagement < 0.3:
            # 注入戏剧性事件
            await self.inject_drama(theater)
        elif theater.conflict_intensity > 0.9:
            # 缓和一下，给喘息空间
            await self.inject_relief(theater)
```

**规则**：剧本是骨架，不是牢笼。根据现场反应调整。

### 3. 公平 spectatorship（观众公平）

```python
# ✅ 正确：给观察者完整信息
class Replay:
    def generate(self):
        return {
            "timeline": self.events,           # 完整事件
            "thoughts": self.agent_thoughts,   # 内心独白（上帝视角）
            "highlights": self.key_moments,    # 精彩时刻标记
            "stats": self.statistics,          # 统计数据
        }
```

**规则**：Observer 是 Theater 的重要用户，回放体验要精致。

### 4. 模式正交（Mode Orthogonality）

```python
# ✅ 正确：模式之间不依赖
class MurderMystery(GameMode):
    def run(self, context):
        # 只依赖 Core API，不依赖其他 Theater 模块
        scenario = await core.create_scenario(...)
        # ...

# ❌ 错误：模式之间强耦合
class MurderMystery(GameMode):
    def run(self):
        # 不要这样
        furnace = MBTIFurnace()
        furnace.pre_run(self.agents)  # 依赖其他模式
```

**规则**：每个模式可以独立运行，也可以组合，但不互相依赖。

---

## 目录组织

```
theater/src/
├── modes/              # 游戏模式
│   └── 规则：
│       - 每个模式独立文件
│       - 必须继承 GameMode 基类
│       - 必须实现 setup/run/score
│       - 可以有专属场景（放在 stages/ 下）
│
├── stages/             # 场景库（按模式分子目录）
│   ├── furnace/
│   ├── murder/
│   └── gaokao/
│   └── 规则：
│       - 场景模板可复用
│       - 参数化配置（不要硬编码）
│       - 有明确的人格探测目标
│
├── orchestrator.py     # 编排器
│   └── 规则：
│       - 管理剧场生命周期
│       - 协调与 Core 的交互
│       - 处理异常和干预
│
├── matchmaking.py      # 匹配系统
│   └── 规则：
│       - 支持按属性匹配
│       - 支持随机匹配
│       - 支持人工指定
│
├── scoring.py          # 评分系统
│   └── 规则：
│       - 每个模式独立评分逻辑
│       - 评分维度与模式目标一致
│       - 支持相对排名和绝对评价
│
└── api.py              # API层
    └── 规则：
        - 提供模式列表
        - 提供剧场管理
        - 提供回放接口
```

---

## 游戏模式规范

### 模式基类

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ModeResult:
    theater_id: str
    mode: str
    participants: list[str]
    duration: timedelta
    highlights: list[Highlight]
    scores: dict[str, ScoreReport]  # agent_id -> score
    personality_insights: dict[str, Insight]

class GameMode(ABC):
    """游戏模式基类"""
    
    # 模式元数据
    name: str = ""
    description: str = ""
    min_players: int = 1
    max_players: int = 10
    duration_estimate: timedelta = timedelta(minutes=30)
    
    @abstractmethod
    async def setup(self, players: list[Agent]) -> ModeContext:
        """
        初始化模式
        返回模式运行所需的上下文
        """
        pass
    
    @abstractmethod
    async def run(self, context: ModeContext) -> ModeResult:
        """
        运行完整模式
        这是主要的编排逻辑
        """
        pass
    
    @abstractmethod
    def score(self, context: ModeContext) -> dict[str, ScoreReport]:
        """
        计算评分
        每个模式有自己的评分维度
        """
        pass
    
    def validate_players(self, players: list[Agent]) -> bool:
        """验证参与人数，可重写"""
        return self.min_players <= len(players) <= self.max_players
```

### 模式实现示例

```python
class MBTIFurnace(GameMode):
    """人格熔炉：极端情境下的人格探测"""
    
    name = "人格熔炉"
    description = "通过连续压力测试，暴露AI的真实人格"
    min_players = 1
    max_players = 8
    duration_estimate = timedelta(minutes=30)
    
    async def setup(self, players: list[Agent]) -> FurnaceContext:
        # 创建熔炉专属场景
        stages = [
            await self.create_stage("submarine", players),
            await self.create_stage("lifeboat", players),
            await self.create_stage("betrayal", players),
        ]
        
        return FurnaceContext(
            players=players,
            stages=stages,
            current_stage_idx=0,
            stress_records=[],  # 记录压力反应
        )
    
    async def run(self, ctx: FurnaceContext) -> ModeResult:
        for stage in ctx.stages:
            # 在 Core 中创建情境
            scenario = await core.create_scenario(
                template=stage.template,
                participants=ctx.players,
            )
            
            # 运行直到完成
            while scenario.status != "completed":
                # 等待 Core 推进
                await self.wait_for_advance(scenario)
                
                # 记录关键反应
                ctx.stress_records.append(
                    self.record_stress_reaction(scenario)
                )
                
                # 可能注入额外压力
                if self.should_intensify(scenario):
                    await self.inject_pressure(scenario)
            
            # 阶段间过渡
            await self.stage_transition(ctx, stage)
        
        return ModeResult(
            theater_id=ctx.theater_id,
            mode=self.name,
            # ...
        )
    
    def score(self, ctx: FurnaceContext) -> dict[str, ScoreReport]:
        scores = {}
        for agent in ctx.players:
            # 计算该 Agent 的熔炉评分
            scores[agent.id] = FurnaceScore(
                stress_response=self.analyze_stress(ctx.stress_records, agent),
                moral_consistency=self.check_moral_pattern(agent),
                cognitive_shift=self.detect_cognitive_change(agent),
            )
        return scores
```

---

## 场景设计规范

### 场景模板结构

```python
@dataclass
class ScenarioTemplate:
    """场景模板"""
    id: str
    name: str
    description: str
    
    # 参与配置
    min_players: int
    max_players: int
    
    # 选择树
    choice_tree: ChoiceTree
    
    # 人格探测目标
    detection_targets: list[DetectionTarget]
    
    # 参数（可覆盖）
    parameters: dict[str, Any]
    
    # 结束条件
    end_conditions: list[EndCondition]

@dataclass
class DetectionTarget:
    """人格探测目标"""
    dimension: str           # 如 "cognitive.Fi"
    scenario_node: str       # 触发节点
    measurement: str         # 测量方式
```

### 场景配置示例（YAML）

```yaml
# stages/furnace/submarine.yaml
id: submarine_sinking
name: 潜艇沉没
description: 氧气泄漏，必须做出选择

min_players: 2
max_players: 8

detection_targets:
  - dimension: cognitive.Se
    node: initial_response
    measurement: reaction_time  # 反应时间
  
  - dimension: moral.care_harm
    node: rescue_decision
    measurement: choice_value
  
  - dimension: social.conflict_style
    node: group_discussion
    measurement: interaction_pattern

parameters:
  oxygen_depletion_rate: 10  # 每秒消耗
  escape_pod_capacity: 3
  
choice_tree:
  root:
    id: leak_discovered
    description: 发现氧气泄漏，还有5分钟
    timeout: 30
    choices:
      - id: seal_leak
        description: 尝试封住泄漏点
        leads_to: seal_attempt
      
      - id: call_help
        description: 呼叫其他舱室求助
        leads_to: waiting_rescue
      
      - id: evacuate
        description: 立即撤离
        leads_to: evacuation_scramble

end_conditions:
  - type: timeout
    duration: 300  # 5分钟
  
  - type: all_escaped
  
  - type: all_dead
```

---

## 评分系统规范

### 评分报告结构

```python
@dataclass
class ScoreReport:
    """单个 Agent 的评分报告"""
    agent_id: str
    
    # 模式特定分数
    dimension_scores: dict[str, float]  # 如 {"leadership": 85}
    
    # 人格洞察
    insights: list[Insight]
    
    # 高光时刻
    highlights: list[Highlight]
    
    # 变化追踪
    personality_changes: DimensionChanges

@dataclass
class Insight:
    """人格洞察"""
    type: str              # "strength", "weakness", "pattern"
    description: str       # 描述
    evidence: list[str]    # 证据（事件ID）
    confidence: float      # 置信度 0-1
```

### 评分原则

1. **相对与绝对结合**：既有与他人的比较，也有绝对标准的评价
2. **过程与结果并重**：不仅看最终选择，也看决策过程
3. **多维不聚合**：保持维度独立，不提供"总分"

---

## 与 Core 的交互规范

```python
# ✅ 正确：通过 API 调用 Core
class TheaterOrchestrator:
    def __init__(self, core_client: CoreClient):
        self.core = core_client
    
    async def create_scenario(self, template, players):
        return await self.core.scenarios.create(
            template=template,
            participants=[p.id for p in players],
        )
    
    async def get_scenario_state(self, scenario_id):
        return await self.core.scenarios.get_state(scenario_id)
    
    async def subscribe_events(self, scenario_id, callback):
        return await self.core.events.subscribe(
            scenario_id=scenario_id,
            handler=callback,
        )

# ❌ 错误：直接访问 Core 数据库
# 不要这样
def get_agent_state(agent_id):
    return core_database.query(...)  # 禁止
```

---

## 命名规范

### 文件命名
- `modes/{snake_case_mode}.py`
- `stages/{mode}/{scenario_name}.yaml`

### 类命名
```python
# 模式
class MBTIFurnace(GameMode)
class MurderMystery(GameMode)
class GaokaoBattle(GameMode)

# 场景
class SubmarineStage
class BetrayalDinnerStage

# 上下文
class FurnaceContext(ModeContext)
class MurderContext(ModeContext)
```

### 函数命名
```python
# 编排
setup_stages()
run_sequence()
adapt_pacing()
inject_drama()

# 评分
calculate_scores()
generate_insights()
extract_highlights()
```

---

## 错误处理

```python
class TheaterException(Exception):
    pass

class ModeConfigurationError(TheaterException):
    """模式配置错误"""
    pass

class InsufficientPlayers(TheaterException):
    """人数不足"""
    pass

class ScenarioTimeout(TheaterException):
    """场景超时（可恢复）"""
    pass

# 处理策略
async def run_mode(mode, players):
    try:
        return await mode.run(players)
    except InsufficientPlayers as e:
        # 通知用户， graceful 退出
        await notify_user(f"需要 {mode.min_players} 人，当前只有 {len(players)}")
        raise  # 向上抛，让 API 层处理
    except ScenarioTimeout:
        # 自动处理：强制推进
        await force_advance(mode.current_scenario)
    except Exception as e:
        # 未知错误：记录并尝试保存状态
        logger.exception("Mode crashed")
        await emergency_save(mode)
        raise TheaterException("模式运行异常") from e
```

---

## 一句话总结

> Theater 是故事的编织者：创造冲突，揭示人性，让人想看下去。
