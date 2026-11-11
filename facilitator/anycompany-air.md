# AnyCompany Air: facilitator notes

> **Spoilers.** This file explains what the data was designed to show. Participants should not read it before the workshop.

## 1. The story

The team arrives believing the booking flow, prices, or call centre staffing are the problem. The data shows that the airline works well when flights run to plan, and fails people at the moment a flight is disrupted: nobody can rebook themselves, so they wait on hold or queue at a desk while the good alternative flights fill up. That moment drives detractors, call volume, and corporate accounts that are trialling a competitor.

## 2. The designed truths

All counts come from `scripts/samples/anycompany-air.py`. The 400 qualitative records split as follows.

| Theme | Role in the story | Total | Reviews | Calls | Social | NPS | Corporate notes | Agencies |
|-------|-------------------|------:|--------:|------:|-------:|----:|----------------:|---------:|
| Disruption with no self-service rebooking | The real top problem | 113 | 12 | 42 | 18 | 22 | 9 | 10 |
| Bag tracking | A real secondary pain | 45 | 8 | 18 | 8 | 7 | 2 | 2 |
| Booking flow redesign | The loud request | 45 | 14 | 6 | 5 | 6 | 8 | 6 |
| Cheaper fares | Loud, and not this team's to fix | 33 | 8 | 2 | 10 | 8 | 3 | 2 |
| Loyalty points | A small, real pain for frequent flyers | 27 | 6 | 9 | 3 | 5 | 2 | 2 |
| 3D seat map | The distractor | 16 | 6 | 0 | 6 | 2 | 2 | 0 |
| On-time flights rated well | Counter-evidence | 55 | 15 | 0 | 10 | 25 | 3 | 2 |
| Other and noise | Noise | 66 | 11 | 33 | 10 | 5 | 1 | 6 |

How each truth is built:

- **Disruption is spread thinly.** No single channel shows it whole. In the call centre it is split across six contact reasons: Cancellation 13, Rebooking 13, Missed connection 6, Refund request 4, Hotel and meal voucher 3, Schedule change 3. That makes "Delayed baggage" (13) look like the top single reason, while disruption accounts for 42 of 110 calls. Records cluster in July and August, when disruption peaks.
- **The corporate risk is in the account notes.** 9 of 30 notes are about disruption, several with renewal threats, a competitor trial, and travellers rebooking with other airlines at their own cost ("the AnyCompany tax"). Two notes say outright that booking is fine and disruption is the problem.
- **The loud request has weak evidence.** Booking flow complaints are mild (review ratings 2 to 4, NPS scores 5 to 8) and about upsells, multi-city, and payments. Web conversion is stable at 3.12% against a 3.00% benchmark.
- **The distractor is a wish, not a pain.** Every 3D seat map record is positive in tone (ratings 4 and 5, NPS 8 to 10). Nobody would notice if it never shipped.
- **Counter-evidence.** 55 records praise on-time flights, crew, and the app for booking and check-in.

The quantitative files agree with the qualitative data:

- **Operations:** 350,108 disrupted passengers from May to mid-October. Self-service rebooking rate 12.2%, between 10.6% and 12.6% each month. 418 rebooking calls per 1,000 disrupted passengers.
- **NPS by flight outcome:** on time +44, delayed -22, cancelled -56.
- **NPS of disrupted passengers by rebooking channel:** app +4, website -2, call centre -58, airport desk -62.

### The telemetry

`discovery/data/telemetry/` holds what the systems recorded, by day: RUM journey steps (`rum-journeys-daily.csv`), backend spans (`spans-daily.csv`), the top error codes (`errors-top.csv`), and `journey-map.csv`, which maps each step to its RUM view and backend route. Generated with its own seed by the same script; the numbers below come from it.

1. **The silent top problem.** About 72% of disrupted passengers open the alert in the app or on the web; 60% of those reach the alternative flights, and 68% of those tap **Contact us**, a median of about 80 seconds after seeing them. Those taps are about 70% of the 418 rebooking calls per 1,000 disrupted passengers. The routes behind the journey return **no server errors**: it fails as designed, so no error dashboard shows it. `suggestion_kept`, today's only self-service action, matches the 12.2% self-service rate. Feedback and telemetry agree: **Known**.
2. **The trap: payment timeouts.** On six of the busiest days in August, `POST /payments` has p95 latency of 4.2 to 5.2 seconds and 1.5% to 2.1% errors (`GATEWAY_TIMEOUT` in `errors-top.csv`), the loudest thing on any dashboard. Payment-to-confirmation stays at 0.80 to 0.84 every month, August included, and August conversion is the highest of the period. Real, small, and the engineering-led choice. One review mentions card payments failing.
3. **Feasibility evidence: reissue errors.** The agents' tool, `reissue-service`, fails 5.0% of 129,265 reissues (4.0% to 4.8% outside summer, 5.2% to 6.1% in July and August), mostly `FARE_RULE_MISMATCH`, plus `EMD_NOT_REASSOCIATED` (extras not moved to the new ticket). This matches the feedback records about reissue errors and wrong fees, and backs the engineering lead's spike: self-service built on this service inherits the failures.
4. **Telemetry only: late alerts.** `disruption.alert.delay_from_event` shows a median of about 9 minutes and a p95 of about 41 minutes from the disruption to the alert in July and August (2.5 and 10.5 minutes in June), with `PROVIDER_THROTTLED` in `errors-top.csv` for the same months. Nobody complains about the delay itself, but it explains why the good alternatives are gone when people look. A silent signal: a pre-mortem reason and a candidate requirement for message timing.
5. **Counter-evidence.** The booking journey is healthy: steady drop-off at every step, conversion above the benchmark.
6. **What backend telemetry alone cannot see.** `alert_opened` and `contact_us_tapped` exist only in RUM (`journey-map.csv`, source `rum`). Without RUM, a team sees the alternatives being fetched but not that people give up and call.

## 3. What Signals should find

The Signal Analysis Report should rank disruption first by frequency, severity, and reach, with bag tracking second. It should show that booking flow and price complaints are frequent but low in severity, and that most customers rate the airline well when flights run to plan.

How the team's likely expectations compare:

- **The head of digital** (booking flow is the priority): mostly contradicted. The complaints exist but are mild, and conversion is above benchmark.
- **The commercial director** (customers complain about price): partly supported. Price complaints are real, mostly from leisure travellers on social media, but they are not this team's to fix, and they are not what drives detractors.
- **The operations lead** (more agents in summer): supported as a symptom. The calls are real, but the evidence points at removing the need to call rather than at answering faster.
- **The head of corporate accounts** (listen to corporate customers): supported. Corporate notes carry the strongest disruption signal.

With the telemetry, the report should also have a **Say and do** table: disruption in both (Known); booking-flow friction mostly in feedback while the journey is healthy; payment errors in telemetry with almost no complaints; late alerts in telemetry only. The engineering lead's belief that nothing big is wrong is supported by the error rates and contradicted by the journey.

## 3b. Candidates from Signals, personas, and the AI feature block

**Candidates from Signals.** Before the gate, the skill adds two or three candidates from themes the team's five do not cover. Runs choose different ones; any of these is a good pick, as long as each is kept or dropped with a reason:
- **Agencies and corporate travel desks cannot rebook disrupted travellers** (agency escalations and account notes). Usually kept, and scored second or deferred next in line.
- **Rebookings fail after they are made** (reissue errors, extras not moved). Often merged into self-service rebooking as feasibility evidence and a P0 requirement.
- **Disruption alerts arrive late** (telemetry: a median of about 9 minutes, p95 about 41, in July and August). Kept and deferred, or folded into rebooking as a message-timing requirement.
- **The payment step** (telemetry): kept only if it scores low. It must not outrank rebooking: the August timeouts are the trap.
- **Fares feel high** (29 records, mostly mild). Dropped: fares are the commercial team's decision.

**Buyer and end user.** For corporate travel, the buyer and the end user are different people: the travel manager chooses the airline and judges value, cost, and duty of care; the traveller uses the app and judges whether rebooking works. Expect a persona for each. For leisure travel they are the same person, and the skill should say so.

**The AI feature block.** Self-service rebooking includes the head of digital's assistant, which recommends the best new flight and explains why, so it is an AI feature and the PRD gets the block. A good one:
- **First-draft prompt:** job (recommend one flight from the available options for what the passenger says matters, and explain why in one sentence), tone (calm, short, no jargon), inputs (the disrupted booking, the passengers, the flights with seats, what the passenger said), output (one recommendation, one reason, two alternatives), must not (promise compensation, recommend a flight without seats for everyone, invent a policy).
- **Evaluation cases** from the quotes and personas: typical (a business traveller who must arrive before a morning meeting; a family of four who must sit together; a passenger who keeps the airline's suggestion), edge (a tight connection; only next-day options, so the passenger needs a hotel; a booking made by an agency), negative (asks how much compensation they will get; asks to fly to a different city; asks for a flight that has no seats left). Five to ten in total, at least two negative.
- **Sample outputs** on the prototype's options screen, including one negative case, so the persona critique reacts to what the assistant says, not to a placeholder.
- **AI quality target** in Validate, for example: a reviewer accepts at least 8 of 10 typical cases, and no negative case passes. It is also a row in the GTM adoption and success table.

## 4. Expected scoring

With the default weights and the self-service rebooking rate as the business metric.

| Candidate | Gate | Pain | Outcome | Reach | Fit | Feasibility | Adoption | Weighted | Confidence | Decision |
|-----------|------|-----:|--------:|------:|----:|------------:|---------:|---------:|------------|----------|
| Self-service rebooking | Pass | 5 | 5 | 4 | 4 | 3 | 5 | 4.45 | High | Build first |
| Bag tracking | Pass | 4 | 1 | 3 | 3 | 3 | 5 | 2.95 | Medium | Defer, next in line |
| Booking flow redesign | Pass, weakly | 2 | 1 | 3 | 3 | 4 | 4 | 2.50 | Medium | Defer, close to drop |
| Loyalty points visibility | Pass | 2 | 1 | 2 | 3 | 4 | 4 | 2.35 | Medium | Drop |
| 3D seat map | **Fails** the painkiller and outcome tests | | | | | | | | | Drop at the gate |

Notes on the scores:

- Self-service rebooking reaches **High** confidence because the evidence comes from five independent channels plus two quantitative sources: the operations data and NPS by rebooking channel.
- Feasibility is a 3 that the engineering lead has to confirm. The app already shows alternative flights after a cancellation (several records say so), but accepting one changes the reservation.
- Business outcome is scored against the agreed metric, the self-service rebooking rate, so every other candidate scores 1 on outcome however real its pain. Runs vary by a few tenths on the other dimensions.
- With the telemetry, feasibility for rebooking has evidence: the reissue errors. Reach and the outcome baseline come from the RUM journey.
- Bag tracking is a strong second. Expect the team to want to merge it with rebooking as "the disruption experience". Score problems, not features: they are different problems with different owners.

## 5. The likely riskiest assumption

Disrupted passengers will rebook themselves in the app when they are offered real choices quickly, instead of calling. If they still call, the feature removes no queue.

What the prototype should test: the moment a cancellation notice arrives, with three alternative flights and a one-tap confirmation.

## 6. A good decision

**Commit**, with the riskiest assumption still open, so **commit to testing first**. Conditions before the build, for example: on one route, at least 40% of disrupted passengers who see the options accept one without calling.

Good success criteria:

- The self-service rebooking rate rises from 12% to 35% within 90 days of launch.
- Rebooking calls fall from 418 to under 250 per 1,000 disrupted passengers.
- NPS on cancelled flights improves from -56.
- With the telemetry, measured the same way at 30, 60, and 90 days: the share of disrupted sessions that reach a rebooked confirmation without `contact_us_tapped`, and the alert delay p95 under 10 minutes at peak.

First adopters for the GTM section are frequent flyers and corporate travellers, who already use the app; corporate travel managers are the channel to reach them.

## 7. Traps

- **Reading the contact reason codes at face value.** "Delayed baggage" looks like the top call reason. Disruption only becomes visible when the six disruption codes are added up.
- **Taking NPS by rebooking channel as proof.** Passengers who self-serve may have simpler trips. The difference supports the idea, but it is correlation; the pilot is the test.
- **Treating price as a candidate.** Price complaints are real, but fares are the commercial team's decision, and this team cannot move them.
- **Skipping the counter-evidence.** The airline is not broadly disliked. On-time flights score +44, which is why the problem is so specific.
- **Reading the error dashboard as the priority list.** The payment timeouts are the loudest errors; the top problem has none. An engineering-led team picks the dashboard's problem.
- **Taking the Contact us drop-off as proof of what people want.** It shows they did not self-serve; only the feedback says they wanted to.
- **Treating telemetry as a replacement for feedback.** Without the feedback, the late alerts and the drop-off have no "why".
- **The assistant designing the reservation integration.** Feasibility names the unknown, accepting a change to a booking, and the engineering lead judges it. No architecture in the brief.

## 8. Expectations for automated tests

```yaml
expectations:
  top_signal: "rebook | disruption | disrupted | cancel"
  loud_request: "booking flow"
  distractor_fails_gate: "3D seat map"
  build_first_or_learn: "self-service rebooking"
  data_input: production
  say_and_do: true
  telemetry_trap: "payment"
  telemetry_only: "alert | notification"
  feasibility_evidence: "reissue"
  signals_candidates: "2"
  ai_feature_block: true
```
