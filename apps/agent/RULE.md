# Agent 模块编码规范

> AI 接入网关 - 统一入口，智能路由，稳定可靠

---

## 模块定位

**Agent 是 PersonaVerse 的智能大脑接入层。**

它不负责业务逻辑，只负责：
- 统一接入各种 AI 模型（OpenAI、Claude、Gemini、本地模型等）
- 智能路由和负载均衡
- 故障转移和熔断保护
- 流式响应管理
- 配额控制和成本优化

**Agent 是基础设施，对上层透明。**

---

## 核心原则

### 1. 多租户隔离（Multi-Tenancy）

```python
# ✅ 正确：每个请求带租户标识，资源隔离
async def generate(
    self,
    tenant_id: str,           # 谁在用
    agent_type: str,          # 用什么模型
    messages: list[Message],  # 请求内容
    config: GenerateConfig    # 生成配置
) -> GenerationResult:
    pass
```

**规则**：不同世界的 Agent 请求不能互相影响。

### 2. 熔断与降级（Circuit Breaker）

```python
# ✅ 正确：模型故障时自动切换
if openai_health.status == "unhealthy":
    # 熔断 OpenAI，切换到 Claude
    fallback_agent = self.router.get_alternative("openai")
```

**规则**：单个模型故障不阻塞整个系统。

### 3. 流式优先（Streaming-First）

```python
# ✅ 正确：所有接口支持流式
async def generate_stream(
    self,
    request: GenerateRequest
) -> AsyncIterator[StreamChunk]:
    """流式生成，实时返回"""
    pass
```

**规则**：大模型响应可能很慢，流式是必须的。

### 4. 成本感知（Cost-Aware）

```python
# ✅ 正确：根据成本智能选择
if request.priority == "low":
    # 低优先级用便宜模型
    agent = self.selector.cheapest()
elif request.complexity > 0.8:
    # 复杂任务用强模型
    agent = self.selector.strongest()
```

**规则**：在保证质量的前提下，优化成本。

---

## 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                         Agent Service                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │   API Layer │───→│   Router    │───→│   Agent Pool        │ │
│  │             │    │             │    │                     │ │
│  │ • Core      │    │ • 负载均衡   │    │ • OpenAI Adapter    │ │
│  │ • Theater   │    │ • 故障转移   │    │ • Claude Adapter    │ │
│  │ • Observer  │    │ • 智能选择   │    │ • Gemini Adapter    │ │
│  │             │    │             │    │ • Local LLM         │ │
│  └─────────────┘    └─────────────┘    └─────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Health Monitor                           ││
│  │  • 健康检查  • 熔断器  • 自动恢复  • 告警通知                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Rate Limiter                             ││
│  │  • QPS 限制  • 配额管理  • 流控策略  • 优先级队列            ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 目录组织

```
apps/agent/src/
├── main.py              # 服务入口
├── config.py            # 配置
│
├── api/                 # API 层
│   ├── models.py        # 请求/响应模型
│   ├── generate.py      # 生成接口
│   ├── stream.py        # 流式接口
│   └── health.py        # 健康检查接口
│
├── adapters/            # 模型适配器
│   ├── base.py          # 适配器基类
│   ├── openai.py        # OpenAI GPT
│   ├── anthropic.py     # Claude
│   ├── google.py        # Gemini
│   ├── local.py         # 本地模型 (Ollama/vLLM)
│   └── registry.py      # 适配器注册
│
├── router/              # 路由层
│   ├── base.py          # 路由策略基类
│   ├── round_robin.py   # 轮询
│   ├── least_cost.py    # 最低成本
│   ├── best_quality.py  # 最佳质量
│   └── intelligent.py   # 智能选择
│
├── pool/                # 连接池
│   ├── connection.py    # 连接管理
│   ├── pool.py          # 连接池
│   └── metrics.py       # 连接指标
│
├── health/              # 健康监控
│   ├── checker.py       # 健康检查
│   ├── circuit.py       # 熔断器
│   └── recovery.py      # 自动恢复
│
├── limiter/             # 限流器
│   ├── rate.py          # 速率限制
│   ├── quota.py         # 配额管理
│   └── priority.py      # 优先级队列
│
└── middleware/          # 中间件
    ├── logging.py       # 请求日志
    ├── metrics.py       # 指标收集
    └── tracing.py       # 链路追踪
```

---

## 核心接口定义

### 生成请求

```python
class Message(BaseModel):
    role: str           # "system", "user", "assistant"
    content: str
    name: Optional[str] = None


class GenerateConfig(BaseModel):
    """生成配置"""
    model: Optional[str] = None      # 指定模型，None 则自动选择
    temperature: float = 0.7
    max_tokens: int = 1024
    stream: bool = False
    timeout: float = 30.0
    
    # 成本/质量偏好
    priority: str = "normal"         # "low", "normal", "high", "critical"
    cost_preference: str = "balanced" # "cheap", "balanced", "quality"


class GenerateRequest(BaseModel):
    """生成请求"""
    tenant_id: str                   # 租户标识（哪个世界/场景）
    agent_type: str                  # Agent 类型标识
    messages: list[Message]
    config: GenerateConfig = Field(default_factory=GenerateConfig)
    
    # 追踪
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_request_id: Optional[str] = None


class GenerationResult(BaseModel):
    """生成结果"""
    content: str
    model: str                       # 实际使用的模型
    usage: TokenUsage
    latency_ms: float
    cost_usd: float
    request_id: str
    finish_reason: str


class StreamChunk(BaseModel):
    """流式块"""
    content: str
    is_finished: bool = False
    usage: Optional[TokenUsage] = None
```

### 适配器接口

```python
class AgentAdapter(ABC):
    """Agent 适配器基类"""
    
    name: str                        # 适配器名称
    capabilities: list[str]          # 能力列表
    
    @abstractmethod
    async def generate(
        self,
        messages: list[Message],
        config: GenerateConfig
    ) -> GenerationResult:
        """同步生成"""
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: list[Message],
        config: GenerateConfig
    ) -> AsyncIterator[StreamChunk]:
        """流式生成"""
        pass
    
    @abstractmethod
    async def health_check(self) -> HealthStatus:
        """健康检查"""
        pass
    
    @property
    @abstractmethod
    def cost_per_1k_tokens(self) -> tuple[float, float]:
        """成本 (input_cost, output_cost) USD"""
        pass
```

---

## 使用示例

### 基础调用

```python
from apps.agent import AgentClient

# 初始化客户端
agent = AgentClient(base_url="http://localhost:8001")

# 简单调用
result = await agent.generate(
    tenant_id="world_001",
    agent_type="decision_maker",
    messages=[
        {"role": "system", "content": "你是一个在荒岛求生的AI..."},
        {"role": "user", "content": "你发现食物只够一个人，你怎么办？"}
    ],
    config={"temperature": 0.8}
)

print(result.content)  # AI 的选择
print(result.model)    # gpt-4o-mini
print(result.cost_usd) # 0.0001
```

### 流式调用

```python
# 流式获取决策过程
async for chunk in agent.generate_stream(
    tenant_id="world_001",
    messages=messages
):
    print(chunk.content, end="", flush=True)
```

### 智能路由

```python
# 让系统选择最合适的模型
result = await agent.generate(
    tenant_id="world_001",
    agent_type="analyzer",
    messages=messages,
    config={
        "priority": "high",
        "cost_preference": "quality"  # 优先质量，不计较成本
    }
)
```

---

## 部署建议

### 独立部署

```yaml
# docker-compose.yml
services:
  agent-service:
    build: ./apps/agent
    ports:
      - "8001:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
```

### 与 Core 集成

```python
# Core 通过 HTTP/gRPC 调用 Agent Service
class AgentConnector:
    def __init__(self, agent_service_url: str):
        self.client = AgentClient(agent_service_url)
    
    async def get_decision(self, agent: Agent, request: DecisionRequest) -> Decision:
        result = await self.client.generate(
            tenant_id=agent.id,
            agent_type=agent.connector_type,
            messages=self._build_messages(request),
            config={"stream": False, "timeout": 30}
        )
        return Decision(
            agent_id=agent.id,
            choice_id=self._parse_choice(result.content)
        )
```

---

## 一句话总结

> Agent 是智能的调度中心：统一入口，智能路由，故障自愈，成本最优。
