"""
Circuit IDE Widgets.

Custom Textual widgets for the IDE interface.
"""

from .file_tree import FileTreeWidget
from .editor import CodeEditor
from .chat import ChatPanel
from .status import AgentStatusWidget, StatusBar
from .terminal import TerminalWidget

__all__ = [
    "FileTreeWidget",
    "CodeEditor",
    "ChatPanel",
    "AgentStatusWidget",
    "StatusBar",
    "TerminalWidget",
]
