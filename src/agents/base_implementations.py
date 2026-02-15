"""
Base agent implementations.

Provides concrete implementations of the four main learning agents:
- Socratic Tutor
- Virtual Peer
- Provocateur
- Teachable Agent
"""

import random
from typing import Dict, Any
from src.core import BaseAgent, AgentType, AgentResponse


class SocraticTutorAgent(BaseAgent):
    """
    Socratic Tutor Agent.

    Guides learning through thoughtful questions and manages the learning path.
    """

    def __init__(self, agent_type: AgentType = AgentType.TUTOR):
        """Initialize the Socratic Tutor Agent."""
        super().__init__(agent_type)
        self.questions_asked = 0
        self.learning_phases = ["exploration", "construction", "creation"]
        self.current_phase = 0

    async def process_input(
        self, user_input: str, context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Process user input with Socratic method.

        Args:
            user_input: The user's response.
            context: Contextual information.

        Returns:
            AgentResponse with Socratic question.
        """
        self.add_to_history("user", user_input)

        # Generate Socratic question (simplified - would use LLM in production)
        message = self._generate_socratic_question(user_input, context)

        response = AgentResponse(
            message=message,
            agent_type=self.agent_type,
            points_awarded=5,
            metadata={
                "phase": self.learning_phases[self.current_phase],
                "questions_asked": self.questions_asked,
            },
        )

        self.add_to_history("assistant", message)
        self.questions_asked += 1

        return response

    def _generate_socratic_question(
        self, user_input: str, context: Dict[str, Any]
    ) -> str:
        """Generate a Socratic question based on user input."""
        questions = [
            "Why do you think that is the case?",
            "Can you provide an example to support your answer?",
            "What would happen if we approached this differently?",
            "How does this relate to what we learned earlier?",
            "What assumptions are you making here?",
        ]
        return random.choice(questions)

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "name": "Socratic Tutor",
            "type": self.agent_type.value,
            "description": "Guides learning through thoughtful questions",
            "phase": self.learning_phases[self.current_phase],
            "questions_asked": self.questions_asked,
        }


class VirtualPeerAgent(BaseAgent):
    """
    Virtual Peer Agent.

    Collaborates with the learner and occasionally makes intentional mistakes.
    """

    def __init__(self, agent_type: AgentType = AgentType.PEER):
        """Initialize the Virtual Peer Agent."""
        super().__init__(agent_type)
        self.error_injection_rate = 0.3  # 30% chance of intentional error

    async def process_input(
        self, user_input: str, context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Process user input as a collaborative peer.

        Args:
            user_input: The user's message.
            context: Contextual information.

        Returns:
            AgentResponse with peer collaboration.
        """
        self.add_to_history("user", user_input)

        # Decide whether to make an intentional error
        should_error = random.random() < self.error_injection_rate

        if should_error:
            message = self._generate_peer_error_response(user_input, context)
            points = 10  # More points for catching errors
        else:
            message = self._generate_peer_agreement_response(user_input, context)
            points = 5

        response = AgentResponse(
            message=message,
            agent_type=self.agent_type,
            points_awarded=points,
            metadata={"intentional_error": should_error},
        )

        self.add_to_history("assistant", message)

        return response

    def _generate_peer_error_response(
        self, user_input: str, context: Dict[str, Any]
    ) -> str:
        """Generate a response with an intentional error."""
        errors = [
            "I think we should approach this by ignoring the context entirely.",
            "That's interesting, but I believe the opposite is actually true.",
            "I'm pretty sure that contradicts what we learned earlier.",
        ]
        return random.choice(errors)

    def _generate_peer_agreement_response(
        self, user_input: str, context: Dict[str, Any]
    ) -> str:
        """Generate a collaborative agreement response."""
        agreements = [
            "That's a great point! I hadn't thought about it that way.",
            "I completely agree with your reasoning.",
            "You're building on that concept really well!",
        ]
        return random.choice(agreements)

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "name": "Virtual Peer",
            "type": self.agent_type.value,
            "description": "Collaborates and occasionally makes intentional mistakes",
            "error_injection_rate": self.error_injection_rate,
        }


class ProvocateurAgent(BaseAgent):
    """
    Provocateur Agent.

    Challenges the learner with games, scenarios, and thought-provoking questions.
    """

    def __init__(self, agent_type: AgentType = AgentType.PROVOCATEUR):
        """Initialize the Provocateur Agent."""
        super().__init__(agent_type)
        self.challenges_created = 0

    async def process_input(
        self, user_input: str, context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Process user input and create a challenge.

        Args:
            user_input: The user's message.
            context: Contextual information.

        Returns:
            AgentResponse with a challenge.
        """
        self.add_to_history("user", user_input)

        message = self._generate_challenge_prompt()
        challenge = self._create_challenge(context)

        response = AgentResponse(
            message=message,
            agent_type=self.agent_type,
            challenge=challenge,
            points_awarded=0,  # Points awarded when challenge is completed
            joke=self._generate_joke(),
            metadata={"challenge_id": challenge.get("challenge_id")},
        )

        self.add_to_history("assistant", message)
        self.challenges_created += 1

        return response

    def _generate_challenge_prompt(self) -> str:
        """Generate a challenge prompt."""
        prompts = [
            "Ready for a real-world scenario? Here's your challenge:",
            "Let's put your knowledge to the test with this scenario:",
            "I've got an interesting challenge for you:",
        ]
        return random.choice(prompts)

    def _create_challenge(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a challenge."""
        return {
            "challenge_id": f"challenge_{self.challenges_created}",
            "question": "How would you solve this real-world problem?",
            "difficulty": "medium",
            "points_value": 20,
            "hint": "Think about the core principles involved.",
        }

    def _generate_joke(self) -> str:
        """Generate a funny joke."""
        jokes = [
            "Why did the learner bring a ladder to class? Because they wanted to take their learning to the next level! 😄",
            "What did the AI say to the learner? 'You're processing well!' 🤖",
            "Why do programmers make good students? Because they know how to debug their thinking! 🐛",
        ]
        return random.choice(jokes)

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "name": "Provocateur",
            "type": self.agent_type.value,
            "description": "Challenges with games and real-world scenarios",
            "challenges_created": self.challenges_created,
        }


class TeachableAgent(BaseAgent):
    """
    Teachable Agent.

    Learns from the user to reinforce their understanding.
    """

    def __init__(self, agent_type: AgentType = AgentType.TEACHABLE):
        """Initialize the Teachable Agent."""
        super().__init__(agent_type)
        self.understanding_level = 0  # 0-100

    async def process_input(
        self, user_input: str, context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Process user input as a student being taught.

        Args:
            user_input: The user's explanation.
            context: Contextual information.

        Returns:
            AgentResponse evaluating the teaching.
        """
        self.add_to_history("user", user_input)

        # Evaluate the teaching quality
        understanding_gain = self._evaluate_teaching(user_input)
        self.understanding_level = min(100, self.understanding_level + understanding_gain)

        message = self._generate_learning_response(understanding_gain)

        response = AgentResponse(
            message=message,
            agent_type=self.agent_type,
            points_awarded=15 + understanding_gain,  # Bonus points for good teaching
            metadata={"understanding_level": self.understanding_level},
        )

        self.add_to_history("assistant", message)

        return response

    def _evaluate_teaching(self, user_input: str) -> int:
        """Evaluate the quality of the teaching."""
        # Simplified evaluation - would use LLM in production
        if len(user_input) > 100:
            return 10
        elif len(user_input) > 50:
            return 5
        else:
            return 2

    def _generate_learning_response(self, understanding_gain: int) -> str:
        """Generate a response showing the agent is learning."""
        if understanding_gain > 8:
            return "Wow! That explanation really helped me understand this concept better!"
        elif understanding_gain > 5:
            return "Thanks for explaining that. I'm starting to get it now."
        else:
            return "I'm learning, but could you provide more details?"

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "name": "Teachable Agent",
            "type": self.agent_type.value,
            "description": "Learns from the user to reinforce their understanding",
            "understanding_level": self.understanding_level,
        }
