# Role Selection

Runs once per session, unless the session already has a role assigned (in which case `session-continuity.md` handles it).

---

## Purpose

Determine which of the two AI-DLC Discovery the user wants to produce in this session, and record it durably.

## Question to ask

Write the following into `Product-Definition/interview/role-selection.md` using the `[Answer]:` tag format from `question-format-guide.md`. Then stop and wait for the user to answer.

```markdown
# Role Selection

## Question: Which role are you taking in this session?

Pick the role that matches who is driving the definition. "Both (sequential)"
is the right choice when the same person will fill in everything in one
continuous effort.

A) Business  — I own the "what and why". I want to produce the Vision Document.
B) Technical — I own the "which tools and constraints". I want to produce the Technical Environment Document.
C) Both (sequential) — I will fill in Business first, then Technical in the same session or in a later one.
X) Other (describe after [Answer]:)

[Answer]:
```

## Handling the answer

Once the user says the answer is ready:

1. **Re-read** `role-selection.md` from disk
2. Validate the answer is non-empty and one of A / B / C / X
3. If X, interpret the free-text and confirm interpretation with the user before proceeding
4. Write the resolved choice into the state file:

```markdown
## Session Metadata
- Current Role: <Business | Technical | Both-Sequential | Custom:{description}>
```

5. Log to `audit.md` (raw input, timestamp, stage = "Role Selection")
6. Proceed to `shared/greenfield-vs-brownfield.md`

## Changing roles later

If the user says they want to change the role mid-session:

1. Do NOT delete existing progress for the previous role
2. Update `Current Role` in the state file
3. If the previous role has unanswered questions, mark the role status as `⏸ Paused` in Role Progress
4. Log the change in `audit.md` with the reason the user gave (if any)
