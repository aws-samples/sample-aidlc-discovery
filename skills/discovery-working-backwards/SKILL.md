---
name: discovery-working-backwards
display_name: "AI-DLC Discovery: Working Backwards"
icon: "📰"
description: "Working Backwards for AI-DLC Discovery: runs the five Working Backwards questions with the team, then writes the PR/FAQ, a readiness check, the PRD, and the riskiest assumption for a selected use case. Use when the user wants to write or challenge a PR/FAQ or press release, write a PRD, run Working Backwards, or name what the prototype must prove."
trigger: "prfaq prd working-backwards press-release"
patterns:
  - pattern: '(?i)\b(?:write|draft|generate|create|challenge)\b.{0,15}?\b(?:pr/?faq|press release|prd|product requirements)\b'
    confidence: 0.90
  - pattern: '(?i)\bworking backwards\b'
    confidence: 0.85
  - pattern: '(?i)\briskiest assumption\b'
    confidence: 0.85
inputs:
  - name: project
    description: "Project folder name under discovery/."
    type: string
    required: true
  - name: use_case
    description: "The selected use case from use-case-scoring.md. With pods, each pod runs this skill for its own use case."
    type: string
    required: true
  - name: mode
    description: "dialog (the team answers the five questions) or draft (write a straw-man PR/FAQ for the team to challenge, for example during a break)."
    type: string
    default: dialog
tools: [file_read, file_write]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery: Working Backwards

## Overview

Working Backwards writes the press release before anything is built: if the team cannot explain the customer benefit clearly enough to announce it, it should not build it. For the use case the team selected, this skill runs the five Working Backwards questions, writes the PR/FAQ and checks it is ready, writes the PRD, and ends by naming the riskiest assumption the prototype has to test. The team writes or challenges every document.

## Workflow

### Step 1: The five questions
- **Mode**: `agentic`
- **Input**: `{{use_case}}`, the Signal Analysis Report, the personas, `use-case-scoring.md`
- **Output**: `discovery/{{project}}/working-backwards/working-backwards.md`
- **Validate**: All five questions answered, in the team's words, with evidence where it exists
- **On failure**: If the team is stuck on a question, offer two suggestions from the signals and let it choose or rewrite

Follow `references/wb-document.md`: Listen, Define, Invent, Refine, Test. Ask one question at a time and summarize each answer before the next. Suggest from the signals, but the answers are the team's. In Listen and Define, apply `references/framing-rules.md`: name the end customer, write root causes as causes, split the impact, and write the Today statement, How Might We, and North Star.

In `draft` mode, answer the five questions yourself from the morning's artifacts, write the PR/FAQ (Step 3), and mark the document as a straw-man. When the team returns, go through each answer with it before Step 4.

### Step 2: Feature description
- **Mode**: `agentic`
- **Input**: The Working Backwards document
- **Output**: `discovery/{{project}}/working-backwards/feature-description.md`
- **Validate**: The team chose one feature idea
- **On failure**: None

Follow `references/feature-description.md`: propose 3 to 5 feature ideas for the problem, and let the team choose or combine them.

### Step 3: PR/FAQ
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The Working Backwards document, the feature description, the personas
- **Output**: `discovery/{{project}}/working-backwards/prfaq.md`
- **Validate**: The press release has a headline, a subheading, and exactly seven paragraphs, each doing its one job, in 500 to 700 words; every claim in the FAQ carries an evidence label, and the press release labels only Assumed and Needs evidence claims; `references/writing-audit.md` passes
- **On failure**: If a quality check fails, show the team which one and rewrite that part with it

Follow `references/prfaq-generation.md`: customer thinking, the seven-paragraph press release, five to seven customer FAQs, and five to seven internal FAQs. The testimonial comes from a persona and is labeled as synthetic. Run `references/writing-audit.md` before showing it, and say in one line what it checked and fixed.

Then ask the team to read the press release aloud and change anything that does not sound like it. This is where the team takes ownership of the document.

### Step 4: Readiness check
- **Mode**: `agentic`
- **Input**: `prfaq.md`
- **Output**: The verdict and the Prototype scope section, appended to `prfaq.md`
- **Validate**: All seven questions have a drafted answer or a marked gap; the verdict is GREEN, AMBER, or RED
- **On failure**: On RED, iterate on the PR/FAQ with the team before the prototype; on AMBER, carry the gaps as open hypotheses

Follow `references/readiness-check.md`.

### Step 5: PRD
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The PR/FAQ, the personas, the Signal Analysis Report, the scoring
- **Output**: `discovery/{{project}}/working-backwards/prd.md`
- **Validate**: P0, P1, and P2 requirements; P0 is small enough to prototype in an hour; when the feature uses AI, the AI feature checklist and the AI feature block are filled in
- **On failure**: If P0 is too big, ask the team what to move to P1

Follow `references/prd-generation.md`, then run `references/writing-audit.md` on it. When the feature uses AI (a model generates, ranks, summarizes, or decides something the customer sees), add the **AI feature block** with `references/ai-feature-block.md`: a first-draft prompt, 5 to 10 evaluation cases from the Signals quotes and the personas, and sample outputs for the prototype. About 10 minutes with the team. If it is unclear whether the feature uses AI, ask.

### Step 6: Riskiest assumption
- **Mode**: `agentic`
- **Tool**: `file_write`
- **Input**: The PR/FAQ and the PRD, especially their Assumed and Needs evidence claims
- **Output**: `discovery/{{project}}/working-backwards/riskiest-assumption.md`
- **Validate**: One assumption, and what the prototype must show about it
- **On failure**: If the team names several, ask which one, if wrong, would end the idea

List the claims labeled Assumed or Needs evidence. Ask the team which one, if it turned out to be wrong, would end the idea. Write it down with what the prototype has to show to test it, and how the team will judge the result in Validate.

## Output

```markdown
# Riskiest assumption: [use case]

**Assumption:** [one sentence]
**Why it is the riskiest:** [what happens to the idea if it is wrong]
**What the prototype must show:** [the interaction or moment that tests it]
**How we will judge it in Validate:** [what would support it, what would contradict it]
```

The other outputs are the Working Backwards document, the feature description, the PR/FAQ with its readiness check, and the PRD, all under `discovery/{{project}}/working-backwards/`.

## Lessons Learned

### Do
- Ask the five questions one at a time.
- Keep the press release to one page, and lead with the customer outcome.
- Label every claim in the FAQ, and only Assumed and Needs evidence claims in the press release; the riskiest assumption comes from the Assumed ones.

### Don't
- Write architecture or technology choices into the PRD.
- Treat the persona quote as a customer quote.
- Let the PRD grow past what can be prototyped today.

### Common Failures
- **The press release describes technology.** Rewrite the first paragraph from the customer's side.
- **The team accepts the draft without changes.** Ask it to read the press release aloud and change what does not sound like it.
- **Every assumption looks risky.** Ask which one, if wrong, means nobody uses it.

### When to Ask the User
- The team's answers contradict the signals.
- The readiness check finds two or more gaps.
- The team cannot agree on the riskiest assumption.
