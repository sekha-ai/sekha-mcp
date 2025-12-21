import asyncio
import json
from typing import Any, Dict, List

import httpx
from mcp.server import Server
from mcp.types import Tool, ToolInputSchema, TextContent

from config import settings


server = Server("sekha-mcp")


# ================================
# Tool definitions
# ================================

TOOLS: List[Tool] = [
    Tool(
        name="memory_store",
        description="Store a new conversation with messages into the Sekha controller.",
        input_schema=ToolInputSchema.json_schema(
            {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "folder": {"type": "string"},
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {"type": "string"},
                                "content": {"type": "string"},
                            },
                            "required": ["role", "content"],
                        },
                    },
                },
                "required": ["label", "folder", "messages"],
            }
        ),
    ),
    Tool(
        name="memory_search",
        description="Semantic search over stored conversations.",
        input_schema=ToolInputSchema.json_schema(
            {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            }
        ),
    ),
    Tool(
        name="memory_update",
        description="Update label and/or folder of an existing conversation.",
        input_schema=ToolInputSchema.json_schema(
            {
                "type": "object",
                "properties": {
                    "conversation_id": {"type": "string"},
                    "label": {"type": "string"},
                    "folder": {"type": "string"},
                },
                "required": ["conversation_id"],
            }
        ),
    ),
    Tool(
        name="memory_get_context",
        description="Assemble relevant context for a query from stored conversations.",
        input_schema=ToolInputSchema.json_schema(
            {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "context_budget": {"type": "integer", "default": 4000},
                    "preferred_labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": [],
                    },
                },
                "required": ["query"],
            }
        ),
    ),
    Tool(
        name="memory_prune",
        description="Get pruning suggestions for old or low-importance conversations.",
        input_schema=ToolInputSchema.json_schema(
            {
                "type": "object",
                "properties": {
                    "threshold_days": {"type": "integer", "default": 90},
                },
                "required": ["threshold_days"],
            }
        ),
    ),
    Tool(
        name="memory_query",
        description="Deprecated: general query over memory; uses the /api/v1/query endpoint.",
        input_schema=ToolInputSchema.json_schema(
            {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            }
        ),
    ),
]


@server.list_tools()
async def list_tools() -> List[Tool]:
    return TOOLS


# ================================
# Helper: HTTP client to controller
# ================================

async def controller_client() -> httpx.AsyncClient:
    """
    Create an HTTP client configured for the Rust controller.
    Uses bearer token from settings.mcp_api_key.
    """
    headers = {
        "Authorization": f"Bearer {settings.mcp_api_key}",
        "Content-Type": "application/json",
    }
    return httpx.AsyncClient(
        base_url=settings.controller_base_url,
        headers=headers,
        timeout=15.0,
    )


def _tool_result(data: Any) -> List[TextContent]:
    """
    Wrap raw JSON-serializable data into MCP TextContent.
    MCP tools return a list of content parts.
    """
    return [
        TextContent(
            type="text",
            text=json.dumps(data, ensure_ascii=False),
        )
    ]


# ================================
# Tool handlers
# ================================

@server.call_tool("memory_store")
async def tool_memory_store(args: Dict[str, Any]):
    """
    Forward to POST /api/v1/conversations
    Body: { label, folder, messages }
    """
    async with await controller_client() as client:
        resp = await client.post("/api/v1/conversations", json=args)
        resp.raise_for_status()
        data = resp.json()
    return _tool_result(data)


@server.call_tool("memory_search")
async def tool_memory_search(args: Dict[str, Any]):
    """
    Forward to POST /api/v1/query
    Body: { query, limit }
    """
    payload = {
        "query": args["query"],
        "limit": args.get("limit", 10),
    }
    async with await controller_client() as client:
        resp = await client.post("/api/v1/query", json=payload)
        resp.raise_for_status()
        data = resp.json()
    return _tool_result(data)


@server.call_tool("memory_update")
async def tool_memory_update(args: Dict[str, Any]):
    """
    Forward to PUT /api/v1/conversations/{id}/label
    Body: { label?, folder? }
    """
    conv_id = args["conversation_id"]
    body: Dict[str, Any] = {}
    if "label" in args:
        body["label"] = args["label"]
    if "folder" in args:
        body["folder"] = args["folder"]

    async with await controller_client() as client:
        resp = await client.put(f"/api/v1/conversations/{conv_id}/label", json=body)
        resp.raise_for_status()
        data = resp.json()
    return _tool_result(data)


@server.call_tool("memory_get_context")
async def tool_memory_get_context(args: Dict[str, Any]):
    """
    Forward to POST /api/v1/context/assemble
    Body: { query, preferred_labels, context_budget }
    """
    payload = {
        "query": args["query"],
        "preferred_labels": args.get("preferred_labels", []),
        "context_budget": args.get("context_budget", 4000),
    }
    async with await controller_client() as client:
        resp = await client.post("/api/v1/context/assemble", json=payload)
        resp.raise_for_status()
        data = resp.json()
    return _tool_result(data)


@server.call_tool("memory_prune")
async def tool_memory_prune(args: Dict[str, Any]):
    """
    Forward to POST /api/v1/prune/dry-run
    Body: { threshold_days }
    """
    payload = {
        "threshold_days": args.get("threshold_days", 90),
    }
    async with await controller_client() as client:
        resp = await client.post("/api/v1/prune/dry-run", json=payload)
        resp.raise_for_status()
        data = resp.json()
    return _tool_result(data)


@server.call_tool("memory_query")
async def tool_memory_query(args: Dict[str, Any]):
    """
    Deprecated alias of memory_search.
    Forward to POST /api/v1/query
    Body: { query, limit }
    """
    payload = {
        "query": args["query"],
        "limit": args.get("limit", 10),
    }
    async with await controller_client() as client:
        resp = await client.post("/api/v1/query", json=payload)
        resp.raise_for_status()
        data = resp.json()
    return _tool_result(data)


# ================================
# Entry points
# ================================

async def amain():
    await server.run_stdio()


def main():
    asyncio.run(amain())
