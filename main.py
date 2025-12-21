"""Entry point for Sekha MCP Server"""

import asyncio
from src.sekha_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main())
