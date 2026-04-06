"""
Agent Service - AI 接入服务
基于 Ollama 本地大模型
端口: 8001
"""

import os
import time
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import httpx

app = FastAPI(title="Agent Service", version="0.1.0")

# Ollama 配置
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "qwen:2.5")


# ========== 数据模型 ==========

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    """通用对话请求"""
    messages: List[Message]
    model: Optional[str] = None
    temperature: float = 0.7


class ProvinceRequest(BaseModel):
    """查省份请求"""
    city: str
    model: Optional[str] = None


class ProvinceResponse(BaseModel):
    """查省份响应"""
    city: str
    province: str
    reasoning: str
    confidence: float
    latency_ms: float


# ========== 核心函数 ==========

async def call_ollama(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    expect_json: bool = False
) -> Dict:
    """
    调用 Ollama 服务
    
    Args:
        messages: 消息列表
        model: 模型名称
        temperature: 温度
        expect_json: 是否期望 JSON 输出
    
    Returns:
        {"content": str, "model": str}
    """
    model = model or DEFAULT_MODEL
    
    # 如果期望 JSON，在 system prompt 中添加提示
    if expect_json and messages:
        # 检查是否已有 system message
        if messages[0]["role"] != "system":
            messages.insert(0, {"role": "system", "content": "请用 JSON 格式返回结果。"})
        else:
            messages[0]["content"] += "\n请用 JSON 格式返回结果，不要包含其他文字。"
    
    try:
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
    except httpx.ConnectError:
        raise HTTPException(503, f"Cannot connect to Ollama at {OLLAMA_URL}. Is it running?")
    except Exception as e:
        raise HTTPException(500, f"Ollama error: {str(e)}")


# ========== API 端点 ==========

@app.post("/v1/chat")
async def chat(request: ChatRequest):
    """
    通用对话接口
    
    Example:
        curl -X POST http://localhost:8001/v1/chat \
          -H "Content-Type: application/json" \
          -d '{"messages": [{"role": "user", "content": "你好"}]}'
    """
    start = time.time()
    
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    result = await call_ollama(messages, request.model, request.temperature)
    
    return {
        "content": result["content"],
        "model": result["model"],
        "latency_ms": (time.time() - start) * 1000
    }


@app.post("/v1/geo/province", response_model=ProvinceResponse)
async def get_province(request: ProvinceRequest):
    """
    根据城市查询所属省份
    
    使用本地大模型推理，返回结构化结果
    
    Example:
        curl -X POST http://localhost:8001/v1/geo/province \
          -H "Content-Type: application/json" \
          -d '{"city": "杭州"}'
    
    Response:
        {
            "city": "杭州",
            "province": "浙江省",
            "reasoning": "杭州是浙江省的省会城市",
            "confidence": 0.95,
            "latency_ms": 1250.5
        }
    """
    start = time.time()
    
    # 构建 prompt
    system_prompt = """你是一个地理知识助手。根据用户输入的城市名称，返回该城市所属的省份。

请用以下 JSON 格式返回，不要包含其他文字：
{
    "province": "省份名称",
    "reasoning": "推理说明",
    "confidence": 0.95
}"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"城市：{request.city}"}
    ]
    
    # 调用 Ollama
    result = await call_ollama(messages, request.model, temperature=0.3, expect_json=True)
    content = result["content"]
    
    # 解析 JSON（处理可能的 markdown 代码块）
    try:
        # 清理可能的 markdown 标记
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        data = json.loads(content)
        
        return ProvinceResponse(
            city=request.city,
            province=data.get("province", "未知"),
            reasoning=data.get("reasoning", ""),
            confidence=data.get("confidence", 0.5),
            latency_ms=(time.time() - start) * 1000
        )
        
    except json.JSONDecodeError:
        # JSON 解析失败，返回原始内容
        return ProvinceResponse(
            city=request.city,
            province="解析失败",
            reasoning=f"模型返回: {content[:200]}",
            confidence=0.0,
            latency_ms=(time.time() - start) * 1000
        )


@app.get("/v1/geo/province")
async def get_province_get(city: str, model: Optional[str] = None):
    """
    查省份 - GET 版本（方便浏览器测试）
    
    Example:
        curl "http://localhost:8001/v1/geo/province?city=杭州"
    """
    return await get_province(ProvinceRequest(city=city, model=model))


@app.get("/v1/health")
async def health():
    """健康检查"""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                model_names = [m.get("name", "unknown") for m in models[:3]]
                return {
                    "status": "healthy",
                    "ollama": "connected",
                    "available_models": model_names
                }
    except Exception as e:
        pass
    
    return {
        "status": "degraded",
        "ollama": "disconnected",
        "error": f"Cannot connect to Ollama at {OLLAMA_URL}"
    }


# ========== 启动 ==========

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print("Agent Service Starting...")
    print("=" * 50)
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"Default Model: {DEFAULT_MODEL}")
    print("\nAvailable endpoints:")
    print(f"  POST /v1/chat              - 通用对话")
    print(f"  POST /v1/geo/province      - 查省份")
    print(f"  GET  /v1/geo/province      - 查省份(GET)")
    print(f"  GET  /v1/health            - 健康检查")
    print("\nTest:")
    print(f'  curl "http://localhost:8001/v1/geo/province?city=杭州"')
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
