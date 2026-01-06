"""
CLI interface for Circuit Agent v3.0.
Main loop, slash commands, and user interaction.
"""

import asyncio
import os
import sys
from getpass import getpass
from pathlib import Path
from typing import Optional

from .agent import CircuitAgent
from .config import (
    MODELS, load_credentials, save_credentials, delete_credentials,
    get_circuit_md_locations, get_config_summary, CONFIG_FILE
)
from .ui import (
    C, clear_screen, clear_line, print_header, print_welcome, print_help,
    print_token_usage, print_error, print_success, print_warning, print_info
)
from .memory import SessionManager


async def run_cli(working_dir: Optional[str] = None):
    """Main CLI entry point."""
    # Determine working directory
    if working_dir is None:
        if len(sys.argv) > 1:
            working_dir = sys.argv[1]
        else:
            working_dir = os.getcwd()

    if not os.path.isdir(working_dir):
        print(f"{C.RED}Error: '{working_dir}' is not a valid directory{C.RESET}")
        sys.exit(1)

    working_dir = os.path.abspath(working_dir)

    clear_screen()
    print_header(working_dir)

    # Load credentials
    client_id, client_secret, app_key = load_credentials()
    credentials_from_config = os.path.exists(CONFIG_FILE)
    needs_save_prompt = False

    if client_id and client_secret and app_key:
        if credentials_from_config:
            print_success(f"Using saved credentials from {CONFIG_FILE}")
        else:
            print_success("Using credentials from environment variables")
    else:
        print(f"""{C.BOLD}Enter your Cisco Circuit credentials:{C.RESET}

  Get these from: {C.CYAN}https://developer.cisco.com/site/ai-ml/{C.RESET}
  → Manage Circuit API Keys → View
""")
        if not client_id:
            client_id = input(f"  {C.CYAN}Client ID:{C.RESET} ").strip()
        if not client_secret:
            client_secret = getpass(f"  {C.CYAN}Client Secret:{C.RESET} ").strip()
        if not app_key:
            app_key = input(f"  {C.CYAN}App Key:{C.RESET} ").strip()
        needs_save_prompt = True

    if not all([client_id, client_secret, app_key]):
        print_error("All credentials are required")
        sys.exit(1)

    # Test connection
    print_info("Testing connection...")
    agent = CircuitAgent(client_id, client_secret, app_key, working_dir)

    try:
        await agent.get_token()
        print_success("Authentication successful!")

        if needs_save_prompt:
            save_response = input(f"\n  {C.CYAN}Save credentials for future sessions? [Y/n]:{C.RESET} ").strip().lower()
            if save_response in ('', 'y', 'yes'):
                if save_credentials(client_id, client_secret, app_key):
                    print_success(f"Credentials saved to {CONFIG_FILE}")
                else:
                    print_warning("Could not save credentials")

    except Exception as e:
        print_error(f"Authentication failed: {e}")
        sys.exit(1)

    # Select model
    print(f"\n{C.BOLD}Select a model:{C.RESET}\n")
    for k, (_, desc) in MODELS.items():
        print(f"  {C.CYAN}{k}){C.RESET} {desc}")

    choice = input(f"\n  Choice [{C.GREEN}2{C.RESET}]: ").strip() or "2"
    if choice in MODELS:
        agent.model = MODELS[choice][0]
    print_success(f"Using {agent.model}")

    # Show welcome message
    print_welcome()

    # Main chat loop
    await chat_loop(agent, working_dir)


async def chat_loop(agent: CircuitAgent, working_dir: str):
    """Main chat loop handling user input and commands."""
    while True:
        try:
            user_input = input(f"\n{C.BLUE}You:{C.RESET} ").strip()

            if not user_input:
                continue

            # Handle slash commands
            if user_input.startswith('/'):
                cmd_result = handle_command(user_input, agent, working_dir)
                if cmd_result == "quit":
                    break
                elif cmd_result == "continue":
                    continue
                # If cmd_result is None, fall through to chat

            # Regular chat
            print(f"{C.DIM}  Thinking...{C.RESET}", end="", flush=True)

            # Streaming callback to print content as it arrives
            first_chunk = [True]  # Use list to allow modification in closure

            def on_content(chunk: str):
                if first_chunk[0]:
                    clear_line()
                    print(f"\n{C.MAGENTA}Agent:{C.RESET} ", end="", flush=True)
                    first_chunk[0] = False
                print(chunk, end="", flush=True)

            response = await agent.chat(user_input, on_content=on_content)
            clear_line()

            # If streaming printed content, just add newline
            if not first_chunk[0]:
                print()  # Newline after streamed content
            elif response:
                print(f"\n{C.MAGENTA}Agent:{C.RESET} {response}")

            # Show token usage
            stats = agent.get_token_stats()
            if stats["last_total"] > 0:
                print_token_usage(
                    stats["last_prompt"],
                    stats["last_completion"],
                    stats["session_prompt"],
                    stats["session_completion"]
                )

        except KeyboardInterrupt:
            print(f"\n\n{C.CYAN}Goodbye!{C.RESET}\n")
            break
        except Exception as e:
            clear_line()
            print_error(str(e))


def handle_command(user_input: str, agent: CircuitAgent, working_dir: str) -> str:
    """
    Handle a slash command.
    Returns: "quit" to exit, "continue" to skip to next iteration, None to fall through
    """
    parts = user_input.lower().split()
    cmd = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    # Quit commands
    if cmd in ['/quit', '/exit', '/q']:
        print(f"\n{C.CYAN}Goodbye!{C.RESET}\n")
        return "quit"

    # Clear history
    elif cmd in ['/clear', '/c']:
        agent.clear_history()
        print_success("Conversation cleared")
        return "continue"

    # Show history
    elif cmd == '/history':
        if not agent.history:
            print_info("No conversation history")
        else:
            print(f"\n{C.BOLD}Recent conversation:{C.RESET}")
            for msg in agent.history[-10:]:
                role = msg.get('role', 'unknown').upper()
                content = msg.get('content', '')
                if role == 'USER':
                    print(f"  {C.BLUE}[USER]{C.RESET} {content[:80]}{'...' if len(content) > 80 else ''}")
                elif role == 'ASSISTANT':
                    preview = content[:80].replace('\n', ' ')
                    print(f"  {C.MAGENTA}[AGENT]{C.RESET} {preview}{'...' if len(content) > 80 else ''}")
        return "continue"

    # List files
    elif cmd == '/files':
        files = list(Path(working_dir).glob('*'))
        print(f"\n{C.DIM}Files in {working_dir}:{C.RESET}")
        for f in sorted(files)[:20]:
            icon = "📁" if f.is_dir() else "📄"
            print(f"  {icon} {f.name}")
        if len(files) > 20:
            print_info(f"... and {len(files) - 20} more")
        return "continue"

    # Change model
    elif cmd == '/model':
        print(f"\n{C.BOLD}Select a model:{C.RESET}")
        for k, (_, desc) in MODELS.items():
            marker = " ←" if MODELS[k][0] == agent.model else ""
            print(f"  {C.CYAN}{k}){C.RESET} {desc}{C.GREEN}{marker}{C.RESET}")
        choice = input(f"\n  Choice: ").strip()
        if choice in MODELS:
            agent.model = MODELS[choice][0]
            print_success(f"Switched to {agent.model}")
        return "continue"

    # Token usage
    elif cmd == '/tokens':
        stats = agent.get_token_stats()
        print(f"\n{C.BOLD}Token Usage:{C.RESET}")
        print(f"  Last request:  {stats['last_prompt']:,} in / {stats['last_completion']:,} out ({stats['last_total']:,} total)")
        print(f"  Session total: {stats['session_prompt']:,} in / {stats['session_completion']:,} out ({stats['session_total']:,} total)")
        return "continue"

    # Undo
    elif cmd in ['/undo', '/u']:
        backup_manager = agent.backup_manager

        # If path specified, undo that file
        if args:
            path = args[0]
            success, message = backup_manager.restore(path)
            if success:
                print_success(message)
            else:
                print_error(message)
        else:
            # Undo last modified file
            last_modified = backup_manager.get_last_modified()
            if last_modified:
                print_info(f"Last modified: {last_modified}")
                confirm = input(f"  {C.CYAN}Restore this file? [y/N]:{C.RESET} ").strip().lower()
                if confirm in ('y', 'yes'):
                    success, message = backup_manager.restore(last_modified)
                    if success:
                        print_success(message)
                    else:
                        print_error(message)
                else:
                    print_info("Cancelled")
            else:
                print_info("No files to undo")

            # Show available backups
            backups = backup_manager.list_backups()
            if backups:
                print(f"\n{C.DIM}Files with backups:{C.RESET}")
                for path, count in backups.items():
                    print(f"  {path} ({count} backup{'s' if count > 1 else ''})")
        return "continue"

    # Configuration
    elif cmd == '/config':
        summary = get_config_summary()
        circuit_md = get_circuit_md_locations(working_dir)

        print(f"\n{C.BOLD}Configuration:{C.RESET}")
        print(f"  Config dir:  {summary['config_dir']}")
        print(f"  Credentials: {'Saved' if summary['credentials_saved'] else 'Not saved'}")
        if summary['client_id_preview']:
            print(f"  Client ID:   {summary['client_id_preview']}")

        print(f"\n{C.BOLD}CIRCUIT.md:{C.RESET}")
        print(f"  Project: {circuit_md['project_path']}")
        print(f"           {'✓ Found' if circuit_md['project'] else '✗ Not found'}")
        print(f"  Global:  {circuit_md['global_path']}")
        print(f"           {'✓ Found' if circuit_md['global'] else '✗ Not found'}")

        print(f"\n{C.BOLD}Current session:{C.RESET}")
        print(f"  Model:       {agent.model}")
        print(f"  Streaming:   {'Enabled' if agent.stream_responses else 'Disabled'}")
        print(f"  Auto-approve: {C.YELLOW + 'ON' + C.RESET if agent.auto_approve else 'Off'}")
        print(f"  History:     {len(agent.history)} messages")
        return "continue"

    # Logout
    elif cmd == '/logout':
        if delete_credentials():
            print_success("Saved credentials deleted")
            print_info("You'll need to re-enter credentials next time")
        else:
            print_warning("No saved credentials found")
        return "continue"

    # Help
    elif cmd in ['/help', '/h']:
        print_help()
        return "continue"

    # Streaming toggle
    elif cmd == '/stream':
        agent.stream_responses = not agent.stream_responses
        status = "enabled" if agent.stream_responses else "disabled"
        print_success(f"Streaming {status}")
        return "continue"

    # Auto-approve toggle
    elif cmd == '/auto':
        agent.auto_approve = not agent.auto_approve
        if agent.auto_approve:
            print_warning("Auto-approve ENABLED - all actions will be executed without confirmation")
        else:
            print_success("Auto-approve disabled - confirmations required")
        return "continue"

    # Git status shortcut
    elif cmd == '/git':
        result = agent.git_tools.git_status({}, False)
        print(f"\n{result}")
        return "continue"

    # Session save
    elif cmd == '/save':
        if not args:
            # Generate name from timestamp
            from datetime import datetime
            name = datetime.now().strftime("%Y%m%d-%H%M%S")
        else:
            name = args[0]

        success, message = agent.save_session(name)
        if success:
            print_success(message)
        else:
            print_error(message)
        return "continue"

    # Session load
    elif cmd == '/load':
        if not args:
            # Show available sessions
            sessions = agent.list_sessions()
            if not sessions:
                print_info("No saved sessions found")
            else:
                print(f"\n{C.BOLD}Saved sessions:{C.RESET}")
                for i, s in enumerate(sessions[:10], 1):
                    print(f"  {i}. {s['name']} ({s['message_count']} msgs, {s['model']})")
                print(f"\n  Use: /load <name>")
        else:
            name = args[0]
            success, message = agent.load_session(name)
            if success:
                print_success(message)
            else:
                print_error(message)
        return "continue"

    # List sessions
    elif cmd == '/sessions':
        sessions = agent.list_sessions()
        if not sessions:
            print_info("No saved sessions found")
        else:
            print(f"\n{C.BOLD}Saved sessions:{C.RESET}")
            for s in sessions[:15]:
                created = s['created_at'][:10] if len(s['created_at']) > 10 else s['created_at']
                print(f"  {C.CYAN}{s['name']}{C.RESET}")
                print(f"    {created} | {s['message_count']} msgs | {s['model']}")
            if len(sessions) > 15:
                print(f"\n  ... and {len(sessions) - 15} more")
        return "continue"

    # Context compaction
    elif cmd == '/compact':
        stats = agent.get_compaction_stats()
        print(f"\n{C.BOLD}Context stats:{C.RESET}")
        print(f"  Messages: {stats['message_count']}")
        print(f"  Est. tokens: ~{stats['estimated_tokens']:,}")

        if stats['needs_compaction']:
            print(f"\n  Would compact: {stats['would_compact']} msgs → summary")
            print(f"  Would keep: {stats['would_keep']} recent msgs")

            confirm = input(f"\n  {C.CYAN}Compact now? [y/N]:{C.RESET} ").strip().lower()
            if confirm in ('y', 'yes'):
                success, message = agent.compact_history()
                if success:
                    print_success(message)
                else:
                    print_info(message)
        else:
            print_info("No compaction needed yet")
        return "continue"

    # Unknown command
    else:
        print_warning("Unknown command. Type /help for help.")
        return "continue"


def main():
    """Entry point for the CLI."""
    try:
        asyncio.run(run_cli())
    except KeyboardInterrupt:
        print(f"\n{C.CYAN}Goodbye!{C.RESET}\n")


if __name__ == "__main__":
    main()
