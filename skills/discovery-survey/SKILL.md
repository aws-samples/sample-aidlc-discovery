---
name: discovery-survey
display_name: "AI-DLC Discovery: Survey"
icon: "📋"
description: "Follow-up surveys for AI-DLC Discovery: turns the open hypotheses from Validate into a short survey for real users, as an HTML form and as questions ready to paste into Microsoft Forms or Google Forms, then builds a results dashboard from the responses and updates each hypothesis's verdict. Use after Discovery to test open hypotheses or the prototype with real users."
trigger: "survey dashboard responses"
patterns:
  - pattern: '(?i)\b(?:create|build|draft)\b.{0,15}?\bsurvey\b'
    confidence: 0.85
  - pattern: '(?i)\b(?:survey|form) (?:results|responses)\b'
    confidence: 0.85
inputs:
  - name: project
    description: "Project folder name under discovery/."
    type: string
    required: true
  - name: mode
    description: "create (draft the survey) or results (build the dashboard from a CSV of responses)."
    type: string
    default: create
tools: [file_read, run_python, file_write, open_in_session_tab]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery: Survey

## Overview

Validate leaves some hypotheses open on purpose: they need real users, not synthetic personas. This skill is for the follow-up. It turns the open hypotheses into a short survey the team sends to real users, then reads the responses back and says which hypotheses they support or contradict. Nothing in Discovery waits for it.

## Workflow

### Step 1: Draft the survey (mode `create`)
- **Mode**: `agentic`
- **Tool**: `file_write`, `open_in_session_tab`
- **Input**: `validate/risk-review.md` and `validate/prioritization.md` (the open hypotheses), the personas
- **Output**: `validate/survey-[topic].html` and `validate/survey-[topic].md`
- **Validate**: Every question maps to an open hypothesis; the survey takes under five minutes
- **On failure**: If there are no open hypotheses, say so; there is nothing to survey

Follow `references/survey-generator.md`. Ask the team which hypotheses to test and who will receive the survey. The assistant cannot host a form, so the HTML is a preview and the Markdown list is ready to paste into Microsoft Forms, Google Forms, or Typeform. Say so.

### Step 2: Read the results (mode `results`)
- **Mode**: `agentic`
- **Tool**: `run_python`, `file_write`
- **Input**: A CSV export of the responses
- **Output**: `validate/dashboard.html` and updated verdicts
- **Validate**: Every hypothesis on the survey has a verdict: supported, contradicted, or still open
- **On failure**: If the CSV's columns do not match the questions, ask the team to map them

Follow `references/results-dashboard.md`. Then add a `## Follow-up results` section to `validate/risk-review.md` with each hypothesis's new verdict and the response count behind it. If a result changes the decision, say so; the team may want to revisit it at the 30-day follow-up.

## Output

- `validate/survey-[topic].html`: the form preview
- `validate/survey-[topic].md`: the questions, ready to paste
- `validate/dashboard.html`: the results, with a hypothesis verdict table

## Lessons Learned

### Do
- Map every question to one hypothesis.
- Keep it under five minutes.
- Report the response count with every verdict.

### Don't
- Treat a handful of responses as proof.
- Survey people outside the target segment and count them.

### Common Failures
- **Leading questions.** Rewrite them neutrally.
- **Too few responses.** Keep the hypothesis open and say how many more are needed.

### When to Ask the User
- Who receives the survey.
- Whether a result changes the decision.
