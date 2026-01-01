"""Unit tests for MCP tools"""

import pytest
from unittest.mock import AsyncMock, patch

from sekha_mcp.tools.memory_store import memory_store_tool
from sekha_mcp.tools.memory_search import memory_search_tool
from sekha_mcp.tools.memory_update import memory_update_tool
from sekha_mcp.tools.memory_get_context import memory_get_context_tool
from sekha_mcp.tools.memory_prune import memory_prune_tool
from sekha_mcp.tools.memory_export import memory_export_tool
from sekha_mcp.tools.memory_stats import memory_stats_tool


# ============================================
# Memory Store Tests
# ============================================

@pytest.mark.asyncio
async def test_memory_store_success():
    """Test successful memory store"""
    with patch('sekha_mcp.client.sekha_client.store_conversation', new=AsyncMock()) as mock_store:
        mock_store.return_value = {
            "success": True,
            "data": {
                "conversation_id": "test-uuid-123",
                "message_count": 2
            }
        }
        
        arguments = {
            "label": "Test Conversation",
            "folder": "/tests",
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ],
            "importance_score": 8
        }
        
        result = await memory_store_tool(arguments)
        
        assert len(result) == 1
        assert "stored successfully" in result[0].text
        assert "test-uuid-123" in result[0].text
        assert mock_store.called


@pytest.mark.asyncio
async def test_memory_store_failure():
    """Test memory store failure handling"""
    with patch('sekha_mcp.client.sekha_client.store_conversation', new=AsyncMock()) as mock_store:
        mock_store.side_effect = Exception("Network error")
        
        arguments = {
            "label": "Test",
            "folder": "/tests",
            "messages": [{"role": "user", "content": "Test"}]
        }
        
        result = await memory_store_tool(arguments)
        
        assert len(result) == 1
        assert "Error" in result[0].text


# ============================================
# Memory Search Tests
# ============================================

@pytest.mark.asyncio
async def test_memory_search_with_results():
    """Test memory search with results"""
    with patch('sekha_mcp.client.sekha_client.search_memory', new=AsyncMock()) as mock_search:
        mock_search.return_value = {
            "success": True,
            "data": {
                "results": [
                    {
                        "label": "Found Conversation",
                        "folder": "/tests",
                        "content": "Test content here with relevant information",
                        "similarity": 0.95,
                        "conversation_id": "result-uuid-1"
                    },
                    {
                        "label": "Another Match",
                        "folder": "/work",
                        "content": "More relevant content",
                        "similarity": 0.87,
                        "conversation_id": "result-uuid-2"
                    }
                ]
            }
        }
        
        arguments = {"query": "test query", "limit": 10}
        result = await memory_search_tool(arguments)
        
        assert len(result) == 1
        assert "Found 2 relevant conversations" in result[0].text
        assert "Found Conversation" in result[0].text
        assert "0.95" in result[0].text


@pytest.mark.asyncio
async def test_memory_search_no_results():
    """Test memory search with no results"""
    with patch('sekha_mcp.client.sekha_client.search_memory', new=AsyncMock()) as mock_search:
        mock_search.return_value = {
            "success": True,
            "data": {"results": []}
        }
        
        arguments = {"query": "nonexistent", "limit": 10}
        result = await memory_search_tool(arguments)
        
        assert len(result) == 1
        assert "No matching conversations" in result[0].text


@pytest.mark.asyncio
async def test_memory_search_with_filters():
    """Test memory search with label filters"""
    with patch('sekha_mcp.client.sekha_client.search_memory', new=AsyncMock()) as mock_search:
        mock_search.return_value = {
            "success": True,
            "data": {"results": []}
        }
        
        arguments = {
            "query": "filtered query",
            "limit": 5,
            "filter_labels": ["Engineering", "Planning"]
        }
        result = await memory_search_tool(arguments)
        
        mock_search.assert_called_once_with(
            query="filtered query",
            limit=5,
            filter_labels=["Engineering", "Planning"]
        )


# ============================================
# Memory Update Tests
# ============================================

@pytest.mark.asyncio
async def test_memory_update_success():
    """Test successful memory update"""
    with patch('sekha_mcp.client.sekha_client.update_conversation', new=AsyncMock()) as mock_update:
        mock_update.return_value = {
            "success": True,
            "data": {
                "updated_fields": ["label", "importance_score"]
            }
        }
        
        arguments = {
            "conversation_id": "test-uuid",
            "label": "Updated Title",
            "importance_score": 9.0
        }
        
        result = await memory_update_tool(arguments)
        
        assert len(result) == 1
        assert "updated" in result[0].text.lower()
        assert "label" in result[0].text


@pytest.mark.asyncio
async def test_memory_update_partial():
    """Test partial memory update (only one field)"""
    with patch('sekha_mcp.client.sekha_client.update_conversation', new=AsyncMock()) as mock_update:
        mock_update.return_value = {
            "success": True,
            "data": {"updated_fields": ["folder"]}
        }
        
        arguments = {
            "conversation_id": "test-uuid",
            "folder": "/new/location"
        }
        
        result = await memory_update_tool(arguments)
        
        assert len(result) == 1
        mock_update.assert_called_once_with(
            conversation_id="test-uuid",
            label=None,
            folder="/new/location",
            importance_score=None
        )


# ============================================
# Memory Get Context Tests
# ============================================

@pytest.mark.asyncio
async def test_memory_get_context_success():
    """Test getting conversation context"""
    with patch('sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
        mock_get.return_value = {
            "success": True,
            "data": {
                "label": "Test Conversation",
                "folder": "/tests",
                "status": "active",
                "importance_score": 7,
                "created_at": "2024-01-01T00:00:00",
                "messages": [
                    {"role": "user", "content": "Question?"},
                    {"role": "assistant", "content": "Answer."}
                ]
            }
        }
        
        arguments = {"conversation_id": "test-uuid"}
        result = await memory_get_context_tool(arguments)
        
        assert len(result) == 1
        assert "Test Conversation" in result[0].text
        assert "USER" in result[0].text
        assert "ASSISTANT" in result[0].text


@pytest.mark.asyncio
async def test_memory_get_context_not_found():
    """Test getting context for non-existent conversation"""
    with patch('sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
        mock_get.return_value = {"success": False}
        
        arguments = {"conversation_id": "nonexistent"}
        result = await memory_get_context_tool(arguments)
        
        assert len(result) == 1
        assert "not found" in result[0].text


# ============================================
# Memory Prune Tests
# ============================================

@pytest.mark.asyncio
async def test_memory_prune_with_suggestions():
    """Test pruning with suggestions"""
    with patch('sekha_mcp.client.sekha_client.prune_memory', new=AsyncMock()) as mock_prune:
        mock_prune.return_value = {
            "success": True,
            "data": {
                "suggestions": [
                    {
                        "label": "Old Conversation",
                        "conversation_id": "old-uuid",
                        "age_days": 45,
                        "importance_score": 3,
                        "reason": "Low importance and old"
                    }
                ]
            }
        }
        
        arguments = {"threshold_days": 30, "importance_threshold": 5.0}
        result = await memory_prune_tool(arguments)
        
        assert len(result) == 1
        assert "Found 1 conversation" in result[0].text
        assert "Old Conversation" in result[0].text


@pytest.mark.asyncio
async def test_memory_prune_no_suggestions():
    """Test pruning with no suggestions"""
    with patch('sekha_mcp.client.sekha_client.prune_memory', new=AsyncMock()) as mock_prune:
        mock_prune.return_value = {
            "success": True,
            "data": {"suggestions": []}
        }
        
        arguments = {"threshold_days": 30}
        result = await memory_prune_tool(arguments)
        
        assert len(result) == 1
        assert "No conversations need pruning" in result[0].text


@pytest.mark.asyncio
async def test_memory_update_no_fields_provided():
    """Test update tool with no fields raises validation error"""
    with patch('sekha_mcp.client.sekha_client.update_conversation', new=AsyncMock()) as mock_update:
        arguments = {"conversation_id": "test-uuid"}  # No fields to update
        
        result = await memory_update_tool(arguments)
        
        assert len(result) == 1
        assert "Validation error" in result[0].text
        assert "at least one field" in result[0].text.lower()


@pytest.mark.asyncio
async def test_memory_store_validation_error_empty_messages():
    """Test store tool validation - empty messages"""
    arguments = {
        "label": "Test",
        "folder": "/tests",
        "messages": []  # Empty - should fail
    }
    
    result = await memory_store_tool(arguments)
    
    assert "❌" in result[0].text  # Just check for the error symbol
    assert "too_short" in result[0].text or "validation" in result[0].text.lower()


@pytest.mark.asyncio
async def test_memory_search_validation_error_empty_query():
    """Test search tool validation - empty query"""
    arguments = {"query": "   "}  # Just whitespace
    
    result = await memory_search_tool(arguments)
    
    assert len(result) == 1
    assert "Validation error" in result[0].text


@pytest.mark.asyncio
async def test_memory_get_context_validation_error_missing_fields():
    """Test context tool validation - API returns incomplete data"""
    with patch('sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
        mock_get.return_value = {
            "success": True,
            "data": {"label": "Test", "folder": "/"}  # Missing messages, status
        }
        
        arguments = {"conversation_id": "test-uuid"}
        result = await memory_get_context_tool(arguments)
        
        assert len(result) == 1
        assert "Validation error" in result[0].text
        assert "missing required fields" in result[0].text.lower()


@pytest.mark.asyncio
async def test_memory_prune_validation_error_negative_threshold():
    """Test prune tool validation - negative threshold"""
    arguments = {"threshold_days": -1}
    
    result = await memory_prune_tool(arguments)
    
    assert "❌ Error:" in result[0].text
    assert "greater than or equal to 1" in result[0].text


@pytest.mark.asyncio
async def test_memory_export_json_success():
    """Test export tool to JSON format"""
    with patch('sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
        mock_get.return_value = {
            "success": True,
            "data": {
                "conversation_id": "conv-123",
                "label": "Test Conversation",
                "folder": "/tests",
                "status": "active",
                "importance_score": 8,
                "created_at": "2024-01-01T00:00:00Z",
                "messages": [
                    {"role": "user", "content": "Hello", "timestamp": "2024-01-01T00:00:00Z"}
                ],
                "word_count": 100,
                "session_count": 1
            }
        }
        
        arguments = {
            "conversation_id": "conv-123",
            "format": "json",
            "include_metadata": True
        }
        
        result = await memory_export_tool(arguments)
        
        assert len(result) == 1
        assert "conv-123" in result[0].text
        assert "Test Conversation" in result[0].text


@pytest.mark.asyncio
async def test_memory_export_markdown_success():
    """Test export tool to Markdown format"""
    with patch('sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
        mock_get.return_value = {
            "success": True,
            "data": {
                "conversation_id": "conv-456",
                "label": "Markdown Export",
                "folder": "/work",
                "status": "active",
                "created_at": "2024-01-01T00:00:00Z",
                "messages": [{"role": "user", "content": "Test"}]
            }
        }
        
        arguments = {
            "conversation_id": "conv-456",
            "format": "markdown",
            "include_metadata": False
        }
        
        result = await memory_export_tool(arguments)
        
        assert len(result) == 1
        assert "# Markdown Export" in result[0].text
        assert "conv-456" in result[0].text


@pytest.mark.asyncio
async def test_memory_export_invalid_format():
    """Test export tool with invalid format"""
    with patch('sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
        mock_get.return_value = {
            "success": True,
            "data": {
                "conversation_id": "conv-123",
                "label": "Test",
                "folder": "/",
                "status": "active",
                "created_at": "2024-01-01T00:00:00Z",
                "messages": []
            }
        }
        
        arguments = {
            "conversation_id": "conv-123",
            "format": "xml"  # Invalid format
        }
        
        result = await memory_export_tool(arguments)
        
        assert len(result) == 1
        assert "Unsupported format" in result[0].text


@pytest.mark.asyncio
async def test_memory_export_conversation_not_found():
    """Test export tool when conversation doesn't exist"""
    with patch('sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
        mock_get.return_value = {"success": False, "error": "Not found"}
        
        arguments = {"conversation_id": "nonexistent"}
        
        result = await memory_export_tool(arguments)
        
        assert len(result) == 1
        assert "Export failed" in result[0].text    


@pytest.mark.asyncio
async def test_memory_update_exception_during_request():
    """Test update tool handles connection errors"""
    with patch('sekha_mcp.client.sekha_client.update_conversation', new=AsyncMock()) as mock_update:
        mock_update.side_effect = Exception("Connection failed")
        
        arguments = {
            "conversation_id": "test-uuid",
            "label": "Test",
            "folder": "/tests"
        }
        
        result = await memory_update_tool(arguments)
        
        assert len(result) == 1
        assert "❌ Error" in result[0].text


@pytest.mark.asyncio
async def test_memory_export_incomplete_metadata():
    """Test export when metadata fields are missing"""
    with patch('sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
        mock_get.return_value = {
            "success": True,
            "data": {
                "conversation_id": "conv-123",
                "label": "Test",
                "folder": "/",
                "status": "active",
                "created_at": "2024-01-01T00:00:00Z",
                "messages": [{"role": "user", "content": "Hello"}]
                # Missing word_count and session_count
            }
        }
        
        arguments = {
            "conversation_id": "conv-123",
            "format": "json",
            "include_metadata": True
        }
        
        result = await memory_export_tool(arguments)
        
        assert len(result) == 1
        assert "conv-123" in result[0].text
        assert "Test" in result[0].text


# Add to hit models.py branches
def test_models_enum_serialization():
    """Test MessageRole enum serializes correctly"""
    from sekha_mcp.models import MessageRole, Message
    
    msg = Message(role=MessageRole.USER, content="Test")
    assert msg.role == MessageRole.USER
    assert msg.role.value == "user"


@pytest.mark.asyncio
async def test_memory_stats_global():
    """Test stats for all conversations"""
    with patch('sekha_mcp.client.sekha_client.get_stats', new=AsyncMock()) as mock_stats:
        mock_stats.return_value = {
            "success": True,
            "data": {
                "total_conversations": 42,
                "average_importance": 7.3,
                "folders": ["/work", "/personal"]
            }
        }
        
        result = await memory_stats_tool({})
        
        assert len(result) == 1
        assert "42" in result[0].text
        assert "7.3" in result[0].text


@pytest.mark.asyncio
async def test_memory_stats_by_folder():
    """Test stats for specific folder"""
    with patch('sekha_mcp.client.sekha_client.get_stats', new=AsyncMock()) as mock_stats:
        mock_stats.return_value = {
            "success": True,
            "data": {
                "total_conversations": 15,
                "average_importance": 8.1,
                "folders": ["/work/projects"]
            }
        }
        
        result = await memory_stats_tool({"folder": "/work/projects"})
        
        assert len(result) == 1
        assert "15" in result[0].text
        mock_stats.assert_called_once_with(folder="/work/projects")


@pytest.mark.asyncio
async def test_memory_stats_api_failure():
    """Test stats handles API failure"""
    with patch('sekha_mcp.client.sekha_client.get_stats', new=AsyncMock()) as mock_stats:
        mock_stats.return_value = {"success": False, "error": "Stats unavailable"}
        
        result = await memory_stats_tool({})
        
        assert len(result) == 1
        assert "❌" in result[0].text    