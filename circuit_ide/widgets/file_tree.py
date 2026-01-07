"""
File Tree Widget for Circuit IDE.

Provides an interactive file browser with keyboard navigation.
"""

import os
from pathlib import Path
from typing import Optional, Set, Callable
from dataclasses import dataclass

from textual.widgets import Tree, Static
from textual.widgets.tree import TreeNode
from textual.message import Message
from textual.reactive import reactive


# File type icons (emoji-based for terminal compatibility)
FILE_ICONS = {
    # Programming languages
    ".py": "🐍",
    ".js": "📜",
    ".ts": "📘",
    ".jsx": "⚛️",
    ".tsx": "⚛️",
    ".go": "🔵",
    ".rs": "🦀",
    ".rb": "💎",
    ".java": "☕",
    ".c": "🔷",
    ".cpp": "🔷",
    ".h": "📎",
    ".cs": "🟣",
    ".php": "🐘",
    ".swift": "🍎",
    ".kt": "🟠",
    # Web
    ".html": "🌐",
    ".css": "🎨",
    ".scss": "🎨",
    ".sass": "🎨",
    ".less": "🎨",
    ".vue": "💚",
    ".svelte": "🔥",
    # Data/Config
    ".json": "📋",
    ".yaml": "📋",
    ".yml": "📋",
    ".toml": "📋",
    ".xml": "📋",
    ".csv": "📊",
    ".sql": "🗃️",
    ".env": "🔐",
    # Documentation
    ".md": "📝",
    ".txt": "📄",
    ".rst": "📝",
    ".pdf": "📕",
    # Shell/Scripts
    ".sh": "💻",
    ".bash": "💻",
    ".zsh": "💻",
    ".fish": "💻",
    ".ps1": "💻",
    # Other
    ".gitignore": "🙈",
    ".dockerignore": "🐳",
    "Dockerfile": "🐳",
    "Makefile": "🔧",
    ".lock": "🔒",
    # Default
    "default": "📄",
    "folder": "📁",
    "folder_open": "📂",
}


@dataclass
class FileInfo:
    """Information about a file or directory."""
    path: Path
    name: str
    is_dir: bool
    size: int = 0
    modified: float = 0

    @property
    def icon(self) -> str:
        """Get the appropriate icon for this file."""
        if self.is_dir:
            return FILE_ICONS["folder"]

        # Check by filename first
        if self.name in FILE_ICONS:
            return FILE_ICONS[self.name]

        # Then by extension
        ext = self.path.suffix.lower()
        return FILE_ICONS.get(ext, FILE_ICONS["default"])


class FileTreeWidget(Tree):
    """Interactive file tree browser."""

    BINDINGS = [
        ("enter", "select_node", "Open"),
        ("space", "toggle_node", "Expand/Collapse"),
        ("r", "refresh", "Refresh"),
        ("n", "new_file", "New File"),
        ("d", "delete_file", "Delete"),
    ]

    # Messages
    class FileSelected(Message):
        """Message sent when a file is selected."""
        def __init__(self, path: Path) -> None:
            self.path = path
            super().__init__()

    class DirectoryChanged(Message):
        """Message sent when navigating to a directory."""
        def __init__(self, path: Path) -> None:
            self.path = path
            super().__init__()

    # Reactive properties
    show_hidden: reactive[bool] = reactive(False)

    def __init__(
        self,
        root_path: str | Path,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        ignored_patterns: list[str] | None = None,
    ):
        """Initialize the file tree.

        Args:
            root_path: Root directory to display
            name: Widget name
            id: Widget ID
            classes: CSS classes
            ignored_patterns: Patterns to ignore (e.g., ['__pycache__', '*.pyc'])
        """
        self.root_path = Path(root_path).resolve()
        self.ignored_patterns = set(ignored_patterns or [
            "__pycache__", "*.pyc", ".git", "node_modules",
            ".venv", "venv", ".tox", "dist", "build",
            ".next", ".cache", "*.egg-info",
        ])

        # Track expanded nodes
        self._expanded: Set[Path] = set()

        super().__init__(
            self.root_path.name,
            data=FileInfo(
                path=self.root_path,
                name=self.root_path.name,
                is_dir=True,
            ),
            name=name,
            id=id,
            classes=classes,
        )

    def on_mount(self) -> None:
        """Called when widget is mounted - load root directory."""
        self._load_directory(self.root, self.root_path)
        self.root.expand()

    def _should_ignore(self, name: str) -> bool:
        """Check if a file/directory should be ignored."""
        if not self.show_hidden and name.startswith("."):
            return True

        for pattern in self.ignored_patterns:
            if pattern.startswith("*."):
                # Extension pattern
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True

        return False

    def _load_directory(self, node: TreeNode, path: Path) -> None:
        """Load contents of a directory into a tree node."""
        node.remove_children()

        try:
            entries = list(path.iterdir())
        except PermissionError:
            node.add_leaf("[Permission Denied]")
            return

        # Separate and sort directories and files
        dirs = []
        files = []

        for entry in entries:
            if self._should_ignore(entry.name):
                continue

            try:
                stat = entry.stat()
                info = FileInfo(
                    path=entry,
                    name=entry.name,
                    is_dir=entry.is_dir(),
                    size=stat.st_size if not entry.is_dir() else 0,
                    modified=stat.st_mtime,
                )

                if entry.is_dir():
                    dirs.append(info)
                else:
                    files.append(info)
            except (PermissionError, OSError):
                continue

        # Sort alphabetically
        dirs.sort(key=lambda x: x.name.lower())
        files.sort(key=lambda x: x.name.lower())

        # Add directories first, then files
        for info in dirs:
            child = node.add(f"{info.icon} {info.name}", data=info)
            # Add placeholder for lazy loading
            child.add_leaf("...")

        for info in files:
            node.add_leaf(f"{info.icon} {info.name}", data=info)

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """Handle node expansion - load directory contents."""
        node = event.node
        data = node.data

        if isinstance(data, FileInfo) and data.is_dir:
            # Check if we need to load (has placeholder)
            children = list(node.children)
            if len(children) == 1 and children[0].data is None:
                self._load_directory(node, data.path)
            self._expanded.add(data.path)

    def on_tree_node_collapsed(self, event: Tree.NodeCollapsed) -> None:
        """Handle node collapse."""
        node = event.node
        data = node.data
        if isinstance(data, FileInfo):
            self._expanded.discard(data.path)

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle node selection."""
        node = event.node
        data = node.data

        if isinstance(data, FileInfo):
            if data.is_dir:
                # Toggle directory
                if node.is_expanded:
                    node.collapse()
                else:
                    node.expand()
                self.post_message(self.DirectoryChanged(data.path))
            else:
                # Open file
                self.post_message(self.FileSelected(data.path))

    def action_refresh(self) -> None:
        """Refresh the file tree."""
        # Reload the root
        self._load_directory(self.root, self.root_path)

    def action_toggle_node(self) -> None:
        """Toggle the current node."""
        if self.cursor_node:
            node = self.cursor_node
            if node.is_expanded:
                node.collapse()
            else:
                node.expand()

    def refresh_path(self, path: Path) -> None:
        """Refresh a specific path in the tree."""
        # Find the node for this path and reload it
        # For now, just refresh the whole tree
        self.action_refresh()

    def select_path(self, path: Path) -> None:
        """Select and reveal a specific path."""
        # Navigate to the path
        rel_path = path.relative_to(self.root_path)
        parts = rel_path.parts

        node = self.root
        for part in parts[:-1]:  # Navigate to parent
            for child in node.children:
                if isinstance(child.data, FileInfo) and child.data.name == part:
                    child.expand()
                    node = child
                    break

        # Select the final node
        for child in node.children:
            if isinstance(child.data, FileInfo) and child.data.name == parts[-1]:
                self.select_node(child)
                break

    def watch_show_hidden(self, show_hidden: bool) -> None:
        """React to show_hidden changes."""
        self.action_refresh()


class FileTreeHeader(Static):
    """Header for the file tree panel."""

    def __init__(self, title: str = "FILES"):
        super().__init__(title)
        self.add_class("panel-header")
