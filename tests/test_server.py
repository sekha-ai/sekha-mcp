"""Tests for MCP server.py"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

from sekha_mcp.server import app, list_tools, call_tool
from sekha_mcp.tools.memory_store import MEMORY_STORE_TOOL
from sekha_mcp.tools.memory_search import MEMORY_SEARCH_TOOL
from sekha_mcp.tools.memory_update import MEMORY_UPDATE_TOOL
from sekha_mcp.tools.memory_get_context import MEMORY_GET_CONTEXT_TOOL
from sekha_mcp.tools.memory_prune import MEMORY_PRUNE_TOOL
from sekha_mcp.tools.memory_export import MEMORY_EXPORT_TOOL
from sekha_mcp.tools.memory_stats import MEMORY_STATS_TOOL


@pytest.mark.asyncio
async def test_list_tools_returns_all_tools():
    """Test that list_tools returns all 5 tools"""
    tools = await list_tools()
    
    assert len(tools) == 7
    tool_names = [tool.name for tool in tools]
    assert "memory_store" in tool_names
    assert "memory_search" in tool_names
    assert "memory_update" in tool_names
    assert "memory_get_context" in tool_names
    assert "memory_prune" in tool_names
    assert "memory_export" in tool_names
    assert "memory_stats" in tool_names


@pytest.mark.asyncio
async def test_call_tool_memory_store():
    """Test calling memory_store tool"""
    with patch('sekha_mcp.server.memory_store_tool', new_callable=AsyncMock) as mock_tool:
        mock_tool.return_value = [{"type": "text", "text": "Success"}]
        
        result = await call_tool("memory_store", {"label": "Test"})
        
        assert len(result) == 1
        mock_tool.assert_called_once_with({"label": "Test"})


@pytest.mark.asyncio
async def test_call_tool_unknown_tool():
    """Test calling unknown tool raises error"""
    with pytest.raises(ValueError) as exc_info:
        await call_tool("unknown_tool", {})
    
    assert "unknown tool" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_call_tool_all_tools_routing():
    """Test that all 7 tools are properly routed"""
    test_cases = [
        ("memory_store", {"label": "Test", "folder": "/tests", "messages": [{"role": "user", "content": "test"}]}),
        ("memory_search", {"query": "test query", "limit": 10}),
        ("memory_update", {"conversation_id": "test-uuid", "label": "Updated"}),
        ("memory_get_context", {"conversation_id": "test-uuid"}),
        ("memory_prune", {"threshold_days": 30}),
        ("memory_export", {"conversation_id": "test-uuid", "format": "json"}),
        ("memory_stats", {"folder": "/work"}),
    ]
    
    for tool_name, arguments in test_cases:
        # Patch the tool in the server module where it's imported
        with patch(f'sekha_mcp.server.{tool_name}_tool', new_callable=AsyncMock) as mock_tool:
            mock_tool.return_value = [{"type": "text", "text": "ok"}]
            
            result = await call_tool(tool_name, arguments)
            
            assert len(result) == 1
            mock_tool.assert_called_once_with(arguments)