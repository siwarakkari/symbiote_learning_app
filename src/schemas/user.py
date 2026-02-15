"""
User and session schemas.

Defines data models for user profiles and learning sessions.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class EducationLevel(str, Enum):
    """User education levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class LearningPurpose(str, Enum):
    """User learning purposes."""

    LEARN = "learn"
    TEST_KNOWLEDGE = "test_knowledge"


class UserProfile(BaseModel):
    """User profile information."""

    name: str = Field(..., min_length=1, max_length=100, description="User's name")
    age: int = Field(..., ge=5, le=100, description="User's age")
    education_level: EducationLevel = Field(
        ..., description="User's education level in the subject"
    )
    subject: str = Field(..., min_length=1, max_length=200, description="Subject of interest")
    purpose: LearningPurpose = Field(..., description="Learning purpose")
    created_at: datetime = Field(default_factory=datetime.now)

    @validator("name")
    def validate_name(cls, v):
        """Validate name contains only valid characters."""
        if not v.replace(" ", "").replace("-", "").isalnum():
            raise ValueError("Name must contain only alphanumeric characters, spaces, or hyphens")
        return v.strip()

    class Config:
        """Pydantic config."""

        use_enum_values = False


class UserSession(BaseModel):
    """User learning session."""

    session_id: str = Field(..., description="Unique session identifier")
    user_profile: UserProfile = Field(..., description="User profile")
    current_phase: str = Field(default="exploration", description="Current learning phase")
    current_points: int = Field(default=0, ge=0, description="Points in current session")
    total_points: int = Field(default=0, ge=0, description="Total points earned")
    learning_path: Dict[str, Any] = Field(default_factory=dict, description="Learning path")
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)

    class Config:
        """Pydantic config."""

        use_enum_values = False
