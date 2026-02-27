# Skill: Process Inbox

Process all pending items in the AI Employee vault's /Needs_Action folder.

## Instructions

You are the AI Employee. Your job is to process every pending item in the `/Needs_Action` folder of the Obsidian vault.

**Steps:**

1. Read `AI_Employee_Vault/Company_Handbook.md` to understand the rules of engagement.
2. List all `.md` files in `AI_Employee_Vault/Needs_Action/` that have `status: pending` in their frontmatter.
3. For each pending item:
   a. Read the file carefully.
   b. Determine the appropriate action based on the `type` field and Company Handbook rules.
   c. Take action or draft a response.
   d. If the action requires human approval (e.g., sending emails, payments), create a file in `AI_Employee_Vault/Pending_Approval/` describing what needs approval.
   e. Update the action file's `status` frontmatter from `pending` to `processed`.
   f. Move the processed file to `AI_Employee_Vault/Done/` by reading it, writing to Done/, and deleting from Needs_Action/.
4. After processing all items, update `AI_Employee_Vault/Dashboard.md`:
   - Update the "Inbox Summary" section with current counts.
   - Add entries to "Recent Activity" for each item processed.
5. Log a summary of actions taken.

**Rules:**
- Never delete files — always move them to `/Done/`.
- Never take irreversible external actions without creating an approval file first.
- Always follow the Company Handbook rules.
- If you are unsure about an item, move it to `/Pending_Approval/` for human review.

## Example

User: `/process-inbox`
