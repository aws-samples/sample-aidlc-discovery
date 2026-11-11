# Discovery brief: Choose My Flight (working name): self-service rebooking for disrupted passengers

> **Demonstration run.** AnyCompany Air and its data are fictional sample material. This brief is a demonstration, not evidence for a build.

## 1. Engagement reference
Engagement reference: Self-serve | Date: 2026-10-29 | Route: AI-DLC workshop | Data: production (fictional sample)

## 2. Decision
**Commit, test the riskiest assumption first.** Decided by the head of digital, engineering lead, customer service operations lead, head of corporate accounts, and UX designer, 2026-10-29; to confirm with the commercial director at the readout.

**Reason (the team's words):** Disruption is the biggest and most painful problem in the data, and it is the metric we agreed. The personas chose and trusted v3, but only real passengers can show they won't call, and reissue is unproven.

**Conditions before the build:**
| # | Condition | Who checks | By when |
|---|-----------|------------|---------|
| 1 | At least 6 of 8 recently disrupted passengers choose a flight without help, reach a boarding pass in under three minutes, and say they would not call for anything. Gates the pilot | Head of digital, UX designer | 30-day follow-up |
| 2 | The reissue spike reports, including complex bookings; and the home-airport voucher rule works (hotel vouchers only when the passenger is away from their home airport) before the pilot | Engineering lead | 30-day follow-up |
| 3 | One-route pilot, Hamburg to Milan, 4 weeks or 500 disrupted passengers, whichever comes first: at least 40% of disrupted passengers who see the options accept one, with no call about that booking before departure | Head of digital | 90-day follow-up |

**Next:** walk-throughs and spike now; the pilot after both pass; the full build after the pilot. If a gate fails, the team decides pivot or park at that follow-up. After full launch, the 90-day targets in section 7 apply. Full decision: [decision.md](../validate/decision.md).

## 3. Problem and evidence
When a flight is cancelled or delayed by more than two hours, AnyCompany Air passengers can see alternative flights in the app and on the website but cannot choose one; the only action is "contact us". So they phone or queue for hours while the flights they could see fill up. Only 12.2% of 350,108 disrupted passengers (May to mid-October 2026) rebooked themselves; about 42 in 100 phoned.

| Signal | Freq. | Sev. | Reach | Score | Quote |
|--------|:-----:|:----:|:-----:|:-----:|-------|
| Disrupted passengers cannot rebook themselves: 118 of 400 records (30%), all 6 sources and 3 segments; 62% of agent handle time in the call sample; survey +4 (app) vs −58 (call centre) | 10 | 9 | 9 | 28 | "The delay wasn't the problem. Not being able to change my flight myself was." (leisure traveller, survey) |
| Passengers cannot see where a delayed bag is: 45 records | 6 | 6 | 5 | 17 | "The bag tag has a barcode, so somebody knows where it is. Why can't I?" (leisure traveller, review) |
| Booking flow friction, not broken: 39 records; conversion above benchmark | 5 | 3 | 6 | 14 | "Took me 12 minutes to book a simple return because of all the upsell pages." (leisure traveller, review) |
| Fares feel high to leisure travellers: 29 records | 4 | 4 | 5 | 13 | "Low-cost to Athens: 49 euros. AnyCompany Air: 149. Same airport." (leisure traveller, social) |
| Frequent flyers cannot trust points and status: 28 records | 4 | 4 | 3 | 11 | "Status expired with zero warning. Thanks for the loyalty." (frequent flyer, social) |

Full report: [signal-summary.md](../signals/signal-summary.md).

## 4. Target customers and personas
**Ingrid Halvorsen** is a regional sales director in Hamburg who flies for work every week on a corporate contract. She needs to reach her meeting, or home, on the best available flight with little lost time. Her main pain: she sees alternative flights but cannot move herself onto one, and waits an hour on hold while they fill up. Primary user. Confidence High.

**Daniel Okafor** is a secondary school teacher in Dublin who flies a few times a year on family holidays. He needs to get his family of four home together, on a flight that works, without losing a day. His main pain: a cancellation text at 23:00 when the phone line is closed, families split by rebooking, and hotel vouchers only through an agent. Confidence High.

**Helena Kowalska** is a retired pharmacist in Warsaw who flies to see her daughter and does not use the app. She needs to get home safely after a disruption, through a person or her daughter. Her main pain: the phone line is overloaded and nobody can rebook for her online. Confidence Low (second-hand evidence; added at the team's request).

**Karim Haddad** is the global travel manager of a pharmaceutical company with about 3,000 travellers. He needs to know where his travellers are during a disruption and get them rebooked fast. His main pain: his desk rebooks one traveller at a time by phone, with no visibility. Confidence Medium (heard through account managers and agencies).

**Sofia Lindqvist** is an architect in Porto who books in minutes, checks in on the app, and has never been disrupted. She needs a fast, predictable trip. Her main pain: none; she is the satisfied customer whose booking and check-in the build must not slow or clutter. Confidence High.

Full personas are in AI-DLC team knowledge and in [personas/](../working-backwards/personas/).

## 5. Prioritized use cases
Weights: pain 25, outcome 25, reach 15, fit 10, feasibility 15, adoption 10 (defaults, no sponsor shift).

| # | Use case | Weighted | Confidence | Decision |
|---|----------|:--------:|:----------:|----------|
| 1 | Disrupted passengers cannot choose their new flight | 4.60 | High | **Build first: this brief** |
| 2 | Leisure shoppers meet booking friction | 3.00 | Medium | Defer |
| 4 | Frequent flyers cannot trust points and status | 2.70 | Medium | Defer |
| 3 | Passengers cannot see where a delayed bag is | 2.55 | Medium | Defer |
| 5 | 3D seat map | — | — | Failed the gate (painkiller test) |

**Overrides:** #2 customer pain 2 → 4 (head of digital: "Our reviews mention it all the time"; reviews show 10 of 80 about booking, none blocking; severity Assumed). #1 feasibility 3 confirmed by the engineering lead (reissue and fare rules are the hard part). Full table: [use-case-scoring.md](../working-backwards/use-case-scoring.md).

## 6. PR/FAQ summary
**Headline:** Disrupted AnyCompany Air passengers can now choose their own new flight.

**Customer benefit:** when a flight is cancelled or delayed by more than two hours, the passenger, or someone they trust, keeps the airline's suggested flight or picks another in the app or on the website, and leaves with a reissued ticket and boarding pass in under three minutes, with nothing to pay.

**FAQ answers that most constrain the build:**
1. **Will it cost me anything?** No change fee or fare difference among the flights offered (confirmed disruption policy). Reissue reliability: Needs evidence (spike).
2. **The airline already moved me. Can I change it?** Yes: the automatic rebooking is shown as a suggestion the passenger keeps or replaces.
3. **I don't use the app. What can I do?** The phone and desk stay; someone with the booking reference and surname can rebook for you, as manage-booking works today. Security: Needs evidence.

Full PR/FAQ with readiness check (GREEN): [prfaq.md](../working-backwards/prfaq.md).

## 7. Success criteria
| # | Criterion | Metric | Baseline | Target | Checked at |
|---|-----------|--------|:--------:|:------:|------------|
| 1 | More disrupted passengers rebook themselves | Self-service rebooking rate, all disrupted passengers | 12% | 35% at 90 days after full launch (team commitment); 20% / 28% at 30 / 60 days [Assumed] | 30, 60, 90 days after launch |
| 2 | Fewer passengers phone to rebook | Rebooking calls per 100 disrupted passengers | 42 | 25 at 90 days (team commitment); 36 / 30 at 30 / 60 days [Assumed] | 30, 60, 90 days after launch |
| 3 | Rebooking themselves leaves nothing to call about | Share of self-service rebookers who call for any reason before departure | Not measured | 10% or less [Assumed] | 30, 90 days after launch |
| 4 | Quick enough to beat the phone | Median time from opening the message to a boarding pass | Not measured | Under 3 minutes (team target) | 30 days after launch |
| 5 | Right first time | Self-service rebookings an agent has to fix | Not measured | Under 2% [Assumed] | 30, 90 days after launch |

Pilot gate (before full launch): at least 40% of disrupted passengers on Hamburg to Milan who see the options accept one with no call before departure. The head of digital sets the Assumed interim targets at the 30-day follow-up.

## 8. GTM
- **First adopters:** corporate travellers on single-passenger bookings, the highest-value segment and over-represented in disruption records (40 of 118). Reached in the disruption message, through account managers briefing travel managers, and through their agencies. Design partners (roles): the software company account trialling a competitor; a large corporate account with a duty-of-care travel manager; one partner agency. Head of corporate accounts confirms by the 7-day follow-up.
- **Positioning:** For disrupted AnyCompany Air passengers who can see alternative flights but have to phone or queue to get onto one, Choose My Flight is a way to rebook in the app or on the website that gets them a boarding pass in under three minutes, at any hour, with nothing to pay. Unlike calling (up to three hours on hold) or accepting the flight the airline picked, it lets the passenger, or someone they trust, decide before the good flights fill up.
- **Viability check:**

| Area | Owner role | Main concern |
|------|------------|--------------|
| Legal and compliance | Head of digital, with legal | Passenger-rights obligations on rebooking and care when the passenger chooses; refund wording |
| Privacy and security | Engineering lead, with the security review | Booking reference plus surname to rebook for someone else; contact details on agency bookings |
| Sales | Head of corporate accounts | Renewal conversations; whether travel desks need an update before it helps renewals |
| Support and success | Customer service operations lead | "Is my self-chosen flight real?"; call-back within the hour at peak; hotel vouchers without an agent |
| Marketing | Head of digital | None for the pilot; at launch, "someone can rebook for you" |

- **Adoption and success:** owner head of digital (confirmed). Adoption metric: share of disrupted passengers who open the message and accept a flight. Leading indicators: time to boarding pass, calls after self-rebooking, seat-gone screens, rebookings for someone else, survey score at or above +4. Business metric: self-service rebooking rate, baseline 12%. Kill criteria [Assumed, set at 30-day]: walk-throughs below 6 of 8 or pilot below 40%: stop and decide pivot or park; after launch, below 20% at 60 days or more than 5% needing an agent fix.
- **Hypotheses with owners:** business model, free for every disrupted passenger, paid back by corporate retention and call centre time (head of digital, head of corporate accounts; revenue at risk sized by the 7-day follow-up). Launch plan: spike → walk-throughs → internal use by agents → design partners → Hamburg to Milan pilot → limited release → general availability, target June 2027 before the summer peak, held until the spike reports (head of digital).

Full GTM: [gtm.md](../working-backwards/gtm.md).

## 9. Scope
**In scope**
- Choosing a new flight from the disruption message, in the app, on the website, and by text or email (feature A).
- The airline's automatic rebooking shown as a suggestion to keep or replace (feature B).
- Rebooking on someone else's behalf with the booking reference and surname (feature C).
- Everyone on a booking moving together; no change fee or fare difference.
- For the pilot: hotel vouchers only for passengers away from their home airport; a call-back with the booking loaded when nothing works.

**Out of scope**
- Refunds and compensation beyond showing the existing refund route.
- Changes to bookings that are not disrupted.
- Booking flow, bag tracking, loyalty, seat map (deferred use cases).
- Replacing the call centre or airport desks.
- How reissue and fare rules work technically (the build decides).

## 10. Prioritized backlog
**P0**
- P0-1: The disruption message offers "choose your new flight" in the app, on the website, and by text or email.
- P0-2: The suggested flight, marked as a suggestion, and the other flights with seats.
- P0-3: Each option shows times, connections, whether everyone sits together, and that there is nothing to pay.
- P0-4: Keep the suggestion or replace it, and confirm.
- P0-5: Reissued ticket and new boarding pass, no change fee or fare difference.
- P0-6: Anyone with the booking reference and surname can make the change; the passenger gets a text.
- P0-7: Everyone on the booking moves together by default.

**P1**
- P1-1: When nothing works, a call-back with the booking loaded, and the refund route.
- P1-2: Hotel and meal help for next-day flights without calling, only away from the home airport (may move to P0 for next-day rebookings if the walk-throughs show calls for the hotel).
- P1-3: Travel desk view: see and rebook affected travellers in bulk within policy.
- P1-4: Groups and mixed fares on one booking.

**P2**
- P2-1: Disruption updates to travel management companies and agencies.
- P2-2: Choosing a different airport or date range.
- P2-3: Disruption reports for corporate accounts.

Non-functional requirements NF-1 to NF-8 (any hour, under 3 minutes, seats current at confirm, under 2% fix-up, accessible on a phone, human route kept, booking and check-in untouched, NF-8 message timing as an Assumed proposal) are in [prd.md](../working-backwards/prd.md).

## 11. Prototype screens and user flows
Chosen version: **v3** ([index.html](../prototype/index.html)). Mobile carries Ingrid's booking; Desktop carries Helena's booking, rebooked by her daughter.

**Screens**
1. **Disruption message.** Purpose: turn the cancellation into an action. Elements: cancelled flight, the suggested 07:20, "Keep the 07:20", "See all flights with seats", "Talk to us instead".
2. **Your options.** Purpose: compare. Elements: "Our suggestion" marked; other flights with times, connections, travellers together, €0.00; "None of these works for me". Desktop: Helena's booking, suggestion two days later, alternative tomorrow with two seats together, one "Seated apart".
3. **Check and confirm.** Purpose: show what changes. Elements: old flight struck through, new flight, traveller(s), seat, bag, €0.00; "Confirm this flight".
4. **You're rebooked (test moment).** Purpose: leave nothing to call about. Elements: ticket issued, e-ticket number, €0.00, bag moved, confirmation texted, "Tonight: Hotel voucher issued", "You don't need to call us for anything", boarding pass.
5. **Rebook for someone else.** Purpose: let someone act for the passenger. Elements: booking reference with a hint where to find it, surname, "Find their booking".
6. **The text Helena receives.** Purpose: tell a passenger without the app. Elements: new flight, seats together, "Your daughter changed this booking", hotel tonight, desk and time.
7. **Seat gone while choosing.** Purpose: the failure state. Elements: "That flight has no seats left now", nothing changed, next available flight.
8. **None of these works.** Purpose: a human route without repeating the story. Elements: call-back "within the hour" while the line is open 07:00 to 22:00, "when the line opens at 07:00" after 22:00; refund instead.

**Core flow**
1. Ingrid: disruption message → "Keep the 07:20" (or options) → check and confirm → you're rebooked.
2. Helena's daughter: rebook for someone else → options (keeps the two together) → check and confirm → you're rebooked → Helena's text.
3. Unhappy: options → seat gone → options; options → none of these works.

**Evolution:** v1 first build from the confirmed plan; v2 removed an "at any hour" call-back the line cannot keep; v3 fixed the persona critique's findings (hotel voucher, e-ticket number, matching dates, booking reference hint, wording, call-back by hour). **Known gap:** v3 issues Ingrid a hotel voucher at her home airport; the rule for the build is vouchers only away from home. See [versions.md](../prototype/versions.md).

## 12. Current product
No codebase was analyzed; no current-product map exists. From the signals: the AnyCompany Air app and website already handle booking and check-in well, already show disruption and alternative flights as information, and offer manage-booking with booking reference plus surname. Rebooking after a disruption works only through an agent or an airport desk.

## 13. Constraints
- The phone line and airport desks stay; nothing removes a human route.
- The phone line is open 07:00 to 22:00.
- No change fee or fare difference among the flights offered after a disruption (policy).
- Hotel vouchers only when the passenger is away from their home airport.
- Booking reference plus surname is today's manage-booking rule, subject to a security review for rebooking.
- Booking and check-in must keep their current speed and layout.
- No delivery date until the reissue spike reports; target June 2027, before the summer peak.

## 14. Open hypotheses and assumptions
1. **Riskiest assumption (open):** do disrupted passengers offered real choices quickly choose a flight themselves and need to call for nothing else, not to check and not for a hotel? (walk-throughs, then pilot)
2. Can reissue and fare rules work without an agent, including complex bookings; do bags follow; is the booking final? (engineering lead)
3. Can hotel vouchers be issued without an agent, only away from the home airport, and how is the home airport known? (customer service operations lead, engineering lead)
4. Does a travel desk or travel management company see the change, or call to reconcile? (head of corporate accounts)
5. How soon after the disruption must the message arrive (NF-8, Assumed)? (head of digital, message audit)
6. Is booking reference plus surname safe enough to rebook for someone else; whose phone gets the text on agency bookings? (security review)
7. How many disrupted passengers will never self-serve, and do desk queues fall? (UX designer)
8. Does a call-back within the hour hold at the summer peak? (customer service operations lead)
9. How much corporate revenue is at risk? (head of corporate accounts)
10. Is part of the +4 vs −58 survey gap selection, with harder cases calling? (research hypothesis 2)
11. Will one route over 4 weeks predict the summer peak, with no winter baseline in the data?
12. Assumed targets: interim 30- and 60-day targets, the 10% call-after-rebooking target, the kill criteria, and NF-8 (set by the head of digital at the 30-day follow-up).

**Top pre-mortem risks and early warning signs**
| Why it failed | Early warning sign |
|---------------|--------------------|
| Passengers still called, for the hotel or to check | Walk-through participants name something they would still call about; pilot calls after self-rebooking |
| Reissue failed on complex bookings; agents fixed them by hand | Reissue errors by booking type; fix-up rate above 2% |
| Travel desks did not see the change and called anyway | Corporate-line calls about travellers who already rebooked |
| The message arrived after the good flights were gone | Time from disruption to message; "no seats left" screens |
| Passengers like Helena never used it; desk queues stayed | Few rebookings for someone else; desk rebookings per 100 disrupted |

## 15. Full artifacts
- [PROJECT.md](../PROJECT.md)
- Signals: [team-expectations.md](../signals/team-expectations.md), [signal-summary.md](../signals/signal-summary.md), [hypotheses.md](../signals/hypotheses.md)
- Personas: [daniel.md](../working-backwards/personas/daniel.md), [helena.md](../working-backwards/personas/helena.md), [ingrid.md](../working-backwards/personas/ingrid.md), [karim.md](../working-backwards/personas/karim.md), [sofia.md](../working-backwards/personas/sofia.md)
- Working Backwards: [use-case-scoring.md](../working-backwards/use-case-scoring.md), [working-backwards.md](../working-backwards/working-backwards.md), [feature-description.md](../working-backwards/feature-description.md), [prfaq.md](../working-backwards/prfaq.md), [prd.md](../working-backwards/prd.md), [riskiest-assumption.md](../working-backwards/riskiest-assumption.md), [gtm.md](../working-backwards/gtm.md)
- Prototype: [index.html](../prototype/index.html) (v3), [v1.html](../prototype/v1.html), [v2.html](../prototype/v2.html), [v3.html](../prototype/v3.html), [compare.html](../prototype/compare.html), [versions.md](../prototype/versions.md), [notes.md](../prototype/notes.md), [persona-critique.md](../prototype/persona-critique.md)
- Validate: [risk-review.md](../validate/risk-review.md), [prioritization.md](../validate/prioritization.md), [decision.md](../validate/decision.md)
- Handoff: [next-steps.md](next-steps.md)
