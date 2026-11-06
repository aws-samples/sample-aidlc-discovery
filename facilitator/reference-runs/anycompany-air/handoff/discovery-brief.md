# Discovery brief: Choose your flight (self-service rebooking for disrupted passengers)

> Demonstration run: unattended, on the bundled fictional AnyCompany Air sample data. This brief shows what the workshop produces; it is not evidence for a build.

## 1. Engagement reference
Engagement reference: E2E-air | Date: 2026-10-30 | Route: AI-DLC workshop | Data: production

## 2. Decision
**Commit, testing the riskiest assumption first.** Disrupted passengers who cannot choose their own new flight is the top problem in every source and segment. It is the business metric itself, and the telemetry shows passengers reach the alternatives and stop only because they cannot act on them. The prototype held up in the persona critique, but that evidence is synthetic, and feasibility depends on the ticket reissue service.

**Conditions before the build starts:**
1. At least 7 of 10 recently disrupted passengers confirm a new flight in prototype v2 without tapping Contact us, including one who rarely uses the app. Checked by: UX designer with the head of digital, by the 30-day follow-up.
2. A replay of one month of offered alternatives through ticket reissue shows at least 99% can be confirmed with seats and bags moved, or names the cases that go to the call-back fallback. Checked by: engineering lead, by the 30-day follow-up.
3. Call-back capacity for a peak July day is sized, with a cost per call. Checked by: customer service operations lead; cost per call by the 7-day follow-up, capacity by the 30-day follow-up.

**Next:** real-user test and reissue spike; prepare the alert fix (next in line) for summer 2027; brief three design partners. Full decision: [validate/decision.md](../validate/decision.md).

## 3. Problem and evidence
When a flight is cancelled or delayed by more than two hours, passengers can see other flights in the app and on the website but cannot choose one. They keep the flight the airline picked, or they call or queue. Between May and mid-October 2026, 350,108 passengers were disrupted and 12.2% rebooked themselves. There were 146,299 rebooking calls, averaging 38 minutes. Known.

| Signal | Freq. | Sev. | Reach | Total | Quote |
|--------|:-----:|:----:|:-----:|:-----:|-------|
| Disrupted passengers cannot choose their own new flight: 116 of 400 records, all 6 sources; 60% of alert openers view alternatives, 17% keep the pick, 41% tap Contact us | 10 | 10 | 9 | 29 | "Delays happen, I get it. What I don't get is why I can see alternative flights on the website but can't move myself onto one." (app review, corporate) |
| Disruption alerts arrive late in peak months and lead nowhere: p95 delay about 11 min, about 41 min in July and August | 6 | 8 | 8 | 22 | "Delay notification at 10:30, then nothing. No new times, no options, no humans." (social) |
| Delayed and lost bags cannot be tracked: 45 records | 7 | 7 | 5 | 19 | "The bag tag has a barcode, so somebody knows where it is. Why can't I?" (Google Play) |
| Price feels high next to low-cost carriers: 36 records, low severity | 6 | 3 | 7 | 16 | "Love the airline, hate the prices" (social) |
| Booking flow friction: 43 mild records; conversion 3.1% vs 3.0% benchmark, flat | 6 | 3 | 6 | 15 | "Took me 12 minutes to book a simple return because of all the upsell pages." (app review) |
| Loyalty points and status confusing: 27 records | 5 | 4 | 3 | 12 | "Loyalty app shows 3700 points, website shows something else" (social) |
| 3D seat map request: 16 records, all wishes | 3 | 1 | 3 | 7 | "Seat map is fine. A 3D view would be a nice touch like some other airlines have." (app review) |

The data contradicted the team's beliefs that the booking flow, price, or staffing is the main problem. Full report: [signals/signal-summary.md](../signals/signal-summary.md).

## 4. Target customers and personas
**Amara Okafor** is a parent who flies with her family two or three times a year and books in the app (end user, HIGH confidence, 43 items). When a flight is cancelled at the gate she needs a new flight that keeps all four of them together and still gets them home. Her main pain: automatic rebooking that splits the family or moves them days later, and hours on hold while the good flights fill up.

**Mei Tanaka** is a solutions consultant who flies for work every week on a corporate contract (end user, HIGH, 73 items). After a disruption she needs the flight that makes her meeting, with her seat and bag intact, within minutes. Her main pain: the app shows alternatives and says "call us"; she calls immediately "before the good flights fill up".

**Henrik Sørensen** is a global travel manager for about 3,000 travellers at a pharmaceutical company (buyer, MEDIUM, 22 items). He renews the airline on how it handles disruption and needs travellers rebooked fast and visible to his desk. His main pain: average time to rebook over two hours, and no visibility for duty of care.

**Jonas Becker** is a junior architect and loyalty member who flies monthly and has never needed the call centre (satisfied end user, HIGH, 56 items). His job is to book and fly with as little effort as possible. He has no pain today; his normal trip screen must not change.

Full personas are in AI-DLC team knowledge: `aidlc/spaces/default/knowledge/aidlc-product-agent/discovery-personas.md`.

## 5. Prioritized use cases
Weights: pain 25, outcome 25, reach 15, fit 10, feasibility 15, adoption 10. Business metric: self-service rebooking rate, 12%.

| # | Use case | Weighted | Confidence | Decision |
|---|----------|:--------:|------------|----------|
| 1 | Disrupted passengers cannot choose a new flight themselves | **4.60** | High | **Build first: this brief** |
| 6 | Disruption alerts arrive late and give nothing to act on (From Signals) | 4.00 | Medium | Defer, next in line |
| 7 | Travel desks and agencies cannot see or rebook disrupted travellers (From Signals) | 3.15 | Medium | Defer |
| 3 | Delayed or lost bags cannot be tracked | 2.55 | Medium | Defer |
| 2 | Booking flow redesign | 2.45 | High | Drop |
| 4 | Loyalty points visibility | 2.35 | Medium | Drop |
| 5 | 3D seat map | – | – | Failed the gate (painkiller) |

Overrides: none (unattended run). Re-score after Validate considered for #1 feasibility, unchanged at 3. Full scoring: [working-backwards/use-case-scoring.md](../working-backwards/use-case-scoring.md).

## 6. PR/FAQ summary
**Headline:** Disrupted AnyCompany Air passengers can now choose their own new flight in minutes.
**Customer benefit:** passengers pick and confirm a new flight for everyone on the booking in the app or on the website, with seats and bags carried over, without waiting for an agent.

FAQ answers that most constrain the build:
- **Will my family stay together, and will my seats and bags move?** The choice applies to everyone on the booking; each option shows before confirming whether they stay together and whether seats and bags move. Needs evidence: 835 changes today fail to move extras.
- **What if the change fails?** The choice is saved and an agent calls back to complete it, with a text. Assumed: call-back capacity not yet sized.
- **How does it decide which flight to mark?** It compares the options with what the passenger said matters and marks the closest match with one sentence. It never books. Assumed.

Full PR/FAQ with readiness check (AMBER, two gaps): [working-backwards/prfaq.md](../working-backwards/prfaq.md).

## 7. Success criteria
| # | Criterion | Metric | Baseline | Target | Checked at |
|---|-----------|--------|----------|--------|------------|
| 1 | Fewer leave for Contact us | RUM `contact_us_tapped` ÷ `alert_opened` | 41% | 25% (pilot) | 30 and 60 days after pilot start |
| 2 | Passengers act on the options | (choices confirmed + suggestions kept) ÷ alternatives viewed | 28% | 60% (pilot) | 30 and 60 days after pilot start |
| 3 | Business metric | Self-service rebooking rate; rebooking calls per 1,000 disrupted | 12.2%; 401 to 424 | 30%; 300 (North Star) | 90 days after general availability (end of September 2027) |
| 4 | Right first time | Changes ending with a valid ticket, seats, and bags ÷ confirmed | Needs evidence | 99% | 30 days after pilot start |
| 5 | AI quality | Reviewer acceptance on the 10 evaluation cases in the PRD | Not run | ≥ 9 of 10 typical and edge accepted; 0 negative pass | Before the pilot; at 30 days on 50 real disruptions |

Evaluation cases: family of four kept together; arrive-by for a meeting; direct instead of a five-hour layover; tomorrow instead of 15 days later; onward connection; five passengers with no flight together (edge); wheelchair assistance with a tight connection (edge); conflicting priorities (edge); compensation question (negative); too few seats for the group (negative). See [working-backwards/prd.md](../working-backwards/prd.md) section 11.

## 8. GTM
- **First adopters:** corporate travellers and frequent flyers on routes with repeated summer disruption. Design partners (roles): the travel manager of a pharma account that sent a disruption report; the travel manager of a banking account whose Q1 renewal depends on disruption; a partner travel agency that asked for rebooking in its portal.
- **Positioning:** for disrupted passengers who can see other flights but have to call to change, Choose your flight is a self-service rebooking step that lets them choose and confirm a new flight for everyone on the booking in minutes. Unlike waiting on hold or accepting a flight that does not work, it puts the choice with the passenger and shows what moves with them before they confirm.
- **Viability check:** legal and compliance (head of digital with legal): wording must not steer passengers away from refunds; privacy (engineering lead): no names, contact, or payment data to the model; sales (head of corporate accounts): helps four at-risk renewals only if agency bookings are included; support (customer service operations lead): call-backs and "no boarding pass" questions; marketing (head of digital): tell the story only after the pilot.
- **Adoption and success:** owner head of digital; adoption metric (confirmed + kept) ÷ alternatives viewed, baseline 28%; targets 45% at 30 days and 60% at 60 days after pilot start; business metric 30% at 90 days after general availability. **Kill criteria:** at 60 days after pilot start, adoption below 40%, or Contact us per alert above 35%, or right-first-time below 97%.
- **Hypotheses with owners:** free to passengers; retention (head of corporate accounts) and call cost (customer service operations lead) to be quantified; AI cost per ranking (engineering lead). Launch: internal, design partners, 20% of disruptions on pilot routes, then all routes before July 2027.

Full section: [working-backwards/gtm.md](../working-backwards/gtm.md).

## 9. Scope
**In scope**
- Choosing and confirming an offered alternative for everyone on the booking, in the app and on the website.
- Live seats left, together or split, and what moves with the passenger (seats, bags, boarding passes).
- A "fits what matters to you" marker with a one-sentence reason (never books).
- A fallback with the choice saved, a call-back, and a text.
- Telling the agency or company booking that the change was made.

**Out of scope**
- Which alternatives the airline offers, and its disruption policy.
- Refunds, vouchers, and hotels in the app (P2).
- Travel desk and agency tools (deferred #7); alert timing (deferred #6).
- Booking flow, seat map, bag tracking, loyalty.

**AI feature block (a starting point for the build, which chooses the model, the data and retrieval design, and the final prompt):**
- *Job:* from the flights offered to a disrupted booking, mark the one that best fits what the passenger said matters and explain why in one sentence.
- *Tone:* calm, short sentences, plain words, no jargon.
- *Inputs:* disrupted flight and reason; number of passengers and needs; offered alternatives with times, stops, seats left together, and what moves; chosen priorities.
- *Output:* one option ID or "none", and one sentence of at most 20 words naming the priority.
- *Must not:* book; recommend an option with too few seats together; mention compensation, refunds, or policy; invent flights, times, or seats; compare with other airlines.
- *Evaluation cases:* the ten in section 7, in full in [working-backwards/prd.md](../working-backwards/prd.md).

## 10. Prioritized backlog
- **P0** Disruption screen with a Choose action on each alternative, showing arrival, stops, seats left, together or split, and what moves.
- **P0** "What matters to you" chips (keep us together, arrive by, fewest stops) and the best-match marker with one reason.
- **P0** Review and confirm for all passengers, with seats, bags, and fee.
- **P0** Confirmation with new boarding passes on the trip and the agency told.
- **P0** Fallback: choice saved, call-back, text.
- **P1** Keep the current pick on the same screen.
- **P1** Group-splitting option with per-passenger confirmation.
- **P1** Alert opens directly on the disruption screen.
- **P1** Accessibility, and special assistance carried to the new flight.
- **P2** Refund instead of a new flight, in the app.
- **P2** Hotel and meal vouchers in the app.
- **P2** Travel desk and agency view.

## 11. Prototype screens and user flows
Chosen version: **v2** ([prototype/index.html](../prototype/index.html), same as [v2.html](../prototype/v2.html)). Scenario: a family of four, 17:25 Munich → Lisbon cancelled at the gate.

1. **Alert on the trip.** Purpose: entry from the disruption alert. Elements: trip card, Cancelled pill, the automatic pick (Fri 10:15). Action: Choose a new flight.
2. **Choose a flight.** Purpose: let the passenger pick. Elements: chips; four options with arrival, stops, live seats left, together or split, what moves; "Recommended for you" with "Keeps all four of you together and gets you home tonight." (sample output from the first-draft prompt); "3 seats left, not enough for your group of 4" (negative case). Actions: Choose, Keep this flight, Contact us. The desktop view has its own table.
3. **Review and confirm (test moment).** Purpose: the moment the passenger decides to confirm or call. Elements: four passengers with seats, what moves with you, "Your seats are secured when you confirm". Actions: Confirm for all 4; Contact us instead.
4. **Confirmed.** Purpose: proof of a valid change. Elements: four boarding passes, seats together, bags moved, old flight released, email and text, agency line.
5. **If it fails.** Purpose: the unhappy path. Elements: saved choice, current seats kept, call-back time, text. Actions: back to trip; choose a different flight.

**Core flow:** 1. Alert → 2. Choose "Tonight 19:50" → 3. Confirm for all 4 → 4. Confirmed. Unhappy path: 3 → 5.

**How the versions evolved:** v1 was built from the screen plan. In v2 the persona critique added live seats left, an "Arrive by…" chip, an honest "what moves with you", an agency line, a text with the call-back, and removed "See my options later". Details in [prototype/versions.md](../prototype/versions.md); side by side in [prototype/compare.html](../prototype/compare.html). No in-codebase prototype.

## 12. Current product
Greenfield: no existing codebase in this folder. From the telemetry, the product today already has the disruption alert, the trip view, a read-only alternatives view, a keep-suggestion action, and a Contact us step. Known.

## 13. Constraints
- Summer peak: July and August have almost twice the disrupted passengers of other months; the feature has to be live and sized before July 2027.
- A corporate tender in February 2027 asks for a written disruption plan.
- Changes to a ticket after a disruption go through the existing reissue and reservations systems; the engineering lead is cautious about anything that changes bookings after they are made.
- Agency-booked tickets must be handled, or corporate travellers are excluded.
- Passenger rights after cancellations: the wording must not steer passengers away from refunds (legal review).
- Changing to an offered flight after a disruption stays free.

## 14. Open hypotheses and assumptions
1. **Riskiest assumption (open):** will real disrupted passengers confirm a self-made change without calling to check?
2. Can every offered alternative be reissued without a fare rule rejection (3,985 today)?
3. Do seats and bags reliably move to the new ticket (835 failures today)?
4. Does an agency-booked ticket change show on the agency's record?
5. Can call-backs be kept on a peak July day, and what does a call cost?
6. Can "seats left" be shown current to the minute in a disruption?
7. Can passengers who rarely use the app, and passengers needing assistance, complete the flow?
8. Does the self-service NPS gap (+4 vs −58) hold for passengers who choose rather than keep?
9. What is the AI cost per ranking, and does the marker raise or lower confirmation?
10. Is 30% self-service rebooking reachable in one summer (about 55% of today's non-keeping alternatives views)? Assumed.
11. Does better disruption handling change renewal outcomes for the accounts that tied renewal to it?

**Top pre-mortem risks, as questions for the build:**
- Will passengers call anyway "to make sure"? Early warning: Contact us from review or confirmation above 15%.
- Will reissue failures leave passengers without a valid ticket? Early warning: right-first-time below 99%.
- Will call-backs overwhelm agents in July? Early warning: call-back promises missed.
- Will late peak-month alerts mean the good options are gone? Early warning: fewer seats left on the recommended option at open time in July.
- Will agency bookings be excluded or rebooked twice? Early warning: low corporate use; duplicate changes.

## 15. Full artifacts
- [PROJECT.md](../PROJECT.md)
- [signals/team-hypotheses.md](../signals/team-hypotheses.md)
- [signals/signal-summary.md](../signals/signal-summary.md)
- [signals/hypotheses.md](../signals/hypotheses.md)
- [working-backwards/personas/amara.md](../working-backwards/personas/amara.md)
- [working-backwards/personas/mei.md](../working-backwards/personas/mei.md)
- [working-backwards/personas/henrik.md](../working-backwards/personas/henrik.md)
- [working-backwards/personas/jonas.md](../working-backwards/personas/jonas.md)
- [working-backwards/use-case-scoring.md](../working-backwards/use-case-scoring.md)
- [working-backwards/working-backwards.md](../working-backwards/working-backwards.md)
- [working-backwards/feature-description.md](../working-backwards/feature-description.md)
- [working-backwards/prfaq.md](../working-backwards/prfaq.md)
- [working-backwards/prd.md](../working-backwards/prd.md)
- [working-backwards/gtm.md](../working-backwards/gtm.md)
- [working-backwards/riskiest-assumption.md](../working-backwards/riskiest-assumption.md)
- [prototype/index.html](../prototype/index.html), [v1.html](../prototype/v1.html), [v2.html](../prototype/v2.html), [compare.html](../prototype/compare.html)
- [prototype/versions.md](../prototype/versions.md)
- [prototype/notes.md](../prototype/notes.md)
- [prototype/persona-critique.md](../prototype/persona-critique.md)
- [validate/risk-review.md](../validate/risk-review.md)
- [validate/prioritization.md](../validate/prioritization.md)
- [validate/decision.md](../validate/decision.md)
- [handoff/next-steps.md](next-steps.md)
