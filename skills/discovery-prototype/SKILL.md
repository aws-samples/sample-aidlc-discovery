---
name: discovery-prototype
display_name: "AI-DLC Discovery: Prototype"
icon: "🔨"
description: "Prototype phase of AI-DLC Discovery: builds a polished, clickable prototype of the core user flow, with several screens shown on a phone and in a desktop browser, in one self-contained HTML file, aimed at the riskiest assumption, then gets the persona critique and iterates with the team. Use when the user wants to build, change, or share a prototype, mockup, or click-dummy for a Discovery use case."
trigger: "prototype click-dummy mockup"
patterns:
  - pattern: '(?i)\b(?:build|create|generate|make|update|iterate)\b.{0,15}?\b(?:prototype|click-?dummy|mock-?up)\b'
    confidence: 0.90
inputs:
  - name: project
    description: "Project folder name under discovery/."
    type: string
    required: true
  - name: use_case
    description: "The selected use case. With pods, each pod builds its own prototype."
    type: string
    required: true
  - name: design_standards
    description: "Optional: the team's design system, as a file in the working folder or a description of colors, type, and components."
    type: string
    required: false
depends-on: [discovery-personas]
tools: [file_read, file_write, open_in_session_tab]
version: "0.4.0"
license: MIT-0
---

# AI-DLC Discovery: Prototype

## Overview

A prototype gives the team and its personas something to react to, which teaches more than another document. This skill turns the PRD into a prototype that looks like a real product: the core user flow as several screens, shown side by side on a flow board, clickable on a phone, and laid out for a desktop browser. It is one self-contained HTML file with no dependencies, built so the riskiest assumption can be tested in it. The team clicks through it as its main persona would, the personas critique it in their own voices, and the team changes it at least once before Validate tries to break it.

## Workflow

### Step 1: Plan the screens
- **Mode**: `agentic`
- **Input**: `prd.md`, `prfaq.md`, `riskiest-assumption.md`, the personas
- **Output**: A screen plan, shown to the team
- **Validate**: The team confirms the plan, and one screen is marked as the test moment for the riskiest assumption
- **On failure**: If the PRD has no P0 features, return to **discovery-working-backwards**

Plan the core user flow as 4 to 8 screens: the entry point, the steps of the main task, the confirmation, and the main unhappy path. For each screen, give one line: what the persona sees and does, and which P0 requirement it carries. Mark the test moment, where the riskiest assumption becomes visible. When the PRD has an AI feature block, the screens that show the AI feature use its sample outputs, word for word, labelled as sample output from the first-draft prompt, so the team and the persona critique react to real AI output. Include at least one edge or negative case on screen. When the Signal Analysis Report has telemetry, name the journey step the test moment is meant to change (for example, the step where most sessions leave for Contact us). Propose a visual direction in one line (for example "warm neutrals, serif headings, one green accent"), or use the team's design standards. Ask the team to confirm, cut, or add. A focused flow that tests the assumption beats a complete app.

### Step 2: Build
- **Mode**: `agentic`
- **Tool**: `file_write`, then `open_in_session_tab`
- **Input**: The confirmed screen list; `{{design_standards}}` if given
- **Output**: `discovery/{{project}}/prototype/v1.html`, copied to `prototype/index.html`, open in a session tab
- **Validate**: Every must-have below is present, and every item on the quality bar in `references/html-prototype.md` passes
- **On failure**: If a must-have is missing, the shell was edited outside the markers; start again from a fresh copy of the shell

Build every version from the shell, never from scratch and never by editing an earlier version's layout:

1. Load `references/prototype-shell.md` and `references/html-prototype.md` with `file_read`. The shell is the single HTML code block in `prototype-shell.md`; copy all of it.
2. Write the new version as an exact copy of that code block, changing **only** the region between the `EDIT BELOW` and `EDIT ABOVE` markers: the `PROTOTYPE` settings (product, version, tagline, URL, clock, theme, test moment, starting state) and one `<template data-screen>` per planned screen, 4 to 8, plus an optional `<template data-desktop>` for a screen that needs its own wide layout.
3. Keep everything outside the markers exactly as it is in the shell. The shell already provides the Flow, Mobile, and Desktop views, the phone and browser frames, the routes (`#/flow`, `#/mobile/screen-id`, `#/desktop/screen-id`), steppers, and the Show test moment toggle. Those are what make it a professional prototype, so never remove or rebuild them.

Put the design into the screens: the persona's real content, the states, one failure state, and the element under test marked with `class="test-moment"` on the screen that has `data-test-moment`. Adjust the look through `theme` (for example the accent color), not by editing the shell's styles.

Open it on the **Flow** view (`v1.html#/flow`), so the team sees the whole journey before clicking through it. Then write the first entry in `prototype/versions.md`.

### Step 3: Team click-through
- **Mode**: `agentic`
- **Input**: The first build
- **Output**: The team's reactions
- **Validate**: The team walked the core flow and the test moment
- **On failure**: None

Show the Flow view, then ask the team to click through the core flow in the Mobile or Desktop view, whichever the main persona uses. Ask: where would this person hesitate? Does the test moment make the riskiest assumption visible? Note the reactions; do not change the prototype yet.

### Step 4: Persona critique
- **Mode**: `agentic`
- **Input**: The first build, the personas, the riskiest assumption
- **Output**: `discovery/{{project}}/prototype/persona-critique.md`
- **Validate**: Every persona walked the core flow and gave a day-one adoption score
- **On failure**: If the personas are missing, ask **discovery-personas** to generate them

Use **discovery-personas** in `critique` mode. Teams often find little to change on their own first click-through; the personas, each grounded in its customer quotes, usually find the problems that matter.

### Step 5: Iterate
- **Mode**: `agentic`
- **Input**: The team's reactions and the critique's findings
- **Output**: A new version, `prototype/v2.html` (then `v3.html`, and so on), copied to `prototype/index.html`; `prototype/versions.md` and `prototype/notes.md` updated; `prototype/compare.html`
- **Validate**: At least one new version, logged in `versions.md` with the finding or request behind each change; earlier versions untouched
- **On failure**: None

Show the team the critique's findings next to its own reactions, and ask which to fix now. Make the changes in plain language. A fix that promises a capability nobody has confirmed (holding seats, sending health or financial data by email or link, a real-time feed) is a question for the build, not a design detail: before adding it, tell the team what it depends on and who must confirm it. If they keep it, log it in `versions.md` as Needs evidence and list it in `notes.md` as a feasibility or compliance question for Validate. Record in the critique which findings were fixed and which were not, and why. Stop when the prototype is good enough to start a conversation, not when it is finished.

Every build or iteration is a **new version file**. Never overwrite a version: the team may want to go back, and Validate picks one. Copy the latest to `index.html`, so links keep working, until the team picks another.

In `versions.md`, add one row per version: what changed, why (the critique finding, the team's reaction, or the request), and who asked. In `notes.md`, keep the screens, the core flow, and the test moment up to date for the current version. Handoff uses both for the brief's prototype section.

Once there are two versions or more, write `prototype/compare.html` from `references/prototype-compare.md`, changing only its `COMPARE` list between the markers: one entry per version with its file and the change from `versions.md`, and `chosen` once Validate picks one. It shows the versions side by side on the Flow, Mobile, or Desktop view.

### Optional: In-codebase prototype
When the working folder is the product's own repository and the harness can run code, the team can ask for a disposable prototype in the real product: follow `references/codebase-prototype.md`. It is never offered in Amazon Quick, and never started without the team asking.

## Output

- `prototype/v1.html`, `v2.html`, …: every version, never overwritten, each a single file with Flow, Mobile, and Desktop views
- `prototype/index.html`: a copy of the current or chosen version
- `prototype/versions.md`: the version log
- `prototype/compare.html`: the versions side by side, once there are two or more
- `prototype/persona-critique.md`: written by **discovery-personas**, with which findings the iteration fixed
- `prototype/notes.md`:

```markdown
# Prototype notes: [use case]

## Screens
### [Screen name]
Purpose / main elements / actions

## Core flow
1. ...

## Test moment
Where the riskiest assumption is tested, and what the team expects to see.

```

`prototype/versions.md`:

```markdown
# Prototype versions: [use case]
Current: v[N] | Chosen for the handoff: [v[N], or "not yet"]

| Version | Date | What changed | Why | Asked by |
|---------|------|--------------|-----|----------|
| v1 | ... | First build from the screen plan | - | - |
| v2 | ... | ... | Critique finding 1: ... | Team |
```

## Lessons Learned

### Do
- Mark the test moment before building.
- Run the persona critique before iterating; it finds what the team misses.
- Save every iteration as a new version, and log why it changed.
- Use realistic content from the personas and signals.
- Keep it to one file so anyone can open it.

### Don't
- Build every P1 feature; the prototype tests an idea, not a release.
- Stretch the phone layout to fill a desktop screen; design the desktop view for its width.
- Add a backend, logins, or external libraries.
- Polish before the first click-through.

### Common Failures
- **The prototype looks finished but tests nothing.** Go back to the test moment.
- **The team iterates on colors.** Ask what the persona would trip over instead.
- **The file breaks after an edit.** Rewrite the affected screen rather than patching repeatedly.

### When to Ask the User
- Which screens to cut.
- Whether the test moment is right.
- When to stop iterating.
