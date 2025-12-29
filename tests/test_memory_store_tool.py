# tests/test_memory_store_tool.py
import pytest
from unittest.mock import AsyncMock, patch
from sekha_llm_bridge.client import sekha_client
from sekha_llm_bridge.tools.memory_store import memory_store_tool

@pytest.mark.asyncio
async def test_memory_store_tool_success():
    with patch.object(sekha_client, "store_conversation", new=AsyncMock()) as mock_store:
        mock_store.return_value = {
            "success": True,
            "data": {"conversation_id": "test-id", "message_count": 2},
        }

        args = {
            "label": "Test",
            "folder": "/tests",
            "messages": [
                {"role": "user", "content": "hi"},
                {"role": "assistant", "content": "hello"},
            ],
        }

        result = await memory_store_tool(args)
        assert len(result) == 1
        assert "stored successfully" in result[0].text.lower()
        mock_store.assert_awaited_once()
