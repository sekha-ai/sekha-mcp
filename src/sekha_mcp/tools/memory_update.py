"""Memory Update Tool - Update conversation metadata"""

import logging
from typing import List
from mcp.types import Tool, TextContent

from ..client import sekha_client
from ..models import UpdateInput

logger = logging.getLogger(__name__)


async def memory_update_tool(arguments: dict) -> List[TextContent]:
    """
    Update conversation metadata (label, folder, importance score).
    
    Args:
        conversation_id: UUID of conversation to update
        label: New conversation title (optional)
        folder: New folder path (optional)
        importance_score: New importance score 0.0-10.0 (optional)
    
    Returns:
        Success status with list of updated fields
    """
    try:
        update_input = UpdateInput(**arguments)
        
        # Validate at least one field is being updated
        fields_to_update = [
            f for f in [update_input.label, update_input.folder, update_input.importance_score]
            if f is not None
        ]
        if not fields_to_update:
            raise ValueError("At least one field (label, folder, or importance_score) must be provided")
        
        result = await sekha_client.update_conversation(
            conversation_id=update_input.conversation_id,
            label=update_input.label,
            folder=update_input.folder,
            importance_score=update_input.importance_score
        )
        
        if result.get("success") and "data" in result:
            updated_fields = result["data"].get("updated_fields", [])
            
            if not updated_fields:
                return [
                    TextContent(
                        type="text",
                        text=(
                            "⚠️ Conversation update completed, but no fields were changed.\n"
                            "Check if the values are different from current ones."
                        )
                    )
                ]
            
            return [
                TextContent(
                    type="text",
                    text=(
                        f"✅ Conversation updated successfully!\n"
                        f"Fields changed: {', '.join(updated_fields)}"
                    )
                )
            ]
        else:
            error_msg = result.get("error", "Update failed")
            logger.warning(f"Update failed: {error_msg}")
            return [TextContent(type="text", text=f"❌ Update failed: {error_msg}")]
    
    except ValueError as ve:
        logger.error(f"Validation error in memory_update: {ve}")
        return [TextContent(type="text", text=f"❌ Validation error: {str(ve)}")]
    except Exception as e:
        logger.error(f"Memory update failed: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_UPDATE_TOOL = Tool(
    name="memory_update",
    description="Update conversation metadata (label, folder, importance score)",
    inputSchema={
        "type": "object",
        "properties": {
            "conversation_id": {
                "type": "string",
                "description": "UUID of the conversation to update",
                "minLength": 1,
                "pattern": "^[a-f0-9\\-]{36}$"
            },
            "label": {
                "type": "string",
                "description": "New conversation title",
                "minLength": 1,
                "maxLength": 500
            },
            "folder": {
                "type": "string",
                "description": "New folder path (e.g., /projects/ai)",
                "pattern": "^/[a-zA-Z0-9_\\-/]*$"
            },
            "importance_score": {
                "type": "number",
                "description": "New importance score (0.0-10.0, higher is more important)",
                "minimum": 0.0,
                "maximum": 10.0
            }
        },
        "required": ["conversation_id"]
    }
)