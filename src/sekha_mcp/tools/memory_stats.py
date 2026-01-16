"""Memory Stats Tool - Get usage analytics and insights"""

import logging

from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from ..client import sekha_client

logger = logging.getLogger(__name__)


class StatsInput(BaseModel):
    folder: str = Field(None, description="Optional folder to analyze")


async def memory_stats_tool(arguments: dict) -> list[TextContent]:
    """
    Get memory system statistics and analytics.

    Args:
        folder: Optional specific folder to analyze
    """
    try:
        input_data = StatsInput(**arguments)

        result = await sekha_client.get_stats(folder=input_data.folder)

        if result.get("success") and "data" in result:
            data = result["data"]

            output = ["📊 Memory Statistics\n", "=" * 30, "\n"]

            output.append(f"Total Conversations: {data.get('total_conversations', 0)}\n")
            output.append(f"Average Importance: {data.get('average_importance', 0):.1f}/10\n")

            if data.get("folders"):
                output.append("\n📁 Folders:\n")
                for folder in data["folders"]:
                    output.append(f"  - {folder}\n")

            if data.get("estimated_token_savings"):
                output.append(f"\n💾 Estimated Storage: {data['estimated_token_savings']} tokens\n")

            return [TextContent(type="text", text="".join(output))]
        else:
            error_msg = result.get("error", "Stats retrieval failed")
            return [TextContent(type="text", text=f"❌ {error_msg}")]

    except Exception as e:
        logger.error(f"Stats failed: {e}")
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_STATS_TOOL = Tool(
    name="memory_stats",
    description="Get memory system statistics and usage analytics",
    inputSchema={
        "type": "object",
        "properties": {
            "folder": {
                "type": "string",
                "description": "Optional specific folder to analyze",
                "pattern": "^/[a-zA-Z0-9_\\-/]*$",
            }
        },
        "required": [],
    },
)
