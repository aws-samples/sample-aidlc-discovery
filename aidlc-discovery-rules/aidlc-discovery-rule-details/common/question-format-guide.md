# Question Format Guide

Consistent rules for writing any question file in `Product-Definition/`.

**Language**: all user-facing text in question files (progress header, context sentences, option labels, examples, footer reminder) is written in the user's language per `common/language-handling.md`. The control tokens (`[Answer]:`, `[CORE]`, question identifiers like `Q1`/`T14`/`QB2`, and the trigger word `ready` with its accepted translations) stay as specified — do not translate them.

---

## Core format

Every question file (Business or Technical) MUST begin with a progress header and a "How to answer" block, then contain one or more questions, and close with a "ready" reminder.

### Progress header (mandatory at the top of every batch)

```markdown
# {Interview Name} — Section {N} of {Total}: {Section Title}

Progress: {bar} {answered}/{total} questions  ·  ~{minutes_left} min remaining

This batch covers Q{first}–Q{last}. Fill in the [Answer]: tags below,
then reply with **"ready"** and I'll validate your answers and move on.
```

- `{bar}` is a 10-segment bar: `█` for answered, `░` for pending. E.g. 10/18 → `█████░░░░░`.
- `{minutes_left}` is estimated at ~1 minute per remaining question.
- Always include the exact word **"ready"** as the trigger — see "The ready trigger" below.

### Multiple-choice question format

```markdown
## Question {N}: {Short title}

{One or two sentences of context — why this matters, what the options imply.}

A) {Option A — with a concrete example when helpful}
B) {Option B}
C) {Option C}
D) {Option D — optional, up to five letters total}
X) Other (please describe after [Answer]: tag below)

[Answer]:
```

### Free-text question format

Use this when there is no natural set of options (e.g. "describe your problem in 1–2 paragraphs"). **Do NOT fake multiple-choice with a single "A) Write your answer below" option — that confuses users.**

```markdown
## Question {N}: {Short title}

{One or two sentences of context, including an example when possible.}

{Example: "Mid-size retail operations managers who track inventory across
multiple stores."}

[Answer]:
```

### Table question format

When the answer is a table, include a **pre-filled example row** the user replaces, plus a blank slot under `[Answer]:`:

```markdown
## Question {N}: {Short title}

{Context.} Replace the example row below with your own data. Add or remove
rows as needed. Put the final table under [Answer]:.

**Example (do not submit as your answer):**

| Column A | Column B | Column C |
|----------|----------|----------|
| (e.g.) …  | …        | …        |

[Answer]:

| Column A | Column B | Column C |
|----------|----------|----------|
|          |          |          |
```

### Footer (mandatory at the bottom of every batch)

```markdown
---

When you're done, reply with a single word: **ready**

(I'll re-read this file from disk and validate your answers.)
```

## Rules for writing questions

1. **One decision per question.** If you need two answers, write two questions.
2. **Options must be mutually distinct.** If A and B overlap, the user won't know which to pick.
3. **Use multiple-choice only when the answer space is naturally discrete.** For one-liners, paragraphs, and tables, use the free-text or table formats above.
4. **Always include X) in multiple-choice questions.** Even a well-designed set of options can miss the user's real answer.
5. **Context before options.** One or two sentences so the user knows what the question actually means.
6. **Plain English.** Avoid jargon the user may not know; if a term is unavoidable, define it inline.
7. **5–7 questions per batch.** More overwhelms, fewer wastes round-trips.
8. **Group by section.** All questions about "Problem Statement" go in one batch; don't interleave.
9. **Number consecutively within the whole file** (Q1, Q2, Q3 …) so later state tracking stays unambiguous even after rewrites.

## The "ready" trigger

The single-word reply **"ready"** (case-insensitive) is the official signal that the user wants the AI to re-read the question file and validate. Accept equivalents the user may use (`done`, `go`, `listo`) but the canonical word printed in every batch is `ready`.

When the user types `ready`:

1. **Re-read the file from disk.** Never trust in-memory content — the user may have edited, and prior tool output may be stale.
2. Validate per "Rules for reading answers" below.
3. If the user replies with free text that is NOT `ready` (e.g. a follow-up question), treat it as a question and respond without validating — wait for the explicit `ready` signal.

## Rules for reading answers

Once the user replies `ready`:

1. **Re-read the file from disk** (see above).
2. **Validate every `[Answer]:` tag:**
   - Non-empty
   - For multiple-choice: starts with one of the offered letters, or `X` followed by free text
   - For free-text: non-empty prose or table content
   - If combined (e.g. `A and C`), accept and record both
   - If the user wrote a qualified answer (e.g. `B — with the caveat that…`), preserve the caveat verbatim in the answer history
3. **Flag ambiguities.** If a letter is missing, or the free text under X is too vague to act on, ask a follow-up **in the same file** (append a new question, do NOT modify the previous one).
4. **Confirm before moving on.** Summarize each validated answer in one line and proceed only when the batch is clean.

## Batched writes (performance)

To reduce file-write overhead, group writes per batch rather than per question:

- **Answers history**: 1 append per batch containing all validated answers for the batch (not one append per question).
- **State checkboxes**: 1 update per batch marking all answered questions `[x]` simultaneously.
- **Audit**: 1 entry per batch summarizing which questions were validated (plus individual entries for batch-open and batch-close events).

The only exception is when the user pauses mid-batch with partial answers — then flush what you have.

## Examples of good answers (educate the user once)

Include this block at the top of the FIRST question file in each role (Business or Technical) so the user learns the pattern. Omit it from subsequent batches to keep them short.

```markdown
## How to answer

- For multiple-choice questions, put the letter first, then a short label:
  `C — financial summary and debt service coverage` is clearer than just `C`.
- For free-text questions, write directly under `[Answer]:`.
- For tables, replace the example row and keep the column headers exactly as shown.
- Include a brief justification when it's not obvious: `A — design-first; generate OpenAPI before code`.
- Combine options when you mean both: `B and C — rate limit at API Gateway and app level`.
- Add a caveat when an option is almost right: `B — migration is a separate project; include a one-time migration only`.
- Use X freely. If no option fits, X is the right choice over forcing a wrong answer.
- To change a prior answer later, just tell me "I want to change my answer to Q{N}" — I'll reopen it without you having to edit files manually.
```

## Re-writing vs appending

- While a section is **in progress**, overwrite the `*-questions.md` file with the next batch.
- Every time a batch is validated, append a consolidated block to `*-answers-history.md`:

```markdown
## Batch — Section {N}, Q{first}–Q{last}   — {ISO8601 timestamp}

### Q{N}: {Short title}
**Answer**: {letter and/or X text, including caveats verbatim}
**Notes** (AI): {optional one-line interpretation notes}

### Q{N+1}: ...
```

- Never rewrite `*-answers-history.md`. It is the append-only audit of everything the user confirmed.
