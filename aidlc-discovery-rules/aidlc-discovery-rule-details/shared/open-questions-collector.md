# Open Questions Collector

Runs at the end of each completed role (Business and/or Technical) to compile the uncertainties that should be handed off to AI-DLC as pre-declared ambiguities.

---

## Why this matters

AI-DLC's Requirements Analysis works best when it knows up front what is uncertain. Open questions surfaced here become the first things AI-DLC asks about — rather than appearing as surprises mid-design.

## Sources to scan

For each completed role, scan:

1. `Product-Definition/interview/<role>/*-answers-history.md` for:
   - Answers tagged `X)` with wording that expresses uncertainty ("maybe", "not sure", "we haven't decided", "TBD")
   - Answers that combine options with a deferral ("A for now, possibly B later")
   - Caveats that include temporal markers ("to be revisited", "phase 2", "after pilot")
2. AI-flagged ambiguities raised during answer validation (see `common/question-format-guide.md` §"Rules for reading answers")
3. Any explicit user statements like "write this down as an open question for AI-DLC"

## Output file

Compile into `Product-Definition/open-questions.md`. This file is **rewritten** each time the collector runs (not append-only), so it always reflects the current state.

### Structure

```markdown
# Open Questions for AI-DLC

Pre-declared ambiguities and unresolved decisions surfaced during definition.
AI-DLC should address these early in Requirements Analysis.

Last generated: <ISO8601>

## Business (Vision) open questions

### OQ-B-1: <Short title>
- **Source section**: <Problem Statement | Target Users | Success Metrics | ...>
- **Question**: <Plain-English restatement of the uncertainty>
- **User's stated reasoning**: <Verbatim caveat from answer history>
- **Suggested resolution path** (AI): <One or two sentences pointing to what would resolve it — e.g. "Needs pilot data", "Requires stakeholder decision from <team>">

### OQ-B-2: ...

## Technical (Technical Environment) open questions

### OQ-T-1: <Short title>
- **Source section**: <Languages | Frameworks | Cloud Services | Security | ...>
- **Question**: <...>
- **User's stated reasoning**: <...>
- **Suggested resolution path** (AI): <...>

### OQ-T-2: ...

## Summary

Total open questions: <N>  (Business: <n_b>, Technical: <n_t>)

AI-DLC should load this file during Requirements Analysis and resolve each entry
before proceeding to User Stories or Application Design.
```

## Numbering

- Business entries use prefix `OQ-B-<N>`.
- Technical entries use prefix `OQ-T-<N>`.
- Numbering is monotonic within each role across rewrites — if OQ-B-3 was resolved and removed, do not reuse `3`; the next new business open question becomes `OQ-B-4`. (Track the last used N in `aidlc-discovery-state.md`.)

## State update

After writing `open-questions.md`, update `aidlc-discovery-state.md`:

```markdown
## Open Questions
- Last Compiled: <ISO8601>
- Business: <n_b> open
- Technical: <n_t> open
- Next Index: {business: <next_b>, technical: <next_t>}
```

## When to re-run

Run the collector:

- At the end of the Business interview completion gate (before rendering `vision-document.md`)
- At the end of the Technical interview completion gate (before rendering `technical-environment.md`)
- Any time the user re-opens a completed section and adds new caveats

Log every run in `audit.md` with stage label `Open Questions — Compiled`.
