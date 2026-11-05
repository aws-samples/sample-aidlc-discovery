# Persona critique: Choose your flight (prototype v1)
Each persona walked through `v1.html` in its usual context. Unattended run: the critique is synthetic and stands in for both the personas and the team's reading of it.

## Amara Okafor
**[Persona: Amara]** Walking through on my Android phone at the gate, two tired children next to me.
- **Walk-through:**
  - *Alert:* clear. "Cancelled" in red and the button straight under it. I would tap Choose at once.
  - *Choose a flight:* the marked flight is exactly what I want: tonight, all four together. "Keep us together" is already ticked, and that's right for us. The 13:05 that says "3 seats left, not enough for your group of 4" saves me a call. But I see "4 seats together" and my first thought is: will they still be there when I press Confirm? On the phone, the good flights went while I waited.
  - *Review:* the four names and seats 14A to 14D are what would make me trust it. "2 checked bags: Move with you". I want to believe it, but after the last time I would want to know what happens if they don't.
  - *Failed:* "We saved your choice" is good, but a call-back "by 17:55" while I am boarding with kids? I'd want a text too.
- **Pain solved:** being split and stuck on hold ("Our family got split across two flights after a cancellation and we couldn't fix it online"; "Spent the evening on hold instead of with my family"). **Pain not solved:** landing at 23:55 with two children, with no help to get home or a hotel, and nothing on the screen about it.
- **Workflow fit:** fits. One hand, a few taps. The chips are fine because one is already ticked.
- **Switching:** I'd stop calling if the boarding passes show up straight away. I'd go back to the phone if Confirm ever left me with no ticket.
- **Riskiest assumption:** **holds**, if the screen tells me plainly whether the seats are still there and the bags really move. Otherwise I tap Contact us "to make sure".
- **Day-one adoption:** **8/10**, because it solves the worst evening I have had with this airline.

## Mei Tanaka
**[Persona: Mei]** Walking through on my iPhone in the taxi queue after a missed connection.
- **Walk-through:**
  - *Alert:* fine. "See my options later" is pointless for me.
  - *Choose a flight:* the chips do not fit me. "Arrive tonight" is not my question. I need "arrive by 13:30". Without it I'm comparing arrival times by eye, which is the thing I want the app to do. The arrival time on the right is good.
  - *Review:* I check two things: is my aisle seat kept, and is my bag on the new ticket. It says "Move with you". If that's ever wrong, I'm on the phone again ("The new ticket wasn't issued").
  - *Confirmed:* I need my company's travel agency to see this, or my travel desk will rebook me a second time. Nothing here says it does.
- **Pain solved:** "I just want to choose my own flight." Yes. **Pain not solved:** my travel desk not knowing; extras going missing.
- **Workflow fit:** fits, if I can say "arrive by" in one tap. Typing a time is fine.
- **Switching:** I'd stop "calling immediately before the good flights fill up" if the confirmation is instant and the seat count is live.
- **Riskiest assumption:** **holds for me** if seats and bags are stated honestly. I'll confirm in seconds.
- **Day-one adoption:** **9/10.** This is the button I've asked for in three calls this month.

## Henrik Sørensen
**[Persona: Henrik]** Reviewing the desktop view as the buyer, for the February tender.
- **Walk-through:**
  - *Desktop options:* a table my travellers can read on a laptop at a hotel, good. The marker's reason is a sentence I can show my board.
  - *Confirmed:* no mention of the travel management company. My duty-of-care team needs to know where travellers are. If the change does not reach us, we may rebook twice.
  - *Failed:* a call-back is better than our desk calling the corporate line one traveller at a time, but I need to know it scales on a summer day.
- **Pain solved:** "average time to rebook over two hours" (ACC-0018), if travellers use it. **Pain not solved:** visibility for my desk ("where travellers are during disruptions", ACC-0012); bulk rebooking for groups.
- **Workflow fit:** fine for travellers. My own workflow is unchanged, which is the deferred candidate #7.
- **Switching:** I'd put it in the tender response if my agency sees the change.
- **Riskiest assumption:** **unclear**: travellers will confirm, but some will still call the corporate line if they think their booking belongs to the agency.
- **Day-one adoption (as buyer, recommending it to travellers):** **7/10**, because it fixes the traveller's side and leaves mine for later.

## Jonas Becker (satisfied today)
**[Persona: Jonas]** Clicking through on my Android phone on a normal Friday.
- **Walk-through:** none of this shows up on a normal trip, which is how I want it. If my flight were cancelled, the alert, the marked flight, and Confirm would be about as many taps as booking.
- **Pain solved:** none today; I have not been disrupted. Assumed: I would expect it the first time I am.
- **Workflow fit:** fits; it uses the trip screen I know.
- **Switching:** nothing to switch from.
- **Riskiest assumption:** **holds**. I'd never call if the app can do it.
- **Day-one adoption:** **6/10**, only because I don't need it until the day I do.
- **What does it change that already works, and what would I lose?** Nothing, as long as the trip screen stays the same on normal days and the "What matters most?" chips stay optional. If the app started pushing the "Recommended for you" style into booking, I'd find it pushy.

## What the critique shows
| # | Finding | Personas | Points to risk | Fix in the iteration? |
|---|---------|----------|----------------|-----------------------|
| 1 | Unsure whether the seats are still there between Choose and Confirm | Amara, Mei | Usable, Valuable (riskiest assumption) | **Yes.** Show live seats left on each option and on review, and say plainly that seats are secured when you confirm. Holding seats was considered and **not** added: it depends on a capability nobody has confirmed (Needs evidence, engineering lead) |
| 2 | Chips miss "arrive by a time" | Mei | Usable | **Yes.** Replace "Arrive tonight" with "Arrive by…" |
| 3 | "Bags move with you" is trusted only if it is honest when they don't | Amara, Mei | Feasible (835 EMD_NOT_REASSOCIATED), Valuable | **Yes.** Show "what moves with you" per item, and an honest state on an option where extras cannot move |
| 4 | Agency or travel desk not told about the change | Mei, Henrik | Viable (corporate renewals) | **Yes**, as a line on the confirmation. Whether the agency record updates is Needs evidence (AGY-0013) |
| 5 | Call-back while boarding: wants a text too | Amara | Usable; call-back capacity Feasible | **Yes**: add a text message line. Call-back capacity stays Needs evidence for the customer service operations lead |
| 6 | Late arrival with children, no help getting home or a hotel | Amara | Valuable | **No.** Vouchers and hotels are P2, out of scope; kept as an open question |
| 7 | "See my options later" is not useful | Mei | Usable | **Yes**: removed |
| 8 | Travel desk visibility and bulk rebooking | Henrik | Valuable (buyer) | **No.** Deferred candidate #7 |

Synthetic personas, not customers: test these findings with real users in the follow-up.

## Fixed in v2
Findings 1, 2, 3, 4, 5, and 7 were fixed in `v2.html` (see `versions.md`). Findings 6 and 8 were not, for the reasons above.
