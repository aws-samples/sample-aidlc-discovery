---
name: discovery-use-case-scoring
display_name: "AI-DLC Discovery: Use Case Scoring"
icon: "⚖️"
description: "Use case scoring for AI-DLC Discovery: ranks 3 to 5 candidate use cases, written as problems, with a gate, six weighted dimensions, a confidence rating, and a decision (build first, prototype to learn, defer, drop), then helps the team select what to take forward. Also re-scores after Validate. Use when the user wants to prioritize or score use cases, decide which problem to work on first, or revisit scores."
trigger: "scoring prioritize use-cases"
patterns:
  - pattern: '(?i)\b(?:score|rank|prioriti[sz]e)\b.{0,20}?\buse cases?\b'
    confidence: 0.90
  - pattern: '(?i)\bwhich (?:problem|use case|idea)\b.{0,20}?\bfirst\b'
    confidence: 0.80
inputs:
  - name: project
    description: "Project folder name under discovery/."
    type: string
    required: true
  - name: mode
    description: "score (Working Backwards) or rescore (after Validate)."
    type: string
    default: score
tools: [file_read, run_python, file_write]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery: Use Case Scoring

## Overview

Scoring decides which problem the rest of the day goes to. The team brings 3 to 5 candidate use cases, or draws them from the signals. Each one goes through a gate, six weighted scores, a confidence rating, and a decision. It scores problems, not features. The skill drafts every score with the evidence behind it; the team reviews every score, overrides any it disagrees with, and owns the ranking.

## Workflow

### Step 1: Candidate use cases
- **Mode**: `agentic`
- **Input**: The team's candidates, or `signals/signal-summary.md` and any Signal Briefs; the personas
- **Output**: 3 to 5 candidates, each written as a problem
- **Validate**: Every candidate has the five fields below, and no two solve the same problem
- **On failure**: If the team brings features, ask what problem each one solves and for whom

Each candidate is a problem with five fields: who has it, the problem, the evidence from Signals, the business metric it moves, and the person on the team who would own the build. If the team brought none, draft 3 to 5 from the top signals and ask the team to confirm or edit them. Merge candidates that solve the same problem.

**Then add candidates from Signals.** When the team brought its own candidates, add two or three drawn from Signals themes that none of them covers, including telemetry-only signals. Write each as a problem with its evidence, and mark it "From Signals". The team keeps or drops each one, which takes about a minute: kept ones go through the gate and are scored like the rest; dropped ones are recorded with the reason and not scored. If every theme is covered, say so and add none.

### Step 2: Weights
- **Mode**: `agentic`
- **Input**: The default weights below
- **Output**: The weights for this Discovery
- **Validate**: The weights add up to 100, and no weight moved by more than 10 points
- **On failure**: Use the defaults

Ask once whether the sponsor shifted any weight at setup. Fix the weights before scoring starts, so they cannot be tuned to favor a candidate afterwards.

### Step 3: Gate
- **Mode**: `agentic`
- **Input**: The candidates
- **Output**: Which candidates pass, and the reason for each that does not
- **Validate**: Every candidate has a pass or a recorded reason
- **On failure**: None

First, **merge duplicates**: a candidate that is a symptom of another candidate's problem, or one solution to it ("rebuild the app" when the app's low rating is about the problem another candidate solves), joins that candidate before the gate. Record the merge.

Then **drop** any candidate that fails one of these, and record which. Failing the gate is never a deferral: defer is for candidates that pass and score 2.5 to 3.4. If someone wants to keep a dropped idea alive, record it as an open hypothesis with a cheap test.

1. **Evidence.** Signals shows no customer evidence for the problem.
2. **Outcome.** It has no link to a business metric the customer cares about.
3. **Owner.** Nobody on the team owns the build.
4. **Build path.** It has no path to a build.
5. **Painkiller.** Customers would not notice if it never shipped.

### Step 4: Draft the scores
- **Mode**: `agentic`
- **Tool**: `run_python` for the weighted scores
- **Input**: The candidates that passed, the signals, the personas
- **Output**: A 1-to-5 score on each dimension, each with one line of evidence
- **Validate**: Every score names its evidence, or is labeled Assumed
- **On failure**: None

| Dimension | Weight | 1 | 3 | 5 |
|-----------|:------:|---|---|---|
| **Customer pain** | 25 | Rare mention, nice to have | Recurring friction with a known workaround | Frequent and blocking; customers escalate, pay for workarounds, or leave |
| **Business outcome** | 25 | No measurable link to the business metric | Indirect link, hard to attribute | Direct, measurable movement within 90 days of launch |
| **Reach** | 15 | A small niche of users | One significant segment | Most users or the highest-value segment |
| **Strategic fit or threat** | 10 | Off strategy, no competitive pressure | Supports the strategy | Core to the strategy, or a competitor or "do nothing" is costing customers now |
| **Feasibility** | 15 | New data, platform, and skills needed | Some data or platform work needed | Data in place, builds on the existing product and platform |
| **Adoption load** | 10 | Heavy change for users, or they have not adopted what already shipped in this area | Moderate change in how users work | Fits how users already work |

Score **business outcome** against the business metric agreed at setup, in the direction setup recorded as good, not against a metric the candidate names for itself. A candidate that moves the metric the wrong way, for example by removing tickets when more tickets mean more onboardings, scores 1 on outcome. A candidate that moves only its own metric (baggage calls, when the metric is the self-service rebooking rate) scores low on outcome, however real its pain.

Weighted score = the sum of (score × weight) ÷ 100, from 1.0 to 5.0.

The data rarely shows strategy or platform, so draft strategic fit and feasibility, mark them as the team's to confirm, and ask the engineering lead about feasibility. When the Signal Analysis Report has telemetry, use it: reach and the outcome baseline from the journey steps, and the error rates of the services a candidate depends on as feasibility evidence.

### Step 5: Confidence and decision
- **Mode**: `agentic`
- **Input**: The drafted scores and their evidence
- **Output**: A confidence rating and a decision for each candidate
- **Validate**: Every candidate has both
- **On failure**: None

| Confidence | Meaning |
|------------|---------|
| **High** | Three or more independent signals, including at least one quantitative source |
| **Medium** | Two signals, or one strong quantitative source |
| **Low** | A single source, or the team's own assumption |

| Weighted score | Confidence | Decision |
|----------------|------------|----------|
| 3.5 or more | High | **Build first.** Take it forward today. |
| 3.5 or more | Medium or low | **Prototype to learn.** Take it forward today; carry the low-confidence scores as open hypotheses. A high-value idea is never scored out for low confidence. |
| 2.5 to 3.4 | Any | **Defer.** Revisit at the 30-day follow-up with new evidence. |
| Below 2.5 | Any | **Drop.** Record why. |

**One decision per team.** Only one candidate is "build first" or "prototype to learn": the one with the highest weighted score. Any other that qualifies is **Defer, next in line**, so the day has one clear focus. With pods, each pod has one.

### Step 6: The team reviews and selects
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The scored table
- **Output**: `discovery/{{project}}/working-backwards/use-case-scoring.md`
- **Validate**: The team confirmed or overrode every score, and named what it takes forward
- **On failure**: If the team disagrees with the framework's decision, record its decision and the reason; the team owns the call

Show the table one candidate at a time. For each score, show the evidence and ask: agree, or change it? Record every override with the reason. Then ask which use case the team takes forward: the top "build first", or the top "prototype to learn" when there is no "build first". With pods, each pod takes one; two pods never take the same one.

### Step 7: Re-score after Validate (mode `rescore`)
- **Mode**: `agentic`
- **Input**: `use-case-scoring.md` and `validate/risk-review.md`
- **Output**: The updated `use-case-scoring.md`
- **Validate**: Every change has a reason and the team's confirmation
- **On failure**: None

Propose changes where the persona critique or the risk review showed something new, for example a usability problem that raises adoption load. The team confirms each change; record it in the Overrides table, marked "after Validate".

### Optional: ROI
Once a PRD exists for a selected use case, follow `references/roi-analyzer.md` if the team asks for a cost and benefit estimate.

## Output

`discovery/{{project}}/working-backwards/use-case-scoring.md`:

```markdown
# Use case scoring: [project]
Weights: pain 25, outcome 25, reach 15, fit 10, feasibility 15, adoption 10 [note any sponsor shift]

## Candidates
| # | Use case (problem) | Who | Business metric | Owner | Source (team or From Signals) |

## From Signals
| Candidate | Evidence | Kept or dropped | Reason |

## Gate
| # | Passed | Reason if not |

## Scores
| # | Pain | Outcome | Reach | Fit | Feas. | Adopt. | Weighted | Confidence | Decision |

## Evidence per score
One line per score: the signal, count, or quote behind it, or "Assumed".

## Overrides
| # | Dimension | Draft | Team | Reason | When |

## Taken forward
[Use case], [build first or prototype to learn], by [pod or team]
```

## Lessons Learned

### Do
- Fix the weights before the first score.
- Show the evidence next to every score.
- Ask the engineering lead about feasibility.

### Don't
- Present a draft score as final.
- Score features; ask what problem each solves.
- Score out a high-value, low-confidence idea; it becomes "prototype to learn".

### Common Failures
- **Every candidate scores between 3 and 4.** The candidates are probably too broad; ask the team to make them more specific.
- **The team overrides everything.** Fine, but ask what evidence the overrides rest on, and label them Assumed where there is none.
- **A stakeholder's favorite fails the gate.** Record the reason; the gate is there to make that visible.

### When to Ask the User
- A candidate has no owner or no business metric.
- The team wants to change the weights after scoring started.
- The team's choice differs from the framework's decision.
