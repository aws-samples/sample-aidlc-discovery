# Next steps: Choose your flight
Decision: commit, testing the riskiest assumption first (see [../validate/decision.md](../validate/decision.md))

> Demonstration run on fictional sample data. AI-DLC was not started; the build is a separate session.

## Start the build
Only once the conditions below are met:
1. Copy or commit the `discovery/` and `aidlc/` folders into the repository where the team will build (`discovery/data/` is in `.gitignore` and stays out).
2. In that repository, run:
   ```text
   aidlc config --harness <claude | kiro | kiro-ide | codex | cursor | opencode | copilot>
   /aidlc workshop Read ./discovery/air/handoff/discovery-brief.md and build what it describes, Choose your flight (engagement E2E-air)
   ```
   Use `/aidlc classic` instead of `/aidlc workshop` if the team continues on its own. Requires AI-DLC 2.10.0 or later.

## Conditions before the build
1. At least 7 of 10 recently disrupted passengers confirm a new flight in prototype v2 without tapping Contact us, including one who rarely uses the app. UX designer with the head of digital, by the 30-day follow-up.
2. A replay of one month of offered alternatives through ticket reissue shows at least 99% can be confirmed with seats and bags moved, or names the cases for the call-back fallback. Engineering lead, by the 30-day follow-up.
3. Call-back capacity for a peak July day is sized, with a cost per call. Customer service operations lead: cost per call by the 7-day follow-up, capacity by the 30-day follow-up.

## Follow-ups
- **7 days:** cost per rebooking call (customer service operations lead); legal review of the refund wording booked (head of digital).
- **30 days:** real-user test of [prototype v2](../prototype/index.html) with 8 to 10 recently disrupted passengers, including one who rarely uses the app and one who needs assistance; show it to the three design partners (head of corporate accounts); reissue spike and agency-ticket check (engineering lead). Open hypotheses to take to real customers: 1, 4, 7, 8, 11 in the brief's section 14. **discovery-survey** can help survey real users on them.
- **At the pilot:** success criteria 1, 2, 4, and 5 read from the same RUM journey measures as the baseline.

## Roadmap: Now, Next, Later (for the product owner)
**Now**
- *Disrupted passengers cannot choose their own new flight* → self-service rebooking rate (12% → 30%), rebooking calls per 1,000 disrupted (about 415 → 300).
  1. Real-user test of v2 passes (condition 1).
  2. Reissue spike passes (condition 2).
  3. Call-back capacity sized (condition 3).
  4. Pilot against success criteria 1, 2, 4, 5; then general availability against criterion 3.

**Next**
- *Disruption alerts arrive late in peak months and lead nowhere* (4.00, Medium) → minutes from event to alert in July and August; Contact us per alert. Moves up with: proof that provider throttling is the cause and how many seats are lost by alert time (engineering lead, 30-day follow-up).
- *Travel desks and agencies cannot see or rebook disrupted travellers* (3.15, Medium) → corporate renewals; time to rebook for corporate travellers. Moves up with: design partners' reaction to v2 and whether agency records update (head of corporate accounts, engineering lead, 30-day follow-up).
- *Delayed and lost bags cannot be tracked* (2.55, Medium) → baggage-related calls. Moves up with: repeat calls per baggage case and whether tracing data can be shown (engineering lead, 60-day follow-up).

**Later**
- *Booking flow friction* (2.45, dropped): conversion is above benchmark and flat. Comes back if an A/B test removing one upsell page lifts conversion by more than 0.1 point (signals hypothesis 10).
- *Loyalty points and status confusing* (2.35, dropped): moves loyalty calls only. Comes back if loyalty calls grow or app and website balances keep disagreeing.
- *3D seat map* (failed the painkiller gate): all mentions were wishes. Comes back if a seat photo test on extra-legroom seats lifts the upgrade take rate (signals hypothesis 9).
- *Price perception* (dropped: outside the digital product): passed to the commercial director as context.
