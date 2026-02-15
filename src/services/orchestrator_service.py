"""
Orchestrator Service - Manages multi-agent coordination.

Handles agent selection, routing, and coordination of multi-agent interactions.
"""

from typing import Dict, Any, Optional
from src.core import BaseAgent, AgentType, AgentResponse
from src.agents import AgentRegistry
from src.schemas import UserProfile


class OrchestratorService:
    """Service for orchestrating multi-agent interactions."""

    def __init__(self, user_profile: UserProfile, registry: AgentRegistry):
        """
        Initialize the orchestrator.

        Args:
            user_profile: User profile for context.
            registry: Agent registry for agent management.
        """
        self.user_profile = user_profile
        self.registry = registry
        self.agents: Dict[AgentType, BaseAgent] = {}
        self.conversation_count = 0
        self.last_agent_type: Optional[AgentType] = None

        # Initialize all agents
        self._initialize_agents()

    def _initialize_agents(self) -> None:
        """Initialize all available agents."""
        for agent_type in self.registry.get_all_registered_types():
            try:
                agent = self.registry.create_agent(agent_type)
                self.agents[agent_type] = agent
            except Exception as e:
                print(f"Failed to initialize agent {agent_type.value}: {str(e)}")

    async def process_user_input(self, user_input: str) -> AgentResponse:
        """
        Process user input and route to appropriate agent.

        Args:
            user_input: User's message.

        Returns:
            Agent response.
        """
        self.conversation_count += 1

        # Decide which agent should handle this
        agent_type = self._decide_next_agent(user_input)

        # Get the agent
        agent = self.agents.get(agent_type)
        if not agent:
            raise ValueError(f"Agent {agent_type.value} not found")

        # Create context
        context = self._create_context(user_input)

        # Process with agent
        response = await agent.process_input(user_input, context)

        # Update last agent
        self.last_agent_type = agent_type

        return response

    def _decide_next_agent(self, user_input: str) -> AgentType:
        """
        Decide which agent should handle the input.

        Args:
            user_input: User's message.

        Returns:
            Agent type to use.
        """
        # Simple routing logic - can be enhanced with ML
        user_input_lower = user_input.lower()

        # Check for specific triggers
        if any(word in user_input_lower for word in ["why", "how", "explain"]):
            return AgentType.TUTOR

        if any(word in user_input_lower for word in ["challenge", "game", "scenario"]):
            return AgentType.PROVOCATEUR

        if any(word in user_input_lower for word in ["teach", "explain to", "help me"]):
            return AgentType.TEACHABLE

        # Default routing based on conversation count
        if self.conversation_count % 4 == 0:
            return AgentType.PEER
        elif self.conversation_count % 4 == 1:
            return AgentType.PROVOCATEUR
        elif self.conversation_count % 4 == 2:
            return AgentType.TEACHABLE
        else:
            return AgentType.TUTOR

    def _create_context(self, user_input: str) -> Dict[str, Any]:
        """
        Create context for agent processing.

        Args:
            user_input: User's message.

        Returns:
            Context dictionary.
        """
        return {
            "user_profile": {
                "name": self.user_profile.name,
                "age": self.user_profile.age,
                "education_level": self.user_profile.education_level.value,
                "subject": self.user_profile.subject,
                "purpose": self.user_profile.purpose.value,
            },
            "conversation_count": self.conversation_count,
            "last_agent": self.last_agent_type.value if self.last_agent_type else None,
            "user_input": user_input,
        }

    def get_agent(self, agent_type: AgentType) -> Optional[BaseAgent]:
        """
        Get an agent by type.

        Args:
            agent_type: Type of agent.

        Returns:
            Agent or None if not found.
        """
        return self.agents.get(agent_type)

    def get_all_agents_info(self) -> Dict[str, Any]:
        """
        Get information about all agents.

        Returns:
            Dictionary with agent information.
        """
        return {
            agent_type.value: agent.get_agent_info()
            for agent_type, agent in self.agents.items()
        }

    def get_orchestrator_info(self) -> Dict[str, Any]:
        """
        Get orchestrator information.

        Returns:
            Dictionary with orchestrator information.
        """
        return {
            "conversation_count": self.conversation_count,
            "last_agent": self.last_agent_type.value if self.last_agent_type else None,
            "active_agents": len(self.agents),
            "agents": list(self.agents.keys()),
        }
