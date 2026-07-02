---
name: aidlc-discovery
display_name: AI-DLC Discovery
description: "Guided product-definition interview (PM + tech lead) producing Product-Definition/ (vision + technical constraints + open questions). Activate with 'start aidlc-discovery' / 'inicia aidlc-discovery'."
icon: "🔍"
trigger: start aidlc-discovery
inputs:
  - name: depth
    description: "quick (CORE questions only) or full (all). Ask if not provided."
    type: string
    required: false
  - name: mode
    description: "single | sequential | parallel (PM and tech lead in separate sessions)."
    type: string
    required: false
tools: [file_read, file_write, file_edit, folder_create, folder_list, run_python, url_fetch, web_search, open_in_session_tab]
depends-on: [quick_suite__spaces]
---

## Overview

Amazon Quick adapter for AI-DLC Discovery. This skill is **self-contained**: the shared core is bundled
inside this skill's own folder (`aidlc-common/`, `skills/`, `aidlc-discovery-rules/`), because Quick
loads each skill as an isolated folder and does not load sibling directories. All file references below
are **relative to this skill's folder**; Quick resolves the actual install location. Interaction is
**conversational** (Quick has no file-based `[Answer]:` flow): questions are asked in chat.

## Workflow

1. **Read the core.** `file_read` the bundled `aidlc-common/protocols/orchestrator-protocol.md` (in this
   skill's folder) — single source of truth; follow its flow. Conventions are in `aidlc-common/conventions/`;
   question banks in `aidlc-discovery-rules/aidlc-discovery-rule-details/{business,technical}/*-interview.md`.
2. **Session + shared selection.** Scaffold `Product-Definition/` per `aidlc-common/conventions/state-schema.md`.
   Ask project-type, depth, mode in chat. Interaction is `conversational` for Quick.
3. **Role interviews (conversational).** For `product-discovery` and `tech-discovery`, ask the question bank
   one at a time (or small groups of 2–3). After each answer, append to the role's `*-answers-history.md`
   and update `*-state.md` (persistence per `aidlc-common/conventions/question-format.md`). If a Quick Space
   holds context, offer to pre-fill answers (`depends-on quick_suite__spaces`).
4. **Join barrier.** When both roles complete, confirm via `state/session-index.md` (or `run_python` the
   bundled `aidlc-common/scripts/process-checker.js`), then run `open-questions` to consolidate and flag
   cross-role contradictions.
5. **Visual (opt-in) + handoff.** Render the paste-ready handoff per `aidlc-common/conventions/handoff-format.md`,
   then `open_in_session_tab` the outputs in `Product-Definition/`.

## Output

`Product-Definition/` — `vision-document.md`, `technical-environment.md`, `open-questions.md`, `[visual/]`.
