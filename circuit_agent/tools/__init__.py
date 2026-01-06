"""
Tools package for Circuit Agent v3.0.

Provides modular tool implementations with parallel execution support.
"""

from .executor import ToolExecutor, BackupManager
from .file_tools import FileTools, FILE_TOOLS
from .git_tools import GitTools, GIT_TOOLS
from .web_tools import WebTools, WEB_TOOLS

# Combined tool definitions for the API
TOOLS = FILE_TOOLS + GIT_TOOLS + WEB_TOOLS

__all__ = [
    'ToolExecutor',
    'BackupManager',
    'FileTools',
    'GitTools',
    'WebTools',
    'TOOLS',
    'FILE_TOOLS',
    'GIT_TOOLS',
    'WEB_TOOLS',
]
