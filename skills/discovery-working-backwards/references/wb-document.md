# The five Working Backwards questions

A structured dialog with the team, one question per round, for the selected use case. It ends with a Working Backwards document that grounds the PR/FAQ. The team answers; you suggest from the signals and personas, and structure what the team says.

## The 5 Working Backwards Questions

Ask one question per round. Each bullet under a question is one question in that round, with a recommended answer drafted from the Signal Analysis Report and the personas (see "Asking the team" in the entry skill). The quoted text shows what each round covers, not the wording to paste.

### Question 1. LISTEN: Who is the customer and what insights do we have?

```
"Let's start with the customer.
 - Who are the primary customers?
 - What key insights do we have about them?
 - What are their biggest pain points?

 (I can make suggestions based on the Signal Summary.)"
```

**Expected Output:**
- Primary customer groups
- Key Customer Insights (from VoC data)
- Pain Points with evidence

---

### Question 2. DEFINE: What is the customer problem / the opportunity?

```
"Based on the insights: What is the core problem?
 - What is the Customer Problem / the Opportunity?
 - How big is the impact?
 - What happens if we do nothing?"
```

**Expected Output:** (apply `framing-rules.md`)
- The end customer, named
- Core problem
- Root causes: structural, why not what
- Impact on the customer and impact on the business, separately
- Constraints
- The Today statement, the How Might We question, and the North Star

---

### Question 3. INVENT: What solutions address the customer need?

```
"Now it gets creative. What solutions could address the problem?
 - What are possible solution approaches?
 - What core capabilities do we need?
 - What is the differential advantage?

 (I can make suggestions based on the Signals.)"
```

**Expected Output:**
- Solution Overview
- Core Capabilities (3-5)
- Differentiator
- Build vs. Buy vs. Partner

---

### Question 4. REFINE: What does the end-to-end customer experience look like?

```
"How would the customer experience the solution?
 - What is the customer journey (step by step)?
 - What is the 'Day 1' vs. 'Ongoing' experience?
 - What metrics define success?"
```

**Expected Output:**
- Customer Journey (Steps)
- Day 1 Experience (Onboarding)
- Ongoing Usage
- Success Metrics

---

### Question 5. TEST & ITERATE: How do we measure customer success?

```
"Finally: How do we validate and measure?
 - What are the key success metrics?
 - How do we test our assumptions?
 - What is the iteration plan?"
```

**Expected Output:**
- Success Metrics (quantified)
- Test/Validation Approach
- Iteration Cadence
- Risks + Mitigations

---

## Dialog Guidance

1. **One question per round.** Not all five at once: each builds on the one before.
2. **Recommend every part.** Draft the answer from the signals and personas, worded so "yes" accepts it.
3. **Facts are yours.** Look up counts, field values, or causes in the data before the round; ask the team only for what the data cannot show.
4. **Summarize briefly.** After each answer, at most three lines, then the next round. Do not ask "Continue?"
5. **Flag what does not add up.** If a target cannot be reached with the chosen scope, say so in one line as a question in the next round.
6. **Consolidate at the end.** All five answers into the WB Document.

## Output: Working Backwards Document

At the end of the dialog you create this document:

```markdown
# Working Backwards: [Product/Feature Name]
**Created:** [Date]
**Customer:** [Customer]

## 1. LISTEN: Who is the customer?

### Primary Customers
- [Customer 1]
- [Customer 2]

### Key Customer Insights
1. [Insight + Evidence]
2. ...

### Pain Points
- [Pain Point 1] (severity: high)
- [Pain Point 2] (severity: ...)

---

## 2. DEFINE: The Customer Problem

### Core Problem
[Clear problem definition in 1-2 sentences]

### End customer
[The person whose day changes when this ships]

### Root Causes (why, not what)
1. ...
2. ...

### Impact on the customer
- ...

### Impact on the business
- ...

### Today statement
Today, [persona] have to [problem] when [context]. They need a way to [outcome].

### How Might We
How might we [outcome] for [persona] so that [benefit]?

### North Star
Deploy [capability] by [when] to [metric 1] and [metric 2], in order to [ultimate goal].

---

## 3. INVENT: Solution Approaches

### Solution: "[Name]"
[Description in 2-3 sentences]

### Core Capabilities
1. [Capability 1]: [Description]
2. [Capability 2]: ...
3. ...

### Differentiation
[What makes us different/better?]

---

## 4. REFINE: Customer Experience

### Customer Journey
1. [Step 1: ...]
2. [Step 2: ...]
3. ...

### Day 1 Experience
[How does the customer experience the solution for the first time?]

### Ongoing Usage
[What does regular usage look like?]

---

## 5. TEST & ITERATE: Measuring Success

### Success Metrics
| Metric | Target | Timeframe |
|--------|--------|-----------|
| ... | ... | ... |

### Validation Approach
- [How do we test?]

### Iteration Plan
- Month 1: ...
- Quarter 1: ...
- Year 1: ...

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| ... | ... | ... | ... |
```

## Storage Location

`discovery/[project]/working-backwards/working-backwards.md`
