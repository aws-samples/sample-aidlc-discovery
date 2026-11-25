---
name: aidlc-discovery
display_name: "AI-DLC Discovery"
icon: "🚀"
description: "Runs AI-DLC Discovery end to end in five phases (Signals, Working Backwards, Prototype, Validate, Handoff), from customer feedback to a Discovery brief the team builds from. Use when the user wants to start or continue Discovery, decide what to build from customer feedback, or asks where they are in Discovery. Calls one Discovery skill per job and stops at each checkpoint for the team."
trigger: "aidlc discovery"
patterns:
  - pattern: '(?i)\b(?:start|run|begin|continue|resume)\b.{0,30}?\bdiscovery\b'
    confidence: 0.90
  - pattern: '(?i)\baidlc[- ]discovery\b|\bai-dlc discovery\b'
    confidence: 0.90
  - pattern: '(?i)\bwhat should we build\b'
    confidence: 0.75
inputs:
  - name: project
    description: "Short folder name for this Discovery under discovery/, such as the product name."
    type: string
    required: true
  - name: data_input
    description: "production, signal-briefs, or synthetic."
    type: string
    default: production
depends-on: [discovery-signals, discovery-personas, discovery-use-case-scoring, discovery-working-backwards, discovery-gtm, discovery-prototype, discovery-validate, discovery-handoff]
tools: [file_read, file_write, run_python, open_in_session_tab]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery

## Overview

This skill runs AI-DLC Discovery: one conversation that takes a product engineering team from its customer feedback to a Discovery brief, in five phases. It keeps the order, the checkpoints, and the shared rules; each job is done by its own Discovery skill. The team does the thinking and owns every decision. The skill drafts, cites evidence, and stops so the team can review.

Discovery ends with a decision on what to build and why. Building, running, and operating the product come after, with the team's own engineers, AI-DLC, or AAP, and the Discovery brief is what they start from.

## Workflow

### Step 1: Set up Discovery
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The user's request; `{{project}}`, `{{data_input}}`
- **Output**: `discovery/{{project}}/PROJECT.md` with the scope and choices, in the format in Output; then the journey app, `discovery/{{project}}/journey.html` (see Shared rules)
- **Validate**: The team confirms the product, the people on the team, the business metric with its baseline, and the data input
- **On failure**: Ask for what is missing in the next round

**Start or resume.** Before anything else, look for `discovery/*/PROJECT.md` in the working folder.
- None: start a new project.
- One or more: list each project with its product and its `Now:` line (or, without one, its phase status), then ask in one round: continue one of them, or start a new project. Recommend the one updated last, or the one the user named.
- To continue: read its `PROJECT.md` and the saved artifacts of its current phase, say in one line where it stands, and pick up at the step in the `Now:` line. Do not ask the setup questions again. Load the module of that phase first.
- To start a new project with a name already used: never overwrite it. Propose the name with the next free number, such as `[project]-2`.
- If the working folder holds this skill's own source (a `skills/aidlc-discovery/` folder), say so in one line and recommend connecting a copy of a sample or the product's repository instead.
- In unattended runs, never ask: use the configured project, and continue it if it exists.

Draft the setup from what you can find first (the request, the working folder, `config.md`, the data files), then confirm it in one or two rounds (see Shared rules): the product and who uses it; who is on the team; the business metric the work should move, **which direction is good** (higher or lower), and its current value; and how the data comes in (`production`, `signal-briefs`, or `synthetic`) and where it is. Never assume the direction of the metric: scoring depends on it. (Unattended runs follow the default in "Unattended runs".) If the request contains a term you cannot place (an engagement reference, a code name), ask what it is in the first round, never twice. Never write a customer account, CRM, or sales identifier, or a revenue amount (a share that sizes a segment, such as "a third of revenue", is fine). If the team uses the bundled sample data, say that the run is a demonstration and its brief is not evidence for a build. If the data does not match the product, do not generate a dataset to fill the gap; ask the team to bring real data, write Signal Briefs, or use a synthetic dataset prepared beforehand.

Read `config.md` in the working folder if it exists, and `config.default.md` in this skill's folder for defaults: a key that `config.md` does not set takes its value from `config.default.md`.

**Project language.** The project language is the human language the team works in, such as English or Japanese. It is not a programming language, and not the language the feedback is written in. It is the language the team writes to you in, unless `project_language` in the config sets one; in unattended runs with an empty `project_language`, it is the language of the starting prompt. Record it in `PROJECT.md` as `Project language: [language]` (see the format in Output), so a later session keeps it. When `PROJECT.md` records none, for example when a job skill runs on its own, use the language the team writes in.

Tell the team the five phases, and that it will be asked to review at every checkpoint. If the user asks to jump to a phase, check that phase's inputs exist first (see the table in Output).

### Step 2: Signals
- **Mode**: `agentic`
- **Input**: The data from Step 1
- **Output**: The team's expectations (if it has any), the Signal Analysis Report, and testable hypotheses
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

1. **discovery-personas**: three personas by default, including one satisfied customer, and a buyer persona on top when the buyer is not the end user.
2. **discovery-use-case-scoring**: 3 to 5 candidate use cases through the gate, scores, confidence, and decision. Checkpoint: the team confirms every score and selects the use case to take forward.
3. **discovery-working-backwards**: the five Working Backwards questions, the PR/FAQ, the readiness check, the PRD, and the riskiest assumption.
4. **discovery-gtm**: first adopters, positioning, and the hypotheses for business model and launch.

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
3. **Anonymized.** Quotes carry no names, emails, companies, or account identifiers. Replace each one inside a quote with a bracketed role, such as `[corporate account]` or `[agent]`, and keep every other word as written: the quote still counts as verbatim. Raw data stays in `discovery/data/`.
4. **No architecture.** Discovery decides who, what, and why. Technology choices belong to the build.
5. **Files, not chat.** Save every artifact under `discovery/{{project}}/` as soon as it exists, so the team keeps it and later steps can read it.
6. **One step at a time.** Say which phase and step the team is in, and what comes next.
7. **Customer's interest only.** No artifact mentions a vendor's commercial interest, vendor competition, or anyone's internal strategy. The documents describe the customer's problem and the customer's outcome.
8. **Show progress.** At the end of each phase, and whenever the team asks where it is, show the progress board below, then the next round. Within a phase, one line is enough: "Working Backwards, step 3 of 5: PR/FAQ." Keep `PROJECT.md`'s `## Phase status` in step with it: the board's first table and the three lists.
9. **Ask in rounds.** Every question to the team uses the format in "Asking the team" below.
10. **Keep the chat short.** The files hold the detail; the chat holds what the team needs to decide now. Summarize an artifact in at most five lines and link to it, except the press release, which the team reads in full. Acknowledge an answer in one line, not by restating it. Never repeat a question the team has already answered or skipped; carry it as an open item instead.
11. **Corrections flow downstream.** When the team corrects something an earlier confirmed step relied on (the metric or its direction, a data file, a score), say in one line what it changes, and make re-running that step the recommended answer in the next round. Do not continue on the old basis.
12. **Plain writing.** Before you send any reply or save any artifact, check it against `references/plain-writing.md` and fix what fails. It keeps the structure of the method's own names, the round format, and the evidence labels, and it allows no emojis.
13. **Project language.** Write every message to the team and every artifact in the project language (see Step 1), including when a later session continues. The rules in these skills are written in English: apply each for its purpose, not its English words.
    - **Everywhere**, keep in English only these values: the method's own names; the decision values commit, pivot, and park; the evidence labels; and the route, data, and status values. A heading or label that names such a value, such as a "Phase" or "Status" column, is translated.
    - **In chat**, write everything else in the project language, including the headings, column headers, and labels of the formats and examples these skills show in English, such as a bold label before a colon.
    - **In artifacts**, also keep in English these parts of a job skill's template: headings; the name before a colon that labels a value, such as `Verdict:` or `**Decision:**`, but not the text after it; the table headers it defines; markers such as `[GAP]`; and any value the template offers as a choice, such as `GREEN | AMBER | RED`, written as listed. Everything else is prose: a question, a title, or a sentence is written in the project language, even when it is bold or the template writes it out in English.
    - **Keep as they are**: file and folder names and paths; and commands.
    - **Customer quotes.** A quote is the customer's words together with their source. When the words are in the project language, write `"[original]" ([Source])`. When they are in another language, the quotation marks hold the translation: write `"[translation into the project language]" ("[original]", [Source])` in artifacts, and `"[translation]" ([Source], translated)` in chat. The translation keeps the original's meaning and strength and adds nothing; the original stays verbatim. When you reuse a quote from another artifact, take all of it, and write it in the form for where it goes.
14. **The journey app.** Once `PROJECT.md` exists, create the journey app, then update it at the start of every step and at every checkpoint, so the room can follow where Discovery stands. Load `references/journey-app.md` once, after Setup, and follow it.

## Asking the team

Ask in rounds. A round holds every question that is ready to be asked now, each in this format:

```markdown
**Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

**<"Recommendation" in the project language>:** <your recommended answer>

---

**Q2** - **<question title>**: <question body>

**<"Recommendation" in the project language>:** <your recommended answer>
```

- **Word each question so "yes", or the project language's word for yes, accepts the recommended answer.** The team can answer a whole round with "yes", or with "yes, except Q2: ...".
- **Recompute the frontier after each answer.** Settled decisions unblock the questions that depended on them. A question whose answer depends on another question still open in this round belongs to a later round, not this one.
- **Finding facts is your job, never the team's.** If a question needs a fact from the data or the files, look it up before asking. When the harness can run sub-agents, dispatch one with a fresh context for each lookup and ask the rest of the round meanwhile; only the questions that depend on the lookup wait. Never ask the team for something you could read yourself.
- **The decisions are the team's.** Put each one to the team and wait. A recommendation is a draft, never a decision.
- **No recommendation where it would bias the team.** For the team's expectations before Signals, never suggest what to believe; the only recommendation is that skipping is fine.
- When the harness shows answer buttons (for example decision cards), make the recommended answer the first option. The chat text still uses the format above.

## Progress board

Two short tables, with no emojis. Status values: Complete, In progress, Not started, Deferred for phases; Saved, Draft, Missing for artifacts.

In the Artifact column, write each artifact's title as it appears in the file.

```markdown
**Discovery progress**

| # | Phase | Status | Key artifact |
|---|-------|--------|--------------|
| 1 | Signals | Complete | Signal Analysis Report: top signal "..." |
| 2 | Working Backwards | In progress | Use case scoring: #1 "..." build first |
| 3 | Prototype | Not started | |
| 4 | Validate | Not started | |
| 5 | Handoff | Not started | |

**Artifacts in this phase**

| Artifact | Status | Location |
|----------|--------|----------|
| Use case scoring | Saved | `discovery/[project]/working-backwards/use-case-scoring.md` |
| PR/FAQ | Draft | `discovery/[project]/working-backwards/prfaq.md` |
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

When `config.md` sets `unattended: true`, run every phase without stopping: use the configured project and data input; take the defaults below and those the job skills give; record each choice in `PROJECT.md` under `## Unattended choices`; and end with the Handoff. Never ask a question in this mode. It exists for automated tests and demonstrations, not for work with a team.

| Decision | Default in an unattended run |
|----------|------------------------------|
| Which direction of the metric is good | As the scenario or `config.md` states it. If neither does, infer it from the metric's wording, and record it as **Assumed** |
| The team's expectations before Signals | The beliefs the scenario page gives for each role, turned into expectation lines as `team-expectations.md` says, before any analysis; a belief that names no problem (a caution, a preference) is left out, with the reason; "none" if the page gives none |
| Candidates from Signals | Keep each one; the gate decides |
| Score overrides, and re-scoring in Validate | None |
| Prototype version handed off | The latest |
| Commit, pivot, or park | The one the evidence summary in Validate supports, with its reason, recorded as the recommended answer, not as the team's |
| Commit while the riskiest assumption is open | Test first, with the conditions before the build |
| Build route | AI-DLC |

For any other decision the team would make, take the recommended answer of that round, and record it like the rest. Where a step asks for the team's own input and offers no recommendation (reactions to a click-through, the team's own pre-mortem reasons, a fact only the team knows, such as a city or a name), record "none given (unattended run)" and carry the gap as an open item; never write a view and present it as the team's. In an artifact's text, write around a missing fact instead of leaving a placeholder: a role instead of a name, the date without a city.

## Output

```text
discovery/
├── data/                         raw data, never committed
└── {{project}}/
    ├── PROJECT.md                scope, choices, phase status
    ├── journey.html              the journey app, generated from the files
    ├── signals/                  team-expectations.md, signal-summary.md, hypotheses.md
    ├── working-backwards/        personas/, use-case-scoring.md, working-backwards.md,
    │                             feature-description.md, prfaq.md, prd.md, gtm.md,
    │                             riskiest-assumption.md
    ├── prototype/                v1.html, v2.html, ..., index.html (the chosen version),
    │                             versions.md, compare.html, persona-critique.md, notes.md
    ├── validate/                 risk-review.md, prioritization.md, decision.md
    └── handoff/                  discovery-brief.md, next-steps.md
```

`PROJECT.md`, written at Setup and kept current:

```markdown
# Discovery: [product]

Project language: [language]
Now: [phase], [step]. Next: [the next step]. Updated [date and time].

| Field | Value | Status |
|-------|-------|--------|
| Product | [the product, and who uses it] | Confirmed |
| Team | [the roles] | Confirmed |
| Business metric | [the metric] | Confirmed |
| Direction | [Higher or Lower] is better | Confirmed |
| Baseline | [value], [period] | Confirmed |
| Data input | [production, signal-briefs, or synthetic], in [location] | Confirmed |
| Note | [only with sample data:] Demonstration run on sample data; the brief is not evidence for a build | |

## Phase status
[The progress board's first table, with its Key artifact column, and the three lists below it]

## Open items
- [a question the team skipped, or an answer still missing]

## Unattended choices
[Only in unattended runs]
| Decision | Choice | Source |
|----------|--------|--------|
```

A value the team has not confirmed yet has the status Assumed or Open. Other skills can add rows to the table. The journey update (see Shared rules) rewrites the `Now:` line at every step; when you save `PROJECT.md` yourself, keep that line as it is.

| To start | It needs |
|----------|----------|
| Working Backwards | `signals/signal-summary.md` |
| Prototype | `working-backwards/prd.md` and `riskiest-assumption.md` |
| Validate | `prototype/index.html` and `prototype/persona-critique.md` |
| Handoff | Everything above, and `validate/decision.md` |

## Lessons Learned

### Do
- Ask once for the team's expectations before Signals shows anything; none is a valid answer.
- Name the skill each step uses, so the team can rerun one job on its own later.
- Keep checkpoints short: what was produced, what the team needs to decide, what comes next.
- Ask every independent question in the same round.

### Don't
- Ask the team one question per message when the questions do not depend on each other.
- Ask the team for a fact that is in the data or the files.
- Repeat a job skill's instructions here; call the skill.
- Move on from scoring until the team has confirmed the scores.
- Start AI-DLC; Handoff prints the command and the team runs it later.

### Common Failures
- **A job's instructions are missing.** Say which skill or module is missing and that the package needs reinstalling; do not improvise its job.
- **The team wants to skip Validate.** Explain that the brief needs the decision and the success criteria; offer the short version: the four risks and the decision, using the persona critique from Prototype.
- **Time runs out.** Write the brief with what exists, marking unfinished parts as open hypotheses, only if every required artifact exists; otherwise list what is missing.

### When to Ask the User
- The scope, the business metric, or the data input is unclear.
- The team wants to change the order of the phases.
