"""
Session Service - Manages user learning sessions.

Handles session creation, retrieval, and lifecycle management.
"""

from typing import Dict, Optional, Any
from datetime import datetime
from src.schemas import UserProfile, UserSession, Message
from src.core import SessionException


class SessionService:
    """Service for managing learning sessions."""

    def __init__(self):
        """Initialize the session service."""
        self.sessions: Dict[str, UserSession] = {}

    def create_session(self, user_profile: UserProfile) -> UserSession:
        """
        Create a new learning session.

        Args:
            user_profile: User profile information.

        Returns:
            Created session.

        Raises:
            SessionException: If session creation fails.
        """
        try:
            session_id = f"{user_profile.name}_{datetime.now().timestamp()}"

            session = UserSession(
                session_id=session_id,
                user_profile=user_profile,
                learning_path={
                    "phases": [
                        "exploration",
                        "construction",
                        "creation",
                    ],
                    "current_phase": 0,
                },
            )

            self.sessions[session_id] = session
            return session

        except Exception as e:
            raise SessionException(f"Failed to create session: {str(e)}")

    def get_session(self, session_id: str) -> Optional[UserSession]:
        """
        Get a session by ID.

        Args:
            session_id: Session identifier.

        Returns:
            Session or None if not found.
        """
        return self.sessions.get(session_id)

    def get_session_or_raise(self, session_id: str) -> UserSession:
        """
        Get a session or raise an exception.

        Args:
            session_id: Session identifier.

        Returns:
            Session.

        Raises:
            SessionException: If session not found.
        """
        session = self.get_session(session_id)
        if not session:
            raise SessionException(f"Session '{session_id}' not found", session_id)
        return session

    def update_session(self, session_id: str, **kwargs) -> UserSession:
        """
        Update session attributes.

        Args:
            session_id: Session identifier.
            **kwargs: Attributes to update.

        Returns:
            Updated session.

        Raises:
            SessionException: If session not found.
        """
        session = self.get_session_or_raise(session_id)

        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)

        session.last_activity = datetime.now()
        return session

    def add_message(self, session_id: str, message: Message) -> UserSession:
        """
        Add a message to session.

        Args:
            session_id: Session identifier.
            message: Message to add.

        Returns:
            Updated session.

        Raises:
            SessionException: If session not found.
        """
        session = self.get_session_or_raise(session_id)
        # Note: In a real implementation, you'd store messages in the session
        session.last_activity = datetime.now()
        return session

    def close_session(self, session_id: str) -> None:
        """
        Close a session.

        Args:
            session_id: Session identifier.

        Raises:
            SessionException: If session not found.
        """
        session = self.get_session_or_raise(session_id)
        session.is_active = False
        session.last_activity = datetime.now()

    def delete_session(self, session_id: str) -> None:
        """
        Delete a session.

        Args:
            session_id: Session identifier.

        Raises:
            SessionException: If session not found.
        """
        if session_id not in self.sessions:
            raise SessionException(f"Session '{session_id}' not found", session_id)

        del self.sessions[session_id]

    def get_all_sessions(self) -> Dict[str, UserSession]:
        """
        Get all sessions.

        Returns:
            Dictionary of all sessions.
        """
        return self.sessions.copy()

    def get_active_sessions(self) -> Dict[str, UserSession]:
        """
        Get all active sessions.

        Returns:
            Dictionary of active sessions.
        """
        return {
            session_id: session
            for session_id, session in self.sessions.items()
            if session.is_active
        }

    def cleanup_inactive_sessions(self, timeout_minutes: int = 30) -> int:
        """
        Clean up inactive sessions.

        Args:
            timeout_minutes: Inactivity timeout in minutes.

        Returns:
            Number of sessions cleaned up.
        """
        now = datetime.now()
        sessions_to_delete = []

        for session_id, session in self.sessions.items():
            if session.is_active:
                inactive_time = (now - session.last_activity).total_seconds() / 60
                if inactive_time > timeout_minutes:
                    sessions_to_delete.append(session_id)

        for session_id in sessions_to_delete:
            self.delete_session(session_id)

        return len(sessions_to_delete)

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """
        Get session information.

        Args:
            session_id: Session identifier.

        Returns:
            Session information.

        Raises:
            SessionException: If session not found.
        """
        session = self.get_session_or_raise(session_id)

        return {
            "session_id": session.session_id,
            "user_name": session.user_profile.name,
            "subject": session.user_profile.subject,
            "current_phase": session.current_phase,
            "current_points": session.current_points,
            "total_points": session.total_points,
            "is_active": session.is_active,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
        }
