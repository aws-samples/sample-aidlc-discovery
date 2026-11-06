# AI feature block

Only for a feature that uses AI: one where a model generates, ranks, summarizes, or decides something the customer sees. About 10 minutes with the team. It goes at the end of the PRD, after the AI feature checklist.

The block is a starting point for the build, not a specification. The model, the data and retrieval design, and the final prompt are chosen in the build. What Discovery adds is a first answer to "what should it say, and how would we know it is good?", drawn from the customers' own words, early enough to test it in the prototype.

## 1. First-draft prompt

Write it as the feature would receive it, in four parts:

```markdown
### First-draft prompt
**Job:** what the feature does for the customer, in one or two sentences.
**Tone:** how it sounds, from the personas and the brand (for example: calm, short sentences, no jargon).
**Inputs:** what it receives each time (for example: the disrupted booking, the passengers, the available flights, what the passenger said matters).
**Output format:** what it returns and how long (for example: one recommended flight, why in one sentence, and two alternatives).
**Must not:** what it must never do (from the guardrails in the checklist).
```

## 2. Evaluation cases

5 to 10 cases, each an input with what a good output looks like. Draw them from the Signals quotes and the personas: every case should trace to a real complaint or a persona's situation.

| # | Type | Input (the situation) | A good output | From |
|---|------|-----------------------|---------------|------|
| 1 | Typical | ... | ... | quote or persona |

- **Typical** (about half): the everyday situations the feature exists for.
- **Edge** (two or three): hard but legitimate situations, for example a group that cannot sit together, or a connection with little time.
- **Negative** (at least two): what the feature must refuse or flag instead of answering, for example promising compensation it cannot grant, recommending a flight with no seats, or inventing a policy.

## 3. Sample outputs for the prototype

For three or four of the cases (at least one typical, one edge, and one negative), write the output the draft prompt would produce, as the feature would show it. The prototype shows these, so the team and the persona critique react to real AI output, not to a placeholder. Label them in the prototype as sample output from the first-draft prompt.

## Then

- The AI quality target in Validate is measured on these cases: for example, the share of typical cases a reviewer accepts, and no negative case passing.
- The Handoff brief carries the block, so the build starts from it.
- Label the prompt and the sample outputs **Assumed**: nobody has run them on a model with real data yet.
