"""
Circuit Agent Service Layer.

Provides a unified backend for all UI implementations (CLI, TUI, GUI).
This layer abstracts the agent logic and provides event-driven communication.
"""

from .events import Event, EventEmitter, EventType
from .state import (
    AgentState,
    ChatMessage,
    ToolCallInfo,
    ConfirmationRequest,
    ConnectionStatus,
    MessageRole,
    ToolStatus,
    TokenUsage,
    CostInfo,
)
from .agent_service import AgentService

__all__ = [
    # Events
    "Event",
    "EventEmitter",
    "EventType",
    # State
    "AgentState",
    "ChatMessage",
    "ToolCallInfo",
    "ConfirmationRequest",
    "ConnectionStatus",
    "MessageRole",
    "ToolStatus",
    "TokenUsage",
    "CostInfo",
    # Service
    "AgentService",
]
