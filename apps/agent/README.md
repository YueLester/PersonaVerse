# Agent Service

AI 接入服务，支持 Ollama 本地大模型。

## 快速开始

```bash
# 1. 安装依赖
pip install fastapi uvicorn httpx pydantic

# 2. 确保 Ollama 运行并下载模型
ollama pull qwen:2.5
ollama serve

# 3. 启动服务
cd apps/agent/src
python main.py
# 或
uvicorn main:app --reload --port 8001
```

## 使用

```bash
# 对话生成
curl -X POST http://localhost:8001/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "你好"}]
  }'

# 健康检查
curl http://localhost:8001/v1/health
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama 地址 |
| `DEFAULT_MODEL` | `qwen:2.5` | 默认模型 |
