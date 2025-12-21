"""Memory Get Context Tool"""

import logging
from mcp.types import Tool, TextContent

from ..client import sekha_client
from ..models import ContextInput

logger = logging.getLogger(__name__)


async def memory_get_context_tool(arguments: dict) -> list[TextContent]:
    """Retrieve full conversation context"""
    try:
        context_input = ContextInput(**arguments)
        
        result = await sekha_client.get_context(context_input.conversation_id)
        
        if result.get("success"):
            data = result["data"]
            
            output = [
                f"📄 **{data['label']}**\n",
                f"Folder: {data['folder']}\n",
                f"Status: {data['status']}\n",
                f"Importance: {data.get('importance_score', 'N/A')}\n",
                f"Created: {data['created_at']}\n\n",
                f"**Messages ({len(data['messages'])}):**\n"
            ]
            
            for msg in data["messages"]:
                output.append(f"\n**{msg['role'].upper()}**: {msg['content']}")
            
            return [TextContent(type="text", text="".join(output))]
        else:
            return [TextContent(type="text", text="❌ Conversation not found")]
    
    except Exception as e:
        logger.error(f"Get context failed: {e}")
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_GET_CONTEXT_TOOL = Tool(
    name="memory_get_context",
    description="Retrieve full conversation with all messages",
    inputSchema={
        "type": "object",
        "properties": {
            "conversation_id": {
                "type": "string",
                "description": "Conversation UUID"
            }
        },
        "required": ["conversation_id"]
    }
)
