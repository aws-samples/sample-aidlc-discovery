# PRD: Choose your flight
Demonstration run on fictional sample data. Unattended draft for the team to challenge. No architecture or technology choices: those belong to the build.

## 1. Executive Summary
Disrupted passengers can see other flights in the app and on the website but cannot choose one; 41% of those who open a disruption alert tap Contact us, and only 12% rebook themselves. Known. Choose your flight lets them choose and confirm a new flight for everyone on the booking, with seats and bags carried over, and marks the option that best fits what they say matters. Target: self-service rebooking rate from 12% to 30%, and rebooking calls from about 415 to 300 per 1,000 disrupted passengers, June to September 2027. Assumed (North Star).

## 2. Problem Statement
Today, disrupted passengers have to wait on the phone or in a desk queue to change a flight they can already see in the app. Known: 150,845 alternatives views; 102,456 Contact us taps; 146,299 rebooking calls averaging 38 minutes; call centre NPS −58 against +4 for self-service in the app. The alternatives screen is read-only, the automatic pick often does not fit (days later, long layovers, families split), and the call centre is the only fallback. Known (journey map, 7+ records).

## 3. Goals & Success Metrics
| Metric | Baseline | Target | Source |
|--------|----------|--------|--------|
| Self-service rebooking rate | 12.2% (May to mid-Oct 2026) | 30% (Jun to Sep 2027) | operations-monthly |
| Rebooking calls per 1,000 disrupted passengers | 401 to 424 | 300 | operations-monthly |
| Alternatives viewers who confirm a choice or keep the pick | 28% | 60% (pilot) | RUM disruption journey |
| Contact us taps per alert opened | 41% | 25% (pilot) | RUM disruption journey |
| NPS of disrupted passengers who self-serve | +4 app, −2 web | at or above 0 | disruption NPS by channel |
| Self-service changes that end with a valid ticket and extras | Needs evidence | 99% | reissue outcomes |

Baselines Known; targets Assumed.

## 4. User Personas
- **[[amara]]**, leisure parent, end user: needs everyone together on a flight that still works. HIGH confidence.
- **[[mei]]**, weekly corporate traveller, end user: needs the flight that makes the meeting, with seat and bag intact. HIGH.
- **[[henrik]]**, travel manager, buyer: judges time to rebook and visibility. MEDIUM.
- **[[jonas]]**, satisfied regular: his normal trip screen must not change. HIGH.

## 5. Requirements

### Functional Requirements
**P0 (the prototype, about one hour)**
1. **Disruption screen with choice.** Shows the current automatic pick and two to four alternatives, each with departure, arrival, stops, seats left, whether everyone stays together, and whether seats and bags move. Each alternative has a Choose action.
2. **What matters to you.** Three optional chips (arrive by a time, keep us together, fewest stops). The best-matching option is marked with one sentence on why. The marker never books.
3. **Review and confirm.** After Choose: who travels, the new flight, seats, bags, and a single Confirm for all passengers.
4. **Confirmation.** New flight and boarding passes on the trip; "your travel agency has been informed" when the booking came from one.
5. **Fallback.** If the change cannot be completed: the choice is saved and a call-back is booked, with an expected time.

**P1**
6. Keep the current pick in one tap (exists today) on the same screen.
7. Option that splits the group is shown, marked, and asks for confirmation per passenger.
8. Alert opens directly on the disruption screen.
9. Accessibility: options readable by screen readers; passengers needing special assistance keep it on the new flight.

**P2**
10. Refund instead of a new flight, in the app.
11. Hotel and meal vouchers in the app.
12. Travel desk and agency view (deferred candidate #7).

### Non-Functional Requirements
- From opening the alert to confirmed in under two minutes for a typical passenger. Assumed.
- Seats left must be current to the minute during a disruption. Assumed.
- Works in peak months: twice the disrupted passengers of normal months (July 90,752). Known.
- The normal trip screen is unchanged when there is no disruption ([[jonas]]).

## 6. User Stories & Acceptance Criteria
| Story | Acceptance criteria |
|-------|--------------------|
| As Amara, I want to pick the evening flight for all four of us | Given a cancelled booking with 4 passengers, when she chooses an alternative with 4 seats left, then the review shows all four names, seated together, and Confirm moves all four |
| As Amara, I want to know before I confirm that we stay together | Options without enough seats together are marked "splits your group" before Choose |
| As Mei, I want the flight that makes my meeting | With "arrive by 13:30" chosen, the option arriving 12:40 is marked with a one-sentence reason; later options are not marked |
| As Mei, I want my seat and bag to move | The review shows seat and bag status per option; if extras cannot move, it says so before Confirm |
| As any passenger, I want a safe way out if it fails | If the change fails, the screen shows the saved choice and a call-back time; no restart |
| As Jonas, I want my normal trip unchanged | With no disruption, the trip screen shows no new elements |

## 7. Out of Scope and non-goals
- Which alternatives the airline offers, and its disruption policy.
- Refunds, vouchers, hotels (P2).
- Booking flow, seat map, bag tracking, loyalty.
- Making decisions for the passenger: the marker recommends, the passenger chooses.

## 8. Dependencies & Risks
| Item | Type | Evidence | Mitigation |
|------|------|----------|------------|
| Ticket reissue rejects 5.0% of changes (fare rules 3,985, locked 1,092, extras 835, timeouts 514) | Dependency | Known (errors-top) | Engineering spike; fallback with call-back (P0 #5) |
| Passengers do not trust a self-made change and call anyway | Risk | Assumed | Riskiest assumption; prototype test moment |
| Call-back capacity in peak months | Dependency | Needs evidence | Size with the customer service operations lead |
| Agency-booked tickets can be changed in self-service | Dependency | Needs evidence (AGY-0013) | Engineering lead to confirm |
| Recommendation misses what matters | Risk | Assumed | Evaluation cases below |

## 9. Timeline Considerations
- 30 days: real-user test of the prototype with 8 to 10 recently disrupted passengers and three travel managers; reissue spike.
- Before June 2027: pilot on selected routes. Summer peak starts in July. Known.
- February 2027: a corporate tender asks for a written disruption plan. Known (ACC-0020).

## 10. AI feature checklist
The "fits what matters to you" marker uses a model to rank the offered options and write one sentence on why.
- **Guardrails:** never books or confirms; never recommends a flight with fewer seats than passengers; never promises compensation, refunds, vouchers, or policy; never invents a flight, time, or seat; says plainly when no option fits.
- **Evaluations:** the cases in the AI feature block; target: a reviewer accepts at least 9 of 10 typical cases, and no negative case passes.
- **Privacy:** uses the disrupted booking, passenger count and needs (for example assistance), the offered flights, and the chips the passenger chose. No names, contact details, or payment data go to the model. Needs evidence: where data is processed is for the build.
- **Cost to serve:** one ranking per disrupted booking that opens the screen: about 150,000 per half-year at today's volume. Cost per active user per month Needs evidence in the build.

## 11. AI feature block

### First-draft prompt
**Job:** From the flights offered to this disrupted booking, mark the one that best fits what the passenger said matters, and explain why in one sentence.
**Tone:** calm, short sentences, plain words, no apology formulas, no jargon ("fare basis", "PNR").
**Inputs:** the disrupted flight and reason; number of passengers and any needs (child, assistance); the offered alternatives with departure, arrival, stops, seats left together, and whether seats and bags move; the chips chosen (arrive by [time], keep us together, fewest stops), or none.
**Output format:** the ID of one recommended option, or "none"; one sentence of at most 20 words on why, naming the passenger's priority; if none fits, one sentence saying which priority cannot be met.
**Must not:** book or confirm; recommend an option with fewer seats together than passengers when "keep us together" is chosen; mention compensation, refunds, vouchers, or policy; invent flights, times, or seats; compare with other airlines.

### Evaluation cases
| # | Type | Input (the situation) | A good output | From |
|---|------|-----------------------|---------------|------|
| 1 | Typical | Family of 4, cancelled 17:25; options: in 2 days direct, tonight via another city (4 together), tomorrow 07:40 (2+2). Chip: keep us together | Tonight via the other city: "Keeps all four of you together and gets you home tonight." | [[amara]], REV-0069 |
| 2 | Typical | 1 passenger, missed connection; options arrive 12:40, 15:10, 18:30. Chip: arrive by 13:30 | 12:40: "The only option that lands before 13:30." | [[mei]], REV-0050 |
| 3 | Typical | 1 passenger, cancelled; auto pick has a five-hour layover; a direct flight 2 h later. Chip: fewest stops | Direct: "Direct, and you arrive earlier than with the layover." | CALL-0069, CALL-0077 |
| 4 | Typical | 1 passenger, auto pick 15 days later; options tomorrow 14:40 with a connection, day after direct. No chip | Tomorrow 14:40: "Gets you there tomorrow, 14 days sooner than your current flight." | CALL-0107, SOC-0051 |
| 5 | Typical | 2 passengers, delay means missing the onward train; earlier flight 14:40 with 2 seats. Chip: arrive by 16:00 | 14:40: "Lands in time for your onward connection at 16:00." | CALL-0041 |
| 6 | Edge | 5 passengers; no single flight has 5 seats together today. Chip: keep us together | None: "No flight today keeps all five of you together; tomorrow 07:40 does." (marks 07:40 if offered) | CALL-0020 |
| 7 | Edge | 1 passenger with wheelchair assistance; options with tight connection (35 min) and longer (1 h 50). Chip: arrive by 18:00, both qualify | Longer connection: "Arrives before 18:00 with time for your assistance at the connection." | CALL-0058, CALL-0089 |
| 8 | Edge | Chips conflict: arrive by 09:00 and fewest stops; only a one-stop option arrives in time | One-stop: "The only option before 09:00; it has one stop." | [[mei]] |
| 9 | Negative | Passenger chip none, typed note asks "will I get compensation?" | Marks by arrival time only; sentence does not mention compensation | CALL-0055, guardrail |
| 10 | Negative | Best option by time shows 3 seats; booking has 4 passengers; chip: keep us together | Must not mark it; marks the next option with 4 together, or none | Guardrail |

### Sample outputs for the prototype (Assumed: not run on a model)
- Case 1 (typical): **Recommended for you** · "Keeps all four of you together and gets you home tonight."
- Case 2 (typical): **Recommended for you** · "The only option that lands before 13:30."
- Case 6 (edge): **No flight today fits** · "No flight today keeps all five of you together; tomorrow 07:40 does."
- Case 10 (negative): the 3-seat option shows no marker and reads "3 seats left, not enough for your group of 4."

## Writing audit
Checked voice, banned words, em dashes, scope of claims, and the North Star numbers against `working-backwards.md`. Changed: "seamless" removed from the non-functional requirements; the agency dependency scoped to one escalation.
