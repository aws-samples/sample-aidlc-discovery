# Use case scoring: air
Weights: pain 25, outcome 25, reach 15, fit 10, feasibility 15, adoption 10 (defaults; no sponsor shift: unattended run)
Business metric agreed at setup: **self-service rebooking rate for disrupted passengers, 12% (12.2% measured, 42,775 of 350,108), May to mid-October 2026.**

## Candidates
| # | Use case (problem) | Who | Business metric | Owner | Source |
|---|--------------------|-----|-----------------|-------|--------|
| 1 | Disrupted passengers cannot choose a new flight themselves and have to call or queue | Passengers whose flight is cancelled, delayed over 2 h, or who miss a connection ([[amara]], [[mei]]) | Self-service rebooking rate | Head of digital | Team |
| 2 | The booking flow looks dated, has too many upsell steps, and lacks multi-city | Everyone who books on web or app ([[jonas]]) | Web booking conversion | Head of digital | Team |
| 3 | Passengers with a delayed or lost bag cannot see where it is | Passengers with delayed or lost bags | Baggage-related calls | Engineering lead | Team |
| 4 | Frequent flyers find points and status progress confusing or missing | Frequent flyers | Loyalty-related calls | Head of digital | Team |
| 5 | Seat buyers cannot see what a seat is like before paying | Anyone choosing a seat | Seat upgrade revenue | UX designer | Team |
| 6 | Disruption alerts arrive late in peak months and give passengers nothing to act on | Disrupted passengers | Self-service rebooking rate | Engineering lead | From Signals |
| 7 | Corporate travel desks and agencies cannot see or rebook their disrupted travellers | Travel managers and agencies ([[henrik]]) | Self-service rebooking rate; corporate renewals | Head of corporate accounts (build: head of digital) | From Signals |

## From Signals
| Candidate | Evidence | Kept or dropped | Reason |
|-----------|----------|-----------------|--------|
| 6. Late, empty alerts | Alert delay p95 about 11 min, about 41 min in July and August; PROVIDER_THROTTLED 955; "Delay notification at 10:30, then nothing" | Kept | Telemetry-only signal no team candidate covers; same metric |
| 7. Travel desk and agency rebooking | 12 of 30 account notes, 10 of 30 agency escalations; renewals tied to disruption | Kept | Buyer side of the top signal; no team candidate covers it |
| Price perception | 36 records, 9%, low severity | Dropped | Pricing is outside the digital product; no build path or owner in the room. Passed to the commercial director as context |

## Gate
| # | Passed | Reason if not |
|---|--------|---------------|
| 1 | Yes | |
| 2 | Yes | Passes narrowly: 43 records of mild friction and a metric. Scored so the comparison is visible |
| 3 | Yes | |
| 4 | Yes | |
| 5 | **No** | **Painkiller:** all 16 mentions are wishes, not pain ("Not a complaint, but…", "Curiosity, not a requirement", average rating 4.7). Customers would not notice if it never shipped. Kept as open hypothesis 9 in `signals/hypotheses.md`, with a cheap test: get the seat upgrade take rate and A/B test a seat photo on extra-legroom seats |
| 6 | Yes | Not merged into #1: different cause (notification capacity) and a fix that is useful even without self-service choice |
| 7 | Yes | Not merged into #1: different user (travel desk, agency) and different surface (portal, feed) |

## Scores
| # | Pain | Outcome | Reach | Fit | Feas. | Adopt. | Weighted | Confidence | Decision |
|---|:----:|:-------:|:-----:|:---:|:-----:|:------:|:--------:|------------|----------|
| 1 | 5 | 5 | 5 | 5 | 3 | 4 | **4.60** | High | **Build first** |
| 6 | 4 | 3 | 5 | 4 | 4 | 5 | **4.00** | Medium | Defer, next in line |
| 7 | 4 | 3 | 2 | 5 | 2 | 3 | **3.15** | Medium | Defer |
| 3 | 4 | 1 | 2 | 3 | 2 | 4 | **2.55** | Medium | Defer |
| 2 | 2 | 1 | 5 | 2 | 3 | 3 | **2.45** | High | Drop |
| 4 | 3 | 1 | 2 | 2 | 3 | 4 | **2.35** | Medium | Drop |

Weighted = Σ(score × weight) ÷ 100.

## Evidence per score
**1. Self-service rebooking**
- Pain 5: 116 of 400 records, all 6 sources; NPS verbatims average 1.9; calls average 38 min; customers leave ("I have started booking another airline for that route"). Known
- Outcome 5: this is the business metric itself; 102,456 Contact us taps and 108,316 alternatives views that did not end in a kept suggestion are the headroom. Known
- Reach 5: every disrupted passenger (350,108 in the period), including corporate travellers, the highest-value segment. Known
- Fit 5: four corporate renewals or tenders tied to disruption; doing nothing costs customers now. Known (renewal notes); strategy fit Assumed, team to confirm
- Feasibility 3: alternatives endpoint exists with 0 errors and p95 425 ms; keep-suggestion route exists; but reissue service rejects 5.0% (FARE_RULE_MISMATCH, TICKET_LOCKED, EMD_NOT_REASSOCIATED) and p95 2.6 s. Engineering lead to confirm. Assumed
- Adoption 4: 60% of alert openers already reach the alternatives screen; choosing is one step beyond what they do today. Known (telemetry); acceptance Assumed

**6. Late, empty alerts**
- Pain 4: a small number of direct quotes, but alerts that lead nowhere lose passengers the best seats ("call immediately before the good flights fill up"). Known
- Outcome 3: earlier alerts give more time to self-serve, but without a Choose action they just send people to Contact us faster. Assumed
- Reach 5: every disrupted passenger receives an alert (334,118 sent). Known
- Fit 4: supports #1. Assumed
- Feasibility 4: a capacity and provider issue in a known service. Assumed, engineering lead to confirm
- Adoption 5: no change for users. Known

**7. Travel desk and agency rebooking**
- Pain 4: renewals at risk; groups rebooked one by one by phone. Known
- Outcome 3: rebookings by agents and travel desks may not count as passenger self-service. Assumed
- Reach 2: about 40 corporate accounts and partner agencies. Known
- Fit 5: corporate is a third of revenue; tender in February. Known
- Feasibility 2: new portal actions and a disruption feed to outside systems. Assumed
- Adoption 3: travel desks need a new workflow. Assumed

**3. Bag tracking**
- Pain 4: 45 records, average NPS 3.1, repeat calls. Known
- Outcome 1: moves baggage calls, not the self-service rebooking rate. Known
- Reach 2: passengers with a delayed or lost bag only; no volume data. Assumed
- Fit 3: "Every airline in 2026 has bag tracking". Known (customer claim)
- Feasibility 2: needs baggage tracing data the product does not hold today; no baggage telemetry. Assumed
- Adoption 4: fits the trip screen. Assumed

**2. Booking flow redesign**
- Pain 2: 43 mild records ("Website feels old but works"), average rating 3.0. Known
- Outcome 1: no link to self-service rebooking; and its own metric, conversion, is 3.1% against a 3.0% benchmark and flat. Known
- Reach 5: every booker. Known
- Fit 2: four corporate accounts said booking is not a renewal factor. Known
- Feasibility 3: existing flow. Assumed
- Adoption 3: [[jonas]] and other satisfied bookers would have to relearn the flow. Assumed

**4. Loyalty visibility**
- Pain 3: 27 records, recurring. Known
- Outcome 1: moves loyalty calls, not the agreed metric. Known
- Reach 2: frequent flyers only (19 of 27). Known
- Fit 2. Assumed
- Feasibility 3: balance mismatch between app and web suggests a data sync issue. Assumed
- Adoption 4. Assumed

## Overrides
| # | Dimension | Draft | Team | Reason | When |
|---|-----------|-------|------|--------|------|
| – | – | – | – | Unattended run: no team overrides; every draft score taken as the default and recorded as such | Working Backwards |
| 1 | Feasibility | 3 | 3 | Re-score considered after Validate: the risk review left feasibility open (reissue 5.0% errors, agency tickets, call-backs) but found nothing that lowers it below "some data or platform work needed". No change | after Validate |

## Taken forward
**#1 Self-service rebooking for disrupted passengers, build first, by the whole team (no pods).**
Next in line: #6 late, empty alerts (4.00, Medium), revisit at the 30-day follow-up; the prototype includes the alert as the entry point so its effect stays visible.
