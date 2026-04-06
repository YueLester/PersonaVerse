# Gateway 模块 - 外部 Agent 接入网关

## 目录结构

```
gateway/
├── __init__.py           # 模块导出
├── server.py             # WebSocket 服务端（入口）
├── connection.py         # 连接池管理
├── handler.py            # 消息处理器
├── auth.py               # JWT 身份验证
├── queue.py              # 离线消息队列
└── README.md             # 本文档
```

## 职责划分

| 文件 | 职责 | 对应架构文档 |
|------|------|--------------|
| `server.py` | WebSocket 握手、认证、连接生命周期 | 2.1 架构概述 |
| `connection.py` | 连接池、心跳检测、负载均衡 | 2.5 服务端职责 |
| `handler.py` | 消息分发、决策请求/响应处理 | 2.3 协议设计 |
| `auth.py` | JWT 验证、Token 管理 | 3.4 安全性 |
| `queue.py` | 离线消息缓存、重连推送 | 2.5 消息队列 |

## 快速开始

```python
# main.py 初始化
from fastapi import FastAPI
from config import settings
from gateway import GatewayServer, ConnectionPool, MessageHandler
from gateway.auth import AuthValidator

app = FastAPI()

# 初始化组件
connection_pool = ConnectionPool(
    max_connections_per_agent=settings.REMOTE_AGENT_MAX_CONNECTIONS_PER_AGENT,
    heartbeat_timeout=settings.REMOTE_AGENT_HEARTBEAT_TIMEOUT,
)

auth_validator = AuthValidator(
    secret_key=settings.REMOTE_AGENT_JWT_SECRET,
    token_ttl=settings.REMOTE_AGENT_JWT_TTL,
)

message_handler = MessageHandler(
    connection_pool=connection_pool,
    scenario_runner=scenario_runner,  # 从 scenarios 导入
    personality_engine=personality_engine,  # 从 personality 导入
)

gateway_server = GatewayServer(
    connection_pool=connection_pool,
    message_handler=message_handler,
    auth_validator=auth_validator,
)

# 注册路由
gateway_server.register_routes(app)
```

## 与现有模块的交互

```
gateway/server.py ──注册──→ FastAPI (main.py)
     │
     ├── 连接管理 ──→ gateway/connection.py
     ├── 身份验证 ──→ gateway/auth.py
     └── 消息处理 ──→ gateway/handler.py
              │
              ├── 决策请求 ──→ scenarios/ScenarioRunner
              └── 状态更新 ──→ world/WorldEngine
```

## 配置项

详见 `apps/core/src/config.py` 中 `REMOTE_AGENT_*` 相关配置。

## TODO

- [ ] 实现 server.py 连接生命周期管理
- [ ] 实现 connection.py 连接池核心逻辑
- [ ] 实现 handler.py 消息分发
- [ ] 实现 auth.py JWT 验证
- [ ] 实现 queue.py Redis 队列
- [ ] 编写单元测试
- [ ] 编写集成测试
