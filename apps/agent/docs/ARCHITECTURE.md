# PersonaVerse Agent Service 架构设计

> **定位**：AI 服务中间件 —— 将算力转化为业务能力  
> **目标**：为 PersonaVerse 系统提供统一、可扩展、可治理的 AI 能力层

---

## 一、核心愿景

### 1.1 解决的问题

| 问题 | 解决方案 |
|------|----------|
| 多个业务模块重复接入 AI 模型 | 统一中间层，一次接入，多处复用 |
| Prompt 散落在代码中难以管理 | 中心化 Prompt 工程与版本控制 |
| 成本不透明，难以优化 | 统一成本追踪与 SLA 治理 |
| 单点故障，无降级能力 | 多模型路由与自动故障转移 |
| 复杂业务流程难以编排 | 可视化流程编排与状态管理 |

### 1.2 设计原则

1. **算力无关**：上层业务不感知具体模型（GPT/Claude/Gemini）
2. **服务化封装**：将 AI 能力封装为可复用的业务服务
3. **可观测性**：全流程可追踪、可度量、可优化
4. **可扩展性**：新服务、新模型、新流程可插拔

---

## 二、分层架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         业务编排层 (Orchestration)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Workflow   │  │ Multi-Agent │  │ Human-in-   │  │   Event     │        │
│  │   Engine    │  │   Manager   │  │   Loop      │  │   Bus       │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│                        服务抽象层 (Service Abstraction)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Personality │  │    World    │  │  Dialogue   │  │  Analysis   │        │
│  │   Service   │  │   Service   │  │   Service   │  │   Service   │        │
│  │  (人格分析)  │  │  (世界生成)  │  │  (对话生成)  │  │  (数据分析)  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│                       能力基础层 (Capability Foundation)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Prompt    │  │    Model    │  │    Cache    │  │   Policy    │        │
│  │   Center    │  │   Router    │  │    Layer    │  │   Engine    │        │
│  │ (Prompt管理) │  │ (多模型路由) │  │ (智能缓存)  │  │ (策略治理)  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│                        算力接入层 (Compute Access)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   OpenAI    │  │   Claude    │  │   Gemini    │  │   Local     │        │
│  │  Provider   │  │  Provider   │  │  Provider   │  │  Provider   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 各层职责

| 层级 | 核心职责 | 关键组件 |
|------|----------|----------|
| **算力接入层** | 统一封装不同 AI 模型接口 | Provider 插件、连接池、健康检查 |
| **能力基础层** | Prompt 工程、路由、缓存、治理 | Prompt Center、Model Router、Cache |
| **服务抽象层** | 将 AI 能力封装为业务服务 | Personality/World/Dialogue/Analysis Service |
| **业务编排层** | 多服务协作流程编排 | Workflow Engine、Multi-Agent Manager |

---

## 三、核心功能域

### 3.1 流程编排 (Workflow Orchestration)

**定位**：有状态、可观测、可干预的业务流程管理

**核心能力**：

| 能力 | 说明 | 场景示例 |
|------|------|----------|
| **DAG 编排** | 定义步骤依赖图，支持并行/串行 | 人格分析→情境生成→选择预测，三步可并行 |
| **状态持久化** | 长流程断点续作 | 复杂世界生成耗时 5 分钟，中断可恢复 |
| **人机回环** | 关键节点人工审核 | 道德敏感情境生成后，人工确认再发布 |
| **条件分支** | 基于结果动态路由 | AI 置信度<0.7，自动转人工或换模型重试 |
| **超时降级** | SLA 保障 | GPT-4 超时则降级到 GPT-3.5 |

**扩展方向**：
- 可视化流程编排器（拖拽配置）
- 流程版本管理（A/B 测试、灰度发布）
- 自定义步骤插件（业务方注册专属步骤）

---

### 3.2 多 Agent 管理 (Multi-Agent Management)

**定位**：从"一个 AI"到"一群 AI 协作"

**协作模式**：

| 模式 | 说明 | PersonaVerse 应用 |
|------|------|-------------------|
| **角色分工** | 不同 Agent 负责不同领域 | Analyst→Creator→Critic 流水线 |
| **对话协作** | Agent 间多轮讨论 | 三个 AI 讨论"情境是否足够测试人格" |
| **竞争选举** | 多方案选最优 | 生成 5 个情境，选最能区分人格的 |
| **层次管理** | 主 Agent 调度子 Agent | Director 分配任务给 Specialist |

**管理维度**：

```
Agent 生命周期：
├── 注册与发现（动态加入新 Agent 类型）
├── 状态监控（健康、负载、成本）
├── 负载均衡（请求分发到多实例）
├── 隔离与限流（租户间资源隔离）
├── 成本归因（哪个 Agent 花了多少钱）
└── 记忆共享（多 Agent 共享上下文）
```

**扩展方向**：
- Agent 市场（第三方贡献 Agent，如"MBTI 专家 Agent"）
- 动态组合（运行时根据需求组装 Agent 团队）

---

### 3.3 Prompt 管理 (Prompt Engineering Management)

**定位**：Prompt 是 AI 时代的"代码"，需要工程化管理

**核心功能**：

| 维度 | 功能 | 优先级 |
|------|------|--------|
| **版本控制** | Prompt 变更历史，可回滚 | P0 |
| **变量注入** | 模板化，动态填充 | P0 |
| **A/B 测试** | 对比两个 Prompt 的效果 | P1 |
| **效果追踪** | Prompt→结果质量关联 | P1 |
| **分类管理** | 按业务域/场景组织 | P1 |

**高级能力**：
- **Prompt 优化建议**：基于效果数据，AI 自动优化 Prompt
- **Few-shot 管理**：动态选择最优示例
- **Prompt 压缩**：长对话历史自动摘要，节省 token
- **多语言 Prompt**：自动翻译/本地化

**Prompt 即配置示例**：

```yaml
prompts:
  personality_analysis:
    version: "2.3.1"
    description: "人格特质分析 Prompt"
    template: |
      你是一个人格心理学专家。请分析以下文本体现的 {dimensions} 维度...
      
      分析文本：
      {text}
      
      请以 JSON 格式返回：
      {"O": 0-100, "C": 0-100, "E": 0-100, "A": 0-100, "N": 0-100}
    variables:
      - dimensions: "大五人格维度"
      - text: "待分析文本"
    examples:
      - input: "我喜欢独自阅读，不太喜欢热闹的聚会..."
        output: '{"O": 80, "C": 65, "E": 30, "A": 70, "N": 55}'
    model: "gpt-4o"
    temperature: 0.3
    max_tokens: 2048
    tags: ["人格", "分析", "big-five"]
```

---

### 3.4 模型路由与治理

**核心能力**：

| 功能 | 说明 |
|------|------|
| **智能路由** | 根据成本/质量/延迟偏好选择模型 |
| **故障转移** | 主模型失败自动切换备用 |
| **成本预算** | 租户级成本配额与告警 |
| **质量监控** | 输出质量评估与异常检测 |
| **流控限流** | 防止单租户耗尽资源 |

**路由策略**：

```python
# 成本优先
cheap_provider = router.select(strategy="cost", max_budget=0.01)

# 质量优先
quality_provider = router.select(strategy="quality", min_capability="gpt-4-level")

# 延迟优先
fast_provider = router.select(strategy="latency", max_latency_ms=1000)

# 智能均衡
balanced = router.select(strategy="smart", context={"tenant": "t1", "priority": "high"})
```

---

## 四、服务域定义

### 4.1 Personality Service（人格服务）

**职责**：人格分析、预测、建模

```python
# 核心接口
async def analyze_traits(text: str, dimensions: list) -> TraitProfile
async def predict_choice(persona: Profile, scenario: Scenario, choices: list) -> Prediction
async def generate_backstory(profile: Profile) -> str
async def detect_persona_shift(history: list) -> ShiftReport
```

### 4.2 World Service（世界服务）

**职责**：情境生成、世界构建、分支推演

```python
# 核心接口
async def generate_scenario(context: WorldContext, personas: list, type: str) -> Scenario
async def generate_branch(scenario: Scenario, choice: str, depth: int) -> BranchTree
async def evaluate_scenario_difficulty(scenario: Scenario, persona: Profile) -> Difficulty
async def generate_npc_dialogue(npc: Profile, situation: Situation) -> str
```

### 4.3 Dialogue Service（对话服务）

**职责**：人格化对话生成

```python
# 核心接口
async def generate_response(persona: Profile, history: list, input: str, emotion: State) -> Response
async def generate_stream(persona: Profile, history: list, input: str) -> Iterator[Chunk]
async def detect_emotion_shift(text: str) -> EmotionDelta
async def adapt_style(text: str, target_persona: Profile) -> str
```

### 4.4 Analysis Service（分析服务）

**职责**：数据分析、洞察提取

```python
# 核心接口
async def extract_structured(text: str, schema: dict) -> dict
async def summarize(text: str, style: str, focus: str) -> str
async def classify(text: str, categories: list) -> Classification
async def analyze_moral_judgment(scenario: str, persona: Profile) -> MoralReport
```

---

## 五、扩展能力规划

### 5.1 数据与记忆管理

| 能力 | 说明 | 优先级 |
|------|------|--------|
| **向量记忆** | RAG 支持，长期记忆检索 | P1 |
| **结构化记忆** | 人格档案、世界状态持久化 | P0 |
| **记忆遗忘** | 重要性衰减、容量管理 | P2 |
| **跨会话记忆** | 用户级/世界级持久化 | P1 |

### 5.2 质量与治理

| 能力 | 说明 | 优先级 |
|------|------|--------|
| **输出验证** | JSON Schema 验证、事实核查 | P0 |
| **偏见检测** | 检测 AI 输出中的偏见 | P1 |
| **安全过滤** | 内容安全、合规检查 | P0 |
| **可解释性** | 为什么 AI 给出这个选择？ | P2 |

### 5.3 观测与调试

| 能力 | 说明 | 优先级 |
|------|------|--------|
| **全链路追踪** | 请求从入口到各服务的完整链路 | P1 |
| **Prompt 回放** | 复现某次 AI 调用的完整上下文 | P1 |
| **效果评估** | 自动化评估 AI 输出质量 | P2 |
| **成本分析** | 功能/租户/模型维度的成本明细 | P1 |

---

## 六、演进路线图

### Phase 1: 基础服务（MVP - 1-2 月）

- [ ] 算力统一接入（OpenAI 为主）
- [ ] 基础服务封装（Personality/World/Dialogue）
- [ ] 简单 Prompt 管理（文件配置）
- [ ] 成本/延迟监控

### Phase 2: 治理增强（2-3 月）

- [ ] Prompt 版本管理与 A/B 测试
- [ ] 多模型路由（OpenAI + Claude）
- [ ] 智能缓存层
- [ ] 基础流程编排（串行/并行）

### Phase 3: 多 Agent 协作（3-4 月）

- [ ] Agent 注册与发现机制
- [ ] 多 Agent 编排引擎
- [ ] Agent 间记忆共享
- [ ] 可视化编排器

### Phase 4: 智能化（4-6 月）

- [ ] Prompt 自动优化
- [ ] 模型自适应选择
- [ ] 预测性扩缩容
- [ ] 高级可解释性

---

## 七、与现有模块关系

```
┌─────────────────────────────────────────────────────────────┐
│                    PersonaVerse 系统                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Core Service          ◄────►   Agent Service (本模块)      │
│   (人格计算引擎)                  (AI 能力中间件)             │
│                                                             │
│   Theater Service       ◄────►   ┌──────────────┐          │
│   (剧场编排)                     │  Workflow    │          │
│                                  │   Engine     │          │
│   Observer (前端)       ◄────►   ├──────────────┤          │
│                                  │   Services   │          │
│                                  │ (Personality │          │
│                                  │  /World/...  │          │
│                                  └──────────────┘          │
│                                                             │
│   Shared Models         ◄────►   Prompt Center             │
│   (共享数据模型)                  (Prompt 管理)             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 八、技术选型建议

| 领域 | 推荐技术 | 备选方案 |
|------|----------|----------|
| **服务框架** | FastAPI | 保持现有 |
| **流程编排** | Temporal / Cadence | 自研轻量版 |
| **缓存** | Redis | 本地 LRU |
| **向量存储** | Pinecone / Milvus | pgvector |
| **监控** | OpenTelemetry + Prometheus | 自研 |
| **配置管理** | Pydantic Settings + 配置中心 | 环境变量 |

---

## 九、关键设计决策

### 决策 1：独立服务 vs 库函数

**选择**：独立 HTTP 服务（保持现有架构）

**理由**：
- 多语言支持（其他服务可用不同语言）
- 独立扩缩容（AI 调用可单独扩容）
- 故障隔离（AI 服务崩溃不影响 Core）

### 决策 2：同步 vs 异步 API

**选择**：两者都支持

**理由**：
- 同步：简单场景，快速响应
- 异步：长流程（世界生成），流式输出（对话）

### 决策 3：Prompt 存储方式

**选择**：文件 + 数据库混合

**理由**：
- 文件：开发阶段，版本控制友好
- 数据库：生产阶段，动态更新

---

## 十、参考资源

- [OpenAI API 文档](https://platform.openai.com/docs)
- [Temporal Workflow 文档](https://docs.temporal.io/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LLM Router 最佳实践](https://...)

---

**最后更新**：2026-04-05  
**维护者**：Agent Service Team  
**状态**：架构设计阶段，欢迎反馈
