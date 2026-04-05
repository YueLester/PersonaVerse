"""Agent 连接器 - 对接外部 AI"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

from .models import Agent


@dataclass
class DecisionRequest:
    """决策请求"""
    agent_id: str
    scenario_id: str
    context: dict[str, Any]       # 情境上下文
    choices: list[dict]           # 可选项
    timeout: float = 30.0         # 超时时间（秒）


@dataclass
class Decision:
    """决策结果"""
    agent_id: str
    choice_id: str                # 选择的 ID
    reasoning: Optional[str] = None  # 思考过程（可选）
    response_time: float = 0.0    # 响应时间


class AgentConnector(ABC):
    """Agent 连接器基类"""
    
    @abstractmethod
    async def get_decision(self, agent: Agent, request: DecisionRequest) -> Decision:
        """获取 Agent 的决策"""
        pass
    
    @abstractmethod
    async def send_perception(self, agent: Agent, perception: dict) -> bool:
        """向 Agent 发送感知信息"""
        pass


class MockConnector(AgentConnector):
    """模拟连接器（用于测试）"""
    
    def __init__(self, choice_callback: Optional[callable] = None):
        self.choice_callback = choice_callback
    
    async def get_decision(self, agent: Agent, request: DecisionRequest) -> Decision:
        """模拟决策 - 随机或回调"""
        await asyncio.sleep(0.5)  # 模拟网络延迟
        
        if self.choice_callback:
            choice_id = self.choice_callback(request)
        else:
            # 随机选择
            choice_id = request.choices[0]["id"] if request.choices else "default"
        
        return Decision(
            agent_id=agent.id,
            choice_id=choice_id,
            reasoning="Mock decision",
            response_time=0.5
        )
    
    async def send_perception(self, agent: Agent, perception: dict) -> bool:
        """模拟发送感知"""
        print(f"[Mock] To {agent.name}: {perception.get('summary', 'update')}")
        return True


class OpenAIConnector(AgentConnector):
    """OpenAI GPT 连接器（示例）"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        if not HAS_HTTPX:
            raise ImportError("httpx is required for OpenAI connector. Install: pip install httpx")
        self.api_key = api_key
        self.model = model
        self.client = httpx.AsyncClient(
            base_url="https://api.openai.com/v1",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0
        )
    
    async def get_decision(self, agent: Agent, request: DecisionRequest) -> Decision:
        """调用 GPT 做决策"""
        start_time = asyncio.get_event_loop().time()
        
        # 构建 prompt
        prompt = self._build_prompt(request)
        
        try:
            response = await self.client.post(
                "/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "你是一个在虚拟世界中做决策的AI。请根据情境选择最合适的选项，只返回选项ID。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 100
                }
            )
            
            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()
            
            # 解析选择（期望直接返回 choice_id）
            choice_id = self._parse_choice(content, request.choices)
            
            response_time = asyncio.get_event_loop().time() - start_time
            
            return Decision(
                agent_id=agent.id,
                choice_id=choice_id,
                reasoning=content if len(content) > 10 else None,
                response_time=response_time
            )
            
        except Exception as e:
            # 失败时默认选第一个
            return Decision(
                agent_id=agent.id,
                choice_id=request.choices[0]["id"] if request.choices else "default",
                reasoning=f"Error: {str(e)}",
                response_time=asyncio.get_event_loop().time() - start_time
            )
    
    def _build_prompt(self, request: DecisionRequest) -> str:
        """构建决策 prompt"""
        lines = [
            "# 情境",
            request.context.get("description", "做出选择："),
            "",
            "# 可选项",
        ]
        for choice in request.choices:
            lines.append(f"- {choice['id']}: {choice.get('description', '')}")
        
        lines.extend([
            "",
            "请直接回复你要选择的选项 ID（只回复 ID，不要其他内容）："
        ])
        
        return "\n".join(lines)
    
    def _parse_choice(self, content: str, choices: list[dict]) -> str:
        """解析选择"""
        valid_ids = {c["id"] for c in choices}
        
        # 直接匹配
        if content in valid_ids:
            return content
        
        # 在文本中查找
        for choice_id in valid_ids:
            if choice_id in content:
                return choice_id
        
        # 默认第一个
        return choices[0]["id"] if choices else "default"
    
    async def send_perception(self, agent: Agent, perception: dict) -> bool:
        """发送感知更新（可选实现）"""
        # MVP 版本：打印日志即可
        print(f"[OpenAI] To {agent.name}: {perception.get('summary', 'update')}")
        return True


class ConnectorFactory:
    """连接器工厂"""
    
    @staticmethod
    def create(connector_type: str, config: dict) -> AgentConnector:
        """创建连接器"""
        if connector_type == "mock":
            return MockConnector()
        elif connector_type == "openai":
            return OpenAIConnector(
                api_key=config.get("api_key", ""),
                model=config.get("model", "gpt-4o-mini")
            )
        else:
            raise ValueError(f"Unknown connector type: {connector_type}")
