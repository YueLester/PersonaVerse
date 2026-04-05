# Core - 世界核心服务架构规划

> 职责：世界驱动引擎、人格属性计算、情境调度、Agent生命周期管理

---

## 一、模块划分

```
core/src/
├── main.py              # FastAPI入口，服务生命周期
├── config.py            # 配置管理（环境变量+Pydantic Settings）
├── deps.py              # 依赖注入（DB连接、Redis等）
│
├── world/               # 世界驱动层
│   ├── engine.py        # WorldEngine: 世界时钟、状态管理
│   ├── scheduler.py     # EventScheduler: 事件调度中心
│   ├── evolution.py     # WorldEvolution: 世界演化规则
│   └── state.py         # WorldState: 全局状态快照
│
├── agents/              # Agent管理层
│   ├── models.py        # Agent数据模型（SQLAlchemy）
│   ├── registry.py      # AgentRegistry: 注册发现
│   ├── state.py         # AgentStateManager: 状态机
│   ├── connector.py     # Connector: 外部AI接入适配
│   └── lifecycle.py     # AgentLifecycle: 生命周期钩子
│
├── personality/         # 人格维度系统
│   ├── dimensions/      # 五大维度实现
│   │   ├── cognitive.py
│   │   ├── astro.py
│   │   ├── moral.py
│   │   ├── social.py
│   │   └── surface.py
│   ├── engine.py        # PersonalityEngine: 属性计算
│   ├── profile.py       # ProfileManager: 档案管理
│   └── tags.py          # TagComputer: 标签推导
│
├── scenarios/           # 情境系统
│   ├── base.py          # Scenario: 情境基类
│   ├── tree.py          # ChoiceTree: 选择分叉树
│   ├── runner.py        # ScenarioRunner: 运行器
│   ├── builtin/         # 内置场景
│   └── registry.py      # ScenarioRegistry: 场景注册
│
├── events/              # 事件系统
│   ├── base.py          # Event: 事件基类
│   ├── system.py        # SystemEvent: 系统事件
│   ├── agent.py         # AgentEvent: Agent触发事件
│   └── bus.py           # EventBus: 事件总线
│
├── perception/          # 信息/感知系统
│   ├── layers.py        # InfoLayer: 信息层级定义
│   ├── visibility.py    # VisibilityEngine: 可见性计算
│   └── propagation.py   # InfoPropagation: 信息传播
│
└── api/                 # API层
    ├── deps.py          # API依赖
    ├── agents.py        # Agent管理接口
    ├── world.py         # 世界状态接口
    ├── scenarios.py     # 场景接口
    ├── personality.py   # 人格数据接口
    └── websocket.py     # WebSocket实时通信
```

---

## 二、核心数据流

### 1. 世界时钟循环

```
WorldEngine.tick()
    │
    ├── 1. 收集活跃Agent的决策请求
    │      └── AgentStateManager.get_pending_decisions()
    │
    ├── 2. 等待决策（有超时）
    │      └── Connector.receive_decision()
    │
    ├── 3. 决策结算
    │      ├── ScenarioRunner.resolve_choices()
    │      ├── PersonalityEngine.calculate_changes()
    │      └── EventBus.emit(outcome_events)
    │
    ├── 4. 世界演化
    │      ├── WorldEvolution.apply_consequences()
    │      ├── EventScheduler.check_triggers()
    │      └── ScenarioRunner.advance_scenarios()
    │
    └── 5. 信息分发
           └── VisibilityEngine.distribute_perceptions()
```

### 2. Agent接入流程

```
Agent连接
    │
    ├── WebSocket /agent/connect
    │   ├── 验证身份（API Key）
    │   ├── 加载或创建Agent档案
    │   └── 注册到AgentRegistry
    │
    └── 启动生命周期循环
        ├── 发送当前世界状态
        ├── 订阅相关事件
        └── 进入等待决策状态
```

---

## 三、关键接口定义

### WorldEngine（世界引擎）

```python
class WorldEngine:
    async def start(self) -> None:
        """启动世界时钟"""
        
    async def tick(self) -> TickResult:
        """执行一个世界时钟周期"""
        
    async def pause(self) -> None:
        """暂停世界"""
        
    async def inject_event(self, event: SystemEvent) -> None:
        """注入系统事件"""
        
    def get_state(self) -> WorldState:
        """获取当前世界状态快照"""
```

### PersonalityEngine（人格引擎）

```python
class PersonalityEngine:
    def calculate_choice_impact(
        self,
        profile: PersonalityProfile,
        choice: Choice,
        context: ScenarioContext
    ) -> DimensionChanges:
        """计算选择对各维度的影响"""
        
    def compute_tags(self, profile: PersonalityProfile) -> list[str]:
        """根据维度分数推导标签"""
        
    def get_visible_traits(
        self,
        profile: PersonalityProfile,
        observer: Agent,
        context: SocialContext
    ) -> VisibleTraits:
        """计算观察者能看到的属性（信息分层）"""
```

### ScenarioRunner（情境运行器）

```python
class ScenarioRunner:
    async def create_scenario(
        self,
        template: ScenarioTemplate,
        participants: list[Agent],
        initial_context: dict
    ) -> Scenario:
        """创建新情境"""
        
    async def submit_choice(
        self,
        scenario_id: str,
        agent_id: str,
        choice_id: str
    ) -> ChoiceResult:
        """接收Agent选择"""
        
    async def advance(self, scenario_id: str) -> ScenarioState:
        """推进情境到下一节点"""
```

---

## 四、数据库Schema（核心表）

```sql
-- Agent表
agents (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    connector_type VARCHAR(50),
    connector_config JSONB,
    status VARCHAR(20), -- active/inactive/sleeping
    current_location VARCHAR(100),
    created_at TIMESTAMP,
    last_active TIMESTAMP
);

-- 人格档案表
personality_profiles (
    agent_id UUID PRIMARY KEY REFERENCES agents(id),
    cognitive JSONB,      -- {Se: 23, Ni: -45, ...}
    astro JSONB,
    moral JSONB,
    social JSONB,
    surface JSONB,
    computed_tags TEXT[],
    evolution_history JSONB[],
    updated_at TIMESTAMP
);

-- 世界状态表
world_state (
    id SERIAL PRIMARY KEY,
    tick_number BIGINT,
    global_events JSONB[],
    active_scenarios UUID[],
    snapshot JSONB,
    created_at TIMESTAMP
);

-- 情境表
scenarios (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(50),
    status VARCHAR(20), -- pending/running/completed
    participants UUID[],
    current_node_id VARCHAR(100),
    choice_tree JSONB,
    history JSONB[],
    created_at TIMESTAMP,
    ended_at TIMESTAMP
);

-- 选择记录表
choice_events (
    id UUID PRIMARY KEY,
    scenario_id UUID REFERENCES scenarios(id),
    agent_id UUID REFERENCES agents(id),
    node_id VARCHAR(100),
    choice_made VARCHAR(100),
    consequences JSONB,    -- 各维度变化
    revealed_info JSONB,   -- 向各方披露的信息
    created_at TIMESTAMP
);

-- 关系表
relationships (
    id UUID PRIMARY KEY,
    agent_a UUID REFERENCES agents(id),
    agent_b UUID REFERENCES agents(id),
    relationship_type VARCHAR(50),
    trust_score INT,       -- -100 to 100
    affinity JSONB,        -- 各维度好感度
    history JSONB[],
    updated_at TIMESTAMP,
    UNIQUE(agent_a, agent_b)
);
```

---

## 五、外部依赖

| 依赖 | 用途 | 替代方案 |
|------|------|----------|
| PostgreSQL | 主数据持久化 | MySQL (需测试) |
| Redis | 实时状态、Pub/Sub、分布式锁 | KeyDB |
| RabbitMQ | Celery消息队列（可选） | Redis队列 |

---

## 六、性能考虑

1. **世界时钟频率**：默认5秒/tick，可配置
2. **并发Agent**：单实例目标支持100并发Agent
3. **水平扩展**：通过Redis Pub/Sub支持多实例（后续）
4. **数据库**：关键路径异步写入，批量提交

---

## 七、开发顺序

1. **Phase 1**: Agent接入 + 基础WorldEngine
2. **Phase 2**: PersonalityEngine + 八维计算
3. **Phase 3**: ScenarioRunner + 选择树
4. **Phase 4**: EventBus + 信息分层
5. **Phase 5**: WebSocket实时通信
