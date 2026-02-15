"""
Message and challenge schemas.

Defines data models for chat messages and learning challenges.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message roles."""

    USER = "user"
    ASSISTANT = "assistant"


class DifficultyLevel(str, Enum):
    """Challenge difficulty levels."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Message(BaseModel):
    """Chat message."""

    role: MessageRole = Field(..., description="Message role")
    content: str = Field(..., min_length=1, description="Message content")
    agent_type: Optional[str] = Field(None, description="Type of agent (if assistant)")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        """Pydantic config."""

        use_enum_values = False


class Challenge(BaseModel):
    """Learning challenge."""

    challenge_id: str = Field(..., description="Unique challenge identifier")
    question: str = Field(..., min_length=1, description="Challenge question")
    correct_answer: str = Field(..., description="Correct answer")
    hint: str = Field(..., description="Hint for solving")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level")
    points_value: int = Field(default=10, ge=5, le=100, description="Points for completion")
    fun_fact: Optional[str] = Field(None, description="Fun fact related to the challenge")
    agent_type: str = Field(..., description="Type of agent that created the challenge")
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        """Pydantic config."""

        use_enum_values = False
