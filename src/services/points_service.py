"""
Points Service - Manages the dynamic point system.

Handles point calculation, multipliers, penalties, and level progression.
"""

from typing import Dict, List, Any
from datetime import datetime


class PointsService:
    """Service for managing user points and gamification."""

    def __init__(self):
        """Initialize the points service."""
        self.current_points = 0
        self.total_points = 0
        self.points_history: List[Dict[str, Any]] = []

        # Point multipliers for different actions
        self.multipliers = {
            "curiosity": 1.5,  # Asking pertinent questions
            "critical_thinking": 2.0,  # Identifying errors
            "collaboration": 1.3,  # Constructive contributions
            "teaching": 2.5,  # Teaching the agent
            "challenge_completion": 3.0,  # Completing challenges
            "hint_penalty": 0.7,  # Hint usage penalty
        }

    def award_points(
        self, action_type: str, base_points: int, metadata: Dict[str, Any] = None
    ) -> int:
        """
        Award points based on action type.

        Args:
            action_type: Type of action performed.
            base_points: Base points for the action.
            metadata: Additional metadata about the action.

        Returns:
            Points actually awarded.
        """
        multiplier = self.multipliers.get(action_type, 1.0)
        points_earned = int(base_points * multiplier)

        self.current_points += points_earned
        self.total_points += points_earned

        self.points_history.append(
            {
                "action": action_type,
                "base_points": base_points,
                "multiplier": multiplier,
                "points_earned": points_earned,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {},
            }
        )

        return points_earned

    def penalize_points(self, reason: str, points_to_deduct: int) -> int:
        """
        Penalize points.

        Args:
            reason: Reason for penalty.
            points_to_deduct: Points to deduct.

        Returns:
            Points actually deducted.
        """
        deducted = min(points_to_deduct, self.current_points)
        self.current_points -= deducted

        self.points_history.append(
            {
                "action": "penalty",
                "reason": reason,
                "points_deducted": deducted,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return deducted

    def use_hint(self) -> int:
        """
        Use a hint (applies point penalty).

        Returns:
            Points deducted.
        """
        penalty = max(1, int(self.current_points * 0.1))  # 10% penalty
        self.penalize_points("hint_used", penalty)
        return penalty

    def get_current_level(self) -> int:
        """
        Calculate current level based on total points.

        Returns:
            Current level.
        """
        return (self.total_points // 100) + 1

    def get_next_level_threshold(self) -> int:
        """
        Get points needed for next level.

        Returns:
            Points threshold for next level.
        """
        current_level = self.get_current_level()
        return current_level * 100

    def get_progress_percentage(self) -> float:
        """
        Get progress percentage to next level.

        Returns:
            Progress percentage (0-100).
        """
        current_level = self.get_current_level()
        current_threshold = (current_level - 1) * 100
        next_threshold = current_level * 100

        if next_threshold == current_threshold:
            return 0.0

        progress = (
            (self.total_points - current_threshold)
            / (next_threshold - current_threshold)
        ) * 100

        return min(100.0, max(0.0, progress))

    def get_summary(self) -> Dict[str, Any]:
        """
        Get points summary.

        Returns:
            Dictionary with points information.
        """
        return {
            "current_points": self.current_points,
            "total_points": self.total_points,
            "level": self.get_current_level(),
            "next_level_points": self.get_next_level_threshold(),
            "progress_to_next_level": self.get_progress_percentage(),
        }

    def get_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get points history.

        Args:
            limit: Maximum number of entries to return.

        Returns:
            Points history.
        """
        if limit:
            return self.points_history[-limit:]
        return self.points_history.copy()

    def reset(self) -> None:
        """Reset all points."""
        self.current_points = 0
        self.total_points = 0
        self.points_history = []
