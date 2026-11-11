# Discovery workshop: air

| Field | Value |
|-------|-------|
| Product | AnyCompany Air website and app (book, check in, manage trips). Fictional sample company |
| Users | Leisure travellers (about 60% of passengers), frequent flyers (about 25%), corporate accounts (about 15% of passengers, a third of revenue, about 40 accounts) |
| People in the room | Head of digital (product owner), engineering lead (digital platform), UX designer, customer service operations lead, head of corporate accounts; commercial director at kickoff and readout |
| Pods | None: one team |
| Business metric | Self-service rebooking rate for disrupted passengers: **12%** (12.2% measured: 42,775 of 350,108), May to mid-October 2026 |
| Data input | `production`, in `discovery/data/` (1 May to 15 October 2026), including telemetry |
| Engagement reference | E2E-air |
| Storage | Working folder |
| Run type | **Demonstration**: unattended, on the bundled fictional sample data. The brief is not evidence for a build |
| Started | 2026-10-30 |

## Phase status
| # | Phase | Status | Key artifact |
|---|-------|--------|--------------|
| 1 | Signals | ✅ Complete | Top signal "disrupted passengers cannot choose their own new flight" (29/30) |
| 2 | Working Backwards | ✅ Complete | #1 self-service rebooking, 4.60, build first; riskiest assumption: passengers will confirm themselves instead of calling |
| 3 | Prototype | ✅ Complete | v2 chosen: live seats, "arrive by", honest "what moves with you", agency told |
| 4 | Validate | ✅ Complete | Commit, testing first: 3 conditions before the build (real-user test, reissue spike, call-back sizing) |
| 5 | Handoff | ✅ Complete | `handoff/discovery-brief.md` and `handoff/next-steps.md`; AI-DLC not started |

## What we know
- Disrupted passengers who cannot choose their own new flight is the top problem: 116 of 400 records, all sources and segments; 41% of alert openers tap Contact us; 12.2% self-serve.
- Booking conversion is above benchmark and flat; price and 3D seat map are low-severity; calls per 1,000 disrupted passengers are flat, so staffing is not the cause.
- The reissue service rejects 5.0% of changes.

## What we don't know
- Whether real passengers confirm a self-made change without calling (riskiest assumption).
- Whether offered alternatives can be reissued with seats and bags moved; agency tickets; call-back capacity and cost; seats-left freshness; AI cost.

## What we're assuming
- 30% self-service is reachable in one summer; the self-service NPS gap holds for choosers; the marker helps.

## Unattended choices
- **Config:** `config.md` with `unattended: true`, project `air`, engagement reference `E2E-air`, data `production` in `discovery/data/`, `default_days: 0` (the whole period). `storage` empty → working folder.
- **Setup:** product, people, metric, and candidate use cases taken from `README.md`. Recorded as a demonstration run.
- **Current-product map:** skipped; the folder holds no product codebase.
- **Team expectations:** written from each person's stated belief in `README.md`, before any analysis.
- **Signals review:** the challenges the people in the room would likely raise are recorded in the report with the data's answer; the engineering lead's reissue concern added to signal 1.
- **Personas:** four kept (Amara, Mei, Henrik as buyer, Jonas as satisfied customer). None set aside.
- **Scoring:** default weights; no overrides; added From Signals candidates #6 (late alerts) and #7 (travel desk rebooking) and dropped price (no build path in the digital product); 3D seat map failed the painkiller gate.
- **Taken forward:** #1 self-service rebooking (build first); #6 next in line.
- **Feature:** options 1 + 2 + 4 combined (choose and confirm, "fits what matters" marker, call-back fallback); the head of digital's recommendation idea kept as a marker that never books.
- **Riskiest assumption:** candidate 1 of 6 (passengers confirm themselves rather than call).
- **Lunch break draft:** not applicable (no break in an unattended run).
- **Prototype:** screen plan taken as drafted (5 screens, test moment on Review and confirm); team click-through reactions written as each role's likely view; critique findings 1, 2, 3, 4, 5, 7 fixed in v2, 6 and 8 not (out of scope, deferred). Seat holding not added (unconfirmed capability).
- **Validate:** re-score considered, none changed; v2 handed off; decision "commit, testing the riskiest assumption first", because the riskiest assumption is supported only by synthetic personas and feasibility is open.
- **Handoff:** route AI-DLC workshop (chosen because the run ends with the AI-DLC start command; the config names no route); team knowledge written to `aidlc/spaces/default/knowledge/aidlc-product-agent/discovery-personas.md` (no `aidlc/active-space`); `discovery/data/` added to `.gitignore`. Anonymized customer account codes from the data replaced with descriptions in saved artifacts. AI-DLC not started.
