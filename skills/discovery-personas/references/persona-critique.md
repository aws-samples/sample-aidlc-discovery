# Persona critique

The end of Prototype. Each persona reacts to the first build in its own voice, so the team sees where the idea serves its customers and where it breaks. The findings drive the team's iteration, and Validate uses them as the main evidence for the valuable and usable risks.

## Inputs

- Every persona in `working-backwards/personas/`
- `prototype/index.html`, walked through screen by screen
- `working-backwards/prfaq.md` and `riskiest-assumption.md`
- The Signal Analysis Report, for the quotes behind each persona

## For each persona

Stay in the persona's role, use its communication style, and ground every reaction in its pain points and quotes. Start each answer with `**[Persona: Name]**`.

1. **Walk through.** Go through the core flow screen by screen, as this person, in their usual context (device, time pressure, place). Say where you would hesitate, get stuck, or give up.
2. **My pain.** Which of my pain points does this solve? Quote the feedback lines that match. Which does it leave unsolved?
3. **My workflow.** Where does it not fit how I work today? Be specific about steps that would not work for me.
4. **Switching.** What would make me drop my current workaround for this? What would stop me?
5. **The riskiest assumption.** From where I stand, is it true? Why?
6. **Day one.** On a scale of 1 to 10, how likely am I to use this on day one, and why?

The satisfied persona answers one more question: what does this change that already works for me, and what would I lose?

## Rules

1. **Stay grounded.** A reaction with no link to the persona's evidence is labeled Assumed.
2. **Be direct.** Personas say what does not work. A critique with no problems is not useful.
3. **Personas are not customers.** They are synthetic. Say so in the summary: the real-user test happens in the follow-up.

## Output

`discovery/[project]/prototype/persona-critique.md`:

```markdown
# Persona critique: [use case]

## [Persona name]
- Walk-through: where they got stuck, by screen
- Pain solved: [...] (quote) | Pain not solved: [...]
- Workflow fit: [...]
- Switching: what would make them switch, what would stop them
- Riskiest assumption: holds / does not hold / unclear, because [...]
- Day-one adoption: [1-10], because [...]

(one section per persona)

## What the critique shows
| Finding | Personas | Points to risk | Fix in the iteration? |
| Gets stuck at [screen] | [names] | Usable | yes / no, because [...] |
| Does not solve [pain] | [names] | Valuable | yes / no, because [...] |

Synthetic personas, not customers: test these findings with real users in the follow-up.
```
