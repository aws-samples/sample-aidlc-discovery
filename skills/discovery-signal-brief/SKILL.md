---
name: discovery-signal-brief
display_name: "AI-DLC Discovery: Signal Brief"
icon: "📝"
description: "Writes Signal Briefs for AI-DLC Discovery: one-page, anonymized summaries of one customer problem each, created by the team from its own data inside its own environment, so raw data never leaves it. Use before Discovery when the team cannot bring raw customer data, or when asked to write, check, or anonymize a Signal Brief."
trigger: "signal-brief anonymize"
patterns:
  - pattern: '(?i)\bsignal briefs?\b'
    confidence: 0.90
inputs:
  - name: problem
    description: "The customer problem this brief is about, in a few words."
    type: string
    required: true
  - name: sources
    description: "Where the team's evidence is: a folder, a Space, or files the team names."
    type: string
    required: false
tools: [file_rag_search, file_read, file_read_pdf, file_read_docx, run_python, file_write]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery: Signal Brief

## Overview

A Signal Brief lets a team bring its customer evidence to Discovery without bringing the data. The team runs this skill in its own AWS Quick, on its own data, a few days before Discovery starts. For each customer problem, it writes one page: the theme, the job the customer is trying to do, anonymized evidence with volumes, impact, confidence, the segment, and a suggested next step. Only the briefs come to Discovery.

## Workflow

### Step 1: Find the evidence
- **Mode**: `agentic`
- **Tool**: `file_rag_search`, `file_read`
- **Input**: `{{problem}}` and `{{sources}}`
- **Output**: The records that describe the problem, and their sources
- **Validate**: The team confirms the records are about this problem
- **On failure**: Ask for other sources, or a narrower problem

### Step 2: Measure
- **Mode**: `agentic`
- **Tool**: `run_python`
- **Input**: The records from Step 1
- **Output**: Volumes and shares, such as "about 35% of setup tickets in the last 90 days"
- **Validate**: Every number is an aggregate, never a list of records
- **On failure**: If the volume cannot be measured, give an estimate and label it as one

### Step 3: Write the brief
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The evidence and volumes
- **Output**: `discovery/signal-briefs/[problem-slug].md`
- **Validate**: All seven fields are filled; the anonymization check passes
- **On failure**: Leave a field marked "unknown" rather than inventing it

Use the template in `references/template.md`. Choose 2 to 4 quotes that show the problem in the customer's words, then anonymize them.

### Step 4: Anonymization check
- **Mode**: `agentic`
- **Input**: The brief
- **Output**: The brief, cleaned, and a short note of what was removed
- **Validate**: No names, emails, phone numbers, company names, account IDs, contract values, or quotes that could be traced to one customer
- **On failure**: Remove or paraphrase, and tell the team what changed

Remove every identifier. Paraphrase quotes that are distinctive enough to trace. Then ask the team to read the brief once more before sharing it: the team is responsible for what leaves its environment.

## Output

`discovery/signal-briefs/[problem-slug].md`, one per problem, in the format in `references/template.md`. The quality bar: someone who has never seen the raw data could write the first paragraph of a press release about the problem from the brief alone.

## Lessons Learned

### Do
- Write one brief per problem.
- Give volumes as aggregates and say over which period.
- Keep each brief to one page.

### Don't
- Copy raw records, full tickets, transcripts, or logs into a brief.
- Include anything that identifies a customer or a person.
- Run it outside the team's own environment.

### Common Failures
- **A quote names the customer's company.** Paraphrase it.
- **The impact is a guess.** Say so, and lower the confidence.
- **Two briefs describe the same problem.** Merge them.

### When to Ask the User
- Whether a quote is safe to share after paraphrasing.
- Whether a problem is one brief or two.
