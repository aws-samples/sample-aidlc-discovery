# Signal Analysis Report: AnyCompany Air digital (website and app)
Data: production | 400 feedback records from 6 sources (80 app and web reviews, 110 call centre contacts, 70 social posts, 80 NPS verbatims, 30 corporate account notes, 30 travel agency escalations), 4 operational and NPS tables, and 4 telemetry tables (RUM and backend spans, app and web) | 1 May to 15 October 2026

> Demonstration run: AnyCompany Air and every record are fictional sample data. This report is not evidence for a build.

## Summary
When a flight is cancelled or delayed by more than two hours, passengers can see other flights in the app and on the website but cannot choose one. They keep the flight the airline picked or they call. That accounts for the 12% self-service rebooking rate, the 38-minute calls, and the worst NPS in the data. It is the top theme in every source and every segment, it is what puts corporate renewals at risk, and the telemetry shows the same thing: 41% of passengers who open a disruption alert end up tapping Contact us, and that share stays the same every month. **[Known]**

## Inventory
| Source | Records | Notes |
|--------|---------|-------|
| App store, Google Play, web reviews | 80 | Ratings 1 to 5 |
| Call centre contacts | 110 | Reason, handle time, transcript snippet |
| Social posts | 70 | Public |
| NPS verbatims | 80 | Score and flight outcome |
| Corporate account notes | 30 | Customers appear as codes only |
| Travel agency escalations | 30 | Agencies appear as numbers only |
| Operations monthly, NPS by flight outcome, disruption NPS by rebooking channel, web booking funnel | 6 / 18 / 4 / 6 rows | Aggregates |
| Telemetry: journey map, RUM journeys daily, spans daily, top errors | 11 / 2,688 / 1,344 / 9 rows | RUM included for app and web on the disruption journey; booking journey on web only |

No names, emails, or booking references in the data. Customers appear as segment or code only. October is a half month (to 15 October).

## Theme counts (all 400 records)
| Theme | Records | Share | Sources (of 6) | Avg NPS score (verbatims) | Avg review rating | Avg call handle time |
|-------|---------|-------|----------------|---------------------------|-------------------|----------------------|
| Disruption rebooking and information | 116 | 29% | 6 | 1.9 (n=22) | 1.5 (n=12) | 38.1 min (n=42) |
| Positive (on time, crew, check-in) | 56 | 14% | 6 | 9.5 | 4.3 | – |
| Baggage (delayed, lost, claims) | 45 | 11% | 6 | 3.1 (n=7) | 2.0 (n=8) | 14.3 min (n=18) |
| Booking flow friction | 43 | 11% | 6 | 5.8 | 3.0 | 14.5 min (n=6) |
| Price | 36 | 9% | 6 | 5.8 | 2.4 | 11.0 min (n=2) |
| Loyalty points and status | 27 | 7% | 6 | 5.8 | 2.3 | 14.2 min (n=9) |
| 3D seat map request | 16 | 4% | 4 | 9.5 (n=2) | 4.7 (n=6) | – |
| Other (special assistance, invoices, cabin, food, Wi-Fi) | 61 | 15% | 6 | – | – | 14.5 min |

Disruption calls are 38% of call contacts but about 62% of call handle time in the sample. **[Known]**

## Top signals

### 1. Disrupted passengers cannot choose their own new flight (frequency 10, severity 10, reach 9, total 29/30)
- **Who:** all three segments: leisure 43, corporate 40, frequent flyer 33 of 116 records. Corporate travellers are over-represented against their 15% share of passengers. **[Known]**
- **Evidence:**
  - 116 of 400 records, in all 6 sources; disruption mentions peak in July (33) and August (30), the months with the most cancellations. **[Known]**
  - 350,108 disrupted passengers in the period; 42,775 (12.2%) rebooked themselves; 146,299 rebooking calls, steady at 401 to 424 calls per 1,000 disrupted passengers each month. **[Known]**
  - Telemetry, disruption journey (app and web): 251,453 alert opens → 221,187 trip views → 150,845 alternatives viewed (60%). From there, 42,529 kept the airline's suggestion (17% of alert opens) and 102,456 tapped Contact us (41%). Alternatives is the longest step in the journey (median 84 s): people read the options and cannot act on them. The kept-suggestion count matches the self-service rebookings (42,529 vs 42,775), so self-service today means accepting the airline's choice. **[Known]**
  - The shares hold month by month (Contact us 40.6% to 40.9% of alert opens in every month), so call volume rises with disruptions while the call rate per passenger is set by the product. **[Known]**
  - NPS by rebooking channel: self-service app +4, self-service web −2, call centre −58, airport desk −62. NPS for cancelled flights runs −53 to −61 each month, against +41 to +46 for on-time flights. **[Known]**
  - Automatic rebooking often picks flights that do not work: 15 and 21 days later, five-hour layovers when a direct flight exists, families split across two days (CALL-0020, CALL-0069, CALL-0077, CALL-0107, REV-0048, SOC-0051, AGY-0021). **[Known]**
  - Corporate: 12 of 30 account notes are about disruption; four accounts tie renewal or tender to it (a banking account: "renewal in Q1 depends on how we handle disruption"; one asks for a written plan before its February tender; a software account is trialling a competitor on two routes; one is flagged at risk). One account's travellers buy tickets on other airlines and claim them back ("the AnyCompany tax"). **[Known]**
  - Agencies: 10 of 30 escalations; the portal shows the new automatic flight but cannot change it; groups of 20 to 46 rebooked by phone one by one. **[Known]**
- **Quotes:**
  - "Delays happen, I get it. What I don't get is why I can see alternative flights on the website but can't move myself onto one." (app review, corporate, 1 star)
  - "The delay wasn't the problem. Not being able to change my flight myself was." (NPS, leisure, delayed, score 4)
  - "Booking is fine. Fix what happens when flights get cancelled." (corporate account note, travel manager)
- **Root cause:** the alternatives screen is read-only, and the only action is keeping the airline's automatic suggestion. Choosing another flight means a reissue that today is done by agents. **[Assumed]** The reissue service rejects 5.0% of requests (FARE_RULE_MISMATCH 3,985, TICKET_LOCKED 1,092, EMD_NOT_REASSOCIATED 835 extras not moved, TIMEOUT_GDS 514), so self-service choice depends on that service. **[Known measurement; effect on a self-service flow Needs evidence]**

### 2. Disruption alerts arrive late and lead nowhere (frequency 6, severity 8, reach 8, total 22/30)
- **Who:** disrupted passengers, worst in July and August. **[Known]**
- **Evidence:** the time from disruption event to alert sent (p95) is about 11 minutes in May, June, September, and October, and about 41 minutes in July and August. In those months the SMS and push provider throttled sends (PROVIDER_THROTTLED, 955). 1,452 alerts fell back to email after expired push tokens. The feedback describes alerts that bring no options ("Delay notification at 10:30, then nothing", "cancelled by text at 23:00 and the phone line opened at 07:00"). Customers say the good flights fill up while they wait ("Being stuck on hold while the good flights filled up"). **[Known]**
- **Quotes:**
  - "Delay notification at 10:30, then nothing. No new times, no options, no humans. Nice gate is chaos" (social, leisure)
  - "Pro tip if your AnyCompany Air flight gets cancelled: don't bother with the app, call immediately before the good flights fill up" (social, corporate)
- **Root cause:** notification capacity is sized for normal months, and the alert offers nothing to act on. **[Assumed]**

### 3. Delayed and lost bags cannot be tracked (frequency 7, severity 7, reach 5, total 19/30)
- **Who:** passengers with a delayed or lost bag; leisure 21, frequent flyer 17, corporate 7. **[Known]**
- **Evidence:** 45 records in all 6 sources; 18 of 110 calls; avg NPS 3.1, avg rating 2.0. Repeat calls and claim forms that time out or reject the tracing reference (CALL-0018, CALL-0030, CALL-0083, REV-0033, SOC-0065, SOC-0069). Corporate and agency mentions are low intensity ("Not a renewal issue"). No baggage telemetry was provided. **[Known]**
- **Quotes:**
  - "The bag tag has a barcode, so somebody knows where it is. Why can't I?" (Google Play, leisure, 3 stars)
  - "Put an AirTag in my suitcase because the airline won't tell me where it is. It's in Warsaw. The airline says it's 'being traced'." (social, frequent flyer)
- **Root cause:** tracing status is held by baggage services and not shown to customers. **[Assumed]**

### 4. Price feels high next to low-cost carriers (frequency 6, severity 3, reach 7, total 16/30)
- **Who:** mostly leisure (24 of 36). **[Known]**
- **Evidence:** 36 records (9%). Low severity: passengers mention price next to praise ("Love the airline, hate the prices"), and corporate travel managers say "disruption costs them more than the fare difference" (ACC-0026). Web booking conversion is 3.08% to 3.17% against an industry benchmark of 3.0%. **[Known]**
- **Quotes:** "Low-cost to Athens: 49 euros. AnyCompany Air: 149. Same airport." (social, leisure)
- **Root cause:** pricing strategy, outside the digital product. **[Assumed]**

### 5. Booking flow friction: upsell steps, multi-city, payment retries (frequency 6, severity 3, reach 6, total 15/30)
- **Who:** web bookers, mostly leisure. **[Known]**
- **Evidence:** 43 records, mostly mild (avg rating 3.0; "Website feels old but works"). Asks: fewer upsell pages, multi-city (phone only today), vouchers that work online, Apple Pay. Conversion is steady at 3.1% and above benchmark; the web funnel moves from extras to payment at 72% and from payment to confirmation at 80% to 84% every month. A payment gateway timeout in August (error rate 0.57% vs 0.20%) did not move conversion (3.17% in August). Four corporate accounts said a booking redesign would not change their renewal (ACC-0014, ACC-0021, ACC-0023, ACC-0024). **[Known]**
- **Quotes:** "Took me 12 minutes to book a simple return because of all the upsell pages." (app review, leisure, 2 stars)
- **Root cause:** accumulated upsell steps. **[Assumed]**

### 6. Loyalty points and status are confusing (frequency 5, severity 4, reach 3, total 12/30)
- **Who:** frequent flyers (19 of 27). **[Known]**
- **Evidence:** 27 records; missing or late points, app and website balances that disagree, status expiring without warning, agency bookings that drop the loyalty number. **[Known]**
- **Quotes:** "Loyalty app shows 3700 points, website shows something else" (social, frequent flyer)

### 7. 3D seat map request (frequency 3, severity 1, reach 3, total 7/30)
- **Who:** seat buyers; leisure 8, frequent flyer 6, corporate 2. **[Known]**
- **Evidence:** 16 records, all positive or neutral (avg rating 4.7, avg NPS 9.5): "nice touch", "would be cool", "Curiosity, not a requirement", "Mentioned once, not raised again". There is no seat upgrade revenue data, so a revenue effect is **[Needs evidence]**. **[Known]**
- **Quotes:** "Seat map is fine. A 3D view would be a nice touch like some other airlines have." (app review, leisure, 5 stars)

## Say and do
| Theme | What customers say | What the systems show | Reading |
|-------|-------------------|-----------------------|---------|
| Cannot choose a new flight | 116 records; "why I can see alternative flights on the website but can't move myself onto one" | 60% of alert openers view alternatives (median 84 s, the longest step); 17% keep the suggestion; 41% tap Contact us; steady every month. Alternatives endpoint: 0 errors | **Both (Known).** The journey fails by design, with no errors: the error dashboard would not show it |
| Long holds and call queues | "Hold music for 175 minutes so far"; disruption calls 38 min | 146,299 rebooking calls; 401 to 424 per 1,000 disrupted passengers every month | **Both (Known).** The call rate per passenger stays flat, so volume drives the queues |
| Rebooked onto flights that do not work | 7+ records: 15 or 21 days later, five-hour layovers, families split | Keep-suggestion endpoint takes only 42,529 of 150,845 who view alternatives | **Both (Known)** |
| Rebooking done but the ticket or extras are wrong | "The new ticket wasn't issued"; "app still shows the cancelled flight"; charged a change fee after a cancellation | Reissue service: 5.0% errors (6,428 of 129,265); 835 extras not moved; up to 5.6% in July and August | **Both (Known)** |
| Late, empty alerts | "Delay notification at 10:30, then nothing" | Alert delay p95 about 11 min normally, about 41 min in July and August (provider throttled) | **Both (Known)** |
| Baggage tracking | 45 records | No baggage telemetry provided | **Feedback only** |
| Booking flow | 43 records, mild | Conversion 3.1% vs 3.0% benchmark, flat; funnel step rates flat | **Both.** Telemetry says booking works: friction, not failure |
| Payment failures | "Payment failed twice, worked the third time" | August gateway timeouts (249), error 0.57%; conversion unchanged | **Both.** Real and small |
| Trips lookup slow | Not mentioned | 2,972 UPSTREAM_SLOW from the reservations system; p95 281 ms on trips endpoint | **Telemetry only.** Measurement Known; customer effect Assumed small |
| Price, loyalty, 3D seat | 36 / 27 / 16 records | Not covered by telemetry | **Feedback only** |

## What the team expected
| Team hypothesis | What the data shows | Verdict |
|-----------------|--------------------|---------|
| 1. Bookers put off by a dated booking flow (head of digital) | 43 mild mentions; conversion 3.1%, above benchmark and flat; four corporate accounts say booking is not a renewal factor | **Contradicted** |
| 2. Disrupted passengers cannot choose a new flight and must call (head of digital) | 116 records, all sources and segments; 41% of alert openers tap Contact us; 12.2% self-service | **Supported** |
| 3. Seat upgrades held back by a flat seat map (UX designer) | 16 mentions, all nice-to-have; no upgrade revenue data | **Not settled** (wanted, not a pain) |
| 4. Summer queues are a staffing problem (customer service operations lead) | Queues peak with volume, but calls per 1,000 disrupted passengers stay flat at about 415, and 41% of passengers who could self-serve tap Contact us | **Contradicted as the cause.** Agents treat the volume; the product sets the call rate |
| 5. Corporate problems hidden behind leisure feedback (head of corporate accounts) | 40 of 116 disruption records are corporate (34% vs 15% of passengers); renewals tied to disruption | **Supported** |
| 6. Customers mainly complain about price (commercial director) | 36 records (9%), fourth theme, low severity | **Contradicted** as the main complaint |
| 7. Post-booking changes are the riskiest systems (engineering lead) | Reissue service has the highest error rate of any service (5.0%) | **Supported** |
| 8. Baggage calls because bags cannot be tracked (engineering lead) | 45 records; repeat calls; no tracking | **Supported** (second theme) |
| 9. Loyalty calls because points and status are confusing (head of digital) | 27 records, mostly frequent flyers | **Supported** (smaller) |

## Customer voices
1. "Missed my connection in Prague because the first leg was late. The app knew. I got a push notification and then nothing: no new flight, no button, just 'call us'." (Google Play, leisure, 1 star)
2. "My 08:15 to Brussels was cancelled. The app tells me to call you and I've been waiting 50 minutes. … I saw those in the app too, why couldn't I just pick one?" (call centre, frequent flyer, 27 min)
3. "Renewal call with [a software account]. Their CFO missed a board meeting after a Lisbon cancellation and spent an hour on the phone. They are trialling a competitor on two routes. The ask is simple: let travellers rebook themselves in the app." (corporate account note)
4. "We're a family of 3 adults and two children. The new flight split us across two days." (call centre, frequent flyer, 31 min)
5. "My parents are stuck in Nice after a cancellation and can't get through on the phone. They don't know how to use the app, and the app can't help anyway" (social, frequent flyer)

## Data gaps
- No airport desk data, though 980 NPS responses came from desk rebookings; desk passengers are only visible in NPS and quotes.
- Booking journey RUM is web only; no app booking telemetry.
- No baggage telemetry, no seat upgrade revenue, no loyalty system data.
- The call after Contact us is not in the app's telemetry, so what happens after the tap is inferred from operations data.
- Travel agency and corporate notes are written by staff, not by travellers: second-hand voice.
- Passengers who gave up and did not rebook at all (the README's "or not at all") are not counted anywhere.
- October covers half a month.

## Review with the team (unattended run)
In an unattended run there is no team to challenge the report. The challenges recorded here are the ones the people in the README would most likely raise, with the answer from the data:
- **Head of digital:** "Booking is where we make money." The funnel is flat and above benchmark; no record ties booking friction to lost revenue. The report stands. Recorded as an open question for the booking team, outside this workshop.
- **Customer service operations lead:** "More agents would fix the summer." Agents would shorten holds. They would not change the 41% Contact us rate or the −58 call-centre NPS. Recorded.
- **Engineering lead:** "Reissue failures make self-service risky." Accepted: the 5.0% reissue error rate is added to signal 1 as a dependency and carried into scoring as a feasibility risk.
- **Under-represented:** passengers who rebook at the airport desk and passengers who do not use the app (SOC-0056). Added to data gaps.
