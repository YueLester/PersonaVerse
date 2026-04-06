"""
Ollama 适配器 - 算力接入层
封装 Ollama API 调用
"""

import os
import httpx
from typing import List, Dict, Optional


OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "qwen:2.5")


async def chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7
) -> Dict:
    """
    调用 Ollama 聊天接口
    
    Args:
        messages: 消息列表 [{"role": "user", "content": "..."}]
        model: 模型名称，默认 qwen:2.5
        temperature: 温度
    
    Returns:
        {"content": str, "model": str}
    """
    model = model or DEFAULT_MODEL
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{OLLAMA_URL}/v1/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
        )
        resp.raise_for_status()
        result = resp.json()
        
        return {
            "content": result["choices"][0]["message"]["content"],
            "model": model
        }


async def health_check() -> Dict:
    """检查 Ollama 服务健康状态"""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                return {
                    "status": "healthy",
                    "models": [m.get("name") for m in models[:5]]
                }
    except:
        pass
    
    return {"status": "unhealthy", "models": []}
