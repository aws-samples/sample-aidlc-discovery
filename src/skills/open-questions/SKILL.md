---
name: open-questions
description: |
  Join stage. Consolidates pre-declared open questions from both roles and flags cross-role
  contradictions (vision <-> constraints). Runs once both roles are complete.
metadata:
  stage: open-questions
  human-clarification: "false"
  plan-creation: "false"
  artefact-verification: "true"
---

# Open Questions (join barrier)

Runs when `state/session-index.md` has `Join: ready` (both roles complete). On platforms with script
execution, `aidlc-common/scripts/process-checker.js` verifies the barrier deterministically.

Reads `vision-document.md` + `technical-environment.md`, consolidates open questions, and flags
contradictions (e.g. the vision needs multi-region/compliance the constraints don't allow).
Reuse v1 `aidlc-discovery-rules/aidlc-discovery-rule-details/shared/open-questions-collector.md`.

## Output
`Product-Definition/open-questions.md` (consolidated, with a Contradictions section).
