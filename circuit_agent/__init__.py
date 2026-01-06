"""
Circuit Agent v3.0 - AI-Powered Coding Assistant

A Cisco Circuit-powered coding assistant that works like Claude Code:
reads files, writes code, runs commands, searches the web, and helps
with software engineering tasks in your project directory.

New in v3.0:
- Web fetch and search tools
- Session save/load
- Context compaction
- Modular tool architecture
"""

__version__ = "3.0.0"
__author__ = "Circuit Agent"

from .agent import CircuitAgent
from .tools import TOOLS, FileTools, GitTools, WebTools, BackupManager
from .memory import SessionManager, ContextCompactor
from .config import (
    load_credentials,
    save_credentials,
    delete_credentials,
    load_circuit_md,
    MODELS,
)
from .cli import run_cli, main

__all__ = [
    "CircuitAgent",
    "FileTools",
    "GitTools",
    "WebTools",
    "BackupManager",
    "SessionManager",
    "ContextCompactor",
    "TOOLS",
    "load_credentials",
    "save_credentials",
    "delete_credentials",
    "load_circuit_md",
    "MODELS",
    "run_cli",
    "main",
    "__version__",
]
