# Technical Role — Technical Environment Document Interview

Structured interview that produces `Product-Definition/technical-environment.md`. Based on the AI-DLC `docs/writing-inputs/technical-environment-guide.md` structure.

---

## Context loading

Before the first question, load for context (do NOT modify):

- `Product-Definition/vision-document.md` if it exists (from the Business role)
- `Product-Definition/interview/project-type.md`
- `Product-Definition/interview/role-selection.md`

If the Vision Document exists, use it to pre-fill educated defaults in questions (e.g. suggest a deployment model aligned with the MVP's NFR priorities). Always present the user with full options anyway — the Technical role may override Business-driven assumptions.

## Step 0 — Depth selection (run ONCE at the start of the Technical role)

Write this into `Product-Definition/interview/technical/tech-env-questions.md`:

```markdown
# Technical Interview — Depth Selection

Pick the interview depth. You can upgrade Quick → Full later if needed.

A) **Quick pass** (~10 questions, ~12 min)
   Core-only questions. Good for prototypes, POCs, internal tools, or
   brand-new projects without strict compliance needs.

B) **Full interview** (~29 questions, ~35 min)
   Covers every section of the Technical Environment guide, including
   security, testing, and example code patterns. Recommended for
   production-grade projects, regulated workloads, and codebases where
   convention matters.

X) Other (e.g. "Full but skip Example Code" — describe after [Answer]:)

[Answer]:

---

When you're done, reply with a single word: **ready**
```

When the user replies `ready`:

1. Re-read, validate the letter.
2. Record the chosen depth:
   ```markdown
   ## Session Metadata
   - Technical Depth: <Quick | Full | Custom:{description}>
   ```
3. Build the question set:
   - **Quick** → only `[CORE]` questions (10 for brand-new projects / 13 when there is an existing system).
   - **Full** → every question.
   - **Custom** → interpret and confirm before proceeding.

## How the interview is structured

Same as the Business interview:

1. Select unanswered questions from the bank matching depth and project type.
2. Write 5–7 questions per batch into `Product-Definition/interview/technical/tech-env-questions.md`.
3. Start every batch with the mandatory **progress header** and end with the mandatory **footer**:

   ```markdown
   # Technical Interview — Section {N} of {Total}: {Section Title}

   Progress: {bar} {answered}/{total} questions  ·  ~{minutes_left} min remaining

   This batch covers Q{first}–Q{last}. Fill in the [Answer]: tags below,
   then reply with **"ready"** and I'll validate your answers and move on.

   ... questions ...

   ---

   When you're done, reply with a single word: **ready**
   ```

4. Include the one-time "How to answer" block only on the very first batch.
5. Wait for `ready`. Re-read. Validate. Append the batch to `tech-env-answers-history.md`. Mark checkboxes. Log to audit. (Batch-scoped — see `common/question-format-guide.md` §"Batched writes".)

**Branching** (AI-internal logic — the user never sees these terms):
- If `Project Type = Greenfield` (user picked A — brand-new), skip the "Existing System" questions.
- If `Project Type = Brownfield` or `Hybrid` (user picked B, C, or qualifying X), include them.

## State registration

Populate `aidlc-discovery-state.md` under `## Technical Questions`:

```markdown
## Technical Questions

### Section T1: Project Technical Summary
- [ ] T1 [CORE]: Runtime environment (cloud / on-prem / hybrid)
- [ ] T2 [CORE]: Cloud provider
- [ ] T3 [CORE]: Deployment model
- [ ] T4: Team size and experience

### Section T2: Programming Languages
- [ ] T5 [CORE]: Required languages (with versions)
- [ ] T6: Permitted languages
- [ ] T7 [CORE]: Prohibited languages (with reasons)

### Section T3: Frameworks and Libraries
- [ ] T8 [CORE]: Required frameworks
- [ ] T9: Preferred frameworks
- [ ] T10 [CORE]: Prohibited libraries (reason + alternative)

### Section T4: Cloud Services
- [ ] T11: Allow-list services
- [ ] T12: Disallow-list services

### Section T5: Architecture and Patterns
- [ ] T13 [CORE]: API style
- [ ] T14 [CORE]: Data patterns
- [ ] T15: Messaging / integration patterns
- [ ] T16: Project structure conventions

### Section T6: Security
- [ ] T17 [CORE]: Authentication method
- [ ] T18: Encryption at rest and in transit
- [ ] T19: Input validation approach
- [ ] T20 [CORE]: Secrets management
- [ ] T21: Compliance framework chosen

### Section T7: Testing
- [ ] T22 [CORE]: Test types required
- [ ] T23: Coverage targets
- [ ] T24: Tooling per test type
- [ ] T25: CI/CD gates

### Section T8: Example Code Patterns
- [ ] T26: Example endpoint pattern
- [ ] T27: Example function / module pattern
- [ ] T28: Example test pattern
- [ ] T29: Example infrastructure snippet

### Existing System — ask only if the user is building on or migrating an existing system (project type B or C)
- [ ] TB1 [CORE]: Existing stack inventory
- [ ] TB2 [CORE]: What must stay unchanged
- [ ] TB3 [CORE]: Prohibited patterns
- [ ] TB4: Source of example code
```

---

## Question Bank

### Section T1: Project Technical Summary

#### T1 [CORE] — Runtime environment

```markdown
## Question T1: What runtime environment will host this system?

A) Cloud only
B) On-premises only
C) Hybrid (cloud + on-prem)
X) Other

[Answer]:
```

#### T2 [CORE] — Cloud provider

```markdown
## Question T2: Which cloud provider will you use?

A) AWS
B) Azure
C) GCP
D) Multi-cloud (specify which under X)
E) Not applicable — on-premises only
X) Other

[Answer]:
```

#### T3 [CORE] — Deployment model

```markdown
## Question T3: What is the target deployment model?

A) Serverless (Lambda, Functions, Cloud Run, etc.)
B) Containers (ECS, EKS, AKS, GKE, Kubernetes, ...)
C) VMs / EC2-style
D) Hybrid across the above
X) Other

[Answer]:
```

#### T4 — Team size and experience

```markdown
## Question T4: Describe the team that will build and own this.

We'll use this to tune recommendations (e.g. a 2-person team shouldn't
adopt Kubernetes unless there's experience).

Example: "3 engineers. Strong in TypeScript/Node and AWS. No prior
Kubernetes experience. One engineer has deep Python/Pandas expertise."

[Answer]:
```

### Section T2: Programming Languages

#### T5 [CORE] — Required languages

```markdown
## Question T5: Which languages MUST be used, for which purpose?

Replace the example row below with your own data.

**Example (do not submit as your answer):**

| Language | Version | Purpose | Rationale |
|----------|---------|---------|-----------|
| (e.g.) TypeScript | 5.x | Backend services, CDK infra | Team expertise, type safety |

[Answer]:

| Language | Version | Purpose | Rationale |
|----------|---------|---------|-----------|
|          |         |         |           |
```

#### T6 — Permitted languages

```markdown
## Question T6: Which languages are permitted (allowed if justified)?

**Example (do not submit as your answer):**

| Language | Conditions for Use |
|----------|--------------------|
| (e.g.) Go | Approved for high-throughput microservices where latency is critical |

A) Fill the table under [Answer]:
B) None — only the required languages are allowed
X) Other

[Answer]:

| Language | Conditions for Use |
|----------|--------------------|
|          |                    |
```

#### T7 [CORE] — Prohibited languages

```markdown
## Question T7: Which languages are prohibited, and why?

**Example (do not submit as your answer):**

| Language | Reason |
|----------|--------|
| (e.g.) PHP | No team expertise; not aligned with platform direction |

A) Fill the table under [Answer]:
B) None — no language is explicitly prohibited
X) Other

[Answer]:

| Language | Reason |
|----------|--------|
|          |        |
```

### Section T3: Frameworks and Libraries

#### T8 [CORE] — Required frameworks

```markdown
## Question T8: Which frameworks MUST be used, for which domain?

**Example (do not submit as your answer):**

| Framework | Domain | Rationale |
|-----------|--------|-----------|
| (e.g.) NestJS | Backend web | Consistent with existing services, DI built-in |

[Answer]:

| Framework | Domain | Rationale |
|-----------|--------|-----------|
|           |        |           |
```

#### T9 — Preferred frameworks

```markdown
## Question T9: Which frameworks are preferred (not required)?

[Answer]:

| Framework | Conditions for Use |
|-----------|--------------------|
|           |                    |
```

#### T10 [CORE] — Prohibited libraries (with alternatives)

```markdown
## Question T10: Which libraries are prohibited? Include the reason AND the recommended alternative.

The reason + alternative columns matter more than a plain "do not use" list.
Without them, AI-DLC will honour the prohibition but may pick a poor substitute.

**Example (do not submit as your answer):**

| Prohibited | Reason | Use Instead |
|------------|--------|-------------|
| (e.g.) axios | Bundle size / security history | native fetch + abort-controller wrapper |

[Answer]:

| Prohibited | Reason | Use Instead |
|------------|--------|-------------|
|            |        |             |
```

### Section T4: Cloud Services

#### T11 — Allow-list

```markdown
## Question T11: Which cloud services are allowed, with any constraints?

A) Fill the table under [Answer]:
B) Not applicable — on-premises only
X) Other

[Answer]:

| Service | Constraints / Notes |
|---------|---------------------|
|         |                     |
```

#### T12 — Disallow-list

```markdown
## Question T12: Which cloud services are disallowed, and why?

A) Fill the table under [Answer]:
B) None
X) Other

[Answer]:

| Service | Reason |
|---------|--------|
|         |        |
```

### Section T5: Architecture and Patterns

#### T13 [CORE] — API style

```markdown
## Question T13: What API style(s) will the system expose?

A) REST (OpenAPI-described)
B) GraphQL
C) gRPC
D) Event-driven (pub/sub, Kafka, EventBridge, ...)
E) Mix — describe under X
X) Other

[Answer]:
```

#### T14 [CORE] — Data patterns

```markdown
## Question T14: What data patterns does the system need?

Select all that apply (combine letters, e.g. `A and E`).

A) Relational / SQL
B) Document / NoSQL
C) Key-value
D) Search index (e.g. OpenSearch)
E) In-memory cache (e.g. Redis / ElastiCache)
F) Event log / streaming
X) Other

[Answer]:
```

#### T15 — Messaging / integration patterns

```markdown
## Question T15: How will services communicate?

A) Synchronous request/response only
B) Async messaging via queue
C) Async messaging via pub/sub
D) Mix (describe which edges use which style under X)
X) Other

[Answer]:
```

#### T16 — Project structure conventions

```markdown
## Question T16: What structural conventions should code follow?

A) Monorepo
B) Multi-repo (one repo per service)
C) Specific layering convention — describe (e.g. "controller / service / repository")
X) Other

[Answer]:
```

### Section T6: Security

#### T17 [CORE] — Authentication method

```markdown
## Question T17: How will users and services authenticate?

A) OAuth2 / OIDC with an external IdP (name it under X if relevant)
B) JWT issued by our own auth service
C) Mutual TLS between services
D) IAM-based authentication (AWS SigV4)
E) Mixed — describe under X
X) Other

[Answer]:
```

#### T18 — Encryption

```markdown
## Question T18: Encryption requirements?

A) Everything encrypted at rest AND in transit (recommended default)
B) In transit only (unusual — justify under X)
C) At rest only (unusual — justify under X)
X) Other

[Answer]:
```

#### T19 — Input validation

```markdown
## Question T19: What is the input validation approach?

A) Schema validation at the API boundary (e.g. Zod, Pydantic, JSON Schema)
B) Validation in the application layer per endpoint
C) Both
X) Other

[Answer]:
```

#### T20 [CORE] — Secrets management

```markdown
## Question T20: How are secrets stored and accessed?

A) AWS Secrets Manager / Parameter Store
B) HashiCorp Vault
C) Environment variables injected by the deployment system
D) Cloud-native secret store for chosen provider
X) Other — describe (we do NOT accept "secrets committed to git" as a valid answer)

[Answer]:
```

#### T21 — Compliance framework

```markdown
## Question T21: Which compliance framework applies?

A) SOC 2
B) ISO 27001
C) HIPAA
D) PCI-DSS
E) None — internal tool with no regulated data
X) Other (include multiple if they stack — e.g. "SOC 2 + HIPAA")

[Answer]:
```

### Section T7: Testing

#### T22 [CORE] — Test types

```markdown
## Question T22: Which test types are required?

Combine letters as needed (e.g. `A, B, F`).

A) Unit
B) Integration
C) Contract (consumer-driven, e.g. Pact)
D) End-to-end
E) Performance / load
F) Security (SAST / DAST)
X) Other

[Answer]:
```

#### T23 — Coverage targets

```markdown
## Question T23: What are your coverage targets?

A) ≥80% on internal code paths (third-party excluded)
B) ≥70% overall
C) 100% on a defined "critical path" only
D) No numeric target — review-based
X) Other

[Answer]:
```

#### T24 — Tooling per test type

```markdown
## Question T24: Which tool is used for each required test type?

**Example (do not submit as your answer):**

| Test Type | Tool |
|-----------|------|
| (e.g.) Unit | Jest |
| (e.g.) Integration | Testcontainers + Jest |

[Answer]:

| Test Type | Tool |
|-----------|------|
|           |      |
```

#### T25 — CI/CD gates

```markdown
## Question T25: What CI/CD gates must pass before a change can merge / deploy?

A) Unit tests pass
B) Integration tests pass
C) Security scans pass
D) Code review approved
E) All of the above
X) Other (describe)

[Answer]:
```

### Section T8: Example Code Patterns

> **Important**: these patterns are the single highest-leverage input to AI-DLC code generation. Each question supports **three valid ways to answer** — don't skip if you don't have a polished snippet handy.

#### T26 — Example endpoint pattern

```markdown
## Question T26: Example endpoint pattern

There are three valid ways to answer:

A) Paste a canonical snippet below inside a code fence
B) Point me to a file path I can read (e.g. "see src/routes/users.py in this repo")
C) Skip — we'll infer from framework conventions (AI-DLC code quality drops
   roughly 20% without at least one concrete example; we'll flag this as an
   open question for later)
X) Other

[Answer]:

<!-- If A, paste code here:
```{language}
// your snippet
```
-->
```

#### T27 — Example function / module pattern

```markdown
## Question T27: Example function / module pattern

Illustrate typical error handling, logging, and dependency-injection conventions.

A) Paste a canonical snippet below
B) Point me to a file path
C) Skip — use framework defaults
X) Other

[Answer]:
```

#### T28 — Example test pattern

```markdown
## Question T28: Example test pattern

Include setup/teardown conventions if relevant.

A) Paste a canonical snippet below
B) Point me to a file path
C) Skip — use framework defaults
X) Other

[Answer]:
```

#### T29 — Example infrastructure snippet

```markdown
## Question T29: Example infrastructure-as-code snippet

(CDK / Terraform / CloudFormation / other)

A) Paste a snippet below
B) Point me to a file path
C) Not applicable — no IaC in scope
X) Other

[Answer]:
```

### Existing System — ask only if the user is building on or migrating an existing system (project type B or C)

#### TB1 [CORE] — Existing stack inventory

```markdown
## Question TB1: What's in the existing stack today?

**Example (do not submit as your answer):**

| Language / Framework | Current Usage | Direction |
|----------------------|---------------|-----------|
| (e.g.) Java 11 | Core backend services | Upgrade to Java 21 in Phase 2 |
| (e.g.) JavaScript | Legacy frontend | Migrate to TypeScript |

"Direction" examples: Maintain | Upgrade to X | Migrate away | Deprecate.

[Answer]:

| Language / Framework | Current Usage | Direction |
|----------------------|---------------|-----------|
|                      |               |           |
```

#### TB2 [CORE] — What must stay unchanged

```markdown
## Question TB2: Which services, schemas, contracts, or configs must NOT be touched?

Example:
  - Payments service API (frozen for PCI audit until Q3)
  - `users` table schema (downstream ETL depends on column order)
  - Existing SSO callback URLs

[Answer]:
```

#### TB3 [CORE] — Prohibited patterns

```markdown
## Question TB3: Which libraries or patterns conflict with your existing codebase?

E.g. "don't introduce a second ORM", "don't mix async/await in this Django app", etc.

A) I'll write a bulleted list
B) None beyond the language/library prohibitions already listed in T7/T10
X) Other

[Answer]:
```

#### TB4 — Source of example code

```markdown
## Question TB4: For the Example Code Patterns section, where do examples come from?

A) I'll point to real files in the repository (AI-DLC should load them)
B) I'll paste snippets pulled directly from existing files
C) Mix
X) Other

[Answer]:
```

## Validation guidance

- **T7, T10, T12** (prohibited lists): warn the user if all three are empty — *"No prohibitions usually means AI-DLC will reach for its defaults, which may not match your house style. Is that intentional?"*
- **T10**: every row MUST have both a reason and a recommended alternative. Flag missing alternatives.
- **T21** (compliance): if a compliance framework is selected, add a reminder to the open-questions collector to ensure T17–T20 align with that framework.
- **T26–T29** (example code): if ALL four are answered C) Skip, flag the risk — AI-DLC code quality drops significantly. Offer a one-shot follow-up: *"Can you point me to just one existing service whose patterns should guide new code?"*
- **T18 + T21 cross-check**: if `T21 = HIPAA` but `T18 != A (everything at rest and in transit)`, flag as a contradiction and ask to resolve before rendering.

## When the section is complete

Same pattern as Business: append a "Section {N} Complete" marker to `tech-env-answers-history.md`, overwrite the next batch into `tech-env-questions.md`, log in `audit.md` with stage label `Technical Interview — Section {N} Complete`.

When the last section is complete, hand off to `technical/tech-env-completion.md`.
