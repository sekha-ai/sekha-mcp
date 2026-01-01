"""Pydantic models for MCP tools and API interactions"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import enum


class MessageRole(str, enum.Enum):
    """Message role types"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """Single message in a conversation"""
    model_config = ConfigDict(from_attributes=True)
    
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @field_validator('metadata', mode='before')
    @classmethod
    def validate_metadata(cls, v):
        """Ensure metadata is always a dict"""
        if v is None:
            return {}
        return v


class ConversationInput(BaseModel):
    """Input for storing a conversation"""
    model_config = ConfigDict(from_attributes=True)
    
    label: str = Field(..., min_length=1, max_length=500)
    folder: str = Field(..., pattern=r'^\/[a-zA-Z0-9_\-\/]*$')
    messages: List[Message] = Field(..., min_length=1)
    importance_score: Optional[float] = Field(None, ge=0.0, le=10.0)

    @field_validator('messages')
    @classmethod
    def validate_messages(cls, v):
        """Ensure at least one message exists"""
        if not v or len(v) == 0:
            raise ValueError('At least one message is required')
        return v


# -- Classes expected by the Tools --
# These are the missing classes causing ImportError

class SearchInput(BaseModel):
    """Input for semantic search (used by memory_search tool)"""
    model_config = ConfigDict(from_attributes=True)
    
    query: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=100)
    filter_labels: Optional[List[str]] = None


class UpdateInput(BaseModel):
    """Input for updating conversation (used by memory_update tool)"""
    model_config = ConfigDict(from_attributes=True)
    
    conversation_id: str = Field(..., min_length=1)
    label: Optional[str] = Field(None, min_length=1, max_length=500)
    folder: Optional[str] = Field(None, pattern=r'^\/[a-zA-Z0-9_\-\/]*$')
    importance_score: Optional[float] = Field(None, ge=0.0, le=10.0)


class ContextInput(BaseModel):
    """Input for getting context (used by memory_get_context tool)"""
    model_config = ConfigDict(from_attributes=True)
    
    conversation_id: str = Field(..., min_length=1)


class PruneInput(BaseModel):
    """Input for pruning (used by memory_prune tool)"""
    model_config = ConfigDict(from_attributes=True)
    
    threshold_days: int = Field(default=30, ge=1)
    importance_threshold: Optional[float] = Field(None, ge=0.0, le=10.0)


# -- Alternative naming convention (API-level models) --
# These match the API endpoints and can be used for type hints

class MemorySearchRequest(SearchInput):
    """Alias for SearchInput for API consistency"""
    pass


class MemoryUpdateRequest(UpdateInput):
    """Alias for UpdateInput for API consistency"""
    pass


class ConversationContextRequest(ContextInput):
    """Alias for ContextInput for API consistency"""
    pass


class MemoryPruneRequest(PruneInput):
    """Alias for PruneInput for API consistency"""
    pass


class SekhaResponse(BaseModel):
    """Standard response format from Sekha Controller"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None


class PruneSuggestion(BaseModel):
    """Suggestion for conversation pruning"""
    model_config = ConfigDict(from_attributes=True)
    
    conversation_id: str
    label: str
    age_days: int
    importance_score: float
    reason: str


class SearchResult(BaseModel):
    """Search result from memory"""
    model_config = ConfigDict(from_attributes=True)
    
    conversation_id: str
    label: str
    folder: str
    content: str
    similarity: float
    created_at: Optional[datetime] = None