"""Memory Update Tool"""

import logging
from mcp.types import Tool, TextContent

from ..client import sekha_client
from ..models import UpdateInput

logger = logging.getLogger(__name__)


async def memory_update_tool(arguments: dict) -> list[TextContent]:
    """Update conversation metadata"""
    try:
        update_input = UpdateInput(**arguments)
        
        result = await sekha_client.update_conversation(
            conversation_id=update_input.conversation_id,
            label=update_input.label,
            folder=update_input.folder,
            importance_score=update_input.importance_score
        )
        
        if result.get("success"):
            updated = result["data"]["updated_fields"]
            return [
                TextContent(
                    type="text",
                    text=f"✅ Conversation updated!\nFields changed: {', '.join(updated)}"
                )
            ]
        else:
            return [TextContent(type="text", text="❌ Update failed")]
    
    except Exception as e:
        logger.error(f"Memory update failed: {e}")
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_UPDATE_TOOL = Tool(
    name="memory_update",
    description="Update conversation metadata (label, folder, importance)",
    inputSchema={
        "type": "object",
        "properties": {
            "conversation_id": {
                "type": "string",
                "description": "Conversation UUID"
            },
            "label": {
                "type": "string",
                "description": "New label/title"
            },
            "folder": {
                "type": "string",
                "description": "New folder path"
            },
            "importance_score": {
                "type": "number",
                "description": "New importance score (1-10)",
                "minimum": 1,
                "maximum": 10
            }
        },
        "required": ["conversation_id"]
    }
)
