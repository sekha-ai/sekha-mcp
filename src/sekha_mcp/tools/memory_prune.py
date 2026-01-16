"""Memory Prune Tool - Get suggestions for old/low-importance conversations"""

import logging

from mcp.types import TextContent, Tool

from ..client import sekha_client
from ..models import PruneInput

logger = logging.getLogger(__name__)


async def memory_prune_tool(arguments: dict) -> list[TextContent]:
    """
    Get pruning suggestions for old or low-importance conversations.

    Args:
        threshold_days: Age threshold in days (default: 30)
        importance_threshold: Minimum importance score to keep (0.0-10.0)

    Returns:
        List of suggested conversations to prune with reasoning
    """
    try:
        prune_input = PruneInput(**arguments)

        result = await sekha_client.prune_memory(
            threshold_days=prune_input.threshold_days,
            importance_threshold=prune_input.importance_threshold,
        )

        if result.get("success") and "data" in result:
            suggestions = result["data"].get("suggestions", [])

            if not suggestions:
                return [
                    TextContent(
                        type="text",
                        text=(
                            "✅ No conversations need pruning.\n"
                            f"All conversations are within {prune_input.threshold_days} days "
                            f"or above importance threshold."
                        ),
                    )
                ]

            output = [
                f"🗑️ Found {len(suggestions)} conversation{'s' if len(suggestions) > 1 else ''} "
                f"to consider pruning:\n"
            ]

            for i, sugg in enumerate(suggestions, 1):
                label = sugg.get("label", "Untitled")
                conv_id = sugg.get("conversation_id", "unknown")
                age = sugg.get("age_days", 0)
                importance = sugg.get("importance_score", 0)
                reason = sugg.get("reason", "No reason provided")

                output.append(
                    f"\n{i}. **{label}** (ID: {conv_id})\n"
                    f"   📅 Age: {age} days\n"
                    f"   ⭐ Importance: {importance}/10\n"
                    f"   💭 Reason: {reason}"
                )

            output.append(
                "\n\n💡 Tip: Review these conversations before pruning. "
                "Consider updating importance scores for valuable old conversations."
            )

            return [TextContent(type="text", text="".join(output))]
        else:
            error_msg = result.get("error", "Prune check failed")
            logger.warning(f"Prune check failed: {error_msg}")
            return [TextContent(type="text", text=f"❌ Prune check failed: {error_msg}")]

    except Exception as e:
        logger.error(f"Memory prune failed: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_PRUNE_TOOL = Tool(
    name="memory_prune",
    description="Get AI-powered suggestions for pruning old or low-importance conversations",
    inputSchema={
        "type": "object",
        "properties": {
            "threshold_days": {
                "type": "integer",
                "description": "Age threshold in days (conversations older than this are candidates)",
                "default": 30,
                "minimum": 1,
                "maximum": 365,
            },
            "importance_threshold": {
                "type": "number",
                "description": "Minimum importance score to keep (0.0-10.0)",
                "minimum": 0.0,
                "maximum": 10.0,
            },
        },
        "required": [],
    },
)
