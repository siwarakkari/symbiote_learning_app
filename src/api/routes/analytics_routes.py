"""
Analytics routes - Endpoints for learning analytics and statistics.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.schemas import PointsResponse, HistoryResponse
from src.services import SessionService, PointsService, HistoryService
from src.core import SessionException

router = APIRouter()


def get_services():
    """Get service instances."""
    return {
        "session_service": SessionService(),
        "points_service": PointsService(),
        "history_service": HistoryService(),
    }


@router.get("/points/{session_id}", response_model=PointsResponse)
async def get_points(
    session_id: str,
    services: Dict[str, Any] = Depends(get_services),
) -> Dict[str, Any]:
    """
    Get points summary for a session.

    Args:
        session_id: Session identifier.
        services: Service instances.

    Returns:
        Points summary and history.
    """
    try:
        session_service = services["session_service"]
        points_service = services["points_service"]

        # Verify session exists
        session_service.get_session_or_raise(session_id)

        return {
            "session_id": session_id,
            "points_summary": points_service.get_summary(),
            "points_history": points_service.get_history(limit=10),
        }

    except SessionException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(
    session_id: str,
    services: Dict[str, Any] = Depends(get_services),
) -> Dict[str, Any]:
    """
    Get learning history and recommendations.

    Args:
        session_id: Session identifier.
        services: Service instances.

    Returns:
        History summary and recommendations.
    """
    try:
        session_service = services["session_service"]
        history_service = services["history_service"]

        # Verify session exists
        session_service.get_session_or_raise(session_id)

        return {
            "session_id": session_id,
            "history_summary": history_service.get_summary(),
            "recommendations": history_service.get_recommendations(),
        }

    except SessionException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/performance/{session_id}")
async def get_performance(
    session_id: str,
    services: Dict[str, Any] = Depends(get_services),
) -> Dict[str, Any]:
    """
    Get detailed performance metrics.

    Args:
        session_id: Session identifier.
        services: Service instances.

    Returns:
        Performance metrics.
    """
    try:
        session_service = services["session_service"]
        history_service = services["history_service"]

        session = session_service.get_session_or_raise(session_id)

        return {
            "session_id": session_id,
            "user_name": session.user_profile.name,
            "subject": session.user_profile.subject,
            "topic_performance": history_service.topic_performance,
            "weak_areas": history_service.identify_weak_areas(),
            "strong_areas": history_service.identify_strong_areas(),
            "total_interactions": len(history_service.interaction_history),
        }

    except SessionException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
