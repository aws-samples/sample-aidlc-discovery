# Audit Format

`Product-Definition/audit.md` is the append-only, ISO8601-timestamped log of every interaction in the session. It exists so we can reconstruct what happened if the state file is ever damaged, and so reviewers can see exactly what the user said in their own words.

---

## File initialization

When `audit.md` does not exist, create it with this header exactly:

```markdown
# AI-DLC Discovery — Audit Log

Append-only log. Every user prompt, question file write, answer validation,
role transition, and approval gate is recorded here with an ISO8601 timestamp
and the user's complete raw input.

Do not rewrite this file. Use Read + Edit (append) only.

---
```

## Entry format

Append a new block for every logged event. Do not modify or remove prior blocks.

```markdown
## [{Stage or Event Type}]
**Timestamp**: {ISO8601 UTC — e.g. 2026-04-27T17:42:00Z}
**User Input**: "{Complete raw user input — never summarized; empty string if the event was AI-driven}"
**AI Action**: "{What the AI did in response, one to three sentences}"
**Context**: {Relevant state, file, or decision touched}

---
```

## Events that MUST be logged

| Event                                 | Stage label                         |
| ------------------------------------- | ----------------------------------- |
| Workflow kicked off                   | `Workflow Start`                    |
| Welcome message displayed             | `Welcome`                           |
| Session detected (new or resume)      | `Session Detection`                 |
| Role selection question written       | `Role Selection — Question`         |
| Role selection answer received        | `Role Selection — Answer`           |
| Greenfield/Brownfield question        | `Project Type — Question`           |
| Greenfield/Brownfield answer          | `Project Type — Answer`             |
| Business question batch written       | `Business Interview — Q{N..M}`      |
| Business answer validated             | `Business Interview — A{N}`         |
| Business completion gate              | `Business Interview — Completion`   |
| Vision document rendered              | `Vision Document — Render`          |
| Technical question batch written      | `Technical Interview — Q{N..M}`     |
| Technical answer validated            | `Technical Interview — A{N}`        |
| Technical completion gate             | `Technical Interview — Completion`  |
| Technical Environment rendered        | `Technical Environment — Render`    |
| Open questions compiled               | `Open Questions — Compiled`         |
| Final handoff message shown           | `Handoff`                           |
| User-requested role change            | `Role Change`                       |
| User-requested section re-open        | `Section Re-open`                   |
| Validation failure (see content-validation.md) | `Validation Failure`       |

## Rules

1. **Append-only.** Always `Read` first, then `Edit` with a targeted append. Never `Write` the whole file.
2. **Raw input, verbatim.** Do not paraphrase, translate, or correct the user. If the user typed with typos, preserve them.
3. **Timestamps in UTC** (ISO8601 with trailing `Z`). Time zones must not vary within one session's log.
4. **One entry per event.** Do not batch multiple events into a single block.
5. **No sensitive data.** If the user pastes what appears to be a secret (API key, password, token), log a redacted marker (`[REDACTED — looked like credential]`) and ask the user to remove the secret from the source file.
