"""Minimal server tests without executing stdio"""

from unittest.mock import patch

import pytest

from sekha_mcp import server as server_module


def test_server_module_imports():
    """Test server module can be imported"""
    assert hasattr(server_module, "app")
    assert hasattr(server_module, "main")
    assert hasattr(server_module, "list_tools")
    assert hasattr(server_module, "call_tool")


def test_app_is_mcp_server():
    """Test app is an MCP Server instance"""
    from mcp.server import Server

    from sekha_mcp.server import app

    assert isinstance(app, Server)
    assert app.name == "sekha-memory"


def test_list_tools_registered():
    """Test that list_tools returns all 7 tools"""
    # Get tools
    import asyncio

    from sekha_mcp.server import list_tools

    tools = asyncio.run(list_tools())

    assert len(tools) == 7
    tool_names = {tool.name for tool in tools}
    assert tool_names == {
        "memory_store",
        "memory_search",
        "memory_update",
        "memory_get_context",
        "memory_prune",
        "memory_export",
        "memory_stats",
    }


@pytest.mark.asyncio
async def test_call_tool_routing():
    """Test call_tool routes to correct tool"""
    from sekha_mcp.server import call_tool

    # Mock the actual function that will be called
    with patch("sekha_mcp.server.memory_store_tool") as mock_tool:
        mock_tool.return_value = [{"type": "text", "text": "test"}]

        arguments = {
            "label": "test",
            "folder": "/tests",
            "messages": [{"role": "user", "content": "test"}],
        }

        result = await call_tool("memory_store", arguments)

        # Verify the tool was called with correct arguments
        mock_tool.assert_called_once()
        # Verify result is returned correctly
        assert result == [{"type": "text", "text": "test"}]
        call_args = mock_tool.call_args[0][0]
        assert call_args["label"] == "test"


@pytest.mark.asyncio
async def test_call_tool_unknown():
    """Test call_tool raises error for unknown tool"""
    from sekha_mcp.server import call_tool

    with pytest.raises(ValueError, match="Unknown tool:"):
        await call_tool("unknown_tool", {})


def test_server_tools_are_accessible():
    """Test that all tool functions are accessible from server"""
    from sekha_mcp import tools

    # Verify we can access all tools
    assert hasattr(tools, "memory_store_tool")
    assert hasattr(tools, "memory_search_tool")
    assert hasattr(tools, "memory_update_tool")
    assert hasattr(tools, "memory_get_context_tool")
    assert hasattr(tools, "memory_prune_tool")
    assert hasattr(tools, "memory_export_tool")
    assert hasattr(tools, "memory_stats_tool")

    # Verify tool definitions exist
    assert hasattr(tools, "MEMORY_STORE_TOOL")
    assert hasattr(tools, "MEMORY_SEARCH_TOOL")
    assert hasattr(tools, "MEMORY_UPDATE_TOOL")
    assert hasattr(tools, "MEMORY_GET_CONTEXT_TOOL")
    assert hasattr(tools, "MEMORY_PRUNE_TOOL")
    assert hasattr(tools, "MEMORY_EXPORT_TOOL")
    assert hasattr(tools, "MEMORY_STATS_TOOL")
