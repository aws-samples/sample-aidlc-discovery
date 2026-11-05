# AnyCompany Air: AI-DLC Discovery Workshop

> **Demonstration run.** AnyCompany Air and its data are fictional sample material. This workshop and its Discovery brief are a demonstration, not evidence for a build.

## Scope

| Item | Value | Status |
|------|-------|--------|
| Project | anycompany-air | Confirmed |
| Engagement reference | Self-serve | Confirmed |
| Product | AnyCompany Air website and app: book, check in, manage trips | Confirmed |
| Who uses it | Leisure travellers (~60% of passengers), frequent flyers (~25%), corporate account travellers (~15% of passengers, ~1/3 of revenue) | Confirmed |
| People in the room | Head of digital (product owner), Engineering lead (digital platform), UX designer, Customer service operations lead, Head of corporate accounts; Commercial director at kickoff and readout | Confirmed |
| Pods | None: one group | Confirmed |
| Business metric | Self-service rebooking rate for disrupted passengers | Confirmed |
| Baseline | 12% (May to mid-October 2026). Disrupted = cancelled or delayed > 2 h | Confirmed |
| Data input | production | Confirmed (fictional sample) |
| Data location | `discovery/data/` (10 CSV files, 1 May to 15 Oct 2026) | Confirmed |

## Candidate use cases the team brings

1. Self-service rebooking (head of digital)
2. Booking flow redesign (head of digital)
3. Bag tracking (engineering lead)
4. Loyalty points visibility (head of digital)
5. 3D seat map (UX designer)

## Phase status

| # | Phase | Status | Key artifact |
|---|-------|--------|--------------|
| 0 | Setup | ✅ Complete | PROJECT.md: one group, metric 12% baseline |
| 1 | Signals | ✅ Complete | Team agreed: work on disruption. Top signal "disrupted passengers cannot rebook themselves" (28/30); 3 challenges recorded, 11 research hypotheses |
| 2 | Working Backwards | ✅ Complete | Taken forward: self-service rebooking (4.60, build first). WB answers and features A+B+C ("Choose My Flight") confirmed; North Star 35% self-service and 25 calls per 100 within 90 days, target June 2027 pending reissue spike. PR/FAQ reviewed; readiness GREEN. Speed target < 3 min. PRD accepted (7 P0); no-fee policy confirmed. Riskiest assumption: passengers offered real choices quickly will choose and trust it enough not to call. Thresholds: supports ≥6/8 real disrupted passengers; contradicts ≥3/8. Reissue and booking-reference security to Validate. GTM draft accepted; owners set (design partners and revenue at risk: head of corporate accounts, 7-day; 8 walk-throughs: head of digital and UX designer, 30-day; reissue spike: engineering lead) |
| 3 | Prototype | ✅ Complete | v2 current (v1 + call-back copy: line opens at 07:00). Team accepted the 3 plan changes; Daniel's path only if the critique needs it. Bag and "final" claims to the reissue spike. Line hours 07:00–22:00 (call-back by hour queued). Persona critique on v2: all chose and trusted; threat is a second reason to call. v3 built (hotel voucher [Needs evidence], e-ticket no., dates, reference hint, call-back by hour). Riskiest assumption widened: no need to call for anything else. Findings 2, 4 to Validate; 7 waits |
| 4 | Validate | ✅ Complete | Re-walk of v3 and four risks drafted: valuable supported (removing calls open), usable/feasible/viable open. New: automatic hotel voucher wrong at a home airport. Feasible open until the spike. Vouchers only away from home airport (for the build). Pre-mortem: team's 5 reasons; new gap: no PRD target for message timing. Success criteria drafted. **Decision: commit, test first.** Gates: 6/8 walk-throughs + reissue spike (30-day), then Hamburg–Milan pilot (4 weeks or 500), ≥40% of those shown options accept with no call before departure (head of digital, 90-day). Home-airport voucher rule in condition 2. Hand off v3. Interim targets, kill criteria, NF-8 message timing: Assumed, head of digital sets at 30-day; head of digital owns adoption. GTM completed (open). Prioritization saved. Commercial director confirms at readout |
| 5 | Handoff | ✅ Complete | Discovery brief (15 sections, route AI-DLC workshop, confirmed by the team 2026-10-29) and next-steps written; personas in AI-DLC team knowledge; discovery/data/ in .gitignore |
