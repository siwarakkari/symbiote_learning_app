"""
API response schemas.

Defines Pydantic models for API responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class SessionResponse(BaseModel):
    """Response for session creation."""

    session_id: str = Field(..., description="Session identifier")
    user_profile: Dict[str, Any] = Field(..., description="User profile data")
    learning_path: Dict[str, Any] = Field(..., description="Learning path")
    welcome_message: str = Field(..., description="Welcome message")
    status: str = Field(..., description="Status message")


class MessageResponse(BaseModel):
    """Response for message processing."""

    session_id: str = Field(..., description="Session identifier")
    agent_response: Dict[str, Any] = Field(..., description="Agent response")
    points_summary: Dict[str, Any] = Field(..., description="Points summary")
    message_count: int = Field(..., ge=0, description="Total message count")
    status: str = Field(..., description="Status message")


class PointsResponse(BaseModel):
    """Response for points query."""

    session_id: str = Field(..., description="Session identifier")
    points_summary: Dict[str, Any] = Field(..., description="Points summary")
    points_history: List[Dict[str, Any]] = Field(..., description="Points history")


class HistoryResponse(BaseModel):
    """Response for history query."""

    session_id: str = Field(..., description="Session identifier")
    history_summary: Dict[str, Any] = Field(..., description="History summary")
    recommendations: Dict[str, Any] = Field(..., description="Learning recommendations")


class ErrorResponse(BaseModel):
    """Response for errors."""

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")
    timestamp: datetime = Field(default_factory=datetime.now)
