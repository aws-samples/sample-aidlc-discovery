# PR/FAQ Generation Prompt Chain

## Purpose
Generate Amazon Working Backwards PR/FAQ documents using a 4-step LLM chain grounded in customer data and personas.

> **Upstream:** ported from the [voc-datalake platform](https://github.com/aws-samples/sample-voice-of-customer-datalake)'s
> [`lambda/api/prompts/prfaq-generation.json`](https://github.com/aws-samples/sample-voice-of-customer-datalake/blob/main/voc-datalake/lambda/api/prompts/prfaq-generation.json).
> Treat that JSON as the source of truth if the two drift.

---

## Step 1: Customer Thinking

### System Prompt
```
You are thinking deeply about customers and their needs.
Channel the voice of real customers based on the feedback data.
```

### User Prompt Template
```
Think deeply about what customers really want and need.

FEATURE IDEA: {feature_idea}

USER PERSONAS:
{personas_context}

CUSTOMER FEEDBACK:
{feedback_context}

Answer these questions from the customer's perspective:
1. What problem does this solve for me?
2. Why should I care about this?
3. How will this make my life better?
4. What would make me skeptical?
5. What would delight me about this?
```

---

## Step 2: Press Release

### System Prompt
```
You are writing an Amazon-style press release for a product that has already launched. You write as a journalist would: factual, third person, with the customer as the subject of the sentences. Every claim comes from the customer evidence you are given.
```

### Structure: exactly seven paragraphs, one job each

Above the paragraphs: a short, bold **headline**, and a one-sentence **subheading** with what launched and the most important customer benefit, with at most two numbers. Write the subheading last, once the body shows which numbers matter most.

| Para | Its only job |
|------|--------------|
| 1 | **Summary.** Location, a future date, what launched, for whom, and the one thing to know. Assume the reader stops here. |
| 2 | **Problem.** The customer's situation today, the friction, and what it costs them. No solution and no product name. |
| 3 | **Solution.** How the product helps, at a high level, in plain language. No step-by-step experience. |
| 4 | **Leader quote** from the company launching the product: why it matters, in two or three short, confident sentences. Format: "Quote," says [Name], [Title]. |
| 5 | **Customer experience.** One journey from trigger to outcome, step by step, for each persona that matters. No architecture. |
| 6 | **Customer testimonial.** Two or three sentences in the persona's own voice: a feeling or a concrete benefit, as they would tell a colleague. Avoid the "I used to, now I" pattern. Mark it as synthetic. |
| 7 | **Call to action.** Where to get started, in one or two sentences. |

### Rules
- 500 to 700 words from the headline to the end of paragraph 7. Fewer usually means a paragraph is missing; more means FAQ material has crept in.
- Flowing paragraphs only. Headings inside the press release turn it into a vision document.
- The customer is the subject: "Chefs can now…", not "[Company] launches a platform that…".
- Start every paragraph positively, with what the product does. Objections belong in the FAQ.
- No superlatives and no "first" or "first-ever" without evidence.
- Draft lean: three or four sentences a paragraph.
- **Labels stay out of the way.** A press release reads as journalism, not as a report. Known claims carry no label in it. Label a claim only when it is Assumed or Needs evidence, once, at the end of its sentence. The FAQ carries the labels for every number.
- **Each claim keeps the scope of its evidence.** A number from one account, one quote, or one month is written as that: "one corporate account reports…", never as a general fact. If you need a general claim, use a figure that covers the whole data.
- **Use the North Star's numbers.** Targets in the press release and the FAQ are the ones in the North Star. If one differs, for example a smaller pilot target, say so and why.

### User Prompt Template
```
Write the press release for this product, following the seven-paragraph structure and rules above.

Customer insights:
{previous_step_output}

Personas (for paragraph 5 and the testimonial):
{personas_context}

Evidence (every number and claim must come from here):
{signal_summary}
```

### Quality checks before moving on

1. Count the paragraphs between the subheading and the FAQ: exactly seven, each doing only its job.
2. Count the words: 500 to 700.
3. Can every claim about the problem and its impact point to evidence in the Signal Analysis Report? Label each claim Known, Assumed, or Needs evidence.
4. Would a real customer in the target segment recognize themselves?
5. Run `writing-audit.md` on the whole PR/FAQ.

---

## Step 3: Customer FAQ

### System Prompt
```
You are anticipating customer questions about a new feature.
Think like a skeptical but interested customer.
```

### User Prompt Template
```
Generate the Customer FAQ section.

Press Release:
{previous_step_output}

Create 5-7 customer FAQs covering:
- How does this work?
- How much does it cost?
- When is it available?
- What if I have problems?
- How is this different from alternatives?
- Questions specific to each persona

Format as Q&A pairs.
```

---

## Step 4: Internal FAQ

### System Prompt
```
You are anticipating internal stakeholder questions.
Think like executives, engineers, and business partners.
```

### User Prompt Template
```
Generate the Internal FAQ section.

Press Release and Customer FAQ:
{previous_step_output}

Create 5-7 internal FAQs covering:
- Why now? Why this?
- What are the technical requirements?
- What are the risks?
- How do we measure success?
- What resources are needed?
- What's the timeline?

Format as Q&A pairs.
```

---

## Final Assembly

After all 4 steps, combine into a single document with sections:
1. Press Release
2. Customer FAQ
3. Internal FAQ

Save as `discovery/{project}/working-backwards/prfaq.md`
