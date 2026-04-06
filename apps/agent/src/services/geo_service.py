"""
地理信息服务 - 领域服务层
提供城市、省份等地理相关功能
"""

from typing import Dict
from pydantic import BaseModel

from core.llm import generate, parse_json_response
from core.prompts import build_province_prompt


class ProvinceResult(BaseModel):
    """省份查询结果"""
    city: str
    province: str
    reasoning: str
    confidence: float
    latency_ms: float


async def get_province_by_city(city: str, model: str = None) -> ProvinceResult:
    """
    根据城市查询所属省份
    
    Args:
        city: 城市名称，如"杭州"
        model: 可选，指定模型
    
    Returns:
        ProvinceResult 包含省份、推理、置信度
    """
    # 构建 Prompt
    prompt = build_province_prompt(city)
    messages = [{"role": "user", "content": prompt}]
    
    # 调用 LLM
    result = await generate(
        messages=messages,
        model=model,
        temperature=0.3,
        expect_json=True
    )
    
    # 解析结果
    data = parse_json_response(result["content"])
    
    if "error" in data:
        return ProvinceResult(
            city=city,
            province="解析失败",
            reasoning=data.get("raw", ""),
            confidence=0.0,
            latency_ms=result["latency_ms"]
        )
    
    return ProvinceResult(
        city=city,
        province=data.get("province", "未知"),
        reasoning=data.get("reasoning", ""),
        confidence=data.get("confidence", 0.5),
        latency_ms=result["latency_ms"]
    )
