# Personal AI Employee — Bronze Tier

> *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

A **Bronze Tier** implementation of the Personal AI Employee from the GIAIC Hackathon. This is the foundation layer — a fully functional local-first autonomous agent powered by Claude Code and an Obsidian vault.

---

## What's Built (Bronze Tier)

| Requirement | Status | Details |
|-------------|--------|---------|
| Obsidian vault with `Dashboard.md` | ✅ | `AI_Employee_Vault/Dashboard.md` |
| `Company_Handbook.md` | ✅ | `AI_Employee_Vault/Company_Handbook.md` |
| File System Watcher | ✅ | `watchers/filesystem_watcher.py` |
| Gmail Watcher (stub) | ✅ | `watchers/gmail_watcher.py` (needs OAuth setup) |
| Vault folder structure | ✅ | Inbox, Needs_Action, Done, Plans, etc. |
| Claude reads/writes to vault | ✅ | Via CLAUDE.md + Agent Skills |
| Agent Skills | ✅ | `/process-inbox`, `/triage-tasks`, `/daily-briefing`, `/update-dashboard` |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AI Employee System                    │
│                                                         │
│  ┌──────────────┐    ┌──────────────────────────────┐   │
│  │  Watchers    │───▶│     AI_Employee_Vault/       │   │
│  │              │    │                              │   │
│  │ • FileSystem │    │  Inbox/        (drop folder) │   │
│  │ • Gmail      │    │  Needs_Action/ (to process)  │   │
│  │   (Silver+)  │    │  Done/         (completed)   │   │
│  └──────────────┘    │  Plans/        (AI plans)    │   │
│                      │  Pending_Approval/ (HITL)    │   │
│  ┌──────────────┐    │  Briefings/    (reports)     │   │
│  │ Claude Code  │◀───│  Dashboard.md  (status)      │   │
│  │              │    │  Company_Handbook.md (rules) │   │
│  │ Agent Skills:│───▶│                              │   │
│  │ /process-inbox│   └──────────────────────────────┘   │
│  │ /triage-tasks │                                       │
│  │ /daily-briefing│                                      │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
personal-ai-employee/
├── AI_Employee_Vault/           # Obsidian vault (the brain's memory)
│   ├── Dashboard.md             # Real-time status
│   ├── Company_Handbook.md      # AI rules of engagement
│   ├── Inbox/                   # Drop files here
│   ├── Needs_Action/            # AI processes these
│   ├── Done/                    # Completed items
│   ├── Plans/                   # AI-generated plans
│   ├── Pending_Approval/        # Awaiting human sign-off
│   ├── Approved/                # Ready to execute
│   ├── Rejected/                # Declined items
│   ├── Briefings/               # CEO briefings
│   └── Accounting/              # Financial records
├── watchers/
│   ├── __init__.py
│   ├── base_watcher.py          # Abstract base class
│   ├── filesystem_watcher.py    # Bronze tier (file drop monitoring)
│   └── gmail_watcher.py         # Silver tier (Gmail monitoring)
├── .claude/
│   └── skills/
│       ├── process-inbox.md     # /process-inbox skill
│       ├── triage-tasks.md      # /triage-tasks skill
│       ├── daily-briefing.md    # /daily-briefing skill
│       └── update-dashboard.md  # /update-dashboard skill
├── CLAUDE.md                    # Claude Code context file
├── pyproject.toml               # UV project config
├── .env.example                 # Environment variable template
└── README.md                    # This file
```

---

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- [Claude Code](https://claude.ai/code) (active subscription)
- [Obsidian](https://obsidian.md) v1.10.6+ (optional, for GUI)

### Setup

```bash
# 1. Clone / navigate to project
cd "personal-ai-employee"

# 2. Install dependencies
uv sync

# 3. Copy environment template
cp .env.example .env
# Edit .env and set VAULT_PATH if needed (default: ./AI_Employee_Vault)

# 4. Start the File System Watcher (Terminal 1)
uv run file-watcher

# 5. Start Claude Code (Terminal 2)
claude
```

### Open Vault in Obsidian (Optional GUI)

1. Open Obsidian → "Open folder as vault"
2. Select `AI_Employee_Vault/`
3. You'll see Dashboard.md update in real-time as the AI works

---

## Usage

### Drop a file for processing

```bash
# Drop any file into the Inbox folder
cp my-document.pdf AI_Employee_Vault/Inbox/

# The FileSystemWatcher detects it and creates an action file in Needs_Action/
# Then run Claude to process it:
claude
> /process-inbox
```

### Run agent skills in Claude Code

```bash
claude
> /process-inbox       # Process all pending items
> /triage-tasks        # Prioritize by urgency
> /daily-briefing      # Generate today's CEO briefing
> /update-dashboard    # Refresh dashboard stats
```

---

## Security

- **Credentials** are never stored in the vault. Use `.env` or system keychain.
- `.env` is in `.gitignore` — never commit it.
- All external actions require human approval via `/Pending_Approval/`.
- `DRY_RUN=true` by default — set to `false` only when ready for live actions.

---

## Tier Roadmap

| Tier | Status | Key Features |
|------|--------|-------------|
| **Bronze** | ✅ Complete | Vault, File Watcher, Agent Skills, HITL framework |
| Silver | Planned | Gmail + WhatsApp watchers, LinkedIn posting, MCP servers |
| Gold | Planned | Full integration, Odoo accounting, Ralph Wiggum loop |
| Platinum | Planned | Cloud + local split, 24/7 always-on |

---

## Hackathon

- **Event:** GIAIC Personal AI Employee Hackathon 0
- **Tier:** Bronze
- **Stack:** Claude Code + Obsidian + Python + watchdog
- **Submit:** https://forms.gle/JR9T1SJq5rmQyGkGA
