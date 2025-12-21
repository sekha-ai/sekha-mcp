"""Pydantic models for MCP tools"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Message(BaseModel):
    """Message in a conversation"""
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(None, description="Message timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ConversationInput(BaseModel):
    """Input for storing a conversation"""
    label: str = Field(..., description="Conversation label/title")
    folder: str = Field(..., description="Folder path (e.g., /projects/sekha)")
    messages: List[Message] = Field(..., description="List of messages")
    importance_score: Optional[float] = Field(None, description="Importance score (1-10)")


class SearchInput(BaseModel):
    """Input for searching memory"""
    query: str = Field(..., description="Search query")
    limit: int = Field(10, description="Maximum results to return")
    filter_labels: Optional[List[str]] = Field(None, description="Filter by labels")


class UpdateInput(BaseModel):
    """Input for updating conversation"""
    conversation_id: str = Field(..., description="Conversation UUID")
    label: Optional[str] = Field(None, description="New label")
    folder: Optional[str] = Field(None, description="New folder")
    importance_score: Optional[float] = Field(None, description="New importance score")


class ContextInput(BaseModel):
    """Input for getting conversation context"""
    conversation_id: str = Field(..., description="Conversation UUID")


class PruneInput(BaseModel):
    """Input for pruning suggestions"""
    threshold_days: int = Field(30, description="Age threshold in days")
    importance_threshold: Optional[float] = Field(None, description="Minimum importance to keep")


class QueryInput(BaseModel):
    """Legacy query input (deprecated)"""
    query: str = Field(..., description="Search query")
    limit: int = Field(10, description="Maximum results")
