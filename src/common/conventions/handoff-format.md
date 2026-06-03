# Handoff Format

At the end of the session the orchestrator prints a **paste-ready handoff prompt** so the user does not
have to figure out how to brief AI-DLC. It has two parts:

1. **A one-line instruction OUTSIDE any code fence** (localised to the user's language), e.g.
   *"Copy the block below and paste it into your AI-DLC session:"*.
2. **A fenced code block** with the prompt **in English** — AI-DLC interop: file paths and section names
   stay English even in non-English sessions. The fence must be copy-clean (no banner/progress inside).

## Prompt template (English, inside the fence)

    Using AI-DLC, start Requirements Analysis for this product. Before anything else, load these
    inputs from Product-Definition/:

    - vision-document.md — business vision: problem, target users, success metrics, MVP scope (IN/OUT), risks.
    - technical-environment.md — technical constraints: languages, frameworks, cloud, architecture, security, testing.
    - open-questions.md — <N> pre-declared ambiguities; resolve them before User Stories or Application Design.

    Treat the MVP "Features IN" list as the scope boundary. Honour the allow/deny lists in
    technical-environment.md as constraints, not suggestions.

### Optional block — include ONLY if the visual sketch exists

Append these lines inside the fence **only** when BOTH `Product-Definition/visual/user-journey.md` and at
least one `Product-Definition/visual/mockups/*.html` exist. Otherwise omit entirely (no orphan header):

    - visual/user-journey.md and visual/mockups/*.html — a UI sketch for alignment only (not a spec).

## Rules

- The instruction line localises; the fenced prompt stays English.
- Substitute `<N>` with the real open-questions count from `open-questions.md`.
- Derive the optional block from the filesystem, not from memory of whether the user opted in.
