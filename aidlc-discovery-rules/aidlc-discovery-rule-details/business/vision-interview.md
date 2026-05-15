# Business Role — Vision Document Interview

Structured interview that produces `Product-Definition/vision-document.md`. Based on the AI-DLC `docs/writing-inputs/vision-document-guide.md` structure.

---

## Step 0 — Depth selection (run ONCE at the start of the Business role)

Before writing any interview questions, ask the user how deep they want to go. Write this into `Product-Definition/interview/business/vision-questions.md`:

```markdown
# Business Interview — Depth Selection

Pick the interview depth. You can upgrade Quick → Full later if needed.

A) **Quick pass** (~8 questions, ~10 min)
   Core-only questions. Good for prototypes, POCs, internal tools, or when
   you already have most of the answers in your head.

B) **Full interview** (~18 questions, ~25 min)
   Covers every section of the Vision Document guide. Recommended for
   production-grade projects and cross-team initiatives.

X) Other (e.g. "Full but skip Risks section" — describe after [Answer]:)

[Answer]:

---

When you're done, reply with a single word: **ready**
```

When the user replies `ready`:

1. Re-read the file, validate the letter.
2. Record the chosen depth in `aidlc-discovery-state.md`:
   ```markdown
   ## Session Metadata
   - Business Depth: <Quick | Full | Custom:{description}>
   ```
3. Build the question set:
   - **Quick** → use only questions marked `[CORE]` in the banks below (8 questions total, 3 sections).
   - **Full** → use every question (18 for brand-new projects; 20 when there is an existing system).
   - **Custom** → interpret the user's free-text and confirm inclusion/exclusion before proceeding.

## How the interview is structured

For each section:

1. Select unanswered questions from the bank below (only those matching the chosen depth and project type).
2. Write a batch of 5–7 questions into `Product-Definition/interview/business/vision-questions.md` using the formats from `common/question-format-guide.md`.
3. Start every batch with the mandatory **progress header**:

   ```markdown
   # Business Interview — Section {N} of {Total}: {Section Title}

   Progress: {bar} {answered}/{total} questions  ·  ~{minutes_left} min remaining

   This batch covers Q{first}–Q{last}. Fill in the [Answer]: tags below,
   then reply with **"ready"** and I'll validate your answers and move on.
   ```

4. End every batch with the mandatory **footer**:

   ```markdown
   ---

   When you're done, reply with a single word: **ready**

   (I'll re-read this file from disk and validate your answers.)
   ```

5. Include the one-time "How to answer" block **only on the very first batch** so the user learns the pattern.
6. Wait for `ready`. Re-read. Validate per `common/content-validation.md`. Append the batch to `vision-answers-history.md`. Mark checkboxes in state. Log to audit. (All batch-scoped, not per-question — see `common/question-format-guide.md` §"Batched writes".)
7. Advance to the next section if all current-section questions are `[x]`.

**Branching** (AI-internal logic — the user never sees these terms):
- If `Project Type = Greenfield` (user picked A — brand-new), skip the "Existing System" questions at the end.
- If `Project Type = Brownfield` or `Hybrid` (user picked B, C, or qualifying X), include them.

## State registration

Before asking the first batch, populate `aidlc-discovery-state.md` under `## Business Questions` with every planned question (include or exclude per depth/project-type):

```markdown
## Business Questions

### Section 1: Executive Summary
- [ ] Q1 [CORE]: Project name and type
- [ ] Q2 [CORE]: Target users one-liner
- [ ] Q3 [CORE]: Core capability
- [ ] Q4 [CORE]: Business problem
- [ ] Q5 [CORE]: Measurable outcome

### Section 2: Business Context
- [ ] Q6: Problem statement in concrete terms
- [ ] Q7: Business drivers / why now
- [ ] Q8 [CORE]: Target users and stakeholders (table)
- [ ] Q9: Business constraints
- [ ] Q10 [CORE]: Success metrics (table)

### Section 3: Full Scope Vision
- [ ] Q11: Product vision statement (long-term aspirational)
- [ ] Q12: Feature areas (list with short descriptions)
- [ ] Q13: Future extensions considered but not committed

### Section 4: MVP Scope — IN
- [ ] Q14 [CORE]: MVP features (table: feature | rationale | user type)
- [ ] Q15: Non-functional priorities for MVP

### Section 5: MVP Scope — OUT
- [ ] Q16: Features deliberately excluded (table: feature | reason | target phase)

### Section 6: Risks and Open Questions
- [ ] Q17: Known risks (table)
- [ ] Q18: Pre-declared open questions / uncertainties

### Existing System — ask only if the user is building on or migrating an existing system (project type B or C)
- [ ] QB1 [CORE]: Current state — one paragraph describing what the system does today
- [ ] QB2 [CORE]: What must NOT change (existing components, APIs, data the new work must not touch)
```

**[CORE] marker** = included in Quick pass (8 questions for brand-new projects / 10 when there is an existing system). Full pass includes every question.

---

## Question Bank

> **Important**: when writing these into the user-facing `vision-questions.md`, ALWAYS wrap the rendered question inside the progress header and footer shown above. The raw question blocks below are templates — they are not what the user sees verbatim.

### Section 1: Executive Summary

#### Q1 [CORE] — Project name and type

```markdown
## Question 1: What is the project name and type?

Tell me the project's working name and pick the category that best fits.

A) A new internal tool / platform
B) A new customer-facing product
C) A significant addition to an existing product
D) A migration / modernisation effort
X) Other — describe

[Answer]:
```

#### Q2 [CORE] — Target users (one-liner)

```markdown
## Question 2: Who is the primary target user, in one sentence?

Keep it to a single sentence. We'll go into detail on user types in Q8.

Example: "Mid-size retail operations managers who track inventory across
multiple stores."

[Answer]:
```

#### Q3 [CORE] — Core capability

```markdown
## Question 3: What is the core capability this product provides?

Describe the single most important thing the product does, in one sentence.

Example: "Unifies inventory, orders, and supplier data in one dashboard
and pushes real-time alerts when stock falls below threshold."

[Answer]:
```

#### Q4 [CORE] — Business problem

```markdown
## Question 4: What business problem does this solve?

A) A tool-fragmentation / manual-process problem (people are stitching work together by hand)
B) A missing-capability problem (customers are asking for something we don't offer)
C) A compliance / regulatory problem (we must do this by a deadline)
D) A cost / efficiency problem (an existing process is too expensive or slow)
X) Other — describe

[Answer]:
```

#### Q5 [CORE] — Measurable outcome

```markdown
## Question 5: What is the single most important measurable outcome you want to achieve?

Express as a number and a direction.

Examples:
  • "30% reduction in order processing time"
  • "Eliminate manual inventory reconciliation entirely (0 hours/week)"
  • "Cut time-to-onboard from 5 days to 1 day"

[Answer]:
```

### Section 2: Business Context

#### Q6 — Problem statement in concrete terms

```markdown
## Question 6: Describe the problem in 1–2 paragraphs, concretely.

Avoid vague phrases like "improve efficiency". Name what hurts today and
who feels it. Pointing me to an existing document is fine too — paste a
file path or URL.

[Answer]:
```

#### Q7 — Business drivers

```markdown
## Question 7: Why is this being pursued NOW?

A) Market pressure / competitive move
B) Regulatory or compliance deadline
C) Internal efficiency / cost reduction
D) Customer demand or contractual obligation
X) Other — include any hard dates

[Answer]:
```

#### Q8 [CORE] — Target users and stakeholders (table)

```markdown
## Question 8: List each user type and their primary need.

Replace the example row below with your own. Add or remove rows as needed.
Put your final table under [Answer]:.

**Example (do not submit as your answer):**

| Role | Description | Primary Need |
|------|-------------|--------------|
| (e.g.) Store Manager | Oversees daily ops at one retail location | Real-time inventory visibility across her store and sister stores |

[Answer]:

| Role | Description | Primary Need |
|------|-------------|--------------|
|      |             |              |
```

#### Q9 — Business constraints

```markdown
## Question 9: What hard constraints apply?

Select all that apply. Append specifics (amount, date, regulation name) after the letter.

A) Budget cap
B) Delivery deadline
C) Regulatory / audit requirements
D) Organisational policies that limit choices
X) Other — describe

[Answer]:
```

#### Q10 [CORE] — Success metrics (table)

```markdown
## Question 10: Which metrics will confirm success?

One row per metric. Replace the example row with your own.

**Example (do not submit as your answer):**

| Metric | Current State | Target State | Measurement Method |
|--------|---------------|--------------|--------------------|
| (e.g.) Order processing time | 4h avg | 2.8h avg | Weekly report from OMS |

[Answer]:

| Metric | Current State | Target State | Measurement Method |
|--------|---------------|--------------|--------------------|
|        |               |              |                    |
```

### Section 3: Full Scope Vision

#### Q11 — Product vision statement

```markdown
## Question 11: What does the world look like when this product is fully realised?

A single-sentence aspirational statement. Not limited to the MVP.

Example: "Every retail operator across our 200+ franchises has the same
real-time view of their business that our flagship stores enjoy today."

[Answer]:
```

#### Q12 — Feature areas

```markdown
## Question 12: What are the major feature areas in the full-scope vision?

List each area and a one-line description. Order doesn't matter yet —
we'll prioritise in Section 4.

Example:
  - Inventory Tracking — real-time stock levels per SKU per location
  - Order Processing — intake, routing, fulfilment across warehouses
  - Supplier Portal — upstream ordering and invoice reconciliation

[Answer]:
```

#### Q13 — Future extensions considered but not committed

```markdown
## Question 13: Which capabilities have you thought about but explicitly decided NOT to commit to yet?

Naming these now prevents them from sneaking in later.

A) I'll write a bulleted list
B) None — the vision above is everything I've considered
X) Other

[Answer]:
```

### Section 4: MVP Scope — IN

#### Q14 [CORE] — MVP features

```markdown
## Question 14: Which features are IN scope for the MVP?

One row per feature. For "Rationale", say why this must be in the first release.

**Example (do not submit as your answer):**

| Feature | Rationale | Primary User Type |
|---------|-----------|-------------------|
| (e.g.) Real-time stock dashboard | Core differentiator; main value prop | Store Manager |

[Answer]:

| Feature | Rationale | Primary User Type |
|---------|-----------|-------------------|
|         |           |                   |
```

#### Q15 — Non-functional priorities for MVP

```markdown
## Question 15: What non-functional properties matter most for the MVP?

Select top 2–3. We'll translate to concrete NFRs in the Technical interview.

A) Latency / responsiveness
B) Scalability (expected concurrent users or request rate?)
C) Availability / uptime target
D) Security and data protection
E) Cost efficiency
X) Other

[Answer]:
```

### Section 5: MVP Scope — OUT

#### Q16 — Features deliberately excluded

```markdown
## Question 16: What is NOT in the MVP, and why?

Every row here is a scope-creep firewall. Include a target phase if deferred.

**Example (do not submit as your answer):**

| Excluded Feature | Reason | Target Phase |
|------------------|--------|--------------|
| (e.g.) Supplier portal | Focus MVP on internal ops first | Phase 2, post-pilot |

[Answer]:

| Excluded Feature | Reason | Target Phase |
|------------------|--------|--------------|
|                  |        |              |
```

### Section 6: Risks and Open Questions

#### Q17 — Known risks

```markdown
## Question 17: What are the known risks?

**Example (do not submit as your answer):**

| Risk | Impact (High/Med/Low) | Mitigation |
|------|-----------------------|------------|
| (e.g.) Legacy OMS API unreliable | High | Build an adapter with retry and circuit breaker |

[Answer]:

| Risk | Impact (High/Med/Low) | Mitigation |
|------|-----------------------|------------|
|      |                       |            |
```

#### Q18 — Open questions

```markdown
## Question 18: What is still uncertain?

These feed directly into AI-DLC as pre-declared ambiguities.

A) I'll write a bulleted list — one question per bullet
B) None — everything above is decided
X) Other

[Answer]:
```

### Existing System — ask only if the user is building on or migrating an existing system (project type B or C)

#### QB1 [CORE] — Current state

```markdown
## Question B1: Describe the current state in one paragraph.

What does the system do today? Who uses it? What are its major components?
Pointing to an existing architecture summary is fine.

[Answer]:
```

#### QB2 [CORE] — What must NOT change

```markdown
## Question B2: What must NOT change?

List existing components, APIs, schemas, or data that the new work must
leave untouched. This is a hard boundary for AI-DLC.

Example:
  - Payment service API (contract frozen for PCI audit)
  - Orders table schema (downstream reports depend on column order)
  - Customer-facing invoice PDF format

[Answer]:
```

## Validation guidance

When validating answers for this interview:

- **Q5** (measurable outcome): if no number and direction are present, ask a follow-up.
- **Q8** (target users table): reject empty "Primary Need" cells.
- **Q10** (success metrics table): reject rows with empty "Target State" or "Measurement Method" columns.
- **Q14** (MVP table): if more than ~12 features are listed, flag as "likely too large for an MVP — do you want to defer any?"
- **Q16** (excluded features): if the table is empty AND depth is Full, ask "Is there truly nothing you considered excluding? Leaving this blank invites scope creep."
- **Q18** and any X-tagged answers in other questions feed `shared/open-questions-collector.md`.

## When the section is complete

After all questions in a section are `[x]`:

1. Append a short "Section {N} Complete" marker to `vision-answers-history.md` with the timestamp.
2. Move to the next section — overwrite `vision-questions.md` with the next batch (header, questions, footer).
3. Log the section transition in `audit.md` with stage label `Business Interview — Section {N} Complete`.

When the last section is complete, hand off to `business/vision-completion.md`.
