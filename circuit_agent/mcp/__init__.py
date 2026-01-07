"""
MCP (Model Context Protocol) client module for Circuit IDE.

Provides integration with MCP servers like GitHub MCP Server,
enabling AI agents to use external tools.
"""

from .config import MCPServerConfig
from .client import MCPClientManager
from .converter import mcp_to_openai, openai_to_mcp_args

__all__ = [
    "MCPServerConfig",
    "MCPClientManager",
    "mcp_to_openai",
    "openai_to_mcp_args",
]
