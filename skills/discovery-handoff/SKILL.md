---
name: discovery-handoff
display_name: "AI-DLC Discovery: Handoff"
icon: "📦"
description: "Handoff phase of AI-DLC Discovery: checks every required artifact exists, then writes the Discovery brief, the single document the team builds from, into the team's repository, with the personas for AI-DLC and the command that starts AI-DLC Inception from the brief. Use when the user wants the Discovery brief, to hand off to engineering, AAP, or AI-DLC, or to finish Discovery."
trigger: "brief handoff discovery-brief"
patterns:
  - pattern: '(?i)\bdiscovery brief\b'
    confidence: 0.90
  - pattern: '(?i)\bhand\s?off\b.{0,20}?\b(?:aidlc|ai-dlc|engineering|build)\b'
    confidence: 0.85
inputs:
  - name: project
    description: "Project folder name under discovery/."
    type: string
    required: true
tools: [file_read, file_write]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery: Handoff

## Overview

Handoff writes the Discovery brief: the single document that carries the team's decision, its evidence, and what is still unproven into whatever build follows, whether the team's own engineering, agents, or AI-DLC. It is written for every decision, including pivot and park, so the evidence is never lost. When the team uses AI-DLC, the brief is the one document AI-DLC Inception reads, and Discovery takes the place of AI-DLC's own Ideation phase.

Supported AI-DLC: 2.10.0 or later (`awslabs/aidlc-workflows`). The brief relies on AI-DLC's single-document input (UTF-8 text, at most 200,000 characters), the `workshop` and `classic` profiles, and team knowledge in `aidlc/spaces/[space]/knowledge/aidlc-product-agent/`.

## Workflow

### Step 1: Check the required artifacts
- **Mode**: `deterministic`
- **Tool**: `file_read`
- **Input**: `discovery/{{project}}/`
- **Output**: The list of artifacts found, or what is missing
- **Validate**: Every artifact in the table exists
- **On failure**: List what is missing and which skill produces it; never write a partial brief

| Artifact | Path under `discovery/{{project}}/` | Produced by |
|----------|-------------------------------------|-------------|
| Team hypotheses | `signals/team-hypotheses.md` | discovery-signals |
| Signal Analysis Report | `signals/signal-summary.md` | discovery-signals |
| Personas (at least two) | `working-backwards/personas/*.md` | discovery-personas |
| Use case scoring | `working-backwards/use-case-scoring.md` | discovery-use-case-scoring |
| PR/FAQ | `working-backwards/prfaq.md` | discovery-working-backwards |
| PRD | `working-backwards/prd.md` | discovery-working-backwards |
| Riskiest assumption | `working-backwards/riskiest-assumption.md` | discovery-working-backwards |
| GTM section | `working-backwards/gtm.md` | discovery-gtm |
| HTML prototype | `prototype/index.html` | discovery-prototype |
| Persona critique | `prototype/persona-critique.md` | discovery-personas |
| Risk review | `validate/risk-review.md` | discovery-validate |
| Prioritized problems with open hypotheses | `validate/prioritization.md` | discovery-validate |
| Decision | `validate/decision.md` | discovery-validate |
| Current-product map (only when a codebase exists) | `signals/current-product-map.md` | discovery-signals |

### Step 2: Write the brief
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: Every artifact above
- **Output**: `discovery/{{project}}/handoff/discovery-brief.md`
- **Validate**: Exactly the 15 sections below, in order; under 200,000 characters; every link resolves
- **On failure**: If the brief is too long, summarize harder and link to the artifacts

Summarize, and link to the full artifacts instead of copying them. Use the template in Output.

### Step 3: Write the AI-DLC team knowledge and protect raw data
- **Mode**: `deterministic`
- **Tool**: `file_write`
- **Input**: The personas
- **Output**: `aidlc/spaces/[space]/knowledge/aidlc-product-agent/discovery-personas.md`, and `discovery/data/` in `.gitignore`
- **Validate**: Both files exist
- **On failure**: Create the folders if they do not exist

When the route is AI-DLC, write every persona in full to the team knowledge file, so AI-DLC's product agent loads them. For any other route, skip it, and say in `next-steps.md` that the team can ask for it later if it moves to AI-DLC. `[space]` is the name in `aidlc/active-space` if that file exists, otherwise `default`. Write nothing else under `aidlc/`. Add `discovery/data/` to `.gitignore`, creating the file if needed, so raw customer data is never committed.

### Step 4: Finish
- **Mode**: `agentic`
- **Input**: The decision
- **Output**: `discovery/{{project}}/handoff/next-steps.md`, and a summary for the team
- **Validate**: The team knows what happens next
- **On failure**: None

Write `handoff/next-steps.md`, so what happens next does not live only in the chat, and show its content to the team. It says, by decision:

- **Commit with AI-DLC**: print the start command, and do not start AI-DLC; the build is a separate session, often days later.

  ```text
  aidlc config --harness <claude | kiro | kiro-ide | codex | cursor | opencode | copilot>
  /aidlc workshop Read ./discovery/{{project}}/handoff/discovery-brief.md and build what it describes, [product or feature name]
  ```

  Use `/aidlc classic` when the team continues on its own. Amazon Quick does not run AI-DLC: tell the team to commit the `discovery/` folder to the repository where it will build, and run the command there.
- **Commit with the team's own engineering or agents**: point to the brief as the build's starting document.
- **Pivot or park**: what happens at the 30-day follow-up, from the decision file.

It also lists any conditions before the build from the decision, and the follow-ups: the real-user test of the prototype and the open hypotheses to take to real customers by day 30.

It ends with a **roadmap for the product owner: Now, Next, Later**, from what Discovery already produced, never new ideas:

- **Now:** the use case taken forward, its conditions in order, and the success criteria.
- **Next:** the deferred candidates from `use-case-scoring.md`, each with the evidence that would move it up, who gets that evidence, and by which follow-up.
- **Later:** the rest, each with why, including what was dropped at the gate and the open hypothesis that could bring it back.

Each item is a customer problem and the metric it moves, ordered by conditions, not by dates. No features beyond the PRD, and no delivery dates: the product owner sets those with the build team.

Then summarize what the team produced, with links, and ask whether it wants to revisit anything before the readout.

## Output

`discovery/{{project}}/handoff/next-steps.md`:

```markdown
# Next steps: [product or feature name]
Decision: [commit | pivot | park]

## Start the build
1. Copy or commit the `discovery/` and `aidlc/` folders into the repository where the team will build.
2. In that repository, run:
   aidlc config --harness <claude | kiro | kiro-ide | codex | cursor | opencode | copilot>
   /aidlc workshop Read ./discovery/[project]/handoff/discovery-brief.md and build what it describes, [name]
(or, for pivot and park, what happens at the 30-day follow-up instead)

## Conditions before the build
## Follow-ups
## Roadmap: Now, Next, Later (for the product owner)
```

`discovery/{{project}}/handoff/discovery-brief.md`, with exactly these sections:

```markdown
# Discovery brief: [product or feature name]

## 1. Context
Date: [YYYY-MM-DD] | Route: [own engineering | agents | AI-DLC workshop | AI-DLC classic | none] | Data: [production | Signal Briefs | synthetic]

## 2. Decision
Commit, pivot, or park, the reason, any conditions that must be true before the build starts, and what happens next.

## 3. Problem and evidence
The problem in two or three sentences, then the top signals with frequency,
severity, and reach, each with one anonymized customer quote.

## 4. Target customers and personas
One paragraph per persona, starting with the persona's name in bold: who they
are, the job they need done, and their main pain. Full personas are in AI-DLC
team knowledge.

## 5. Prioritized use cases
The scored table: each candidate with its weighted score, confidence, and
decision, the team's overrides with reasons, and the use case this brief builds.

## 6. PR/FAQ summary
The press-release headline, the customer benefit, and the three FAQ answers
that most constrain the build.

## 7. Success criteria
The testable criteria from Validate: metric, baseline, target, and when it is checked.
For an AI feature, include the AI quality target and the evaluation cases it is
measured on.

## 8. GTM
First adopters, positioning, the viability check with owner roles, and the
adoption and success table. Business model, pricing, and launch plan as
hypotheses with owners.

## 9. Scope
In scope and out of scope, as two lists.
For an AI feature, add the AI feature block from the PRD: the first-draft prompt
and the evaluation cases, marked as a starting point for the build, which chooses
the model, the data and retrieval design, and the final prompt.

## 10. Prioritized backlog
The PRD features ranked P0, P1, P2, one line each.

## 11. Prototype screens and user flows
The chosen version (from `prototype/versions.md`), each screen as text (purpose,
main elements, actions), then the core flow as numbered steps, from the
prototype notes, and one line on how the versions evolved. Note an in-codebase prototype
branch if one exists, and that it is disposable.

## 12. Current product
The current-product map summary, or "Greenfield: no existing codebase."

## 13. Constraints
Constraints the team stated: regulation, systems that must integrate,
deadlines. No architecture or technology choices.

## 14. Open hypotheses and assumptions
Every hypothesis Validate did not settle, every claim still labeled Assumed or
Needs evidence, the riskiest assumption if it is still open, and the top
pre-mortem risks with their early warning signs, each as a question for the build.

## 15. Full artifacts
Relative links to every artifact under discovery/[project]/.
```

## Lessons Learned

### Do
- Write the brief for every decision; a parked idea's evidence is worth keeping.
- Link to artifacts instead of copying them.
- Read the brief as an engineer who took no part in Discovery.

### Don't
- Write architecture, technology choices, or code into the brief.
- Write customer account, CRM, or sales identifiers, or revenue figures, into the team's repository.
- Start AI-DLC; print the command.

### Common Failures
- **A required artifact is missing.** List it with the skill that produces it.
- **The brief is too long.** Summarize each section to its essentials and link.
- **Persona names differ between the brief and the team knowledge.** Use the name exactly as the persona file's first line.

### When to Ask the User
- The route, if the decision is commit and the route is not clear.
- Anything in the brief the team wants to change before the readout.
