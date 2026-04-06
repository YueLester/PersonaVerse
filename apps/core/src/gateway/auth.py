"""
身份验证
处理外部 Agent 连接的认证
"""

from fastapi import WebSocket, HTTPException
from typing import Optional
import jwt


class AuthValidator:
    """
    JWT Token 验证器
    
    验证流程：
    1. 从 Header 提取 X-Agent-Token
    2. 验证 JWT 签名和有效期
    3. 验证 agent_id 与白名单
    """
    
    def __init__(self, secret_key: str, token_ttl: int = 300):
        self.secret_key = secret_key
        self.token_ttl = token_ttl
        
    async def validate(self, websocket: WebSocket) -> Optional[str]:
        """
        验证 WebSocket 连接
        
        Returns:
            agent_id: 验证成功返回 agent_id
        Raises:
            HTTPException: 验证失败
        """
        # TODO: 1. 提取 token from header
        # TODO: 2. JWT 解码和验证
        # TODO: 3. 检查 agent_id 是否存在
        pass
