# Slide outline: AI-DLC Discovery, stage by stage

A deck of about 21 slides (30 to 40 minutes) introducing the method to new facilitators. Each slide has a headline that states the point, at most three bullets, what to **show** (an artifact from the AnyCompany Air reference run), and what to **say**.

Source: [phase-map.html](phase-map.html). Terms follow [glossary.html](glossary.html). Example artifacts are in [`facilitator/reference-runs/anycompany-air/`](../../facilitator/reference-runs/anycompany-air/), the unattended run. For a live demo, [`anycompany-air-with-team/`](../../facilitator/reference-runs/anycompany-air-with-team/) is stronger: every checkpoint has a team decision in it, and it is the run train-the-trainer demos. The "Or, with a team" lines point to it. Don't show `facilitator/anycompany-air.md` to people who will play the sample later: it is the answer key.

For leaders or participants, keep slides 1–5, one slide per stage (the first slide of each section), and 19–20.

---

## Opening

### 1. In one day, a team goes from customer feedback to a decision and a brief the build starts from
- Five phases, about 6.5 working hours, run in Amazon Quick Desktop
- The assistant drafts; the team decides
- The team leaves with a decision, a clickable prototype, and the Discovery brief

**Say:** "Today we decide what to build next, from evidence, and leave with a brief the build starts from." (The kickoff line from the run-sheet.)

### 2. Teams build what the loudest voice asks for
- Discovery puts the team's beliefs on record first
- Then it tests them against customer evidence
- It ends in a decision: commit, pivot, or park

**Say:** In the Air sample, the head of digital is sure the booking flow is the problem. The data says otherwise. The method is built to make that visible without anyone losing face.

### 3. Five questions, asked in order
| Phase | The question |
|---|---|
| Signals | What are customers telling us? |
| Working Backwards | Which problem first, for whom, and how would we announce it? |
| Prototype | What would it look like? |
| Validate | What could make it fail, and how will we know it worked? |
| Handoff | What does the build start from? |

**Show:** the day timeline from the phase map (09:00 kickoff, 16:15 readout).

### 4. Each phase hands a file to the next
- Signals → `signal-summary.md` → Working Backwards → `prd.md` + `riskiest-assumption.md` → Prototype → `index.html` + `persona-critique.md` → Validate → `decision.md` → Handoff
- A phase can't start until its file exists
- So a team can stop and resume next week, or in a new chat

**Show:** the relay diagram from the phase map.

### 5. Three rules hold every phase together
- **The team decides:** every phase ends at a checkpoint
- **Every claim carries a label:** Known, Assumed, or Needs evidence
- **No architecture:** Discovery decides who, what, and why

**Say:** Ask the room to listen for the three labels all day. They are how unproven ideas survive as honest open questions.

---

## Setup and Signals

### 6. Setup agrees the one number everything is scored against
- Product, people, the business metric and its baseline, the data input
- Data is production, Signal Briefs, or synthetic prepared beforehand, never written on the day
- The product owner confirms the metric out loud

**Show:** `PROJECT.md`.
**Say:** Don't confirm the setup yourself. Ask, "Is anything here wrong or missing?"

### 6b. In a team Space, everyone follows and one person drives
- Save the workshop in an Amazon Quick team Space: everyone attaches it, reads, asks questions, and opens the prototype
- One driver at a time; anyone can take over with one prompt
- Customer data stays out unless the Space is restricted to people allowed to see it

**Show:** [`docs/team-space.md`](../../docs/team-space.md), the folder tree.
**Say:** Nothing in the method changes; only where the files live. Optional, and Amazon Quick only.

### 7. Signals: beliefs go on record before the data speaks
- Five questions, one at a time, before any analysis
- Each becomes "We expect [segment] to [problem], because [...]"
- AI analysis is persuasive; written beliefs let the team check itself

**Show:** [`signals/team-hypotheses.md`](../../facilitator/reference-runs/anycompany-air/signals/team-hypotheses.md): nine beliefs, one per role.
**Say:** Ask the quietest person first.

### 8. The report weighs signal over frequency
- Top signals scored on frequency, severity, and reach (out of 30), with counts and quotes
- In Air, "Delayed baggage" is the top single call reason, but disruption is 42 of 110 calls and 62% of handle time
- The "What the team expected" table shows each belief against the data

**Show:** the "What the team expected" table in [`signals/signal-summary.md`](../../facilitator/reference-runs/anycompany-air/signals/signal-summary.md).
**Say:** Read what each person got right before what the data contradicts. Ask "Where does it work well?" before the challenge.

---

## Working Backwards

### 9. Personas put faces on the signals, and one of them is happy today
- Three or more, drawn from real quotes, each with a confidence rating
- One is satisfied today, so the team sees what it could break
- They are synthetic: hypotheses, not customer evidence

**Show:** the four Air personas (`working-backwards/personas/`): Tomasz, Amara, Rafael, Hanne.
**Say:** Ask the people closest to customers: "Have you met this person?"

### 10. Scoring picks one problem, and the team owns every score
- Gate first: evidence, outcome, owner, build path, painkiller
- Six weighted scores, then confidence, then build first, prototype to learn, defer, or drop
- One use case per team or pod goes forward

**Show:** the Scores table in [`use-case-scoring.md`](../../facilitator/reference-runs/anycompany-air/working-backwards/use-case-scoring.md): rebooking 4.60, build first; the 3D seat map dropped at the gate as "customers would not notice".
**Say:** Fix the weights before the first score, so nobody can move one to help their favourite.
**Or, with a team:** the head of digital's override in [`use-case-scoring.md`](../../facilitator/reference-runs/anycompany-air-with-team/working-backwards/use-case-scoring.md): booking flow 2.50 to 3.00, still Defer. Heard, and the day didn't change.

### 11. Frame the problem before writing the press release
- **Today statement:** "They need a way to [outcome]", never a mechanism
- **How Might We:** one question that opens the solution space
- **North Star:** a capability, not a product, with the day's numbers

**Show:** the Today statement and North Star in `working-backwards/working-backwards.md` (self-service rebooking from 12% to 40%).

### 12. The press release comes before anything is built
- Exactly seven paragraphs, 500 to 700 words, the customer as the subject
- The team reads it aloud and rewrites what doesn't sound like them
- A readiness check gives GREEN, AMBER, or RED, and names the prototype slice

**Show:** [`prfaq.md`](../../facilitator/reference-runs/anycompany-air/working-backwards/prfaq.md): AMBER, three gaps carried as open hypotheses.
**Or, with a team:** [`prfaq.md`](../../facilitator/reference-runs/anycompany-air-with-team/working-backwards/prfaq.md): AMBER to GREEN as the room closed gaps, and a sentence rewritten by the operations lead.
**Say:** AMBER is a good result; don't chase GREEN. Background: [Vogels, "Working Backwards"](https://www.allthingsdistributed.com/2006/11/working_backwards.html).

### 13. Name the one assumption that would end the idea
- Chosen from the Assumed and Needs evidence claims
- Everyone chooses before anyone speaks
- Set the pass mark now, before any result

**Show:** [`riskiest-assumption.md`](../../facilitator/reference-runs/anycompany-air/working-backwards/riskiest-assumption.md): "...trust the confirmation enough not to call or queue."
**Say:** "Which one, if wrong, means we built something nobody uses?"
**Or, with a team:** [`riskiest-assumption.md`](../../facilitator/reference-runs/anycompany-air-with-team/working-backwards/riskiest-assumption.md): the critique widened it from "won't call to check" to "won't need to call for anything", with thresholds set before any test.

---

## Prototype

### 14. The prototype is aimed at the riskiest assumption
- 4 to 8 screens, with one marked as the test moment
- One HTML file with Flow, Mobile, and Desktop views
- A prototype that tests nothing is a demo

**Show:** `prototype/index.html` on the Flow view, then Mobile.

### 15. The personas find what the team misses, and every change is a new version
- Each persona walks the flow in its own voice and gives a day-one adoption score
- The team picks which findings to fix; v1 is never overwritten
- A fix that promises something unconfirmed is logged as Needs evidence

**Show:** [`versions.md`](../../facilitator/reference-runs/anycompany-air/prototype/versions.md) and `compare.html` (open it in a browser; in Amazon Quick its frames show empty): v2 added the ticket number and "You don't need to call us"; the agency notice is logged Needs evidence.
**Say:** "Looks good" at the first click-through is normal. The critique does the work.

---

## Validate

### 16. Validate tries to prove it fails, using only what's in the room
- Four risks: valuable, usable, feasible, viable ([Cagan](https://www.svpg.com/four-big-risks/))
- Pre-mortem: "It's 90 days after launch and it failed. Why?" ([Klein](https://hbr.org/2007/09/performing-a-project-premortem))
- It never waits for surveys; what's unsettled stays open

**Show:** the four-risks table in `validate/risk-review.md`.

### 17. Success criteria are numbers with dates, and the decision is the team's
- 3 to 5 criteria, each with metric, baseline, target, and check date
- Commit, pivot, or park; commit can mean "test first", with conditions
- A validated decision not to build is a good outcome

**Show:** [`decision.md`](../../facilitator/reference-runs/anycompany-air/validate/decision.md): commit, testing first, with three conditions, each with an owner, due by day 30.

---

## Handoff and after

### 18. The brief is one document for someone who wasn't in the room
- 15 sections, plain Markdown, no architecture
- Written for every decision, including park
- For AI-DLC it replaces Ideation; AI-DLC starts at Inception, and the skill prints the command

**Show:** scroll [`handoff/discovery-brief.md`](../../facilitator/reference-runs/anycompany-air/handoff/discovery-brief.md) (about 19,000 characters).
**Say:** "Could an engineer who wasn't here start from this brief?"

### 19. The follow-ups do what the personas couldn't
- 7 days: the baseline is in, the brief is in the build repository
- 30 days: real users try the prototype; open hypotheses go to real customers
- 30 and 60 days: the numbers against the success and kill criteria

**Say:** What the team learns goes back into Signals for the next cycle.

### 20. Your job is the room
- Time, energy, and making sure the team does the thinking
- Hold the line on order: hypotheses before analysis, risks before the decision
- Next: run the solo dry run, take the train-the-trainer session, co-facilitate once

**Show:** [`facilitator/run-sheet.md`](../../facilitator/run-sheet.md) and [`train-the-trainer.md`](../../facilitator/train-the-trainer.md), "Ready to facilitate".

---

## Building the deck

To turn this into a branded deck, ask for the AWS presentations toolkit with this file as the outline. Screenshot the reference-run artifacts rather than retyping them, so the deck shows real output.
