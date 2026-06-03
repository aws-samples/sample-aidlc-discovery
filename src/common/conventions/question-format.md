# Question Format

Each question:

```
### Q<n>: <text>           # Q for business, T for technical; suffix [CORE] = part of the Quick pass

a) ...
b) ...
c) Other

**Recommendation:** <option + brief reasoning>   # optional, for non-trivial choices

[Answer]:
```

Control tokens stay in English regardless of the user's language: `[Answer]:`, `[CORE]`, identifiers (`Q1`, `T14`), and the trigger word `ready`.

## Batch persistence (CRITICAL)

Two files per role, with distinct rules — this split is what prevents information loss (it is how v1 works):

- **`*-questions.md`** = buffer for the **active batch**. While a section is in progress it MAY be
  overwritten with the next batch, to keep the buffer clean for the user to fill in.
- **`*-answers-history.md`** = **append-only** record of every validated batch (questions + answers,
  caveats verbatim). NEVER rewrite or truncate it. Because confirmed answers already live here,
  overwriting the buffer never loses data.

On each validated batch: append a consolidated block to `*-answers-history.md`, update the role's
`*-state.md` checkboxes, then (optionally) overwrite `*-questions.md` with the next batch.

**Buffer header note (batch mode):** the `*-questions.md` progress header MUST state that prior batches are preserved — e.g. *"Previous batches (Q1–Q5): ✅ saved in `<role>-answers-history.md` — nothing is lost. This file shows only the active batch."* This removes the false impression that earlier questions were dropped.

## Interaction modes

The user picks an interaction mode during shared selection (`session-index.md` → `Interaction`):

- **`batch`** (default): questions are written to `*-questions.md` as a batch of 5–7; the user fills the `[Answer]:` tags and replies `ready`. Best for long sessions — fewer round-trips, edit at your own pace.
- **`conversational`**: questions are asked directly in chat, one at a time (or in small groups of 2–3); the user answers inline. No file editing. Best for a guided, question-by-question flow.

**Persistence is identical in both modes** (this is what keeps every mode resumable and lossless): on each validated question/batch, append to `*-answers-history.md` and update the `*-state.md` checkboxes. In `batch` mode the active `*-questions.md` buffer may then be overwritten; in `conversational` mode no buffer file is needed, but `*-answers-history.md` and `*-state.md` are still written.

Question banks are identical across modes and adapters, reused from the v1 rules
(`aidlc-discovery-rules/aidlc-discovery-rule-details/{business,technical}/*-interview.md`).
Adapter note: Kiro / Claude default to `batch`; Amazon Quick is `conversational` by nature.

## Approval & adjust loop (CRITICAL)

After answers for a batch/section are presented (pre-filled or completed), offer two choices —
**Approve** or **Request changes**. **Do NOT advance** to the next stage (next section, the other role,
the rendered document, or the join) **without an explicit Approve**. Never infer approval from silence
or from a "request changes" reply.

On **Request changes**, run this loop until the user approves:

1. Ask which question(s) to change and the new value(s).
2. Apply the change and persist it (`*-answers-history.md` + `*-state.md`).
3. **Re-show** the updated answer(s).
4. Offer **Approve / Request changes** again.

How "change" works per mode (the loop is the same; only the input differs):

- **batch** (Kiro / Claude): the user edits the `[Answer]:` tags in `*-questions.md` and replies `ready`,
  or names the question + new value in chat. Re-validate and re-show. *(This is the existing batch flow.)*
- **conversational** (Amazon Quick): the user states the change in chat; apply, re-show, re-confirm.
