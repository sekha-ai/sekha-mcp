"""Health check utilities for Sekha MCP Server"""

import httpx
from pydantic import BaseModel

from sekha_mcp.config import settings


class HealthStatus(BaseModel):
    """Health status response"""

    status: str
    controller_reachable: bool
    controller_url: str
    error: str | None = None


async def check_controller_health() -> HealthStatus:
    """Check if Sekha Controller (Rust core) is reachable"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.controller_url}/health",
                headers={"Authorization": f"Bearer {settings.controller_api_key}"},
            )
        return HealthStatus(
            status="healthy" if response.status_code == 200 else "degraded",
            controller_reachable=response.status_code == 200,
            controller_url=settings.controller_url,
            error=None,
        )
    except Exception as e:
        return HealthStatus(
            status="unhealthy",
            controller_reachable=False,
            controller_url=settings.controller_url,
            error=str(e),
        )
