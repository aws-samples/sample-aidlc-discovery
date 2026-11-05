# Risk review: self-service rebooking for disrupted passengers ("Choose My Flight")
Validate, 2026-10-29. Prototype reviewed: **v3**. Demonstration run on fictional sample data.

> **Reviewed, 2026-10-29.** Four risks reviewed (engineering lead confirmed feasible as open). Pre-mortem from the team's five reasons; warning signs and prevention drafted. Success criteria drafted; the proposed 30- and 60-day interim targets and criterion 3's 10% are not yet confirmed by the team. Decision recorded in `decision.md`.

## Re-walk of v3 (changed findings only)
| Finding | Persona | Fixed? | What the re-walk shows |
|---------|---------|--------|------------------------|
| 5 Dates inconsistent | Ingrid | Yes | Every screen says "Fri 30 Oct · 07:20"; the cancelled flight says "Thu 29 Oct" |
| 6 No ticket number | Ingrid | Yes | E-ticket number on "You're rebooked" |
| 1 Next-day flight, no hotel | Daniel, Helena | Yes, on screen | "Tonight: Hotel voucher issued" answers "where do we sleep" for passengers away from home. Daniel's family of four is still not shown (finding 7 waits) |
| 1 Next-day flight, no hotel | **Ingrid** | **New problem** | **Ingrid lives in Hamburg and is cancelled from Hamburg.** The screen issues her an airport hotel voucher she does not need; she would go home. An automatic voucher is wrong for passengers disrupted at their home airport, and adds hotel cost. Her persona's scenario says "go to the hotel", which conflicts with her home city; the team should say which is true for corporate travellers on their home leg. [Assumed] **Decided for the build (engineering lead, 2026-10-29): hotel vouchers only when the passenger is away from their home airport.** v3 still shows Ingrid a voucher in Hamburg. |
| 3 Where to find the booking reference | Helena's daughter | Yes | Hint names the confirmation email and the agency's document. Still no help if neither is to hand (finding 4, to Validate) |
| 8 "No seats left together" for one | Ingrid | Yes | "That flight has no seats left now." |
| 9 Call-back by hour | Daniel | Yes, as copy | Shows "within the hour" with the after-22:00 wording beneath it; the prototype does not switch by time. Whether "within the hour" holds at peak: open |

## Four risks
| Risk | Assumption | Evidence for | Evidence against | Verdict (draft) | Test to settle it |
|------|------------|--------------|------------------|-----------------|-------------------|
| **Valuable** | Disrupted passengers want to rebook themselves enough to stop calling | 118 of 400 records (30%) in all 6 sources; 37 ask to choose themselves; holds up to three hours; survey +4 (app) vs −58 (call centre); four corporate notes tie renewal or a tender to disruption [Known]. Personas: Ingrid 8, Daniel 7, daughter 8, Sofia 9 [synthetic] | Survey gap may partly be selection [Assumed]; Karim's desk 3 of 10: travel desks may still call to reconcile (finding 2); Helena alone 2 of 10 | **Supported** that passengers want it; **open** whether it removes calls (the riskiest assumption) | The 8 walk-throughs (head of digital, UX designer, 30-day); then the pilot's calls per 100 disrupted |
| **Usable** | Each persona completes the flow without help, in under three minutes | Every disrupted persona reached the boarding pass without help; Ingrid in three taps; v3 fixed findings 3, 5, 6, 8, 9 [synthetic] | Synthetic only; families not shown (finding 7); the daughter may not have the reference; Helena alone does not use it; the automatic hotel voucher is wrong at a home airport (re-walk) | **Open** | The 8 walk-throughs, timed, against "6 of 8 in under three minutes" |
| **Feasible** | There is a known path to build it with today's data, product, and platform | Alternatives already shown in the app and website; manage-booking already uses reference plus surname; no AI needed [Known] | Reissue and fare rules work reliably only through an agent today; 13 records of reissue errors and wrong fees [Known]. Unknowns: hotel vouchers without an agent; bags following the rebooking; "final" without an agent; seat availability current at confirm; contact details on agency bookings; security of reference plus surname for rebooking | **Open** until the reissue spike reports (engineering lead, 2026-10-29) | Reissue spike (engineering lead); voucher check (customer service operations lead); security review (engineering lead) |
| **Viable** | It works for the business | Corporate accounts ~1/3 of revenue with renewals tied to disruption; ~59,500 fewer calls (~36,700 agent hours) over the period if calls fall to 25 per 100 [Known / Assumed] | Revenue at risk not sized; hotel cost if vouchers are issued automatically, including to passengers who would go home; agency and travel-desk side not connected | **Open**, completed by the GTM viability check next | Revenue at risk (head of corporate accounts, 7-day); voucher policy and cost (customer service operations lead) |

## Riskiest assumption
Disrupted passengers offered real choices quickly will choose a flight themselves and need to call for nothing else: **open**. At the test moment, every synthetic persona chose and said it would not call to check, and v3 answers the hotel question for passengers away from home. But the thresholds need 8 real, recently disrupted passengers, and two second reasons to call remain unanswered on screen: the travel desk (finding 2) and whether the hotel is real without an agent.

## Pre-mortem
It is 90 days after launch, and Choose My Flight failed. Reasons named by the team, 2026-10-29; warning signs and prevention drafted for the team to confirm.

| # | Why it failed | Named by | Early warning sign | Prevention now |
|---|---------------|----------|--------------------|----------------|
| 1 | Passengers still called, for the hotel or to check, because the confirmation did not answer everything | Customer service operations lead | In the 8 walk-throughs: passengers name something they would still call about. In the pilot: self-service rebookers who call before their new flight leaves, tagged by reason | Ask every walk-through participant "what would you still call us about?"; tag pilot calls "after self-rebooking" with a reason; confirm vouchers can be issued without an agent before the pilot |
| 2 | Reissue failed on complex bookings and agents had to fix them by hand | Engineering lead | In the spike and internal use: reissue errors by booking type; fix-up rate above 2% | Spike covers complex bookings explicitly (mixed fares, groups, partner and agency bookings); pilot limited to single-passenger bookings; bookings the flow cannot reissue go to an agent with the booking loaded, not to an error |
| 3 | Travel desks did not see the change and called the airline anyway | Head of corporate accounts | Calls to the corporate line from travel desks or travel management companies about travellers who already rebooked | At the 7-day follow-up, ask the design partners what their desk sees after a traveller rebooks; decide whether the travel management company update (P2-1) moves up before the corporate pilot |
| 4 | The message arrived late, after the good flights were gone | Head of digital | Time from disruption to message; share of passengers who hit "no seats left" or find only far-off flights; chosen flight later than the airline's suggestion | **No PRD requirement sets when the message must arrive.** Add one (proposed: NF-8, a target time from disruption to message) and run the message audit by time of day (research hypothesis 5) [Needs evidence] |
| 5 | Passengers like Helena never used it, and the airport desk queues stayed the same | UX designer | Share of rebookings made "for someone else"; airport desk rebookings per 100 disrupted (not tracked today; 980 desk responses at −62) | Survey disrupted callers and desk users on why they did not use it (research hypothesis 11); start tracking desk rebookings as a measure; tell passengers and families "someone can rebook for you" in the disruption message and the text |

**Two more from the evidence, for the team to swap in or leave out:**
- **The one-route pilot did not predict the summer peak.** The data covers May to mid-October only, with no winter baseline; a pilot run in winter on one route may behave differently from June at double the disruptions. Warning sign: pilot passengers differ from the summer mix (corporate share, time of day). Prevention: pick the route and season so the pilot includes evening and corporate disruptions, and re-check the condition in the first summer weeks. [Assumed]
- **The seats shown were stale.** Passengers chose flights that had already filled, met "no seats left" more than once, and called. Overlaps with reason 4. Warning sign: seat-gone screens per rebooking. Prevention: part of the reissue spike (NF-3). [Assumed]

## Success criteria (draft, for the team to confirm)
Consistent with the North Star in `working-backwards.md`. The 30- and 60-day interim targets and criterion 3's 10% are **proposals, [Assumed]**, for the head of digital to set at the 30-day follow-up.

| # | Criterion | Metric | Baseline | Target | Checked at |
|---|-----------|--------|:--------:|:------:|------------|
| 1 | More disrupted passengers rebook themselves | Self-service rebooking rate, all disrupted passengers (agreed metric) | 12% | 35% (proposed interim: 20% at 30 days, 28% at 60) | 30, 60, 90 days |
| 2 | Fewer passengers phone to rebook | Rebooking calls per 100 disrupted passengers | 42 | 25 (proposed interim: 36 at 30 days, 30 at 60) | 30, 60, 90 days |
| 3 | Rebooking themselves leaves nothing to call about (riskiest assumption, live) | Share of self-service rebookers who call for any reason before their new flight leaves | Not measured | Proposed: 10% or less [Assumed] | 30, 90 days |
| 4 | It is quick enough to beat the phone | Median time from opening the message to a boarding pass | Not measured | Under 3 minutes (team target) | 30 days |
| 5 | Self-service rebookings are right first time | Self-service rebookings an agent has to fix | Not measured | Under 2% (PRD NF-4) | 30, 90 days |

The survey score for passengers who rebook online (at or above +4) stays in the GTM adoption table as a leading indicator.

## Pre-build condition (decided by the team, 2026-10-29; recorded in decision.md)
1. **Next 30 days:** the 8 walk-throughs with recently disrupted passengers, and the reissue spike.
2. **Gate 1:** at least 6 of 8 walk-throughs pass (choose without help, boarding pass in under three minutes, would not call for anything). This gates the pilot.
3. **Gate 2, one-route pilot:** Hamburg to Milan, for 4 weeks or 500 disrupted passengers, whichever comes first. At least 40% of disrupted passengers who see the options accept one with no call about that booking before departure.
4. **Then the full build.** The 35% of all disrupted passengers stays the 90-day target after full launch.
5. **Checked by** the head of digital at the 90-day follow-up (moved from 60 days, 2026-10-29). Before the pilot, the home-airport voucher rule must work (engineering lead, added to condition 2).

## Open hypotheses
| # | Question for the build | Verdict | Owner |
|---|------------------------|---------|-------|
| 1 | Do disrupted passengers choose a flight and need to call for nothing else? (riskiest assumption) | Open | Head of digital, UX designer (8 walk-throughs, 30-day); route pilot |
| 2 | Can reissue and fare rules work without an agent, including complex bookings; do bags follow; is the booking final? | Open | Engineering lead (reissue spike) |
| 3 | Can hotel vouchers be issued without an agent, and only for passengers away from their home airport? | Open | Customer service operations lead; home-airport rule for the build |
| 4 | Does a travel desk or travel management company see the change, or call to reconcile? | Open | Head of corporate accounts (7-day, design partners) |
| 5 | How soon after the disruption does the message arrive, and is that soon enough? | Open | Head of digital (message audit, research hypothesis 5) |
| 6 | Is booking reference plus surname safe enough to rebook for someone else; whose phone gets the text on agency bookings? | Open | Engineering lead, security review |
| 7 | How many disrupted passengers will never self-serve, and do desk queues fall? | Open | UX designer (research hypothesis 11) |
| 8 | Does a call-back "within the hour" hold at the summer peak? | Open | Customer service operations lead |
| 9 | How much corporate revenue is at risk? | Open | Head of corporate accounts (7-day) |

## Decision intent (stated 2026-10-29, not yet recorded in decision.md)
"Commit, but test the riskiest assumption first. Condition: on one route, at least 40% of disrupted passengers who see the options accept one without calling."
Open before it can be recorded: risk verdicts confirmed (engineering lead on feasible), pre-mortem, success criteria, GTM viability and adoption table, prototype version to hand off, and the condition's details (see the questions below), plus the roles deciding.

### Questions on the condition
1. A live route needs a working flow (reissue, vouchers), so it is a pilot of the build, not a test before it. Is the order: 8 walk-throughs → reissue spike → one-route pilot → full build?
2. Does the route pilot replace the 6-of-8 walk-through threshold, or come after it?
3. Denominator: "who see the options" differs from the agreed metric (all disrupted passengers, baseline 12%). Keep both?
4. "Without calling": within what window (for example, before departure or 24 hours), which route, how long or how many passengers, and who checks it by which follow-up?
