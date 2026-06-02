# Changelog

All notable changes to `aidlc-discovery` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed

- **Release packaging trimmed.** The published zip (and therefore the installed `.aidlc/aidlc-discovery/` package) now ships only the runtime rules (`aidlc-discovery-rules/`), user-facing reference docs (`README.md`, `how-to-use.md`, `CHANGELOG.md`), `LICENSE`, `VERSION`, and `.source`. Repo-governance files (`install.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`) are no longer bundled — they are not needed inside the installed package. Updated the Manual install layout in `install.md` accordingly.

### Planned

- **First-class source ingestion (formal extraction mode)** — a rule-governed alternative to the prompt-based [pre-loading pattern](README.md#pre-loading-context-from-files-or-mcp). Will include:
  - Explicit `Source Ingestion` stage before depth selection in each role
  - `pre-filled-analysis.md` intermediate artefact with coverage report (covered / partially covered / not covered / contradictions)
  - Inline `**Source**:` attribution on every answer in `*-answers-history.md`
  - Pre-ingestion secret scanning to keep credentials out of `audit.md`
  - Automatic contradiction detection across multiple sources
  - Section-level bulk approval UX
- Multi-user identity and session locking so two people can work on the same `Product-Definition/` folder without trampling each other's state.
- Optional re-open of approved sections post-gate without manual state editing.
- End-to-end validation of the install flow in Kiro, Cursor, Cline, Amazon Q Developer, Antigravity, and Copilot — move each from "experimental" to "validated" in [install.md](install.md).

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
[0.2.1]: #021--2026-05-15
[0.2.0]: #020--2026-05-15
[0.1.0]: #010--2026-04-28
