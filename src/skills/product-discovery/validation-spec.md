# Product Discovery — Validation Spec

## Inputs
- Artifact: `vision-document.md`
- State: `state/business-state.md`

## Rules
1. All sections present (Executive Summary, Problem, Target Users, Success Metrics, Full Vision, MVP IN, MVP OUT, Risks/Open). Empty section → state "None identified".
2. MVP IN and MVP OUT present and non-empty (prevents scope creep).
3. Every answered question is traceable to a section (complete coverage).
4. Artifact rendered in the user's language; control tokens (`[Answer]:`, IDs) in English.
