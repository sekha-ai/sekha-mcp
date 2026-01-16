"""Memory Store Tool - Stores conversations in Sekha memory system"""

import logging

from mcp.types import TextContent, Tool

from ..client import sekha_client
from ..models import ConversationInput, MessageRole

logger = logging.getLogger(__name__)


async def memory_store_tool(arguments: dict) -> list[TextContent]:
    """
    Store a new conversation in Sekha memory.

    Args:
        label: Conversation title/label (max 500 chars)
        folder: Folder path (e.g., /projects/ai)
        messages: List of message objects with role, content, timestamp, metadata
        importance_score: Optional importance score 0.0-10.0

    Returns:
        List of TextContent objects with status message and conversation ID
    """
    try:
        # Validate and parse input
        conv_input = ConversationInput(**arguments)

        # Ensure at least one message
        if not conv_input.messages:
            raise ValueError("At least one message is required")

        # Convert to API format
        conversation = {
            "label": conv_input.label,
            "folder": conv_input.folder,
            "messages": [
                {
                    "role": msg.role.value if isinstance(msg.role, MessageRole) else msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                    "metadata": msg.metadata or {},
                }
                for msg in conv_input.messages
            ],
        }

        if conv_input.importance_score is not None:
            conversation["importance_score"] = conv_input.importance_score

        # Store via Sekha Controller
        result = await sekha_client.store_conversation(conversation)

        if result.get("success") and "data" in result:
            data = result["data"]
            return [
                TextContent(
                    type="text",
                    text=(
                        f"✅ Conversation stored successfully!\n"
                        f"ID: {data.get('conversation_id', 'unknown')}\n"
                        f"Messages: {data.get('message_count', 0)}"
                    ),
                )
            ]
        else:
            error_msg = result.get("error", "Unknown error")
            logger.warning(f"Store failed: {error_msg}")
            return [TextContent(type="text", text=f"❌ Failed to store conversation: {error_msg}")]

    except ValueError as ve:
        logger.error(f"Validation error in memory_store: {ve}")
        return [TextContent(type="text", text=f"❌ Validation error: {str(ve)}")]
    except Exception as e:
        logger.error(f"Memory store failed: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_STORE_TOOL = Tool(
    name="memory_store",
    description="Store a new conversation in Sekha memory system with validation",
    inputSchema={
        "type": "object",
        "properties": {
            "label": {
                "type": "string",
                "description": "Conversation title/label",
                "minLength": 1,
                "maxLength": 500,
            },
            "folder": {
                "type": "string",
                "description": "Folder path (e.g., /projects/ai)",
                "pattern": "^/[a-zA-Z0-9_\\-/]*$",
            },
            "messages": {
                "type": "array",
                "description": "List of conversation messages",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {
                            "type": "string",
                            "enum": ["user", "assistant", "system"],
                            "description": "Message role",
                        },
                        "content": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Message content",
                        },
                        "timestamp": {
                            "type": "string",
                            "format": "date-time",
                            "description": "ISO 8601 timestamp",
                        },
                        "metadata": {
                            "type": "object",
                            "description": "Additional message metadata",
                            "default": {},
                        },
                    },
                    "required": ["role", "content"],
                },
            },
            "importance_score": {
                "type": "number",
                "description": "Importance score (0.0-10.0, higher is more important)",
                "minimum": 0.0,
                "maximum": 10.0,
                "default": 5.0,
            },
        },
        "required": ["label", "folder", "messages"],
    },
)
