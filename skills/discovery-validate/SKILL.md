---
name: discovery-validate
display_name: "AI-DLC Discovery: Validate"
icon: "✅"
description: "Validate phase of AI-DLC Discovery: challenges the selected use case on the day against four risks (valuable, usable, feasible, viable), runs a pre-mortem, sets testable success criteria, prioritizes the customer problems with the hypotheses still open, and records the team's decision: commit, pivot, or park. Use when the user wants to validate a concept, challenge assumptions, run a pre-mortem, set success criteria, or decide whether to build."
trigger: "validate pre-mortem risks decision"
patterns:
  - pattern: '(?i)\b(?:validate|challenge|stress-?test)\b.{0,20}?\b(?:concept|idea|assumptions?|use case|prototype)\b'
    confidence: 0.85
  - pattern: '(?i)\bpre-?mortem\b|\bfour risks\b|\bcommit, pivot,? or park\b'
    confidence: 0.90
inputs:
  - name: project
    description: "Project folder name under discovery/."
    type: string
    required: true
  - name: use_case
    description: "The use case being validated. With pods, each pod validates its own."
    type: string
    required: true
  - name: mode
    description: "review (four risks, pre-mortem, success criteria, prioritized problems) or decide (commit, pivot, or park)."
    type: string
    default: review
tools: [file_read, run_python, file_write]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery: Validate

## Overview

Validate answers: what could make this fail, and how will we know it worked? The team spends about 45 minutes trying to prove the idea will fail, using only what is in the room: the data, the personas, and the prototype. It does not wait for surveys. Anything it cannot confirm or refute stays an open hypothesis and goes into the brief; real users test the prototype in the follow-up. It ends with the team's decision: commit, pivot, or park.

## Workflow

### Step 1: Check the inputs (mode `review`)
- **Mode**: `deterministic`
- **Tool**: `file_read`
- **Input**: `prototype/index.html`, `prototype/persona-critique.md`, `prototype/notes.md`, `working-backwards/` (PR/FAQ, PRD, GTM draft, riskiest assumption, scoring)
- **Output**: The inputs loaded, or a list of what is missing
- **Validate**: The prototype and the persona critique exist
- **On failure**: If the persona critique is missing, ask **discovery-prototype** to finish its critique and iteration first; the critique is the main evidence for the first two risks

Then re-walk the iterated prototype with the primary personas, only for the findings the iteration changed: did the change fix it? Five minutes, recorded in the risk review. The critique judged the first build; Validate judges the one the team will hand off.

### Step 2: Four risks
- **Mode**: `agentic`
- **Input**: The persona critique and the re-walk, the signals, the prototype, the PRD
- **Output**: A verdict for each risk, with evidence
- **Validate**: Each risk is supported, contradicted, or open, and names its evidence
- **On failure**: With no evidence either way, the verdict is open

| Risk | The question | Main evidence |
|------|--------------|---------------|
| **Valuable** | Will customers want it enough to change what they do today? | The critique's pain and switching answers; the signals' frequency and severity |
| **Usable** | Can each persona complete the core flow without help? | The critique's walk-through and the re-walk of the iterated version |
| **Feasible** | Is there a known path to build it with the team's data, product, and platform? | The engineering lead; the PRD's dependencies. Name unknowns, not an architecture |
| **Viable** | Does it work for the business? | The GTM viability check, completed next by **discovery-gtm** |

For each risk, state the assumption, the evidence for and against, the verdict, and the test that would settle it. Check the riskiest assumption explicitly: does the test moment in the prototype support it, contradict it, or leave it open?

### Step 3: Pre-mortem
- **Mode**: `agentic`
- **Input**: The four risks
- **Output**: Five failure reasons
- **Validate**: Each reason has an early warning sign and a prevention step
- **On failure**: None

Tell the team: it is 90 days after launch, and the feature failed. Ask for the reasons first, then add your own from the evidence. Keep the five most likely, each with the early warning sign and what to do now to prevent it. The reasons the team already worries about are the ones most worth writing down.

### Step 4: Success criteria
- **Mode**: `agentic`
- **Input**: The PR/FAQ, the GTM draft, the business metric from setup
- **Output**: 3 to 5 testable criteria
- **Validate**: Each has a metric, a baseline where the data gives one, a target, and when it is checked (30, 60, or 90 days)
- **On failure**: If a criterion cannot be measured, ask what data would show it, and who will get it

These are what the build is measured against, and what the follow-ups check. For an AI feature, one of the 3 to 5 criteria is an **AI quality target** measured on the evaluation cases in the PRD's AI feature block, for example the share of typical cases a reviewer accepts, and no negative case passing. When the Signal Analysis Report has telemetry, write the criteria as the same journey measures where they exist (for example, the share of sessions that complete the journey without leaving for Contact us), so the 30, 60, and 90-day follow-ups read the same telemetry. Keep them consistent with the adoption and success table that **discovery-gtm** completes, and with the North Star's targets in `working-backwards/working-backwards.md`. Where a criterion differs from the North Star, for example a pilot target, say why.

### Step 5: Prioritize the problems
- **Mode**: `agentic`
- **Tool**: `run_python`
- **Input**: The signals and the risk review
- **Output**: `discovery/{{project}}/validate/prioritization.md`
- **Validate**: Every problem has frequency, severity, and reach scores, and the open hypotheses are listed
- **On failure**: None

Follow `references/prioritization.md`.

Save Steps 2 to 4 as `discovery/{{project}}/validate/risk-review.md`. Then the entry skill runs **discovery-gtm** to complete the viability check and the adoption table, and **discovery-use-case-scoring** if the review changed any score.

### Step 6: The decision (mode `decide`)
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The risk review, the completed GTM section, any re-scoring
- **Output**: `discovery/{{project}}/validate/decision.md`
- **Validate**: The team chose commit, pivot, or park, and gave its reason
- **On failure**: If the team cannot agree, record the positions and the evidence each rests on, and ask the sponsor at the readout

First ask which prototype version the team hands off, showing `prototype/compare.html` if there are several. Copy that version to `prototype/index.html` and record the choice in `prototype/versions.md`.

Summarize the evidence in three lines: what is supported, what is contradicted, what is still open. Then ask the team to decide:

- **Commit**: build it. The brief goes to the build.

If the riskiest assumption is still open, ask one more question before recording commit: does the team commit to building it, or to testing the assumption first? When it is testing first, record the conditions that must be true before the build starts (for example, "8 of 10 owners answer correctly after seeing the status"), and who checks them by which follow-up. The brief carries these conditions in its Decision section.
- **Pivot**: keep what was learned and reframe. Record what changes, and that the reframed or next-ranked use case is taken up at the 30-day follow-up.
- **Park**: stop for now and keep everything. Record the evidence and what would make the team reopen it. A validated decision not to build is a good outcome.

## Output

`validate/risk-review.md`:

```markdown
# Risk review: [use case]

## Four risks
| Risk | Assumption | Evidence for | Evidence against | Verdict | Test to settle it |

## Riskiest assumption
[assumption]: supported / contradicted / open, because [what the test moment showed]

## Pre-mortem
| # | Why it failed | Early warning sign | Prevention now |

## Success criteria
| # | Criterion | Metric | Baseline | Target | Checked at |

## Open hypotheses
Every assumption with verdict "open", as a question for the build.
```

`validate/decision.md`:

```markdown
# Decision: [use case]
**Decision:** commit | pivot | park
**Reason:** [two or three sentences]
**Evidence:** supported [...] / contradicted [...] / open [...]
**Conditions before the build:** [only when the riskiest assumption is open: what must be true, who checks it, by when]
**Next:** [what happens now, for the chosen route; for pivot, what changes; for park, what would reopen it]
**Prototype handed off:** v[N]
**Decided by:** [roles], [date]
```

## Lessons Learned

### Do
- Start from the persona critique and the re-walk; they are the evidence for the first two risks.
- Let the team name the pre-mortem reasons first.
- Make every success criterion measurable, with a date.

### Don't
- Wait for survey results; open hypotheses go into the brief.
- Choose an architecture under feasibility.
- Treat park as failure; record what was learned.

### Common Failures
- **Every risk comes back supported.** Ask what the satisfied persona loses, and what the pre-mortem's top reason says about it.
- **The success criteria are vanity metrics.** Tie each one to the business metric or to adoption.
- **The team wants to decide before the review.** Do the four risks first; the decision rests on them.

### When to Ask the User
- The engineering lead's view on feasibility.
- Whether a contradicted risk changes the decision.
- The decision itself; never make it for the team.

### Follow-up
For open hypotheses the team wants to test with real users after the day, use **discovery-survey**.
