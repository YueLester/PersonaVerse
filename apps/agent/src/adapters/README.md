# adapters/ - 算力接入层

## 职责
统一接入各类 AI 模型（Ollama、OpenAI、Claude 等），提供标准化接口。

## 功能
- 封装不同模型的 API 差异
- 健康检查与故障转移
- 模型参数转换

## 文件
- `ollama_adapter.py` - Ollama 本地模型适配
