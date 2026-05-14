# Content Validation

Every file this workflow creates under `Product-Definition/` MUST pass these checks before it is written.

---

## Checks

### 1. Markdown integrity

- Headings are hierarchical (no jumps from `#` to `###`).
- Tables are well-formed: same number of columns per row, pipes balanced, header separator row present.
- Code fences are properly opened and closed with matching language tags.
- Links and references resolve — no dangling `[…](…)` with empty targets.

### 2. Character escaping

- Escape any unintended markdown formatting in user-provided text (e.g. a raw `*` inside a table cell).
- Preserve user content verbatim where possible; prefer escaping over silent edits.
- Use fenced code blocks for multi-line user text that could contain markdown syntax.

### 3. Diagrams and visuals

- ASCII diagrams: align with monospace grid; avoid tab characters; document each symbol in a legend.
- Mermaid (if ever used): validate the syntax mentally before writing; if unsure, omit the diagram and provide a short prose description instead.
- Always include a text alternative next to any diagram so the file is readable without rendering.

### 4. Answer validity

Before appending an answer into `*-answers-history.md`:

- The `[Answer]:` tag must be non-empty.
- The answer must start with a letter listed in the question, or with `X` followed by free text.
- Caveats must be preserved verbatim.
- If an answer is ambiguous, do NOT append it — ask a clarifying follow-up question instead.

### 5. State file integrity

- Before writing `aidlc-discovery-state.md`, always `Read` the current version and apply a minimal diff.
- Never remove per-question entries unless the user explicitly asks.
- The `Last Updated` metadata field must reflect the current ISO8601 timestamp.

### 6. Audit log integrity

- `audit.md` is **append-only**.
- Every write must use Read + Edit (append), never Write (overwrite).
- Entries follow `common/audit-format.md` exactly.

### 7. Output documents (vision-document.md, technical-environment.md)

When rendering the final outputs from the answer history:

- All sections from the corresponding guide template MUST be present (even if marked "Not applicable" with a short rationale).
- Tables MUST match the column headers specified in the guide.
- Code examples included in the Technical Environment document MUST be syntactically correct for the declared language.
- If the user marked a question X with free text, translate the intent into the document prose — don't leave raw `[Answer]:` tags in the final doc.

## Error handling

If a validation check fails:

1. **Do not write** the file.
2. Explain to the user which check failed, quoting the problematic content.
3. Offer a suggested fix and wait for the user's go-ahead.
4. Log the validation failure in `audit.md`.
