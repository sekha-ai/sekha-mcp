# tests/test_memory_search_tool.py
from unittest.mock import AsyncMock, patch

import pytest

from sekha_mcp.client import sekha_client
from sekha_mcp.tools.memory_search import memory_search_tool


@pytest.mark.asyncio
async def test_memory_search_tool_renders_results():
    with patch.object(sekha_client, "search_memory", new=AsyncMock()) as mock_search:
        mock_search.return_value = {
            "success": True,
            "data": {
                "results": [
                    {
                        "label": "Found",
                        "folder": "/tests",
                        "content": "some content",
                        "similarity": 0.9,
                        "conversation_id": "id-1",
                    }
                ]
            },
        }
        result = await memory_search_tool({"query": "x", "limit": 5})
        assert "found 1 relevant" in result[0].text.lower()
