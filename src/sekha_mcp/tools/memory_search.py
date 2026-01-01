"""Memory Search Tool - Semantic search across conversations"""

import logging
from typing import List
from mcp.types import Tool, TextContent

from ..client import sekha_client
from ..models import SearchInput

logger = logging.getLogger(__name__)


async def memory_search_tool(arguments: dict) -> List[TextContent]:
    """
    Search conversations using semantic similarity.
    
    Args:
        query: Natural language search query
        limit: Maximum results to return (default: 10, max: 50)
        filter_labels: Optional list of labels to restrict search
    
    Returns:
        Formatted search results with similarity scores and excerpts
    """
    try:
        search_input = SearchInput(**arguments)
        
        # Validate query
        if not search_input.query.strip():
            raise ValueError("Search query cannot be empty")
        
        result = await sekha_client.search_memory(
            query=search_input.query,
            limit=search_input.limit,
            filter_labels=search_input.filter_labels
        )
        
        if result.get("success") and "data" in result:
            results = result["data"].get("results", [])
            
            if not results:
                return [TextContent(type="text", text="🔍 No matching conversations found.")]
            
            output = [
                f"🔍 Found {len(results)} relevant conversation{'s' if len(results) > 1 else ''}:\n"
            ]
            
            for i, res in enumerate(results, 1):
                similarity = res.get('similarity', 0)
                label = res.get('label', 'Untitled')
                folder = res.get('folder', '/')
                content = res.get('content', '')[:200]
                conv_id = res.get('conversation_id', 'unknown')
                
                output.append(
                    f"\n{i}. **{label}** (Score: {similarity:.2f})\n"
                    f"   📁 {folder}\n"
                    f"   📝 {content}{'...' if len(res.get('content', '')) > 200 else ''}\n"
                    f"   🆔 {conv_id}"
                )
            
            return [TextContent(type="text", text="".join(output))]
        else:
            error_msg = result.get("error", "Search failed")
            logger.warning(f"Search failed: {error_msg}")
            return [TextContent(type="text", text=f"❌ Search failed: {error_msg}")]
    
    except ValueError as ve:
        logger.error(f"Validation error in memory_search: {ve}")
        return [TextContent(type="text", text=f"❌ Validation error: {str(ve)}")]
    except Exception as e:
        logger.error(f"Memory search failed: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_SEARCH_TOOL = Tool(
    name="memory_search",
    description="Search conversations using semantic similarity with scoring",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language search query",
                "minLength": 1,
                "maxLength": 1000
            },
            "limit": {
                "type": "integer",
                "description": "Maximum results to return",
                "default": 10,
                "minimum": 1,
                "maximum": 50
            },
            "filter_labels": {
                "type": "array",
                "description": "Filter by specific conversation labels",
                "items": {
                    "type": "string",
                    "minLength": 1
                },
                "default": []
            }
        },
        "required": ["query"]
    }
)