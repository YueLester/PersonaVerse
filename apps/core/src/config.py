"""Core 模块配置"""

import os
from dataclasses import dataclass


try:
    from pydantic_settings import BaseSettings
    
    class Settings(BaseSettings):
        """应用配置"""
        APP_NAME: str = "PersonaVerse Core"
        DEBUG: bool = False
        WORLD_TICK_INTERVAL: float = 5.0
        WORLD_AUTO_START: bool = True
        DATABASE_URL: str = "postgresql+asyncpg://localhost/personiverse"
        REDIS_URL: str = "redis://localhost:6379"
        
        # AI 模型配置
        OPENAI_API_KEY: str = ""
        ANTHROPIC_API_KEY: str = ""
        
        # Agent 服务配置（优先使用 Agent 服务而非直接调用模型）
        AGENT_SERVICE_URL: str = "http://localhost:8001"
        AGENT_SERVICE_API_KEY: str = ""
        AGENT_SERVICE_ENABLED: bool = False  # 是否启用 Agent 服务
        
        class Config:
            env_file = ".env"
    
    settings = Settings()
    
except ImportError:
    # Fallback: 使用 dataclass + os.environ
    @dataclass
    class Settings:
        APP_NAME: str = "PersonaVerse Core"
        DEBUG: bool = os.environ.get("DEBUG", "false").lower() == "true"
        WORLD_TICK_INTERVAL: float = float(os.environ.get("WORLD_TICK_INTERVAL", "5.0"))
        WORLD_AUTO_START: bool = True
        DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql+asyncpg://localhost/personiverse")
        REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost:6379")
        
        # AI 模型配置
        OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
        ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
        
        # Agent 服务配置
        AGENT_SERVICE_URL: str = os.environ.get("AGENT_SERVICE_URL", "http://localhost:8001")
        AGENT_SERVICE_API_KEY: str = os.environ.get("AGENT_SERVICE_API_KEY", "")
        AGENT_SERVICE_ENABLED: bool = os.environ.get("AGENT_SERVICE_ENABLED", "false").lower() == "true"
    
    settings = Settings()
