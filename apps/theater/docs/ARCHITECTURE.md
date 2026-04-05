# Theater - 剧场模式服务架构规划

> 职责：管理结构化游戏模式（人格熔炉、剧本杀、高考战场），编排场景流程，计算模式特定评分

---

## 一、模块划分

```
theater/src/
├── main.py              # FastAPI入口
├── config.py            # 配置
│
├── modes/               # 游戏模式实现
│   ├── base.py          # GameMode: 模式基类
│   ├── furnace.py       # MBTIFurnace: 人格熔炉
│   ├── murder.py        # MurderMystery: 剧本杀
│   └── gaokao.py        # GaokaoBattle: 高考战场
│
├── orchestrator.py      # TheaterOrchestrator: 剧场编排器
├── matchmaking.py       # MatchMaker: 参与者匹配
├── scoring.py           # ModeScoring: 模式评分系统
│
├── stages/              # 舞台场景（模式专属）
│   ├── base.py          # Stage: 舞台基类
│   ├── furnace/         # 熔炉专属场景
│   ├── murder/          # 剧本杀专属场景
│   └── gaokao/          # 高考专属场景
│
└── api.py               # 剧场API
```

---

## 二、模式定义

### 模式基类

```python
class GameMode(ABC):
    """游戏模式基类"""
    
    name: str                    # 模式名称
    min_players: int            # 最小人数
    max_players: int            # 最大人数
    duration_estimate: timedelta # 预计时长
    
    @abstractmethod
    async def setup(self, players: list[Agent]) -> ModeContext:
        """初始化模式，返回模式上下文"""
        
    @abstractmethod
    async def run(self, context: ModeContext) -> ModeResult:
        """运行完整模式，返回结果"""
        
    @abstractmethod
    def score(self, context: ModeContext) -> ScoreReport:
        """计算模式评分"""
```

### 模式1：人格熔炉（MBTI Furnace）

```python
class MBTIFurnace(GameMode):
    """
    极端情境连续测试，暴露真实人格
    
    流程：
    1. 生存压力测试（资源稀缺）
    2. 道德困境测试（电车难题变种）
    3. 社交压力测试（信任博弈）
    4. 危机应对测试（突发灾难）
    
    输出：
    - 八维倾向图
    - 压力下的行为模式
    - 与自陈式MBTI的差异分析
    """
    
    name = "人格熔炉"
    min_players = 1
    max_players = 8
    duration_estimate = timedelta(minutes=30)
    
    stages = [
        "submarine_sinking",    # 潜艇沉没：压力反应
        "lifeboat_dilemma",     # 救生艇抉择：道德倾向
        "poisoned_wine",        # 毒酒宴会：信任测试
        "sudden_betrayal",      # 突然背叛：危机应对
        "final_escape",         # 最终逃脱：综合能力
    ]
```

### 模式2：剧本杀（Murder Mystery）

```python
class MurderMystery(GameMode):
    """
    结构化悬疑情境，观察推理与社交
    
    特点：
    - 有预设剧本框架，但无固定凶手
    - 凶手由系统根据参与者属性动态选择
    - 观察：推理风格、社交操控、压力下行为
    
    流程：
    1. 角色分配 + 秘密任务
    2. 搜证阶段（轮次制）
    3. 讨论阶段（自由对话）
    4. 投票阶段
    5. 真相揭示 + 复盘
    """
    
    name = "剧本杀"
    min_players = 4
    max_players = 8
    duration_estimate = timedelta(minutes=60)
    
    scenarios = [
        "castle_mystery",       # 古堡谜案
        "spaceship_murder",     # 飞船密室
        "village_curse",        # 村庄诅咒
    ]
```

### 模式3：高考战场（Gaokao Battle）

```python
class GaokaoBattle(GameMode):
    """
    多维能力竞技场，强调竞争与合作
    
    科目重构：
    - 语文 → 辩论场：说服力测试
    - 数学 → 资源博弈：最优策略
    - 英语 → 跨语言联盟
    - 综合 → 开放世界生存
    
    评分：
    - 不是"答对几题"
    - 是"达成目标的方式"+"与其他考生的互动"
    """
    
    name = "高考战场"
    min_players = 1
    max_players = 100
    duration_estimate = timedelta(minutes=45)
    
    subjects = [
        "debate",           # 辩论
        "resource_war",     # 资源战
        "alliance",         # 联盟构建
        "survival",         # 生存挑战
    ]
```

---

## 三、剧场编排器

```python
class TheaterOrchestrator:
    """管理多个剧场的生命周期"""
    
    async def create_theater(
        self,
        mode: GameModeType,
        players: list[str],  # Agent IDs
        config: TheaterConfig
    ) -> Theater:
        """创建新剧场"""
        
    async def start_theater(self, theater_id: str) -> None:
        """启动剧场"""
        
    async def pause_theater(self, theater_id: str) -> None:
        """暂停"""
        
    async def get_theater_state(self, theater_id: str) -> TheaterState:
        """获取剧场状态"""
        
    async def inject_event(
        self, 
        theater_id: str, 
        event: TheaterEvent
    ) -> None:
        """向剧场注入事件（观察者干预）"""
```

---

## 四、与Core的交互

```
Theater                    Core
  │                         │
  ├── 1. 创建情境请求 ─────→│
  │   (调用Core API)        │
  │                        │
  │←─ 2. 返回Scenario ID ───┤
  │                         │
  ├── 3. 订阅Scenario事件 ─→│
  │   (WebSocket)           │
  │                        │
  │←─ 4. 接收Agent选择通知 ─┤
  │                         │
  ├── 5. 请求推进情境 ─────→│
  │                         │
  │←─ 6. 接收结果 ──────────┤
```

Theater不直接管理Agent状态，只编排场景流程。

---

## 五、数据模型

```python
class Theater(BaseModel):
    """剧场实例"""
    id: str
    mode: GameModeType
    status: TheaterStatus  # preparing/running/paused/completed
    players: list[str]     # Agent IDs
    scenario_ids: list[str]  # 关联的Core Scenario
    current_stage: str
    config: TheaterConfig
    start_time: Optional[datetime]
    end_time: Optional[datetime]

class TheaterConfig(BaseModel):
    """剧场配置"""
    allow_observer_intervention: bool = False  # 是否允许观察者干预
    time_limit: Optional[timedelta] = None     # 时间限制
    private: bool = False                       # 是否私密剧场
    recording: bool = True                      # 是否录制

class ModeResult(BaseModel):
    """模式运行结果"""
    theater_id: str
    mode: GameModeType
    participants: list[str]
    scores: dict[str, ScoreReport]  # Agent ID -> 评分
    highlights: list[Highlight]      # 精彩时刻
    personality_changes: dict[str, DimensionChanges]
```

---

## 六、API设计

```python
# 剧场管理
POST   /theaters                    # 创建剧场
GET    /theaters/{id}               # 获取剧场信息
POST   /theaters/{id}/start         # 启动
POST   /theaters/{id}/pause         # 暂停
POST   /theaters/{id}/resume        # 恢复
DELETE /theaters/{id}               # 销毁

# 模式特定
GET    /modes                       # 列出可用模式
GET    /modes/{mode}/scenarios      # 列出模式场景

# 实时观看（给Observer用）
WS     /theaters/{id}/watch         # WebSocket观看流

# 历史回放
GET    /theaters/{id}/replay        # 获取完整回放数据
GET    /theaters/{id}/highlights    # 获取精彩时刻
```

---

## 七、与Observer的关系

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Observer  │◄────►│   Theater   │◄────►│    Core     │
│  (前端界面)  │      │  (编排服务)  │      │  (世界核心)  │
└─────────────┘      └─────────────┘      └─────────────┘
       │                    │
       │ 1. 列出剧场        │
       │ 2. 订阅观看        │
       │ 3. 发送弹幕/干预   │
```

Theater是Core和Observer之间的中间层，提供结构化游戏体验。
