---
name: discovery-personas
display_name: "AI-DLC Discovery: Personas"
icon: "👥"
description: "Synthetic personas for AI-DLC Discovery: generates personas from customer feedback or Signal Briefs, runs the persona critique of a prototype at the end of Prototype, and lets the team talk to a persona or run a persona panel. Use when the user wants to create personas, hear how a persona would react to an idea or prototype, run a persona critique, or hold a panel discussion."
trigger: "personas persona critique panel"
patterns:
  - pattern: '(?i)\b(?:generate|create|build)\b.{0,15}?\bpersonas?\b'
    confidence: 0.85
  - pattern: '(?i)\bpersona (?:critique|panel|walk-?through)\b'
    confidence: 0.90
  - pattern: '(?i)\b(?:talk to|load|switch to)\b.{0,10}?\bpersona\b'
    confidence: 0.80
inputs:
  - name: project
    description: "Project folder name under discovery/."
    type: string
    required: true
  - name: mode
    description: "generate (Working Backwards), critique (end of Prototype), or simulate (talk to one persona, or a panel)."
    type: string
    default: generate
  - name: count
    description: "How many personas to generate."
    type: number
    default: 3
tools: [file_rag_search, file_read, run_python, file_write]
version: "0.4.0"
license: MIT-0
---

# AI-DLC Discovery: Personas

## Overview

Personas put a face on the signals. In Working Backwards they are generated first, because scoring, the PR/FAQ, and the prototype all refer to them. At the end of Prototype, each persona critiques the prototype in its own voice. The critique drives the team's iteration, and Validate uses it as the main evidence for whether the idea is valuable and usable. Every trait and quote traces back to the customer data; personas are synthetic, so the real-user test still happens in the follow-up.

## Workflow

### Step 1: Generate personas (mode `generate`)
- **Mode**: `agentic`
- **Tool**: `file_rag_search`, `run_python`
- **Input**: `discovery/{{project}}/signals/signal-summary.md` and the data behind it; `{{count}}`
- **Output**: One file per persona in `discovery/{{project}}/working-backwards/personas/`
- **Validate**: At least two personas; every quote is real; each has a confidence rating and an evidence count
- **On failure**: If the data supports fewer distinct segments than asked, generate fewer and say why

Follow `references/persona-generation.md`: find behavioral segments in the feedback, write each persona in the format in `references/persona-document.md`, then check each one against the data. Make one of them a customer who is satisfied today, so the team sees what it could break. When the buyer and the end user are different people (for example a travel manager who chooses the airline, and the traveller who uses the app), give each one a persona and say which is which: the buyer judges value and cost; the end user judges whether the workflow works. If they are the same person, say so.

With a synthetic dataset, rate confidence no higher than Medium, whatever the item count: the items are not real customers. With Signal Briefs, there is no record-level data. Build segments from the briefs' segments and jobs, use only the quotes the briefs contain, and rate confidence no higher than Medium unless three or more briefs describe the same segment.

Show the team a one-line summary of each persona (name, tagline, confidence) and ask whether they recognize these people. Change or drop any persona the team says does not exist among its customers, and record why. A persona you set aside, for example because it overlaps another, goes in `working-backwards/set-aside-personas.md`, never in `personas/`, so the brief and AI-DLC see only the personas the team kept.

### Step 2: Persona critique (mode `critique`)
- **Mode**: `agentic`
- **Input**: The personas, `prototype/index.html`, `prfaq.md`, `riskiest-assumption.md`
- **Output**: `discovery/{{project}}/prototype/persona-critique.md`
- **Validate**: Every persona walked through the core flow and gave a day-one adoption score with a reason
- **On failure**: If the prototype is missing, say so; the critique needs something to react to

Follow `references/persona-critique.md`. When the prototype shows AI output from the PRD's AI feature block, each persona also reacts to that output: would they trust it, act on it, or want something else. Run each persona in turn, then summarize what the critique shows and which risk each finding points to. Hand the findings to **discovery-prototype** for the iteration; **discovery-validate** reads the file later.

### Step 3: Talk to a persona or run a panel (mode `simulate`)
- **Mode**: `agentic`
- **Input**: A persona name, or a topic for a panel
- **Output**: The conversation; for a panel, `working-backwards/personas/panel-[topic].md`
- **Validate**: Each answer starts with `**[Persona: Name]**` and stays in character
- **On failure**: If the persona does not exist, list the project's personas

For a single persona, answer as that person until the user says "stop": their language, their pain points, their constraints. When something is outside their experience, say so. For a panel, ask each persona the same question in turn, then summarize where they agree and where they differ. Useful in Working Backwards to test a PR/FAQ headline, and in prep calls.

## Output

- `working-backwards/personas/[first-name].md`: one per persona, in the format in `references/persona-document.md`
- `prototype/persona-critique.md`: one section per persona and a findings table
- `working-backwards/personas/panel-[topic].md`: optional

## Lessons Learned

### Do
- Generate personas before scoring; scoring and the PR/FAQ use them.
- Include one satisfied customer.
- Vary names, genders, ages, and backgrounds across personas, and never pair them with roles by stereotype. If two personas share the same demographic pattern, change one.
- Ask the team whether it recognizes each persona.

### Don't
- Invent quotes, or give a persona traits the data does not show.
- Let a critique come back with no problems; ask again, more specifically.
- Treat a persona's reaction as customer evidence; it is a hypothesis to test.

### Common Failures
- **Two personas are the same person with different names.** Merge them.
- **A persona has only one feedback item behind it.** Keep it with Low confidence, or drop it if the team agrees.
- **The critique drifts into feature requests.** Bring it back to the persona's pain and workflow.

### When to Ask the User
- The team does not recognize a persona.
- The data supports fewer segments than the requested count.
- The team wants a specific persona that the data does not show; create it only as Assumed.
