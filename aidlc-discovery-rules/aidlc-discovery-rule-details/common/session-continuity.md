# Session Continuity

Governs how the workflow detects, creates, and resumes a definition session.

---

## Detection

At the start of every invocation (after the welcome message):

1. Check for `./Product-Definition/aidlc-discovery-state.md` in the current working directory
2. If **absent** → this is a **new session**
3. If **present** → this is a **resume session**

## New Session Bootstrap

If no state file exists:

1. Create the scaffold:
   ```
   Product-Definition/
   ├── aidlc-discovery-state.md           (from template below)
   ├── audit.md                           (from common/audit-format.md)
   └── interview/
       ├── business/
       └── technical/
   ```
2. Write the initial state file:
   ```markdown
   # AI-DLC Discovery State

   ## Session Metadata
   - Created: <ISO8601>
   - Last Updated: <ISO8601>
   - Project Type: <pending>
   - Current Role: <pending>

   ## Role Progress
   - Business (Vision Document):     ⚪ Not Started
   - Technical (Technical Env Doc):  ⚪ Not Started

   ## Business Questions
   (will be populated when Business interview starts)

   ## Technical Questions
   (will be populated when Technical interview starts)
   ```
3. Proceed to `common/role-selection.md`

## Resume Session

If a state file exists:

1. **Read** `aidlc-discovery-state.md` from disk (do not rely on prior context memory)
2. Parse:
   - Session Metadata (project type, current role)
   - Role Progress (Business / Technical status)
   - Per-question checkboxes (unanswered count per section)
3. Present a resume summary to the user. Template:

```
Existing aidlc-discovery session detected.

Session created:   <created_ts>
Last updated:      <last_updated_ts>
Project type:      <Brand-new | Feature on existing | Migration | pending>
                   (display the user-facing classification from state,
                    not the internal Greenfield/Brownfield label)

Role progress
─────────────
  Business (Vision):            <status>  (<answered>/<total>)
  Technical (Technical Env):    <status>  (<answered>/<total>)

What would you like to do?

  A) Continue <current-role> from the next unanswered question
  B) Start the other role now
  C) Review / edit a specific section of a role already marked complete
  X) Other (describe)

[Answer]:
```

4. Wait for the user's choice. Based on the answer:
   - **A** → jump into the relevant interview file and find the first unchecked question
   - **B** → run the Role Selection stage only if no role was previously selected; otherwise start the other role directly
   - **C** → ask which section, then load the relevant interview file and rewrite that section's questions into `*-questions.md` with previous answers pre-populated so the user can edit
   - **X** → interpret the user's custom intent and proceed accordingly

## Updating State

**CRITICAL rules**:

- Always use `Read` before modifying `aidlc-discovery-state.md` (never blind-overwrite)
- Update the `Last Updated` metadata field on every change
- Append — never remove — per-question entries unless the user explicitly asks to remove a section
- Reflect the current stage in `Current Role` so resume works correctly

## Audit

Every detection, bootstrap, and resume decision MUST be logged in `Product-Definition/audit.md` per `common/audit-format.md`. This is how we reconstruct sessions if the state file is ever damaged.
