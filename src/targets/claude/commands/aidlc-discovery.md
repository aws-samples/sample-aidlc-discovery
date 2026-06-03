---
description: Start the AI-DLC Discovery interview (vision + technical constraints → Product-Definition/)
---

Load and follow `.claude/skills/discovery-orchestrator/SKILL.md`, which points to
`.claude/aidlc-common/protocols/orchestrator-protocol.md` as the single source of truth for the flow.

Run the guided discovery interview in the current working directory, producing the `Product-Definition/`
folder (vision-document.md, technical-environment.md, open-questions.md). Default interaction mode is
`batch` (file-based `[Answer]:`); the user may choose `conversational`. Respond in the user's language;
keep control tokens (`[Answer]:`, IDs, `ready`) and control files in English.
