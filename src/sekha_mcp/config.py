"""Configuration for Sekha MCP Server

v2.0 Updates:
- Compatible with Sekha v2.0 provider registry architecture
- Supports multi-provider LLM routing via controller
- No MCP-side changes needed (controller handles provider logic)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """MCP Server configuration

    v2.0 Compatibility:
    - Works with both v1.x and v2.0 controllers
    - Controller handles provider routing transparently
    - MCP server simply forwards requests to controller API
    """

    # Sekha Controller (Rust core)
    controller_url: str = "http://localhost:8080"
    controller_api_key: str = "test_key_12345678901234567890123456789012"

    # Server settings
    server_name: str = "sekha-memory"
    server_version: str = "2.0.0"  # Updated for v2.0 compatibility

    # Timeouts
    request_timeout: int = 30

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, frozen=False)


settings = Settings()
