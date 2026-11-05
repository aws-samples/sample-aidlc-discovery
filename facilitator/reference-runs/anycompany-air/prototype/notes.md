# Prototype notes: Choose your flight (v2)
Open `index.html#/flow` (a copy of `v2.html`) in a browser. Versions side by side: `compare.html`. Visual direction: warm neutrals, serif headings, one blue accent (#1f5a8a). Scenario: [[amara]]'s family of four, 17:25 Munich → Lisbon cancelled at the gate.

## Screen plan (confirmed by the team default in the unattended run)
| # | Screen | What the persona sees and does | P0 |
|---|--------|-------------------------------|----|
| 1 | Alert on the trip | Cancelled banner, current automatic pick (Fri 10:15), "Choose a new flight" | Entry |
| 2 | Choose a flight | Chips (Keep us together ✓, Arrive by…, Fewest stops); recommended option with one-sentence reason (AI sample output); split option; not-enough-seats option (negative case); keep current | 1, 2 |
| 3 | Review and confirm | Four passengers and seats, what moves with you, live seats left, Confirm for all 4 or Contact us | 3 (**test moment**) |
| 4 | Confirmed | Four boarding passes, seats together, bags moved, old flight released, agency told | 4 |
| 5 | If it fails | Choice saved, current seats kept, call-back by 17:55 and a text | 5 |

## Screens
### Alert on the trip
Purpose: entry point from the disruption alert. Elements: trip card, cancelled pill, current automatic pick. Action: Choose a new flight.
### Choose a flight
Purpose: let the passenger pick. Elements: chips, four option cards with arrival, stops, seats left, together or split, what moves; the "Recommended for you" marker with "Keeps all four of you together and gets you home tonight." labeled as sample output from the first-draft prompt; "3 seats left, not enough for your group of 4". Actions: Choose, Keep this flight, Contact us. Desktop has its own table layout.
### Review and confirm
Purpose: the test moment. Elements: who travels with seats; what moves with you; "Your seats are secured when you confirm". Actions: Confirm for all 4; Contact us instead; a prototype-only link to the failure state.
### Confirmed
Purpose: proof of a valid change. Elements: four boarding passes, seats, bags, Fri 10:15 released, email and text, agency line.
### If it fails
Purpose: the unhappy path. Elements: saved choice, current seats kept, call-back time, text. Actions: back to trip; choose a different flight.

## Core flow
1. Alert → Choose a new flight
2. Choose a flight → Choose on "Tonight 19:50"
3. Review → Confirm for all 4
4. Confirmed
(Unhappy path: Review → prototype link → If it fails)

## Test moment
On **Review and confirm**: does the passenger tap Confirm for all 4 or Contact us instead? The journey step it is meant to change is `alternatives_viewed` → `contact_us_tapped`: 68 of every 100 alternatives viewers tap Contact us today. Known. The team expects personas and real users to confirm when seats, bags, and boarding passes are stated plainly, and to hesitate when any of them is unclear.

## Team click-through (unattended default)
- Engineering lead: "Bags move with you" promises what the reissue service fails at 835 times; keep it, but as Needs evidence.
- Customer service operations lead: a call-back "by 17:55" commits agents in peak hours; needs sizing.
- Head of corporate accounts: the confirmation should say the agency sees the change.
- UX designer: the recommended card is the clearest element on the screen; keep the marker visually lighter than the Choose button so it informs and does not decide.

## Questions for Validate (feasibility and compliance)
1. Can every offered alternative be confirmed without a fare rule rejection (3,985 FARE_RULE_MISMATCH)? Engineering lead.
2. Do seats and bags reliably move to the new ticket (835 EMD_NOT_REASSOCIATED)? Engineering lead.
3. Does an agency-booked ticket update on the agency's record (AGY-0013)? Engineering lead, head of corporate accounts.
4. Can the call-back promise be kept on a July day? Customer service operations lead.
5. Seat holding between Choose and Confirm: not in the prototype; open question for the build.
