"""
Session routes - Endpoints for session management.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.schemas import UserProfileRequest, SessionResponse
from src.services import SessionService
from src.core import SessionException

router = APIRouter()

# Dependency injection
def get_session_service() -> SessionService:
    """Get session service instance."""
    return SessionService()


@router.post("/create", response_model=SessionResponse)
async def create_session(
    profile_request: UserProfileRequest,
    session_service: SessionService = Depends(get_session_service),
) -> Dict[str, Any]:
    """
    Create a new learning session.

    Args:
        profile_request: User profile information.
        session_service: Session service instance.

    Returns:
        Session creation response.
    """
    try:
        from src.schemas import UserProfile

        user_profile = UserProfile(**profile_request.dict())
        session = session_service.create_session(user_profile)

        return {
            "session_id": session.session_id,
            "user_profile": user_profile.dict(),
            "learning_path": session.learning_path,
            "welcome_message": f"Welcome, {user_profile.name}! Let's start your learning journey.",
            "status": "Session created successfully",
        }

    except SessionException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{session_id}")
async def get_session(
    session_id: str,
    session_service: SessionService = Depends(get_session_service),
) -> Dict[str, Any]:
    """
    Get session information.

    Args:
        session_id: Session identifier.
        session_service: Session service instance.

    Returns:
        Session information.
    """
    try:
        return session_service.get_session_info(session_id)
    except SessionException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{session_id}")
async def close_session(
    session_id: str,
    session_service: SessionService = Depends(get_session_service),
) -> Dict[str, str]:
    """
    Close a session.

    Args:
        session_id: Session identifier.
        session_service: Session service instance.

    Returns:
        Status message.
    """
    try:
        session_service.close_session(session_id)
        return {"status": "Session closed successfully"}
    except SessionException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
