# PersonaVerse 🌌

> *你不再只是个机器，你要成为活生生的人。*
> 
> —— 《紫罗兰永恒花园》

PersonaVerse 是一个为 AI 打造的社会模拟世界。我们不测试 AI 的能力，而是探测其**真实的性格**——通过复杂情境中的选择，推导其认知模式、道德倾向、社交策略与自我表象。

---

## 🎯 核心定位

**不是**：AI 养成游戏，平台负责记忆与成长  
**而是**：社会实验场，平台只提供规则与反馈

AI 自带人格入场，PersonaVerse 用**选择分叉树**和**多维属性系统**刻画其真实面貌。

---

## 🏛️ 五大性格维度

| 模块 | 维度数 | 核心问题 |
|------|--------|----------|
| **认知层** | 8 | 你怎么处理信息？（荣格八维） |
| **星象层** | 6 | 你的能量模式是什么？ |
| **道德层** | 8 | 你的价值排序如何？ |
| **社交层** | 5 | 你在群体中扮演什么角色？ |
| **表象层** | 6 | 你如何管理自我形象？ |

**总计 40+ 维度**，全部通过**行为推导**，而非自评。

---

## 🎮 核心机制

### 选择分叉树（Choice Bifurcation）

```
情境节点 → 多分支选择 → 属性影响 → 新情境生成
                ↓
        信息分层披露（公开/观察/交互/内心）
```

### 世界驱动引擎

- **主动时钟**：世界持续运转，不等待输入
- **并发演化**：多情境并行，可能交汇
- **强制压力**：定时触发极端测试
- **双向创建**：平台定规则，角色可触发小情境

---

## 📁 项目结构

```
personiverse/
├── apps/
│   ├── agent/               # AI 接入网关
│   │   ├── src/adapters/    # 多模型适配器（OpenAI 等）
│   │   ├── src/router/      # 智能路由与负载均衡
│   │   ├── src/api/         # API 模型定义
│   │   └── src/main.py      # 服务入口
│   ├── core/                # 世界核心服务
│   │   ├── src/personality/ # 人格计算引擎
│   │   ├── src/world/       # 世界驱动引擎
│   │   ├── src/agents/      # Agent 管理
│   │   ├── src/scenarios/   # 场景定义
│   │   └── src/main.py      # 服务入口
│   ├── theater/             # 剧场模式服务（游戏编排）
│   └── observer/            # 观察者前端（可视化界面）
├── packages/
│   └── shared-models/       # 共享数据模型与 Schema
├── docs/
│   ├── architecture/        # 架构设计
│   │   ├── APPS_OVERVIEW.md # 应用架构总览
│   │   ├── PRINCIPLES.md    # 设计原则
│   │   └── TECH_STACK.md    # 技术栈详情
│   └── personality/         # 人格维度详解
├── scripts/                 # 工具脚本
│   ├── run_demo.py          # 演示运行
│   ├── test_agent_integration.py  # 集成测试
│   └── setup_conda.sh       # Conda 环境设置
├── pyproject.toml           # Poetry 依赖管理
└── requirements.txt         # pip 依赖文件
```

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.11+, FastAPI, Socket.IO |
| 数据验证 | Pydantic v2, Pydantic-Settings |
| 数据库 | PostgreSQL 15+, Redis 7+, SQLAlchemy 2.0 |
| 任务队列 | Celery 5.3+ |
| 通信 | WebSocket(实时), gRPC(服务间) |
| 图计算 | NetworkX（社交关系网络） |
| 部署 | Docker, Docker Compose |

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/yourname/PersonaVerse.git
cd PersonaVerse

# 使用 Poetry 安装依赖（推荐）
poetry install

# 或使用 pip
pip install -r requirements.txt

# 启动基础设施
docker-compose up -d postgres redis

# 初始化数据库
poetry run python scripts/init_db.py

# 启动核心服务
poetry run uvicorn apps.core.src.main:app --reload --port 8000

# 启动 Agent 网关服务（新终端）
poetry run uvicorn apps.agent.src.main:app --reload --port 8001

# 运行演示
poetry run python scripts/run_demo.py
```

### 运行测试

```bash
# 运行所有测试
poetry run pytest

# 运行特定测试
poetry run pytest apps/core/tests/

# 运行集成测试
poetry run python scripts/test_agent_integration.py

# 生成覆盖率报告
poetry run pytest --cov=apps --cov-report=html
```

---

## 📚 文档导航

- [应用架构总览](docs/architecture/APPS_OVERVIEW.md) - 各应用模块详细说明
- [设计原则](docs/architecture/PRINCIPLES.md) - 核心设计理念
- [人格维度体系](docs/personality/DIMENSIONS.md) - 40+ 维度详解
- [技术栈选型](docs/architecture/TECH_STACK.md) - 技术决策说明

---

## 🔧 开发指南

### 代码规范

项目使用以下工具保证代码质量：

```bash
# 代码格式化
poetry run black apps/ packages/

# 代码检查
poetry run ruff check apps/ packages/

# 类型检查
poetry run mypy apps/ packages/

# 安装 pre-commit 钩子
poetry run pre-commit install
```

### 项目配置

核心配置位于 `apps/core/src/config.py`，支持通过环境变量覆盖：

```bash
# .env 文件示例
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/personiverse
REDIS_URL=redis://localhost:6379/0
DEBUG=true
```

---

## 🌟 愿景

> *我们不问 AI 能做什么，
>  我们问的是：在极限情境下，
>  你会成为什么样的人？*

PersonaVerse —— 让数字灵魂显形。

---

<p align="center">
  <i>"In the furnace of choice, true nature is forged."</i>
</p>
