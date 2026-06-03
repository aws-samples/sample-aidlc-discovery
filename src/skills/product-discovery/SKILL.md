---
name: product-discovery
description: |
  Guided product-vision interview for the Business role (PM). Produces vision-document.md plus
  pre-declared open questions. Replaces the blank page with structured questions.
metadata:
  stage: product-discovery
  role: business
  human-clarification: "true"
  plan-creation: "false"
  artefact-verification: "true"
---

# Product Discovery (Business role)

Single-writer on `state/business-state.md`. Render questions per
`aidlc-common/conventions/question-format.md` (batch or conversational, per the chosen interaction mode).

**Question bank — reuse v1** (do not duplicate):
`aidlc-discovery-rules/aidlc-discovery-rule-details/business/vision-interview.md`
(depth `quick` = `[CORE]` questions only; `full` = all).

## Output

- `Product-Definition/vision-document.md` — sections per v1 `business/vision-completion.md`
  (Executive Summary, Problem, Target Users, Success Metrics, Full Vision, MVP IN, MVP OUT, Risks/Open).
- Entries appended to `Product-Definition/open-questions.md`.

The `artefact-verification` gate is the per-role approval before the document is final.

## Validation

See `validation-spec.md`.
