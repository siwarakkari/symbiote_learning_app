"""
Chat routes - Endpoints for chat and message handling.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.schemas import UserMessageRequest, HintRequest, MessageResponse
from src.services import (
    SessionService,
    OrchestratorService,
    PointsService,
    HistoryService,
)
from src.agents import AgentRegistry, register_default_agents
from src.core import SessionException, AgentException

router = APIRouter()

# Initialize registry
register_default_agents()


def get_services():
    """Get service instances."""
    return {
        "session_service": SessionService(),
        "agent_registry": AgentRegistry(),
        "points_service": PointsService(),
        "history_service": HistoryService(),
    }


@router.post("/message", response_model=MessageResponse)
async def send_message(
    message_request: UserMessageRequest,
    services: Dict[str, Any] = Depends(get_services),
) -> Dict[str, Any]:
    """
    Send a message and receive agent response.

    Args:
        message_request: Message and session information.
        services: Service instances.

    Returns:
        Agent response with points update.
    """
    try:
        session_service = services["session_service"]
        agent_registry = services["agent_registry"]
        points_service = services["points_service"]
        history_service = services["history_service"]

        # Get session
        session = session_service.get_session_or_raise(message_request.session_id)

        # Create orchestrator
        orchestrator = OrchestratorService(session.user_profile, agent_registry)

        # Process message
        agent_response = await orchestrator.process_user_input(message_request.message)

        # Award points
        if agent_response.points_awarded > 0:
            points_earned = points_service.award_points(
                action_type="collaboration",
                base_points=agent_response.points_awarded,
            )
        else:
            points_earned = 0

        # Handle hint penalty
        if message_request.use_hint:
            penalty = points_service.use_hint()
            agent_response.metadata["hint_penalty"] = penalty

        # Update history
        history_service.add_interaction(
            agent_type=agent_response.agent_type.value,
            topic=session.user_profile.subject,
            user_response=message_request.message,
            agent_response=agent_response.message,
            points_earned=points_earned,
        )

        return {
            "session_id": message_request.session_id,
            "agent_response": agent_response.to_dict(),
            "points_summary": points_service.get_summary(),
            "message_count": 1,  # Would increment from session
            "status": "Message processed successfully",
        }

    except SessionException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/hint")
async def request_hint(
    hint_request: HintRequest,
    services: Dict[str, Any] = Depends(get_services),
) -> Dict[str, Any]:
    """
    Request a hint for a challenge.

    Args:
        hint_request: Hint request information.
        services: Service instances.

    Returns:
        Hint with point penalty.
    """
    try:
        session_service = services["session_service"]
        points_service = services["points_service"]

        # Verify session exists
        session_service.get_session_or_raise(hint_request.session_id)

        # Apply penalty
        penalty = points_service.use_hint()

        return {
            "session_id": hint_request.session_id,
            "hint_penalty": penalty,
            "current_points": points_service.current_points,
            "message": "Hint requested. Points have been adjusted.",
        }

    except SessionException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
