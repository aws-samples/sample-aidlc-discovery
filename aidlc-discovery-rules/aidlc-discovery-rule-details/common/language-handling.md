# Language Handling

Defines which language the tool uses for user-facing content vs control content.

---

## Policy (the only rule that matters)

There are **two language zones**:

| Zone | What belongs here | Language |
|---|---|---|
| **User-facing** | Question files, answer history, welcome/resume banners, gate messages, the final `vision-document.md` and `technical-environment.md`, `role-selection.md`, `project-type.md`, `open-questions.md` | **User's language** |
| **Control** | `aidlc-discovery-state.md`, `audit.md`, file names, directory names, internal tags (`[Answer]:`, `[CORE]`, `ready`), section identifiers (`Q1`, `T14`, `QB2`, `OQ-B-1`) | **English (always)** |

Control content stays in English for three reasons: the AI-DLC ecosystem it hands off to expects English identifiers; the audit log needs to be machine-readable regardless of who operates the tool later; and the `[Answer]:` / `ready` triggers are parsed by string match.

## Detection (run ONCE, at the start of the first session)

Immediately after `welcome-message.md`, before `role-selection.md`, the tool must detect the user's language using this priority order:

1. **Explicit user instruction** — the user says "work in Spanish", "responde en español", "使用中文", etc. in the invocation or first turn.
2. **Steering files** — any of: `CLAUDE.md`, `.claude/CLAUDE.md`, `.cursorrules`, `.kiro/steering/`, `AGENTS.md` in the workspace root or parents. If these files are predominantly in a non-English language, adopt that language.
3. **User's recent prompt language** — if the user's invocation prompt itself is non-English ("Lee aidlc-discovery/... y ejecuta"), adopt that language.
4. **Default** — English.

Record the result in `aidlc-discovery-state.md`:

```markdown
## Session Metadata
- User Language: <BCP-47 tag: en | es | pt | fr | ja | zh-Hans | ...>
- Language Source: <explicit | steering:<file> | prompt-inference | default>
- Detected: <ISO8601>
```

Log the detection in `audit.md` with stage label `Language Detection`.

## Confirmation (one-time, only when detection is not "explicit")

If the detected language is NOT from explicit user instruction, confirm once in the user's inferred language. Example for Spanish:

```
He detectado que prefieres trabajar en español. Lo usaré para todas las
preguntas, los documentos finales y los mensajes. Los archivos de control
(aidlc-discovery-state.md y audit.md) se mantienen en inglés porque AI-DLC los
consume en ese idioma.

¿Confirmas? (sí / no / usa otro idioma)
```

Wait for confirmation. Record the confirmation in `audit.md`. If the user rejects, ask what language they prefer and restart detection.

If the user wants to change language mid-session, they can say so at any time; update the state field, log the change, and continue. Previously-generated user-facing content is NOT translated retroactively (to keep the audit trail intact) — only new content switches.

## What to translate

Once the language is set, every **user-facing string** the tool writes is in that language:

- ✅ Welcome banner
- ✅ Resume summary
- ✅ Role-selection question & options
- ✅ Project-type question & options ("Brand-new project", "New feature on an existing product", "Migration / modernisation")
- ✅ Depth-selection question & options
- ✅ All interview questions (Q1–Q18, T1–T29, QB1–QB2, TB1–TB4) including their context sentences, examples, and option labels
- ✅ Progress headers ("Progress: 10/20 questions · ~8 min remaining" → "Progreso: 10/20 preguntas · ~8 min restantes")
- ✅ Footers and the `ready` reminder text (the trigger word itself stays `ready` in English — see "Control content" below)
- ✅ Completion gate messages
- ✅ Final rendered `vision-document.md` and `technical-environment.md`
- ✅ `open-questions.md` descriptions
- ✅ Validation-error messages and ambiguity follow-ups

## What to NEVER translate

These are **control strings**. Translate them and the tool breaks.

- ❌ File names (`aidlc-discovery-state.md`, `vision-document.md`, etc.)
- ❌ Directory names (`Product-Definition/`, `interview/`, `business/`, `technical/`, `visual/`)
- ❌ The `[Answer]:` tag (parsed by string match)
- ❌ The `[CORE]` marker in state
- ❌ Question identifiers: `Q1`, `Q2`, `T14`, `QB2`, `TB3`, `OQ-B-1`, `OQ-T-2`
- ❌ Section identifiers: `Section 1`, `Section T5` (keep numeric/alpha codes in English)
- ❌ Stage labels in `audit.md`: `Business Interview — Batch Q1–Q5 validated`
- ❌ Metadata keys in `aidlc-discovery-state.md`: `Session Metadata`, `Role Progress`, `Current Role`, etc.
- ❌ Status symbols: `✅`, `⏳`, `⚪`, `[x]`, `[ ]`
- ❌ Internal enum values: `Greenfield`, `Brownfield`, `Hybrid` (the *user-facing* classification is translated — see below — but the internal mapping stays in English)
- ❌ The trigger word `ready` that the user types

### Special case — the trigger word

The canonical trigger in the footer is `ready`. In non-English sessions, ALSO accept the local equivalent (case-insensitive):

| Language | Local trigger (accepted) | Canonical (printed) |
|---|---|---|
| English | `ready`, `done`, `go` | `ready` |
| Spanish | `listo`, `listos`, `ya` | `listo` |
| Portuguese | `pronto` | `pronto` |
| French | `prêt`, `pret` | `prêt` |
| German | `fertig` | `fertig` |
| Japanese | `準備完了`, `ok` | `準備完了` |
| Chinese (Simplified) | `好了`, `完成` | `好了` |

The footer prints the canonical local trigger. Detection still also matches `ready` in any language (as a safety net).

### Special case — user-facing classification labels

When the user picks their project type in `project-type.md`, the tool asks:

- **English**: "Brand-new project" / "New feature on an existing product" / "Migration / modernisation"
- **Spanish**: "Proyecto nuevo" / "Nueva funcionalidad sobre un producto existente" / "Migración / modernización"

These LABELS the user sees are translated. The internal mapping stored in state still uses the English enum values (`Greenfield` / `Brownfield` / `Hybrid`) so downstream branching logic and AI-DLC interop remain unchanged.

## Glossary handling

If the user asks what "greenfield" or "brownfield" means (because they saw those words in AI-DLC docs elsewhere), explain in their language using the glossary in `shared/greenfield-vs-brownfield.md`.

## Final documents — what language they end up in

| Output file | Language |
|---|---|
| `vision-document.md` | User's language |
| `technical-environment.md` | User's language |
| `open-questions.md` | User's language (but `OQ-B-N` / `OQ-T-N` identifiers stay in English) |

**Note on handoff to AI-DLC**: AI-DLC itself is typically driven in English. When the user hands off these documents, their AI-DLC runner will read them in the user's language; AI-DLC's own tooling handles multi-language input. If the user explicitly wants the final documents ALSO in English (for handoff to an English-only team), offer that as a one-time re-render after the final gate:

```
¿Quieres también una versión en inglés de los documentos finales para
entregar a un equipo que no habla español? (sí / no)
```

If yes, render `vision-document.en.md` and `technical-environment.en.md` alongside the originals. State metadata records both were produced.

## Validation

Content-validation rules (`common/content-validation.md`) apply the same way regardless of language. The validator checks:

- All required sections present (use the English section key from the template, even if the visible heading is translated).
- Tables have all required columns filled.
- Answers are non-empty and parseable.

Language-specific gotchas:

- **Right-to-left languages** (Arabic, Hebrew): preserve RTL in the file; do not reverse tables or code fences.
- **Wide-character languages** (Chinese, Japanese, Korean): the progress bar `████░░░░░░` still uses ASCII box chars — don't substitute local variants.
- **Diacritics**: never strip them from user answers ("café" stays "café", not "cafe") when appending to history.

## Audit entries

Add a new entry type to `common/audit-format.md`:

| Event | Stage label |
|---|---|
| Initial language detection | `Language Detection` |
| User confirms detected language | `Language Confirmed` |
| User changes language mid-session | `Language Changed` |
| Bilingual final render requested | `Final Render — Bilingual` |
