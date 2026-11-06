# Decision: self-service rebooking for disrupted passengers ("Choose My Flight")

**Decision:** **Commit, test the riskiest assumption first.**

**Reason (the team's words, head of digital, 2026-10-29):** Disruption is the biggest and most painful problem in the data, and it is the metric we agreed. The personas chose and trusted v3, but only real passengers can show they won't call, and reissue is unproven.

**Evidence:**
- **Supported:** passengers want it (valuable): 118 of 400 records, 37 asking to choose themselves, holds up to three hours, survey +4 in the app against −58 through the call centre, four corporate notes tying renewal or a tender to disruption. Every disrupted persona chose a flight without help in the prototype (synthetic).
- **Contradicted:** none. Partly: an automatic hotel voucher is wrong at a passenger's home airport (re-walk of v3); the build rule is vouchers only away from the home airport.
- **Open:** the riskiest assumption; usable with real passengers; feasible until the reissue spike reports; viable until corporate revenue at risk is sized; travel desks reconciling; message timing; security of booking reference plus surname; hotel vouchers without an agent.

**Conditions before the build:**
| # | Condition | Who checks | By when |
|---|-----------|------------|---------|
| 1 | At least 6 of 8 recently disrupted passengers choose a flight without help, reach the boarding pass in under three minutes, and say they would not call for anything. Gates the pilot | Head of digital and UX designer | 30-day follow-up |
| 2 | Reissue spike reports, including complex bookings; **and the home-airport voucher rule works (hotel vouchers only when the passenger is away from their home airport)** before the pilot starts | Engineering lead | 30-day follow-up |
| 3 | One-route pilot, Hamburg to Milan, 4 weeks or 500 disrupted passengers, whichever first: at least 40% of disrupted passengers who see the options accept one, with no call about that booking before departure | Head of digital | 90-day follow-up (moved from 60 days so a slipped gate does not break it) |

**Next:** walk-throughs and spike now; pilot after both pass; full build after the pilot. The 90-day follow-up counts from today; the 90-day targets count from full launch. After full launch, the 90-day targets apply: self-service rebooking 12% to 35%, rebooking calls 42 to 25 per 100 disrupted passengers. If gate 1 or 3 fails, the team returns to the evidence and decides pivot or park at that follow-up.

**Prototype handed off:** v3

**Decided by:** head of digital, engineering lead, customer service operations lead, head of corporate accounts, UX designer, 2026-10-29. To confirm with the commercial director at the readout.
