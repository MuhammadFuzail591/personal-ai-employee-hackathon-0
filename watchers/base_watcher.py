"""
base_watcher.py — Abstract base class for all AI Employee watchers.

All watchers follow the same pattern:
  1. check_for_updates() — detect new items
  2. create_action_file() — write .md to /Needs_Action
  3. run() — loop forever at check_interval
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime


def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)


class BaseWatcher(ABC):
    """Abstract base class for all vault watchers."""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / "Needs_Action"
        self.done = self.vault_path / "Done"
        self.check_interval = check_interval
        self.logger = setup_logging(self.__class__.__name__)
        self._ensure_folders()

    def _ensure_folders(self):
        """Make sure required vault folders exist."""
        for folder in [self.needs_action, self.done]:
            folder.mkdir(parents=True, exist_ok=True)

    def update_dashboard(self, message: str):
        """Append a timestamped entry to Dashboard.md recent activity."""
        dashboard = self.vault_path / "Dashboard.md"
        if not dashboard.exists():
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"- [{timestamp}] {message}\n"
        content = dashboard.read_text()
        marker = "## Recent Activity"
        if marker in content:
            insert_pos = content.index(marker) + len(marker) + 1
            # Find the next line after the marker
            next_newline = content.index("\n", insert_pos)
            content = content[: next_newline + 1] + entry + content[next_newline + 1 :]
            dashboard.write_text(content)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process."""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create a .md file in /Needs_Action and return its path."""
        pass

    def run(self):
        """Main loop — runs continuously until interrupted."""
        self.logger.info(f"Starting {self.__class__.__name__} (interval={self.check_interval}s)")
        self.logger.info(f"Vault: {self.vault_path}")
        self.logger.info("Press Ctrl+C to stop.")
        while True:
            try:
                items = self.check_for_updates()
                if items:
                    self.logger.info(f"Found {len(items)} new item(s) to process")
                for item in items:
                    path = self.create_action_file(item)
                    self.logger.info(f"Created action file: {path.name}")
                    self.update_dashboard(f"{self.__class__.__name__} created: {path.name}")
            except KeyboardInterrupt:
                self.logger.info("Watcher stopped by user.")
                break
            except Exception as e:
                self.logger.error(f"Error during check: {e}", exc_info=True)
            time.sleep(self.check_interval)
