"""
API request schemas.

Defines Pydantic models for incoming API requests.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from .user import EducationLevel, LearningPurpose


class UserProfileRequest(BaseModel):
    """Request to create a user profile."""

    name: str = Field(..., min_length=1, max_length=100, description="User's name")
    age: int = Field(..., ge=5, le=100, description="User's age")
    education_level: EducationLevel = Field(
        ..., description="User's education level"
    )
    subject: str = Field(..., min_length=1, max_length=200, description="Subject to learn")
    purpose: LearningPurpose = Field(..., description="Learning purpose")

    @validator("name")
    def validate_name(cls, v):
        """Validate name."""
        if not v.replace(" ", "").replace("-", "").isalnum():
            raise ValueError("Name must contain only alphanumeric characters")
        return v.strip()

    class Config:
        """Pydantic config."""

        use_enum_values = False


class UserMessageRequest(BaseModel):
    """Request to send a user message."""

    session_id: str = Field(..., min_length=1, description="Session identifier")
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    use_hint: bool = Field(default=False, description="Whether to use a hint")

    @validator("message")
    def validate_message(cls, v):
        """Validate message is not just whitespace."""
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()


class HintRequest(BaseModel):
    """Request to use a hint."""

    session_id: str = Field(..., min_length=1, description="Session identifier")
    challenge_id: str = Field(..., min_length=1, description="Challenge identifier")
