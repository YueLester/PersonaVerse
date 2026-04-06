# Agent Service 文档

## 📚 文档导航

| 文档 | 内容 | 适合读者 |
|------|------|----------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 系统架构设计、功能域定义、演进路线 | 架构师、Tech Lead |
| [RULE.md](../RULE.md) | 代码规范、开发约定 | 开发人员 |
| API 文档 (待补充) | 接口定义、使用示例 | 后端开发人员 |
| 部署指南 (待补充) | 部署、配置、运维 | DevOps |

## 🎯 快速理解

### 一句话定位

Agent Service 是 PersonaVerse 的 **AI 能力中间件**，负责将算力（OpenAI/Claude/Gemini）转化为业务能力（人格分析/世界生成/对话等）。

### 核心职责

1. **算力接入**：统一封装多模型接口
2. **服务封装**：将 AI 能力封装为业务服务
3. **Prompt 管理**：工程化 Prompt 生命周期
4. **流程编排**：支持复杂 AI 工作流
5. **多 Agent 管理**：支持多 AI 协作

### 架构分层

```
业务编排层 (Workflow / Multi-Agent)
        ↓
服务抽象层 (Personality / World / Dialogue / Analysis)
        ↓
能力基础层 (Prompt Center / Model Router / Cache)
        ↓
算力接入层 (OpenAI / Claude / Gemini / Local)
```

## 🚀 开始使用

### 开发环境

```bash
# 进入目录
cd apps/agent

# 安装依赖
poetry install

# 配置环境变量
cp .env.example .env
# 编辑 .env 添加 OPENAI_API_KEY

# 启动服务
poetry run uvicorn src.main:app --reload --port 8001
```

### 调用示例

```python
from ai_service import AIService, OpenAIProvider

# 初始化
compute = OpenAIProvider(api_key="sk-...")
ai = AIService(compute)

# 调用人格分析
result = await ai.personality.analyze_traits(
    text="我喜欢独自阅读，不太喜欢热闹的聚会..."
)

# 调用世界生成
scenario = await ai.world.generate_scenario(
    context={"world_type": "cyberpunk"},
    personas=[persona1, persona2],
    type="moral_dilemma"
)
```

## 📋 开发任务看板

### 当前阶段：Phase 1 (MVP)

- [x] 基础架构设计
- [ ] 算力统一接入（OpenAI）
- [ ] Personality Service 实现
- [ ] World Service 实现
- [ ] Dialogue Service 实现
- [ ] 基础 Prompt 管理
- [ ] 成本监控

### 下一阶段：Phase 2 (治理增强)

- [ ] Prompt 版本管理
- [ ] 多模型路由
- [ ] 智能缓存
- [ ] 流程编排基础

## 🤝 协作方式

### 与 Core Service 协作

Core 负责人格计算逻辑，Agent 负责 AI 能力调用：

```
Core: 构建人格提示词 → Agent: 调用 AI → Core: 解析结果更新人格
```

### 与 Theater Service 协作

Theater 负责剧场编排，Agent 负责内容生成：

```
Theater: 请求情境 → Agent.World: 生成情境 → Theater: 编排呈现
```

## 📞 联系方式

- 技术讨论：#agent-dev 频道
- 架构问题：@架构组
- 紧急问题：@oncall

---

**欢迎补充和反馈！**
