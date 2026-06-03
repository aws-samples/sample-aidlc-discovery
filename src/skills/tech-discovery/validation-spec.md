# Tech Discovery — Validation Spec

## Inputs
- Artifact: `technical-environment.md`
- State: `state/technical-state.md`

## Rules
1. All sections present (Languages, Frameworks, Cloud Services, Architecture, Security, Testing, Example Code). Empty section → state "None identified".
2. Allow/deny lists captured as constraints, not as stack-design decisions.
3. Every answered question is traceable to a section.
4. Artifact rendered in the user's language; control tokens (`[Answer]:`, IDs) in English.
