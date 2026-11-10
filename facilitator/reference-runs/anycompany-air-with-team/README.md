# Reference run: AnyCompany Air, with a team

**Facilitators only. Spoilers.**

One complete Discovery run on the Air sample, facilitated by hand in AWS Quick Desktop on 29 October 2026 by following `../../dry-run-air.md`, with the team's answers pasted from it. Unlike the unattended run (`../anycompany-air/`), every checkpoint here has a team decision in it: challenges, an override, changes to the prototype plan, and a decision review. It passes every automated check (`TESTING.md`).

**Made before the telemetry and skill 3.0.0.** This run has no Say and do table, no telemetry evidence, no roadmap in `next-steps.md`, no candidates from Signals, no separate buyer and end-user personas, no AI feature block, and no AI quality target; a run today has all of them.

What it shows that the unattended run cannot:

- **Signals challenged.** In [signals/signal-summary.md](signals/signal-summary.md), "Team challenges": the head of digital's blind spot (shoppers who never booked), a correction to the report (corporate travellers do speak for themselves), and the operations lead's point about passengers who won't use an app, carried forward as hypothesis 11 and a persona.
- **An override that is heard but does not change the day.** In [working-backwards/use-case-scoring.md](working-backwards/use-case-scoring.md), the head of digital raises the booking flow's pain to 4; the score moves from 2.50 to 3.00 and stays Defer, and the assistant checks the claim against the reviews without undoing it.
- **The team's framing and targets.** In [working-backwards/working-backwards.md](working-backwards/working-backwards.md) and [working-backwards/prfaq.md](working-backwards/prfaq.md): the targets the team signed up to (35%, 25 calls per 100, a boarding pass in under three minutes), a sentence rewritten by the operations lead, and the readiness check moving from AMBER to GREEN as the team closes gaps.
- **A riskiest assumption that the critique widened.** [working-backwards/riskiest-assumption.md](working-backwards/riskiest-assumption.md): passengers choose and trust the new flight, but the persona critique found they would still call for a hotel or their travel desk, so "won't call to check" became "won't need to call for anything", with thresholds set before any test.
- **Three prototype versions.** [prototype/versions.md](prototype/versions.md) logs why each changed. Open [prototype/index.html](prototype/index.html) (v3) in a browser, go to "You're rebooked", and tick "Show test moment": that confirmation screen is where trust is won or lost. Claims nobody has confirmed are marked Needs evidence.
- **A decision that refused to be rushed.** [validate/decision.md](validate/decision.md): the decision was given early, saved as intent, and recorded only after the pre-mortem, with three ordered conditions, each with an owner and a follow-up.
- **The handoff.** [handoff/discovery-brief.md](handoff/discovery-brief.md) and [handoff/next-steps.md](handoff/next-steps.md), with the AI-DLC command and the owners of every open item.

Open `prototype/compare.html` in a browser, not in AWS Quick's session tab, where its frames stay empty.
