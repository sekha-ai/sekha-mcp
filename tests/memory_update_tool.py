# tests/test_memory_update_tool.py
import pytest
from unittest.mock import AsyncMock, patch
from sekha_mcp.client import sekha_client
from sekha_mcp.tools.memory_update import memory_update_tool

@pytest.mark.asyncio
async def test_memory_update_tool_renders_results():
    with patch.object(sekha_client, "search_memory", new=AsyncMock()) as mock_update:
        mock_update.return_value = {
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
        # This needs to be corrected
        result = await memory_update_tool({"query": "x", "limit": 5})
        assert "found 1 relevant" in result[0].text.lower()
