# Next steps: Choose My Flight (working name)
Decision: **commit, test the riskiest assumption first** (2026-10-29; to confirm with the commercial director at the readout). Route: AI-DLC workshop (confirmed by the team, 2026-10-29). Demonstration run on fictional sample data.

## Start the build
Do not start the full build until the conditions below pass. When they do:
1. Copy or commit the `discovery/` and `aidlc/` folders into the repository where the team will build. (AWS Quick does not run AI-DLC.)
2. In that repository, run:
   ```text
   aidlc config --harness <claude | kiro | kiro-ide | codex | cursor | opencode | copilot>
   /aidlc workshop Read ./discovery/anycompany-air/handoff/discovery-brief.md and build what it describes, Choose My Flight (engagement Self-serve)
   ```
   Use `/aidlc classic` instead if the team continues on its own. Requires AI-DLC 2.10.0 or later.

The reissue spike and the home-airport voucher rule (condition 2) come before the pilot and can use the brief as their starting document.

## Conditions before the build
| # | Condition | Who checks | By when |
|---|-----------|------------|---------|
| 1 | At least 6 of 8 recently disrupted passengers choose a flight without help, reach a boarding pass in under three minutes, and would not call for anything. Gates the pilot | Head of digital, UX designer | 30-day follow-up |
| 2 | Reissue spike reports, including complex bookings; the home-airport voucher rule works | Engineering lead | 30-day follow-up |
| 3 | Hamburg to Milan pilot, 4 weeks or 500 disrupted passengers: at least 40% of those who see the options accept one with no call about that booking before departure | Head of digital | 90-day follow-up |

If a gate fails, decide pivot or park at that follow-up.

## Follow-ups
**7-day**
- Confirm the design partners; size the corporate revenue at risk (head of corporate accounts).
- Ask the design partners what their travel desk sees after a traveller rebooks.

**30-day**
- The 8 walk-throughs of prototype v3 (`prototype/index.html`) with recently disrupted passengers (head of digital, UX designer). Ask each: "What would you still call us about?"
- Reissue spike and home-airport voucher rule (engineering lead).
- Can hotel vouchers be issued without an agent; does a call-back within the hour hold at peak (customer service operations lead)?
- Security review of booking reference plus surname for rebooking, and contact details on agency bookings (engineering lead).
- Head of digital sets the Assumed items: 30- and 60-day interim targets, the 10% call-after-rebooking target, kill criteria, and NF-8 message timing (after the message audit).
- Bring evidence for the deferred use cases: drop-off by booking step (booking), repeat calls per bag case (bags), points call volume (loyalty).

**90-day**
- Hamburg to Milan pilot result against the 40% gate (head of digital).

Open hypotheses to take to real customers: section 14 of the brief. To survey real users on them, ask for the Discovery survey job.
