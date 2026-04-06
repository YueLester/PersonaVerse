"""
LLM 调用封装 - 能力基础层
封装底层模型调用，提供统一接口
"""

import json
import time
from typing import List, Dict, Optional
from fastapi import HTTPException

from adapters.ollama_adapter import chat_completion


async def generate(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    expect_json: bool = False
) -> Dict:
    """
    调用 LLM 生成内容
    
    Args:
        messages: 消息列表
        model: 模型名称
        temperature: 温度
        expect_json: 是否期望 JSON 输出
    
    Returns:
        {"content": str, "model": str, "latency_ms": float}
    """
    start = time.time()
    
    # 如需 JSON，添加 system 提示
    if expect_json:
        if not messages or messages[0]["role"] != "system":
            messages.insert(0, {"role": "system", "content": "请用 JSON 格式返回结果。"})
        else:
            messages[0]["content"] += "\n请用 JSON 格式返回，不要包含其他文字。"
    
    try:
        result = await chat_completion(messages, model, temperature)
        result["latency_ms"] = (time.time() - start) * 1000
        return result
    except Exception as e:
        raise HTTPException(503, f"LLM service error: {str(e)}")


def parse_json_response(content: str) -> Dict:
    """
    解析 LLM 返回的 JSON
    处理 markdown 代码块等情况
    """
    # 清理 markdown 标记
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "JSON parse failed", "raw": content[:200]}
