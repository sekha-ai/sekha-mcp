"""Memory Search Tool"""

import logging
from mcp.types import Tool, TextContent

from ..client import sekha_client
from ..models import SearchInput

logger = logging.getLogger(__name__)


async def memory_search_tool(arguments: dict) -> list[TextContent]:
    """
    Search conversations using semantic similarity.
    
    Args:
        query: Search query
        limit: Maximum results (default: 10)
        filter_labels: Optional list of labels to filter by
    
    Returns:
        Relevant conversation excerpts with metadata
    """
    try:
        search_input = SearchInput(**arguments)
        
        result = await sekha_client.search_memory(
            query=search_input.query,
            limit=search_input.limit,
            filter_labels=search_input.filter_labels
        )
        
        if result.get("success"):
            results = result["data"]["results"]
            
            if not results:
                return [TextContent(type="text", text="No matching conversations found.")]
            
            output = [f"🔍 Found {len(results)} relevant conversations:\n"]
            
            for i, res in enumerate(results, 1):
                output.append(
                    f"\n{i}. **{res['label']}** (Score: {res['similarity']:.2f})\n"
                    f"   Folder: {res['folder']}\n"
                    f"   Excerpt: {res['content'][:200]}...\n"
                    f"   ID: {res['conversation_id']}"
                )
            
            return [TextContent(type="text", text="".join(output))]
        else:
            return [TextContent(type="text", text="❌ Search failed")]
    
    except Exception as e:
        logger.error(f"Memory search failed: {e}")
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


MEMORY_SEARCH_TOOL = Tool(
    name="memory_search",
    description="Search conversations using semantic similarity",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (natural language)"
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
                "items": {"type": "string"}
            }
        },
        "required": ["query"]
    }
)
