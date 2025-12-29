"""Unit tests for MCP tools"""

import pytest
from unittest.mock import AsyncMock, patch

from sekha_llm_bridge.tools.memory_store import memory_store_tool
from sekha_llm_bridge.tools.memory_search import memory_search_tool
from sekha_llm_bridge.tools.memory_update import memory_update_tool
from sekha_llm_bridge.tools.memory_get_context import memory_get_context_tool
from sekha_llm_bridge.tools.memory_prune import memory_prune_tool


# ============================================
# Memory Store Tests
# ============================================

@pytest.mark.asyncio
async def test_memory_store_success():
    """Test successful memory store"""
    with patch('src.sekha_mcp.client.sekha_client.store_conversation', new=AsyncMock()) as mock_store:
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
    with patch('src.sekha_mcp.client.sekha_client.store_conversation', new=AsyncMock()) as mock_store:
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
    with patch('src.sekha_mcp.client.sekha_client.search_memory', new=AsyncMock()) as mock_search:
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
    with patch('src.sekha_mcp.client.sekha_client.search_memory', new=AsyncMock()) as mock_search:
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
    with patch('src.sekha_mcp.client.sekha_client.search_memory', new=AsyncMock()) as mock_search:
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
    with patch('src.sekha_mcp.client.sekha_client.update_conversation', new=AsyncMock()) as mock_update:
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
    with patch('src.sekha_mcp.client.sekha_client.update_conversation', new=AsyncMock()) as mock_update:
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
    with patch('src.sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
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
    with patch('src.sekha_mcp.client.sekha_client.get_context', new=AsyncMock()) as mock_get:
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
    with patch('src.sekha_mcp.client.sekha_client.prune_memory', new=AsyncMock()) as mock_prune:
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
        assert "Found 1 conversations" in result[0].text
        assert "Old Conversation" in result[0].text


@pytest.mark.asyncio
async def test_memory_prune_no_suggestions():
    """Test pruning with no suggestions"""
    with patch('src.sekha_mcp.client.sekha_client.prune_memory', new=AsyncMock()) as mock_prune:
        mock_prune.return_value = {
            "success": True,
            "data": {"suggestions": []}
        }
        
        arguments = {"threshold_days": 30}
        result = await memory_prune_tool(arguments)
        
        assert len(result) == 1
        assert "No conversations need pruning" in result[0].text
