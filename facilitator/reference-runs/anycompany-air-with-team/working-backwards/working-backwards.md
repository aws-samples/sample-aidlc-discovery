# Working Backwards: self-service rebooking for disrupted passengers
**Created:** 2026-10-29
**Workshop:** AnyCompany Air (Self-serve; demonstration run on fictional sample data)

> **Confirmed by the team, 2026-10-29.** Drafted during the break from the Signal Analysis Report, the five personas, and the use case scoring; the head of digital confirmed the five answers as the team's own, and the North Star targets and date.

## 1. LISTEN: Who is the customer?

### Primary customers
- **Disrupted passengers in all three segments:** leisure (Daniel), frequent flyers, corporate travellers (Ingrid). 350,108 disrupted passengers from May to mid-October 2026. [Known]
- **People who rebook for someone else:** family members (Helena's daughter), assistants, partner agencies, corporate travel desks (Karim). [Known] that they exist; how many [Needs evidence]

### Key customer insights
1. Passengers can already see alternative flights; what they lack is a way to choose one. 37 records ask for exactly this. [Known]
2. The disruption, not the delay, is what they judge the airline on: "The delay wasn't the problem. Not being able to change my flight myself was." [Known]
3. Disrupted passengers who rebooked in the app score +4; through the call centre −58; at an airport desk −62. Harder cases may call more often, so part of the gap is selection. [Known] / [Assumed]
4. Speed matters because good flights fill up while passengers wait on hold ("call immediately before the good flights fill up"). [Known]
5. Corporate buyers judge renewals on disruption handling; four account notes tie a renewal, risk, or tender to it. [Known]

### Pain points
- No action to choose a new flight; the app says "contact us". Severity: High. [Known]
- Holds of 50 to 175 minutes. Severity: High. [Known]
- Automatic rebooking onto flights days later or with long layovers (9 records). Severity: High. [Known]
- Families and groups split (11 records). Severity: High. [Known]
- No help out of hours (17 records). Severity: High. [Known]
- Errors and conflicting information during disruption: ticket not reissued, change fee charged (13 records). Severity: Medium. [Known]
- No way to rebook on someone else's behalf, or in bulk for a travel desk (7 records plus 2 assistants). Severity: Medium. [Known]

## 2. DEFINE: The customer problem

### Core problem
When their flight is cancelled or delayed by more than two hours, AnyCompany Air passengers can see the alternative flights but cannot choose one, so they have to phone or queue, and lose hours and the best flights while they wait.

### End customer
The **disrupted passenger**: the person whose evening changes when this ships. Primary example: Ingrid, cancelled at the gate with a meeting in the morning. Also affected: the people who act for passengers (Helena's daughter, Karim's travel desk) and the call centre agents, who get time back for the passengers who still call.

### Root causes (why, not what)
1. The app and website show disruption and alternatives as information only; the only action they offer is "contact us". [Known]
2. Reissuing a ticket and applying fare rules after a change works reliably only through an agent today; online attempts produce errors and wrong change fees (13 records; engineering lead). [Known]
3. Automatic rebooking chooses a flight for the passenger without asking, so a passenger who disagrees must call to undo it. [Known]
4. A booking can only be changed online by the passenger, so a family member, assistant, agency, or travel desk has no way to act for them. [Known]
5. Human help depends on the phone line's opening hours, and disruptions do not. [Known]

### Impact on the customer
- Hours on hold or in a queue (50 to 175 minutes reported). [Known]
- Missed meetings, a lost day of school or work, a night in an unplanned place. [Known]
- Families split across flights. [Known]
- Feeling helpless and let down: "The airline didn't care once the flight was cancelled." [Known]

### Impact on the business
- Only 12% of disrupted passengers rebook themselves; about 42 rebooking calls per 100 disrupted passengers. [Known]
- Disruption calls are 39% of contacts and 62% of agent handle time in the sample, 37 minutes each on average. [Known]
- Corporate renewals and tenders at risk; one account trialling a competitor on two routes. [Known]
- Partner agencies reconsidering packages and planning a disruption fee. [Known]

### Constraints
- Some passengers will not use an app; the phone and the airport desk stay (team challenge 3). [Known]
- The engineering lead wants a spike on reissue and fare rules before any delivery date. [Known]
- Discovery decides who, what, and why; how reissue works belongs to the build.

### Today statement
Today, disrupted AnyCompany Air passengers have to phone or queue to change their flight when it is cancelled or delayed by more than two hours, even though they can see the alternatives. They need a way to get onto a new flight that works for them within minutes, at any hour, on their own or through someone they trust.

### How Might We
How might we get disrupted passengers onto a new flight that works for them within minutes, at any hour, so that a disruption costs them minutes instead of an afternoon on hold?

### North Star (confirmed by the head of digital, 2026-10-29)
Deploy a way for disrupted passengers, or someone acting for them, to choose and confirm a new flight without calling, by June 2027, to raise the self-service rebooking rate from 12% to 35% and cut rebooking calls from 42 to 25 per 100 disrupted passengers, in order to make a disruption something passengers settle in minutes and still trust the airline afterwards. The 35% and 25 are the team's commitment, not evidence; June 2027 holds until the reissue spike reports.

## 3. INVENT: Solution approaches

### Solution: "Choose My Flight" (working name)
When a flight is disrupted, the passenger sees the flight the airline suggests and the other flights with seats, and either accepts the suggestion or picks another; the new ticket and boarding pass are issued on the spot. Someone acting for the passenger can do the same with the booking reference.

### Core capabilities
1. **Choose a new flight**: from the disruption message, pick from the alternatives and confirm. Addresses root cause 1.
2. **Reliable reissue**: the new ticket is issued correctly with no change fee for a disruption. Addresses root cause 2; subject to the engineering spike.
3. **We suggest, you decide**: an automatic rebooking is shown as a suggestion the passenger can accept or replace. Addresses root cause 3.
4. **Rebook for someone else**: a family member, assistant, or agency can act with the booking reference. Addresses root cause 4.
5. **At any hour**: all of the above works when the phone line is closed. Addresses root cause 5.

### Differentiation
The passenger acts on the options they can already see, at the moment of the disruption, before the good flights fill up. The airline already holds the alternatives; this gives the passenger the decision.

### Build vs buy vs partner
For the build to decide. Discovery notes only that reissue and fare rules are the hard part.

## 4. REFINE: Customer experience

### Customer journey (Ingrid, cancelled at the gate)
1. Notification: "Your flight to Milan is cancelled."
2. She opens it and sees the suggested flight (tomorrow 07:20) and two others.
3. She taps the 07:20 and sees what changes: times, seat, no extra cost.
4. She confirms; the new ticket and boarding pass appear.
5. Optional next step if the flight is the next day (for example, a hotel). [Assumed, P1]

### Day 1 experience
The first time is the disruption itself: no set-up, no new app. The passenger meets the feature in the cancellation message they already receive.

### Ongoing usage
Frequent travellers learn to act straight away instead of calling. Travel desks and agencies use it for the travellers they look after.

## 5. TEST & ITERATE: Measuring success

### Success metrics (first two confirmed by the team; last two Assumed, for Validate)
| Metric | Baseline | Target | Timeframe |
|--------|:--------:|:------:|-----------|
| Self-service rebooking rate, disrupted passengers | 12% | 35% | 90 days after launch |
| Rebooking calls per 100 disrupted passengers | 42 | 25 | 90 days after launch |
| Survey score, disrupted passengers who rebooked online | +4 (app) | Stays at or above +4 at the higher volume | 90 days after launch |
| Time from opening the message to a boarding pass | Not measured | Under 3 minutes (team target; callers give up after about 5) | From launch; tested in the prototype |
| Rebookings that need an agent to fix afterwards | Not measured | Under 2% | From launch |

### Validation approach
- Prototype walk-through with the personas today; real disrupted passengers next (research hypothesis 1).
- Engineering spike on reissue and fare rules before any date.
- Pilot on a share of disrupted passengers, compared with the rest (A/B).

### Iteration plan
- Month 1: spike on reissue; prototype test with disrupted passengers.
- Quarter 1: pilot for single-passenger bookings on a set of routes.
- Year 1: groups and families, rebooking for someone else, travel desk and agency access.

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Reissue fails or charges wrong fees | Medium | High | Spike first; agent fallback; measure fix-up rate |
| Passengers do not trust the self-chosen flight and call anyway | Medium | High | Prototype test; clear confirmation and boarding pass |
| Passengers who will not self-serve are left behind | Medium | Medium | Rebook for someone else; phone and desk stay |
| The +4 vs −58 gap is mostly selection, so scores rise less | Medium | Medium | Compare like-for-like disruptions (hypothesis 2) |
