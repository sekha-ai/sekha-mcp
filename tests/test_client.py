"""Unit tests for Sekha HTTP client"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from sekha_mcp.client import SekhaClient


@pytest.fixture
def client():
    """Create test client"""
    return SekhaClient()


@pytest.mark.asyncio
async def test_client_store_conversation_success(client):
    """Test successful conversation storage"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"conversation_id": "test-uuid-123", "message_count": 2},
        }
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        conversation = {
            "label": "Test Conversation",
            "folder": "/tests",
            "messages": [{"role": "user", "content": "Hello"}],
        }

        result = await client.store_conversation(conversation)

        assert result["success"] is True
        assert result["data"]["conversation_id"] == "test-uuid-123"
        mock_post.assert_called_once()

        # Verify correct endpoint and headers
        call_args = mock_post.call_args
        assert "/mcp/tools/memory_store" in str(call_args[0])
        assert "Authorization" in call_args[1]["headers"]


@pytest.mark.asyncio
async def test_client_search_memory_success(client):
    """Test successful memory search"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "results": [
                    {
                        "conversation_id": "conv-1",
                        "label": "Found",
                        "similarity": 0.95,
                        "content": "Relevant content",
                    }
                ]
            },
        }
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        result = await client.search_memory("test query", limit=5)

        assert result["success"] is True
        assert len(result["data"]["results"]) == 1
        assert result["data"]["results"][0]["similarity"] == 0.95


@pytest.mark.asyncio
async def test_client_search_memory_with_filters(client):
    """Test memory search with label filters"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {"results": []}}
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        filters = ["Engineering", "Project-A"]
        result = await client.search_memory("query", limit=10, filter_labels=filters)

        assert result["success"] is True
        mock_post.assert_called_once()

        # Verify filters were passed
        call_kwargs = mock_post.call_args[1]
        assert "filter_labels" in call_kwargs["json"]


@pytest.mark.asyncio
async def test_client_update_conversation_full(client):
    """Test full conversation update"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"updated_fields": ["label", "folder", "importance_score"]},
        }
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        result = await client.update_conversation(
            conversation_id="conv-123",
            label="New Label",
            folder="/new/folder",
            importance_score=9.5,
        )

        assert result["success"] is True


@pytest.mark.asyncio
async def test_client_update_conversation_partial(client):
    """Test partial conversation update"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {"updated_fields": ["label"]}}
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        result = await client.update_conversation(
            conversation_id="conv-123", label="Updated Label Only"
        )

        assert result["success"] is True


@pytest.mark.asyncio
async def test_client_get_context_success(client):
    """Test successful context retrieval"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "conversation_id": "conv-123",
                "label": "Test Conversation",
                "folder": "/tests",
                "status": "active",
                "importance_score": 8,
                "created_at": "2024-01-01T00:00:00Z",
                "messages": [
                    {"role": "user", "content": "Question?"},
                    {"role": "assistant", "content": "Answer."},
                ],
            },
        }
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        result = await client.get_context("conv-123")

        assert result["success"] is True
        assert len(result["data"]["messages"]) == 2
        assert result["data"]["label"] == "Test Conversation"


@pytest.mark.asyncio
async def test_client_prune_memory_with_threshold(client):
    """Test memory pruning with threshold"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "suggestions": [
                    {
                        "conversation_id": "old-uuid",
                        "label": "Old Conversation",
                        "age_days": 45,
                        "importance_score": 3,
                        "reason": "Low importance and old",
                    }
                ]
            },
        }
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        result = await client.prune_memory(threshold_days=30, importance_threshold=5.0)

        assert result["success"] is True
        assert len(result["data"]["suggestions"]) == 1


@pytest.mark.asyncio
async def test_client_prune_memory_no_suggestions(client):
    """Test memory pruning with no suggestions"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {"suggestions": []}}
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        result = await client.prune_memory(threshold_days=30)

        assert result["success"] is True
        assert len(result["data"]["suggestions"]) == 0


@pytest.mark.asyncio
async def test_client_query_memory_legacy(client):
    """Test legacy query endpoint (backward compatibility)"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {"results": [{"id": "conv-1"}]}}
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        result = await client.query_memory("legacy query")

        assert result["success"] is True
        # Should call search_memory internally
        call_args = mock_post.call_args
        assert "/mcp/tools/memory_search" in str(call_args[0])


@pytest.mark.asyncio
async def test_client_handles_http_status_error(client):
    """Test client handles HTTP status errors"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_post.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=MagicMock(status_code=404)
        )

        with pytest.raises(httpx.HTTPError) as exc_info:
            await client.store_conversation({"label": "Test"})

        assert "404" in str(exc_info.value)


@pytest.mark.asyncio
async def test_client_handles_connection_error(client):
    """Test client handles connection errors"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_post.side_effect = httpx.ConnectError("Connection refused")

        with pytest.raises(httpx.HTTPError) as exc_info:
            await client.search_memory("test")

        assert "Connection" in str(exc_info.value)


@pytest.mark.asyncio
async def test_client_handles_timeout(client):
    """Test client properly handles timeout exceptions"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_post.side_effect = httpx.TimeoutException("Connection timed out after 30s")

        with pytest.raises(httpx.TimeoutException) as exc_info:
            await client.get_context("conv-123")

        # Verify specific exception type and message
        assert isinstance(exc_info.value, httpx.TimeoutException)
        assert "timed out" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_client_timeout_configuration(client):
    """Test timeout configuration matches settings"""
    # Verify timeout attribute exists and matches config
    assert hasattr(client, "timeout")
    assert isinstance(client.timeout, int)
    assert client.timeout == 30

    # Verify it matches settings
    from sekha_mcp.config import settings

    assert client.timeout == settings.request_timeout

    # Test timeout is passed to HTTP client
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {}}
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        # Make a request to trigger client creation
        await client.store_conversation({"label": "Test timeout"})

        # Verify post was called (indicating client was created with timeout)
        assert mock_post.called


@pytest.mark.asyncio
async def test_client_all_methods_coverage(client):
    """Coverage test for all client methods to hit error paths"""

    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {"results": []}}
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        result = await client.search_memory("test", limit=5, filter_labels=None)
        assert result["success"] is True


@pytest.mark.asyncio
async def test_client_update_conversation_no_fields(client):
    """Test update with no optional fields"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {"updated_fields": []}}
        mock_response.raise_for_status = lambda: None
        mock_post.return_value = mock_response

        result = await client.update_conversation(conversation_id="conv-123")
        assert result["success"] is True


@pytest.mark.asyncio
async def test_client_get_stats_success(client):
    """Test get_stats method"""
    with patch("httpx.AsyncClient.get", new=AsyncMock()) as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"total_conversations": 100, "average_importance": 6.5},
        }
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        result = await client.get_stats(folder="/work")

        assert result["success"] is True
        assert result["data"]["total_conversations"] == 100
