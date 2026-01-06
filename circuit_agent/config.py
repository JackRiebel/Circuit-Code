"""
Configuration management for Circuit Agent.
Handles credentials, settings, and CIRCUIT.md loading.
"""

import json
import os
from typing import Tuple, Optional, Dict, Any


# Configuration paths
CONFIG_DIR = os.path.expanduser("~/.config/circuit-agent")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
GLOBAL_CIRCUIT_MD = os.path.join(CONFIG_DIR, "CIRCUIT.md")

# API Configuration
TOKEN_URL = "https://id.cisco.com/oauth2/default/v1/token"
CHAT_BASE_URL = "https://chat-ai.cisco.com/openai/deployments"
API_VERSION = "2025-04-01-preview"

# Available models
MODELS = {
    "1": ("gpt-4.1", "GPT-4.1 - Complex reasoning (120K context)"),
    "2": ("gpt-4o", "GPT-4o - Fast multimodal (120K context)"),
    "3": ("gpt-4o-mini", "GPT-4o Mini - Quick & efficient (120K context)"),
    "4": ("o4-mini", "o4-mini - Large context (200K context)"),
}

# Dangerous command patterns to warn about
DANGEROUS_PATTERNS = [
    r"rm\s+(-rf?|--recursive).*(/|~|\$HOME)",
    r"rm\s+-rf?\s+\.",
    r"sudo\s+rm",
    r"sudo\s+mv\s+/",
    r"sudo\s+chmod",
    r"sudo\s+chown",
    r"mkfs\.",
    r"dd\s+.*of=/dev/",
    r"shutdown",
    r"reboot",
    r":(){ :\|:& };:",  # Fork bomb
    r">\s*/dev/sd",
    r"chmod\s+-R\s+777\s+/",
    r"chown\s+-R.*\s+/",
    r"git\s+push.*--force",
    r"git\s+push.*-f\b",
    r"git\s+reset\s+--hard",
    r"curl.*\|\s*(ba)?sh",
    r"wget.*\|\s*(ba)?sh",
    r">\s*/etc/",
    r"mv\s+/\w",
    r"rm\s+-rf?\s+/\w",
]


def load_credentials() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Load credentials from config file or environment variables.
    Returns (client_id, client_secret, app_key) - any can be None if not found.
    """
    client_id = None
    client_secret = None
    app_key = None

    # First, try config file
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                client_id = config.get('client_id')
                client_secret = config.get('client_secret')
                app_key = config.get('app_key')
        except (json.JSONDecodeError, IOError):
            pass

    # Environment variables override config file
    if os.environ.get('CIRCUIT_CLIENT_ID'):
        client_id = os.environ.get('CIRCUIT_CLIENT_ID')
    if os.environ.get('CIRCUIT_CLIENT_SECRET'):
        client_secret = os.environ.get('CIRCUIT_CLIENT_SECRET')
    if os.environ.get('CIRCUIT_APP_KEY'):
        app_key = os.environ.get('CIRCUIT_APP_KEY')

    return client_id, client_secret, app_key


def save_credentials(client_id: str, client_secret: str, app_key: str) -> bool:
    """Save credentials to config file. Returns True on success."""
    try:
        os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)
        config = {
            'client_id': client_id,
            'client_secret': client_secret,
            'app_key': app_key
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        # Secure the file (readable only by owner)
        os.chmod(CONFIG_FILE, 0o600)
        return True
    except IOError:
        return False


def delete_credentials() -> bool:
    """Delete saved credentials. Returns True on success."""
    try:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        return True
    except IOError:
        return False


def load_circuit_md(working_dir: str) -> Optional[str]:
    """
    Load CIRCUIT.md configuration file.
    Checks (in order):
    1. Working directory: ./CIRCUIT.md
    2. Global config: ~/.config/circuit-agent/CIRCUIT.md

    Returns the content or None if not found.
    """
    # Check project-specific first
    project_circuit_md = os.path.join(working_dir, "CIRCUIT.md")
    if os.path.exists(project_circuit_md):
        try:
            with open(project_circuit_md, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            pass

    # Fall back to global
    if os.path.exists(GLOBAL_CIRCUIT_MD):
        try:
            with open(GLOBAL_CIRCUIT_MD, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            pass

    return None


def get_circuit_md_locations(working_dir: str) -> Dict[str, bool]:
    """Get the locations and existence status of CIRCUIT.md files."""
    return {
        "project": os.path.exists(os.path.join(working_dir, "CIRCUIT.md")),
        "global": os.path.exists(GLOBAL_CIRCUIT_MD),
        "project_path": os.path.join(working_dir, "CIRCUIT.md"),
        "global_path": GLOBAL_CIRCUIT_MD,
    }


def detect_project_type(working_dir: str) -> str:
    """Detect project type and return context string."""
    info_parts = []

    # Check for common project files
    checks = [
        ("package.json", "Node.js/JavaScript project"),
        ("pyproject.toml", "Python project (pyproject.toml)"),
        ("setup.py", "Python project (setup.py)"),
        ("requirements.txt", "Python project"),
        ("Cargo.toml", "Rust project"),
        ("go.mod", "Go project"),
        ("pom.xml", "Java/Maven project"),
        ("build.gradle", "Java/Gradle project"),
        ("Gemfile", "Ruby project"),
        ("composer.json", "PHP project"),
        ("Makefile", "Project with Makefile"),
        ("Dockerfile", "Docker containerized"),
        (".git", "Git repository"),
    ]

    for filename, description in checks:
        if os.path.exists(os.path.join(working_dir, filename)):
            info_parts.append(description)

    if info_parts:
        return "**Project detected**: " + ", ".join(info_parts[:3])
    return ""


def get_config_summary() -> Dict[str, Any]:
    """Get a summary of current configuration."""
    client_id, client_secret, app_key = load_credentials()

    return {
        "credentials_saved": os.path.exists(CONFIG_FILE),
        "config_dir": CONFIG_DIR,
        "config_file": CONFIG_FILE,
        "global_circuit_md": os.path.exists(GLOBAL_CIRCUIT_MD),
        "has_credentials": bool(client_id and client_secret and app_key),
        "client_id_preview": client_id[:8] + "..." if client_id else None,
    }
