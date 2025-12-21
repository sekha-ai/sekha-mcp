"""HTTP client for Sekha Controller API"""

import httpx
import logging
from typing import Dict, Any, List, Optional

from config import settings

logger = logging.getLogger(__name__)


class SekhaClient:
    """Client for interacting with Sekha Controller (Rust core)"""
    
    def __init__(self):
        self.base_url = settings.controller_url
        self.api_key = settings.controller_api_key
        self.timeout = settings.request_timeout
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def store_conversation(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Store a new conversation"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/mcp/tools/memory_store",
                json=conversation,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def search_memory(
        self,
        query: str,
        limit: int = 10,
        filter_labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Search conversations semantically"""
        payload = {
            "query": query,
            "limit": limit
        }
        if filter_labels:
            payload["filter_labels"] = filter_labels
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/mcp/tools/memory_search",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def update_conversation(
        self,
        conversation_id: str,
        label: Optional[str] = None,
        folder: Optional[str] = None,
        importance_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """Update conversation metadata"""
        payload = {"conversation_id": conversation_id}
        
        if label is not None:
            payload["label"] = label
        if folder is not None:
            payload["folder"] = folder
        if importance_score is not None:
            payload["importance_score"] = importance_score
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/mcp/tools/memory_update",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get_context(self, conversation_id: str) -> Dict[str, Any]:
        """Get full conversation context"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/mcp/tools/memory_get_context",
                json={"conversation_id": conversation_id},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def prune_memory(
        self,
        threshold_days: int = 30,
        importance_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """Get pruning suggestions"""
        payload = {"threshold_days": threshold_days}
        
        if importance_threshold is not None:
            payload["importance_threshold"] = importance_threshold
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/mcp/tools/memory_prune",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def query_memory(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Legacy query endpoint (deprecated, use memory_search)"""
        return await self.search_memory(query, limit)


# Global client instance
sekha_client = SekhaClient()
