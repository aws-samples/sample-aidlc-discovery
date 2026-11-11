# Research hypotheses: AnyCompany Air website and app
From the Signal Analysis Report (`signal-summary.md`), 2026-10-29. Demonstration run on fictional data. No market or competitive research was supplied, so evidence is customer feedback and operational metrics only.

Confidence: HIGH = 3+ independent sources; MEDIUM = 2 sources or one strong source; LOW = 1 source or inferred.

### Hypothesis 1: Disrupted passengers would rebook themselves if they could choose
**Statement:** We believe that disrupted passengers in all segments would choose a new flight themselves in the app or on the website, instead of calling, if they were offered the alternatives with a way to pick one, because today they see alternatives but are told to call.

**Evidence:**
- 37 records ask to choose or change the flight themselves; 118 disruption records across all 6 sources. **[Known]**
- Self-service rebooking rate 12.2%; about 42 calls per 100 disrupted passengers every month. **[Known]**

**Confidence:** HIGH

**Test approach:**
- [ ] Prototype a "choose your new flight" flow after a cancellation and walk disrupted passengers through it.
- [ ] Method: prototype test and interviews; later an A/B test on a share of disrupted passengers.
- [ ] Expected outcome: most participants complete a rebooking without help; in a live test, the self-service rate rises well above 12%.

**Connection to Working Backwards:** Persona: disrupted leisure traveller, frequent flyer, corporate traveller. PR/FAQ topic: "Flight cancelled? Pick your new flight in two taps."

### Hypothesis 2: Rebooking themselves makes disrupted passengers much less unhappy
**Statement:** We believe that disrupted passengers who rebook themselves score the airline far higher than those who call or queue, because waiting on hold while good flights fill up is the worst part of disruption.

**Evidence:**
- Disrupted survey score by channel: app +4, website −2, call centre −58, airport desk −62. **[Known]**
- "The delay wasn't the problem. Not being able to change my flight myself was." **[Known]**
- Harder cases may self-select into calling. **[Assumed]**

**Confidence:** MEDIUM (strong single metric, possible selection bias)

**Test approach:**
- [ ] Compare survey scores for comparable disruptions (same cause, route, delay length) by channel.
- [ ] Method: analysis of existing survey data; then an A/B test.
- [ ] Expected outcome: the gap stays large for comparable cases.

**Connection to Working Backwards:** Persona: all disrupted passengers. PR/FAQ topic: the customer outcome of a calm, controlled disruption.

### Hypothesis 3: Corporate renewals depend on disruption handling, including for travel desks and agencies
**Statement:** We believe that corporate accounts and partner agencies judge AnyCompany Air on disruption handling, and need to rebook travellers in bulk and see where they are, because today their agents call one traveller at a time.

**Evidence:**
- 12 of 30 corporate notes are about disruption; four tie renewal, risk, or a tender to it; one account is trialling a competitor. **[Known]**
- 10 of 30 agency escalations are about disruption: groups rebooked by phone, packages reconsidered, a disruption fee planned. **[Known]**

**Confidence:** MEDIUM-HIGH (two independent sources, both second-hand)

**Test approach:**
- [ ] Interview 5 travel managers and 3 agencies about their last disruption.
- [ ] Method: interviews, then a prototype of the travel-desk view.
- [ ] Expected outcome: rebooking control and traveller visibility rank above booking or price in their renewal criteria.

**Connection to Working Backwards:** Persona: corporate travel manager; agency agent. PR/FAQ topic: "Your travellers rebooked before they reach the gate desk."

### Hypothesis 4: Automatic rebooking picks flights that do not work for customers
**Statement:** We believe that a share of rebooking calls exist only to undo an automatic rebooking (days later, long layovers, split groups), because customers are not asked before the airline chooses.

**Evidence:**
- 9 records about unsuitable automatic rebookings, 11 about split groups and families. **[Known]**

**Confidence:** MEDIUM (three sources: calls, reviews, agencies)

**Test approach:**
- [ ] Sample 100 rebooking calls and tag whether the caller is changing an automatic rebooking.
- [ ] Method: call audit.
- [ ] Expected outcome: a significant share (more than 20%) of rebooking calls change an automatic choice.

**Connection to Working Backwards:** Persona: disrupted family; group organiser. PR/FAQ topic: "We suggest, you decide."

### Hypothesis 5: Disrupted passengers are left without information, especially out of hours
**Statement:** We believe that passengers disrupted late at night or while the phone line is closed get no usable information or options, because notifications say "we will contact you" or "call us".

**Evidence:**
- 17 records about no information or out-of-hours disruption; 13 about errors or conflicting information. **[Known]**

**Confidence:** MEDIUM

**Test approach:**
- [ ] Map every disruption message customers receive, by time of day.
- [ ] Method: message audit and interviews.
- [ ] Expected outcome: most messages give no next step that the customer can act on.

**Connection to Working Backwards:** Persona: leisure traveller cancelled at night. PR/FAQ topic: help available at 23:00.

### Hypothesis 6: Showing bag status would cut repeat baggage calls
**Statement:** We believe that passengers with a delayed or lost bag call repeatedly because they cannot see its status, and would call less if they could.

**Evidence:**
- 45 baggage records in all 6 sources; repeat calls and broken tracing links are common; survey score 3.1. **[Known]**

**Confidence:** MEDIUM

**Test approach:**
- [ ] Count repeat calls per baggage case.
- [ ] Method: call data analysis, then a prototype status page.
- [ ] Expected outcome: most delayed-bag cases generate more than one call.

**Connection to Working Backwards:** Persona: leisure traveller with a delayed bag. PR/FAQ topic: "Know where your bag is."

### Hypothesis 7: A booking flow redesign would not move conversion much
**Statement:** We believe that a full booking flow redesign would bring little gain, and that targeted fixes (fewer upsell steps, multi-city, payment reliability) address the real friction, because conversion is already above benchmark and complaints are low-severity.

**Evidence:**
- Conversion 3.08% to 3.17% against a 3.0% benchmark; 39 booking records with average rating 3.1; corporate say booking is fine. **[Known]**

**Confidence:** MEDIUM

**Test approach:**
- [ ] Measure drop-off by booking step.
- [ ] Method: funnel analysis and A/B tests of the upsell steps.
- [ ] Expected outcome: drop-off concentrates on one or two steps, not the whole flow.

**Connection to Working Backwards:** Persona: leisure web booker. PR/FAQ topic: a faster booking with fewer steps.

### Hypothesis 8 (team expectation 5, not settled): More summer agents would shorten waits but not reduce calls
**Statement:** We believe that more summer agents would cut hold times but would not change the number of rebooking calls per disrupted passenger, because the calls are caused by the missing self-service option, not by too few agents.

**Evidence:**
- Calls per 1,000 disrupted passengers stay between 401 and 424 every month; holds of 50 to 175 minutes. **[Known]**
- No staffing or wait-time data. **[Needs evidence]**

**Confidence:** LOW

**Test approach:**
- [ ] Get staffing levels and measured wait times by month from the call centre.
- [ ] Method: compare months with different staffing at similar disruption volumes.
- [ ] Expected outcome: wait times fall with staffing; calls per disrupted passenger do not.

**Connection to Working Backwards:** Persona: call centre agent (internal stakeholder). PR/FAQ topic: the FAQ "Why not just hire more agents?"

### Hypothesis 9 (team expectation 3, not settled): A better seat preview would raise upgrade sales
**Statement:** We believe that seat-upgrade sales are held back because customers cannot see the seat, and a richer preview would raise them.

**Evidence:**
- 15 requests for a 3D view, from satisfied customers; no upgrade revenue data. **[Assumed]**

**Confidence:** LOW

**Test approach:**
- [ ] Get upgrade attach rates by route and aircraft.
- [ ] Method: A/B test seat photos against today's seat map.
- [ ] Expected outcome: a measurable lift in paid seat selection.

**Connection to Working Backwards:** Persona: leisure traveller choosing a seat. PR/FAQ topic: "See your seat before you pay."

### Hypothesis 10 (team challenge 1): The booking flow loses shoppers the feedback cannot see
**Statement:** We believe that some shoppers abandon the booking flow at specific steps and book elsewhere, and that this loss is invisible in customer feedback, because only people who booked leave reviews and survey comments.

**Evidence:**
- No feedback from shoppers who abandoned; 1 record of a shopper leaving because the price rose. **[Known]**
- Conversion 3.08% to 3.17%, stable and above the 3.0% benchmark in the file; benchmark definition unknown. **[Known]** / **[Needs evidence]**

**Confidence:** LOW

**Test approach:**
- [ ] Measure drop-off by booking step from web analytics.
- [ ] Method: funnel analysis, plus a one-question exit survey on abandoned searches.
- [ ] Expected outcome if true: a large drop at one or more steps for reasons the flow controls (not price).

**Connection to Working Backwards:** Persona: shopper who did not book. PR/FAQ topic: none yet; informs the booking flow use case.

### Hypothesis 11 (team challenge 3): Some disrupted passengers will not self-serve, but many are helped by someone else
**Statement:** We believe that a share of disrupted passengers will never rebook in an app, and that many of them have someone who could do it for them (family, an assistant, an agency, a travel desk), because several callers are rebooking for another person.

**Evidence:**
- 1 record of passengers who cannot use the app; 2 about less technical customers; 2 assistants rebooking for a boss; agencies and travel desks asking to rebook in bulk. **[Known]**
- Share of disrupted passengers who would not self-serve: unknown. **[Needs evidence]**

**Confidence:** LOW

**Test approach:**
- [ ] Ask disrupted passengers who called why they did not use the app (survey question).
- [ ] Method: survey and call audit (tag calls made on someone else's behalf).
- [ ] Expected outcome: a minority say they cannot or will not use digital channels; a noticeable share of calls are on behalf of someone else.

**Connection to Working Backwards:** Persona: passenger who will not use the app; person rebooking for someone else. PR/FAQ topic: FAQ "What if I don't use the app?"
