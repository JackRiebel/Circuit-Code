# Circuit Agent v3.0

An AI-powered coding assistant for Cisco Circuit, similar to Claude Code. Works in your project directory with full file access, git integration, shell command execution, and **web search capabilities**.

## What's New in v3.0

- **Web Tools**: Search the web and fetch documentation directly from the agent
- **Session Persistence**: Save and load conversation sessions
- **Context Compaction**: Compress old messages to handle long conversations
- **Modular Architecture**: Tools organized into separate modules

## Quick Start

```bash
# Install dependencies
pip install httpx html2text  # html2text optional but recommended for web tools

# Run in current directory
python circuit_agent.py

# Or specify a project directory
python circuit_agent.py /path/to/project
```

## Features

### Tools (13 total)

| Category | Tool | Description |
|----------|------|-------------|
| **File** | `read_file` | Read files with line numbers (supports line ranges) |
| | `write_file` | Create or overwrite files |
| | `edit_file` | Find and replace text in files |
| | `list_files` | Find files by glob pattern |
| | `search_files` | Regex search across files |
| | `run_command` | Execute shell commands |
| **Git** | `git_status` | Show working tree status |
| | `git_diff` | Show changes (staged/unstaged) |
| | `git_log` | View commit history |
| | `git_commit` | Stage and commit changes |
| | `git_branch` | List/create/switch branches |
| **Web** | `web_fetch` | Fetch content from URLs (docs, APIs) |
| | `web_search` | Search the web for information |

### Commands

| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/files` | List files in working directory |
| `/clear` | Clear conversation history |
| `/model` | Change AI model |
| `/tokens` | Show token usage |
| `/undo` | Restore file from backup |
| `/git` | Quick git status |
| `/auto` | Toggle auto-approve mode |
| `/config` | Show configuration |
| `/save [name]` | Save current session |
| `/load [name]` | Load a saved session |
| `/sessions` | List all saved sessions |
| `/compact` | Compress old messages |
| `/quit` | Exit |

### Safety Features
- **Confirmation prompts** for file writes and dangerous commands
- **Auto-approve mode** - Type `a` during confirmation or use `/auto`
- **Automatic backups** before file modifications
- **Undo support** - Restore files with `/undo`
- **Path traversal protection** - Can't access files outside working directory

## Credentials

Get credentials from: https://developer.cisco.com/site/ai-ml/
→ Manage Circuit API Keys → View

### Options (checked in order):
1. **Config file**: `~/.config/circuit-agent/config.json` (saved on first run)
2. **Environment variables**: `CIRCUIT_CLIENT_ID`, `CIRCUIT_CLIENT_SECRET`, `CIRCUIT_APP_KEY`
3. **Interactive prompt** (with option to save)

## Project Configuration

Create a `CIRCUIT.md` file in your project root to give the agent project-specific instructions:

```markdown
## Project Context
This is a Python FastAPI backend with PostgreSQL.

## Conventions
- Use snake_case for functions
- Always add type hints
- Run `pytest` before committing

## Commands
- Test: `pytest -v`
- Lint: `ruff check .`
```

The agent automatically loads this into its system prompt.

## Available Models

| # | Model | Context | Best For |
|---|-------|---------|----------|
| 1 | gpt-4.1 | 120K | Complex reasoning |
| 2 | gpt-4o | 120K | Fast multimodal (default) |
| 3 | gpt-4o-mini | 120K | Quick & efficient |
| 4 | o4-mini | 200K | Large documents |

## Architecture

```
circuit_agent.py          # Entry point
circuit_agent/
├── __init__.py           # Package exports, version 3.0.0
├── agent.py              # CircuitAgent class (streaming, tools, retry)
├── cli.py                # Main loop and slash commands
├── config.py             # Credentials and CIRCUIT.md loading
├── streaming.py          # SSE response parsing
├── ui.py                 # Colors and display helpers
├── tools/                # Modular tool implementations
│   ├── __init__.py       # Tool exports, combined TOOLS list
│   ├── executor.py       # ToolExecutor with parallel support
│   ├── file_tools.py     # File operations (read, write, edit, etc.)
│   ├── git_tools.py      # Git operations (status, diff, commit, etc.)
│   └── web_tools.py      # Web operations (fetch, search)
└── memory/               # Session and context management
    ├── __init__.py       # Memory module exports
    ├── session.py        # Session save/load
    └── compaction.py     # Context compaction for long conversations
```

## Files

| File | Description |
|------|-------------|
| `circuit_agent.py` | Main entry point |
| `Circuit_Chat_Test.py` | Simple chat test (no tools) |
| `SETUP.md` | Detailed setup & troubleshooting |
| `CODEBASE_SUMMARY.md` | Codebase overview |
| `PLAN_V3.md` | v3.0 enhancement plan |
| `CIRCUIT.md` | Project-specific agent instructions |

## Dependencies

```
# Required
httpx>=0.24.0          # HTTP client for API calls

# Optional (recommended)
html2text>=2020.1.16   # HTML to markdown for web_fetch
```
