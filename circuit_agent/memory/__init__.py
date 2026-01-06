"""
Memory module for Circuit Agent v3.0.

Provides session persistence and context compaction.
"""

from .session import SessionManager
from .compaction import ContextCompactor

__all__ = [
    'SessionManager',
    'ContextCompactor',
]
