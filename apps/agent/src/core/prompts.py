"""
Prompt 模板 - 能力基础层
集中管理所有 Prompt 模板
"""

# 地理查询 Prompt
GEO_PROVINCE_PROMPT = """你是一个地理知识助手。根据用户输入的城市名称，返回该城市所属的省份。

请用以下 JSON 格式返回，不要包含其他文字：
{
    "province": "省份名称",
    "reasoning": "推理说明",
    "confidence": 0.95
}

城市：{city}
"""


def build_province_prompt(city: str) -> str:
    """构建查省份 Prompt"""
    return GEO_PROVINCE_PROMPT.format(city=city)
