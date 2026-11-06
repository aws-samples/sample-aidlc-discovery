# Go-to-market: Choose My Flight (working name)
Self-service rebooking for disrupted passengers | AnyCompany Air | 2026-10-29

> **Completed in Validate, 2026-10-29.** Parts 1, 2, 3, and 5 accepted in Working Backwards; parts 4, 6, and 7 drafted in Validate for the team to confirm. Status per part below. Demonstration run on fictional sample data.

## Owners and dates (team, 2026-10-29)
| Action | Owner | Due |
|--------|-------|-----|
| Confirm the design partners (part 1) | Head of corporate accounts | 7-day follow-up |
| Size the corporate revenue at risk (part 3) | Head of corporate accounts | 7-day follow-up |
| Recruit 8 recently disrupted passengers for the riskiest-assumption walk-throughs | Head of digital and UX designer | 30-day follow-up |
| Spike on reissue and fare rules (stage 0 of the launch plan) | Engineering lead | Before any date is committed |

## 1. First adopters
**Required | Status: open** (design partners confirmed by the 7-day follow-up; segment size not in the data)

- **Segment:** corporate travellers on single-passenger bookings (Ingrid). They are about 15% of passengers but 40 of the 118 disruption records, fly weekly, have high tech affinity, and already use the app for check-in and boarding passes. [Known] Their companies are the accounts tying renewals and tenders to disruption handling. [Known] Single-passenger bookings also match the first pilot step in the PRD, before families and groups.
- **Size:** if corporate travellers are disrupted in proportion to their share of passengers, about 52,000 of the 350,108 disrupted passengers from May to mid-October 2026. [Assumed] The operations data does not split disruptions by segment. [Needs evidence]
- **How the team reaches them:**
  - **In product:** the disruption message itself (P0-1). No sign-up, no new app.
  - **Corporate accounts:** account managers brief travel managers at the accounts that raised disruption, so travellers know to act instead of calling. (Head of corporate accounts)
  - **Partners:** the travel management companies and agencies that book for these accounts, using the booking reference (feature C).
- **Design partners** (roles, not names; the head of corporate accounts confirms which accounts by the 7-day follow-up):
  1. The software company account whose CFO missed a board meeting after a Lisbon cancellation and that is trialling a competitor on two routes. [Known] from the account note
  2. A large corporate account with a travel manager who owns duty of care for thousands of travellers (the profile behind Karim). Whether a specific account will commit: [Needs evidence]
  3. One partner travel agency that today rebooks groups one at a time by phone and is reconsidering its packages. [Known] from agency escalations

## 2. Positioning
**Required | Status: open** (the "no call" benefit rests on the riskiest assumption)

> For **disrupted AnyCompany Air passengers** who **can see alternative flights but have to phone or queue to get onto one**, **Choose My Flight** is **a way to rebook in the app or on the website** that **gets them onto a new flight, with a boarding pass, in under three minutes, at any hour, with nothing to pay**. Unlike **calling the call centre (up to three hours on hold) or accepting the flight the airline picked**, it **lets the passenger, or someone they trust, decide before the good flights fill up**.

Evidence:
- "Can see alternatives but have to phone": 37 records ask to choose the flight themselves; the app and website offer only "contact us". [Known]
- "Up to three hours on hold": holds of 50 to 175 minutes reported; customer service operations lead. [Known]
- "Accepting the flight the airline picked" is the do-nothing alternative: 9 records describe automatic rebookings days later or with long layovers. [Known]
- "Under three minutes": team target; callers give up after about five. [Assumed]
- "Nothing to pay": disruption policy, confirmed by the head of digital. [Known]
- The cost of changing is low: the passenger meets it in the disruption message they already receive. Whether passengers trust it enough not to call is the riskiest assumption. [Needs evidence]

## 3. Business model and pricing
**Hypothesis | Status: open | Owner: head of digital, with the head of corporate accounts** (revenue at risk by the 7-day follow-up; voucher cost now part of the case)

- **Included free for every disrupted passenger.** The disruption policy rules out a fee or fare difference among the flights offered. [Known] There is no willingness-to-pay question for passengers.
- **Why it pays:**
  - **Retention of corporate accounts.** Corporate travellers are about a third of revenue; four account notes tie a renewal, risk, or tender to disruption handling; one account is trialling a competitor. [Known] How much revenue is at risk: [Needs evidence] (head of corporate accounts sizes it from the accounts flagged, by the 7-day follow-up).
  - **Call centre time.** If rebooking calls fall from 42 to 25 per 100 disrupted passengers, the same five and a half months would have had about 59,500 fewer rebooking calls. At the sample's average of 37 minutes per disruption call, that is roughly 36,700 agent hours. [Assumed]: the 37 minutes comes from a 110-contact sample, and the calls that remain may be the harder, longer ones. Staffing and cost per hour: [Needs evidence] (research hypothesis 8).
  - **Partner agencies.** Agencies planning a disruption fee for their clients may not need one. [Assumed]
- **Possible later add-on:** the travel desk view (P1-3) and disruption reports (P2-3) as part of the corporate contract offering, not a separate price. [Assumed]; travel managers' needs [Needs evidence] (research hypothesis 3)
- **Cost to serve:** no AI in the PRD, so no model cost. Build and running costs belong to the build.

## 4. Viability check
**Required | Status: open** (drafted in Validate; owners to confirm)

| Area | Owner role | Main concern |
|------|------------|--------------|
| Legal and compliance | Head of digital, with legal | Passenger-rights obligations on rebooking and care (hotel, meals) when the airline lets the passenger choose; refund wording on the "none works" route |
| Privacy and security | Engineering lead, with the security review | Booking reference plus surname as permission to rebook for someone else; contact details on agency bookings |
| Sales | Head of corporate accounts | Changes corporate renewal conversations; whether travel desks need the P2 update before it helps renewals |
| Support and success | Customer service operations lead | New questions ("is my self-chosen flight real?"), call-backs within the hour at peak, desks seeing what passengers already did, hotel vouchers without an agent |
| Marketing | Head of digital | None for the pilot; at launch, telling passengers and families "someone can rebook for you" |

## 5. Launch plan
**Hypothesis | Status: open | Owner: head of digital** (the decision adds the walk-throughs and the Hamburg to Milan pilot before stage 2; see below)

| Stage | What happens | Exit criteria |
|-------|--------------|---------------|
| 0. Before any stage | Engineering spike on reissue and fare rules | Spike reports; the team confirms or moves June 2027 |
| 1. Internal use | Call centre agents use the same flow while on the phone with disrupted callers, on a set of routes | Reissued tickets correct, with no change fee charged, in agents' hands; fewer than 2% need fixing |
| 2. Design partners | Travellers at 2 to 3 corporate accounts and one partner agency, on single-passenger bookings, on those routes | The riskiest-assumption thresholds met with real passengers; boarding pass in under 3 minutes; design partners say they would keep it |
| 3. Limited release | A share of all disrupted single-passenger bookings on a wider set of routes, compared with similar disrupted passengers who are not offered it | Self-service rate and calls per 100 moving toward 35% and 25; survey score at or above +4 |
| 1b. Gates (decision, 2026-10-29) | 8 walk-throughs, the reissue spike, and the home-airport voucher rule in 30 days; then the Hamburg to Milan pilot, 4 weeks or 500 disrupted passengers | 6 of 8 walk-throughs pass; pilot: at least 40% of those who see the options accept with no call before departure (head of digital, 90-day follow-up) |
| 4. General availability | All disrupted passengers, then families and groups (P1-4); target June 2027, before the summer peak | Launch; the 90-day targets start counting |

**Enablement before the limited release:**
- **Call centre:** what to say when a passenger asks "I chose a flight online, is it real?", and how to take over from a call-back with the booking loaded (P1-1). (Customer service operations lead)
- **Corporate accounts:** a one-page brief for travel managers and travel management companies, and how travellers are told. (Head of corporate accounts)
- **Partner agencies:** how to rebook a customer with the booking reference. (Head of corporate accounts)
- **Airport desks:** what the passenger may have already done before reaching the desk. (Customer service operations lead)

## 6. Adoption and success
**Required | Status: open** (adoption owner confirmed; interim targets and kill criteria are proposals, [Assumed], for the head of digital to set at the 30-day follow-up)

| Item | Content |
|------|---------|
| Adoption owner | Head of digital (confirmed by the team, 2026-10-29) |
| Adoption metric | Share of disrupted passengers who open the message and accept a flight in the flow |
| Leading indicators | Median time to boarding pass (under 3 minutes); share who call after rebooking themselves; seat-gone screens per rebooking; share rebooked "for someone else"; survey score for online rebookers at or above +4 |
| Business metric | Self-service rebooking rate for disrupted passengers, baseline 12% |
| Targets | Pilot: at least 40% of those who see the options. After full launch: 35% self-service and 25 calls per 100 at 90 days (team commitment). Interim 20% / 28% and 36 / 30 calls at 30 and 60 days: [Assumed] proposals |
| Kill criteria | [Assumed] proposal, head of digital sets at the 30-day follow-up: pilot below 40% after 4 weeks or 500 passengers, or walk-throughs below 6 of 8: stop and decide pivot or park. After full launch: below 20% self-service at 60 days, or more than 5% of self-service rebookings needing an agent to fix |

## 7. Risks and open hypotheses
**Status: open**
- Do passengers need to call for nothing else after rebooking themselves? (riskiest assumption; walk-throughs and pilot)
- Does a travel desk see the change, or call to reconcile? (head of corporate accounts, 7-day)
- How much corporate revenue is at risk? (head of corporate accounts, 7-day)
- Can hotel vouchers be issued without an agent, only away from home, at what cost? (customer service operations lead)
- Will the pilot route predict the summer peak? (no winter baseline)
