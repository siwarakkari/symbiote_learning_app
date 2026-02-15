"""
History Service - Manages learning history and performance tracking.

Tracks interactions, identifies weak/strong areas, and provides recommendations.
"""

from typing import Dict, List, Any
from datetime import datetime


class HistoryService:
    """Service for managing learning history and analytics."""

    def __init__(self):
        """Initialize the history service."""
        self.interaction_history: List[Dict[str, Any]] = []
        self.topic_performance: Dict[str, Dict[str, Any]] = {}
        self.weak_areas: List[str] = []
        self.strong_areas: List[str] = []

    def add_interaction(
        self,
        agent_type: str,
        topic: str,
        user_response: str,
        agent_response: str,
        points_earned: int,
        correct: bool = None,
    ) -> None:
        """
        Add an interaction to the history.

        Args:
            agent_type: Type of agent involved.
            topic: Topic of the interaction.
            user_response: User's response.
            agent_response: Agent's response.
            points_earned: Points earned.
            correct: Whether the response was correct.
        """
        interaction = {
            "agent_type": agent_type,
            "topic": topic,
            "user_response": user_response,
            "agent_response": agent_response,
            "points_earned": points_earned,
            "correct": correct,
            "timestamp": datetime.now().isoformat(),
        }

        self.interaction_history.append(interaction)
        self._update_topic_performance(topic, correct, points_earned)

    def _update_topic_performance(
        self, topic: str, correct: bool, points_earned: int
    ) -> None:
        """Update performance metrics for a topic."""
        if topic not in self.topic_performance:
            self.topic_performance[topic] = {
                "total_interactions": 0,
                "correct_responses": 0,
                "total_points": 0,
                "accuracy": 0.0,
            }

        self.topic_performance[topic]["total_interactions"] += 1
        if correct:
            self.topic_performance[topic]["correct_responses"] += 1
        self.topic_performance[topic]["total_points"] += points_earned

        # Calculate accuracy
        total = self.topic_performance[topic]["total_interactions"]
        correct_count = self.topic_performance[topic]["correct_responses"]
        self.topic_performance[topic]["accuracy"] = (
            (correct_count / total * 100) if total > 0 else 0
        )

    def identify_weak_areas(self, threshold: float = 50.0) -> List[str]:
        """
        Identify weak areas based on accuracy.

        Args:
            threshold: Accuracy threshold for weak areas.

        Returns:
            List of weak topics.
        """
        self.weak_areas = [
            topic
            for topic, perf in self.topic_performance.items()
            if perf["accuracy"] < threshold and perf["total_interactions"] >= 3
        ]
        return self.weak_areas

    def identify_strong_areas(self, threshold: float = 80.0) -> List[str]:
        """
        Identify strong areas based on accuracy.

        Args:
            threshold: Accuracy threshold for strong areas.

        Returns:
            List of strong topics.
        """
        self.strong_areas = [
            topic
            for topic, perf in self.topic_performance.items()
            if perf["accuracy"] >= threshold and perf["total_interactions"] >= 3
        ]
        return self.strong_areas

    def get_recommendations(self) -> Dict[str, Any]:
        """
        Get learning recommendations.

        Returns:
            Dictionary with recommendations.
        """
        weak = self.identify_weak_areas()
        strong = self.identify_strong_areas()

        return {
            "focus_on": weak,
            "doing_well_in": strong,
            "next_challenge": self._suggest_next_challenge(),
            "review_topics": self._suggest_review_topics(),
        }

    def _suggest_next_challenge(self) -> str:
        """Suggest next challenge."""
        if self.weak_areas:
            return f"Let's focus on {self.weak_areas[0]} to strengthen your understanding!"
        elif self.strong_areas:
            return f"You're doing great in {self.strong_areas[0]}! Ready for a harder challenge?"
        else:
            return "Keep learning! You're making progress!"

    def _suggest_review_topics(self) -> List[str]:
        """Suggest topics to review."""
        return self.weak_areas[:3]

    def get_summary(self) -> Dict[str, Any]:
        """
        Get history summary.

        Returns:
            Dictionary with history information.
        """
        return {
            "total_interactions": len(self.interaction_history),
            "topic_performance": self.topic_performance,
            "weak_areas": self.weak_areas,
            "strong_areas": self.strong_areas,
            "recent_interactions": (
                self.interaction_history[-5:] if self.interaction_history else []
            ),
        }

    def get_interaction_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get interaction history.

        Args:
            limit: Maximum number of interactions to return.

        Returns:
            Interaction history.
        """
        if limit:
            return self.interaction_history[-limit:]
        return self.interaction_history.copy()

    def reset(self) -> None:
        """Reset all history."""
        self.interaction_history = []
        self.topic_performance = {}
        self.weak_areas = []
        self.strong_areas = []
