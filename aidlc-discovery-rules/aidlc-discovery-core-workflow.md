# PRIORITY: This workflow OVERRIDES all other built-in workflows
# When user requests to define a product (vision + technical environment) for AI-DLC, ALWAYS follow this workflow FIRST

## Purpose

`aidlc-discovery` (AI-DLC Discovery) is a role-based interview workflow that produces the two canonical inputs AI-DLC expects before the Inception phase:

1. **Vision Document** — what to build and why (Business role)
2. **Technical Environment Document** — what tools and constraints apply (Technical role)

It mirrors the AI-DLC pattern (Question → Doc → Approval, durable state, audit log) but is scoped to product definition rather than software construction.

## Adaptive Workflow Principle

**The workflow adapts to the session, not the other way around.**

The AI model intelligently:
1. Detects whether the user is starting fresh or resuming an existing definition session
2. Routes the user to the appropriate role-based interview (Business / Technical / Both sequential)
3. Adjusts brownfield vs greenfield question branches
4. Persists state at the per-question granularity

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files under:

- `aidlc-discovery-rules/aidlc-discovery-rule-details/`

All subsequent rule detail file references (e.g., `common/role-selection.md`, `business/vision-interview.md`) are relative to that directory.

**Common Rules**: ALWAYS load common rules at workflow start:

- Load `common/welcome-message.md` for the welcome banner
- Load `common/language-handling.md` for language detection and the user-facing / control split
- Load `common/session-continuity.md` for session resumption guidance
- Load `common/role-selection.md` for role routing
- Load `common/question-format-guide.md` for question formatting rules
- Load `common/content-validation.md` for content validation requirements
- Load `common/audit-format.md` for audit log format
- Reference these throughout the workflow execution

## MANDATORY: Content Validation

**CRITICAL**: Before creating ANY file, you MUST validate content according to `common/content-validation.md` rules:
- Escape special characters properly
- Keep tables well-formed
- Provide text alternatives for complex visual content

## MANDATORY: Question File Format

**CRITICAL**: When asking questions at any phase, you MUST follow question format guidelines.

**See `common/question-format-guide.md` for complete question formatting rules including**:
- Multiple choice format (A, B, C, D, X options)
- `[Answer]:` tag usage
- Answer validation and ambiguity resolution

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY `aidlc-discovery` invocation, you MUST display the welcome message.

**How to Display Welcome Message**:
1. Load the welcome message from `common/welcome-message.md`
2. Display the complete message to the user
3. This should only be done ONCE at the start of a new workflow or when the user explicitly starts a new session
4. Do NOT load this file in subsequent interactions to save context space

---

# AI-DLC DISCOVERY WORKFLOW

**Purpose**: Collect the information AI-DLC needs to begin Inception.

**Focus**: Determine WHAT to build (Business) and WITH WHICH TOOLS (Technical).

**Stages**:
- Session Detection (ALWAYS)
- Language Detection (ALWAYS — new sessions only; resumes read it from state)
- Role Selection (ALWAYS — unless resuming)
- Project Type Selection (ALWAYS — Greenfield or Brownfield)
- Business Interview (CONDITIONAL — if role includes Business)
  - Step 0: Depth Selection (Quick ~10 min / Full ~25 min)
  - Sections 1–6 (depth-filtered)
- Technical Interview (CONDITIONAL — if role includes Technical)
  - Step 0: Depth Selection (Quick ~12 min / Full ~35 min)
  - Sections T1–T8 (depth-filtered)
- Open Questions Compilation (ALWAYS — at the end of each completed role)
- Visual Sketch (OPTIONAL — opt-in, after Open Questions, before Final Handoff)
- Final Handoff (ALWAYS — after all selected roles complete)

---

## Session Detection (ALWAYS EXECUTE)

1. **MANDATORY**: Prepare to log the initial user request in `Product-Definition/audit.md` with complete raw input (create the file if missing — see `common/audit-format.md`)
2. Load all steps from `common/session-continuity.md`
3. Execute session detection:
   - Check for existing `Product-Definition/aidlc-discovery-state.md` in the current working directory
   - If present, parse the state and present a resume summary
   - If absent, prepare a fresh `Product-Definition/` directory scaffold
4. Determine next stage:
   - **New session** → Language Detection
   - **Resume** → load `User Language` from state and skip Language Detection; present the resume summary in the stored language
5. **MANDATORY**: Log findings in `Product-Definition/audit.md`

---

## Language Detection (ALWAYS EXECUTE — new sessions only)

1. **MANDATORY**: Log any user input during this stage in `Product-Definition/audit.md`
2. Load all steps from `common/language-handling.md`
3. Detect the user's language using the priority order: (1) explicit instruction, (2) workspace steering files like `CLAUDE.md`, (3) prompt-inference from the user's invocation, (4) default to English
4. Record `User Language`, `Language Source`, and `Detected` timestamp in `aidlc-discovery-state.md`
5. If the source is not `explicit`, ask for one-time confirmation in the detected language (see `common/language-handling.md` §"Confirmation")
6. From this point on, ALL user-facing content is in the confirmed language; control content stays in English (see `common/language-handling.md` for the complete list)
7. **MANDATORY**: Log the detection and confirmation in `Product-Definition/audit.md`

---

## Role Selection (ALWAYS EXECUTE — unless resuming with a role already selected)

1. **MANDATORY**: Log user input in `Product-Definition/audit.md`
2. Load all steps from `common/role-selection.md`
3. Present role options to the user:
   - **A) Business** — fill in the Vision Document only
   - **B) Technical** — fill in the Technical Environment Document only
   - **C) Both (sequential)** — complete Business first, then Technical (Technical will use the Vision as context)
   - **X) Other** — user describes a custom flow
4. Write the selection into `Product-Definition/interview/role-selection.md`
5. Update `Product-Definition/aidlc-discovery-state.md` with the chosen role
6. **MANDATORY**: Log user's response in `Product-Definition/audit.md` with complete raw input

---

## Project Type Selection (ALWAYS EXECUTE)

1. **MANDATORY**: Log user input in `Product-Definition/audit.md`
2. Load all steps from `shared/greenfield-vs-brownfield.md`
3. Ask whether the project is Greenfield or Brownfield (multiple choice per `common/question-format-guide.md`)
4. Write the answer into `Product-Definition/interview/project-type.md`
5. Update `Product-Definition/aidlc-discovery-state.md` with the project type
6. **MANDATORY**: Log user's response in `Product-Definition/audit.md`

---

## Business Interview (CONDITIONAL)

**Execute IF**: Role selection includes Business (A or C).

**Skip IF**: Role selection is Technical only (B).

**Execution**:
1. **MANDATORY**: Log any user input in `Product-Definition/audit.md`
2. Load all steps from `business/vision-interview.md`
3. **Step 0 — Depth Selection**: ask the user Quick pass (~10 min, 8 core questions) vs Full interview (~25 min, all 18 questions); record in state
4. Execute per-section interview using the per-question granularity tracked in `aidlc-discovery-state.md`
5. Each batch: write 5–7 unanswered questions into `Product-Definition/interview/business/vision-questions.md` using the formats in `common/question-format-guide.md` (with the mandatory progress header and "ready" footer)
6. Wait for the user to reply with the single word **`ready`**; then **re-read** the file (do NOT rely on in-memory content)
7. Validate answers per `common/content-validation.md`, flag ambiguities, write the batch into `Product-Definition/interview/business/vision-answers-history.md` (batched append — one block per batch, not per question), tick off state entries
8. Continue until all selected sections are complete (depth-dependent)
9. Execute completion steps from `business/vision-completion.md`:
   - Render `Product-Definition/vision-document.md`
   - Mark Business as ✅ complete in `aidlc-discovery-state.md`
   - **Wait for Explicit Approval** before handing off to the Technical role
10. **MANDATORY**: Log user's response in `Product-Definition/audit.md`

---

## Technical Interview (CONDITIONAL)

**Execute IF**: Role selection includes Technical (B or C).

**Skip IF**: Role selection is Business only (A).

**Execution**:
1. **MANDATORY**: Log any user input in `Product-Definition/audit.md`
2. Load all steps from `technical/tech-env-interview.md`
3. If `Product-Definition/vision-document.md` exists, load it as context for coherence (but do NOT modify it)
4. **Step 0 — Depth Selection**: ask the user Quick pass (~12 min, 10 core questions) vs Full interview (~35 min, all 29 questions); record in state
5. Execute per-section interview using per-question granularity
6. Each batch: write 5–7 unanswered questions into `Product-Definition/interview/technical/tech-env-questions.md` using the formats in `common/question-format-guide.md` (with the mandatory progress header and "ready" footer)
7. Wait for the user to reply with the single word **`ready`**; re-read; validate; append the batch (batched write, one block per batch) to `Product-Definition/interview/technical/tech-env-answers-history.md`
8. Continue until all selected sections are complete
9. Execute completion steps from `technical/tech-env-completion.md`:
   - Render `Product-Definition/technical-environment.md`
   - Mark Technical as ✅ complete in `aidlc-discovery-state.md`
   - **Wait for Explicit Approval** before final handoff
10. **MANDATORY**: Log user's response in `Product-Definition/audit.md`

---

## Open Questions Compilation (ALWAYS EXECUTE at the end of each role)

1. Load all steps from `shared/open-questions-collector.md`
2. Scan the completed interview artefacts for user-declared uncertainties and AI-flagged ambiguities
3. Append them to `Product-Definition/open-questions.md` (grouped by role)
4. These will be consumed by AI-DLC during Requirements Analysis as pre-declared ambiguities

---

## Visual Sketch (OPTIONAL — runs once, after Open Questions Compilation, before Final Handoff)

**Execute IF**: All selected roles are ✅ complete AND the user has not previously answered this stage's opt-in question for the current session.

**Skip IF**: The user already chose to skip in this session, or the workflow is resuming with `Visual Sketch — Status: ✅ Complete | Skipped | Discarded`.

**Execution**:
1. **MANDATORY**: Log any user input in `Product-Definition/audit.md`
2. Load all steps from `shared/visual-sketch.md`
3. Step 0 — present the opt-in question and wait for `ready`
4. If the user picks **No** → log `Visual Sketch — Skipped` and proceed to Final Handoff
5. If the user picks **Yes**:
   - Step 1 — write the 5-question mini-interview into `Product-Definition/interview/visual/visual-questions.md`, wait for `ready`, validate, append to `visual-answers-history.md`, tick state checkboxes
   - Step 2 — read context (Vision, Technical Environment, visual answers) and generate `user-journey.md` (Mermaid) and one self-contained HTML file per journey node under `visual/mockups/`, plus `index.html`
   - Step 3 — run the cross-validation checks from `shared/visual-sketch.md`
   - Step 4 — present the gate (Request Changes / Approve and Continue / Discard and Skip)
   - Step 5 — handle the gate response and update state accordingly
6. Whatever path was taken, proceed to Final Handoff
7. **MANDATORY**: Log every batch write, validation result, and gate decision in `Product-Definition/audit.md`

**Output (sidecar — referenced in the AI-DLC handoff but not a formal AI-DLC interview input)**:
```
Product-Definition/
├── visual/                            # output — referenced by the handoff prompt
│   ├── user-journey.md
│   └── mockups/
│       ├── index.html
│       └── <NN>-<slug>.html  ×N
└── interview/visual/                  # workspace — process artefacts
    ├── visual-questions.md
    └── visual-answers-history.md
```

---

## Final Handoff (ALWAYS EXECUTE)

1. Confirm all selected roles are ✅ complete in `aidlc-discovery-state.md`
2. Confirm Visual Sketch reached a terminal state (`✅ Complete`, `Skipped`, or `Discarded`) — see `## Visual Sketch` block above
3. Render the handoff message. Adapt the OPTIONAL block based on whether `Product-Definition/visual/` exists (i.e. Visual Sketch was approved):

```
AI-DLC Discovery Complete ✅

To kick off AI-DLC, paste this into a fresh context:

  I'm starting a new project. Please read the following inputs before
  beginning the AI-DLC workflow:

  REQUIRED inputs (always present):

  • Product-Definition/vision-document.md
    The Vision Document — what we're building, who it's for, the success
    metrics, and what's in/out of MVP scope. Use this as the primary input
    to Requirements Analysis.

  • Product-Definition/technical-environment.md
    The Technical Environment Document — required languages, frameworks,
    cloud services, architecture patterns, security/compliance constraints,
    testing standards, and example code patterns. These are binding
    constraints for NFR Requirements, NFR Design, Infrastructure Design,
    and Code Generation.

  • Product-Definition/open-questions.md
    Pre-declared ambiguities and open items the user already knows about.
    Treat each as a clarifying question to resolve during Requirements
    Analysis — do not silently assume defaults.

  OPTIONAL inputs (only if Visual Sketch was approved — check if folder exists):

  • Product-Definition/visual/user-journey.md
    Mermaid flowchart(s) showing the user journey through the product per
    persona. Use as reference for UX flows when designing requirements
    and APIs.

  • Product-Definition/visual/mockups/index.html and the screen files
    Self-contained HTML mockups of the main screens. NOT functional code —
    they are visual references for primary CTAs, screen-to-screen
    navigation, and the data each screen displays. Cross-reference against
    user-journey.md.

  Please confirm you've read all available files, then begin the AI-DLC
  workflow at the Inception phase.
```

   When generating the message, include the OPTIONAL block only if `Product-Definition/visual/` exists. If the user skipped or discarded Visual Sketch, omit the entire OPTIONAL section.

4. **MANDATORY**: Log completion in `Product-Definition/audit.md`

---

## Key Principles

- **Adaptive Execution**: Only run the roles and depth the user selected
- **Transparent Progress**: Every batch starts with a progress bar and time estimate
- **Single-Word Trigger**: User replies `ready` to move forward — no need to type full instructions
- **User Control**: User can change role, change depth mid-stream, skip sections, or backlog items at any gate
- **Per-Question Progress Tracking**: `aidlc-discovery-state.md` tracks every question individually, but writes are batched per-batch (not per-question) to keep the loop snappy
- **Complete Audit Trail**: Log ALL user inputs and AI responses in `audit.md` with timestamps
  - **CRITICAL**: Capture user's COMPLETE RAW INPUT exactly as provided
  - **CRITICAL**: Never summarize or paraphrase user input in audit log
  - **CRITICAL**: Log every interaction, not just approvals
- **Quality Focus**: The outputs are the contract between you and AI-DLC — accuracy matters more than speed

## MANDATORY: Per-Question Checkbox Enforcement

1. **NEVER complete any question without updating the state checkbox**
2. **IMMEDIATELY after confirming an answer, mark that question `[x]` in `aidlc-discovery-state.md`**
3. **This must happen in the SAME interaction where the answer is confirmed**
4. **NO EXCEPTIONS**: Every confirmed answer MUST be tracked with a checkbox update

## Prompts Logging Requirements

- **MANDATORY**: Log EVERY user input (prompts, questions, responses) with timestamp in `Product-Definition/audit.md`
- **MANDATORY**: Capture user's COMPLETE RAW INPUT exactly as provided (never summarize)
- **CRITICAL**: ALWAYS append changes to `audit.md`, NEVER overwrite its contents
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Include stage context for each entry

See `common/audit-format.md` for the exact template.

## Directory Structure

```text
<WORKSPACE-ROOT>/                              # Where the user invokes the rule (cwd)
│
├── Product-Definition/                        # Generated by aidlc-discovery (ALL outputs live here)
│   │
│   │   # Control files — read by the workflow to resume / audit
│   ├── aidlc-discovery-state.md               # Per-question state + role progress
│   ├── audit.md                               # Append-only ISO8601 log
│   │
│   │   # Final outputs — referenced in the AI-DLC handoff prompt
│   ├── vision-document.md                     # ✅ FINAL — Vision Document (Business)
│   ├── technical-environment.md               # ✅ FINAL — Technical Environment (Technical)
│   ├── open-questions.md                      # ✅ FINAL — Pre-declared ambiguities
│   │
│   │   # Visual sidecar — only present if Visual Sketch was approved
│   ├── visual/
│   │   ├── user-journey.md                    # Mermaid flowchart(s)
│   │   └── mockups/
│   │       ├── index.html                     # Hub linking every screen
│   │       └── <NN>-<slug>.html               # One file per journey node
│   │
│   │   # Process workspace — drafts and batches; descartable post-handoff
│   └── interview/
│       ├── role-selection.md                  # Initial Q: Business | Technical | Both
│       ├── project-type.md                    # Initial Q: brand-new | feature | migration
│       ├── business/
│       │   ├── vision-questions.md            # Active questions with [Answer]: tags
│       │   └── vision-answers-history.md      # Confirmed answers (append-only)
│       ├── technical/
│       │   ├── tech-env-questions.md
│       │   └── tech-env-answers-history.md
│       └── visual/                            # Only if Visual Sketch was approved
│           ├── visual-questions.md
│           └── visual-answers-history.md
│
└── aidlc-discovery-rules/                     # The rule set itself (read-only for the workflow)
    ├── aidlc-discovery-core-workflow.md       # ← You are here
    └── aidlc-discovery-rule-details/
        ├── common/
        ├── business/
        ├── technical/
        └── shared/
```

**CRITICAL RULES**:
- Generated artefacts: `Product-Definition/` only.
- The `Product-Definition/` root holds **two control files**, **three final outputs** consumed by AI-DLC, and the **optional `visual/` sidecar** referenced from the handoff prompt.
- All process artefacts (initial setup answers, per-batch question files, answer history) live under `Product-Definition/interview/`.
- The `aidlc-discovery-rules/` directory is the rule set and must not be edited by the workflow itself.
