"""Memory Store Tool"""

import logging
from mcp.types import Tool, TextContent

from ..client import sekha_client
from ..models import ConversationInput

logger = logging.getLogger(__name__)


async def memory_store_tool(arguments: dict) -> list[TextContent]:
    """
    Store a new conversation in Sekha memory.
    
    Args:
        label: Conversation title/label
        folder: Folder path (e.g., /projects/ai)
        messages: List of messages with role, content, timestamp
        importance_score: Optional importance score (1-10)
    
    Returns:
        Success status and conversation ID
    """
    try:
        # Validate input
        conv_input = ConversationInput(**arguments)
        
        # Convert to API format
        conversation = {
            "label": conv_input.label,
            "folder": conv_input.folder,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                    "metadata": msg.metadata or {}
                }
                for msg in conv_input.messages
            ]
        }
        
        if conv_input.importance_score is not None:
            conversation["importance_score"] = conv_input.importance_score
        
        # Store via Sekha Controller
        result = await sekha_client.store_conversation(conversation)
        
        if result.get("success"):
            return [
                TextContent(
                    type="text",
                    text=f"✅ Conversation stored successfully!\n"
                         f"ID: {result['data']['conversation_id']}\n"
                         f"Messages: {result['data']['message_count']}"
                )
            ]
        else:
            return [TextContent(type="text", text=f"❌ Failed to store conversation")]
    
    except Exception as e:
        logger.error(f"Memory store failed: {e}")
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


# Tool definition
MEMORY_STORE_TOOL = Tool(
    name="memory_store",
    description="Store a new conversation in Sekha memory system",
    inputSchema={
        "type": "object",
        "properties": {
            "label": {
                "type": "string",
                "description": "Conversation title/label"
            },
            "folder": {
                "type": "string",
                "description": "Folder path (e.g., /projects/ai)"
            },
            "messages": {
                "type": "array",
                "description": "List of conversation messages",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string", "enum": ["user", "assistant"]},
                        "content": {"type": "string"},
                        "timestamp": {"type": "string", "format": "date-time"},
                        "metadata": {"type": "object"}
                    },
                    "required": ["role", "content"]
                }
            },
            "importance_score": {
                "type": "number",
                "description": "Importance score (1-10)",
                "minimum": 1,
                "maximum": 10
            }
        },
        "required": ["label", "folder", "messages"]
    }
)
