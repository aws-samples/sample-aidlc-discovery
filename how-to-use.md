# How to use aidlc-discovery

This guide walks through a complete session end-to-end, then covers the three most common side-flows (resume, change an answer, hand off to AI-DLC).

If you haven't read the [README](README.md) yet, start there.

---

## Table of Contents

1. [Before you start](#before-you-start)
2. [End-to-end example — OrderFlow Real-Time Inventory Sync](#end-to-end-example)
   - [Session start & role selection](#1-session-start--role-selection)
   - [Project type](#2-project-type)
   - [Business role — depth selection](#3-business-role--depth-selection)
   - [Answering a batch](#4-answering-a-batch)
   - [Business completion gate](#5-business-completion-gate)
   - [Technical role](#6-technical-role)
   - [Visual Sketch (optional)](#7-visual-sketch-optional)
   - [Final handoff](#8-final-handoff)
3. [Side-flow — resuming a session](#side-flow-1-resuming-a-session)
4. [Side-flow — changing an answer you already gave](#side-flow-2-changing-an-answer)
5. [Side-flow — handing off to AI-DLC](#side-flow-3-handing-off-to-ai-dlc)
6. [Side-flow — using another language](#side-flow-4-using-another-language)
7. [Side-flow — pre-loading context from files or MCP](#side-flow-5-pre-loading-context-from-files-or-mcp)
8. [Tips from real sessions](#tips-from-real-sessions)
9. [Troubleshooting](#troubleshooting)

---

## Before you start

### What you need

- A workspace folder where the tool will create `Product-Definition/`
- An AI assistant that can read local files, write files, and follow multi-step markdown instructions (Claude Code, Cursor, Amazon Q Developer, etc.)
- ~10 min (Quick pass) to ~60 min (Full interview, both roles) of focused time

### What you do NOT need

- You do not need to know what "greenfield" or "brownfield" means — the tool asks in everyday language.
- You do not need to have written anything beforehand — answer what you know, use X) or the free-text fields for the rest.
- You do not need to finish in one sitting — state persists across sessions.
- You do not need to work in English. The tool renders every question, message, and final document in your workspace's language (Spanish, Portuguese, French, Japanese, etc.). Control files (`aidlc-discovery-state.md`, `audit.md`) stay in English for AI-DLC interop. See the [Language support section in the README](README.md#language-support).

### Invocation

**If you have installed aidlc-discovery in this project** (via the prompt in [install.md](install.md) — recommended), invoke it naturally in any chat:

```
start aidlc-discovery
```

Also accepted: `inicia aidlc-discovery`, `prepare AI-DLC discovery`, `run aidlc-discovery`.

**If you have not installed it** (or your agent does not load project rules), use the universal fallback — works in any agent that can read local files:

```
Read .aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md
and execute the workflow in the current working directory.
```

Either entry point triggers the same workflow described below.

---

## End-to-end example

We'll simulate a real session for a fictional team adding a real-time inventory sync feature to an existing platform called OrderFlow. The user is Laura, a Product Manager who will do both roles herself because the team is small.

### 1. Session start & role selection

**You type** (after running the install prompt once per project):

```
start aidlc-discovery
```

Or, if aidlc-discovery is not installed in this project yet, the universal fallback:

```
Read .aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md
and execute the workflow in the current working directory.
```

**The tool shows:**

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                        AI-DLC DISCOVERY                          ║
║              Define what to build before AI builds it            ║
║                                                                  ║
║  A role-based interview workflow that produces the two           ║
║  canonical inputs AI-DLC needs before Inception:                 ║
║                                                                  ║
║    1) Vision Document             (Business role)                ║
║    2) Technical Environment Doc   (Technical role)               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

How this works
──────────────
  • You pick a role: Business, Technical, or Both (sequential).
  • You pick a depth: Quick pass (~10 min) or Full interview (~25 min).
  • I ask questions in a markdown file, not in chat.
  • You fill in the [Answer]: tags.
  • When you're done with a batch, reply with a single word: ready
  • I re-read the file, validate, and move on.
  • Progress is shown at the top of every batch.
  • You can stop mid-way and resume later — state is saved per question.
```

Then the tool writes `Product-Definition/interview/role-selection.md`:

```markdown
# Role Selection

## Question: Which role are you taking in this session?

A) Business  — I own the "what and why". I want to produce the Vision Document.
B) Technical — I own the "which tools and constraints". I want to produce the Technical Environment Document.
C) Both (sequential) — I will fill in Business first, then Technical.
X) Other (describe after [Answer]: tag below)

[Answer]:

---

When you're done, reply with a single word: **ready**
```

**Laura opens the file, edits it to:**

```markdown
[Answer]: C — same person filling in both; we want a coherent single pass
```

**Laura types in chat:**

```
ready
```

**The tool re-reads, validates, and updates state.** It now proceeds to project type.

---

### 2. Project type

The tool writes `Product-Definition/interview/project-type.md`:

```markdown
# Project Type

## Question: Which best describes this project?

A) **Brand-new project** — we are building something from scratch. There is no
   existing code, and no existing system we must integrate with or preserve.

B) **New feature on an existing product** — there is already a system in
   production (or built), and we are adding a capability to it. Existing code,
   schemas, APIs, or users must continue to work.

C) **Migration / modernisation of an existing system** — there is a system
   in place and we are rebuilding, replatforming, or replacing part of it.
   Some existing contracts or data will carry over.

X) Other — describe after [Answer]: below
   (example: "mostly brand-new but we must connect to one existing service
   for authentication")

[Answer]:

---

When you're done, reply with a single word: **ready**
```

**Laura answers:**

```markdown
[Answer]: B — adding real-time inventory sync to our existing OrderFlow platform (live in production since 2022)
```

Because the answer is B (there is an existing system), the tool asks a follow-up in the same file:

```markdown
## Question: How can I learn about your existing system?

Pick whichever is easiest — later interview questions are smoother when I have
something to look at, but prose also works.

A) The existing code is in this workspace or in a repository I can read —
   tell me the path and I'll explore it as needed.

B) No code access, but I have documents (architecture notes, ADRs, wiki pages,
   screenshots) — I'll share the paths or links when the interview asks.

C) Neither — I'll describe the existing system in my own words when the
   interview asks.

X) Other

[Answer]:
```

**Laura answers:**

```markdown
[Answer]: A — codebase is at /workspace/orderflow-platform; architecture docs live at /workspace/docs/arch/
```

**Laura replies `ready`.**

The tool records both answers, maps internally (B → Brownfield), updates state, and moves to the Business interview.

---

### 3. Business role — depth selection

First thing in the Business role, the tool writes `Product-Definition/interview/business/vision-questions.md`:

```markdown
# Business Interview — Depth Selection

Pick the interview depth. You can upgrade Quick → Full later if needed.

A) **Quick pass** (~8 questions, ~10 min)
   Core-only questions. Good for prototypes, POCs, internal tools, or when
   you already have most of the answers in your head.

B) **Full interview** (~18 questions, ~25 min)
   Covers every section of the Vision Document guide. Recommended for
   production-grade projects and cross-team initiatives.

X) Other (e.g. "Full but skip Risks section" — describe after [Answer]:)

[Answer]:

---

When you're done, reply with a single word: **ready**
```

**Laura:** `[Answer]: B` → replies `ready`.

The tool records the depth and builds the question set. Because project type is Brownfield, it adds QB1 and QB2 to the end.

---

### 4. Answering a batch

The tool writes the first batch into `Product-Definition/interview/business/vision-questions.md`:

```markdown
# Business Interview — Section 1 of 6: Executive Summary

Progress: ░░░░░░░░░░ 0/20 questions  ·  ~20 min remaining

This batch covers Q1–Q5. Fill in the [Answer]: tags below,
then reply with **"ready"** and I'll validate your answers and move on.

## How to answer

- For multiple-choice questions, put the letter first, then a short label:
  `C — financial summary and debt service coverage` is clearer than just `C`.
- For free-text questions, write directly under `[Answer]:`.
- For tables, replace the example row and keep the column headers exactly as shown.
- Include a brief justification when it's not obvious.
- Combine options when you mean both: `B and C`.
- Use X freely. If no option fits, X is the right choice.
- To change a prior answer later, just tell me "I want to change my answer to Q{N}".

## Question 1: What is the project name and type?

Tell me the project's working name and pick the category that best fits.

A) A new internal tool / platform
B) A new customer-facing product
C) A significant addition to an existing product
D) A migration / modernisation effort
X) Other — describe

[Answer]:

## Question 2: Who is the primary target user, in one sentence?

Keep it to a single sentence. We'll go into detail on user types in Q8.

Example: "Mid-size retail operations managers who track inventory across
multiple stores."

[Answer]:

## Question 3: What is the core capability this product provides?

Describe the single most important thing the product does, in one sentence.

Example: "Unifies inventory, orders, and supplier data in one dashboard
and pushes real-time alerts when stock falls below threshold."

[Answer]:

## Question 4: What business problem does this solve?

A) A tool-fragmentation / manual-process problem (people are stitching work together by hand)
B) A missing-capability problem (customers are asking for something we don't offer)
C) A compliance / regulatory problem (we must do this by a deadline)
D) A cost / efficiency problem (an existing process is too expensive or slow)
X) Other — describe

[Answer]:

## Question 5: What is the single most important measurable outcome you want to achieve?

Express as a number and a direction.

Examples:
  • "30% reduction in order processing time"
  • "Eliminate manual inventory reconciliation entirely (0 hours/week)"
  • "Cut time-to-onboard from 5 days to 1 day"

[Answer]:

---

When you're done, reply with a single word: **ready**

(I'll re-read this file from disk and validate your answers.)
```

**Laura fills it in:**

```markdown
## Question 1: What is the project name and type?
...
[Answer]: C — A significant addition to an existing product; project name is "OrderFlow Real-Time Inventory Sync"

## Question 2: Who is the primary target user, in one sentence?
...
[Answer]: Store managers and regional inventory planners at mid-size retail chains (10–200 stores)

## Question 3: What is the core capability this product provides?
...
[Answer]: Real-time (sub-2-second) inventory visibility and alerting across a chain's store network

## Question 4: What business problem does this solve?
...
[Answer]: A — tool-fragmentation. Managers stitch inventory data from CSV dumps, spreadsheets, and phone calls to sister stores

## Question 5: What is the single most important measurable outcome you want to achieve?
...
[Answer]: Reduce stock-out incidents by 40% within 6 months of rollout across the pilot chains (measured via OrderFlow's existing stockout-event table)
```

**Laura saves the file and replies in chat:**

```
ready
```

**The tool does several things in one turn:**

1. Re-reads `vision-questions.md` from disk.
2. Validates each `[Answer]:`:
   - Q1 starts with `C` ✓
   - Q2–Q3 are non-empty prose ✓
   - Q4 starts with `A` ✓
   - Q5 has a number (40%) and a direction (reduction) ✓
3. Appends the whole batch to `vision-answers-history.md` in one write:

   ```markdown
   ## Batch — Section 1, Q1–Q5   — 2026-04-28T09:34:12Z

   ### Q1: Project name and type
   **Answer**: C — A significant addition to an existing product; project name is "OrderFlow Real-Time Inventory Sync"

   ### Q2: Target users one-liner
   **Answer**: Store managers and regional inventory planners at mid-size retail chains (10–200 stores)

   ### Q3: Core capability
   **Answer**: Real-time (sub-2-second) inventory visibility and alerting across a chain's store network

   ### Q4: Business problem
   **Answer**: A — tool-fragmentation

   ### Q5: Measurable outcome
   **Answer**: Reduce stock-out incidents by 40% within 6 months of rollout...
   ```

4. Updates `aidlc-discovery-state.md` — Q1–Q5 all `[x]` now.
5. Logs one entry in `audit.md` with stage label `Business Interview — Batch Q1–Q5 validated`.
6. Writes the next batch (Section 2: Q6–Q10) into `vision-questions.md`, replacing the previous batch. Progress header now shows:

   ```
   Progress: █████░░░░░░░░░░░░░░░ 5/20 questions  ·  ~15 min remaining
   ```

The cycle repeats for Sections 2 through 6, then for the Existing System questions (QB1, QB2).

#### What a table question looks like when answered

For Q8 (Target users table), the tool wrote an example row and an empty slot. Laura replaces the example with her own data:

```markdown
## Question 8: List each user type and their primary need.

Replace the example row below with your own. Add or remove rows as needed.
Put your final table under [Answer]:.

**Example (do not submit as your answer):**

| Role | Description | Primary Need |
|------|-------------|--------------|
| (e.g.) Store Manager | Oversees daily ops at one retail location | Real-time inventory visibility across her store and sister stores |

[Answer]:

| Role | Description | Primary Need |
|------|-------------|--------------|
| Store Manager | Runs one retail location; makes daily replenishment decisions | Real-time view of in-store and sister-store inventory |
| Regional Planner | Oversees 10–25 stores; handles redistributions | Aggregated stock levels + low-stock alerts across region |
| Chain HQ Ops Lead | Our direct customer | API access to inventory events for their BI tools |
```

The tool validates that each row has all three columns filled.

---

### 5. Business completion gate

After QB2 is answered and all 20 boxes are `[x]`, the tool doesn't silently move on. It runs the completion gate:

1. Scans for open questions (user wrote "TBD", "not sure", "legal review pending", etc.) → appends them to `Product-Definition/open-questions.md` as OQ-B-1, OQ-B-2, OQ-B-3.
2. Renders `Product-Definition/vision-document.md` from the answers history.
3. Shows this message in chat:

```
Vision Document complete — review before we continue.

  Product-Definition/vision-document.md is ready for your review.

Your options:

  1) Request Changes — tell me what to fix and I'll update the document
     (and back-propagate to vision-answers-history.md and aidlc-discovery-state.md).

  2) Approve and Continue — mark Business as ✅ complete and
     (if your role selection is "Both (sequential)") move on to the
     Technical interview.

What would you like to do?
```

**Laura reads `vision-document.md`.** The opening section looks like this:

```markdown
# Vision Document — OrderFlow Real-Time Inventory Sync

Generated by aidlc-discovery on 2026-04-28T11:32:11Z.
Project type: Brownfield

---

## Executive Summary

OrderFlow Real-Time Inventory Sync is a new capability layered onto the existing
OrderFlow order-management platform. It gives store managers and regional
planners at mid-size retail chains a sub-2-second view of inventory across their
entire store network, replacing the current 12–24h nightly CSV process. The
expected outcome is a 40% reduction in stock-out incidents within 6 months of
rollout at the pilot chains.

---

## Business Context

### Problem Statement
Mid-size retail chains run multiple store locations with independent OMS
instances. Inventory data reaches the OrderFlow dashboard through nightly CSV
exports, which means a customer asking "do you have this in size M?" in a store
often gets wrong answers because the data is up to 24h stale...

### Target Users and Stakeholders

| Role | Description | Primary Need |
|------|-------------|--------------|
| Store Manager | Runs one retail location... | Real-time view of in-store and sister-store inventory |
| Regional Planner | Oversees 10–25 stores... | Aggregated stock levels + low-stock alerts across region |
| Chain HQ Ops Lead | Our direct customer | API access to inventory events for their BI tools |

### Success Metrics

| Metric | Current State | Target State | Measurement Method |
|--------|---------------|--------------|--------------------|
| Stock-out incidents/week | 450 avg | 270 avg (-40%) | OrderFlow stockout_events table |
| Data staleness | 12–24h | <2s p95 | Grafana dashboard on sync-latency metric |
| "Is it in stock?" resolution time | 30–45 min | <30s | Customer survey Q3 + Q4 2026 |

... and so on through MVP Scope IN, MVP Scope OUT, Risks, Current State, What Must Not Change.
```

**Laura notices the Executive Summary says "mid-size retail chains" but she wanted to emphasise that the anchor customer is specifically fashion retail.**

```
Request Changes. In the Executive Summary, specify "mid-size fashion retail chains" instead of just "mid-size retail chains". Also in Target Users.
```

The tool:

1. Appends a correction entry to `vision-answers-history.md` (not an overwrite — the original wrong answer is preserved for audit):

   ```markdown
   ## Correction — 2026-04-28T11:28:04Z
   **Scope**: Q2 target-users one-liner; affects Executive Summary and §Business Context/Target Users prose
   **User Input**: "specify 'mid-size fashion retail chains' instead of just 'mid-size retail chains'"
   **New value**: Store managers and regional inventory planners at mid-size **fashion** retail chains (10–200 stores)
   ```

2. Re-renders `vision-document.md`.
3. Re-presents the gate.

**Laura approves:**

```
Approve and continue
```

The tool:
1. Marks Business ✅ in `aidlc-discovery-state.md`.
2. Logs the approval in `audit.md`.
3. Moves on to the Technical interview.

---

### 6. Technical role

The Technical role runs the same way as Business:

1. **Context load**: reads `vision-document.md` (now that it exists) to align NFR suggestions with the MVP priorities Laura already declared.
2. **Depth selection**: asks Quick (~12 min) vs Full (~35 min). Laura picks Full because this is a production system.
3. **Section T1–T8 + Existing System**: 33 questions total. Batches of 5–7.

When Laura hits Section T8 (Example Code Patterns), she uses option B for all four questions because she has a real codebase:

```markdown
## Question T26: Example endpoint pattern

There are three valid ways to answer:

A) Paste a canonical snippet below inside a code fence
B) Point me to a file path I can read
C) Skip — we'll infer from framework conventions
X) Other

[Answer]: B — see /workspace/orderflow-platform/services/inventory-sync/src/handlers/
```

The tool records the path. It does not need the snippet pasted — AI-DLC will load the real file during Code Generation.

After the final batch, the completion gate runs:

1. Adds OQ-T-1 and OQ-T-2 to `open-questions.md`.
2. Renders `technical-environment.md`.
3. Presents the 2-option gate.

Laura approves.

---

### 7. Visual Sketch (optional)

Right before the final handoff the tool offers an opt-in stage:

```
Visual Sketch — Optional

Now that the documents are approved, you can optionally generate a visual
sketch of the product: a user-journey flowchart and lightweight HTML mockups
of the main screens. Adds ~10–15 min.

A) Yes — generate the user journey + HTML mockups
B) No — skip and go straight to the AI-DLC handoff

[Answer]:
```

Laura picks **A**. The tool writes a 5-question batch into
`Product-Definition/interview/visual/visual-questions.md` covering persona, depth (happy
path vs happy path + error paths), style (wireframe / lo-fi / branded), sample
data (realistic vs placeholder) and viewport (desktop / mobile / both).

Once Laura replies `ready`, the tool reads the Vision and Technical Environment
docs, asks the IDE / agent to generate:

- `Product-Definition/visual/user-journey.md` — a Mermaid `flowchart TD` per
  selected persona, with one node per screen and verb-phrase edges.
- `Product-Definition/visual/mockups/<NN>-<slug>.html` — one self-contained
  Tailwind-CDN HTML file per journey node, every screen wearing an amber
  "🎨 MOCKUP — not functional" banner so reviewers cannot mistake them for
  product.
- `Product-Definition/visual/mockups/index.html` — a hub linking to every
  screen in journey order.

Each agent generates with whatever it has: Kiro / Cursor / Claude Code produce
proper HTML; agents without HTML write capability fall back to ASCII wireframes
in markdown. The contract (one node = one screen, primary CTA matches edge,
banner present, no fabricated features) is the same.

A 3-option gate runs at the end (Request Changes / Approve and Continue /
Discard and Skip). Laura approves.

---

### 8. Final handoff

With both roles ✅ complete and the Visual Sketch stage resolved (approved, skipped, or discarded), the tool prints the handoff prompt below. The OPTIONAL block appears only if you approved the Visual Sketch — it is omitted when the stage was skipped or discarded.

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   AI-DLC Discovery Complete ✅                                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

To kick off AI-DLC, paste this into a fresh context:

  I'm starting a new project. Please read the following inputs before
  beginning the AI-DLC workflow:

  REQUIRED inputs (always present):

  • Product-Definition/vision-document.md
    The Vision Document — what we're building, who it's for, the success
    metrics, and what's in/out of MVP scope. Use this as the primary input
    to Requirements Analysis.

  • Product-Definition/technical-environment.md
    The Technical Environment Document — required languages, frameworks,
    cloud services, architecture patterns, security/compliance constraints,
    testing standards, and example code patterns. These are binding
    constraints for NFR Requirements, NFR Design, Infrastructure Design,
    and Code Generation.

  • Product-Definition/open-questions.md
    Pre-declared ambiguities and open items the user already knows about.
    Treat each as a clarifying question to resolve during Requirements
    Analysis — do not silently assume defaults.

  OPTIONAL inputs (only if Visual Sketch was approved — check if folder exists):

  • Product-Definition/visual/user-journey.md
    Mermaid flowchart(s) showing the user journey through the product per
    persona. Use as reference for UX flows when designing requirements
    and APIs.

  • Product-Definition/visual/mockups/index.html and the screen files
    Self-contained HTML mockups of the main screens. NOT functional code —
    they are visual references for primary CTAs, screen-to-screen
    navigation, and the data each screen displays. Cross-reference against
    user-journey.md.

  Please confirm you've read all available files, then begin the AI-DLC
  workflow at the Inception phase.
```

See [Side-flow — handing off to AI-DLC](#side-flow-3-handing-off-to-ai-dlc) for more detail.

---

## Side-flow 1: resuming a session

**Scenario**: Laura did Business yesterday (Monday). She's back Wednesday morning for the Technical role.

**She invokes the tool the same way:**

```
Read .aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md and execute.
```

**The tool detects `Product-Definition/aidlc-discovery-state.md` exists.** No welcome banner this time — instead:

```
Existing aidlc-discovery session detected.

Session created:   2026-04-27T09:15:22Z
Last updated:      2026-04-28T11:32:11Z
Project type:      Feature on existing

Role progress
─────────────
  Business (Vision):            ✅ Complete (20/20)
  Technical (Technical Env):    ⚪ Not Started  (0/33)

What would you like to do?

  A) Continue Business from the next unanswered question
     (no unanswered questions — Business is complete)
  B) Start the Technical role now
     (Vision Document will be loaded as context for coherence)
  C) Review / edit a specific section of Business (marked ✅)
  X) Other (describe)

[Answer]:
```

**Laura:** `B` → tool proceeds to the Technical role.

### Resuming mid-batch

If Laura had left mid-Business (say, 7/20 questions answered), the resume summary would show:

```
Role progress
─────────────
  Business (Vision):            ⏳ In Progress (7/20)
  Technical (Technical Env):    ⚪ Not Started

What would you like to do?

  A) Continue Business from Q8 (Target users and stakeholders)
  B) Switch to the Technical role now (Business stays paused)
  C) Review / edit a specific section
  X) Other
```

State granularity is per-question, so the tool knows exactly that Q1–Q7 are `[x]` and Q8 is next.

---

## Side-flow 2: changing an answer

**Scenario**: Laura is halfway through the Technical interview when she realises her Q14 answer (SQL only) is wrong — the team has already decided to use DynamoDB for the new event store.

**In chat, she says:**

```
I want to change my answer to Q14. We're using DynamoDB for the new event store, not SQL.
```

**The tool:**

1. Finds Q14 in `aidlc-discovery-state.md` under `## Business Questions`. It's `[x]`.
2. Reads the Q14 entry from `vision-answers-history.md`.
3. Writes a correction question into the current `vision-questions.md`:

```markdown
# Correction to Q14: Data patterns

You previously answered: `A — Relational / SQL only`

What's the new answer?

A) Relational / SQL
B) Document / NoSQL
C) Key-value
D) Search index
E) In-memory cache
F) Event log / streaming
X) Other (combine letters if multiple)

[Answer]:

---

When you're done, reply with a single word: **ready**
```

Wait — Q14 is a Business question, not Technical. Let me redo the example to avoid confusion:

**Scenario (corrected)**: Laura is halfway through Technical when she realises her T14 (Data patterns) answer was incomplete. She originally put `A — SQL only` but wants to add DynamoDB.

She says:

```
Change my answer to T14. Add DynamoDB — we're going with SQL for the existing schema and DynamoDB for the new event store.
```

**The tool:**

1. Locates T14 in state — it's `[x]`.
2. Appends a **correction entry** to `tech-env-answers-history.md` (does NOT overwrite the original):

   ```markdown
   ## Correction — 2026-04-28T13:44:22Z
   **Scope**: T14 (Data patterns)
   **Original answer**: A — Relational / SQL
   **New answer**: A and B — SQL (MySQL) for existing schema; DynamoDB for new inventory event store
   **User Input**: "Change my answer to T14. Add DynamoDB — we're going with SQL for the existing schema and DynamoDB for the new event store."
   **Downstream impact**: Affects Section T5 §Existing Stack Inventory (add DynamoDB), §Data Patterns prose in final doc
   ```

3. Keeps the `[x]` marker in state (the question is still answered, just corrected).
4. Logs the correction in `audit.md` with stage label `Technical Interview — Correction T14`.
5. Asks if the change affects any downstream questions already answered (e.g. T11 allow-list now needs DynamoDB):

```
T14 updated. This change may affect previous answers:
  - T11 (Cloud services allow-list): should DynamoDB be added?

  A) Yes, add DynamoDB to T11 allow-list
  B) No, T11 is already correct
  X) Other

[Answer]:
```

This back-propagation step is what keeps the final document coherent even when answers change mid-stream.

---

## Side-flow 3: handing off to AI-DLC

At the end of the session, you have three required files AI-DLC needs, plus an optional visual sidecar if you ran the Visual Sketch stage:

**Required**

- `Product-Definition/vision-document.md`
- `Product-Definition/technical-environment.md`
- `Product-Definition/open-questions.md`

**Optional (only if Visual Sketch was approved)**

- `Product-Definition/visual/user-journey.md`
- `Product-Definition/visual/mockups/index.html` and the screen files

### Option 1 — Same AI assistant, fresh context

The simplest handoff: close the current chat / session / window, start a new one, then paste the handoff prompt the tool printed at the end (the one in [Final handoff](#8-final-handoff)). It tells AI-DLC the path of every file and what each one contains.

If you skipped or discarded Visual Sketch, the tool already omitted the OPTIONAL block from the printed prompt, so you can just paste it as-is.

### Option 2 — Different AI assistant or later session

Same prompt, same files. The documents are self-contained markdown — they do not depend on the `aidlc-discovery-state.md` or `audit.md` history. You can move them to any workspace and hand them to any AI that runs the AI-DLC workflow.

### What AI-DLC will do with each file

| File | AI-DLC's use |
|---|---|
| `vision-document.md` | Primary input to Requirements Analysis. Skips "what are we building?" clarifying questions. |
| `technical-environment.md` | Binding constraints for NFR Requirements, NFR Design, Infrastructure Design, and Code Generation. |
| `open-questions.md` | First batch of clarifying questions AI-DLC will present in the `requirement-verification-questions.md` file. |
| `visual/user-journey.md` (optional) | Reference for UX flows when designing requirements and APIs. |
| `visual/mockups/*.html` (optional) | Visual references for primary CTAs, screen-to-screen navigation, and the data each screen displays. NOT functional code — Construction phase regenerates real components. |

### What to keep from the `Product-Definition/` folder

After handoff, you can delete or archive the `interview/` folder (initial setup answers, per-batch question files, answer history) if you want. But keep:

- `vision-document.md` and `technical-environment.md` — AI-DLC references them throughout the workflow.
- `open-questions.md` — AI-DLC consumes it during Requirements Analysis.
- `visual/` — if you ran Visual Sketch, useful for stakeholder alignment and as Construction-phase context.
- `audit.md` — valuable for post-mortems or compliance review; never deleted.
- `aidlc-discovery-state.md` — small, keep it for future reference (e.g. if you re-run this tool for a v2).

---

## Side-flow 4: using another language

The tool adapts automatically. You generally don't have to do anything special — it picks up your language from your invocation, your workspace steering files (`CLAUDE.md`, `.cursorrules`, `.kiro/steering/`, `AGENTS.md`), or explicit instruction. Here's what changes and what doesn't.

### Starting in a non-English workspace

Laura's team has `CLAUDE.md` in Spanish. She invokes:

```
Lee .aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md y ejecuta.
```

The tool detects Spanish from both her prompt and the steering file, then confirms once:

```
He detectado que prefieres trabajar en español. Lo usaré para todas las
preguntas, los documentos finales y los mensajes. Los archivos de control
(aidlc-discovery-state.md y audit.md) se mantienen en inglés porque AI-DLC los
consume en ese idioma.

¿Confirmas? (sí / no / usa otro idioma)
```

Laura replies `sí`. From that point on, the welcome banner, every question, the progress header, the gate messages, and the final `vision-document.md` + `technical-environment.md` are all in Spanish.

**What a Spanish question batch looks like:**

```markdown
# Entrevista de Negocio — Sección 1 de 6: Resumen Ejecutivo

Progreso: ░░░░░░░░░░ 0/20 preguntas  ·  ~20 min restantes

Este bloque cubre Q1–Q5. Completa los campos [Answer]: abajo y luego
responde **"listo"** para que revise tus respuestas y continuemos.

## Pregunta 1: ¿Cuál es el nombre y el tipo de proyecto?

...

A) Una nueva herramienta / plataforma interna
B) Un nuevo producto de cara al cliente
C) Una adición significativa a un producto existente
D) Un esfuerzo de migración / modernización
X) Otro — describe

[Answer]:

---

Cuando termines, responde con una sola palabra: **listo**

(Volveré a leer el archivo desde el disco y validaré tus respuestas.)
```

Note:
- Question text and options are in Spanish.
- The `[Answer]:` tag stays in English — the tool parses it by string match.
- Question identifier `Q1` stays in English for downstream interop.
- The accepted trigger word in Spanish is `listo` (English `ready` is also accepted as a safety net).

### Control files stay in English

Even in a Spanish session, `aidlc-discovery-state.md` still looks like:

```markdown
## Session Metadata
- User Language: es
- Language Source: steering:CLAUDE.md
- Business Depth: Full
- Current Role: Business

## Role Progress
- Business (Vision Document):  ⏳ In Progress (5/20)
- Technical (Technical Env):   ⚪ Not Started
```

The section headers and metadata keys are in English. If AI-DLC (or a future operator) opens this file, they can read the state without translation.

Same for `audit.md` — stage labels stay in English (`Business Interview — Batch Q1–Q5 validated`), but the user's raw input field preserves the original (Spanish) text verbatim.

### Switching language mid-session

If Laura wants to change from Spanish to English partway through, she says so:

```
Let's switch to English from here.
```

The tool updates `User Language: en` in the state, logs the change in `audit.md` (stage label `Language Changed`), and renders the NEXT batch in English. Previously-generated Spanish content is not retranslated (to preserve the audit trail) — so `vision-answers-history.md` will have mixed Spanish (batches 1–2) and English (batches 3+) blocks. That is intentional and correct.

### Asking for a bilingual final render

If the session is in Spanish but Laura needs to hand off to an English-only AI-DLC team, at the final gate she says:

```
Please also produce English versions of the final documents.
```

The tool generates:

- `vision-document.md` (Spanish, the primary)
- `vision-document.en.md` (English, for handoff)
- `technical-environment.md` (Spanish)
- `technical-environment.en.md` (English)

Both records go in the state file. The handoff message lists the English ones as the canonical files to paste into AI-DLC.

### Supported languages

Any language the underlying AI assistant handles well. Tested patterns work for: English, Spanish, Portuguese, French, German, Italian, Japanese, Simplified Chinese. Right-to-left languages (Arabic, Hebrew) are supported; the tool preserves the text direction and does not reverse tables or code fences.

**The canonical "ready" trigger** varies by language but accepts fallbacks:

| Language | Printed in footer | Also accepted |
|---|---|---|
| English | `ready` | `done`, `go` |
| Spanish | `listo` | `ya`, `ready` |
| Portuguese | `pronto` | `ready` |
| French | `prêt` | `ready` |
| Japanese | `準備完了` | `ok`, `ready` |
| Chinese (Simplified) | `好了` | `完成`, `ready` |

English `ready` always works as a safety net.

---

## Side-flow 5: pre-loading context from files or MCP

The workflow doesn't read your files or MCP servers by itself. But the AI agent you are running it on (Claude, Kiro, Cursor, Amazon Q) already knows how to do that. You can use that capability *before* the workflow starts, and the agent will apply the context while answering the interview. No rule changes needed — only your invocation prompt.

### When this helps

- Adding a feature to an existing codebase (the tech stack is already decided, you just need it captured).
- You have a vision doc, architecture doc, or PR/FAQ that already covers most of the "why" for Business.
- Your organisation has an internal standards wiki or a template repo that defines most Technical choices.

### Basic pattern

Wrap your normal invocation with a preamble that tells the agent what to read first. Example:

```
Before starting, please read the following as context:

  - /workspace/orderflow-platform/README.md
  - /workspace/orderflow-platform/package.json
  - /workspace/docs/arch/system-overview.md

Then read .aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md
and execute. When a question can be answered from the files above, propose
the answer in the [Answer]: field with a short "(source: <file>)" note.
Only ask me directly for things the files don't cover.
```

When the agent writes the first batch, the `[Answer]:` fields are pre-filled. Your job becomes: read the proposals, verify the citations, change what's wrong, reply `ready`. For most production codebases this turns a 35-min Technical interview into a 10-min review.

### Worked example — Technical role with a local repo

**Laura types:**

```
Before starting, please read:
  - /workspace/orderflow-platform/README.md
  - /workspace/orderflow-platform/package.json
  - /workspace/orderflow-platform/cdk.json
  - /workspace/docs/arch/system-overview.md
  - /workspace/docs/standards/code-style.md

Then read .aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md
and execute the Technical role. Pre-fill every answer you can infer from
those files; cite the source inline as "(source: <file>)". Ask me only
for what you can't determine.
```

**The agent reads all five files**, then proceeds through the workflow normally (welcome, session detection, role selection, project type, depth selection). When it gets to T1 it writes the first batch with pre-filled answers:

```markdown
# Technical Interview — Section 1 of 8: Project Technical Summary

Progress: ░░░░░░░░░░ 0/33 questions  ·  ~35 min remaining (pre-filled: 4/4 in this batch)

This batch covers T1–T4. I pre-filled every answer I could from the files
you shared. Review, correct anything wrong, then reply **"ready"**.

## Question T1: What runtime environment will host this system?

A) Cloud only
B) On-premises only
C) Hybrid
X) Other

[Answer]: A — Cloud only (source: cdk.json shows AWS CDK stacks; no on-prem references in arch doc)

## Question T2: Which cloud provider will you use?

A) AWS
B) Azure
C) GCP
D) Multi-cloud
E) Not applicable
X) Other

[Answer]: A — AWS (source: cdk.json + package.json aws-cdk-lib dependency)

## Question T3: What is the target deployment model?

A) Serverless
B) Containers
C) VMs
D) Hybrid
X) Other

[Answer]: B and A — Containers (ECS Fargate) for the core, plus Serverless (Lambda + EventBridge) for the new inventory-sync module (source: system-overview.md §3 "Deployment Topology")

## Question T4: Describe the team that will build and own this.

[Answer]: Not covered in source files. I need you to answer this one.

---

Cuando termines, responde con una sola palabra: **listo**
```

**Laura reviews.** T1, T2, T3 look right. T4 is correctly marked as "needs human answer". She adds team info and replies `ready`.

**Result**: 4 questions, ~90 seconds of reviewing vs ~4 minutes of typing.

### Worked example — Business role with a vision Word doc

**Laura types:**

```
I have a vision doc at /workspace/docs/OrderFlow-Vision-v3.docx. Please read
it first, then read .aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md
and execute the Business role. For each question, either propose an answer
extracted from the Vision doc (with a section reference) or tell me it's not
covered. Pay special attention to the MVP Scope IN and OUT sections — those
are decisions I probably still need to make even if the Vision doc is silent.
```

**The agent reads the .docx**, detects it covers §Executive Summary, §Problem Statement, §Target Users, §Success Metrics, and §Full Scope. When the workflow reaches Section 4 (MVP Scope IN) and Section 5 (MVP Scope OUT), the Vision doc is silent — so the agent presents those questions unfilled and labelled:

```markdown
## Question 14: Which features are IN scope for the MVP?

**Not covered in OrderFlow-Vision-v3.docx** — the Vision doc describes the
full scope in §6 but does not distinguish MVP from later phases. This is
a decision I need from you.

(from §6 "Feature Areas", the candidate features are:
  - Real-time inventory dashboard
  - Low-stock alert engine
  - Cross-store redistribution recommender
  - Inventory event stream API
  - Audit & reconciliation module)

Please fill the table under [Answer]:. Use the list above as a starting
point; remove or defer what's not in the first release.

...
```

This is the outcome you intuited earlier: **the Vision doc covers the "what and why", but the MVP cut still needs a human decision.** The tool makes that explicit.

### Worked example — MCP-connected sources

If your agent has MCP access to documentation or knowledge sources, the same pattern applies. Here's an example using the public [AWS Documentation MCP server](https://awslabs.github.io/mcp/servers/aws-documentation-mcp-server):

```
You have access to the AWS Documentation MCP server
(awslabs.aws-documentation-mcp-server). Before starting, consult:

  - https://docs.aws.amazon.com/lambda/latest/dg/welcome.html          (service overview)
  - https://docs.aws.amazon.com/lambda/latest/dg/lambda-foundation.html (core concepts)
  - https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html   (best practices)

Then read .aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md and
execute. Cite the source inline as "(source: <URL>)" for every pre-filled
answer. Ask me for everything the sources don't cover.
```

The agent uses the MCP tools to fetch each resource, then runs the workflow with that context loaded. This works for any MCP that returns markdown, text, or structured data the agent can read — documentation portals, wikis, ticketing systems, design-doc repositories, API catalogues. Swap the server and URLs for your own (for example, `https://github.com/your-org/your-repo` or `https://wiki.example.com/standards`).

### Things to watch out for

**Hallucinated citations.** The agent might write `(source: README.md)` when the README said no such thing. Read the citation and skim the file yourself for anything critical (MVP scope, prohibited libraries, security choices).

**Silent preference between contradictory sources.** If `CLAUDE.md` says "use React" and `package.json` has `vue`, the agent may pick one without flagging it. Before the final gate, ask explicitly:

```
Before I approve, did any of the sources you read contradict each other
on questions we answered? List any contradictions.
```

**Secrets in files.** If you include a file that has credentials, API keys, or PII (`.env`, a log dump, an unscrubbed SQL dump), that content can end up paraphrased in `vision-answers-history.md` or `audit.md`. Do not include those files in your preamble. If you're unsure, add: `"do not read anything under /secrets/ or anything matching *.env*"`.

**Answers that feel too confident.** If the agent writes a crisp-looking answer with a citation, it's tempting to skim and approve. The fastest way to burn this flow is to trust the pre-fill blindly. Use X) freely to override when your domain knowledge contradicts the file.

### Pre-loading vs waiting for a formal extraction mode

| Thing | Pre-loading today | Future formal mode |
|---|---|---|
| Agent reads your sources | ✅ | ✅ |
| Inline citation on answers | ✅ if you ask for it | ✅ enforced |
| Secrets filter before things land in history | ⚠️ relies on agent's general safety behaviour | ✅ pre-ingestion scan |
| Contradiction detection | ⚠️ only if you ask before the gate | ✅ flagged automatically |
| Structured coverage report (`pre-filled-analysis.md`) | ❌ | ✅ |
| Bulk approve / correct / answer-rest UX | ❌ one at a time | ✅ section-level |

For most teams, pre-loading today covers the essential value. The formal mode is the upgrade when you're running the tool routinely on regulated or high-stakes projects.

---

## Tips from real sessions

These come from post-session reviews of teams that used this tool.

### Answer what you know; use X) for the rest

Don't stall on a question because none of the letters feels exactly right. `X — we haven't decided yet; both A and C are on the table` is a perfectly valid answer. It will land in `open-questions.md` as a pre-declared ambiguity and AI-DLC will resolve it with more context.

### Use the measurable outcome question (Q5) as a forcing function

If you cannot write a number and a direction for the single most important outcome, that is a signal your vision is not ready to hand to AI-DLC. Stop, align with your team, come back.

### For tables, do not leave cells blank

The content-validation rules in the tool reject table rows with empty required cells. Either fill the cell or delete the row. "N/A" is acceptable; empty is not.

### For MVP Scope — OUT (Q16), fill in at least 2 rows

Even on small projects. Naming what's out is the strongest scope-creep firewall AI-DLC will have. A Q16 left empty is the #1 reason projects drift in Construction.

### Do Quick first, then upgrade if needed

If you are not sure whether Quick or Full is right, start with Quick. If the resulting document feels thin, you can re-invoke the tool and say "upgrade Business to Full" — the tool will add the missing questions and keep your existing answers.

### Do the Technical role with the actual code open

Even for production systems, answering T5–T10 and T24 is much faster when you have `package.json`, `pyproject.toml`, or equivalent in front of you. The tool accepts "see file path" as an answer in several places precisely for this.

### If two people fill in different roles, commit the state file

`aidlc-discovery-state.md` and `audit.md` are the durable state. Put `Product-Definition/` under version control and let Business and Technical take turns. The tool does not have a multi-user locking mechanism, so use git branches or simple coordination to avoid both editing at the same time.

---

## Troubleshooting

### "The tool is asking questions I already answered"

Most likely the `[Answer]:` tag was left empty or written in a format the validator didn't recognise (e.g. `Answer: A` instead of `[Answer]: A`). Check the exact format in the active question file and re-save.

Second most likely: you edited the file but didn't type `ready` in chat. The tool only re-reads when you send the trigger word.

### "The tool ignored my correction"

The `ready` trigger is for answering a batch, not for corrections. To change a prior answer, say it in natural language:

```
Change my answer to Q7. I picked B but meant D.
```

### "The state file doesn't match what the tool said"

If the tool says "Q8 is next" but the state file shows Q8 as `[x]`, force a resync:

```
Please re-read Product-Definition/aidlc-discovery-state.md from disk and tell me
exactly which question is next.
```

The tool should never rely on in-memory state when disk state is authoritative.

### "I answered but the tool didn't render the final document"

The completion gate runs only when ALL questions for the selected depth are `[x]`. Check the state file for any `[ ]` remaining — a missed question is the most common cause.

### "I want to redo the whole thing"

Delete (or rename) the `Product-Definition/` folder and re-invoke the tool. It will start a fresh session.

### "I started with Quick but now want Full"

Just say it:

```
Upgrade my Business role to Full. Keep my existing answers.
```

The tool will add the missing questions to the state file with `[ ]` markers and resume from the first missing one.

---

If something isn't covered here, the source of truth is the rule files themselves under `aidlc-discovery-rules/aidlc-discovery-rule-details/`. They are plain markdown and readable end-to-end.
