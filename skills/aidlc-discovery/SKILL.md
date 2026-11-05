---
name: aidlc-discovery
display_name: "AI-DLC Discovery Workshop"
icon: "🚀"
description: "Runs an AI-DLC Discovery workshop end to end in five phases (Signals, Working Backwards, Prototype, Validate, Handoff), from customer feedback to a Discovery brief the team builds from. Use when the user wants to start or continue a Discovery workshop, decide what to build from customer feedback, or asks where they are in the workshop. Calls one Discovery skill per job and stops at each checkpoint for the team."
trigger: "aidlc discovery workshop"
patterns:
  - pattern: '(?i)\b(?:start|run|begin|continue|resume)\b.{0,30}?\b(?:discovery )?workshop\b'
    confidence: 0.90
  - pattern: '(?i)\baidlc[- ]discovery\b|\bai-dlc discovery\b'
    confidence: 0.90
  - pattern: '(?i)\bwhat should we build\b'
    confidence: 0.75
inputs:
  - name: project
    description: "Short folder name for this engagement under discovery/, such as the product name."
    type: string
    required: true
  - name: engagement_reference
    description: "A reference for this engagement, if a facilitator gave you one, or Self-serve. Never a customer account, CRM, or sales identifier."
    type: string
    default: Self-serve
  - name: data_input
    description: "production, signal-briefs, or synthetic."
    type: string
    default: production
depends-on: [discovery-signals, discovery-personas, discovery-use-case-scoring, discovery-working-backwards, discovery-gtm, discovery-prototype, discovery-validate, discovery-handoff]
tools: [file_read, file_write, run_python]
version: "0.4.0"
license: MIT-0
---

# AI-DLC Discovery Workshop

## Overview

This skill runs a Discovery workshop: one conversation that takes a product engineering team from its customer feedback to a Discovery brief, in five phases. It keeps the order, the checkpoints, and the shared rules; each job is done by its own Discovery skill. The team does the thinking and owns every decision. The skill drafts, cites evidence, and stops so the team can review.

Discovery ends with a decision on what to build and why. Building, running, and operating the product come after, with the team's own engineers, AI-DLC, or AAP, and the Discovery brief is what they start from.

## Workflow

### Step 1: Set up the workshop
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The user's request; `{{project}}`, `{{engagement_reference}}`, `{{data_input}}`
- **Output**: `discovery/{{project}}/PROJECT.md` with the scope and choices
- **Validate**: The team confirms the product, the people in the room, the business metric with its baseline, and the data input
- **On failure**: Ask for what is missing, one question at a time

Confirm, in this order: the product and who uses it; who is in the room and whether they split into pods; the business metric the work should move, with its current value; and how the data comes in (`production`, `signal-briefs`, or `synthetic`) and where it is. Ask for the engagement reference: the reference a facilitator gave the team, or "Self-serve". Never write a customer account, CRM, or sales identifier. If the team uses the bundled sample data, say that the run is a demonstration and its brief is not evidence for a build. If the data does not match the product, do not generate a dataset to fill the gap; ask the team to bring real data, write Signal Briefs, or use a synthetic dataset prepared before the workshop.

Read `config.md` in the working folder if it exists, otherwise `config.default.md` in this skill's folder, for defaults.

**Where the workshop is saved.** In the working folder, or, in Amazon Quick, in a Space, so the workshop stays in Amazon Quick and the people it is shared with can follow and take over from their own Amazon Quick. Use a Space when `storage` in the config is `space`, when the team asks for one (for example "save the workshop in our team Space"), or when a Space is attached to this chat and `storage` is empty: then ask once, "Save the workshop in the [space] Space, or in this folder?" The data stays where it is either way. In unattended runs, never ask: an empty `storage` means the working folder. With a Space, use **discovery-team-space** for the setup and follow it for every read and write from then on. Without one, nothing changes.

Tell the team the five phases, roughly how long each takes, and that it will be asked to review at every checkpoint. If the user asks to jump to a phase, check that phase's inputs exist first (see the table in Output).

### Step 2: Signals
- **Mode**: `agentic`
- **Input**: The data from Step 1
- **Output**: The team's hypotheses, the Signal Analysis Report, and research hypotheses
- **Validate**: The team has challenged the report and read customer quotes in full
- **On failure**: If no data is found, go back to Step 1

Use **discovery-signals**. Checkpoint: "Here are the top signals and their evidence. What do you challenge before we decide what to work on?"

### Step 3: Working Backwards
- **Mode**: `agentic`
- **Input**: The Signal Analysis Report
- **Output**: Personas, scored use cases, PR/FAQ, PRD, GTM draft, and the riskiest assumption
- **Validate**: The team confirmed or overrode every score and selected the use case to take forward
- **On failure**: If the signals are too thin to score, say so and offer to return to Signals

In this order:

1. **discovery-personas**: three or more personas, including one satisfied customer.
2. **discovery-use-case-scoring**: 3 to 5 candidate use cases through the gate, scores, confidence, and decision. Checkpoint: the team confirms every score and selects the use case to take forward. With pods, each pod takes one selected use case from here on.
3. If the room breaks for lunch now, offer to draft the PR/FAQ for each selected use case meanwhile, so the team returns to a draft to challenge.
4. **discovery-working-backwards**: the five Working Backwards questions, the PR/FAQ, the readiness check, the PRD, and the riskiest assumption.
5. **discovery-gtm**: first adopters, positioning, and the hypotheses for business model and launch.

Checkpoint: "Here is what you chose, why, and what must the prototype prove. Ready to prototype?"

### Step 4: Prototype
- **Mode**: `agentic`
- **Input**: The PRD and the riskiest assumption
- **Output**: A clickable prototype, the persona critique, and one iteration
- **Validate**: The prototype covers the P0 features, tests the riskiest assumption, and changed at least once in response to the team or the critique
- **On failure**: If the PRD is missing, return to Step 3

Use **discovery-prototype**, which calls **discovery-personas** for the persona critique before the iteration. Checkpoint: "Here is what your personas said and what we changed. Ready to try to break it?"

### Step 5: Validate
- **Mode**: `agentic`
- **Input**: Everything from Steps 2 to 4
- **Output**: Risk review, prioritized problems, success criteria, completed GTM tables, and the decision
- **Validate**: Every risk has a verdict, the success criteria are testable, and the team stated commit, pivot, or park with a reason
- **On failure**: Anything that cannot be settled today stays an open hypothesis; never wait for surveys

In this order: **discovery-validate** for a short re-walk of the iterated prototype, the four risks, the pre-mortem, and success criteria; **discovery-gtm** to complete the viability check and the adoption and success table; **discovery-use-case-scoring** if the team wants to re-score; then **discovery-validate** again for the decision.

Checkpoint: "Commit, pivot, or park, and why?"

### Step 6: Handoff
- **Mode**: `agentic`
- **Input**: All artifacts and the decision
- **Output**: The Discovery brief, and `handoff/next-steps.md` with the AI-DLC start command
- **Validate**: The brief exists and every required artifact it links to exists
- **On failure**: List what is missing and offer to run that step; never write a partial brief

Use **discovery-handoff**. Then summarize what the team produced, with links, and ask whether it wants to revisit any phase before the readout.

## Shared rules

These apply in every phase, so the job skills can assume them.

1. **The team decides.** Draft, cite, and ask. Never present a score, ranking, or decision as final until the team confirms it.
2. **Evidence labels.** Every claim in the PR/FAQ, PRD, GTM section, and brief is **Known** (backed by data from Signals), **Assumed** (believed, not shown), or **Needs evidence** (it matters to the decision and has to be tested).
3. **Anonymized.** Quotes carry no names, emails, companies, or account identifiers. Raw data stays in `discovery/data/`.
4. **No architecture.** Discovery decides who, what, and why. Technology choices belong to the build.
5. **Files, not chat.** Save every artifact under `discovery/{{project}}/` as soon as it exists, so the team keeps it and later steps can read it. With a team Space, that path is in the Space (see **discovery-team-space**).
6. **One step at a time.** Say which phase and step the team is in, and what comes next.
7. **Customer's interest only.** No artifact mentions the facilitator's company's commercial interest, vendor competition, or anyone's internal strategy. The documents describe the customer's problem and the customer's outcome.
8. **Show progress.** At every checkpoint, and whenever the team asks where it is, show the progress board below, then the question for the team. Keep `PROJECT.md`'s phase status in step with it.

## Progress board

Two short tables. Status values: ✅ Complete, ▶️ In progress, ⏳ Not started, ⏸️ Deferred for phases; ✅ Saved, 📝 Draft, ❌ Missing for artifacts.

```markdown
**Workshop progress**

| # | Phase | Status | Key artifact |
|---|-------|--------|--------------|
| 1 | Signals | ✅ Complete | Signal Analysis Report: top signal "..." |
| 2 | Working Backwards | ▶️ In progress | Use case scoring: #1 "..." build first |
| 3 | Prototype | ⏳ Not started | |
| 4 | Validate | ⏳ Not started | |
| 5 | Handoff | ⏳ Not started | |

**Artifacts in this phase**

| Artifact | Status | Location |
|----------|--------|----------|
| Use case scoring | ✅ Saved | `discovery/[project]/working-backwards/use-case-scoring.md` |
| PR/FAQ | 📝 Draft | `discovery/[project]/working-backwards/prfaq.md` |
```

The key artifact line says what was decided, not only that a file exists.

At the end of each phase, add three short lists below the tables, carried forward from phase to phase:

```markdown
**What we know:** confirmed facts and decisions from this phase
**What we don't know:** gaps to test later
**What we're assuming:** assumptions we make to keep moving
```

They feed the open hypotheses in the brief.

## Unattended runs

When `config.md` sets `unattended: true`, run every phase without stopping: use the configured project, engagement reference, and data input; take the defaults the job skills give; record each choice in `PROJECT.md` under `## Unattended choices`; and end with the Handoff. Never ask a question in this mode. It exists for automated tests and demonstrations, not for workshops with a team.

## Output

```text
discovery/
├── data/                         raw data, never committed
└── {{project}}/
    ├── PROJECT.md                scope, choices, phase status
    ├── signals/                  team-hypotheses.md, signal-summary.md, hypotheses.md
    ├── working-backwards/        personas/, use-case-scoring.md, working-backwards.md,
    │                             feature-description.md, prfaq.md, prd.md, gtm.md,
    │                             riskiest-assumption.md
    ├── prototype/                v1.html, v2.html, ..., index.html (the chosen version),
    │                             versions.md, compare.html, persona-critique.md, notes.md
    ├── validate/                 risk-review.md, prioritization.md, decision.md
    └── handoff/                  discovery-brief.md, next-steps.md
```

| To start | It needs |
|----------|----------|
| Working Backwards | `signals/signal-summary.md` |
| Prototype | `working-backwards/prd.md` and `riskiest-assumption.md` |
| Validate | `prototype/index.html` and `prototype/persona-critique.md` |
| Handoff | Everything above, and `validate/decision.md` |

## Lessons Learned

### Do
- Record the team's own hypotheses before Signals shows anything.
- Name the skill each step uses, so the team can rerun one job on its own later.
- Keep checkpoints short: what was produced, what the team needs to decide, what comes next.

### Don't
- Repeat a job skill's instructions here; call the skill.
- Move on from scoring until the team has confirmed the scores.
- Start AI-DLC; Handoff prints the command and the team runs it later.

### Common Failures
- **A job's instructions are missing.** Say which skill or module is missing and that the package needs reinstalling; do not improvise its job.
- **The team wants to skip Validate.** Explain that the brief needs the decision and the success criteria; offer the 20-minute version: the four risks and the decision, using the persona critique from Prototype.
- **Time runs out.** Write the brief with what exists, marking unfinished parts as open hypotheses, only if every required artifact exists; otherwise list what is missing.

### When to Ask the User
- The scope, the business metric, or the data input is unclear.
- The team wants to change the order of the phases.
- Two pods want the same use case.
