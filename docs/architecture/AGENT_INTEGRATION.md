# Agent 接入架构设计

> 文档版本: 1.1  
> 最后更新: 2026-04-06  
> 状态: 技术细节已补充，待评审

---

## 快速参考

| 关键参数 | 值 |
|----------|-----|
| 心跳间隔 | 30s |
| 心跳超时 | 60s |
| 决策超时 | 30s |
| 重连初始延迟 | 1s |
| 重连最大延迟 | 60s |
| 单 Agent 最大连接 | 100 |
| 消息大小限制 | 64KB |

---

## 一、背景与需求

### 1.1 场景描述

我们需要支持**第三方 AI Agent（如 OpenClaw）接入 PersonaVerse 平台**，形成以下交互模式：

- **远端服务端**：PersonaVerse Core（部署在云服务器，有公网 IP）
- **本地客户端**：用户自己的 OpenClaw（部署在本地/内网，无公网 IP）
- **核心需求**：服务端能够主动向客户端发送消息（如决策请求），客户端处理后返回结果

### 1.2 约束条件

| 约束 | 说明 |
|------|------|
| 客户端无公网 IP | 无法直接暴露 HTTP 服务供服务端回调 |
| 防火墙限制 | 客户端通常只能发起出站连接 |
| 客户端极简原则 | 客户端应尽量少做工作，复杂度放在服务端 |
| 实时性要求 | 需要双向实时通信，轮询方案不合适 |

---

## 二、推荐方案：WebSocket 反向连接

### 2.1 架构概述

参考 OpenClaw 接入钉钉/飞书的 Channel 模式，采用**客户端主动连接 + 长连接保持**的架构：

```
┌─────────────────────────────────────────────────────────────────┐
│                        PersonaVerse 服务端                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              WebSocket Connection Manager                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │   │
│  │  │ Connection  │  │ Connection  │  │   Connection    │  │   │
│  │  │  (claw_01)  │  │  (claw_02)  │  │    (claw_03)    │  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘  │   │
│  │         └─────────────────┴──────────────────┘            │   │
│  │                          │                                │   │
│  │                    ┌─────┴─────┐                          │   │
│  │                    │  Router   │  ← 按 agent_id 路由消息   │   │
│  │                    └─────┬─────┘                          │   │
│  └──────────────────────────┼────────────────────────────────┘   │
│                             │                                     │
│  ┌──────────────────────────▼────────────────────────────────┐   │
│  │              Core 世界引擎（ScenarioRunner）                 │   │
│  │     需要 Agent 决策时 → 查找连接 → 发送 DecisionRequest      │   │
│  └────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────┬────────────────────────────┘
                                     │ WebSocket (WSS)
                                     │ 客户端主动建立
┌────────────────────────────────────▼────────────────────────────┐
│                        OpenClaw 客户端（本地）                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Agent Adapter Module                    │   │
│  │                                                          │   │
│  │  1. 启动时连接 wss://personaverse.com/ws/agent          │   │
│  │  2. 发送注册信息 {agent_id, capabilities, version}      │   │
│  │  3. 监听消息循环                                          │   │
│  │     ├── 收到 DecisionRequest → 调用本地 LLM 处理        │   │
│  │     └── 返回 DecisionResponse                           │   │
│  │  4. 自动心跳保活 + 断线重连                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                             │                                   │
│                             ▼                                   │
│                    ┌─────────────────┐                         │
│                    │   本地 LLM      │                         │
│                    │ (Ollama/Claude) │                         │
│                    └─────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 时序图

```
OpenClaw (本地)              PersonaVerse (远端)
    │                              │
    ├── 1. WebSocket 连接 ────────→│ wss://pv.com/ws/agent
    │   {agent_id: "claw_01",      │
    │    version: "1.0.0",         │
    │    capabilities: [...]}      │
    │                              │
    │                              ├── 2. 验证 agent_id
    │                              ├── 3. 存入 ConnectionPool
    │◄── 4. 返回确认 ─────────────│ {status: "connected"}
    │                              │
    │◄═══ 5. 心跳保活 (30s) ════════│ 双向 ping/pong
    │                              │
    │◄── 6. DecisionRequest ──────│ Core 需要决策
    │   {scenario_id: "s_001",     │
    │    context: {...},           │
    │    timeout: 30000}           │
    │                              │
    ├── 7. 本地 LLM 推理 ────────→│ (本地处理，无网络)
    │                              │
    │◄── 8. 生成决策结果 ─────────│
    │                              │
    ├── 9. DecisionResponse ─────→│ {choice: "A",
    │                              │  reasoning: "..."}
    │                              │
    │                              ├── 10. 更新世界状态
    │                              ├── 11. 通知其他 Agent
    │◄── 12. 下一个请求/等待 ──────│
```

### 2.3 协议设计

#### 2.3.1 连接建立

```http
GET wss://api.personaverse.com/v1/agents/connect
Headers:
  X-Agent-ID: claw_01
  X-Agent-Token: <jwt_token>
  X-Version: 1.0.0
  X-Protocol-Version: pv-agent-v1
```

**连接参数：**

| 参数 | 值 | 说明 |
|------|-----|------|
| 协议版本 | pv-agent-v1 | 用于未来协议升级兼容 |
| 初始超时 | 10s | WebSocket 握手超时 |
| 连接限额 | 100/Agent | 单 Agent 最大并发连接数 |

#### 2.3.2 消息格式

**基础消息结构：**
```json
{
  "type": "message_type",
  "msg_id": "uuid_v7",      // 全局唯一消息ID，用于幂等和追踪
  "timestamp": 1712380800,   // Unix timestamp (ms)
  "payload": {...}           // 具体消息内容
}
```

**服务端 → 客户端：DecisionRequest**
```json
{
  "type": "decision_request",
  "msg_id": "req_xxx",
  "payload": {
    "scenario_id": "scene_xxx",
    "node_id": "node_xxx",
    "context": {
      "situation": "你在一个陌生的房间里...",
      "available_choices": [
        {"id": "A", "text": "开门出去"},
        {"id": "B", "text": "先观察环境"}
      ],
      "persona_traits": {...}
    },
    "timeout_ms": 30000
  }
}
```

**客户端 → 服务端：DecisionResponse**
```json
{
  "type": "decision_response",
  "msg_id": "resp_xxx",
  "ref_msg_id": "req_xxx",    // 引用请求消息ID
  "payload": {
    "agent_id": "claw_01",
    "choice": "B",
    "reasoning": "作为谨慎的性格，我选择先观察...",
    "latency_ms": 1250
  }
}
```

**心跳机制详细参数：**

| 参数 | 值 | 说明 |
|------|-----|------|
| 心跳间隔 | 30s | 客户端发送 ping 间隔 |
| 心跳超时 | 60s | 服务端未收到 ping 视为断开 |
|  pong 超时 | 10s | 发送 ping 后等待 pong 超时 |
|  最大失败次数 | 3 | 连续 3 次 ping 无响应触发重连 |

```json
// 客户端发送
{"type": "ping", "msg_id": "ping_001", "timestamp": 1712380800}
// 服务端回复
{"type": "pong", "ref_msg_id": "ping_001", "timestamp": 1712380800}
```

**状态广播：**
```json
// 服务端广播世界状态更新
{
  "type": "state_update",
  "msg_id": "state_001",
  "payload": {
    "world_tick": 12345,
    "visible_events": [...],
    "scenario_updates": {...}
  }
}
```

### 2.4 客户端职责（极简）

| 职责 | 说明 |
|------|------|
| 建立连接 | 启动时连接远端 WebSocket |
| 身份注册 | 发送 agent_id 和基本信息 |
| 消息监听 | 阻塞监听，收到请求后处理 |
| 本地推理 | 调用本地 LLM 生成决策 |
| 返回结果 | 通过同一连接发送响应 |
| 心跳保活 | 每 30s 发送 ping，等待 pong |
| 断线重连 | 指数退避重连策略 |

**客户端重连策略详细参数：**

```python
RECONNECT_POLICY = {
    "initial_delay": 1.0,           # 首次重连等待 1s
    "max_delay": 60.0,              # 最大重连间隔 60s
    "multiplier": 2.0,              # 指数退避乘数
    "jitter": 0.1,                  # 10% 随机抖动，避免惊群
    "max_attempts": None,           # 无限重连（None）或指定次数
    "reset_after": 300.0,           # 成功连接 5min 后重置退避计数
}

# 重连间隔序列：1s, 2s, 4s, 8s, 16s, 32s, 60s, 60s...
```

**客户端状态机：**

```
[Disconnected] ──启动/重连──→ [Connecting]
                                    │
                                    ▼
[Reconnecting] ◄──失败/断开── [Connected] ──注册成功──→ [Ready]
     │                                                       │
     │                                                       │ 接收 DecisionRequest
     │                                                       ▼
     └──────────────── 回到 Connecting ◄─────────── [Processing]
```

### 2.5 服务端职责（承担复杂度）

| 职责 | 说明 |
|------|------|
| 连接管理 | 维护所有在线 Agent 的连接池 |
| 身份验证 | 验证 agent_id 和 token 合法性 |
| 状态追踪 | 记录每个 Agent 的在线/离线状态 |
| 消息路由 | 根据 agent_id 找到对应连接发送请求 |
| 超时处理 | 等待响应超时后重试或标记失败 |
| 消息队列 | 离线时缓存消息，重连后推送 |
| 负载均衡 | 同一 Agent 多实例时的选择策略 |

**服务端超时处理详细参数：**

| 超时类型 | 时间 | 处理方式 |
|----------|------|----------|
| Decision 响应 | 30s | 超时后标记为默认选择，记录日志 |
| WebSocket 发送 | 10s | 发送缓冲区满或网络阻塞 |
| 连接建立 | 10s | WebSocket 握手超时 |
| 心跳检测 | 60s | 未收到 ping，主动关闭连接 |
| 优雅关闭 | 5s | 关闭时等待未完成消息 |

**服务端重试策略：**

```python
RETRY_POLICY = {
    "max_retries": 2,               # 最多重试 2 次
    "retry_delay": 1.0,             # 首次重试等待 1s
    "retry_backoff": 2.0,           # 退避乘数
    "retry_conditions": [           # 仅在以下情况重试
        "ConnectionResetError",
        "TimeoutError", 
        "AgentDisconnected"
    ]
}

# 注意：Agent 已处理过的决策不重试，避免重复决策
```

**连接池管理：**

```python
class ConnectionPool:
    # 数据结构
    connections: Dict[str, Set[WebSocket]]  # agent_id -> 连接集合
    agent_state: Dict[str, AgentState]       # agent_id -> 状态元数据
    pending_requests: Dict[str, PendingReq]  # request_id -> 等待中的请求
    
    # 容量限制
    max_connections_per_agent = 100
    max_pending_requests = 1000
    
    # 清理策略
    stale_connection_timeout = 120  # 2min 无心跳视为失效
    cleanup_interval = 60           # 每 60s 扫描清理
```

**消息队列（离线缓存）：**

```python
OFFLINE_QUEUE_CONFIG = {
    "max_size_per_agent": 100,      # 单 Agent 最大缓存消息数
    "max_total_size": 10000,        # 全局最大缓存数
    "ttl_seconds": 3600,            # 消息有效期 1h
    "drop_policy": "oldest",        # 满时丢弃最旧消息
}
```

---

## 三、潜在问题与解决方案

### 3.1 网络分区与连接中断

**问题描述：**
- 客户端网络波动（WiFi 切换、VPN 断开、路由器重启）
- 服务端部署更新需要重启
- 中间代理（Nginx/Cloudflare）超时断开连接

**解决方案：**
1. **快速检测**：WebSocket 层 ping/pong 帧（比应用层心跳更快）
2. **优雅重连**：指数退避 + 抖动，避免所有客户端同时重连压垮服务端
3. **状态恢复**：
   ```json
   // 重连时客户端发送
   {"type": "resume", "last_received_msg_id": "msg_xxx", "agent_id": "claw_01"}
   // 服务端返回断线期间错过的消息
   ```

**潜在风险：**
- 网络闪断（<1s）可能导致消息重复发送
- 需要设计幂等机制（基于 msg_id 去重）

### 3.2 消息丢失与重复

**问题场景：**

| 场景 | 风险 | 应对策略 |
|------|------|----------|
| 服务端发送后崩溃 | 客户端收到但 ACK 丢失 | 客户端幂等处理，重复 Decision 相同结果 |
| 客户端处理中崩溃 | 决策结果丢失 | 服务端超时后重发给其他实例 |
| 网络分区 | 双方都认为对方离线 | 分区恢复后状态同步 |

**幂等保证：**
```python
# 服务端记录已处理的 response
processed_responses: Set[str]  # request_id 集合，TTL 5min

# 客户端相同 request_id 返回相同结果（基于缓存）
decision_cache: Dict[str, DecisionResponse]  # request_id -> response
```

### 3.3 服务端重启后的状态恢复

**问题描述：**
- Core 重启后丢失内存中的连接池
- 正在进行的 Scenario 需要恢复

**解决方案：**
1. **持久化状态**：
   - Redis 保存 `agent_id → 连接元数据`（非连接本身，可重建）
   - PostgreSQL 保存 Scenario 状态
2. **恢复流程**：
   ```
   Core 重启
       ↓
   从 DB 恢复活跃 Scenario
       ↓
   等待 Agent 重连（不主动连接）
       ↓
   Agent 重连时发送 resume 请求
       ↓
   恢复断点继续运行
   ```

### 3.4 安全性问题

**攻击面分析：**

| 攻击类型 | 风险等级 | 防护措施 |
|----------|----------|----------|
| 伪造 Agent | 高 | JWT Token 验证 + agent_id 白名单 |
| 重放攻击 | 中 | Token 包含时间戳，有效期 5min |
| DDoS 连接 | 高 | 单 IP 连接限流（10 conn/min） |
| 消息篡改 | 中 | WSS 加密传输 |
| 内存耗尽 | 中 | 单 Agent 连接数限制 + 消息大小限制 |

**认证流程：**
```
1. 用户注册 Agent → 服务端生成 agent_id + secret
2. 客户端连接时：JWT(agent_id, secret, timestamp) → Token
3. 服务端验证：签名正确 + timestamp 未过期 + agent_id 存在
```

**消息大小限制：**
```python
MAX_MESSAGE_SIZE = 64 * 1024      # 64KB 单条消息限制
MAX_DECISION_CONTEXT = 32 * 1024  # 32KB Decision 上下文
MAX_REASONING_LENGTH = 4000       # 推理文本最大 4000 字符
```

### 3.5 资源泄漏

**潜在泄漏点：**
1. **连接泄漏**：客户端异常退出未关闭连接
   - 解决：心跳超时自动清理（60s 无 ping 关闭）
2. **内存泄漏**：消息队列无限增长
   - 解决：限制队列大小，LRU 淘汰
3. **文件句柄泄漏**：WebSocket 连接句柄未释放
   - 解决：上下文管理器确保关闭

**监控指标：**
```python
METRICS = {
    "active_connections": Gauge,      # 当前活跃连接数
    "messages_per_second": Counter,   # 消息速率
    "reconnect_rate": Counter,        # 重连频率
    "average_latency": Histogram,     # 决策延迟分布
    "error_rate": Counter,            # 错误率
}
```

### 3.6 时序与竞态条件

**问题场景：**
- 同一 Agent 多个连接同时处理不同 Decision
- 快速重连时旧连接未完全清理

**解决方案：**
1. **连接去重**：同一 agent_id 新连接建立时，关闭旧连接
2. **请求并发控制**：
   ```python
   # 服务端限制单 Agent 并发 Decision 数
   max_concurrent_decisions_per_agent = 3
   ```
3. **顺序保证**：
   - 同 Scenario 的 Decision 按顺序发送
   - 不同 Scenario 可并行处理

### 3.7 大消息传输问题

**问题描述：**
- 复杂 Scenario 的 context 可能很大（>100KB）
- 超出 WebSocket 默认帧大小（64KB）

**解决方案：**
1. **分片传输**：大消息拆分为多帧（WebSocket 原生支持）
2. **引用传递**：
   ```json
   {
     "type": "decision_request",
     "payload": {
       "context_ref": "scenario:xxx:context",  // 引用 Redis 中的完整上下文
       "context_summary": "精简摘要..."         // 用于快速理解
     }
   }
   ```
3. **压缩**：启用 permessage-deflate 压缩

### 3.8 版本兼容性

**问题描述：**
- 协议升级后旧版 Agent 无法连接
- 新增字段导致旧客户端解析失败

**解决方案：**
1. **协议版本协商**：
   - Header: `X-Protocol-Version: pv-agent-v1`
   - 服务端拒绝不兼容版本，返回 `426 Upgrade Required`
2. **字段兼容性**：
   - 新增字段为 optional
   - 旧客户端忽略未知字段（JSON 宽松解析）
3. **平滑升级**：
   - 同时支持多个协议版本
   - 逐步淘汰旧版本（deprecation notice）

### 3.9 调试与可观测性

**问题描述：**
- 分布式场景下难以追踪消息流
- 客户端本地问题难以复现

**解决方案：**
1. **全链路追踪**：
   ```json
   {
     "trace_id": "trace_xxx",      // 整个请求链路
     "span_id": "span_xxx",        // 当前阶段
     "parent_span_id": "parent_xxx"
   }
   ```
2. **日志标准格式**：
   ```
   [timestamp] [level] [agent_id] [trace_id] [component] message
   ```
3. **调试模式**：
   - 客户端启动参数 `--debug` 开启详细日志
   - 服务端提供 `/debug/agent/{id}/messages` 查看最近消息

### 3.10 本地 LLM 延迟问题

**问题描述：**
- 本地 Ollama 推理可能很慢（>30s）
- 导致服务端超时误判

**解决方案：**
1. **流式响应**：
   ```json
   // 服务端支持流式接收
   {"type": "decision_chunk", "content": "..."}
   {"type": "decision_chunk", "content": "..."}
   {"type": "decision_complete", "final_choice": "A"}
   ```
2. **进度通知**：
   ```json
   // 客户端定期发送进度
   {"type": "progress", "request_id": "xxx", "percent": 50, "eta_seconds": 10}
   ```
3. **动态超时**：根据历史延迟调整超时时间

---

## 四、备选方案对比

### 4.1 方案对比表

| 方案 | 连接方向 | 客户端工作 | 复杂度 | 适用场景 |
|------|----------|------------|--------|----------|
| **WebSocket 反向连接** | 客户端→服务端 | 最少 | 中 | ⭐ 推荐方案 |
| WebHook + 内网穿透 | 服务端→客户端 | 需配穿透 | 高 | 客户端有临时公网能力 |
| SSE + HTTP POST | 客户端→服务端 | 较少 | 低 | 单向推送为主 |
| gRPC 双向流 | 客户端→服务端 | 较少 | 高 | 内部微服务 |
| 消息队列 (MQ) | 双方→MQ | 较少 | 高 | 高可靠异步场景 |
| HTTP 长轮询 | 客户端→服务端 | 中等 | 低 | 兼容性要求高的旧系统 |

### 4.2 各方案详情

#### 方案 A：WebHook + 内网穿透

```
OpenClaw (本地) ──frp/ngrok──→ 公网地址
     ▲                              │
     └────────── HTTP POST ─────────┘
              服务端主动回调
```

- **优点**：服务端直接调用，符合传统 HTTP API 思维
- **缺点**：
  - 客户端需配置内网穿透工具（frp/ngrok）
  - 穿透服务稳定性依赖第三方
  - 配置复杂，对用户不友好

#### 方案 B：SSE + HTTP POST

```
OpenClaw ──HTTP SSE──→ 服务端（保持连接接收推送）
     │                        │
     └──HTTP POST 结果───────┘
```

- **优点**：基于标准 HTTP，兼容性好
- **缺点**：
  - SSE 只能服务端→客户端单向
  - 客户端回复需另开 HTTP POST
  - 连接管理较复杂

#### 方案 C：gRPC 双向流

```
OpenClaw ──gRPC Bidirectional Stream──→ 服务端
```

- **优点**：高性能、强类型、流式支持好
- **缺点**：
  - 需定义 protobuf
  - 浏览器/部分环境支持差
  - 调试复杂

#### 方案 D：消息队列 (Redis/RabbitMQ)

```
OpenClaw ──订阅──→ Redis Channel ←── 服务端发布
     │                                    │
     └── 发布结果 ──→ Redis Channel ───┘
```

- **优点**：完全解耦、可靠性高、支持离线消息
- **缺点**：
  - 需额外部署 MQ 服务
  - 延迟稍高
  - 架构复杂

---

## 五、行业调研参考

### 5.1 OpenClaw 现有 Channel 模式

OpenClaw 接入 IM 平台的通用模式：

| 平台 | 连接方式 | OpenClaw 角色 |
|------|----------|---------------|
| **钉钉** | WebSocket | 客户端（连接钉钉服务器） |
| **飞书** | WebSocket 长连接 | 客户端（连接飞书服务器） |
| **QQ (OneBot)** | WebSocket/HTTP | 服务端（接收 go-cqhttp 推送） |
| **企业微信** | 长连接/回调 | 混合模式 |

**关键洞察**：当 OpenClaw 作为**客户端**时，都采用 WebSocket 主动连接平台服务器；当作为**服务端**时，需要平台能直接访问到它（需要公网 IP）。

### 5.2 其他 Agent 框架方案

| 框架 | 远程 Agent 方案 | 参考链接 |
|------|-----------------|----------|
| **Claude Desktop** | 本地运行，通过官方 API 中转 | - |
| **AutoGPT** | 本地运行，需自行暴露服务 | - |
| **HiClaw** | 内置 Matrix Server，客户端连 Matrix | 无需配置 Feishu/DingTalk |
| **cc-connect** | 支持多平台，本地作为客户端连接 | 支持 Feishu/DingTalk/Slack 等 |

### 5.3 类似架构的产品

- **VSCode Remote SSH**：本地客户端连接远程服务端，与我们的方案类似
- **Cloudflare Tunnel**：客户端主动出向连接，无需公网 IP
- **Tailscale/ZeroTier**：P2P 打洞，但需双方安装客户端

---

## 六、后续改进方向 (Roadmap)

### Phase 1：MVP 实现（当前）

- [ ] 基础 WebSocket 客户端/服务端实现

- [ ] WebSocket 基础连接
- [ ] JSON 文本协议
- [ ] 简单心跳保活
- [ ] 单实例 Agent 支持

### Phase 2：稳定性增强

- [ ] 断线自动重连（指数退避）
- [ ] 消息队列（离线消息缓存）
- [ ] 多实例 Agent 负载均衡
- [ ] 连接健康监控

### Phase 3：性能优化

- [ ] 二进制协议（MessagePack）
- [ ] 流式传输（Stream Decision）
- [ ] 压缩（permessage-deflate）
- [ ] 连接池优化

### Phase 4：功能扩展

- [ ] 多 Agent 协作通信
- [ ] Agent 能力动态发现
- [ ] 文件/图片传输
- [ ] 端到端加密

### Phase 5：企业级特性

- [ ] mTLS 双向认证
- [ ] 代理服务器支持（HTTP/SOCKS5）
- [ ] 私有化部署网关
- [ ] 审计日志

---

## 七、决策记录 (ADR)

### ADR-001: 选择 WebSocket 反向连接

**决策日期**: 2026-04-06  
**决策状态**: 已接受  

**上下文**：
- 客户端（OpenClaw）通常运行在无公网 IP 的内网环境
- 服务端（PersonaVerse）部署在云服务器，有固定公网地址
- 需要服务端能够主动发起通信

**考虑方案**：
1. WebSocket 反向连接
2. WebHook + 内网穿透
3. SSE + HTTP POST
4. gRPC 双向流

**决策**：采用 **WebSocket 反向连接**

**理由**：
1. **客户端极简**：无需配置穿透工具，自动重连逻辑简单
2. **成熟模式**：参考 OpenClaw Channel 架构，有大量先例
3. **实时性好**：真正的双向实时通信
4. **穿透性强**：只需客户端能访问外网即可，兼容各种防火墙

**权衡**：
- ✅ 服务端需维护连接池（复杂度转移）
- ✅ 需处理断线重连（已有成熟方案）
- ❌ 不适合浏览器环境（但我们的客户端是 OpenClaw，非浏览器）

---

## 七、附录

### 7.1 术语表

| 术语 | 说明 |
|------|------|
| Agent | 在 PersonaVerse 中，指接入的 AI 实体，可以是本地 OpenClaw 或其他 AI 服务 |
| Channel | OpenClaw 中的概念，指接入特定平台（如钉钉、飞书）的适配器 |
| DecisionRequest | 服务端向 Agent 发送的决策请求 |
| ConnectionPool | 服务端维护的 WebSocket 连接池 |

### 7.2 参考资料

1. [OpenClaw GitHub](https://github.com/OpenClaw/OpenClaw) - 官方仓库
2. [dingtalk-openclaw-connector](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector) - 钉钉接入实现参考
3. [OpenClaw 飞书接入文档](https://open.feishu.cn/document/home/index) - 飞书开放平台
4. [WebSocket RFC 6455](https://tools.ietf.org/html/rfc6455)

---

## 附录 B：风险清单与缓解措施汇总

| 风险 | 概率 | 影响 | 缓解措施 | 状态 |
|------|------|------|----------|------|
| 网络闪断导致消息重复 | 高 | 中 | 基于 request_id 的幂等处理 | 待实现 |
| 服务端重启丢失连接 | 中 | 高 | Redis 持久化 + 状态恢复 | 待实现 |
| 客户端频繁重连压垮服务 | 中 | 高 | 指数退避 + 抖动 + 连接限流 | 已设计 |
| 本地 LLM 超时 | 高 | 中 | 流式响应 + 进度通知 + 动态超时 | 待实现 |
| 伪造 Agent 攻击 | 低 | 高 | JWT 认证 + 白名单 + IP 限流 | 待实现 |
| 消息队列内存溢出 | 低 | 高 | 队列大小限制 + LRU 淘汰 | 已设计 |
| 协议版本不兼容 | 低 | 中 | 版本协商 + 向后兼容字段 | 已设计 |
| 大 Context 传输失败 | 中 | 中 | 引用传递 + 分片 + 压缩 | 待实现 |

---

## 附录 C：开发检查清单

### 服务端实现
- [ ] WebSocket 连接管理器（ConnectionPool）
- [ ] JWT 认证中间件
- [ ] 心跳检测与超时清理
- [ ] 消息路由器（按 agent_id 路由）
- [ ] 超时处理器（Decision 30s 超时）
- [ ] 幂等性保证（processed_responses 缓存）
- [ ] 离线消息队列（Redis）
- [ ] 状态恢复机制（Core 重启后恢复）
- [ ] 监控指标上报
- [ ] 优雅关闭处理

### 客户端实现
- [ ] WebSocket 连接管理
- [ ] 指数退避重连策略
- [ ] 心跳保活（30s ping）
- [ ] 决策缓存（幂等性）
- [ ] 状态恢复请求（resume）
- [ ] 本地 LLM 集成
- [ ] 流式响应支持（可选）
- [ ] 日志与调试模式

### 测试场景
- [ ] 正常连接/断开流程
- [ ] 网络闪断后自动恢复
- [ ] 服务端重启后客户端重连
- [ ] 重复消息幂等处理
- [ ] 大 Context 传输
- [ ] 高并发连接压力测试
- [ ] 认证失败处理

---

*本文档由开发团队讨论生成，如有疑问请联系架构组。*
