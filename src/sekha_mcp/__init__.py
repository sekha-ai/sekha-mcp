"""Sekha MCP Server - Model Context Protocol implementation for AI memory

v0.2.0 Release:
- Compatible with Sekha v2.0 multi-provider architecture
- Transparent provider routing via controller
- No breaking changes to MCP API
"""

__version__ = "0.2.0"
__all__ = ["main", "server", "client", "config", "health", "models", "tools"]

from . import client, config, health, main, models, server, tools
