"""Memory Export Tool - Export conversations to portable formats"""

import logging
import json
from datetime import datetime
from typing import List, Optional
from mcp.types import Tool, TextContent

from ..client import sekha_client
from ..models import ConversationContextRequest

logger = logging.getLogger(__name__)


async def memory_export_tool(arguments: dict) -> List[TextContent]:
    """
    Export conversation to JSON or Markdown format.
    
    Args:
        conversation_id: UUID of conversation to export
        format: Export format ('json' or 'markdown')
        include_metadata: Include metadata fields (default: true)
    
    Returns:
        Exported conversation in requested format
    """
    try:
        context_request = ConversationContextRequest(**arguments)
        export_format = arguments.get("format", "json")
        include_metadata = arguments.get("include_metadata", True)
        
        # Retrieve full conversation
        result = await sekha_client.get_context(context_request.conversation_id)
        
        if not result.get("success") or "data" not in result:
            error_msg = result.get("error", "Conversation not found")
            return [TextContent(type="text", text=f"❌ Export failed: {error_msg}")]
        
        data = result["data"]
        
        if export_format.lower() == "json":
            export_content = _export_to_json(data, include_metadata)
            return [TextContent(type="text", text=export_content)]
        
        elif export_format.lower() == "markdown":
            export_content = _export_to_markdown(data, include_metadata)
            return [TextContent(type="text", text=export_content)]
        
        else:
            raise ValueError(f"Unsupported format: {export_format}. Use 'json' or 'markdown'")
    
    except ValueError as ve:
        logger.error(f"Export validation error: {ve}")
        return [TextContent(type="text", text=f"❌ Validation error: {str(ve)}")]
    except Exception as e:
        logger.error(f"Export failed: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


def _export_to_json(data: dict, include_metadata: bool) -> str:
    """Export conversation to JSON format"""
    export = {
        "conversation_id": data.get("conversation_id"),
        "label": data.get("label"),
        "folder": data.get("folder"),
        "status": data.get("status"),
        "importance_score": data.get("importance_score"),
        "created_at": data.get("created_at"),
        "exported_at": datetime.utcnow().isoformat() + "Z",
        "messages": data.get("messages", []),
    }
    
    if include_metadata and data.get("word_count"):
        export["metadata"] = {
            "word_count": data.get("word_count"),
            "session_count": data.get("session_count"),
        }
    
    return json.dumps(export, indent=2, ensure_ascii=False)


def _export_to_markdown(data: dict, include_metadata: bool) -> str:
    """Export conversation to Markdown format"""
    lines = [
        f"# {data.get('label', 'Untitled Conversation')}",
        "",
        f"**ID:** `{data.get('conversation_id')}`",
        f"**Folder:** {data.get('folder', '/')}",
        f"**Status:** {data.get('status', 'unknown')}",
        f"**Importance:** {data.get('importance_score', 'N/A')}/10",
        f"**Created:** {data.get('created_at', 'Unknown')}",
        f"**Exported:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        "",
    ]
    
    if include_metadata:
        if data.get("word_count"):
            lines.append(f"**Word Count:** {data.get('word_count')}")
        if data.get("session_count"):
            lines.append(f"**Sessions:** {data.get('session_count')}")
        lines.append("")
    
    lines.append("## Messages")
    lines.append("")
    
    for i, msg in enumerate(data.get("messages", []), 1):
        role = msg.get('role', 'unknown').capitalize()
        content = msg.get('content', '')
        timestamp = msg.get('timestamp', '')
        
        lines.append(f"### {i}. {role}")
        if timestamp:
            lines.append(f"*{timestamp}*")
        lines.append("")
        lines.append(content)
        lines.append("")
    
    return "\n".join(lines)


MEMORY_EXPORT_TOOL = Tool(
    name="memory_export",
    description="Export conversation to JSON or Markdown format for backup or external use",
    inputSchema={
        "type": "object",
        "properties": {
            "conversation_id": {
                "type": "string",
                "description": "UUID of conversation to export",
                "minLength": 1,
                "pattern": "^[a-f0-9\\-]{36}$"
            },
            "format": {
                "type": "string",
                "description": "Export format: 'json' or 'markdown'",
                "enum": ["json", "markdown"],
                "default": "json"
            },
            "include_metadata": {
                "type": "boolean",
                "description": "Include metadata fields (word count, session count)",
                "default": True
            }
        },
        "required": ["conversation_id"]
    }
)