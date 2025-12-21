from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Rust controller
    controller_base_url: str = "http://localhost:8080"
    mcp_api_key: str = "test_key_12345678901234567890123456789012"

    class Config:
        env_file = ".env"
        env_prefix = "SEKHA_MCP_"
        env_file_encoding = "utf-8"


settings = Settings()