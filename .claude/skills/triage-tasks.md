# Skill: Triage Tasks

Triage all items in /Needs_Action and prioritize them according to Company Handbook rules.

## Instructions

You are the AI Employee. Your job is to triage and prioritize all items in the vault.

**Steps:**

1. Read `AI_Employee_Vault/Company_Handbook.md` for escalation rules and priorities.
2. List all files in `AI_Employee_Vault/Needs_Action/`.
3. For each file, read its frontmatter and content.
4. Assign a priority based on these rules:
   - **URGENT**: Contains keywords: "urgent", "legal", "payment over $500", "complaint", "security breach"
   - **HIGH**: Emails from known important contacts, invoices due today, tasks overdue
   - **NORMAL**: Standard emails, routine file drops, informational items
   - **LOW**: FYI items, newsletters, non-actionable notifications
5. Update each file's frontmatter: set `priority` to `urgent`, `high`, `normal`, or `low`.
6. For URGENT items: also create a copy in `AI_Employee_Vault/Needs_Action/` prefixed with `URGENT_`.
7. Generate a triage summary report:

```markdown
## Triage Report — <Timestamp>

| Priority | Count | Items |
|----------|-------|-------|
| URGENT   | X     | list  |
| HIGH     | X     | list  |
| NORMAL   | X     | list  |
| LOW      | X     | list  |

### Urgent Items Requiring Immediate Attention
<list urgent items with brief description>
```

8. Update `AI_Employee_Vault/Dashboard.md` with the triage summary in Recent Activity.

**Important:** This skill only reads and re-prioritizes. It does NOT process or complete items — use `/process-inbox` for that.

## Example

User: `/triage-tasks`
