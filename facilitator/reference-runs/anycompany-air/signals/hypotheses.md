# Research hypotheses: AnyCompany Air digital
From the Signal Analysis Report (`signal-summary.md`). Demonstration run on fictional data. No market or competitive research documents were in the data, so the market and competitive evidence below comes only from what customers said about other airlines.

### Hypothesis 1: Choosing is the missing action
**Statement:** We believe that disrupted passengers who view alternatives would choose a new flight themselves if the screen let them, because 60% already view alternatives and 41% tap Contact us instead.
**Evidence:**
- VoC: 116 disruption records; "why I can see alternative flights on the website but can't move myself onto one".
- Telemetry: 150,845 alternatives views, 42,529 kept suggestions, 102,456 Contact us taps.
- Competitive: "Other airlines show you where your bag is" type comparisons appear for bags, not for rebooking; no competitor rebooking evidence. **[Needs evidence]**
**Confidence:** HIGH (feedback in 6 sources, telemetry, operations data)
**Test approach:**
- [ ] Prototype the alternatives screen with a Choose action; run it with disrupted passengers.
- [ ] Method: prototype test, then an A/B test on a share of disruptions.
- [ ] Expected: at least half of those who view alternatives complete a choice without calling.
**Connection to Working Backwards:** Persona: disrupted leisure traveller, corporate road warrior. PR/FAQ: "Disrupted passengers can now pick their new flight in the app in under two minutes."

### Hypothesis 2: The airline's automatic pick is the trigger for most calls
**Statement:** We believe that most rebooking calls come from passengers whose automatic rebooking does not fit their plans (wrong day, long layover, family split), because only 28% of those who view alternatives keep the suggestion.
**Evidence:** VoC: CALL-0069, CALL-0077, CALL-0107, REV-0048, AGY-0021. Telemetry: keep-suggestion 42,529 of 150,845.
**Confidence:** MEDIUM
**Test approach:** [ ] Sample 200 rebooking calls and code why the suggestion did not work. [ ] Method: call audit. [ ] Expected: over 60% name timing, routing, or group splits.
**Connection:** Persona: family traveller. PR/FAQ topic: "Your new flight, your choice."

### Hypothesis 3: Self-service rebooking raises disrupted-passenger NPS
**Statement:** We believe that passengers who rebook themselves are much less unhappy than those who call, because self-service app NPS is +4 against −58 for the call centre.
**Evidence:** Disruption NPS by rebooking channel (410 / 260 / 1,630 / 980 responses). **Confounder:** today's self-service passengers kept a suggestion that suited them. **[Assumed]** that the gap holds for passengers who choose.
**Confidence:** MEDIUM
**Test approach:** [ ] Compare NPS of choosers vs callers in the pilot. [ ] Method: A/B test. [ ] Expected: choosers' NPS at least 40 points above callers'.
**Connection:** Persona: all disrupted. PR/FAQ: NPS quote.

### Hypothesis 4: Ticket reissue failures will break self-service choice
**Statement:** We believe that a self-service choice will fail for about 5% of passengers unless the reissue errors are handled, because the reissue service rejects 5.0% of requests today (fare rules, locked tickets, extras not moved).
**Evidence:** Telemetry errors-top; VoC: "The new ticket wasn't issued", charged a change fee after a cancellation.
**Confidence:** HIGH that the errors exist; LOW on how they show up in self-service.
**Test approach:** [ ] Engineering replays a month of reissue requests for alternatives that would be offered. [ ] Method: technical spike. [ ] Expected: error rate and the cases that need a fallback.
**Connection:** Persona: corporate road warrior (extras, fare rules). PR/FAQ: FAQ on "what if my extras don't move".

### Hypothesis 5: Corporate renewals depend on disruption handling
**Statement:** We believe that corporate accounts will renew on better terms if travellers can self-rebook and the travel desk can see status, because four accounts tie renewal or tender to disruption.
**Evidence:** ACC-0008, -0012, -0015, -0017, -0018, -0020; AGY-0015.
**Confidence:** MEDIUM (account manager notes, second-hand)
**Test approach:** [ ] Show the prototype to three travel managers. [ ] Method: interviews. [ ] Expected: they name it as a renewal factor.
**Connection:** Persona: travel manager. PR/FAQ: travel manager quote.

### Hypothesis 6: Late alerts cost passengers the best alternatives
**Statement:** We believe that in peak months passengers lose the good alternatives before they are alerted, because alert delay p95 rises from about 11 to about 41 minutes in July and August.
**Evidence:** Spans: disruption.alert.delay_from_event; PROVIDER_THROTTLED 955; VoC: "call immediately before the good flights fill up".
**Confidence:** MEDIUM
**Test approach:** [ ] Measure seats left on the best alternative at alert time vs event time. [ ] Method: data analysis. [ ] Expected: fewer options at alert time in peak.
**Connection:** Persona: leisure. PR/FAQ: FAQ on how fast passengers hear.

### Hypothesis 7: More agents would not move the self-service rate (team hypothesis 4, not settled)
**Statement:** We believe that adding summer agents would shorten holds but leave the call rate per disrupted passenger at about 415 per 1,000, because the rate is flat across months with very different volumes.
**Evidence:** operations-monthly.
**Confidence:** MEDIUM
**Test approach:** [ ] Compare hold time and calls per 1,000 in weeks with different staffing. [ ] Method: operations data. [ ] Expected: hold time falls, calls per 1,000 stays.

### Hypothesis 8: Bag tracking would cut repeat baggage calls
**Statement:** We believe that passengers with delayed bags call repeatedly because they cannot see status, because 45 records describe repeat calls and untracked bags.
**Evidence:** VoC only; no baggage telemetry.
**Confidence:** MEDIUM
**Test approach:** [ ] Count repeat calls per baggage case. [ ] Method: call data. [ ] Expected: over two calls per case.

### Hypothesis 9: A 3D seat map would increase seat upgrade revenue (team hypothesis 3, not settled)
**Statement:** We believe that seat buyers would upgrade more with a 3D view, because 16 customers asked for one.
**Evidence:** VoC: 16 mentions, all nice-to-have. No revenue data.
**Confidence:** LOW
**Test approach:** [ ] Get seat upgrade take rates and test a photo view of extra-legroom seats. [ ] Method: A/B test. [ ] Expected: measurable uplift, or none.

### Hypothesis 10: Booking redesign would raise conversion (team hypothesis 1, not settled)
**Statement:** We believe that fewer upsell steps and multi-city would lift web conversion above 3.1%, because 43 records mention friction.
**Evidence:** Conversion already above benchmark and flat. **Confidence:** LOW
**Test approach:** [ ] A/B test removing one upsell page. [ ] Expected: conversion change under 0.1 point if the hypothesis is wrong.
