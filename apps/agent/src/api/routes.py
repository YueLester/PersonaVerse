"""
API 路由 - 接口层
定义所有对外暴露的 HTTP 接口
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from services.geo_service import get_province_by_city, ProvinceResult
from adapters.ollama_adapter import health_check as ollama_health
from core.llm import generate


router = APIRouter()


# ========== 数据模型 ==========

class ChatRequest(BaseModel):
    """通用对话请求"""
    messages: List[dict]
    model: Optional[str] = None
    temperature: float = 0.7


class ProvinceRequest(BaseModel):
    """查省份请求"""
    city: str
    model: Optional[str] = None


# ========== 路由定义 ==========

@router.post("/geo/province", response_model=ProvinceResult)
async def query_province(request: ProvinceRequest):
    """
    根据城市查询所属省份
    
    Example:
        POST /v1/geo/province
        {"city": "杭州"}
    """
    return await get_province_by_city(request.city, request.model)


@router.get("/geo/province")
async def query_province_get(city: str, model: Optional[str] = None):
    """查省份 GET 版本（方便测试）"""
    return await get_province_by_city(city, model)


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    通用对话接口
    
    Example:
        POST /v1/chat
        {"messages": [{"role": "user", "content": "你好"}]}
    """
    result = await generate(
        messages=request.messages,
        model=request.model,
        temperature=request.temperature
    )
    return {
        "content": result["content"],
        "model": result["model"],
        "latency_ms": result["latency_ms"]
    }


@router.get("/health")
async def health():
    """健康检查"""
    ollama = await ollama_health()
    return {
        "service": "agent",
        "status": "healthy" if ollama["status"] == "healthy" else "degraded",
        "ollama": ollama
    }
