# Project Type Selection

Asked once per session, immediately after Role Selection. The answer branches several downstream questions in both the Business and Technical interviews.

**Important for the AI model**: this file uses the internal terms "Greenfield" and "Brownfield" because the rest of the workflow does. **The user NEVER sees those words.** The question is phrased in plain language (new project / feature on existing / migration), and the AI maps the user's answer to the internal type silently.

---

## Internal mapping

| User picks                        | Internal type | Downstream branching                                                        |
| --------------------------------- | ------------- | --------------------------------------------------------------------------- |
| A — Brand-new project             | Greenfield    | No "Current State" / "What must not change"; no Reverse Engineering         |
| B — New feature on existing       | Brownfield    | Include "Current State" + "What must not change"; Reverse Engineering later |
| C — Migration/modernisation       | Brownfield    | Same as B, plus "Existing Stack Inventory" flagged as migration source      |
| X — Other / mixed                 | Hybrid        | Ask follow-up to classify as primarily new or primarily existing            |

## Question to ask (user-facing — keep the wording exactly like this)

Write the following into `Product-Definition/interview/project-type.md`:

```markdown
# Project Type

## Question: Which best describes this project?

A) **Brand-new project** — we are building something from scratch. There is no
   existing code, and no existing system we must integrate with or preserve.

B) **New feature on an existing product** — there is already a system in
   production (or built), and we are adding a capability to it. Existing code,
   schemas, APIs, or users must continue to work.

C) **Migration / modernisation of an existing system** — there is a system
   in place and we are rebuilding, replatforming, or replacing part of it.
   Some existing contracts or data will carry over.

X) Other — describe after [Answer]: below
   (example: "mostly brand-new but we must connect to one existing service
   for authentication")

[Answer]:

---

When you're done, reply with a single word: **ready**
```

Stop and wait for the user's answer.

## Validation

After the user replies `ready`:

1. **Re-read** `project-type.md` from disk.
2. Validate the answer starts with `A`, `B`, `C`, or `X`.
3. Map to the internal type using the table above. Do NOT show the internal term to the user unless they ask.
4. For `X`, ask a follow-up (in the same file) to classify the project as primarily new (→ Greenfield) or primarily built on something existing (→ Brownfield or Hybrid). Downstream branches need a primary type.

## Recording the answer

Update the state file with both the user-facing choice and the internal mapping:

```markdown
## Session Metadata
- Project Type: <Greenfield | Brownfield | Hybrid:{description}>
- User-facing classification: <A — Brand-new | B — New feature on existing | C — Migration | X:{description}>
```

Append to `audit.md` per `common/audit-format.md` with stage label `Project Type — Answer`.

## Follow-up (ask only if B or C — i.e. there IS an existing system)

Append this second question in the same `project-type.md` file below the first:

```markdown
## Question: How can I learn about your existing system?

Pick whichever is easiest — later interview questions are smoother when I have
something to look at, but prose also works.

A) The existing code is in this workspace or in a repository I can read —
   tell me the path and I'll explore it as needed.

B) No code access, but I have documents (architecture notes, ADRs, wiki pages,
   screenshots) — I'll share the paths or links when the interview asks.

C) Neither — I'll describe the existing system in my own words when the
   interview asks.

X) Other

[Answer]:

---

When you're done, reply with a single word: **ready**
```

Record this answer alongside the first. It informs how the Business interview phrases "Current State" questions and whether the Technical interview pulls example code from real files or asks the user to paste snippets.

## Transition

Once the question(s) are answered and logged, proceed per the chosen role:

- Role includes Business → `business/vision-interview.md`
- Role includes Technical → `technical/tech-env-interview.md`
- Role is "Both (sequential)" → Business first, Technical second

## Glossary (AI-only; do NOT show to the user)

If the user asks what "greenfield" or "brownfield" means (because they saw it in AI-DLC docs elsewhere), explain naturally:

- **Greenfield** = brand-new project with no existing code to preserve (= user's option A).
- **Brownfield** = existing codebase we're extending or modifying (= user's options B or C).

Use those words only if the user uses them first.
