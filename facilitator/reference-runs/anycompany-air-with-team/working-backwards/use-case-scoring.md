# Use case scoring: anycompany-air
> Demonstration run on fictional sample data. Status: **CONFIRMED by the team, 2026-10-29.** Every score reviewed; one override (candidate 2, pain).

Business metric (from setup): self-service rebooking rate for disrupted passengers, baseline 12% (May to mid-October 2026).

Weights: pain 25, outcome 25, reach 15, fit 10, feasibility 15, adoption 10. Defaults, no sponsor shift (confirmed by head of digital, 2026-10-29). Fixed before scoring.

## Candidates
Each candidate brought by the team, rewritten as a problem.

| # | Use case (problem) | Who | Evidence from Signals | Business metric | Owner |
|---|--------------------|-----|-----------------------|-----------------|-------|
| 1 | Disrupted passengers can see alternative flights but cannot choose one themselves, so they phone or queue (team brought: "Self-service rebooking") | All three segments; corporate over-represented. Includes people rebooking for someone else (family, assistants, travel desks, agencies) | Top signal 28/30: 118 of 400 records, all 6 sources; 37 ask to choose themselves; 12.2% self-serve; ~42 calls per 100 disrupted; 62% of handle time; survey app +4 vs call centre −58 | Self-service rebooking rate (12%) | Head of digital |
| 2 | Leisure shoppers meet friction in the booking flow: upsell pages, multi-city only by phone, failing card payments, hard-to-read mobile calendar (team brought: "Booking flow redesign") | Mostly leisure web bookers | Signal 3, 14/30: 39 records, rating 3.1, survey 5.8; conversion 3.08–3.17%, above 3.0% benchmark | Web conversion rate (~3.1%) | Head of digital |
| 3 | Passengers with a delayed or lost bag cannot see where it is, so they call again and again (team brought: "Bag tracking") | Leisure and frequent flyers | Signal 2, 17/30: 45 records, all 6 sources; rating 2.0, survey 3.1; repeat calls; tracing links fail | Repeat baggage calls; bag-case survey score | Engineering lead |
| 4 | Frequent flyers cannot trust their points balance and status (missing points, app vs web mismatch, status expiring without warning) (team brought: "Loyalty points visibility") | Frequent flyers | Signal 5, 11/30: 28 records; 10 calls in sample | Loyalty call volume; frequent flyer retention | Head of digital |
| 5 | Seat choosers cannot see the seat they pay for, so upgrades may not sell (team brought: "3D seat map") | Spread across segments | Signal 6, 7/30: 15 mentions, from satisfied customers (rating 4.7, survey 9.5); no upgrade revenue data | Seat upgrade attach rate (no data) | UX designer |

## Merges (before the gate)
- Sub-problems of signal 1 (corporate and agency bulk rebooking, rebooking on someone else's behalf, unsuitable automatic rebooking, split families, out-of-hours help) are part of **candidate 1**, not separate candidates. They are the same problem for different people.
- "Booking flow redesign" is a solution; it is scored as the problem it would solve (candidate 2). It does not solve the disruption problem, so it is not merged into candidate 1.

## Gate (draft, for the team to confirm)
| # | Passed | Reason if not |
|---|--------|---------------|
| 1 | Yes | |
| 2 | Yes | Passes; note it is linked to conversion, not to the agreed metric, which will show in the outcome score |
| 3 | Yes | |
| 4 | Yes | |
| 5 | **No** | **Painkiller.** The people asking are already satisfied (rating 4.7, survey 9.5); account managers call it "curiosity, not a requirement". Customers would not notice if it never shipped. |

**Open hypothesis kept alive (candidate 5):** "A better seat preview would raise upgrade sales" (research hypothesis 9). Cheap test: get upgrade attach rates by route and aircraft; A/B test seat photos against today's seat map.

## Scores
Draft. Fit and feasibility are the team's to confirm; feasibility goes to the engineering lead.

| # | Pain | Outcome | Reach | Fit | Feas. | Adopt. | Weighted | Confidence | Decision (draft) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|---|
| 1 Disruption rebooking | 5 | 5 | 5 | 5 | 3 | 4 | **4.60** | High | **Build first** (all six scores confirmed by team, 2026-10-29) |
| 4 Loyalty trust | 3 | 1 | 3 | 3 | 3 | 5 | 2.70 | Medium | Defer (all six scores confirmed by team, 2026-10-29) |
| 3 Bag visibility | 3 | 1 | 2 | 3 | 3 | 5 | 2.55 | Medium | Defer (all six scores confirmed by team, 2026-10-29; owner agrees to defer behind rebooking) |
| 2 Booking friction | **4** (team override; draft 2) | 1 | 3 | 3 | 4 | 4 | **3.00** | Medium | Defer (pain overridden by head of digital; other five confirmed by team, 2026-10-29) |
| 5 Seat map | — | — | — | — | — | — | — | — | Failed gate (painkiller) |

## Evidence per score

### 1. Disrupted passengers cannot choose their new flight (4.60, High)
- **Pain 5:** 118 of 400 records (30%) in all 6 sources; holds of 50 to 175 minutes; review rating 1.5, survey 1.9; one corporate account trialling a competitor, travellers booking other airlines and claiming it back. Frequent, blocking, customers leave. [Known]
- **Outcome 5:** Directly the agreed metric: 12.2% self-serve today, ~42 rebooking calls per 100 disrupted passengers. Moving rebooking into the app moves the metric within 90 days. [Known] for the baseline; size of the lift [Needs evidence] (research hypothesis 1).
- **Reach 5:** All three segments (45 / 33 / 40 records); 350,108 disrupted passengers May to mid-October; corporate, the highest-value segment (~1/3 of revenue), over-represented. [Known]
- **Fit 5 (confirmed by team, 2026-10-29):** "Do nothing" is costing customers now: four corporate notes tie renewal, risk, or a tender to disruption; agencies reconsidering packages. Fit with the digital strategy itself [Assumed].
- **Feasibility 3 (confirmed by engineering lead, 2026-10-29):** The app and website already show alternative flights, so the options exist in the data [Known]. Letting the customer confirm one needs ticket reissue and fare rules; 13 records show reissue errors and wrong change fees today [Known]. Engineering lead: "3 is right, not lower. Showing alternatives is easy, we already do it. Reissuing the ticket and applying fare rules is the hard part, and that's where today's errors come from." **Condition: a spike on ticket reissue and fare rules before the team commits to a date.** Reissue reliability [Needs evidence].
- **Adoption 4:** Disrupted passengers already open the app and see alternatives; 410 already rebook there [Known]. Not 5: Helena-type passengers will not self-serve, so a path for rebooking on someone's behalf is needed (team challenge 3) [Needs evidence].

### 4. Frequent flyers cannot trust points and status (2.70, Medium)
- **Pain 3:** 28 records; missing points, app vs web mismatch, status expiring without warning; 10 calls. Recurring friction with a workaround (calling). [Known]
- **Outcome 1:** No link to the self-service rebooking rate. Moves loyalty calls and retention only. [Known]
- **Reach 3:** Frequent flyers (~25% of passengers), one significant segment; 19 of 28 records are theirs. [Known]
- **Fit 3 (confirmed by team, 2026-10-29):** Supports the loyalty programme; no evidence of competitive pressure. [Assumed]
- **Feasibility 3 (confirmed by team, 2026-10-29):** Mismatched balances suggest a data sync problem between systems. [Assumed]
- **Adoption 5:** Members already check balances in the app; no change in how they work. [Assumed]

### 3. Passengers cannot see where a delayed bag is (2.55, Medium)
- **Pain 3:** 45 records in all 6 sources; rating 2.0, survey 3.1; repeat calls ("third time calling"). Severe for those affected, with a workaround (calling). [Known]
- **Outcome 1:** No link to the self-service rebooking rate; moves repeat baggage calls only. [Known]
- **Reach 2:** Only passengers with a delayed or lost bag; 7 of 13 delayed-bag calls in May. A small share of passengers. [Known] for records; share of passengers [Assumed]
- **Fit 3 (confirmed by team, 2026-10-29):** Supports self-service; no competitive pressure in the data. [Assumed]
- **Feasibility 3 (confirmed by engineering lead, 2026-10-29):** Engineering lead: "tracing status exists internally but there's no customer-facing way to show it yet." Tracing links already fail. [Known] (engineering lead) for the internal status; integration effort [Assumed]
- **Adoption 5:** A status page fits how customers already look for information. [Assumed]

### 2. Leisure shoppers meet booking friction (3.00 after override; draft 2.50; Medium)
- **Pain 2 (draft):** 39 records, rating 3.1, survey 5.8; several say "fine" or "works". Friction, rarely blocking. [Known]
- **Pain 4 (team override, head of digital, 2026-10-29):** "Our reviews mention it all the time." Check against the review file: 10 of 80 app and web reviews (12.5%) are about booking, average rating 3.1; 4 of the 10 say it is "fine", "OK", or "gets the job done"; none says the customer could not book or left. For comparison, 13 of 80 reviews are about disruption. Frequency in reviews is [Known]; severity at the level of 4 (frequent and close to blocking) is [Assumed]. Hypotheses 7 and 10 (drop-off by booking step) would show whether friction is blocking shoppers the feedback cannot see.
- **Outcome 1:** Linked to conversion, not to the self-service rebooking rate. Conversion already 3.08–3.17%, above the 3.0% benchmark. [Known]
- **Reach 3:** Leisure (~60% of passengers) is the main segment affected: 26 of 39 records. [Known]
- **Fit 3 (confirmed by team, 2026-10-29):** Head of digital: "booking is where we make money". Supports the strategy. [Assumed]
- **Feasibility 4 (confirmed by team, 2026-10-29):** Targeted fixes to an existing, working flow. [Assumed]
- **Adoption 4:** Small fixes keep the flow familiar; a full redesign would score lower. [Assumed]
- **Note:** The draft sat on the 2.5 boundary between Defer and Drop; after the pain override it is 3.00, inside Defer. At the 30-day follow-up, bring drop-off by booking step (research hypotheses 7 and 10) to test the override.

## Overrides
| # | Dimension | Draft | Team | Reason | When |
|---|-----------|-------|------|--------|------|
| 1 | Feasibility | 3 | 3 (confirmed) | Engineering lead: alternatives already shown; reissue and fare rules are the hard part and the source of today's errors | Scoring, 2026-10-29 |
| 2 | Customer pain | 2 | 4 | Head of digital: "Our reviews mention it all the time." Reviews: 10 of 80 about booking, avg rating 3.1, none blocking. Severity [Assumed]. Weighted 2.50 → 3.00; decision unchanged (Defer) | Scoring, 2026-10-29 |

## Conditions and open items carried forward
- **Reissue spike (candidate 1).** Before committing to a delivery date, the engineering lead wants a spike on reissuing the ticket and applying fare rules when a customer chooses a new flight. Carry to the riskiest assumption and the Validate risk review (feasibility risk). Owner: engineering lead. [Needs evidence]

## Taken forward
**Self-service rebooking for disrupted passengers** (candidate 1: disrupted passengers can see alternative flights but cannot choose one themselves). Weighted 4.60, confidence High, **build first**. Taken forward by the whole team (one group, no pods), 2026-10-29. Matches the framework's decision.

Carried with it:
- The reissue spike before any delivery date (engineering lead).
- A path for passengers who will not self-serve, and for rebooking on someone else's behalf (team challenge 3; personas Helena and Karim).

## Deferred, for the 30-day follow-up
| # | Use case | Weighted | Bring this evidence |
|---|----------|:---:|---|
| 2 | Booking friction | 3.00 | Drop-off by booking step; exit survey on abandoned searches (hypotheses 7, 10) |
| 4 | Loyalty trust | 2.70 | Points and status call volume; app vs web balance mismatch rate |
| 3 | Bag visibility | 2.55 | Repeat calls per bag case (hypothesis 6) |
| 5 | Seat map | Gate fail | Upgrade attach rate by route and aircraft (hypothesis 9) |
