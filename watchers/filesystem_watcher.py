"""
filesystem_watcher.py — Bronze Tier File System Watcher

Monitors the /Inbox drop folder. When a new file is dropped in,
it creates a corresponding action file in /Needs_Action/ for Claude to process.

Usage:
    python watchers/filesystem_watcher.py
    # or via uv:
    uv run file-watcher
"""

import os
import shutil
import time
import logging
from pathlib import Path
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from watchers.base_watcher import setup_logging


class DropFolderHandler(FileSystemEventHandler):
    """Handles new file events in the Inbox drop folder."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / "Needs_Action"
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logging("DropFolderHandler")
        self._processed: set[str] = set()

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        # Skip hidden files and temp files
        if source.name.startswith(".") or source.name.endswith("~"):
            return
        if str(source) in self._processed:
            return
        self._processed.add(str(source))

        self.logger.info(f"New file detected in Inbox: {source.name}")
        self._handle_new_file(source)

    def _handle_new_file(self, source: Path):
        """Copy file and create metadata action file in /Needs_Action."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = source.stem.replace(" ", "_")
        dest_name = f"FILE_{timestamp}_{safe_name}{source.suffix}"
        dest = self.needs_action / dest_name

        try:
            shutil.copy2(source, dest)
            self.logger.info(f"Copied to Needs_Action: {dest_name}")
        except Exception as e:
            self.logger.error(f"Failed to copy file: {e}")
            return

        # Create the metadata .md action file
        self._create_metadata(source, dest, timestamp)

        # Update Dashboard
        self._update_dashboard(source.name, dest_name)

    def _create_metadata(self, source: Path, dest: Path, timestamp: str):
        """Create a Markdown action file for the dropped file."""
        try:
            file_size = source.stat().st_size
        except Exception:
            file_size = 0

        size_str = self._format_size(file_size)
        meta_path = self.needs_action / f"ACTION_{timestamp}_{source.stem.replace(' ', '_')}.md"

        content = f"""---
type: file_drop
original_name: {source.name}
copied_as: {dest.name}
size: {size_str}
received: {datetime.now().isoformat()}
priority: normal
status: pending
---

## New File Dropped for Processing

A new file has been detected in the Inbox drop folder and requires processing.

**File:** `{source.name}`
**Size:** {size_str}
**Received:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Suggested Actions

- [ ] Review file contents
- [ ] Determine file type and intent
- [ ] Process according to Company Handbook rules
- [ ] Log outcome to `/Logs/`
- [ ] Move this file to `/Done/` when complete

## Notes

> Add any notes here after reviewing the file.
"""
        meta_path.write_text(content)
        self.logger.info(f"Created action file: {meta_path.name}")

    def _format_size(self, size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / 1024 ** 2:.1f} MB"

    def _update_dashboard(self, original_name: str, action_name: str):
        """Append entry to Dashboard.md recent activity."""
        dashboard = self.vault_path / "Dashboard.md"
        if not dashboard.exists():
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"- [{timestamp}] FileWatcher: New file `{original_name}` → `{action_name}`\n"
        content = dashboard.read_text()
        marker = "## Recent Activity"
        if marker in content:
            idx = content.index(marker) + len(marker)
            next_newline = content.index("\n", idx)
            content = content[: next_newline + 1] + entry + content[next_newline + 1 :]
            dashboard.write_text(content)


class FilesystemWatcher:
    """Main watcher class that monitors the Inbox folder using watchdog."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / "Inbox"
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logging("FilesystemWatcher")

    def run(self):
        self.logger.info(f"Starting FilesystemWatcher")
        self.logger.info(f"Watching folder: {self.inbox}")
        self.logger.info("Drop files into the Inbox folder to trigger processing.")
        self.logger.info("Press Ctrl+C to stop.")

        event_handler = DropFolderHandler(str(self.vault_path))
        observer = Observer()
        observer.schedule(event_handler, str(self.inbox), recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping watcher...")
            observer.stop()
        observer.join()
        self.logger.info("FilesystemWatcher stopped.")


def main():
    """Entry point — load vault path from env and start the watcher."""
    from dotenv import load_dotenv
    load_dotenv()
    vault_path = os.getenv("VAULT_PATH", "./AI_Employee_Vault")
    vault_path = str(Path(vault_path).resolve())
    watcher = FilesystemWatcher(vault_path)
    watcher.run()


if __name__ == "__main__":
    main()
