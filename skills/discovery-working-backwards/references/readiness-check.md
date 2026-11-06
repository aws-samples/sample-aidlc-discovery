# Readiness check

Run after the PR/FAQ and before the prototype. The check makes sure the PR/FAQ says enough to build a prototype that proves something, so the prototype session validates answers instead of discovering them.

## The seven questions

For each question, **draft a full answer** from the PR/FAQ, the PRD so far, and the signals: three to five sentences, not a status label. Where the answer is missing or vague, write what is there and mark the gap inline with `[GAP]`, saying what is missing and how to get it.

| # | Question | What a ready answer contains |
|---|----------|------------------------------|
| 1 | **Persona** | Who the primary user is (a persona name and role) and the one thing they are accountable for |
| 2 | **Pain today** | The current process end to end, how long it takes, and the worst part, with evidence |
| 3 | **Prototype experience** | The full future journey step by step, then the **slice the prototype will show**, and what that slice does. This is the most common gap |
| 4 | **Vision** | What happens automatically, what stays with the person, and how fast it should be |
| 5 | **Views and signals** | The screens the user needs (for example summary, exceptions, detail), what must be visible at a glance, and how the user is told when to act |
| 6 | **Data** | Which data the product needs, where it lives today, how fresh it must be, and the main business objects (for example orders, accounts, deliveries) and how they relate. Business level only: no architecture |
| 7 | **Prototype metric** | What the prototype measures, and how it maps to the PR/FAQ's success metric and the riskiest assumption |

## Verdict

- **GREEN:** every question answered. Go to the PRD and the prototype.
- **AMBER:** one to three gaps. Go ahead, with the gaps listed as open hypotheses.
- **RED:** four or more gaps. Iterate on the PR/FAQ with the team before the prototype.

Show the team the verdict, the gaps with a question that would close each, and the prototype slice. Ask whether to close the gaps now or carry them.

## Output

Append to `working-backwards/prfaq.md`:

```markdown
## Readiness check
Verdict: GREEN | AMBER | RED, because [one sentence]

## Prototype scope
**Q: Who is the primary user, and what are they accountable for?**
A: [drafted answer, with [GAP] markers]
(one Q and A per question, seven in total)

**Full journey:** [the end-to-end story]
**Prototype slice:** [what the prototype shows, and why this slice]

| # | Gap | Question that would close it | Must-have or nice-to-have |
```

Handoff and the prototype use the Prototype scope section, so keep it in the PR/FAQ.
