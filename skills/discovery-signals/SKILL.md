---
name: discovery-signals
display_name: "AI-DLC Discovery: Signals"
icon: "📡"
description: "Signals phase of AI-DLC Discovery: turns customer feedback, Signal Briefs, or a synthetic dataset into a Signal Analysis Report and testable hypotheses, after the team writes down what it expects to find. Use when the user wants to analyze customer feedback or VoC data, combine Signal Briefs, find the top customer problems with evidence, or start the Signals phase of Discovery."
trigger: "signals voc feedback signal-analysis"
patterns:
  - pattern: '(?i)\b(?:analy[sz]e|review)\b.{0,20}?\b(?:customer feedback|voc|signals|signal briefs|reviews|support tickets)\b'
    confidence: 0.85
  - pattern: '(?i)\bsignal analysis\b'
    confidence: 0.85
inputs:
  - name: project
    description: "Project folder name under discovery/. The entry skill passes it; ask if it is missing."
    type: string
    required: true
  - name: data_input
    description: "How the customer data comes in: production (feedback the team can load), signal-briefs (one-page anonymized summaries written by the team), or synthetic (a dataset prepared during scoping)."
    type: string
    default: production
  - name: data_location
    description: "Where the data is: an AWS Quick Space name, or a folder relative to the working folder. Usually discovery/data/ for production or synthetic data, and discovery/signal-briefs/ for Signal Briefs."
    type: string
    default: discovery/data/
tools: [file_rag_search, file_read, file_read_pdf, file_read_docx, run_python, file_write]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery: Signals

## Overview

Signals answers "what are customers telling us?" It turns the team's customer feedback into a Signal Analysis Report: the top problems ranked by frequency, severity, and reach, each with evidence and quotes, plus testable hypotheses. Before any analysis, the team writes down what it expects to find, so the report can show which beliefs the data supports. It works the same way on production data, Signal Briefs, or a synthetic dataset.

## Workflow

### Step 1: The team's own hypotheses
- **Mode**: `agentic`
- **Input**: The team, before it sees any analysis
- **Output**: `discovery/{{project}}/signals/team-hypotheses.md`
- **Validate**: At least three hypotheses, each a sentence the data could prove wrong
- **On failure**: If the team cannot name any, ask which customer problem it would bet on today and why

Ask the team what it expects the data to show: the top problems, who has them, and why. Write each answer down as given, without improving it. This matters because AI analysis is persuasive. With the team's beliefs recorded first, the report can show where the data agrees and where it does not, and the team learns something either way. Follow `references/team-hypotheses.md`.

### Step 2: Find and check the data
- **Mode**: `agentic`
- **Tool**: `file_rag_search` for a Space; `file_read` for a folder
- **Input**: `{{data_input}}` at `{{data_location}}`
- **Output**: A short inventory: sources, record or brief counts, time period, and gaps
- **Validate**: The team confirms the inventory matches what it meant to bring
- **On failure**: Ask for the location again, or for the files to be added to the folder

Search the data instead of reading every file into context. Never generate customer data yourself, not even as a synthetic dataset: data written in the session, after the team's hypotheses, can only echo what the team expects. If the data is missing, or is about a different product, stop and offer three options: bring real data, write Signal Briefs with **discovery-signal-brief**, or use a synthetic dataset prepared beforehand. Report what you found before analyzing it: how many records or briefs, from which sources, over which period, and anything that looks missing, such as a channel with no records. If the data contains names, emails, or account identifiers, say so and keep them out of every saved artifact. If it includes telemetry, list its tables, the journeys in the journey map, the period, and whether real user monitoring (RUM) is included: without RUM, the steps on the screen are not visible.

### Step 3: Analyze
- **Mode**: `agentic`
- **Tool**: `run_python` for counts and aggregation
- **Input**: The data from Step 2
- **Output**: Per-item or per-brief findings, kept in working memory or under `discovery/data/`
- **Validate**: Every theme has a count and at least one quote
- **On failure**: If a source cannot be read, continue with the others and list it under data gaps

Choose the path for `{{data_input}}`:

- **production** or **synthetic**: analyze each record with `references/voc-analysis.md` (sentiment, category, urgency, root cause, persona signal, quote), then aggregate with Python. For research documents and competitor material in the same location, use `references/market-and-competitive.md`.
- **signal-briefs**: follow `references/signal-brief-mode.md`. Merge briefs that describe the same problem, check each brief's evidence against the others, and keep each brief's volumes as its evidence.

**Telemetry**, with any data input: if the data includes telemetry (a `telemetry/` folder, or RUM, trace, metric, or log exports), also follow `references/telemetry-analysis.md`. It reads the journey map first, measures each journey step and service, and writes the Say and do table. Telemetry is read next to the feedback, never instead of it.

Save per-item results only under `discovery/data/`, never under the project folder, and do not save the helper scripts anywhere in the working folder.

### Step 4: Write the Signal Analysis Report
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The findings from Step 3 and the team's hypotheses from Step 1
- **Output**: `discovery/{{project}}/signals/signal-summary.md`
- **Validate**: The report has every section in the Output below, and every claim carries an evidence label
- **On failure**: If the evidence for a theme is thin, keep the theme and label it Assumed

### Step 5: Write the hypotheses
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The report from Step 4
- **Output**: `discovery/{{project}}/signals/hypotheses.md`
- **Validate**: 5 to 10 hypotheses, each with evidence, a confidence rating, and a test approach
- **On failure**: Fewer hypotheses is fine when the data is narrow; say why

Follow `references/hypothesis-generation.md`. Include the team's own hypotheses from Step 1 that the data did not settle.

### Step 6: Review with the team
- **Mode**: `agentic`
- **Input**: The report and the hypotheses
- **Output**: The team's challenges, and any changes made to the report
- **Validate**: The team has read at least five customer quotes in full
- **On failure**: None; this step is the team's

Walk the team through the top three signals. Show five full customer quotes, not just theme names, so the team hears customers in their own words. Then ask what contradicts the top signals, and which segments or channels the data under-represents. Change the report where the team finds a real gap, and record the challenge where it does not.

### Optional: Current-product map
When the working folder is the product's own repository, and the harness can read code, follow `references/current-product-map.md` to write `signals/current-product-map.md`. It is usually pre-work. It never blocks Discovery, and in AWS Quick it is skipped.

### Optional: Research deep dive
When the team wants to go deeper on one question, follow `references/research-analysis.md`.

## Output

`discovery/{{project}}/signals/signal-summary.md`:

```markdown
# Signal Analysis Report: [product]
Data: [input type] | [N records or briefs] from [sources] | [period]

## Summary
Two or three sentences: the problem that matters most and the evidence for it.

## Top signals
### 1. [Problem] (frequency X, severity Y, reach Z, total /30)
- Who: [segment]
- Evidence: [counts] [Known]
- Quotes: two or three anonymized quotes, with source
- Root cause: [hypothesis] [Assumed]
(three to seven signals)

## Say and do (when the data includes telemetry)
| Theme | What customers say | What the systems show | Both, Feedback only, or Telemetry only |

## What the team expected
| Team hypothesis | What the data shows | Supported, contradicted, or not settled |

## Customer voices
Five full, anonymized quotes that show the problem in the customer's words.

## Data gaps
Channels, segments, or periods the data does not cover.
```

Every claim carries an evidence label: **Known** (a count, quote, or metric from the data), **Assumed** (believed, not shown), or **Needs evidence** (it matters and has to be tested).

## Lessons Learned

### Do
- Record the team's hypotheses before showing any analysis.
- Quote customers verbatim, anonymized, and give counts with every theme.
- Say when all the evidence comes from one channel.
- Weigh signal over frequency: a topic mentioned often is not always the one that matters most. One clear statement of what customers or the team need can outweigh many mentions of a detail. Severity and reach count as much as volume.

### Don't
- Read every file into context when a search will do.
- Save per-item results or helper scripts in the project folder.
- Drop a theme for thin evidence; label it Assumed instead.

### Common Failures
- **The data has personal information.** Keep it out of saved artifacts and tell the team; suggest masking before the next run.
- **Briefs overlap.** Merge them and keep both briefs' evidence.
- **The data does not match the product.** Stop and offer the three options in Step 2. Do not write a dataset to fill the gap.
- **A file cannot be read.** List it under data gaps and continue.

### When to Ask the User
- The data location is unclear, or the inventory does not match what the team expected.
- The detected categories do not match how the team talks about its product.
- The team wants to drop or merge a signal.
