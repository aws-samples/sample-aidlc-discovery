# Reference run: AnyCompany Air, unattended

**Facilitators only. Spoilers.**

One complete Discovery run on the Air sample, with its telemetry, made by the automated end-to-end test on 30 October 2026 with skill 3.0.0: the skill ran all five phases in Claude Code with no team present, taking its defaults at every checkpoint. It passed every automated check (`TESTING.md`). Use it as the example of the current formats; `../anycompany-air-with-team/` shows what a team adds, but predates them.

What to look at, in workshop order:

- [signals/signal-summary.md](signals/signal-summary.md): disruption first, and the **Say and do** table, which reads each theme against the telemetry: the rebooking journey fails with no server errors, the August payment timeouts are real and small, and the alerts arrive late in peak months.
- [working-backwards/personas/](working-backwards/personas/): a **buyer** (the travel manager, who judges value and renewal) and **end users** (the travellers), each labelled, plus a satisfied regular.
- [working-backwards/use-case-scoring.md](working-backwards/use-case-scoring.md): the **candidates from Signals** (late, empty alerts and travel-desk rebooking kept; price dropped, with the reason), then one decision: self-service rebooking build first (4.60), late alerts next in line (4.00), the 3D seat map dropped at the gate.
- [working-backwards/working-backwards.md](working-backwards/working-backwards.md) and [working-backwards/prfaq.md](working-backwards/prfaq.md): "Choose your flight", the framing, the seven-paragraph press release, and the readiness verdict with the Prototype scope.
- [working-backwards/prd.md](working-backwards/prd.md), section 11: the **AI feature block** for the head of digital's assistant: a first-draft prompt, 10 evaluation cases (typical, edge, and negative), and sample outputs, labelled Assumed.
- [prototype/index.html](prototype/index.html): open it in a browser and use the Flow, Mobile, and Desktop views. The options screen shows the sample outputs; [prototype/persona-critique.md](prototype/persona-critique.md) has the personas reacting to them, and [prototype/versions.md](prototype/versions.md) logs the changes.
- [validate/risk-review.md](validate/risk-review.md) and [validate/decision.md](validate/decision.md): commit, testing the riskiest assumption first, with the success criteria, including the **AI quality target** (at least 9 of 10 typical and edge cases accepted, no negative case passing), also a row in [working-backwards/gtm.md](working-backwards/gtm.md).
- [handoff/discovery-brief.md](handoff/discovery-brief.md) and [handoff/next-steps.md](handoff/next-steps.md): the brief carries the AI feature block and the quality target, and next steps end with the **roadmap for the product owner: Now, Next, Later**.

**How it differs from a workshop with a team.** Nobody challenged the signals, overrode a score, or iterated on the prototype by hand, so every decision is the skill's default. `PROJECT.md` lists each choice under "Unattended choices". A run with a team will have different personas and numbers, because each run analyzes the same data independently.
