# Changelog

All notable changes to `aidlc-discovery` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- **Cowork build.** `python3 scripts/build.py --target cowork` builds the same skills for Claude Cowork as one `.skill` file: Cowork tool names, `${CLAUDE_SKILL_DIR}` paths, and a "Running in Cowork" section. The AWS Quick build is unchanged.
- **Journey app**, in both builds: `discovery/[project]/journey.html`, one page that the room can follow, with the five phases, a **Now** banner with the current step and the next one, every artifact rendered, the prototype versions clickable in place, the decision and its conditions, and the evidence labels counted. The page is a fixed shell (`references/journey-shell.md`) that renders the project's files itself; a short Python update, in `references/journey-app.md`, copies the files into it at the start of every step and at every checkpoint, and checks that the shell is unchanged. AWS Quick opens it in the session tab, Cowork publishes it as an artifact, and opened from the working folder in a browser it refreshes itself every 15 seconds.
- In Cowork, every prototype version is also published as its own artifact, and each round of questions also appears as question cards.
- The README, the facilitator guides (English and Japanese), and the sample pages cover Claude Cowork next to AWS Quick: install, connecting a folder, and running the workshop.
- **Install with your assistant.** The README gives a prompt to paste into AWS Quick or Cowork, and install steps written for the assistant: it gets the right release package and prepares it, and the user does the last click. Each release now also publishes the Cowork `.skill` file.
- `tests/e2e/check_workspace.py` grades a working folder from any harness, with `--journey` for the journey app checks; `tests/test_cowork.py` covers the Cowork build, and `tests/test_journey.py` the journey app.

### Removed

- **Breaking:** the team Space (`discovery-team-space`): saving Discovery in an AWS Quick Space, the Storage and Driver lines in `PROJECT.md`, and taking over from another person's chat. Discovery is saved in the working folder, with one person at the keyboard. The `storage` and `space_name` config keys are gone. Data can still come from a Space.

### Fixed

Gaps that the first Cowork end-to-end run had to guess at, in both builds:

- **Unattended defaults.** The entry skill now has a default for every decision the team would make (the metric's direction, the team's expectations, candidates from Signals, overrides and re-scoring, the prototype version, commit, pivot, or park, building or testing first, the build route), and takes the round's recommended answer for anything else.
- **Config.** A key that `config.md` does not set takes its value from `config.default.md`.
- **Scoring.** The 3 to 5 is the team's own list; with the candidates from Signals, up to eight reach the gate.
- **Brief section 12** tells a product with no code in the working folder apart from a greenfield one.
- **Prioritization** writes the trend in words, as the plain-writing rules ask, not with arrows.
- **Samples** state which direction of the business metric is good.
- **Personas.** The count is the number of end-user personas, the satisfied customer included; a buyer persona, when the buyer is a different person, comes on top.
- **PR/FAQ.** The 500 to 700 words are a check, not a target: a short release means a paragraph is missing its job, and words are never added only to reach the range.
- **Prototype.** The test moment must sit on the core flow with no detour before it, instead of "two taps from the start", which a longer flow cannot meet.
- **Say and do.** The Signals template and the telemetry reference use the same column name, Reading.
- **Unattended runs** record "none given (unattended run)" where a step asks for the team's own input and has no recommendation, instead of writing a view as the team's.
- **Quotes.** An identifier inside a quote is replaced with a bracketed role, such as `[corporate account]`, and the quote still counts as verbatim.
- **Press release.** Paragraph 2 opens with the customer's situation today; only the other paragraphs open with what the product does.
- **Revenue.** Revenue amounts stay out of the repository; a share that sizes a segment, such as "a third of revenue", is fine.
- **Signal scores** have their 1 to 10 bands in Signals itself, the same bands Validate's prioritization uses, with ties ranked by severity.
- **Persona backgrounds** come from the data, then the market the data implies, then the company's home market, and only then the project language.
- **Scoring** keeps the team's name for each of its candidates next to the problem it is written as, in the Candidates table and the Taken forward line.
- **No time estimates.** The phase and step durations are removed: they were guesses. The survey's length limit and the P0 size check stay.
- **No placeholders** such as `[City]` or `[Name]` in a finished artifact: the press release uses the title alone, or the date without a city, and the gap goes to the open items.
- **Step order.** The readiness check drafts from what exists before the PRD; `draft` mode includes the feature description; Prototype logs a version before it opens it.
- **`PROJECT.md`** has one template in the entry skill, which the journey app reads.

---

## [3.0.0] — 2026-11-11

v3 replaces the interview workflow with a full Discovery process for AWS Quick Desktop. A team brings its customer feedback and leaves with a decision on what to build first, a clickable prototype, and a Discovery brief that a build, including AI-DLC, starts from.

### Added

- Five phases (Signals, Working Backwards, Prototype, Validate, Handoff), run by one entry skill, `aidlc-discovery`, that calls eleven job skills. Each job also works on its own.
- **Questions in rounds.** Every question to the team uses one format: a numbered question, a recommended answer worded so "yes" accepts it, and only the questions that are ready now. The assistant looks up facts in the data itself instead of asking the team.
- **Plain-writing rules** (`skills/aidlc-discovery/references/plain-writing.md`), applied to every reply and artifact: short chat, links instead of pasted artifacts, no emojis.
- Signals records the team's optional expectations before any analysis (`signals/team-expectations.md`, E1, E2), kept apart from the testable hypotheses it writes from the data (H1, H2).
- Setup asks which direction of the business metric is good, and scoring judges business outcome in that direction. Handoff confirms the build route before writing.
- **Data preparation tool** (`tools/prepare-data/`): a short Python script around Microsoft Presidio that removes personal data from exports offline, on the team's machine, with a report to review before sharing. `--synthetic N` writes invented rows in the shape of the scrubbed data, for rehearsals.
- Optional team Space support, so several people can follow Discovery and take it over.
- Two synthetic samples (AnyCompany Air, with telemetry, and AnyCompany Health), and facilitator material: answer keys, a run sheet, a dry run, and train-the-trainer.
- `scripts/build.py`, which bundles the skills into one installable AWS Quick skill with a module per job, and writes the release zip to `dist/`.
- One-button releases: **Actions**, **Release**, **Run workflow**, then patch, minor, or major. The version is worked out from the latest tag at release time (`scripts/bump_version.py`), and the release notes and this changelog's entry are generated from the merged pull requests. Steps in `CONTRIBUTING.md`.
- Unit tests for the skills, the bundle, the samples, and the data preparation tool, and an end-to-end test harness. The Presidio tests run in their own workflow, only when the tool changes.

### Removed

- **Breaking:** the Kiro and Claude Code bundles, the Node build (`build.js`), and the v1 rule set. The skill now targets AWS Quick Desktop only. Earlier releases remain available on the releases page.

### What's Changed
* V3 by @ConnorKirk in https://github.com/aws-samples/sample-aidlc-discovery/pull/1
* Remove reference to a workshop by @ConnorKirk in https://github.com/aws-samples/sample-aidlc-discovery/pull/3
* docs(readme): link the AI-DLC Discovery workshop by @hjgraca in https://github.com/aws-samples/sample-aidlc-discovery/pull/2
* Amazon Quick -> AWS Quick by @ConnorKirk in https://github.com/aws-samples/sample-aidlc-discovery/pull/4
* refactor(signals)!: rename team hypotheses to team expectations by @ConnorKirk in https://github.com/aws-samples/sample-aidlc-discovery/pull/5
* feat: ask in rounds, plain writing, optional expectations, data preparation tool by @hjgraca in https://github.com/aws-samples/sample-aidlc-discovery/pull/6

### New Contributors
* @ConnorKirk made their first contribution in https://github.com/aws-samples/sample-aidlc-discovery/pull/1
* @hjgraca made their first contribution in https://github.com/aws-samples/sample-aidlc-discovery/pull/2

**Full Changelog**: https://github.com/aws-samples/sample-aidlc-discovery/compare/v2.0.1...v3.0.0

---

## [2.0.1] — 2026-07-02 (pre-release)

Patch release. Fixes the AWS Quick installation.

### Fixed

- **AWS Quick install fix.** Some users installing from GitHub hit an "access to a private folder" error during AWS Quick setup. The skill now describes its bundled files (`aidlc-common/`, `skills/`, `aidlc-discovery-rules/`) **relative to its own folder**, matching how Quick resolves the install location. The install docs now use the supported desktop UI import flow (**Agents & skills → Skills → + Create → Import from file**), and the automated install prompt is pinned to `v2.0.1` so users pull the corrected assets.

---

## [2.0.0] — 2026-06-02 (skill-based multiplatform rewrite · pre-release)

v2 repackages aidlc-discovery as an **independent, skill-based, multiplatform** tool. The interview *method* (question banks, Quick/Full depth, visual sketch) is reused from v1; the *packaging and orchestration* are new. AI-DLC is a consumer of the output, not its container.

### Added

- **Skill-based architecture** (agentskills.io): a `discovery-orchestrator` (setup) plus `product-discovery`, `tech-discovery`, `open-questions`, and `visual-sketch` skills, with shared `aidlc-common/` (orchestrator protocol, conventions, deterministic `process-checker.js`).
- **Multiplatform via core + adapters + `build.js`** → `dist/<target>/`: `kiro` (IDE/CLI), `claude` (Claude Code **and** Claude Cowork desktop), `amazon-quick`. All are Tier 1.
- **Parallel roles**: PM ∥ tech lead in separate sessions, with **single-writer state per role** and a deterministic **join barrier** (`process-checker.js`) that consolidates open-questions and reconciles cross-role contradictions. Turns v1's `Both-Sequential` into `Both-Parallel` without races.
- **Two interaction modes**: `batch` (file `[Answer]:`) and `conversational` (question-by-question in chat).
- **Self-contained bundles**: `build.js` packages the v1 question banks into each target, so installs don't depend on fetching v1.

### Changed

- **Install model**: from "download release zip into `.aidlc/`" (v1) to "`node build.js` → copy `dist/<target>/` into the platform's install dir" (v2), plus an automated install prompt per platform.

### Removed

- **Language module**: v2 drops explicit language detection/handling — the agent uses the user's language, like AI-DLC. Control tokens and control files stay in English.

### Fixed

- **Batch information loss**: reinstated v1's split between an active-batch buffer (`*-questions.md`) and an **append-only `*-answers-history.md`**, which the initial v2 scaffolding had omitted.

---

## [0.2.2] — 2026-06-02

Patch release. Trims the published package so it ships only what the installed `.aidlc/aidlc-discovery/` needs.

### Changed

- **Release packaging trimmed.** The published zip (and therefore the installed `.aidlc/aidlc-discovery/` package) now ships only the runtime rules (`aidlc-discovery-rules/`), user-facing reference docs (`README.md`, `how-to-use.md`, `CHANGELOG.md`), `LICENSE`, `VERSION`, and `.source`. Repo-governance files (`install.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`) are no longer bundled — they are not needed inside the installed package. Updated the Manual install layout in `install.md` accordingly.

---

## [1.0.0] — 2026-06-02

First **stable** release. Promotes the 0.2.x line to a supported **1.0.0** major — same functionality, now versioned as v1.

### Changed

- The install prompt now pins to the **v1.0.0** release instead of `latest`, so v1 installations stay on the v1 line as later majors ship.

---

## [0.2.1] — 2026-05-15

Bugfix follow-up to v0.2.0. Improves the UX of the AI-DLC handoff prompt so users can copy and paste it cleanly without dragging the banner or stale conditional headers along.

### Fixed

- **Handoff prompt is now a separate, copy-clean code block.** Previously, the completion banner and the "paste this into a fresh context:" instruction lived inside the same code block as the prompt, forcing the user to hand-select the prompt portion. The agent now prints the banner and a one-line instruction OUTSIDE any code fence, then opens its own fenced code block for the prompt content with no leading indentation. Selecting the entire fenced block now copies exactly what AI-DLC needs.
- **Stale "OPTIONAL inputs (only if Visual Sketch was approved...)" header no longer appears** when the user skipped or discarded the Visual Sketch. The rule (`aidlc-discovery-rules/aidlc-discovery-core-workflow.md` §"Final Handoff") now uses an explicit `INCLUDE_OPTIONAL` boolean derived from the filesystem (checks `Product-Definition/visual/user-journey.md` AND `Product-Definition/visual/mockups/*.html` exist) and either includes the OPTIONAL block in full or omits it entirely. No orphan headers, no caveat text.
- **Handoff prompt body is now rendered in English even in non-English sessions.** AI-DLC interoperability requires English file paths and section names; only the instructional line ("Copy the block below and paste it...") localises.

### Changed

- The Final Handoff stage in `aidlc-discovery-core-workflow.md` is rewritten as a 6-step rendering procedure (Steps 4a–4f) instead of a single template-with-caveats block. Each step has a single responsibility (banner / instruction / open fence / required block / conditional optional / closing line / close fence) and the rule states the rendering rules explicitly so agents do not need to interpret embedded conditionals.
- `how-to-use.md` §"Final handoff" updated to match the new on-screen output, including a separate "what the user sees" block and "what the user copies" block.

---

## [0.2.0] — 2026-05-15

Second release. Adds an optional UI sketch stage, reorganises the output folder for clarity, and ships a self-describing handoff prompt for AI-DLC.

### Added

- **Optional Visual Sketch stage** (`aidlc-discovery-rules/aidlc-discovery-rule-details/shared/visual-sketch.md`) that runs after Open Questions Compilation and before the Final Handoff. Asks the user to opt in (default = skip), then a 5-question mini-interview (persona, depth, style, sample data, viewport), then delegates to the agent to generate a Mermaid `user-journey.md` and one self-contained HTML mockup per journey node under `Product-Definition/visual/mockups/`. Sidecar output — referenced from the AI-DLC handoff prompt but not required. Includes a strict validation pass (banner, primary-CTA-matches-edge, no fabricated features, self-contained HTML) and a three-option gate (Request Changes / Approve / Discard). Falls back to ASCII wireframes for agents without HTML write capability.
- **Self-describing AI-DLC handoff prompt** at the end of the session. The Final Handoff now prints a paste-ready block that tells AI-DLC every file path AND what each file is for (Vision, Technical Environment, open questions, plus the optional user-journey and mockups). The OPTIONAL section is omitted automatically when Visual Sketch was skipped or discarded. Replaces the previous one-line "point AI-DLC at Product-Definition/" text.
- **Responsible AI notice** in the README hero (GitHub `[!IMPORTANT]` callout) linking to the [AWS Responsible AI Policy](https://aws.amazon.com/ai/responsible-ai/policy/), aligned with the parent [aidlc-workflows](https://github.com/awslabs/aidlc-workflows) repository.

### Changed

- **`Product-Definition/` layout reorganised** for clarity. Root now contains exactly: two control files (`aidlc-discovery-state.md`, `audit.md`), three final outputs (`vision-document.md`, `technical-environment.md`, `open-questions.md`), and the optional `visual/` sidecar. All process artefacts (initial setup answers `role-selection.md` / `project-type.md`, per-batch question files, answer history for every role, and `interview/visual/` for the visual mini-interview) now live under `Product-Definition/interview/`. The Visual Sketch output (`visual/user-journey.md` + `visual/mockups/`) stays at root because the AI-DLC handoff prompt references it directly.

### Breaking

- The `Product-Definition/` layout change is **not auto-migrated**. v0.1.0 sessions continue to work but their file tree differs from the new layout. To adopt the new layout in an existing project, finish the in-flight session under v0.1.0 paths or move the relevant files into the new locations manually:
  - `Product-Definition/role-selection.md` → `Product-Definition/interview/role-selection.md`
  - `Product-Definition/project-type.md` → `Product-Definition/interview/project-type.md`
  - `Product-Definition/business/` → `Product-Definition/interview/business/`
  - `Product-Definition/technical/` → `Product-Definition/interview/technical/`
  - `Product-Definition/visual/visual-questions.md` and `visual-answers-history.md` → `Product-Definition/interview/visual/`
  - `Product-Definition/visual/user-journey.md` and `mockups/` stay at `Product-Definition/visual/`

---

## [0.1.0] — 2026-04-28

First working version. All core stages and both role interviews are complete.

### Added

#### Workflow structure

- Entry point `aidlc-discovery-rules/aidlc-discovery-core-workflow.md` with PRIORITY override directive.
- Seven workflow stages: Session Detection, Language Detection, Role Selection, Project Type Selection, Business Interview, Technical Interview, Open Questions Compilation, Final Handoff.
- Conditional branching per role (Business / Technical / Both-sequential).
- Per-question state tracking in `aidlc-discovery-state.md`; resume from any point.
- Append-only `audit.md` with ISO-8601 timestamps on every interaction.
- Batched writes (1 append to history + 1 state update + 1 audit entry per batch of 5–7 questions) to keep the loop snappy.
- Two-option completion gates at the end of each role (Request Changes / Approve and Continue), with back-propagation when answers are corrected.

#### User experience

- Plain-language project-type question ("Brand-new project" / "New feature on an existing product" / "Migration / modernisation") that maps internally to Greenfield / Brownfield / Hybrid without surfacing the jargon.
- Follow-up for existing-system projects asking how the agent should access source material.
- Depth selection at the start of each role: Quick pass (~10 min, core questions only) or Full interview (~25–35 min, every section).
- Progress header on every batch: section N of M, progress bar, answered/total, minutes remaining.
- Single-word trigger `ready` to advance; localised equivalents accepted (`listo`, `pronto`, `prêt`, `準備完了`, `好了`).
- Table questions include a pre-filled example row plus an empty slot to reduce ambiguity.
- Free-text questions render without fake multiple-choice wrappers.
- Example-code questions (T26–T29) support three valid answer paths: paste a snippet, point to a file, or skip with a documented quality trade-off.
- One-time "How to answer" block in the first batch of each role.

#### Language support

- Automatic detection of the user's language in four tiers: explicit instruction, steering files (`CLAUDE.md`, `.cursorrules`, `.kiro/steering/`, `AGENTS.md`), invocation-prompt inference, English default.
- One-time confirmation in the detected language before the interview starts.
- User-facing content (banners, questions, gate messages, `vision-document.md`, `technical-environment.md`, `open-questions.md`) rendered in the user's language.
- Control content (`aidlc-discovery-state.md`, `audit.md`, file names, internal identifiers, `[Answer]:` tag) stays in English for downstream AI-DLC interoperability.
- Mid-session language change supported; previously rendered content is preserved verbatim for audit integrity.
- Optional bilingual final render (`vision-document.en.md` alongside `vision-document.md`) for handoff to English-only teams.
- Right-to-left language support (Arabic, Hebrew); diacritics preserved in user answers.

#### Validation and safety

- Content-validation rules for markdown integrity, character escaping, answer validity, state-file integrity, audit-log append-only enforcement, and final-document completeness.
- Cross-question consistency checks (e.g. HIPAA compliance requires encryption at rest and in transit; flagged if T21 and T18 disagree).
- Ambiguity detection on user answers with follow-up questions appended to the same question file rather than modifying previous entries.
- Open-questions collector scans completed interviews for declared uncertainties and AI-flagged ambiguities, producing a monotonically numbered `open-questions.md` for AI-DLC handoff.

#### Install and packaging

- **One-prompt AI-assisted installer** ([install.md](install.md)) that downloads the latest release into `.aidlc/aidlc-discovery/` in the user's project, writes the correct rules / steering file for the detected IDE (Claude Code, Kiro, Cursor, Cline, Amazon Q, Antigravity, Copilot, generic `AGENTS.md`), and adds `.aidlc/` to `.gitignore`. Aligns with the AI-DLC official setup pattern.
- **Marker-based append for rules files** (`<!-- aidlc-discovery:begin -->` / `<!-- aidlc-discovery:end -->`). First-time install adds the block; subsequent updates replace only the marked block, preserving any other content in `CLAUDE.md`, `AGENTS.md`, etc.
- **GitHub release packaging workflow** (`.github/workflows/release.yml`) triggered on `v*.*.*` tags. Stages the shipped files, stamps `VERSION` and `.source` (repo / tag / commit / build time), verifies the CHANGELOG has a matching section, and publishes the zip as a release asset.
- **Natural-language invocation** after install (`start aidlc-discovery`, `inicia aidlc-discovery`, `prepare AI-DLC discovery`) in addition to the universal fallback (`Read .aidlc/aidlc-discovery/.../aidlc-discovery-core-workflow.md and execute`).

#### Documentation

- [README.md](README.md) with design principles, architecture, language-support policy, pre-loading-context pattern, and known limitations.
- [how-to-use.md](how-to-use.md) with a full end-to-end OrderFlow walkthrough and five side-flows: resuming, changing an answer, handing off to AI-DLC, using another language, pre-loading context from files or MCP.
- Inline prompt examples for pre-loading context from local files, Word documents, and MCP-connected sources (internal repos, wikis).
- README section [Install](README.md#install) with pointer to [install.md](install.md); `install.md` documents IDE-specific paths with experimental status flags.

### Known limitations

- **No multi-user identity or session locking.** Treat one `Product-Definition/` folder as one session; coordinate handoffs out of band (e.g. a shared git branch).
- **No rule-governed extraction with source citations.** Users can still ask their agent to read files, repos, or MCP endpoints before invoking the workflow (see [Pre-loading context from files or MCP](README.md#pre-loading-context-from-files-or-mcp)), but the structured `pre-filled-analysis.md`, automatic contradiction detection, and pre-ingestion secret scan are planned for a later release.
- **Depth Quick skips some sections entirely.** Upgrade Quick → Full mid-session to unlock the skipped sections while preserving existing answers.
- **Example-code questions rely on user-provided context.** For a brand-new project with no reference code, T26–T29 answers may be deferred with a documented quality trade-off.

### Internal

- 14 markdown rule files totalling ~2 900 lines under `aidlc-discovery-rules/`.
- Directory structure: `common/` (welcome, session-continuity, role-selection, question-format-guide, content-validation, audit-format, language-handling), `shared/` (project-type, open-questions-collector), `business/` (vision-interview, vision-completion), `technical/` (tech-env-interview, tech-env-completion).

---

[Unreleased]: #unreleased
[2.0.1]: #201--2026-07-02
[2.0.0]: #200--2026-06-02-skill-based-multiplatform-rewrite--pre-release
[0.2.2]: #022--2026-06-02
[1.0.0]: #100--2026-06-02
[0.2.1]: #021--2026-05-15
[0.2.0]: #020--2026-05-15
[0.1.0]: #010--2026-04-28
