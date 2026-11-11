# PRD: Choose My Flight (working name)
Self-service rebooking for disrupted passengers | AnyCompany Air | 2026-10-29

> **Accepted by the team, 2026-10-29**, with the disruption fare policy confirmed and the booking-reference rule sent to Validate. Demonstration run on fictional sample data. Built from the confirmed Working Backwards answers, the reviewed PR/FAQ and its readiness check, the five personas, and the use case scoring. Discovery decides who, what, and why; how it is built belongs to the build.

## 1. Executive summary
When their flight is cancelled or delayed by more than two hours, AnyCompany Air passengers can see alternative flights but cannot choose one, so most phone or queue. Choose My Flight lets the passenger, or someone acting for them, keep the airline's suggested flight or pick another, and leave with a reissued ticket and boarding pass in under three minutes, at any hour. The team commits to raising the self-service rebooking rate from 12% to 35%, and cutting rebooking calls from 42 to 25 per 100 disrupted passengers, within 90 days of launch. Target launch: June 2027, held until the reissue spike reports.

## 2. Problem statement
- 350,108 passengers were disrupted from May to mid-October 2026; 12.2% rebooked themselves and about 42 in 100 phoned. [Known]
- Disruption and rebooking is 30% of all feedback (118 of 400 records), across all six sources and all three segments; 37 records ask directly to choose the flight themselves. [Known]
- Callers wait on hold for up to three hours (50 to 175 minutes reported) while the flights they can see fill up. Disruption calls are 39% of contacts and 62% of handle time in the call sample, averaging 37 minutes. [Known]
- Disrupted passengers who rebooked in the app score +4; through the call centre −58; at an airport desk −62. Part of the gap may be harder cases choosing to call. [Known] / [Assumed]
- Four corporate account notes tie a renewal, risk, or tender to disruption handling; one account is trialling a competitor on two routes. [Known]

**Root causes** (from `working-backwards.md`): the app and website show alternatives as information only; reissue and fare rules work reliably only through an agent; automatic rebooking chooses without asking; only the passenger can change a booking online; human help depends on the phone line's opening hours. [Known]

## 3. Goals and success metrics
| Metric | Baseline | Target | Timeframe | Label |
|--------|:--------:|:------:|-----------|-------|
| Self-service rebooking rate, disrupted passengers | 12% | 35% | Within 90 days of launch | Team commitment; baseline [Known] |
| Rebooking calls per 100 disrupted passengers | 42 | 25 | Within 90 days of launch | Team commitment; baseline [Known] |
| Time from opening the disruption message to a boarding pass | Not measured | Under 3 minutes | From launch; tested in the prototype | Team target. Basis: callers give up and call after about five minutes (customer service operations lead, from what callers say) [Assumed] |
| Survey score, disrupted passengers who rebook online | +4 (app) | At or above +4 at the higher volume | Within 90 days of launch | [Assumed], for Validate |
| Self-service rebookings that need an agent to fix afterwards | Not measured | Under 2% | From launch | [Assumed], for Validate |

**Goal:** a disruption becomes something passengers settle in minutes, and they still trust the airline afterwards.

## 4. User personas
| Persona | Role in this PRD | Confidence |
|---------|------------------|:----------:|
| **Ingrid Halvorsen**, corporate traveller, weekly flyer | Primary user. Cancelled at the gate, meeting at 9:00 tomorrow | High |
| **Daniel Okafor**, leisure traveller with a family | Second journey. Cancelled at 23:00; the airline's choice splits the day and the family | High |
| **Helena Kowalska**, passenger who does not use the app | Third journey, through her daughter rebooking from home | Low |
| **Karim Haddad**, corporate travel manager | P1 user (travel desk view); needs still [Assumed] until travel managers are interviewed | Medium |
| **Sofia Lindqvist**, the happy regular | Guardrail: nothing in this PRD may slow or clutter the booking and check-in she relies on | High |

## 5. Requirements

### Functional requirements

**P0: what the prototype must show and the first release must have**

| ID | Requirement | Feature | Persona | Label |
|----|-------------|:-------:|---------|-------|
| P0-1 | The disruption message offers a direct action to choose a new flight, in the app, on the website, and by text or email for passengers without the app | A | Ingrid, Daniel | Need [Known] |
| P0-2 | The passenger sees the airline's suggested flight, marked as a suggestion, and the other flights that still have seats | A, B | All | Need [Known] |
| P0-3 | For each option the passenger sees, at a glance: departure and arrival time, connections, whether everyone on the booking sits together, and that there is nothing to pay | A | All | Need [Known] (13 records on wrong fees; 11 on split families) |
| P0-4 | The passenger keeps the suggestion or replaces it with another option, and confirms | A, B | Ingrid, Daniel | Need [Known] (9 records on unsuitable automatic rebookings) |
| P0-5 | After confirmation, the passenger receives the reissued ticket and a new boarding pass, with no change fee or fare difference among the options offered | A | All | Policy [Known] (confirmed by head of digital, 2026-10-29); reissue reliability [Needs evidence] (engineering spike) |
| P0-6 | Anyone with the booking reference and the passenger's surname can open the booking and make the same change; the passenger receives the new flight by text | C | Helena's daughter, assistants, agencies | Need [Known]; reference plus surname is what manage-booking uses today [Known] (engineering lead); whether it is safe enough for rebooking [Needs evidence] (security review in Validate) |
| P0-7 | Every passenger on the booking moves together by default | A | Daniel | Need [Known]; seat availability together [Assumed] |

**P1: next, after the pilot**

| ID | Requirement | Label |
|----|-------------|-------|
| P1-1 | When no option works: a call-back with the booking already loaded for the agent, and the refund route. In the prototype, one screen if time allows (nice-to-have, head of digital) | Team decision |
| P1-2 | Hotel and meal help when the new flight is the next day, without calling (out-of-hours help). **Only when the passenger is away from their home airport** (engineering lead, 2026-10-29) | Need [Known] (17 records on out-of-hours; vouchers only through an agent); how the home airport is known [Needs evidence] |
| P1-3 | Travel desk view: a corporate travel desk sees every affected traveller and rebooks them within policy, in bulk | [Assumed] until travel managers confirm (research hypothesis 3) |
| P1-4 | Groups and bookings with different fares on one booking | [Needs evidence] (engineering spike) |

**P2: later**

| ID | Requirement | Label |
|----|-------------|-------|
| P2-1 | Disruption updates to travel management companies and partner agencies, so they act before the traveller calls | [Assumed] |
| P2-2 | Passenger chooses a different airport or date range than the options offered | [Assumed] |
| P2-3 | Disruption reports for corporate accounts: time to rebook, travellers affected | [Assumed] (Karim's renewal reporting) |

### Non-functional requirements
| ID | Requirement | Label |
|----|-------------|-------|
| NF-1 | Works at any hour, including when the phone line is closed | Need [Known] |
| NF-2 | A passenger reaches a boarding pass in under 3 minutes from opening the message | Team target |
| NF-3 | The seats shown are still available when the passenger confirms; if a flight fills up meanwhile, the passenger is told before confirming and offered the next option | [Assumed]; currency of availability [Needs evidence] (engineering spike) |
| NF-4 | Fewer than 2% of self-service rebookings need an agent to fix | [Assumed] |
| NF-5 | Usable on a phone, one-handed, at a gate; readable for passengers with low tech affinity, and accessible to passengers using assistive technology | Need [Known] (Helena; "too many options on one page") |
| NF-6 | The phone line and airport desk stay available; nothing in this PRD removes a human route | Team constraint (challenge 3) |
| NF-7 | Booking and check-in in the app keep their current speed and layout | Guardrail (Sofia; engineering lead's expectation 6) |
| NF-8 | **Proposal:** the disruption message reaches the passenger within a set time of the disruption being known, before the good flights fill (pre-mortem reason 4). Time to be set | [Assumed]; head of digital sets it at the 30-day follow-up, after the message audit (research hypothesis 5) |

## 6. User stories and acceptance criteria

**Ingrid: cancelled at the gate**
- *As Ingrid, I want to move myself onto the 07:20 from the gate, so that I make my 9:00 meeting.*
  - Given her flight is cancelled, when she opens the notification, then she sees the suggested flight and at least the other flights with seats.
  - When she picks the 07:20 and confirms, then she has a new boarding pass, with nothing to pay, in under 3 minutes from opening the message.

**Daniel: cancelled at 23:00**
- *As Daniel, I want to replace the flight the airline picked with one where the four of us sit together, so that we do not lose a day.*
  - Given the airline's suggestion is two days later, when he opens the options, then the suggestion is marked as a suggestion and he can choose another.
  - Each option shows whether all four sit together; when he confirms, all four move together.
- *As Daniel, I want to do this at 23:00, so that the children go to bed knowing how we get home.*
  - The flow works with the phone line closed, and needs no agent.

**Helena's daughter: rebooking from home**
- *As Helena's daughter, I want to rebook my parents from my own laptop, so that they know where to go without queuing.*
  - Given the booking reference and surname, she sees her parents' options and confirms one.
  - Helena receives a text with the new flight and gate.

**When nothing works (P1-1)**
- *As a passenger with no suitable option, I want a call-back from someone who already has my booking, so that I do not explain everything again.*
  - The passenger can request a call-back or open the refund route from the options view.

## 7. Out of scope and non-goals
- Refunds and compensation claims beyond showing the existing refund route.
- Changes to bookings that are not disrupted.
- Booking flow changes (candidate 2, deferred).
- Bag tracking and loyalty (candidates 3 and 4, deferred).
- Choosing how reissue and fare rules work technically; that belongs to the build.
- Replacing the call centre or airport desks.

## 8. Dependencies and risks
| Item | Type | Detail | Owner | Label |
|------|------|--------|-------|-------|
| Reissue and fare rules spike | Dependency | Must report before any date is committed; can move June 2027 | Engineering lead | [Needs evidence] |
| Disruption fare policy | Dependency | No change fee or fare difference among the options offered | Head of digital | [Known]: confirmed as policy, 2026-10-29 |
| Passengers choose and need nothing else | Risk | If they wait for the airline, call to check, or call for something else such as a hotel, no queue is removed | Team | [Assumed]: **the riskiest assumption** (`riskiest-assumption.md`, widened after the persona critique) |
| Hotel help is P1-2, but the widened assumption needs it for next-day rebookings | Open question | The prototype (v3) shows a hotel voucher on the confirmation. If the walk-throughs show passengers call for the hotel, P1-2 may need to move to P0 for next-day rebookings | Head of digital | [Needs evidence]; vouchers without an agent: customer service operations lead |
| Passengers who will not self-serve | Risk | Left behind if the human route weakens | Customer service operations lead | [Needs evidence] (research hypothesis 11) |
| Selection in the survey gap | Risk | The +4 vs −58 gap may be partly harder cases calling, so scores rise less than hoped | Team | [Assumed] (research hypothesis 2) |
| Booking reference as permission to act | Risk (feasibility and security) | Reference plus surname is today's manage-booking rule; someone holding them could change a booking the passenger did not want changed | Engineering lead, with security review | [Needs evidence]: goes to the Validate risk review |

## 9. Timeline considerations
- **Now:** prototype and persona critique today; reissue spike next. [Team plan]
- **Target launch:** June 2027, before the summer peak, when disruptions and calls double. Held until the reissue spike reports. [Known] for the summer peak; date is the team's target.
- **Proposed sequence:** pilot for single-passenger bookings on a set of routes, measured against comparable disrupted passengers; then families and groups; then rebooking for someone else at scale and P1. [Assumed]

## 10. AI feature checklist
Not applicable: no requirement in this PRD uses AI. The airline's suggested flight is today's automatic rebooking, shown as a suggestion.

## Writing audit
Checked: customer as subject, active voice, no superlatives, buzzwords, unproven firsts, or em dashes; one set of targets (North Star plus the team's 3-minute target, which the PR/FAQ now carries too); claims kept to their scope; no architecture. P0 is seven requirements on one flow with three paths, small enough to prototype in an hour.
