---
name: tech-discovery
description: |
  Guided technical-constraints interview for the Technical role (tech lead). Captures
  human-provided constraints (allow/deny lists for languages, frameworks, cloud, security,
  testing). It records constraints — it does not design the stack.
metadata:
  stage: tech-discovery
  role: technical
  human-clarification: "true"
  plan-creation: "false"
  artefact-verification: "true"
---

# Tech Discovery (Technical role)

Single-writer on `state/technical-state.md`. Render questions per
`aidlc-common/conventions/question-format.md` (batch or conversational, per the chosen interaction mode).

**Question bank — reuse v1** (do not duplicate):
`aidlc-discovery-rules/aidlc-discovery-rule-details/technical/tech-env-interview.md`
(depth `quick` = `[CORE]` questions only; `full` = all).

## Output

- `Product-Definition/technical-environment.md` — sections per v1 `technical/tech-env-completion.md`
  (Languages, Frameworks, Cloud Services, Architecture, Security, Testing, Example Code).
- Entries appended to `Product-Definition/open-questions.md`.

## Validation

See `validation-spec.md`.
