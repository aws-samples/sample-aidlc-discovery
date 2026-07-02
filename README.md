# AI-DLC Discovery

> **Define what to build before AI builds it.**

> [!IMPORTANT]
> Generative AI can make mistakes. Review all output and costs from your chosen model and agent.
> See [AWS Responsible AI Policy](https://aws.amazon.com/ai/responsible-ai/policy/).

Independent **product-discovery** tool for Product Managers and tech leads: a guided, role-based interview
that produces `Product-Definition/` — a Vision Document, a Technical Environment Document, and pre-declared
open questions. AI-DLC is a **consumer** of that output, not its container.

## Why this exists

AI-DLC's quality depends on what you feed it. It expects a Vision Document and a Technical Environment
Document before Inception — but writing those from a blank page is slow and easy to skip. Teams either
show up with half-baked inputs (and spend the first hour answering clarifying questions) or skip the
documents entirely (and get generic output).

aidlc-discovery **replaces the blank page with a guided interview**: multiple-choice and short-text
questions, section by section, per role, with state saved between sessions. At the end you get the two
documents AI-DLC expects — formatted, validated, and with known ambiguities pre-declared.

## Who it's for

- **Product owners, PMs, business analysts** → a coherent Vision Document without a template crawl.
- **Tech leads, architects, staff engineers** → lock in the stack and constraints before code gets generated on wrong assumptions.
- **Teams where Business and Technical are different people** → progress persists per role (single-writer state), so each person works in their own session — even in parallel.

## What it produces

A `Product-Definition/` folder organised in three groups: control files (so the workflow can resume),
final outputs (what AI-DLC consumes), and a process workspace under `interview/`.

```
Product-Definition/
├── vision-document.md          # ✅ final output — what to build and why
├── technical-environment.md    # ✅ final output — tools and constraints
├── open-questions.md           # ✅ final output — pre-declared ambiguities
├── state/                      # control — session-index + per-role state (resume)
├── audit/                      # control — per-role audit log
├── interview/                  # process — per-role question buffers + answer history
└── visual/                     # optional — Mermaid user journey + HTML mockups
```

## Highlights

- **Skill-based** (agentskills.io) + a small orchestrator.
- **Multiplatform** via core + adapters + `build.js` (Kiro · Claude Code/Cowork · Amazon Quick).
- **Parallel roles** — PM ∥ tech lead, single-writer state per role + a deterministic join barrier.
- **Two interaction modes** — `batch` (file `[Answer]:`) or `conversational` (question-by-question in chat).
- **Quick/Full depth**, optional **Visual Sketch**, and a **paste-ready AI-DLC handoff** prompt.

## Build

```bash
node build.js            # all targets → dist/<target>/
node build.js kiro       # one target
```

## Install

| Platform | Bundle → destination | Entry point |
|---|---|---|
| Kiro IDE / CLI | `dist/kiro/.kiro/` → project `.kiro/` | `start aidlc-discovery` |
| Claude Code / Cowork desktop | `dist/claude/.claude/` → project `.claude/` | `/aidlc-discovery` |
| Amazon Quick desktop | `dist/amazon-quick/skills/aidlc-discovery/` → import via UI (Agents & skills → Skills → + Create → Import from file) | `start aidlc-discovery` |

Automated prompt install + per-platform reference tables → **[install.md](install.md)**.

## Pre-loading context from files or MCP

The workflow does not fetch or parse external sources itself. **But** the agent you run it on (Claude,
Kiro, Amazon Quick, etc.) can already read files, explore git repos, and query MCP servers. Leverage that
before — or alongside — the interview, and the agent uses the context when answering.

**The pattern:** add a short preamble to your invocation telling the agent what to read first. The
interview then starts normally, but its proposed answers are informed by what the agent saw.

**Example — Technical role with a local codebase:**
```
Before starting, read these as context:
  - ./README.md
  - ./package.json
  - ./docs/arch/system-overview.md
Then start aidlc-discovery for the Technical role. When a question can be answered from
those files, propose the answer with a short "(source: <file>)" note so I can verify.
Only ask me directly for what the files don't cover.
```

**Example — Business role with a vision doc:**
```
I have a vision doc at ./docs/Vision-v3.docx. Read it first, then start aidlc-discovery
for the Business role only. For each question, either propose an answer from the doc
(with a section reference) or tell me it's not covered and ask me.
```

**Example — MCP-connected sources (docs, wikis, repos):**
```
You have a documentation MCP server available (e.g. Confluence, or a public docs MCP).
Consult the relevant pages first, then start aidlc-discovery. Use what you found to
pre-fill what you can, citing the source inline as "(source: <URL>)". Ask me for the rest.
```

The same pattern works with any MCP server that exposes docs, wikis, or repositories — swap in your own.

## What it is **not**

- **Not a replacement for AI-DLC** — it is its *front door*.
- **Not a validator of business logic** — it asks the questions, you answer; it flags ambiguities but does not "grade" your vision.
- **Not a code generator** — no source code here; code generation happens in AI-DLC's Construction phase.
- **Not a UI builder** — the optional Visual Sketch produces static HTML mockups + a Mermaid user journey for review and alignment, never functional or runnable apps. Implementation belongs to AI-DLC Construction.
- **Not an automated extraction tool** — it does not crawl your repo or parse docs on its own. But you can ask the agent to pre-load context (see above). A rule-governed extraction mode with citations and contradiction detection is planned.

## Repo layout

```
src/skills/      discovery-orchestrator · product-discovery · tech-discovery · open-questions · visual-sketch
src/common/      protocols · conventions (question-format, state-schema, handoff-format) · scripts/process-checker.js
src/targets/     kiro · claude (Code + Cowork) · amazon-quick
build.js         assembles dist/<target>/
aidlc-discovery-rules/   question banks reused by the skills
```

## Key documentation

Read these in roughly this order — each builds on the previous.

- **[README.md](README.md)** — you are here. Why it exists, what it produces, install, what it is not.
- **[install.md](install.md)** — automated prompt install plus per-platform reference tables and commands.
- **[how-to-use.md](how-to-use.md)** — end-to-end walkthrough with a worked example and side-flows.
- **[CHANGELOG.md](CHANGELOG.md)** — version history and what shipped in each release.
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — how to file issues, structure PRs, and test changes.
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** — Amazon Open Source Code of Conduct.
- **[LICENSE](LICENSE)** — MIT-0.

## Status

Pre-release. All three adapters build and validate: Kiro (agent + hook), Claude Code/Cowork (slash command
+ hook), Amazon Quick (self-contained skill). Join barrier tested; Kiro flow validated end-to-end.

## License

MIT-0. See [LICENSE](LICENSE).
