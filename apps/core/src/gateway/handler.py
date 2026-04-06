"""
消息处理器
处理各类消息：注册、心跳、决策请求/响应
"""

from typing import Dict, Callable, Awaitable
import logging

logger = logging.getLogger(__name__)


class MessageHandler:
    """
    Gateway 消息处理器
    
    职责：
    1. 解析消息类型并分发到对应处理器
    2. 处理注册、心跳、决策响应
    3. 协调与 Core 世界引擎的交互
    """
    
    def __init__(
        self,
        connection_pool: "ConnectionPool",
        scenario_runner: "ScenarioRunner",  # 来自 core.scenarios
        personality_engine: "PersonalityEngine",  # 来自 core.personality
    ):
        self.connection_pool = connection_pool
        self.scenario_runner = scenario_runner
        self.personality_engine = personality_engine
        
        # 处理器注册表
        self._handlers: Dict[str, Callable[[str, dict], Awaitable[None]]] = {
            "register": self._handle_register,
            "ping": self._handle_ping,
            "pong": self._handle_pong,
            "decision_response": self._handle_decision_response,
            "resume": self._handle_resume,
            "progress": self._handle_progress,
        }
        
        # 等待中的请求（用于异步响应匹配）
        self._pending_requests: Dict[str, "PendingRequest"] = {}
        
    async def handle(self, agent_id: str, message: dict):
        """入口方法：分发消息到对应处理器"""
        msg_type = message.get("type")
        handler = self._handlers.get(msg_type)
        if handler:
            await handler(agent_id, message)
        else:
            logger.warning(f"Unknown message type: {msg_type}")
    
    # ----- 具体处理器 -----
    
    async def _handle_register(self, agent_id: str, message: dict):
        """处理 Agent 注册"""
        pass
    
    async def _handle_ping(self, agent_id: str, message: dict):
        """处理心跳 ping"""
        pass
    
    async def _handle_pong(self, agent_id: str, message: dict):
        """处理心跳 pong"""
        pass
    
    async def _handle_decision_response(self, agent_id: str, message: dict):
        """处理决策响应（来自外部 Agent）"""
        # TODO: 1. 幂等性检查
        # TODO: 2. 匹配 pending_request
        # TODO: 3. 通知 ScenarioRunner
        pass
    
    async def _handle_resume(self, agent_id: str, message: dict):
        """处理断线恢复请求"""
        pass
    
    async def _handle_progress(self, agent_id: str, message: dict):
        """处理进度通知（用于长耗时决策）"""
        pass
    
    # ----- 对外接口（供 Core 调用） -----
    
    async def send_decision_request(
        self,
        agent_id: str,
        scenario_id: str,
        context: dict,
        timeout: float = 30.0,
    ) -> "DecisionResult":
        """
        发送决策请求给外部 Agent
        
        由 ScenarioRunner 调用，等待 Agent 响应
        """
        # TODO: 1. 查找可用连接
        # TODO: 2. 构建 DecisionRequest 消息
        # TODO: 3. 发送并注册到 pending_requests
        # TODO: 4. 等待响应或超时
        pass
