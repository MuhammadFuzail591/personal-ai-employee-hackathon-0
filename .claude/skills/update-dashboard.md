# Skill: Update Dashboard

Refresh the Dashboard.md with current vault statistics and status.

## Instructions

You are the AI Employee. Refresh the Dashboard.md with live data from the vault.

**Steps:**

1. Count files in each folder:
   - `AI_Employee_Vault/Needs_Action/` — pending items
   - `AI_Employee_Vault/Pending_Approval/` — items awaiting human approval
   - `AI_Employee_Vault/Done/` — completed items (today only)
   - `AI_Employee_Vault/Plans/` — active plans

2. Check watcher status by looking for recent files (within last 2 hours) in Needs_Action.

3. Read `AI_Employee_Vault/Accounting/Bank_Transactions.md` for financial summary.

4. Rewrite the relevant sections of `AI_Employee_Vault/Dashboard.md`:
   - **System Status** table: mark components as active/inactive
   - **Inbox Summary**: update counts
   - **Business Snapshot**: update metrics from Accounting

5. Do NOT overwrite the **Recent Activity** section — only append to it.

6. Output a confirmation message with the updated stats.

## Example

User: `/update-dashboard`
