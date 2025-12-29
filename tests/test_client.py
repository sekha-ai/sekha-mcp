"""Tests for Sekha HTTP client"""

import pytest
from unittest.mock import AsyncMock, patch
import httpx

from sekha_llm_bridge.client import SekhaClient


@pytest.fixture
def client():
    """Create test client"""
    return SekhaClient()


@pytest.mark.asyncio
async def test_client_store_conversation(client):
    """Test store conversation method"""
    with patch('httpx.AsyncClient.post', new=AsyncMock()) as mock_post:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {"conversation_id": "test"}}
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response
        
        result = await client.store_conversation({"label": "Test"})
        
        assert result["success"] is True
        assert mock_post.called


@pytest.mark.asyncio
async def test_client_handles_errors(client):
    """Test client error handling"""
    with patch('httpx.AsyncClient.post', new=AsyncMock()) as mock_post:
        mock_post.side_effect = httpx.HTTPError("Connection failed")
        
        with pytest.raises(httpx.HTTPError):
            await client.store_conversation({"label": "Test"})
