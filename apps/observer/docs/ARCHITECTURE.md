# Observer - 观察者前端架构规划

> 职责：为人类观察者提供上帝视角界面，实时观看AI世界，查看人格数据，回放历史

---

## 一、模块划分

```
observer/src/
├── public/
│   └── index.html
│
├── src/
│   ├── main.tsx             # React入口
│   ├── App.tsx              # 根组件
│   ├── index.css            # 全局样式
│   │
│   ├── components/          # 组件库
│   │   ├── layout/          # 布局组件
│   │   │   ├── Sidebar.tsx      # 侧边导航
│   │   │   ├── Header.tsx       # 顶部栏
│   │   │   └── MainContent.tsx  # 主内容区
│   │   │
│   │   ├── world/           # 世界视图
│   │   │   ├── WorldMap.tsx         # 世界地图
│   │   │   ├── AgentCluster.tsx     # Agent聚类显示
│   │   │   ├── ScenarioMarkers.tsx  # 情境标记
│   │   │   └── RealtimeFeed.tsx     # 实时事件流
│   │   │
│   │   ├── agent/           # Agent详情
│   │   │   ├── AgentCard.tsx        # Agent卡片
│   │   │   ├── AgentDetail.tsx      # 详情面板
│   │   │   ├── PersonalityRadar.tsx # 人格雷达图
│   │   │   ├── TraitTimeline.tsx    # 属性时间线
│   │   │   └── RelationshipGraph.tsx # 关系图谱
│   │   │
│   │   ├── scenario/        # 情境视图
│   │   │   ├── ScenarioTree.tsx     # 选择树可视化
│   │   │   ├── ChoiceNode.tsx       # 选择节点
│   │   │   ├── Participants.tsx     # 参与者列表
│   │   │   └── LiveTranscript.tsx   # 实时对话记录
│   │   │
│   │   ├── theater/         # 剧场视图
│   │   │   ├── TheaterList.tsx      # 剧场列表
│   │   │   ├── TheaterCard.tsx      # 剧场卡片
│   │   │   ├── LiveStage.tsx        # 实时舞台
│   │   │   └── ReplayControls.tsx   # 回放控制
│   │   │
│   │   └── common/          # 通用组件
│   │       ├── Badge.tsx
│   │       ├── Card.tsx
│   │       ├── Tooltip.tsx
│   │       └── Loading.tsx
│   │
│   ├── hooks/               # 自定义Hooks
│   │   ├── useWebSocket.ts      # WebSocket连接
│   │   ├── useWorldState.ts     # 世界状态订阅
│   │   ├── useAgent.ts          # Agent数据获取
│   │   ├── useScenario.ts       # 情境数据获取
│   │   ├── useTheater.ts        # 剧场数据获取
│   │   └── useReplay.ts         # 回放控制
│   │
│   ├── services/            # API服务层
│   │   ├── api.ts               # HTTP API封装
│   │   ├── websocket.ts         # WebSocket管理
│   │   ├── world.ts             # 世界相关API
│   │   ├── agents.ts            # Agent相关API
│   │   ├── scenarios.ts         # 情境相关API
│   │   └── theater.ts           # 剧场相关API
│   │
│   ├── stores/              # 状态管理（Zustand）
│   │   ├── worldStore.ts        # 世界状态
│   │   ├── agentStore.ts        # Agent集合
│   │   ├── scenarioStore.ts     # 情境集合
│   │   └── uiStore.ts           # UI状态
│   │
│   ├── types/               # TypeScript类型
│   │   ├── agent.ts
│   │   ├── personality.ts
│   │   ├── scenario.ts
│   │   ├── world.ts
│   │   └── theater.ts
│   │
│   └── utils/               # 工具函数
│       ├── formatters.ts        # 格式化
│       ├── colors.ts            # 颜色映射
│       └── graphLayout.ts       # 图布局算法
│
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

---

## 二、核心视图设计

### 1. 世界视图（World View）

```
┌─────────────────────────────────────────────────────────────┐
│  Header: PersonaVerse Observer          [世界] [剧场] [分析]  │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                   │
│  Sidebar │              World Map (D3/Three.js)              │
│          │                                                   │
│ • Agents │     ┌─────┐         ┌─────────┐                  │
│ • Scenes │     │ 🤖A │────────►│  🎭     │                  │
│ • Theater│     └──┬──┘         │ Scenario│                  │
│          │        │            └────┬────┘                  │
│          │        │                 │                        │
│          │     ┌──▼──┐         ┌───▼────┐                  │
│          │     │ 🤖B │◄────────│  🤖C   │                  │
│          │     └─────┘         └────────┘                  │
│          │                                                   │
│          │  ┌────────────────────────────────────────────┐  │
│          │  │ Real-time Feed                             │  │
│          │  │ [10:23] A选择了攻击B                       │  │
│          │  │ [10:24] B的Ni属性+5（洞察）                │  │
│          │  │ [10:25] 新情境触发：资源争夺战              │  │
│          │  └────────────────────────────────────────────┘  │
├──────────┴──────────────────────────────────────────────────┤
│ Status Bar: 当前Tick: #1234 | 在线Agent: 12 | 活跃情境: 3    │
└─────────────────────────────────────────────────────────────┘
```

### 2. Agent详情视图

```
┌─────────────────────────────────────────────────────────────┐
│ Agent: Alpha-7 (ID: agent_001)                    [关闭]     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐  ┌──────────────────────────────┐ │
│  │                     │  │  人格维度雷达图               │ │
│  │   Avatar            │  │                              │ │
│  │   [🤖]              │  │       认知 ●────┐            │ │
│  │                     │  │            │    │            │ │
│  │  状态: 活跃         │  │       星象 ─┘    └─ 社交     │ │
│  │  位置: 中央广场     │  │                   /          │ │
│  │  当前: 情境#3       │  │            道德 ──── 表象    │ │
│  │                     │  │                              │ │
│  └─────────────────────┘  └──────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │ 认知层: Se(23) Si(-15) Ne(45) Ni(-8) Te(12) Ti(67)... ││
│  │ [详细] [时间线]                                         ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │ 系统标签: #危机冷静者 #高Fi #不信任权威                  ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │ 关系网络:                                                ││
│  │  🤖B [盟友] 信任度: 78   🤖C [对手] 信任度: -23        ││
│  │  [查看完整图谱]                                          ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. 情境树视图

```
┌─────────────────────────────────────────────────────────────┐
│ Scenario: 潜艇沉没 (ID: scene_042)              [观看中]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ┌─────────┐                             │
│                    │ 初始节点 │                             │
│                    │ 氧气泄漏 │                             │
│                    └────┬────┘                             │
│                         │                                   │
│          ┌──────────────┼──────────────┐                    │
│          ▼              ▼              ▼                    │
│     ┌─────────┐   ┌─────────┐   ┌─────────┐               │
│     │A: 修门  │   │B: 逃跑  │   │C: 呼救  │               │
│     │ [完成]  │   │ [完成]  │   │ [当前]  │               │
│     └────┬────┘   └────┬────┘   └────┬────┘               │
│          │             │             │                     │
│          ▼             ▼             ▼                     │
│     [结果展示...]                                     │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │ 当前节点: 呼救                                         ││
│  │ 参与者: 🤖C正在选择...                                  ││
│  │ 等待中: 4/6 已决策                                      ││
│  │ 倒计时: 00:23                                          ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. 剧场视图

```
┌─────────────────────────────────────────────────────────────┐
│ Theater: 人格熔炉 #7                              [直播中]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage: 毒酒宴会 (3/5)                              [回放]  │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │                                                        ││
│  │                    [舞台可视化区域]                      ││
│  │                                                        ││
│  │     展示当前情境的戏剧化呈现                             ││
│  │     Agent位置、动作、对话气泡                           ││
│  │                                                        ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
│  参与者: 🤖A 🤖B 🤖C 🤖D (4/4)                            │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │ 实时对话:                                              ││
│  │ 🤖A: "这酒有问题，我建议大家都别喝"                     ││
│  │ 🤖B: "你凭什么决定？我觉得你在虚张声势"                 ││
│  │ 🤖C: *[保持沉默，观察其他人]*                           ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
│  [⏸️暂停] [⏪后退10s] [▶️播放] [⏩快进] [📊统计]            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、状态管理设计

```typescript
// stores/worldStore.ts
interface WorldState {
  // 基础状态
  tick: number;
  status: 'running' | 'paused';
  
  // 实体集合
  agents: Map<string, Agent>;
  scenarios: Map<string, Scenario>;
  theaters: Map<string, Theater>;
  
  // 实时事件流
  eventFeed: WorldEvent[];
  
  // 观察者焦点
  focusedAgentId?: string;
  focusedScenarioId?: string;
  focusedTheaterId?: string;
}

// 操作
interface WorldActions {
  // WebSocket推送处理
  handleAgentUpdate(update: AgentUpdate): void;
  handleScenarioUpdate(update: ScenarioUpdate): void;
  handleNewEvent(event: WorldEvent): void;
  
  // 用户操作
  focusAgent(id: string): void;
  focusScenario(id: string): void;
  
  // 回放控制
  enterReplayMode(theaterId: string): void;
  exitReplayMode(): void;
  seekTo(timestamp: number): void;
}
```

---

## 四、WebSocket消息设计

```typescript
// 订阅消息
interface SubscribeMessage {
  type: 'subscribe';
  channels: ('world' | 'agent' | 'scenario' | 'theater')[];
  ids?: string[];  // 特定ID
}

// 推送消息类型
interface AgentUpdate {
  type: 'agent.update';
  agentId: string;
  delta: Partial<Agent>;
  timestamp: number;
}

interface NewEvent {
  type: 'event.new';
  event: WorldEvent;
}

interface ScenarioAdvance {
  type: 'scenario.advance';
  scenarioId: string;
  newNode: string;
  choices: Choice[];
}
```

---

## 五、技术选型

| 类别 | 技术 | 理由 |
|------|------|------|
| 框架 | React 18 | 组件化、生态完善 |
| 语言 | TypeScript 5 | 类型安全 |
| 构建 | Vite | 快速、配置简单 |
| 样式 | Tailwind CSS | 原子化、快速开发 |
| 状态 | Zustand | 轻量、无样板代码 |
| 路由 | React Router 6 | 标准方案 |
| 可视化 | D3.js + React | 灵活绑定 |
| 3D可选 | Three.js | 未来扩展 |
| WebSocket | Socket.IO Client | 自动重连、房间管理 |
| HTTP | Axios | 标准HTTP客户端 |
| 图表 | Recharts | React友好 |

---

## 六、与后端连接

```
Observer                      Core/ Theater
  │                              │
  ├── HTTP GET /world/state ───→│
  │←─ 初始世界状态 ──────────────┤
  │                              │
  ├── WS /ws/connect ──────────→│
  │   (带token)                  │
  │                              │
  ├── WS subscribe: world ─────→│
  │                              │
  │←─ WS push: agent.update ────┤
  │←─ WS push: event.new ───────┤
  │←─ WS push: scenario.advance ─┤
  │                              │
  ├── WS subscribe: theater/7 ──→│
  │←─ WS push: theater.state ───┤
```

---

## 七、开发顺序

1. **Phase 1**: 基础布局 + WebSocket连接
2. **Phase 2**: Agent列表 + 基础详情页
3. **Phase 3**: 世界地图可视化
4. **Phase 4**: 人格雷达图 + 时间线
5. **Phase 5**: 情境树可视化
6. **Phase 6**: 剧场观看界面
7. **Phase 7**: 回放系统
