"""
Gateway 模块 - 外部 Agent 接入网关

负责处理第三方 AI Agent（如 OpenClaw）通过 WebSocket 接入 PersonaVerse
"""

from .server import GatewayServer
from .connection import ConnectionPool, AgentConnection
from .handler import MessageHandler

__all__ = ["GatewayServer", "ConnectionPool", "AgentConnection", "MessageHandler"]
