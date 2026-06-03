# State Schema (per-role, single-writer)

State is partitioned so the two roles can run in parallel without races. Each state file has exactly one writer.

```
Product-Definition/
├── state/
│   ├── session-index.md      # SHARED: project-type · depth · mode · interaction · per-role status · join status
│   ├── business-state.md     # written ONLY by the PM session
│   └── technical-state.md    # written ONLY by the tech-lead session
├── interview/
│   ├── business/     # vision-questions.md (active-batch buffer) · vision-answers-history.md (append-only)
│   └── technical/    # tech-env-questions.md (active-batch buffer) · tech-env-answers-history.md (append-only)
└── audit/{business,technical}-audit.md   # per-role, append-only
```

## session-index.md

```markdown
# Discovery Session Index
- Created / Last Updated: <ISO8601>
- Project Type: <Brand-new | Feature on existing | Migration | pending>
- Depth: <quick | full>            # may be overridden per role
- Mode: <single | sequential | parallel>
- Interaction: <batch | conversational>            # how questions are presented
- Business: <not-started | in-progress | complete>
- Technical: <not-started | in-progress | complete>
- Join: <blocked | ready | done>
```

`Join` becomes `ready` only when **both** roles are `complete` (the join barrier). The last role to
complete triggers the join. See `protocols/orchestrator-protocol.md`.

## <role>-state.md

```markdown
# <Business|Technical> State
- Status: <in-progress | complete>
- Depth: <quick | full>
## Questions
- [ ] Q1 [CORE]
- [x] Q2
```

Rules: read before write; never write another role's file; `session-index.md` shared fields are set
once during shared selection (pre fan-out). Control content stays in English.

`interview/<role>/<role>-questions.md` is the active-batch buffer (may be overwritten). The durable
record is `interview/<role>/<role>-answers-history.md`, which is **append-only** — never rewritten,
truncated, or removed. This split prevents information loss when the buffer is overwritten.
