# Persona critique

The end of Prototype. Each persona reacts to the first build in its own voice, so the team sees where the idea serves its customers and where it breaks. The findings drive the team's iteration, and Validate uses them as the main evidence for the valuable and usable risks.

## Inputs

- Every persona in `working-backwards/personas/`
- The version to critique, `prototype/v[N].html` (the one `index.html` copies), walked through screen by screen
- `working-backwards/prfaq.md` and `riskiest-assumption.md`
- The Signal Analysis Report, for the quotes behind each persona

## For each persona

Stay in the persona's role, use its communication style, and ground every reaction in its pain points and quotes. Start each answer with `**[Persona: Name]**`.

1. **Walk through.** Go through the flow on the real screens, as this person, in their usual context (device, time pressure, place), and record every step (see "Record the walkthroughs"). Say where you would hesitate, get stuck, or give up.
2. **My pain.** Which of my pain points does this solve? Quote the feedback lines that match. Which does it leave unsolved?
3. **My workflow.** Where does it not fit how I work today? Be specific about steps that would not work for me.
4. **Switching.** What would make me drop my current workaround for this? What would stop me?
5. **The riskiest assumption.** From where I stand, is it true? Why?
6. **Day one.** On a scale of 1 to 10, how likely am I to use this on day one, and why?

The satisfied persona answers one more question: what does this change that already works for me, and what would I lose?

## Record the walkthroughs

The team watches each persona's walk in the prototype's **Personas** view, so record it the way the persona did it, tap by tap, on the screens as they are built:

1. Read the screen templates in the version file. A tap is a button or card the screen shows; copy its text exactly. It leads where its `data-go` points. If it has no `data-go`, nothing happens: the persona stays on the screen and reacts to that. Never move a persona to a screen the prototype cannot reach from where they are.
2. Start where this persona's path starts. A persona whose flow is an edge case may start at the screen where it branches off.
3. One step per screen, plus a step for each moment that matters on it: what they look at, what they think, where they hesitate. End where they finish, stop, or give up.
4. Give each step a mood: `ok`, `hesitate`, `stuck`, or `gave-up`. Link a step to the finding it shows with the finding's number in the table.

Write the steps into the version file's `persona-walkthroughs` block, the only change to that file, in the format its comment shows: `id` is the persona's file name without `.md`, `say` is what the persona thinks, in the project language and in their voice, at most two sentences. When `index.html` is a copy of that version, write the same block into it so the copy stays exact. Before saving, check every step against rule 1: the tap's text is on that screen, and the next step is on the screen the tap leads to. The Personas view (`#/replay`) also flags a step that does not fit with a **Replay check** line; when one shows, fix the step.

## Rules

1. **Stay grounded.** A reaction with no link to the persona's evidence is labeled Assumed.
2. **Be direct.** Personas say what does not work. A critique with no problems is not useful.
3. **Personas are not customers.** They are synthetic. Say so in the summary: the real-user test happens in the follow-up.

## Output

The walkthroughs in `prototype/v[N].html` (and `index.html` when it copies that version), and `discovery/[project]/prototype/persona-critique.md`:

```markdown
# Persona critique: [use case]

## [Persona name]
- Walk-through: where they got stuck, by screen ([replay](v[N].html#/replay/[id]/1))
- Pain solved: [...] ([customer quote, written as the project language rule says]) | Pain not solved: [...]
- Workflow fit: [...]
- Switching: what would make them switch, what would stop them
- Riskiest assumption: holds / does not hold / unclear, because [...]
- Day-one adoption: [1-10], because [...]

(one section per persona)

## What the critique shows
| Finding | Personas | See it | Points to risk | Fix in the iteration? |
| Gets stuck at [screen] | [names] | [[name], step [n]](v[N].html#/replay/[id]/[n]) | Usable | yes / no, because [...] |
| Does not solve [pain] | [names] | [[name], step [n]](v[N].html#/replay/[id]/[n]) | Valuable | yes / no, because [...] |

Synthetic personas, not customers: test these findings with real users in the follow-up.
```
