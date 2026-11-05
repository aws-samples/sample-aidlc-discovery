# Signal Analysis Report: AnyCompany Air website and app
Data: production (fictional sample, demonstration run) | 400 text records from 6 sources (80 app and web reviews, 110 call centre contacts, 70 social posts, 80 post-flight survey comments, 30 corporate account notes, 30 travel agency escalations) plus 4 metric tables (operations, survey score by flight outcome, disruption survey score by rebooking channel, web booking funnel) | 1 May to 15 October 2026

> Method note: each record was assigned one primary theme by keyword rules, then reviewed by hand. Counts are accurate to within a few records. The call file is a sample of 110 contacts, not total call volume.

## Summary
The problem that matters most is what happens after a flight is disrupted: passengers can see alternative flights in the app and on the website but cannot choose one, so they phone or queue, and their experience collapses. Disruption and rebooking is the largest theme (118 of 400 records, 30%), the only one that appears strongly in all six sources and all three segments, takes 62% of agent handle time in the call sample, and is tied to corporate renewals at risk. Disrupted passengers who rebooked in the app score +4; those who rebooked through the call centre score −58. **[Known]**

## Theme overview

| Theme | Records | % | Leisure / FF / Corporate | Avg review rating (1–5) | Avg survey score (0–10) |
|---|---|---|---|---|---|
| Disruption and rebooking | 118 | 30% | 45 / 33 / 40 | 1.5 | 1.9 |
| Positive / no issue | 58 | 15% | 30 / 12 / 16 | 4.3 | 9.5 |
| Baggage | 45 | 11% | 21 / 17 / 7 | 2.0 | 3.1 |
| Booking flow | 39 | 10% | 26 / 6 / 7 | 3.1 | 5.8 |
| Price and fees | 29 | 7% | 20 / 4 / 5 | 2.4 | 5.8 |
| Loyalty | 28 | 7% | 4 / 19 / 5 | 2.3 | 5.8 |
| Seat (incl. 15 mentions of a 3D seat map) | 19 | 5% | 9 / 6 / 4 | 4.7 | 9.5 |
| Other (special assistance, general enquiries, comfort, admin) | 64 | 16% | 35 / 6 / 23 | 2.3 | 7.0 |

FF = frequent flyers. **[Known]**

## Top signals

Scored out of 10 each for frequency, severity, and reach. Scores are a draft for the team to challenge.

### 1. Disrupted passengers cannot rebook themselves (frequency 10, severity 9, reach 9, total 28/30)
- **Who:** all three segments: leisure 45, frequent flyers 33, corporate 40 records. Corporate is over-represented for its size. **[Known]**
- **Evidence:**
  - 118 of 400 records (30%), in all 6 sources: 43 calls, 22 survey comments, 18 social posts, 13 reviews, 12 of 30 corporate notes, 10 of 30 agency escalations. **[Known]**
  - 37 records say directly that the customer wanted to choose or change the flight themselves, or that the app or website only told them to call. **[Known]**
  - 61 records mention phoning, holding, or queuing at a desk; customers report holds of 50 to 175 minutes. **[Known]**
  - Operations: 350,108 disrupted passengers from May to mid-October; 12.2% rebooked themselves; about 42 rebooking calls per 100 disrupted passengers, every month. July and August doubled because disruptions doubled. **[Known]**
  - In the call sample, disruption calls are 39% of contacts and 62% of handle time, averaging 37 minutes against about 14 minutes for baggage or loyalty calls. **[Known]**
  - Disrupted passengers' survey score by rebooking channel: app +4 (410 responses), website −2 (260), call centre −58 (1,630), airport desk −62 (980). **[Known]** Harder cases may be more likely to call, so the gap is not all down to the channel. **[Assumed]**
  - Corporate: accounts flagged at risk or tying renewal or a tender to disruption handling (four notes), one account trialling a competitor, travellers of another booking any airline and claiming it back. Agencies: partners reconsidering packages, charging clients a disruption fee, rebooking groups one at a time by phone. **[Known]**
- **Related sub-problems** (records can count in more than one):
  - Automatic rebooking onto unsuitable flights (6 to 21 days later, long layovers when a direct exists): 9 records. **[Known]**
  - App or website errors and conflicting information during disruption (error page, ticket not reissued, change fee charged, refund shown only as a voucher): 13 records. **[Known]**
  - No information or no help out of hours (cancelled at night, line closed until 07:00): 17 records. **[Known]**
  - Groups and families split or rebooked one by one: 11 records. **[Known]**
  - Corporate travel desks and agencies cannot rebook in bulk or see where travellers are: 7 records. **[Known]**
- **Quotes:**
  - "Delays happen, I get it. What I don't get is why I can see alternative flights on the website but can't move myself onto one." (corporate traveller, review)
  - "My 08:15 to Brussels was cancelled. The app tells me to call you and I've been waiting 50 minutes. … I saw those in the app too, why couldn't I just pick one?" (frequent flyer, call centre)
  - "Booking is fine. Fix what happens when flights get cancelled." (corporate customer, quoted in an account note)
- **Root cause:** the app and website show disruption and alternatives but offer no action to choose one, and automatic rebooking chooses without the customer. **[Assumed]**

### 2. Passengers with a delayed or lost bag cannot see where it is (frequency 6, severity 6, reach 5, total 17/30)
- **Who:** leisure 21, frequent flyers 17, corporate 7. **[Known]**
- **Evidence:**
  - 45 of 400 records (11%), in all 6 sources. **[Known]**
  - 18 calls in the sample, short (about 14 minutes average). Repeat calls are common ("third time calling"). 7 of the 13 "Delayed baggage" calls came in May. **[Known]**
  - Average review rating 2.0, survey score 3.1: severe for the people who have it. **[Known]**
  - Online claim forms and tracing references time out or show errors (5 records). **[Known]**
- **Quotes:**
  - "Five days and my suitcase is still 'being traced'. I have no idea where it is and no way to find out." (leisure traveller, review)
  - "The bag tag has a barcode, so somebody knows where it is. Why can't I?" (leisure traveller, review)
- **Root cause:** tracing status exists internally but is not shown to the customer. **[Assumed]**

### 3. The booking flow has friction, but it is not broken (frequency 5, severity 3, reach 6, total 14/30)
- **Who:** mostly leisure (26 of 39). **[Known]**
- **Evidence:**
  - 39 records (10%): too many upsell pages, multi-city only by phone, card payments failing, the calendar hard to read on a phone, bag and seat prices showing up late, a dated look. **[Known]**
  - Low severity: average rating 3.1, survey score 5.8. Several say "fine" or "works". **[Known]**
  - Web conversion is 3.08% to 3.17% every month, above the 3.0% industry benchmark in the file. **[Known]**
  - Corporate accounts say booking is not the issue: "fine, nobody complains"; asked about a redesign, "their questions were all about disruptions". **[Known]**
- **Quotes:**
  - "Took me 12 minutes to book a simple return because of all the upsell pages." (leisure traveller, review)
  - "Website feels old but works." (leisure traveller, survey)

### 4. Fares feel high, especially to leisure travellers (frequency 4, severity 4, reach 5, total 13/30)
- **Who:** mostly leisure (20 of 29). **[Known]**
- **Evidence:**
  - 29 records (7%) about fares, bag fees, and prices rising during search. Survey score 5.8: passives rather than detractors. **[Known]**
  - Agencies see price-sensitive leisure customers moving to low-cost carriers on short routes. **[Known]**
  - A corporate travel manager said disruption costs them more than the fare difference. **[Known]**
- **Quote:**
  - "Low-cost to Athens: 49 euros. AnyCompany Air: 149. Same airport." (leisure traveller, social)
- Pricing is a commercial decision, mostly outside the digital product. **[Assumed]**

### 5. Frequent flyers cannot trust their points and status (frequency 4, severity 4, reach 3, total 11/30)
- **Who:** frequent flyers (19 of 28). **[Known]**
- **Evidence:**
  - 28 records: missing or late points, the app and website showing different balances, status expiring without warning, partner and agency bookings not earning points. 10 calls in the sample. **[Known]**
- **Quote:**
  - "Status expired with zero warning. Thanks for the loyalty." (frequent flyer, social)

### 6. A 3D seat map is a nice-to-have from happy customers (frequency 3, severity 1, reach 3, total 7/30)
- **Who:** spread across segments. **[Known]**
- **Evidence:**
  - 15 mentions of a 3D seat map or cabin view: 6 reviews, 6 social posts, 1 survey comment, 2 corporate notes. **[Known]**
  - The people asking are satisfied: average review rating 4.7, survey score 9.5. Account managers record it as "curiosity, not a requirement" and "mentioned once, not raised again". **[Known]**
  - The data has no seat-upgrade revenue figures, so it cannot show whether upgrades sell poorly. **[Needs evidence]**
- **Quote:**
  - "Not a complaint, but a 3D seat preview would be amazing" (leisure traveller, social)

## What the team expected

| # | Team hypothesis | What the data shows | Verdict |
|---|---|---|---|
| 1 | Leisure web bookers complain about a dated booking flow (head of digital) | 39 complaints, mostly leisure, but low severity. Conversion is above the benchmark, and corporate customers say booking is fine. | Partly supported: the friction is real, but it is not the top problem |
| 2 | Customers complain mainly about fares (commercial director) | 29 records (7%), mostly leisure passives. Disruption is four times as frequent and far more severe. | Contradicted as the main complaint |
| 3 | Seat choosers can't see what they pay for, so upgrades don't sell; a 3D map would help (UX designer) | 15 requests for a 3D view, almost all from satisfied customers. There is no upgrade revenue data. | Contradicted as a problem; the upgrade-sales question is not settled |
| 4 | Corporate travellers have the most problems (head of corporate accounts) | Corporate travellers are 40 of the 118 disruption records, and 12 of 30 corporate notes are about disruption, several tied to renewals or tenders. | Supported, and the data names the problem: disruption |
| 5 | Summer call spikes; more agents is the answer (call centre lead) | The spike is real but follows disruption volume: calls per disrupted passenger stay at about 42 in 100 every month. Waits are long. The data has no staffing figures. | Spike supported; "more agents is the answer" not settled |
| 6 | No major problem in the app's booking and check-in (engineering lead) | Booking and check-in in the app draw praise. The app fails when a flight is disrupted. | Supported for booking and check-in; disruption is the gap |
| 7 | Lost and delayed bags are the biggest call reason (call centre lead) | "Delayed baggage" ties with "Cancellation" and "Rebooking" at 13 calls each, but all baggage calls total 18 against 43 disruption calls, and bag calls are about a third as long. | Contradicted |

**What would surprise the team:**
- *"If booking turned out not to matter."* (head of digital) Booking matters, but customers rate it as working. **[Known]**
- *"If customers wanted to change their own bookings in the app."* (engineering lead) This is the clearest request in the data: 37 records ask to choose or change a flight themselves after a disruption. **[Known]**

## Customer voices
1. "The delay wasn't the problem. Not being able to change my flight myself was." (leisure traveller, delayed flight, survey score 4 of 10)
2. "Flight to Seville cancelled at the gate. The app just said 'please contact us'. 170 minutes on hold to get moved to a flight the next afternoon. The flight itself was fine; the cancellation handling was a disaster." (corporate traveller, app review)
3. "Renewal call with a software customer. Their CFO missed a board meeting after a Lisbon cancellation and spent an hour on the phone. They are trialling a competitor on two routes. The ask is simple: let travellers rebook themselves in the app." (corporate account manager note)
4. "My parents are stuck in Nice after a cancellation and can't get through on the phone. They don't know how to use the app, and the app can't help anyway" (frequent flyer, social)
5. "The portal let us see the new automatic flight but not change it. Every change after a disruption is a phone call for us too." (partner travel agency escalation)

## Data gaps
- **People who never booked:** the feedback only covers people who booked or flew. Anyone who abandoned the booking flow, or switched airline without saying so, is invisible. The funnel shows 5.2% of searches book, but not why the other 95% do not, or at which step they leave. **[Needs evidence]** (team challenge 1)
- **Airport desks:** 980 survey responses rebooked there, but there are no desk transcripts or comments.
- **App and website behaviour:** no usage data on what disrupted passengers try to do, or where they drop off.
- **Call centre capacity:** no staffing levels, real wait times, or full-volume handle times, so the staffing option cannot be sized.
- **Seat upgrades:** no upgrade revenue or attach-rate data.
- **Corporate buyers:** travel managers and travel desks, who decide renewals, are heard only through account managers and agencies. Corporate travellers themselves do speak first-hand in 72 records. (team challenge 2)
- **Passengers who cannot or will not use the app:** no data on how many there are, or how they rebook today. **[Needs evidence]** (team challenge 3)
- **Season:** May to mid-October only, so there is no winter baseline. October is a half month.
- **Volume:** 400 text records. Enough to rank themes, but segment-level counts are small.
- **Channels:** no complaint emails or web forms.

## Team challenges (Signals review, 2026-10-29)

### 1. "The data only covers people who booked. How do we know booking isn't losing customers we can't see?" (head of digital)
**Verdict: valid gap. It weakens the verdict on team hypothesis 1 but does not reverse it.**
- True: no record comes from someone who abandoned a booking. **[Known]**
- What the funnel shows: 11.3 million sessions, 6.7 million searches (60%), 353,216 bookings. Search-to-booking is 5.1% to 5.4% and conversion is 3.08% to 3.17% every month, above the 3.0% benchmark in the file. **[Known]**
- What that means: a flow that drove many people away would usually show up as below-benchmark or falling conversion. It does neither. **[Assumed]** The file does not say how the benchmark is defined, so the comparison may not be like-for-like. **[Needs evidence]**
- Lost customers we can partly see: 1 record of a shopper leaving during booking ("Searched twice and the price went up 40 euros. Not booking.", about price); 6 records of customers or agencies switching airline after disruption. The invisible-customer problem applies to disruption too. **[Known]**
- To close it: drop-off by booking step, and a short exit survey on abandoned searches. Added as research hypothesis 10.

### 2. "Corporate travellers are heard second-hand. Their own voice is under-represented." (head of corporate accounts)
**Verdict: partly right. The report's data gap was imprecise and has been corrected.**
- Corporate travellers speak first-hand in 72 records (19 reviews, 27 calls, 13 survey comments, 13 social posts). 27 of those 72 (38%) are about disruption, more than the 30% across all records. **[Known]**
- The second-hand voice is the corporate buyer: travel managers and travel desks, who decide renewals, appear only through 30 account notes and 5 agency escalations. **[Known]**
- So the disruption signal holds in the travellers' own words, and the buyers' needs (bulk rebooking, knowing where travellers are) are **[Assumed]** until a travel manager confirms them. Research hypothesis 3 already tests this through interviews.

### 3. "Some passengers won't use an app at all. Self-service won't help them." (customer service operations lead)
**Verdict: valid. Recorded as a constraint on the use case and as research hypothesis 11.**
- Direct evidence is thin: 1 record of passengers who cannot use the app (the parents in Nice), 2 about less technical or elderly customers struggling with booking. **[Known]** How many disrupted passengers would never self-serve is unknown. **[Needs evidence]**
- Several records show people rebooking *for someone else*: two assistants calling to rebook a boss ("The online tool just says to call"), agencies wanting to rebook in their portal, corporate travel desks asking for bulk rebooking. Self-service does not have to mean the traveller on their own phone. **[Known]**
- Note that the parents in Nice also "can't get through on the phone": today neither channel works for them. **[Known]**
- If passengers who can self-serve stop calling, agents have more time for those who cannot. **[Assumed]**
- Implication for Working Backwards: a self-service rebooking concept needs a path for people who will not use it, and a way to rebook on someone else's behalf.
