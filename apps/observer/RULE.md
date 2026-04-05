# Observer 模块编码规范

> 观察者前端 - 上帝视角，洞见真理，优雅呈现

---

## 模块定位

**Observer 是 PersonaVerse 的眼睛。**

它不做决策，不改变状态，只负责：
- 真实呈现世界的运转
- 优雅展示人格的多维
- 流畅播放剧场的叙事
- 让复杂变得可理解

**Observer 是纯粹的信息界面，它是透明的玻璃，不是滤镜。**

---

## 核心原则

### 1. 只读不写（Read-Only）

```typescript
// ✅ 正确：只订阅，不修改
function useWorldState() {
    const [state, setState] = useState<WorldState | null>(null);
    
    useEffect(() => {
        const ws = connectWebSocket();
        ws.on('world.update', (data) => {
            setState(data);  // 只更新本地状态
        });
        return () => ws.close();
    }, []);
    
    return state;  // 只读
}

// ❌ 错误：Observer 不应该发送修改请求
function badExample() {
    const ws = connectWebSocket();
    ws.send('agent.update', {  // Observer 不该这样做
        agentId: '123',
        newState: {...}
    });
}
```

**规则**：Observer 唯一的写操作是用户界面偏好（如主题、布局）。

### 2. 渐进披露（Progressive Disclosure）

```typescript
// ✅ 正确：信息分层展示
function AgentCard({ agent }: { agent: Agent }) {
    return (
        <Card>
            {/* 第一层：一眼可见 */}
            <Avatar name={agent.name} status={agent.status} />
            <Name>{agent.name}</Name>
            <Tags tags={agent.surfaceTraits} />  {/* 表象标签 */}
            
            {/* 第二层：悬停/点击展开 */}
            <Expandable>
                <PersonalityRadar data={agent.personality} />
                <RecentActivity events={agent.recentEvents} />
            </Expandable>
            
            {/* 第三层：详情页 */}
            <Link to={`/agents/${agent.id}`}>
                完整档案 →
            </Link>
        </Card>
    );
}
```

**规则**：不要一次性展示所有信息，让用户按需探索。

### 3. 实时反馈（Real-Time Feedback）

```typescript
// ✅ 正确：每个重要事件都有视觉反馈
function WorldMap() {
    const [events, setEvents] = useState<Event[]>([]);
    
    useEffect(() => {
        ws.on('event.new', (event) => {
            // 1. 添加到事件流
            setEvents(prev => [event, ...prev]);
            
            // 2. 地图上闪烁标记
            flashMarker(event.location);
            
            // 3. 如果相关，弹出通知
            if (isRelevant(event, focusedAgent)) {
                toast.info(`${event.actor} ${event.action}`);
            }
        });
    }, []);
}
```

**规则**：世界在运转，界面要让人"感觉到"活力。

### 4. 可回放（Replayable）

```typescript
// ✅ 正确：所有状态可回放
function ReplayProvider({ children }) {
    const [mode, setMode] = useState<'live' | 'replay'>('live');
    const [currentTick, setCurrentTick] = useState(0);
    
    const state = mode === 'live' 
        ? useLiveState() 
        : useReplayState(currentTick);
    
    return (
        <StateContext.Provider value={{ state, mode, setCurrentTick }}>
            {children}
            {mode === 'replay' && <ReplayControls />}
        </StateContext.Provider>
    );
}
```

**规则**：任何时刻都应该可以暂停、回放、慢动作。

---

## 目录组织

```
observer/src/
├── components/         # 组件
│   ├── layout/        # 布局组件
│   │   └── 规则：
│   │       - 只负责布局，不承载业务逻辑
│   │       - 响应式支持（mobile/tablet/desktop）
│   │
│   ├── world/         # 世界视图
│   │   └── 规则：
│   │       - 使用 D3/Three.js 进行可视化
│   │       - 支持缩放、平移、筛选
│   │       - 性能优化（虚拟化、节流）
│   │
│   ├── agent/         # Agent 组件
│   │   └── 规则：
│   │       - AgentCard 必须支持不同尺寸
│   │       - PersonalityRadar 使用统一配色
│   │       - TraitTimeline 支持时间缩放
│   │
│   ├── scenario/      # 情境组件
│   │   └── 规则：
│   │       - ScenarioTree 使用层级布局
│   │       - ChoiceNode 明确显示状态（等待/完成/当前）
│   │       - LiveTranscript 自动滚动
│   │
│   ├── theater/       # 剧场组件
│   │   └── 规则：
│   │       - LiveStage 是主要观看区域
│   │       - ReplayControls 支持变速播放
│   │       - TheaterList 显示关键指标
│   │
│   └── common/        # 通用组件
│       └── 规则：
│           - 原子化设计（Button, Card, Badge）
│           - 统一主题色和间距
│
├── hooks/             # 自定义 Hooks
│   └── 规则：
│       - 一个 Hook 一个职责
│       - 必须处理 loading/error 状态
│       - 自动清理副作用
│
├── services/          # 服务层
│   └── 规则：
│       - API 调用集中管理
│       - WebSocket 连接统一管理
│       - 错误处理和重试逻辑
│
├── stores/            # 状态管理
│   └── 规则：
│       - 使用 Zustand，避免 Redux 样板
│       - 按领域拆分（world/agent/scenario/ui）
│       - 持久化用户偏好
│
├── types/             # TypeScript 类型
│   └── 规则：
│       - 与后端 API 对应
│       - 共享类型从 shared-models 导入
│       - 前端特有类型本地定义
│
└── utils/             # 工具函数
    └── 规则：
        - 纯函数，无副作用
        - 有单元测试
        - 命名清晰
```

---

## 组件设计规范

### 组件结构

```typescript
// ✅ 标准组件模板
import React from 'react';
import { useAgent } from '@/hooks/useAgent';
import { Card, Avatar, Badge } from '@/components/common';
import styles from './AgentCard.module.css';  // 或 Tailwind

// Props 类型定义
interface AgentCardProps {
    agentId: string;
    variant?: 'compact' | 'full' | 'minimal';
    onClick?: (agent: Agent) => void;
}

// 组件实现
export const AgentCard: React.FC<AgentCardProps> = ({
    agentId,
    variant = 'compact',
    onClick
}) => {
    // 数据获取
    const { agent, isLoading, error } = useAgent(agentId);
    
    // 状态处理
    if (isLoading) return <Skeleton variant={variant} />;
    if (error) return <ErrorMessage error={error} />;
    if (!agent) return null;
    
    // 渲染
    return (
        <Card 
            className={styles.card}
            onClick={() => onClick?.(agent)}
            data-variant={variant}
        >
            <Avatar src={agent.avatar} status={agent.status} />
            <div className={styles.info}>
                <h3>{agent.name}</h3>
                <Tags tags={agent.tags} />
            </div>
            {variant === 'full' && <PersonalityPreview agent={agent} />}
        </Card>
    );
};

export default AgentCard;
```

### 性能优化

```typescript
// ✅ 使用 memo 避免不必要的重渲染
export const AgentList = React.memo<AgentListProps>(({ agents }) => {
    return (
        <ul>
            {agents.map(agent => (
                <AgentCard key={agent.id} agentId={agent.id} />
            ))}
        </ul>
    );
});

// ✅ 大数据列表使用虚拟化
import { FixedSizeList } from 'react-window';

function EventFeed({ events }: { events: Event[] }) {
    return (
        <FixedSizeList
            height={500}
            itemCount={events.length}
            itemSize={50}
            itemData={events}
        >
            {EventRow}
        </FixedSizeList>
    );
}

// ✅ 防抖高频更新
function useThrottledState<T>(initial: T, delay: number = 100) {
    const [state, setState] = useState(initial);
    const throttledSet = useMemo(
        () => throttle(setState, delay),
        [delay]
    );
    return [state, throttledSet] as const;
}
```

---

## 状态管理规范

### Store 拆分

```typescript
// stores/worldStore.ts
interface WorldState {
    tick: number;
    status: 'running' | 'paused';
    agents: Map<string, Agent>;
    scenarios: Map<string, Scenario>;
    events: Event[];
}

export const useWorldStore = create<WorldState & WorldActions>((set, get) => ({
    tick: 0,
    status: 'running',
    agents: new Map(),
    scenarios: new Map(),
    events: [],
    
    // Actions
    handleAgentUpdate: (update) => set((state) => {
        const agents = new Map(state.agents);
        agents.set(update.id, { ...agents.get(update.id), ...update });
        return { agents };
    }),
    
    handleNewEvent: (event) => set((state) => ({
        events: [event, ...state.events].slice(0, 1000)  // 限制数量
    })),
}));

// stores/uiStore.ts - UI 状态单独管理
interface UIState {
    sidebarOpen: boolean;
    theme: 'light' | 'dark';
    focusedAgent: string | null;
}

export const useUIStore = create<UIState & UIActions>((set) => ({
    sidebarOpen: true,
    theme: 'dark',
    focusedAgent: null,
    
    toggleSidebar: () => set(s => ({ sidebarOpen: !s.sidebarOpen })),
    setTheme: (theme) => set({ theme }),
    focusAgent: (id) => set({ focusedAgent: id }),
}), {
    name: 'ui-store',
    partialize: (state) => ({ theme: state.theme })  // 只持久化主题
});
```

---

## 可视化规范

### 颜色系统

```typescript
// 维度颜色映射（统一整个应用）
const DIMENSION_COLORS = {
    // 认知层
    cognitive: {
        Se: '#FF6B6B',  // 红色 - 当下行动
        Si: '#4ECDC4',  // 青色 - 经验
        Ne: '#FFE66D',  // 黄色 - 可能性
        Ni: '#95E1D3',  // 薄荷 - 洞察
        Te: '#F38181',  // 粉红 - 效率
        Ti: '#AA96DA',  // 紫色 - 逻辑
        Fe: '#FCBAD3',  // 浅粉 - 和谐
        Fi: '#FFFFD2',  // 淡黄 - 价值
    },
    // 其他层...
} as const;

// 状态颜色
const STATUS_COLORS = {
    active: '#10B981',     // 绿色
    inactive: '#6B7280',   // 灰色
    sleeping: '#6366F1',   // 靛蓝
    error: '#EF4444',      // 红色
} as const;
```

### 图表组件

```typescript
// PersonalityRadar.tsx
import { Radar, RadarChart, PolarGrid, PolarAngleAxis } from 'recharts';

interface RadarData {
    dimension: string;
    value: number;  // -100 to 100
    fullMark: 100;
}

export const PersonalityRadar: React.FC<{
    data: RadarData[];
    color?: string;
}> = ({ data, color = '#8884d8' }) => {
    return (
        <RadarChart cx={200} cy={200} outerRadius={150} width={400} height={400} data={data}>
            <PolarGrid />
            <PolarAngleAxis dataKey="dimension" />
            <Radar
                name="Personality"
                dataKey="value"
                stroke={color}
                fill={color}
                fillOpacity={0.3}
            />
        </RadarChart>
    );
};
```

---

## WebSocket 管理

```typescript
// services/websocket.ts
class WebSocketManager {
    private ws: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private listeners = new Map<string, Set<Function>>();
    
    connect() {
        this.ws = new WebSocket(WS_URL);
        
        this.ws.onopen = () => {
            this.reconnectAttempts = 0;
            this.authenticate();
        };
        
        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleMessage(message);
        };
        
        this.ws.onclose = () => {
            this.attemptReconnect();
        };
    }
    
    subscribe(channel: string, callback: Function) {
        if (!this.listeners.has(channel)) {
            this.listeners.set(channel, new Set());
            this.send({ type: 'subscribe', channel });
        }
        this.listeners.get(channel)!.add(callback);
        
        // 返回取消订阅函数
        return () => {
            this.listeners.get(channel)?.delete(callback);
        };
    }
    
    private handleMessage(message: any) {
        const { type, data } = message;
        const handlers = this.listeners.get(type);
        handlers?.forEach(handler => {
            try {
                handler(data);
            } catch (e) {
                console.error('Handler error:', e);
            }
        });
    }
}

export const wsManager = new WebSocketManager();
```

---

## 代码规范

### ESLint 配置

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react-hooks/recommended"
  ],
  "rules": {
    "@typescript-eslint/explicit-function-return-type": "warn",
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn",
    "no-console": ["warn", { "allow": ["error", "warn"] }]
  }
}
```

### 文件模板

```typescript
// 每个文件顶部
/**
 * @file AgentCard.tsx
 * @description Agent 信息卡片组件
 * @author PersonaVerse Team
 */

import React from 'react';
// ... imports
```

---

## 性能预算

| 指标 | 目标 | 最大 |
|------|------|------|
| 首屏加载 | < 2s | < 3s |
| 交互响应 | < 100ms | < 200ms |
| 动画帧率 | 60fps | 30fps |
| 内存占用 | < 100MB | < 200MB |

---

## 一句话总结

> Observer 是世界的镜子：不评判，只呈现；不干扰，只记录；让真理可见，让复杂优雅。
