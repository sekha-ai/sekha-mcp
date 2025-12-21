"""Configuration for Sekha MCP Server"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """MCP Server configuration"""
    
    # Sekha Controller (Rust core)
    controller_url: str = "http://localhost:8080"
    controller_api_key: str = "test_key_12345678901234567890123456789012"
    
    # Server settings
    server_name: str = "sekha-memory"
    server_version: str = "1.0.0"
    
    # Timeouts
    request_timeout: int = 30
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
