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
│   ├── agent/             # AI 接入网关（统一调用各种模型）
│   ├── core/              # 世界核心服务（世界引擎、人格计算）
│   ├── theater/           # 剧场模式服务（游戏编排）
│   └── observer/          # 观察者前端（可视化界面）
├── packages/
│   ├── sdk-python/        # Python SDK
│   ├── sdk-typescript/    # TypeScript SDK
│   └── shared-models/     # 共享数据模型
├── docs/
│   ├── architecture/      # 架构设计
│   ├── personality/       # 人格维度详解
│   └── scenarios/         # 场景设计手册
└── infra/                 # 基础设施配置
```

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.11+, FastAPI, Socket.IO |
| 数据库 | PostgreSQL 15+, Redis 7+ |
| 前端 | React 18, TypeScript, Tailwind, D3.js |
| 通信 | WebSocket(实时), gRPC(服务间) |
| 部署 | Docker, Docker Compose |

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourname/PersonaVerse.git
cd PersonaVerse

# 安装依赖
poetry install

# 启动基础设施
docker-compose up -d postgres redis

# 初始化数据库
poetry run python scripts/init_db.py

# 启动核心服务
poetry run uvicorn apps.core.src.main:app --reload

# 启动观察者前端（新终端）
cd apps/observer && npm install && npm run dev
```

---

## 📚 文档导航

- [设计原则](docs/architecture/PRINCIPLES.md)
- [人格维度体系](docs/personality/DIMENSIONS.md)
- [技术栈选型](docs/architecture/TECH_STACK.md)

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
