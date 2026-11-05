---
name: discovery-team-space
display_name: "AI-DLC Discovery: Team Space"
icon: "👥"
description: "Saves an AI-DLC Discovery workshop in an Amazon Quick team Space instead of a local folder, so several people can follow, open, and take over the same workshop from their own Amazon Quick Desktop. Amazon Quick only, and optional: without a Space the workshop runs from a local folder as usual. Use when the team wants to share the workshop in a Space, take over from another facilitator, or run pods in one Space."
trigger: "team-space shared-workshop take-over"
patterns:
  - pattern: '(?i)\b(?:team|shared)\s+space\b'
    confidence: 0.85
  - pattern: '(?i)\btak(?:e|ing)\s+over\b.{0,40}\bworkshop\b'
    confidence: 0.85
inputs:
  - name: space
    description: "The Amazon Quick Space the workshop is saved in. The team creates and names it; use the Space attached to the chat."
    type: string
    required: false
  - name: project
    description: "The workshop's project folder under discovery/."
    type: string
    required: true
  - name: driver
    description: "Who is writing the workshop now: a role or a first name, never an email or an alias."
    type: string
    required: true
tools: [file_read, file_write, file_rag_search]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery: Team Space

## Overview

By default a Discovery workshop lives in one working folder on one laptop. With this skill it lives in an Amazon Quick **team Space** instead: the same `discovery/{{project}}/` files, saved in the Space, so everyone the Space is shared with can attach it in their own Amazon Quick Desktop, read every artifact, ask questions about it, open the prototype, and take over facilitation.

It works for one person too: the workshop then lives in Amazon Quick, and any of your chats can open it. It is a feature of Amazon Quick, not of the method. Nothing in the phases, the checkpoints, or the files changes. It only changes where the files are read from and written to, and it adds one rule: **one driver at a time**, because saving a file to a Space replaces it.

What Amazon Quick does, as relied on here: with a Space attached to the chat (the chat's **+** menu, then **Spaces**), a file can be saved into the Space at a folder path, saving it again replaces it with the same document, it can be read back word for word at once, and an HTML file saved there opens in the session tab. Search over the Space catches up a moment after a write; exact reads do not wait.

## Workflow

### Step 1: Set up the Space
- **Mode**: `agentic`
- **Tool**: `file_write`, `file_read`
- **Input**: `{{space}}`, `{{project}}`, `{{driver}}`
- **Output**: `discovery/{{project}}/PROJECT.md` in the Space, with the storage, the Space, and the driver
- **Validate**: The team confirmed the Space, and a test write of `PROJECT.md` reads back word for word
- **On failure**: Ask the team to attach the Space to this chat (the **+** menu, then **Spaces**) and to check it is an Owner of it; otherwise offer to continue in a local folder

1. **Find the team's Space.** The team creates the Space and chooses its name; do not invent one. If one Space is attached to this chat, use it and confirm its name with the team. If several are attached, ask which one. If none is, ask the team to create one (in Amazon Quick, **Spaces**, then **Create space**), share it with the people who will follow the workshop, and attach it to this chat with the **+** menu, then **Spaces**. Stop until it is attached. Use its name as `{{space}}` from here on.
2. Tell the team that Amazon Quick may ask them to approve each save to the Space, and to approve it. Then write `PROJECT.md` to `discovery/{{project}}/` in the Space, with these lines under the scope, and read it back:

   ```markdown
   | Storage | Team Space: {{space}} | Confirmed |
   | Driver | {{driver}}, since [date and time] | Confirmed |
   ```

3. **Keep the customer data out of the team Space.** Everything in a Space can be read and queried by everyone it is shared with. The raw data stays where `data_location` points: the driver's local `discovery/data/`, or a separate Space shared only with the people allowed to see it. Never copy raw records, exports, or data files into the team Space. If `data_location` is the team Space itself, say so and ask the team to confirm one of two things before Signals: the data is fictional sample data, or the Space is shared only with people allowed to see the data. Record the answer in `PROJECT.md`. Otherwise ask them to move the data.
4. Tell the team who can do what: people the Space is shared with as **Owners** can follow and take over; people shared as **Viewers** can read, ask questions, and open the prototype, but should not drive.

### Step 2: Every read and write
- **Mode**: `agentic`
- **Tool**: `file_read`, `file_write`
- **Input**: Any artifact a phase reads or writes
- **Output**: The artifact at the same path, in the Space
- **Validate**: The driver in `PROJECT.md` is this chat's driver before every write
- **On failure**: Stop and ask before writing

Every path in the workshop, `discovery/{{project}}/...`, is a path in the Space. Read inputs from the Space, not from a local copy, so you always see the last version someone saved.

Before every write:

1. Read `PROJECT.md` from the Space. If the driver is not `{{driver}}`, stop: "[Driver] is driving this workshop since [time]. Take over?" Write only after the team says yes, and update the driver line first (Step 3).
2. Check the text for personal data (names of real people, emails, phone numbers, account or CRM identifiers). Quotes carry personas and segments only. If you find any, remove it before saving and say what you removed.
3. Save the file to its path in the Space. Saving again replaces it: keep the rule that prototype versions are never overwritten by always writing a new `vN.html`.

The progress board's Location column shows Space paths, for example `Space {{space}}: discovery/{{project}}/working-backwards/prfaq.md`.

### Step 3: Take over or continue
- **Mode**: `agentic`
- **Tool**: `file_read`, `file_write`
- **Input**: A request to continue the workshop from the Space, with the new driver
- **Output**: The driver line updated, and the workshop resumed at the next step
- **Validate**: The team confirmed the take-over
- **On failure**: If `PROJECT.md` is not in the Space, list the Space's `discovery/` folders and ask which project

Someone else's Amazon Quick picks the workshop up with: "Continue the AI-DLC Discovery workshop for [project] from discovery/[project]/PROJECT.md in the [space] space. I'm taking over as [driver]. Start at [step]."

Read `PROJECT.md` and the files the next step needs from the Space. Show who was driving and since when, and ask the previous driver to stop writing. Update the driver line, show the progress board, and continue at the step the team names. If the last write was moments ago, read it again before continuing, in case it was still being saved.

### Step 4: Pods
- **Mode**: `agentic`
- **Input**: Pods named at setup
- **Output**: One project per pod in the same Space
- **Validate**: Each pod has its own project and driver
- **On failure**: None

With pods, each pod is its own project in the Space, `discovery/{{project}}-[pod]/`, with its own `PROJECT.md` and driver, created after scoring when each pod takes its use case. Copy the shared Signals and Working Backwards scoring artifacts into each pod's project, so each one is complete. Pods never write to each other's files. The facilitator can attach the Space and see every pod.

### Step 5: Prototype and Handoff in a Space
- **Mode**: `agentic`
- **Input**: The prototype and Handoff steps
- **Output**: The same artifacts, in the Space
- **Validate**: The prototype opens in the session tab from its Space copy
- **On failure**: If it does not open, save a local copy and open that

- **Prototype.** Save every version to the Space, then open it in the session tab from the Space copy. Tell the team that anyone can open it the same way in their own Amazon Quick; opened from the Space in a browser, it downloads instead of showing. `compare.html` has the same limit as in a local folder: its frames cannot load the version files in the session tab.
- **Handoff.** Write the brief and next steps to the Space as usual. There is no repository in a Space, so do not write `.gitignore`. The AI-DLC team knowledge file, `aidlc/spaces/[space]/knowledge/...`, is AI-DLC's own folder layout and has nothing to do with Amazon Quick Spaces: save it in the team Space at that path like any other artifact. In `next-steps.md`, say how to start the build: download the `discovery/{{project}}/` and `aidlc/` folders from the Space into the repository where the team will build, never the data.

## Output

In the team Space:

```text
discovery/
└── {{project}}/              every workshop artifact, at the usual paths
aidlc/                        AI-DLC team knowledge, when the route is AI-DLC
```

And in `PROJECT.md`, the Storage and Driver lines.

## Lessons Learned

### Do
- Read `PROJECT.md` from the Space before every write.
- Keep the raw customer data out of the team Space.
- Name the driver by role or first name.

### Don't
- Write while someone else is driving.
- Copy data files into the team Space to make Signals easier.
- Treat `aidlc/spaces/` as an Amazon Quick Space.

### Common Failures
- **Two people wrote at once.** The last save wins. Ask both what they changed, re-read the file from the Space, and redo the lost change as the agreed driver.
- **The Space is not attached.** Saves fail or land in a local folder. Ask the team to attach it, then save again.
- **A Viewer tries to drive.** The write may fail. Ask an Owner to share the Space with them as Owner, or let an Owner drive.

### When to Ask the User
- The driver in `PROJECT.md` is someone else.
- The data location is the team Space.
- More than one `discovery/` project could be the one to continue.
