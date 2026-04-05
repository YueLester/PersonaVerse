# 技术栈选型

> 状态：已定稿 | 最后更新：2024

## 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 主开发语言 |
| FastAPI | 0.109+ | Web框架，自动API文档 |
| Socket.IO | 5.11+ | WebSocket实时通信 |
| SQLAlchemy | 2.0+ | ORM，支持async |
| PostgreSQL | 15+ | 主数据库 |
| Redis | 7+ | 缓存、状态、Pub/Sub |
| Celery | 5.3+ | 异步任务队列 |
| gRPC | 1.60+ | 服务间通信 |

## 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| React | 18+ | UI框架 |
| TypeScript | 5.3+ | 类型安全 |
| Tailwind CSS | 3.4+ | 样式 |
| D3.js | 7+ | 数据可视化 |
| Socket.IO Client | 4.7+ | 实时通信 |

## 基础设施

- Docker + Docker Compose：容器化
- Nginx：反向代理、负载均衡
- Prometheus + Grafana：监控（可选）
