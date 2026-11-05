# Go-to-market: Choose your flight
Demonstration run on fictional sample data. Drafted in Working Backwards; parts 4, 6, and 7 completed in Validate.

## 1. First adopters
**Required. Status: validated**
- **Segment:** corporate travellers and frequent flyers on the routes with repeated summer disruption (Stockholm, Oslo, Munich, Lisbon, Milan, Athens, Budapest in the feedback). Corporate is 15% of passengers and a third of revenue; 73 of 116 disruption records come from corporate travellers and frequent flyers. Known. They fly often enough to meet a disruption within weeks of launch, and they already act fast on alerts ("call immediately before the good flights fill up"). Known.
- **Size:** about 40 corporate accounts; frequent flyers are 25% of passengers. Known (README). Disrupted passengers in these segments per summer: Needs evidence.
- **How we reach them:** in product (the disruption alert itself); the corporate account team at quarterly reviews; partner travel agencies for agency-booked travellers.
- **Design partners (roles, not names):**
  1. The travel manager of a pharma account with about 3,000 travellers that sent a disruption report and asked for self-service rebooking (ACC-0018). Known.
  2. The travel manager of a banking account whose Q1 renewal depends on disruption handling (ACC-0015). Known.
  3. A partner travel agency that asked for a disruption feed and rebooking (AGY-0018). Known.

## 2. Positioning
**Required. Status: validated**
> For **disrupted AnyCompany Air passengers** who **can see other flights but have to call to change**, **Choose your flight** is a **self-service rebooking step in the app and on the website** that **lets them choose and confirm a new flight for everyone on the booking in minutes**. Unlike **waiting on hold or in a desk queue (50 to 175 minutes quoted; call centre NPS −58), or accepting a flight that does not work**, it **puts the choice with the passenger and shows before confirming what moves with them**.

Evidence: alternatives viewed 150,845, Contact us 102,456, holds quoted 50 to 175 minutes, NPS by channel. Known. The honest alternative for many is doing nothing (keeping the automatic pick, 17%); the benefit beats it only when the pick does not fit. Assumed.

## 3. Business model and pricing
**Hypothesis. Status: open**
- **Why it exists:** retention and cost, not new revenue. Included for every passenger at no charge; changing to an offered flight after a disruption is already free. Known (CALL-0045).
- **Retention hypothesis:** corporate accounts renew when disruption handling improves (four accounts tie renewal or tender to it). Needs evidence: renewal outcomes after launch. Owner: head of corporate accounts.
- **Cost hypothesis:** each self-service rebooking replaces part of a 38-minute call. At 30%, about 60,000 more self-service rebookings over a period like May to mid-October. Assumed. Cost per call: Needs evidence from the customer service operations lead.
- **AI cost to serve:** one ranking per disrupted booking that opens the screen, about 150,000 per half-year. Cost per active user per month: Needs evidence in the build; it has to stay well below the cost of the call it replaces. Owner: engineering lead.

## 4. Viability check
**Required. Status: validated** (every area has an owner and a concern; two concerns stay open questions)
| Area | Owner role | Main concern |
|------|-----------|--------------|
| Legal and compliance | Head of digital, with the airline's legal team | Passenger rights after cancellations and long delays: the screen must not steer passengers away from a refund they are entitled to. Refund stays visible through Contact us (P2 to bring into the app). Needs evidence: legal review of the wording |
| Privacy and security | Engineering lead | The marker uses booking details (passenger count, children, assistance needs). No names, contact or payment data go to the model (PRD). Where that processing happens is for the build |
| Sales | Head of corporate accounts | Changes no deals. Gives the account team an answer for four at-risk renewals and the February tender, only if agency bookings are included (open) |
| Support and success | Customer service operations lead | New questions: "I chose a flight but didn't get a boarding pass", call-backs from failed changes. Agents need the saved choice in front of them. Call-back capacity open |
| Marketing | Head of digital | A story to tell ("choose your own flight"), but only after the pilot proves it: promising it before reissue failures are handled would hurt the brand on the worst day |

## 5. Launch plan
**Hypothesis. Status: open**
| Stage | Who | Exit criteria |
|-------|-----|---------------|
| Internal | Call centre agents and digital team rebook test bookings; agents try it during real disruptions on behalf of passengers | No change that ends without a valid ticket; agents can explain it |
| Design partners | Travellers of the three design partners on their main routes | At least 60% of their disrupted travellers who view alternatives confirm or keep; travel managers say they would extend it |
| Limited release | 20% of disruptions on the pilot routes, compared with the rest | Contact us taps per alert opened under 25% for the pilot group; self-service NPS at or above 0 |
| General availability | All disruptions, app and web, before July 2027 | Pilot targets met; call-back capacity sized for peak |

**Enablement before limited release:** call centre agents briefed on the call-back queue and on what passengers see; corporate account team given a one-page explanation for travel managers; agencies told how changes show in the portal.

## 6. Adoption and success
**Required. Status: validated** (targets set; real-user results open)
| Item | Content |
|------|---------|
| Adoption owner | Head of digital (product owner on the product engineering team) |
| Adoption metric | (Choices confirmed + suggestions kept) ÷ alternatives viewed, among disrupted passengers in the release group. Baseline 28% |
| Leading indicators | Contact us taps per alert opened falling from 41%; median time on the alternatives step falling from 84 s; Contact us taps from the review screen under 15%; failed changes under 1% |
| Business metric | Self-service rebooking rate for disrupted passengers: baseline 12.2% (May to mid-October 2026) |
| AI quality | At least 9 of 10 typical and edge evaluation cases accepted by a reviewer; 0 negative cases pass (PRD AI feature block) |
| Targets | **30 days after pilot start:** adoption 45%, Contact us per alert 33%, right-first-time changes 99%. **60 days:** adoption 60%, Contact us per alert 25%. **90 days after general availability (end of September 2027):** self-service rebooking rate 30%, rebooking calls 300 per 1,000 disrupted passengers |
| Kill criteria | 60 days after pilot start, adoption below 40% **or** Contact us taps per alert opened above 35% **or** right-first-time changes below 97%: stop the rollout and return to Discovery on why passengers do not confirm |

## 7. Risks and open hypotheses
**Status: open**
1. Will corporate travellers whose tickets belong to an agency be able to use it, and will the agency's record update? Owner: engineering lead, head of corporate accounts.
2. Does the improvement change renewal outcomes for the four accounts that tied renewal to disruption? Owner: head of corporate accounts, at Q1 renewals.
3. What is the cost per rebooking call, and how much of it does a self-service rebooking save once call-backs are counted? Owner: customer service operations lead, by the 7-day follow-up.
4. What is the AI cost per ranking? Owner: engineering lead, in the build.
5. Does legal approve the wording on refund rights? Owner: head of digital.

## Status of all parts
| Part | Status |
|------|--------|
| 1. First adopters | **validated**: segment and design partners supported by the critique (Mei, Henrik) and account notes; partners not yet asked |
| 2. Positioning | **validated**: consistent with the press release and the persona critique |
| 3. Business model and pricing | **open**: no charge is settled; the retention and cost hypotheses need numbers |
| 4. Viability check | **validated** |
| 5. Launch plan | **open**: stages set; exit criteria depend on the reissue spike and call-back sizing |
| 6. Adoption and success | **validated** |
| 7. Risks and open hypotheses | **open** |
