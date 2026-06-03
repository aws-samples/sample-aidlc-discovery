# AI-DLC Discovery

> **Define what to build before AI builds it.**

> [!IMPORTANT]
> Generative AI can make mistakes. Review all output and costs from your chosen model and agent.
> See [AWS Responsible AI Policy](https://aws.amazon.com/ai/responsible-ai/policy/).

Independent **product-discovery** tool for Product Managers and tech leads: a guided, role-based interview
that produces `Product-Definition/` (vision + technical constraints + pre-declared open questions).
AI-DLC is a **consumer** of that output, not its container.

Walkthrough: [how-to-use.md](how-to-use.md).

## What it produces

```
Product-Definition/
├── vision-document.md          # business vision: problem, users, metrics, MVP IN/OUT, risks
├── technical-environment.md    # technical constraints: stack, architecture, security, testing
├── open-questions.md           # ambiguities to resolve before AI-DLC
├── state/ · interview/ · audit/  # session state, per-role buffers + answer history, audit
└── visual/                     # optional Mermaid user journey + HTML mockups
```

## Highlights

- **Skill-based** (agentskills.io) + a small orchestrator, instead of monolithic rules.
- **Multiplatform** via core + adapters + `build.js` → `dist/<target>/` (Kiro · Claude Code/Cowork · Amazon Quick).
- **Parallel roles** — PM ∥ tech lead in separate sessions, per-role single-writer state + a deterministic join barrier.
- **Two interaction modes** — `batch` (file `[Answer]:`) or `conversational` (question-by-question in chat).
- **Quick/Full depth**, optional **Visual Sketch**, and a **paste-ready AI-DLC handoff** prompt.
- The interview content (question banks) is reused from the original rule set, not rewritten.

## Optional: pre-load context & on-demand stages

The agent can draw on what it already has access to, to **pre-fill** answers (you still review/approve each one):

- **Local files** — ask it to read existing docs first: *"read ./README.md and ./docs/spec.md, then start aidlc-discovery"*.
- **MCP servers** — if you have an MCP configured, ask it to pull context: *"use the Confluence MCP to fetch the architecture page, then start aidlc-discovery"*.
- **On-demand stages** — ask any time for *"make a visual sketch"* or to *"show the AI-DLC handoff prompt"*.

## Build

```bash
node build.js            # all targets → dist/<target>/
node build.js kiro       # one target
```

Each bundle = the shared **core** (`src/skills` + `src/common` + question banks) plus the platform **adapter**.

## Install (per platform)

| Platform | Bundle → destination | Entry point |
|---|---|---|
| Kiro IDE / CLI | `dist/kiro/.kiro/` → project `.kiro/` | `start aidlc-discovery` (agent) |
| Claude Code / Cowork desktop | `dist/claude/.claude/` → project `.claude/` | `/aidlc-discovery` (slash command) |
| Amazon Quick desktop | `dist/amazon-quick/skills/aidlc-discovery/` → `~/.quickwork/profiles/federate-prod/skills/` | `start aidlc-discovery` (skill) |

**Per-platform reference tables (Piece · Location · Role) and exact commands → [install.md](install.md).**

## Repo layout

```
src/skills/      discovery-orchestrator · product-discovery · tech-discovery · open-questions · visual-sketch
src/common/      protocols · conventions (question-format, state-schema, handoff-format) · scripts/process-checker.js
src/targets/     kiro · claude (Code + Cowork) · amazon-quick
build.js         assembles dist/<target>/
dist/<target>/   build output (gitignored)
aidlc-discovery-rules/   question banks reused by the skills
```

## Status

Pre-release (last stable target). All three adapters build and validate: **Kiro** (agent + hook),
**Claude Code/Cowork** (slash command + hook), **Amazon Quick** (self-contained skill). Join barrier
tested; Kiro flow validated end-to-end.

## License

MIT-0. See [LICENSE](LICENSE).
