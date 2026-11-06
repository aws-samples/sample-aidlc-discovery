# Risk review: self-service rebooking for disrupted passengers (Choose your flight)
Inputs checked: `prototype/index.html` (v2), `prototype/persona-critique.md`, `prototype/notes.md`, and every file in `working-backwards/`. All present. Unattended run: the engineering lead's and the operations lead's views are the defaults recorded in `prototype/notes.md`, not their confirmed answers.

## Re-walk of v2 (the findings the iteration changed)
| Finding | Persona | Did v2 fix it? |
|---------|---------|----------------|
| 1. Seats still there? | **[Persona: Amara]** "5 seats left, and it says they're secured when I confirm. I'd press Confirm now rather than call." **[Persona: Mei]** "Live count is what I need." | Fixed for the personas. Whether "seats left" can be shown current to the minute is Needs evidence |
| 2. Arrive by | **[Persona: Mei]** "'Arrive by…' is the chip I'd tap." | Fixed (the chip is shown; its time picker is not built in the prototype) |
| 3. What moves with you | **[Persona: Amara]** "Bags moved, boarding passes straight away: that's what I'd check." **[Persona: Mei]** "The 07:40 says seats need choosing again. Good, at least it's honest." | Fixed on screen; the promise depends on the reissue service (835 extras not moved) |
| 4. Agency told | **[Persona: Henrik]** "That line goes in my tender response, if it is true." | Fixed on screen; Needs evidence (AGY-0013) |
| 5. Text with call-back | **[Persona: Amara]** "A text while I'm boarding, yes." | Fixed on screen; call-back capacity Needs evidence |

## Four risks
| Risk | Assumption | Evidence for | Evidence against | Verdict | Test to settle it |
|------|-----------|--------------|------------------|---------|-------------------|
| **Valuable** | Disrupted passengers want to choose their own flight enough to stop calling | 116 of 400 records in every source and segment; 60% of alert openers already view alternatives; NPS app +4 vs call −58; three end-user personas would switch (day-one 6 to 9) | The self-service NPS gap may partly reflect who self-serves today (they kept a pick that suited them). Amara's late-arrival problem (getting home with children) is untouched | **Supported** | Pilot NPS of choosers vs callers |
| **Usable** | Each persona completes alert → choose → confirm without help, in under two minutes | All four personas completed the flow in v1; v2 removed the hesitations they named (seats, arrive by, what moves) | No real user has tried it. Passengers who do not use the app (SOC-0056 "They don't know how to use the app") and passengers who need assistance were not walked through | **Supported for the personas; open for real users** | 30-day test with 8 to 10 recently disrupted passengers, including one who rarely uses the app and one needing assistance |
| **Feasible** | Offered alternatives can be confirmed in self-service with seats and bags moved, reliably, in peak months | Alternatives (0 errors, p95 425 ms) and keep-suggestion (0.08% errors) exist in the product today | Reissue service rejects 5.0% (fare rules 3,985, ticket locked 1,092, extras 835, reservations timeouts 514), p95 about 2.6 s; agency-ticket changes unknown; seats-left freshness unknown; call-back capacity unknown | **Open** | Engineering spike: replay a month of offered alternatives through reissue; check agency-ticket changes; customer service operations lead sizes call-backs for a July day |
| **Viable** | It works for the business: retention and cost, no new charge | Free to passengers as changes after a cancellation already are; four corporate accounts tie renewal or tender to disruption; 146,299 rebooking calls averaging 38 minutes | Cost per call and the AI cost to serve are not known; call-backs move some agent work rather than remove it | **Supported** (cost figures open) | Customer service operations lead brings cost per call by the 7-day follow-up; engineering lead estimates AI cost per ranking |

## Riskiest assumption
*When disrupted passengers can see what each option means for them and choose one, most of them will confirm a new flight in the app themselves rather than tap Contact us.*
**Open.** At the test moment in v2, every persona chose Confirm over Contact us, and named what made them trust it (seats secured on confirm, bags shown, boarding passes straight away). They are synthetic personas, so this supports the design direction but is not customer evidence. The real-user test in the follow-up settles it.

## Pre-mortem
It is 90 days after launch and Choose your flight failed. Why?
| # | Why it failed | Early warning sign | Prevention now |
|---|---------------|--------------------|----------------|
| 1 | Passengers chose a flight, then called anyway "to make sure" | In the pilot, Contact us taps from the review or confirmation screen above 15%; calls per 1,000 disrupted not falling | Real-user test of the review screen before the pilot; boarding passes and text confirmation within seconds |
| 2 | Changes failed at reissue and passengers reached the gate with no valid ticket or no bag | Self-service changes ending without a valid ticket and extras above 1% | Reissue spike before the pilot; only offer alternatives the spike shows can be reissued; fallback with call-back |
| 3 | Call-backs overwhelmed agents on the first big July disruption | Call-back promises missed; hold times unchanged | Size call-back capacity with the customer service operations lead; cap call-backs and show the real wait |
| 4 | Alerts arrived 40 minutes late in peak months, and the good options were gone before passengers opened them | Seats left on the recommended option at open time falling in July vs June | Fix alert throttling (scoring candidate #6) before summer 2027 |
| 5 | Agency and corporate bookings could not use it, or travel desks rebooked travellers twice | Low use among corporate travellers; duplicate changes on agency records | Check agency-ticket changes in the spike; include one agency design partner in the pilot |

## Success criteria
| # | Criterion | Metric | Baseline | Target | Checked at |
|---|-----------|--------|----------|--------|------------|
| 1 | Fewer disrupted passengers leave for Contact us | Contact us taps ÷ alerts opened (RUM `contact_us_tapped` ÷ `alert_opened`) | 41% | 25% in the pilot group | 30 and 60 days after pilot start |
| 2 | Passengers who see options act on them | (choices confirmed + suggestions kept) ÷ alternatives viewed | 28% | 60% in the pilot group | 30 and 60 days after pilot start |
| 3 | The business metric moves | Self-service rebooking rate; rebooking calls per 1,000 disrupted passengers (operations-monthly) | 12.2%; 401 to 424 | 30%; 300 (North Star) | 90 days after general availability (end of September 2027) |
| 4 | Self-service changes are right first time | Changes that end with a valid ticket, seats, and bags ÷ changes confirmed | Needs evidence (reissue errors 5.0% for all changes today) | 99% | 30 days after pilot start |
| 5 | AI quality: the marker helps and never misleads | Reviewer acceptance on the 10 evaluation cases in the PRD | Not run | At least 9 of 10 typical and edge cases accepted; 0 negative cases pass | Before the pilot; again at 30 days on 50 real disruptions |

Criteria 1 and 2 are pilot targets on the journey measures, so the follow-ups read the same telemetry; criterion 3 is the North Star from `working-backwards/working-backwards.md`.

## Open hypotheses
1. Will real disrupted passengers confirm a self-made change without calling? (riskiest assumption)
2. Can every offered alternative be reissued without a fare rule rejection?
3. Do seats and bags reliably move to the new ticket?
4. Does an agency-booked ticket change show on the agency's record?
5. Can call-backs be kept on a peak July day, and at what cost per call?
6. Can "seats left" be shown current to the minute during a disruption?
7. Can passengers who rarely use the app, and passengers with assistance needs, complete the flow?
8. Does the self-service NPS gap (+4 vs −58) hold for passengers who choose rather than keep?
9. What is the AI cost per ranking, and does a recommendation marker raise or lower confirmation?
