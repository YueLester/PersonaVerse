"""
WebSocket 服务端
负责监听外部 Agent 连接、身份验证、连接管理
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class GatewayServer:
    """
    外部 Agent 接入网关 - WebSocket 服务端
    
    职责：
    1. 监听 WebSocket 连接
    2. 身份验证（JWT Token）
    3. 将连接交给 ConnectionPool 管理
    4. 分发消息到 MessageHandler
    """
    
    def __init__(
        self,
        connection_pool: "ConnectionPool",
        message_handler: "MessageHandler",
        auth_validator: Optional["AuthValidator"] = None,
    ):
        self.connection_pool = connection_pool
        self.message_handler = message_handler
        self.auth_validator = auth_validator
        
    def register_routes(self, app: FastAPI, prefix: str = "/v1"):
        """注册 WebSocket 路由到 FastAPI 应用"""
        
        @app.websocket(f"{prefix}/agents/connect")
        async def agent_websocket(websocket: WebSocket):
            await self._handle_connection(websocket)
    
    async def _handle_connection(self, websocket: WebSocket):
        """处理单个 WebSocket 连接生命周期"""
        # TODO: 1. 握手和认证
        # TODO: 2. 创建 AgentConnection
        # TODO: 3. 加入 ConnectionPool
        # TODO: 4. 启动消息循环
        # TODO: 5. 断开时清理
        pass
