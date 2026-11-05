# Problem prioritization: AnyCompany Air website and app
Validate, 2026-10-29. From the Signal Analysis Report (400 text records, 6 sources, 1 May to 15 October 2026) and the risk review. Scores are Frequency + Severity + Reach (1 to 10 each, max 30), taken from the Signals scoring. Effort is a rough draft for the engineering lead to confirm. Demonstration run on fictional sample data.

| Rank | Problem | Freq. | Sev. | Reach | Score | Trend | Effort | Confidence |
|------|---------|:-----:|:----:|:-----:|:-----:|:-----:|:------:|:----------:|
| 1 | Disrupted passengers cannot rebook themselves | 10 | 9 | 9 | 28 | → (rate stable at ~42 calls per 100; volume doubles in summer) | L | HIGH |
| 2 | Passengers cannot see where a delayed bag is | 6 | 6 | 5 | 17 | → (7 of 13 delayed-bag calls in May; too few to call a trend) | M | MEDIUM |
| 3 | Booking flow friction (upsells, multi-city, payments) | 5 | 3 | 6 | 14 | → (conversion stable 3.08–3.17%) | M | MEDIUM |
| 4 | Fares feel high to leisure travellers | 4 | 4 | 5 | 13 | Unknown | n/a (commercial) | MEDIUM |
| 5 | Frequent flyers cannot trust points and status | 4 | 4 | 3 | 11 | Unknown | M | MEDIUM |
| 6 | No 3D seat preview | 3 | 1 | 3 | 7 | Unknown | M | LOW |

Use case scoring (a separate ranking of the team's candidates) took #1 forward; booking scored 3.00 after the team's pain override, above bags at 2.55.

- **Quick wins:** none confirmed. Small booking fixes (upsell steps, payment retries) may be; measure drop-off by step first.
- **Big bets:** #1, Choose My Flight (committed, test first).
- **Monitor:** #2 bags (repeat calls per case, research hypothesis 6); #5 loyalty.
- **Defer:** #3 until drop-off data (hypotheses 7, 10); #4 is commercial; #6 failed the gate (upgrade attach-rate data, hypothesis 9).

## Recommended next actions
1. Run the two gates for #1 (walk-throughs, reissue spike, then the Hamburg to Milan pilot).
2. Pull drop-off by booking step and repeat calls per bag case for the 30-day follow-up.

## Open hypotheses (from the risk review)
1. Riskiest assumption: passengers choose a flight and need to call for nothing else.
2. Reissue and fare rules without an agent, including complex bookings; bags follow; booking final.
3. Hotel vouchers without an agent, only away from the home airport.
4. Travel desks see the change or call to reconcile.
5. Message timing: soon enough before the good flights fill.
6. Booking reference plus surname safe for rebooking; contact details on agency bookings.
7. Share of passengers who never self-serve; desk queues.
8. Call-back within the hour at the summer peak.
9. Corporate revenue at risk.
