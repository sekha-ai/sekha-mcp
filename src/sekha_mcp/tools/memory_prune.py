"""Memory Prune Tool"""

import logging
from mcp.types import Tool, TextContent

from ..client import sekha_client
from ..models import PruneInput

logger = logging.getLogger(__name__)


async def memory_prune_tool(arguments: dict) -> list[TextContent]:
    """Get pruning suggestions for old conversations"""
    try:
        prune_input = PruneInput(**arguments)
        
        result = await sekha_client.prune_memory(
            threshold_days=prune_input.threshold_days,
            importance_threshold=prune_input.importance_threshold
        )
        
        if result.get("success"):
            suggestions = result["data"]["suggestions"]
            
            if not suggestions:
                return [TextContent(type="text", text="✅ No conversations need pruning")]
            
            output = [f"🗑️ Found {len(suggestions)} conversations to consider pruning:\n"]
            
            for i, sugg in enumerate(suggestions, 1):
                output.append(
                    f"\n{i}. **{sugg['label']}** (ID: {sugg['conversation_id']})\n"
                    f"   Age: {sugg['age_days']} days\n"
                    f"   Importance: {sugg['importance_score']}\n"
                    f"   Reason: {sugg['reason']}"
                )
            
            return [TextContent(type="text", text="".join(output))]
        else:
            return [TextContent(type="text", text="❌ Prune check failed")]
    
    except Exception as e:
        logger.error(f"Memory prune failed: {e}")
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_PRUNE_TOOL = Tool(
    name="memory_prune",
    description="Get suggestions for pruning old/low-importance conversations",
    inputSchema={
        "type": "object",
        "properties": {
            "threshold_days": {
                "type": "integer",
                "description": "Age threshold in days",
                "default": 30,
                "minimum": 1
            },
            "importance_threshold": {
                "type": "number",
                "description": "Minimum importance score to keep",
                "minimum": 1,
                "maximum": 10
            }
        },
        "required": []
    }
)
