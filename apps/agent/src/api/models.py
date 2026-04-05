"""API 数据模型"""

from typing import Any, AsyncIterator, Optional
from pydantic import BaseModel, Field
import uuid


class Message(BaseModel):
    """消息"""
    role: str = Field(..., description="system/user/assistant")
    content: str
    name: Optional[str] = None


class TokenUsage(BaseModel):
    """Token 使用统计"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class GenerateConfig(BaseModel):
    """生成配置"""
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1024
    stream: bool = False
    timeout: float = 30.0
    priority: str = "normal"  # low/normal/high/critical
    cost_preference: str = "balanced"  # cheap/balanced/quality


class GenerateRequest(BaseModel):
    """生成请求"""
    tenant_id: str
    agent_type: str
    messages: list[Message]
    config: GenerateConfig = Field(default_factory=GenerateConfig)
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    parent_request_id: Optional[str] = None


class GenerationResult(BaseModel):
    """生成结果"""
    content: str
    model: str
    usage: TokenUsage
    latency_ms: float
    cost_usd: float
    request_id: str
    finish_reason: str = "stop"


class StreamChunk(BaseModel):
    """流式块"""
    content: str
    is_finished: bool = False
    usage: Optional[TokenUsage] = None


class HealthStatus(BaseModel):
    """健康状态"""
    status: str  # healthy/degraded/unhealthy
    latency_ms: float
    last_checked: str
    error_count: int = 0
