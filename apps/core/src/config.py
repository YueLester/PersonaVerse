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
        OPENAI_API_KEY: str = ""
        ANTHROPIC_API_KEY: str = ""
        
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
        OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
        ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
    
    settings = Settings()
