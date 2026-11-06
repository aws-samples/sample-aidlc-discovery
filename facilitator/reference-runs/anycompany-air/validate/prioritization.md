# Problem prioritization: AnyCompany Air digital
400 feedback items from 6 sources, 1 May to 15 October 2026 (168 days), plus telemetry. Scores from `signals/signal-summary.md`; this is the backlog of problems the brief carries, separate from the use case scoring.

| Rank | Problem | Frequency | Severity | Reach | Score | Trend | Effort | Confidence |
|------|---------|:---------:|:--------:|:-----:|:-----:|:-----:|:------:|:----------:|
| 1 | Disrupted passengers cannot choose their own new flight | 10 | 10 | 9 | **29** | ↑ in summer (8 records in May, 33 in July), seasonal | L | HIGH |
| 2 | Disruption alerts arrive late in peak months and lead nowhere | 6 | 8 | 8 | **22** | ↑ in July and August (p95 about 11 → 41 min) | S to M | MEDIUM |
| 3 | Delayed and lost bags cannot be tracked | 7 | 7 | 5 | **19** | → (12 in May, 11 in August) | L | MEDIUM |
| 4 | Price feels high next to low-cost carriers | 6 | 3 | 7 | **16** | → | Outside digital | MEDIUM |
| 5 | Booking flow friction (upsell steps, multi-city, payment retries) | 6 | 3 | 6 | **15** | → (conversion flat at 3.1%) | M | HIGH |
| 6 | Loyalty points and status confusing | 5 | 4 | 3 | **12** | → | M | MEDIUM |
| 7 | 3D seat map request | 3 | 1 | 3 | **7** | → | L | MEDIUM |

Trend for rank 1 follows disruption volume: the rate per disrupted passenger is flat. Effort is a rough estimate for the team's discussion, not an engineering estimate.

## Quick wins
- **#2 Late alerts:** high score and a contained fix in a known service (provider throttling in July and August). Next in line in the scoring; do before summer 2027.
- Small fixes found in the data, outside the scored use cases: cancellation vouchers that work online (REV-0011, CALL-0034), the tracing reference error page (CALL-0030, SOC-0065), app and website showing different point balances (CALL-0070, SOC-0060).

## Big bets
- **#1 Self-service rebooking:** the decision of this workshop.
- **#3 Bag tracking:** real pain, but it needs baggage data the product does not hold today and does not move the agreed metric.

## Monitor
- Payment gateway timeouts (August only, error 0.57%; conversion unchanged).
- Reservations lookups slower than 2 seconds (2,972 UPSTREAM_SLOW): telemetry only.

## Defer
- #5 Booking redesign, #6 loyalty, #7 3D seat map: low severity, stable, and each has a cheap test in `signals/hypotheses.md`.
- #4 Price: for the commercial director, outside the digital product.

## Open hypotheses
From `risk-review.md`, still open:
1. **Riskiest assumption:** real disrupted passengers will confirm a self-made change without calling.
2. Every offered alternative can be reissued without a fare rule rejection.
3. Seats and bags reliably move to the new ticket.
4. An agency-booked ticket change shows on the agency's record.
5. Call-backs can be kept on a peak July day, and their cost per call.
6. "Seats left" can be shown current to the minute.
7. Passengers who rarely use the app, and passengers with assistance needs, can complete the flow.
8. The self-service NPS gap holds for passengers who choose.
9. The AI cost per ranking, and whether the marker raises or lowers confirmation.
