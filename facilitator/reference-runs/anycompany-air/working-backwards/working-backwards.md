# Working Backwards: self-service rebooking for disrupted passengers
**Created:** 2026-10-30
**Workshop:** E2E-air (AnyCompany Air, fictional sample data)
**Mode:** unattended run. Each answer is drafted from the Signal Analysis Report, the personas, and the scoring, and stands in for the team's answer. With a real team, go through each answer before the PR/FAQ is used.

## 1. LISTEN — Who is the customer?

### Primary Customers
- Disrupted passengers on any route: [[amara]] (leisure family) and [[mei]] (weekly corporate traveller). 350,108 disrupted passengers from May to mid-October 2026. Known
- Buyer on the corporate side: [[henrik]] (travel manager), who renews on disruption handling. Known (account notes)
- Satisfied passengers whose normal trip must not get worse: [[jonas]]. Known

### Key Customer Insights
1. Passengers already look for another flight themselves: 60% of alert openers reach the alternatives screen, and it is the longest step (median 84 s). Known
2. They cannot act on what they see: the only action is keeping the airline's pick (17% of alert openers); 41% tap Contact us. Known
3. The airline's automatic pick often does not fit: days later, long layovers, families split. Known (7+ records)
4. The phone is where the experience breaks: call centre NPS −58, airport desk −62, self-service app +4. Known
5. For corporate buyers this is the renewal issue, not price or booking design. Known (12 of 30 account notes)

### Pain Points
- Cannot choose from the alternatives shown. Severity: High
- Holds of 50 to 175 minutes while good flights fill up. Severity: High
- Automatic rebooking onto flights that do not work. Severity: High
- New ticket or extras not carried over after a change. Severity: Medium
- Alerts that come late and lead nowhere. Severity: Medium

## 2. DEFINE — The Customer Problem

### Core Problem
When a flight is disrupted, passengers can see other flights but cannot choose one, so they keep a flight that does not work for them or wait on the phone while the good options disappear.

### End customer
The disrupted passenger at the gate or in the terminal ([[amara]], [[mei]]). Also affected: travel managers and agencies who answer for them, and call centre agents.

### Root Causes (why, not what)
1. The alternatives screen is read-only: the product only lets a passenger accept the airline's automatic choice, so any other choice has to go through an agent. Known (journey map, telemetry)
2. The automatic choice does not know what matters to the passenger (arrival time, staying together, direct routing), so it often picks a flight that does not fit. Assumed
3. Changing a ticket after a disruption fails often enough (5.0% reissue rejections) that changes are kept with agents, who can fix failures by hand. Assumed
4. The call centre is the only fallback, sized for normal months, so its capacity sets how long passengers wait in peak months. Known (calls per 1,000 flat; volume doubles in July and August)

### Impact on the customer
- Hours lost on hold or in desk queues (50 to 175 minutes quoted).
- Missed meetings, onward trains, hotel nights, and family time.
- Families and groups split across flights or days.
- Loss of control and trust ("you are on your own").

### Impact on the business
- 146,299 rebooking calls in five and a half months, averaging 38 minutes. Known
- NPS for cancelled flights runs at about −56, against +44 for on-time flights. Known
- Corporate renewals and a February tender tied to disruption; routes being moved to competitors. Known (account notes)
- Agencies plan disruption fees and reconsider packages. Known (agency escalations)

### Today statement
Today, disrupted passengers have to wait on the phone or in a desk queue to change a flight they can already see in the app, when their flight is cancelled, delayed by more than two hours, or they miss a connection. They need a way to choose a new flight that works for them and know it is confirmed, within minutes and wherever they are.

### How Might We
How might we let disrupted passengers choose a new flight that works for them and know it is confirmed, so that they stay in control of their trip without waiting for an agent?

### North Star
Deploy a way for disrupted passengers to choose and confirm their own new flight in the app and on the website by June 2027, before the summer peak, to raise the self-service rebooking rate from 12% to 30% and reduce rebooking calls from about 415 to 300 per 1,000 disrupted passengers by the end of September 2027, in order to have every disrupted passenger back in control of their trip within minutes.

*How the numbers were set:* 30% means about 60,000 more self-service rebookings over a period like this one. That is about 55% of the 108,316 alternatives views that today end without a kept suggestion. Assumed: it has to be tested in the prototype and pilot. 300 calls per 1,000 follows if most new self-service rebookings would otherwise have been calls. Assumed.

## 3. INVENT — Solution Approaches

### Solution: "Choose your flight"
On the disruption screen the passenger picks one of the alternatives and confirms it, for everyone on the booking, with seats and bags carried over. The screen shows what each option means for them (arrival time, stops, whether the group stays together), and the flight that best fits what they say matters is marked with a one-sentence reason.

### Core Capabilities
1. **Choose and confirm** — Select any offered alternative and confirm it in one step; the new boarding pass appears on the trip.
2. **Everyone together** — The choice applies to all passengers on the booking; options that would split them are marked.
3. **What you keep** — Each option shows whether seats and bags move with the passenger, before they confirm.
4. **Fits what matters to you** — The passenger says what matters most (arrive by a time, stay together, fewest stops) and the best match is marked with one sentence on why.
5. **Safe fallback** — If a change cannot be completed, the passenger keeps their place and gets a call-back with the choice already made, instead of starting over on hold.

### Differentiation
The passenger does in two minutes what today takes a 38-minute call, and the option they pick is the one they chose, not the one the system assigned.

### Build vs. Buy vs. Partner
For the build to decide. Discovery notes that alternatives and keep-suggestion already exist in the product.

## 4. REFINE — Customer Experience

### Customer Journey
1. Alert: "Your 17:25 to Lisbon is cancelled. Choose a new flight." Opens the disruption screen.
2. Sees the current automatic pick next to two to four alternatives, each with arrival time, stops, seats left, and whether everyone stays together.
3. Optionally taps what matters (arrive by, stay together, fewest stops); the best match is marked with one reason.
4. Chooses a flight; sees what moves with them (seats, bags) and confirms for all passengers.
5. Gets the confirmation and the new boarding passes on the trip screen; travel agency or travel desk is informed.
6. If confirmation fails: a call-back is booked with the choice saved.

### Day 1 Experience
No onboarding: the passenger meets the feature only when a disruption alert arrives, on the screen they already open today.

### Ongoing Usage
Frequent travellers like [[mei]] learn to act on the alert immediately; [[jonas]] never sees it until his first disruption, and his normal trip screen is unchanged.

## 5. TEST & ITERATE — Measuring Success

### Success Metrics
| Metric | Target | Timeframe |
|--------|--------|-----------|
| Self-service rebooking rate | 12% → 30% | June to September 2027 |
| Rebooking calls per 1,000 disrupted passengers | about 415 → 300 | June to September 2027 |
| Alternatives viewers who confirm a choice or keep the pick | 28% → 60% | Pilot |
| Contact us taps per alert opened | 41% → 25% | Pilot |
| Disrupted-passenger NPS for those who self-serve | stays at or above 0 | Pilot |

### Validation Approach
- Prototype with persona critique today; then a test with real disrupted passengers.
- Pilot on a share of disruptions on a few routes, compared with disruptions handled today.

### Iteration Plan
- Month 1: test the prototype with 8 to 10 recently disrupted passengers and three travel managers.
- Quarter 1: pilot on selected routes; engineering spike on reissue failures.
- Year 1: all routes before summer 2027; travel desk and agency view (scoring #7) next.

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Passengers do not trust a self-made change and call anyway | Medium | High | Show what moves with them and a clear confirmation; test in prototype |
| Reissue failures leave passengers without a valid ticket | Medium | High | Safe fallback with call-back; spike before pilot |
| Recommendation picks a flight that does not fit, eroding trust | Medium | Medium | Recommendation marks, never books; evaluation cases |
| Normal trip screen gets heavier for satisfied passengers | Low | Medium | Disruption screen only appears on disruption |
