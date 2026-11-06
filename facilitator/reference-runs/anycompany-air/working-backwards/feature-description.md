# Feature: Choose your flight

## Feature proposals considered
1. **Choose from alternatives** — Add a Choose action to the existing alternatives screen, for everyone on the booking. Addresses: root cause 1 (read-only screen).
2. **Recommended for you** — The head of digital's idea: the passenger says what matters and an assistant recommends the best new flight with a one-sentence reason. Addresses: root cause 2 (automatic pick ignores what matters).
3. **Earlier, actionable alerts** — Alerts that arrive within minutes in peak months and open straight on the choice. Addresses: next-in-line candidate #6.
4. **Call-back with the choice saved** — If self-service fails, the passenger keeps their place and an agent completes the saved choice. Addresses: root cause 3 (reissue failures).
5. **Travel desk view** — Travel managers and agencies see and rebook disrupted travellers. Addresses: candidate #7.

**Chosen (unattended default):** 1 + 2 + 4 combined. Option 1 is the core; option 2 is the use case owner's idea, kept as a marker on the options rather than a decision made for the passenger; option 4 makes option 1 safe. Options 3 and 5 stay deferred, as in the scoring.

## Problem Statement
Disrupted passengers can see other flights but cannot choose one, so they keep a flight that does not work or wait 50 to 175 minutes on the phone.

## Solution
The disruption screen lets the passenger choose any offered alternative and confirm it for everyone on the booking, showing what each option means for them and what moves with them. The option that best fits what they say matters is marked with one sentence on why. If the change cannot be completed, an agent calls back with the choice already saved.

## Target Users
- **Primary:** disrupted passengers ([[amara]], [[mei]])
- **Secondary:** travel managers ([[henrik]]); satisfied passengers whose normal flow must not change ([[jonas]])

## Key Capabilities
1. Choose and confirm — any offered alternative, one confirmation, new boarding pass on the trip.
2. Everyone together — applies to all passengers; options that split the group are marked.
3. What you keep — seats and bags shown per option before confirming.
4. Fits what matters to you — the best match marked, with a one-sentence reason.
5. Safe fallback — call-back with the choice saved.

## User Stories

### As Amara (family)
- I want to pick the evening flight for all four of us, so that we get home tonight together.
- I want to see before I confirm that we are seated together, so that I do not have to call afterwards.

### As Mei (weekly traveller)
- I want to compare arrival times and choose the one that makes my meeting, so that I do not lose it while on hold.
- I want my seat and bag to move with me, so that the new ticket is right the first time.

### As Henrik (travel manager)
- I want my travellers to rebook themselves within minutes, so that I can show my board the time to rebook falling.

## Success Criteria
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Self-service rebooking rate | 12% → 30% (North Star) | operations-monthly |
| Alternatives viewers who confirm a choice or keep the pick | 28% → 60% (pilot) | RUM disruption journey |
| Contact us taps per alert opened | 41% → 25% (pilot) | RUM disruption journey |

## Out of Scope
- Refunds and vouchers in the app (separate requests in the data; P2).
- Hotel and meal vouchers.
- Travel desk and agency tools (deferred candidate #7).
- Changing the airline's disruption policy or which alternatives are offered.
- The booking flow.

## Assumptions & Risks
| Assumption/Risk | Type | Mitigation |
|-----------------|:----:|------------|
| Passengers will confirm a change themselves instead of calling | Assumption | Prototype test moment |
| Showing what moves with them is enough to trust it | Assumption | Persona critique, real-user test |
| The recommendation helps rather than distracts | Assumption | Evaluation cases, critique |
| Reissue failures can be caught and handed to an agent | Risk | Engineering spike |

## Connection to the WB Document
- Listen (Insights): 60% already reach alternatives; 41% tap Contact us.
- Define (Problem): read-only alternatives screen.
- Invent (Solution): capabilities 1 to 5.
