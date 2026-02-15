"""
Agent Registry - Manages agent creation and registration.

Provides a centralized registry for all available agents, allowing
dynamic registration and instantiation of new agent types.
"""

from typing import Dict, Type, Callable, Optional, Any
from src.core import BaseAgent, AgentType, RegistryException


class AgentRegistry:
    """
    Central registry for managing agent classes and instances.

    This class implements the Registry pattern to allow:
    - Dynamic agent registration
    - Agent factory creation
    - Agent instance management
    - Easy extension with new agent types
    """

    def __init__(self):
        """Initialize the agent registry."""
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
        self._agent_factories: Dict[AgentType, Callable] = {}
        self._instances: Dict[str, BaseAgent] = {}

    def register_agent(
        self,
        agent_type: AgentType,
        agent_class: Type[BaseAgent],
        factory: Optional[Callable] = None,
    ) -> None:
        """
        Register a new agent type.

        Args:
            agent_type: The type of agent to register.
            agent_class: The class implementing the agent.
            factory: Optional factory function for custom instantiation.

        Raises:
            RegistryException: If agent type is already registered.
        """
        if agent_type in self._agent_classes:
            raise RegistryException(
                f"Agent type '{agent_type.value}' is already registered"
            )

        self._agent_classes[agent_type] = agent_class

        if factory:
            self._agent_factories[agent_type] = factory
        else:
            # Default factory: simple instantiation
            self._agent_factories[agent_type] = lambda: agent_class(agent_type)

    def unregister_agent(self, agent_type: AgentType) -> None:
        """
        Unregister an agent type.

        Args:
            agent_type: The type of agent to unregister.

        Raises:
            RegistryException: If agent type is not registered.
        """
        if agent_type not in self._agent_classes:
            raise RegistryException(
                f"Agent type '{agent_type.value}' is not registered"
            )

        del self._agent_classes[agent_type]
        del self._agent_factories[agent_type]

        # Remove instances of this type
        self._instances = {
            k: v
            for k, v in self._instances.items()
            if v.agent_type != agent_type
        }

    def create_agent(self, agent_type: AgentType, instance_id: str = None) -> BaseAgent:
        """
        Create an agent instance.

        Args:
            agent_type: The type of agent to create.
            instance_id: Optional identifier for the instance.

        Returns:
            An instance of the requested agent type.

        Raises:
            RegistryException: If agent type is not registered.
        """
        if agent_type not in self._agent_classes:
            raise RegistryException(
                f"Agent type '{agent_type.value}' is not registered"
            )

        factory = self._agent_factories[agent_type]
        agent = factory()

        if instance_id:
            self._instances[instance_id] = agent

        return agent

    def get_agent(self, instance_id: str) -> Optional[BaseAgent]:
        """
        Get a registered agent instance.

        Args:
            instance_id: The identifier of the agent instance.

        Returns:
            The agent instance or None if not found.
        """
        return self._instances.get(instance_id)

    def get_agent_class(self, agent_type: AgentType) -> Type[BaseAgent]:
        """
        Get the class for an agent type.

        Args:
            agent_type: The type of agent.

        Returns:
            The agent class.

        Raises:
            RegistryException: If agent type is not registered.
        """
        if agent_type not in self._agent_classes:
            raise RegistryException(
                f"Agent type '{agent_type.value}' is not registered"
            )

        return self._agent_classes[agent_type]

    def is_registered(self, agent_type: AgentType) -> bool:
        """
        Check if an agent type is registered.

        Args:
            agent_type: The type of agent.

        Returns:
            True if registered, False otherwise.
        """
        return agent_type in self._agent_classes

    def get_all_registered_types(self) -> list[AgentType]:
        """
        Get all registered agent types.

        Returns:
            List of registered agent types.
        """
        return list(self._agent_classes.keys())

    def get_all_instances(self) -> Dict[str, BaseAgent]:
        """
        Get all registered agent instances.

        Returns:
            Dictionary of instance_id -> agent.
        """
        return self._instances.copy()

    def clear_instances(self) -> None:
        """Clear all agent instances."""
        self._instances.clear()

    def get_registry_info(self) -> Dict[str, Any]:
        """
        Get information about the registry.

        Returns:
            Dictionary containing registry statistics.
        """
        return {
            "registered_types": [t.value for t in self.get_all_registered_types()],
            "total_types": len(self._agent_classes),
            "total_instances": len(self._instances),
            "instances": list(self._instances.keys()),
        }


# Global registry instance
_global_registry = AgentRegistry()


def get_registry() -> AgentRegistry:
    """Get the global agent registry."""
    return _global_registry


def register_default_agents() -> None:
    """Register all default agents."""
    from .base_implementations import (
        SocraticTutorAgent,
        VirtualPeerAgent,
        ProvocateurAgent,
        TeachableAgent,
    )

    registry = get_registry()

    registry.register_agent(AgentType.TUTOR, SocraticTutorAgent)
    registry.register_agent(AgentType.PEER, VirtualPeerAgent)
    registry.register_agent(AgentType.PROVOCATEUR, ProvocateurAgent)
    registry.register_agent(AgentType.TEACHABLE, TeachableAgent)
