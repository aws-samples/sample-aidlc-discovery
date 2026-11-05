# Feature: Choose My Flight (working name)

> **Chosen by the team, 2026-10-29:** A + B + C. Travel desk view (E) and out-of-hours hotel help (part of D) are P1. Working name "Choose My Flight" kept.

## Feature ideas for the team
1. **A. Choose your new flight**: pick and confirm a new flight from the disruption message, in the app or on the website. Addresses: root cause 1 (information but no action).
2. **B. We suggest, you decide**: an automatic rebooking becomes a suggestion the passenger accepts or replaces. Addresses: root cause 3 (the airline chooses without asking).
3. **C. Rebook for someone else**: a family member, assistant, or agency changes the flight with the booking reference. Addresses: root cause 4 (only the passenger can act); team challenge 3.
4. **D. Out-of-hours disruption help**: the disruption message gives a next step at any hour, including a hotel where the next flight is the following day. Addresses: root cause 5.
5. **E. Travel desk view**: corporate travel desks see affected travellers and rebook them in bulk within policy. Addresses: Karim; research hypothesis 3 (buyers' needs still Assumed).

**Team's choice: A + B + C** (head of digital, 2026-10-29). A is the core of the metric; B removes calls that only undo an automatic choice; C gives a path to passengers like Helena. D's "any hour" comes free with A; the hotel part and E go to P1.

## Problem statement
Disrupted passengers can see alternative flights but cannot choose one, so they phone or queue for hours while the good flights fill up.

## Solution
From the disruption message, the passenger sees the suggested flight and the alternatives, accepts or picks one, and gets the new ticket and boarding pass on the spot. Anyone with the booking reference can do it for them.

## Target users
- **Primary:** disrupted passengers in all segments (Ingrid, Daniel).
- **Secondary:** people acting for a passenger (Helena's daughter, assistants, agencies); later, corporate travel desks (Karim).

## Key capabilities
1. Choose a new flight from the alternatives.
2. Accept or replace the airline's suggested flight.
3. Rebook on someone else's behalf with the booking reference.

## User stories
### As Ingrid (corporate traveller)
- I want to move myself onto the 07:20 from the gate, so that I make my 9:00 meeting.
### As Daniel (leisure, family)
- I want to choose a flight where the four of us sit together at 23:00, so that the children go to bed knowing how we get home.
- I want to change the flight the airline picked for us, so that we do not lose a day.
### As Helena's daughter
- I want to rebook my parents from home, so that they know where to go without queuing.

## Success criteria
| Metric | Target | Measurement method |
|--------|--------|--------------------|
| Self-service rebooking rate | 12% → 35% within 90 days of launch (North Star, team commitment) | Operations data, disrupted passengers |
| Rebooking calls per 100 disrupted | 42 → 25 within 90 days of launch (North Star, team commitment) | Call centre data |

## Out of scope
- Refunds and compensation claims.
- Bulk rebooking for travel desks (P1).
- Changes to bookings that are not disrupted.

## Assumptions & risks
| Assumption/Risk | Type | Mitigation |
|-----------------|:----:|------------|
| Passengers will choose for themselves if they can | Assumption | Prototype test; research hypothesis 1 |
| Reissue and fare rules can work without an agent | Risk | Engineering spike before any date |
| A booking reference is enough to act for someone else | Assumption | Test with people who rebook for others |

## Connection to the WB document
- Listen: 37 records ask to choose themselves; holds of 50 to 175 minutes.
- Define: root causes 1, 3, and 4.
- Invent: capabilities 1, 3, and 4 (capability 2, reliable reissue, is the condition for all three).
