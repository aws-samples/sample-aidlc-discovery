# Riskiest assumption: self-service rebooking for disrupted passengers
Named by the team, 2026-10-29; widened by the head of digital after the persona critique, 2026-10-29. Demonstration run on fictional sample data.

**Assumption:** Disrupted passengers who are offered real choices quickly will choose a new flight themselves, and will not need to call for anything else: not to check the flight, and not for what the disruption leaves them needing, such as a hotel for tonight.

*Changed after the persona critique (v2):* the first wording was "trust it enough not to call". The critique found that every disrupted persona trusted the flight they chose, but Ingrid, Daniel, and Helena would still call for a hotel when the new flight is the next day, and corporate travellers may be called by their travel desk. A passenger who calls for the hotel removes no queue, so the assumption now covers every reason to call.

**Why it is the riskiest:** If passengers wait for the airline to decide, or choose and then call to check, no queue is removed: the self-service rate does not reach 35%, rebooking calls do not fall to 25 per 100, and the feature adds a screen without removing a call. Everything else in the PRD (reissue, rebooking for someone else, P1) depends on it. Evidence for it today: 37 records ask to choose the flight themselves, and 410 disrupted passengers already rebook in the app [Known]; evidence that they would trust their choice without calling: none yet [Needs evidence] (research hypotheses 1 and 2).

**What the prototype must show:** the moment of decision. In each of the three paths (Ingrid at the gate, Daniel at 23:00, Helena's daughter at home), the passenger opens the disruption message, sees the airline's suggestion and the real alternatives with times, seats together, and nothing to pay, chooses one, confirms, and reaches a boarding pass and confirmation, in under three minutes. The confirmation screen is where it is won or lost: it must show, plainly, that the new ticket is issued (with its e-ticket number), nothing was charged, everyone moved together, and, when the new flight is the next day, where the passenger sleeps tonight, so nothing is left to call about.

**How we will judge it** (thresholds set by the team, 2026-10-29). Test: 8 recently disrupted passengers walk through the prototype.
- **Supports it:** at least 6 of 8 choose a flight without help, reach the boarding pass in under three minutes, and say they would not call for anything: not to check the flight, not for a hotel or anything else.
- **Contradicts it:** 3 or more of 8 say they would still call, for any reason, or wait for the airline to decide.
- **In between:** a result that meets neither rule (for example, 5 of 8 pass, and the others only miss the three-minute target) settles nothing on its own. The team reads the reasons and decides in Validate whether it is a usability fix or a sign against the assumption.
- **Who can judge it:** the thresholds need real, recently disrupted passengers. The persona critique today is synthetic: it can find problems with the screens, but it cannot meet or break these thresholds. Until the 8 walk-throughs run, the assumption stays an open hypothesis in the brief (research hypothesis 1). Recruiting the 8: head of digital and UX designer, by the 30-day follow-up (team, 2026-10-29).

## Not the riskiest assumption, but carried to Validate
| Item | Type | Owner | Why it goes to Validate |
|------|------|-------|-------------------------|
| Reissue and fare rules work without an agent | Feasibility | Engineering lead | Tested by the engineering spike, not by the prototype; can move June 2027 |
| Bags follow a self-service rebooking, and the booking is final without an agent (shown on the v1/v2 screens) | Feasibility | Engineering lead | Part of the reissue spike |
| Hotel vouchers can be issued without an agent (shown on v3's "You're rebooked" and Helena's text) | Feasibility | Customer service operations lead | The widened assumption depends on it; today vouchers only come through an agent |
| The company's travel desk and travel management company see the change, so they do not call to reconcile (critique finding 2) | Valuable / feasibility | Head of corporate accounts, with design partners | A second reason to call that no screen answers; informing them is P2-1 |
| Whose phone gets the text when an agency booked (critique finding 4) | Feasibility / security | Engineering lead, with the security review | Contact details on agency bookings may be the agency's |
| Booking reference plus surname is safe enough to rebook for someone else (feature C) | Feasibility and security | Engineering lead, with security review | It is today's manage-booking rule; rebooking raises the stakes |
