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

### Step 1: The team's expectations (optional)
- **Mode**: `agentic`
- **Input**: The team, before it sees any analysis
- **Output**: `discovery/{{project}}/signals/team-expectations.md`, with the team's expectations or a line saying it had none
- **Validate**: The file exists before the analysis; any expectations are written as the team gave them
- **On failure**: None; no expectations is a valid answer

Ask once, in a single question, whether the team already expects the data to show something. If it does, write each expectation down as given, without improving it, so the report can show where the data agrees and where it does not. If it has none, or says skip, write the file with "No expectations recorded before the analysis." and go straight to Step 2 in the same message. Do not explain why expectations matter, ask again, or set a minimum. Follow `references/team-expectations.md`.

### Step 2: Find and check the data
- **Mode**: `agentic`
- **Tool**: `file_rag_search` for a Space; `file_read` for a folder
- **Input**: `{{data_input}}` at `{{data_location}}`
- **Output**: A short inventory: sources, record or brief counts, time period, and gaps
- **Validate**: The team confirms the inventory matches what it meant to bring
- **On failure**: Ask for the location again, or for the files to be added to the folder

Search the data instead of reading every file into context. Never generate customer data yourself, not even as a synthetic dataset: data written in the session, after the team's expectations, can only echo what the team expects. If the data is missing, or is about a different product, stop and offer three options: bring real data, write Signal Briefs with **discovery-signal-brief**, or use a synthetic dataset prepared beforehand. Report what you found before analyzing it: how many records or briefs, from which sources, over which period, and anything that looks missing, such as a channel with no records. Production data should arrive prepared by the team on its own machine with the data preparation script (`tools/prepare-data/` in the [aidlc-discovery repository](https://github.com/aws-samples/sample-aidlc-discovery/tree/main/tools/prepare-data)): placeholders such as `[PERSON_1]` or `[REFERENCE]` show that it was. If production records still contain names, emails, phone numbers, or account identifiers, stop before analyzing them: name the files and the kinds of data, without quoting any value, and ask the team to run the script and replace the files. If the folder holds a `schema.md` and no records, the team kept its records on its own machine; take the schema-only path in Step 3. The fake rows in `schema.md` exist only to write code against: never count or quote them. If it includes telemetry, list its tables, the journeys in the journey map, the period, and whether real user monitoring (RUM) is included: without RUM, the steps on the screen are not visible.

### Step 3: Analyze
- **Mode**: `agentic`
- **Tool**: `run_python` for counts and aggregation
- **Input**: The data from Step 2
- **Output**: Per-item or per-brief findings, kept in working memory or under `discovery/data/`
- **Validate**: Every theme has a count and at least one quote
- **On failure**: If a source cannot be read, continue with the others and list it under data gaps

Choose the path for `{{data_input}}`:

- **production** or **synthetic**: analyze each record with `references/voc-analysis.md` (sentiment, category, urgency, root cause, persona signal, quote), then aggregate with Python. For research documents and competitor material in the same location, use `references/market-and-competitive.md`.
- **Schema only** (production data the team kept on its own machine): write the analysis as one Python script against `schema.md` and its fake rows. It counts records per category, channel, segment, and month, and per theme by keyword in the text, and it prints only counts, shares, and averages, with any group under 5 records shown as `<5`. Give the script to the team to run, and analyze the output they paste back. Ask the team for five scrubbed quotes for the report. Keyword themes are coarser than reading each record, so label root causes Assumed.
- **signal-briefs**: follow `references/signal-brief-mode.md`. Merge briefs that describe the same problem, check each brief's evidence against the others, and keep each brief's volumes as its evidence.

**Telemetry**, with any data input: if the data includes telemetry (a `telemetry/` folder, or RUM, trace, metric, or log exports), also follow `references/telemetry-analysis.md`. It reads the journey map first, measures each journey step and service, and writes the Say and do table. Telemetry is read next to the feedback, never instead of it.

Save per-item results only under `discovery/data/`, never under the project folder, and do not save the helper scripts anywhere in the working folder.

### Step 4: Write the Signal Analysis Report
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The findings from Step 3 and the team's expectations from Step 1, if any
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

Follow `references/hypothesis-generation.md`. Turn each team expectation from Step 1 that the data did not settle into a hypothesis, and say which expectation it came from.

When the team gave expectations, two lists exist from here on, and teams confuse them. **Team expectations** (`E1`, `E2`, ...) are what the team believed before the data; each gets a verdict. **Testable hypotheses** (`H1`, `H2`, ...) are the open questions the data leaves; each gets a test plan. Each file opens with a one-line "What this is" note, and in the chat always give the ID with its sentence ("E3, 'we have reduced errors'"), never a bare number.

### Step 6: Review with the team
- **Mode**: `agentic`
- **Input**: The report and the hypotheses
- **Output**: The team's challenges, and any changes made to the report
- **Validate**: The team has read at least five customer quotes in full, or the report says the data holds none
- **On failure**: None; this step is the team's

Walk the team through the top three signals, one or two lines each, and link to the report for the rest. Show five full customer quotes, not just theme names, so the team hears customers in their own words. Then ask, in one round, what contradicts the top signals, which segments or channels the data under-represents, and whether the business metric still looks right. Change the report where the team finds a real gap, and record the challenge where it does not. Ask this round once; if the team moves on, record "no challenges".

**When the data has no customer words** (counts, tickets, or metrics without free text), say so in the inventory, not at the review. Ask the team, in the same round as the inventory, for three to five things customers have said to them, anonymized, and label them as reported by the team. If there are none, the report's Customer voices section says so, and every root cause stays Assumed.

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
| Team expectation (E1: the team's sentence) | What the data shows | Supported, contradicted, or not settled |
(When the team recorded no expectations: one line saying so, and no table.)

## Customer voices
Five full, anonymized quotes that show the problem in the customer's words.

## Data gaps
Channels, segments, or periods the data does not cover.
```

Every claim carries an evidence label: **Known** (a count, quote, or metric from the data), **Assumed** (believed, not shown), or **Needs evidence** (it matters and has to be tested).

## Lessons Learned

### Do
- Ask for the team's expectations once, before showing any analysis, and accept none.
- Quote customers verbatim, anonymized, and give counts with every theme.
- Say when all the evidence comes from one channel.
- Weigh signal over frequency: a topic mentioned often is not always the one that matters most. One clear statement of what customers or the team need can outweigh many mentions of a detail. Severity and reach count as much as volume.

### Don't
- Read every file into context when a search will do.
- Save per-item results or helper scripts in the project folder.
- Drop a theme for thin evidence; label it Assumed instead.

### Common Failures
- **The data has personal information.** Stop before analyzing it, keep it out of saved artifacts, and ask the team to run the data preparation script on its own machine and replace the files.
- **Briefs overlap.** Merge them and keep both briefs' evidence.
- **The data does not match the product.** Stop and offer the three options in Step 2. Do not write a dataset to fill the gap.
- **A file cannot be read.** List it under data gaps and continue.
- **The team mixes up the two hypothesis lists.** Answer with both IDs and sentences side by side, in two lines.
- **The data has no free text.** See Step 6: ask for team-reported quotes at the inventory, and keep root causes Assumed.

### When to Ask the User
- The data location is unclear, or the inventory does not match what the team expected.
- The detected categories do not match how the team talks about its product.
- The team wants to drop or merge a signal.
