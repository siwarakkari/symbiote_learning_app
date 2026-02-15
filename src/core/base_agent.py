"""
Base agent interface and types.

Defines the contract that all agents must implement.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime


class AgentType(str, Enum):
    """Enumeration of available agent types."""

    TUTOR = "tutor"
    PEER = "peer"
    PROVOCATEUR = "provocateur"
    TEACHABLE = "teachable"


@dataclass
class AgentResponse:
    """Standardized response from an agent."""

    message: str
    agent_type: AgentType
    points_awarded: int = 0
    challenge: Optional[Dict[str, Any]] = None
    hint: Optional[str] = None
    joke: Optional[str] = None
    next_agent: Optional[AgentType] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "message": self.message,
            "agent_type": self.agent_type.value,
            "points_awarded": self.points_awarded,
            "challenge": self.challenge,
            "hint": self.hint,
            "joke": self.joke,
            "next_agent": self.next_agent.value if self.next_agent else None,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


class BaseAgent(ABC):
    """
    Abstract base class for all learning agents.

    Defines the interface that all agents must implement.
    """

    def __init__(self, agent_type: AgentType):
        """
        Initialize the agent.

        Args:
            agent_type: The type of agent being created.
        """
        self.agent_type = agent_type
        self.conversation_history: List[Dict[str, str]] = []

    @abstractmethod
    async def process_input(
        self, user_input: str, context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Process user input and generate a response.

        Args:
            user_input: The user's message or input.
            context: Contextual information about the user and session.

        Returns:
            AgentResponse: The agent's response with metadata.
        """
        pass

    @abstractmethod
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about the agent.

        Returns:
            Dictionary containing agent metadata.
        """
        pass

    def add_to_history(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.

        Args:
            role: The role of the speaker ('user' or 'assistant').
            content: The message content.
        """
        self.conversation_history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history.copy()

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.agent_type.value})"
