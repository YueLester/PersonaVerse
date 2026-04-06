# Agent Service - 架构说明

基于多层洋葱架构的 AI 服务。

## 架构分层

```
┌─────────────────────────────────────┐
│  api/          - 接口层              │
│  职责: 对外暴露 HTTP 接口             │
├─────────────────────────────────────┤
│  services/     - 领域服务层          │
│  职责: 实现业务逻辑（查省份等）        │
├─────────────────────────────────────┤
│  core/         - 能力基础层          │
│  职责: LLM 调用、Prompt 管理          │
├─────────────────────────────────────┤
│  adapters/     - 算力接入层          │
│  职责: 封装 Ollama 等模型 API         │
└─────────────────────────────────────┘
```

## 调用链

```
外部请求
    ↓
api/routes.py (接口层)
    ↓
services/geo_service.py (领域服务层)
    ↓
core/llm.py + prompts.py (能力基础层)
    ↓
adapters/ollama_adapter.py (算力接入层)
    ↓
Ollama 本地模型
```

## 各层详情

| 目录 | 层 | 职责 | 文件 |
|------|-----|------|------|
| `adapters/` | 算力接入层 | 统一接入AI模型 | `ollama_adapter.py` |
| `core/` | 能力基础层 | Prompt、LLM封装 | `llm.py`, `prompts.py` |
| `services/` | 领域服务层 | 业务逻辑实现 | `geo_service.py` |
| `api/` | 接口层 | HTTP接口定义 | `routes.py` |

## 快速开始

```bash
# 启动服务
cd src
python main.py

# 测试查省份
curl -X POST http://localhost:8001/v1/geo/province \
  -d '{"city": "杭州"}'
```
