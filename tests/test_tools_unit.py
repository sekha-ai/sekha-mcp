"""Integration tests for MCP server"""

import pytest
import httpx
from unittest.mock import AsyncMock, patch

from sekha_mcp.client import sekha_client
from sekha_mcp.tools.memory_store import memory_store_tool
from sekha_mcp.tools.memory_search import memory_search_tool


@pytest.mark.asyncio
async def test_memory_store_tool():
    """Test memory store tool"""
    with patch.object(sekha_client, "store_conversation", new=AsyncMock()) as mock_store:
        mock_store.return_value = {
            "success": True,
            "data": {
                "conversation_id": "test-uuid",
                "message_count": 2
            }
        }
        
        arguments = {
            "label": "Test Conversation",
            "folder": "/tests",
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ]
        }
        
        result = await memory_store_tool(arguments)
        
        assert len(result) == 1
        assert "stored successfully" in result[0].text
        assert "test-uuid" in result[0].text


@pytest.mark.asyncio
async def test_memory_search_tool():
    """Test memory search tool"""
    with patch.object(sekha_client, "search_memory", new=AsyncMock()) as mock_search:
        mock_search.return_value = {
            "success": True,
            "data": {
                "results": [
                    {
                        "label": "Found Conversation",
                        "folder": "/tests",
                        "content": "Test content here",
                        "similarity": 0.95,
                        "conversation_id": "test-uuid"
                    }
                ]
            }
        }
        
        arguments = {"query": "test query", "limit": 10}
        result = await memory_search_tool(arguments)
        
        assert len(result) == 1
        assert "Found 1 relevant conversation" in result[0].text