"""
gmail_watcher.py — Gmail Watcher (Silver Tier)

Monitors Gmail for unread important messages and creates action files
in /Needs_Action/ for Claude to process.

Setup:
  1. Go to https://console.cloud.google.com/
  2. Create a project, enable Gmail API
  3. Create OAuth 2.0 credentials (Desktop app)
  4. Download credentials.json to ./credentials/
  5. Run once to authorize: python watchers/gmail_watcher.py --auth
  6. Set GMAIL_CREDENTIALS_PATH in your .env file

Usage:
    python watchers/gmail_watcher.py
"""

import os
import json
from pathlib import Path
from datetime import datetime

from watchers.base_watcher import BaseWatcher


class GmailWatcher(BaseWatcher):
    """Watches Gmail for unread important messages."""

    def __init__(self, vault_path: str, credentials_path: str):
        super().__init__(vault_path, check_interval=120)
        self.credentials_path = Path(credentials_path)
        self.processed_ids: set[str] = set()
        self._state_file = self.vault_path / ".gmail_processed_ids.json"
        self._load_state()
        self._service = None

    def _load_state(self):
        """Load previously processed message IDs to avoid duplicates."""
        if self._state_file.exists():
            try:
                data = json.loads(self._state_file.read_text())
                self.processed_ids = set(data.get("processed_ids", []))
                self.logger.info(f"Loaded {len(self.processed_ids)} processed message IDs")
            except Exception as e:
                self.logger.warning(f"Could not load state: {e}")

    def _save_state(self):
        """Persist processed message IDs."""
        # Keep only the last 1000 IDs to prevent unbounded growth
        ids_list = list(self.processed_ids)[-1000:]
        self._state_file.write_text(json.dumps({"processed_ids": ids_list}))

    def _get_service(self):
        """Lazily initialize Gmail API service."""
        if self._service is not None:
            return self._service
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build

            SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
            creds = None
            token_path = self.credentials_path.parent / "gmail_token.json"

            if token_path.exists():
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_path), SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                token_path.write_text(creds.to_json())

            self._service = build("gmail", "v1", credentials=creds)
            self.logger.info("Gmail API service initialized")
            return self._service
        except ImportError:
            self.logger.error(
                "Google API libraries not installed. Run: uv add google-api-python-client google-auth-oauthlib"
            )
            return None
        except Exception as e:
            self.logger.error(f"Failed to initialize Gmail service: {e}")
            return None

    def check_for_updates(self) -> list:
        """Fetch unread important messages from Gmail."""
        service = self._get_service()
        if service is None:
            return []
        try:
            results = service.users().messages().list(
                userId="me", q="is:unread is:important"
            ).execute()
            messages = results.get("messages", [])
            new_messages = [m for m in messages if m["id"] not in self.processed_ids]
            return new_messages
        except Exception as e:
            self.logger.error(f"Failed to fetch Gmail messages: {e}")
            return []

    def create_action_file(self, message: dict) -> Path:
        """Create an action .md file for an email."""
        service = self._get_service()
        try:
            msg = service.users().messages().get(
                userId="me", id=message["id"]
            ).execute()
        except Exception as e:
            self.logger.error(f"Failed to fetch message {message['id']}: {e}")
            return Path()

        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        sender = headers.get("From", "Unknown Sender")
        subject = headers.get("Subject", "No Subject")
        date = headers.get("Date", datetime.now().isoformat())
        snippet = msg.get("snippet", "")

        # Sanitize for filename
        safe_id = message["id"][:12]
        filepath = self.needs_action / f"EMAIL_{safe_id}.md"

        content = f"""---
type: email
message_id: {message["id"]}
from: {sender}
subject: {subject}
received: {date}
priority: high
status: pending
---

## Email Content

**From:** {sender}
**Subject:** {subject}
**Received:** {date}

**Preview:**
> {snippet}

## Suggested Actions

- [ ] Review email content
- [ ] Draft reply (move draft to /Pending_Approval/ for review)
- [ ] Forward to relevant party if needed
- [ ] Archive after processing
- [ ] Move this file to /Done/ when complete

## Notes

> Add your notes here.
"""
        filepath.write_text(content)
        self.processed_ids.add(message["id"])
        self._save_state()
        return filepath


def main():
    """Entry point for Gmail watcher."""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    vault_path = os.getenv("VAULT_PATH", "./AI_Employee_Vault")
    credentials_path = os.getenv("GMAIL_CREDENTIALS_PATH", "./credentials/credentials.json")
    vault_path = str(Path(vault_path).resolve())
    watcher = GmailWatcher(vault_path, credentials_path)
    watcher.run()


if __name__ == "__main__":
    main()
