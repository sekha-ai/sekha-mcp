"""Health check tests for Sekha MCP Server"""

import pytest
from unittest.mock import AsyncMock, patch
from sekha_mcp.health import check_controller_health, HealthStatus


@pytest.mark.asyncio
async def test_controller_health_check_success():
    """Test successful health check"""
    with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = AsyncMock(return_value={"status": "healthy"})
        mock_get.return_value = mock_response
        
        health = await check_controller_health()
        
        assert health.status == "healthy"
        assert health.controller_reachable is True
        assert health.error is None


@pytest.mark.asyncio
async def test_controller_health_check_unreachable():
    """Test health check when controller is unreachable"""
    with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = Exception("Connection refused")
        
        health = await check_controller_health()
        
        assert health.status == "unhealthy"
        assert health.controller_reachable is False
        assert "Connection refused" in health.error


def test_health_status_model():
    """Test HealthStatus model"""
    health = HealthStatus(
        status="healthy",
        controller_reachable=True,
        controller_url="http://localhost:8080"
    )
    
    assert health.status == "healthy"
    assert health.controller_reachable is True
    assert health.controller_url == "http://localhost:8080"