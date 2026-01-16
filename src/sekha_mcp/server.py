"""Sekha MCP Server Implementation"""

import asyncio
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server

from .config import settings
from .tools.memory_export import MEMORY_EXPORT_TOOL, memory_export_tool
from .tools.memory_get_context import MEMORY_GET_CONTEXT_TOOL, memory_get_context_tool
from .tools.memory_prune import MEMORY_PRUNE_TOOL, memory_prune_tool
from .tools.memory_search import MEMORY_SEARCH_TOOL, memory_search_tool
from .tools.memory_stats import MEMORY_STATS_TOOL, memory_stats_tool
from .tools.memory_store import MEMORY_STORE_TOOL, memory_store_tool
from .tools.memory_update import MEMORY_UPDATE_TOOL, memory_update_tool

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Create MCP server
app = Server(settings.server_name)


@app.list_tools()
async def list_tools():
    """Register available MCP tools"""
    return [
        MEMORY_STORE_TOOL,
        MEMORY_SEARCH_TOOL,
        MEMORY_UPDATE_TOOL,
        MEMORY_GET_CONTEXT_TOOL,
        MEMORY_PRUNE_TOOL,
        MEMORY_EXPORT_TOOL,
        MEMORY_STATS_TOOL,
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Route tool calls to appropriate handlers"""
    logger.info(f"Tool called: {name}")

    tools = {
        "memory_store": memory_store_tool,
        "memory_search": memory_search_tool,
        "memory_update": memory_update_tool,
        "memory_get_context": memory_get_context_tool,
        "memory_prune": memory_prune_tool,
        "memory_export": memory_export_tool,
        "memory_stats": memory_stats_tool,
    }

    if name not in tools:
        raise ValueError(f"Unknown tool: {name}")

    return await tools[name](arguments)


async def main():
    """Start MCP server using stdio transport"""
    logger.info(f"🚀 Starting {settings.server_name} v{settings.server_version}")
    logger.info(f"📡 Connected to Sekha Controller: {settings.controller_url}")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
