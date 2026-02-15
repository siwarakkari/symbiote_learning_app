"""
Custom exceptions for the Symbiote Learning App.

Provides domain-specific exceptions for better error handling and clarity.
"""


class SymbioteException(Exception):
    """Base exception for all Symbiote-related errors."""

    def __init__(self, message: str, code: str = "SYMBIOTE_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class AgentException(SymbioteException):
    """Exception raised when an agent encounters an error."""

    def __init__(self, message: str, agent_type: str = "Unknown"):
        super().__init__(message, code=f"AGENT_ERROR_{agent_type.upper()}")
        self.agent_type = agent_type


class SessionException(SymbioteException):
    """Exception raised when a session encounters an error."""

    def __init__(self, message: str, session_id: str = None):
        super().__init__(message, code="SESSION_ERROR")
        self.session_id = session_id


class ValidationException(SymbioteException):
    """Exception raised when validation fails."""

    def __init__(self, message: str, field: str = None):
        super().__init__(message, code="VALIDATION_ERROR")
        self.field = field


class LLMException(SymbioteException):
    """Exception raised when LLM integration fails."""

    def __init__(self, message: str):
        super().__init__(message, code="LLM_ERROR")


class RegistryException(SymbioteException):
    """Exception raised when agent registry encounters an error."""

    def __init__(self, message: str):
        super().__init__(message, code="REGISTRY_ERROR")
