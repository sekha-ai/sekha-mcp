"""Memory Get Context Tool - Retrieve full conversation details"""

import logging
from typing import List
from mcp.types import Tool, TextContent

from ..client import sekha_client
from ..models import ContextInput

logger = logging.getLogger(__name__)


async def memory_get_context_tool(arguments: dict) -> List[TextContent]:
    """
    Retrieve full conversation with all messages and metadata.
    
    Args:
        conversation_id: UUID of the conversation to retrieve
    
    Returns:
        Complete conversation with formatted message history
    """
    try:
        context_input = ContextInput(**arguments)
        
        result = await sekha_client.get_context(context_input.conversation_id)
        
        if result.get("success") and "data" in result:
            data = result["data"]
            
            # Validate required fields
            required_fields = ['label', 'folder', 'status', 'messages']
            missing = [f for f in required_fields if f not in data]
            if missing:
                raise ValueError(f"Missing required fields: {missing}")
            
            messages = data.get("messages", [])
            if not messages:
                logger.warning(f"Conversation {context_input.conversation_id} has no messages")
            
            output = [
                f"📄 **{data.get('label', 'Untitled')}**\n",
                f"📁 Folder: {data.get('folder', '/')}\n",
                f"📊 Status: {data.get('status', 'unknown')}\n",
                f"⭐ Importance: {data.get('importance_score', 'N/A')}\n",
                f"🕐 Created: {data.get('created_at', 'Unknown')}\n",
                f"📝 Messages: {len(messages)}\n",
                "=" * 50,
                "\n"
            ]
            
            for i, msg in enumerate(messages, 1):
                role = msg.get('role', 'unknown').upper()
                content = msg.get('content', '')
                output.append(f"{i}. **{role}**: {content}\n")
            
            if not messages:
                output.append("\n*No messages found in this conversation*\n")
            
            return [TextContent(type="text", text="".join(output))]
        else:
            error_msg = result.get("error", "Conversation not found")
            logger.warning(f"Get context failed: {error_msg}")
            return [TextContent(type="text", text=f"❌ Conversation not found: {error_msg}")]
    
    except ValueError as ve:
        logger.error(f"Validation error in memory_get_context: {ve}")
        return [TextContent(type="text", text=f"❌ Validation error: {str(ve)}")]
    except Exception as e:
        logger.error(f"Get context failed: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_GET_CONTEXT_TOOL = Tool(
    name="memory_get_context",
    description="Retrieve complete conversation context with full message history",
    inputSchema={
        "type": "object",
        "properties": {
            "conversation_id": {
                "type": "string",
                "description": "UUID of the conversation to retrieve",
                "minLength": 1,
                "pattern": "^[a-f0-9\\-]{36}$"
            }
        },
        "required": ["conversation_id"]
    }
)