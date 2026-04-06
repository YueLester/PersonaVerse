# Agent Service

基于多层架构的 AI 服务。

## 架构

```
src/
├── adapters/     # 算力接入层 - 统一接入AI模型
├── core/         # 能力基础层 - LLM调用、Prompt管理
├── services/     # 领域服务层 - 业务逻辑实现
├── api/          # 接口层 - 对外暴露HTTP接口
└── main.py       # 入口
```

每层文件夹内有 README 说明该层职责。

## 快速启动

```bash
pip install fastapi uvicorn httpx pydantic
cd src
python main.py
```

## 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/v1/geo/province` | POST/GET | 根据城市查省份 |
| `/v1/chat` | POST | 通用对话 |
| `/v1/health` | GET | 健康检查 |

## 示例

```bash
curl -X POST http://localhost:8001/v1/geo/province \
  -d '{"city": "杭州"}'
```
