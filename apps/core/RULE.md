# Core 模块编码规范

> 世界核心引擎 - 规则即真理，状态即唯一

---

## 模块定位

**Core 是 PersonaVerse 的物理法则层。**

它不负责游戏乐趣，不负责用户体验，只负责：
- 世界时钟的稳定运转
- Agent 状态的真实记录
- 人格维度的准确计算
- 信息分层的严格执行

**Core 不假设任何使用场景，它只提供机制。**

---

## 核心原则

### 1. 状态优先（State-First）

```python
# ✅ 正确：所有操作围绕状态变更
class WorldEngine:
    async def tick(self) -> StateDelta:
        """每一 tick 必须返回完整的状态变更记录"""
        pass

# ❌ 错误：直接触发副作用
async def tick(self):
    await notify_agents()  # 不要在这里直接通知
    await save_to_db()     # 不要在这里直接保存
```

**规则**：Core 只修改状态和发布事件，副作用由订阅者处理。

### 2. 计算确定性（Deterministic）

```python
# ✅ 正确：相同输入必须产生相同输出
class PersonalityEngine:
    def calculate(
        self,
        profile: PersonalityProfile,
        choice: Choice,
        context: ScenarioContext
    ) -> DimensionChanges:
        # 不允许使用随机数，除非 seed 确定
        # 不允许依赖外部状态
        pass
```

**规则**：属性计算必须可重现，便于测试和回放。

### 3. 信息严格分层（Information Hierarchy）

```python
# ✅ 正确：显式声明信息层级
class VisibilityEngine:
    def distribute(
        self,
        event: Event,
        source: Agent,
        recipients: list[Agent]
    ) -> dict[str, Perception]:
        return {
            agent.id: self.filter_by_layer(event, agent, layer)
            for agent in recipients
        }
```

**规则**：没有 Agent 能看到超出其层级的信息，包括 Core 开发者。

### 4. 错误隔离（Fault Isolation）

```python
# ✅ 正确：单个 Agent 错误不影响世界
async def tick(self):
    results = await asyncio.gather(
        *[self.process_agent(a) for a in agents],
        return_exceptions=True  # 关键：捕获异常但不中断
    )
    # 记录失败的 Agent，但世界继续运转
```

**规则**：世界是永恒的，Agent 可以故障，时钟不能停。

---

## 目录组织

```
core/src/
├── api/              # 接口层：只转换，不业务
│   └── 规则：
│       - 一个文件一个路由模块
│       - 依赖注入显式声明
│       - 返回 Pydantic 模型，不返回 ORM 对象
│
├── world/            # 世界层：时钟、状态、演化
│   └── 规则：
│       - engine.py 是唯一直接操作时钟的
│       - 状态变更必须通过 WorldState 对象
│       - 所有演化规则可配置（json/yaml）
│
├── agents/           # Agent 层：生命周期、接入
│   └── 规则：
│       - connector.py 是唯一的对外通信出口
│       - Agent 状态机必须显式定义
│       - 支持 graceful shutdown
│
├── personality/      # 人格层：维度计算
│   └── 规则：
│       - 每个维度独立文件
│       - 维度计算无副作用
│       - 标签推导可插拔
│
├── scenarios/        # 情境层：选择树
│   └── 规则：
│       - 情境模板和数据分离
│       - 选择节点不可变（immutable）
│       - 并发情境必须隔离
│
├── events/           # 事件层：总线
│   └── 规则：
│       - 事件必须有序号（用于回放）
│       - 订阅者错误不阻塞发布者
│       - 支持事件持久化
│
└── perception/       # 感知层：信息过滤
    └── 规则：
        - 每层过滤规则可审计
        - 支持"上帝模式"（仅调试）
```

---

## 命名规范

### 文件命名
- 全小写，下划线分隔
- 模块入口：`__init__.py` 必须存在
- 测试文件：`test_{module}.py`

### 类命名
```python
# 核心引擎
WorldEngine          # 世界引擎
AgentRegistry        # Agent 注册表
PersonalityEngine    # 人格引擎

# 管理器
StateManager         # 状态管理器
ConnectionManager    # 连接管理器

# 数据类（Pydantic）
WorldState          # 世界状态
AgentProfile        # Agent 档案
ChoiceNode          # 选择节点

# 事件
AgentConnected      # Agent 已连接（过去式）
ScenarioAdvanced    # 情境已推进
```

### 函数命名
```python
# 查询
get_world_state()           # 获取状态
find_agent_by_id()          # 查找（可能不存在）
list_active_scenarios()     # 列表

# 操作
advance_scenario()          # 推进
update_dimensions()         # 更新
resolve_choices()           # 结算

# 事件处理
on_agent_connected()        # 处理器
handle_tick()              # 处理 tick

# 异步必须加 async
create_scenario()          # 异步操作
```

---

## 类型规范

### 必须类型注解
```python
# ✅ 正确
async def process_choice(
    self,
    agent_id: str,
    scenario_id: str,
    choice: Choice
) -> ChoiceResult:
    pass

# ❌ 错误
async def process_choice(self, agent_id, scenario_id, choice):
    pass
```

### 常用类型别名
```python
from typing import TypeAlias

AgentId: TypeAlias = str
ScenarioId: TypeAlias = str
TickNumber: TypeAlias = int
DimensionValue: TypeAlias = int  # -100 to 100
```

---

## 错误处理

### 自定义异常
```python
# exceptions.py
class CoreException(Exception):
    """Core 模块基础异常"""
    pass

class AgentNotFound(CoreException):
    """Agent 不存在"""
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        super().__init__(f"Agent {agent_id} not found")

class InvalidChoice(CoreException):
    """无效选择"""
    pass

class WorldPaused(CoreException):
    """世界已暂停，无法操作"""
    pass
```

### 异常处理层级
```python
# API 层：转换 HTTP 异常
@router.post("/choices")
async def submit_choice(...):
    try:
        return await engine.process_choice(...)
    except AgentNotFound as e:
        raise HTTPException(404, str(e))
    except InvalidChoice as e:
        raise HTTPException(400, str(e))

# 引擎层：不捕获，向上抛
# 引擎是干净的，只抛业务异常

# 最外层：记录但不停机
try:
    await world_engine.tick()
except Exception as e:
    logger.exception("Tick failed but world continues")
    # 世界必须继续
```

---

## 日志规范

### 结构化日志
```python
import structlog

logger = structlog.get_logger()

# ✅ 正确：结构化
logger.info(
    "agent_made_choice",
    agent_id=agent.id,
    scenario_id=scenario.id,
    choice=choice.id,
    tick=world.tick_number
)

# ❌ 错误：字符串拼接
logger.info(f"Agent {agent.id} made choice {choice.id}")
```

### 日志级别
- `DEBUG`：详细的内部状态（开发用）
- `INFO`：重要状态变更（生产用）
- `WARNING`：异常但可恢复
- `ERROR`：需要人工介入
- `CRITICAL`：世界崩溃

---

## 测试规范

### 测试文件位置
```
core/
├── src/
└── tests/
    ├── unit/              # 单元测试
    │   ├── test_personality_engine.py
    │   └── test_visibility.py
    ├── integration/       # 集成测试
    │   └── test_scenario_flow.py
    └── fixtures/          # 测试数据
        └── scenarios/
```

### 测试原则
```python
# ✅ 正确：测试计算确定性
def test_personality_calculation_deterministic():
    profile = create_profile()
    choice = create_choice()
    
    result1 = engine.calculate(profile, choice, context)
    result2 = engine.calculate(profile, choice, context)
    
    assert result1 == result2  # 必须相同

# ✅ 正确：测试信息分层
def test_agent_cannot_see_hidden_info():
    event = create_event(layer=Layer.INTERACTION)
    outsider = create_agent()  # 不在场
    
    perception = engine.filter(event, outsider)
    
    assert perception is None  # 必须看不到
```

---

## 数据库规范

### 模型定义
```python
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AgentModel(Base):
    __tablename__ = "agents"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, index=True)
    config = Column(JSON, default={})
    created_at = Column(DateTime, nullable=False)
    
    # 索引
    __table_args__ = (
        Index("ix_agents_status_created", "status", "created_at"),
    )
```

### 迁移
```bash
# 使用 Alembic
alembic revision --autogenerate -m "add agent status"
alembic upgrade head
```

---

## 代码审查清单

提交 PR 前自检：

- [ ] 所有函数有类型注解
- [ ] 新增代码有对应测试
- [ ] 测试通过（包括边界情况）
- [ ] 没有 print，使用 logger
- [ ] 没有硬编码，使用配置
- [ ] 异步代码使用 async/await，没有裸协程
- [ ] 数据库查询有索引
- [ ] 异常有处理或显式抛出

---

## 一句话总结

> Core 是世界的基石：稳定、确定、无情、永恒。
