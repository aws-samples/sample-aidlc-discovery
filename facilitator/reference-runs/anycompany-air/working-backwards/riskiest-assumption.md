# Riskiest assumption: self-service rebooking for disrupted passengers

## Candidates (claims labeled Assumed or Needs evidence)
1. Passengers will choose and confirm a new flight themselves, instead of calling, when the screen lets them.
2. Showing what moves with them (seats, bags, everyone together) is enough for them to trust the change.
3. Reissue failures can be caught and handed to an agent without leaving passengers without a ticket.
4. The "fits what matters" marker helps rather than distracts or misleads.
5. 30% self-service rebooking is reachable in one summer.
6. Call-back capacity is enough in peak months.

## The one the team takes forward (unattended default)
**Assumption:** When disrupted passengers can see what each option means for them and choose one, most of them will confirm a new flight in the app themselves rather than tap Contact us to have an agent do it or check it.

**Why it is the riskiest:** Everything else rests on it. If passengers still call to check, or do not trust a change they made themselves, call volume and the self-service rate barely move, and the 30% North Star fails even with perfect systems. Today 41% of alert openers tap Contact us although they can see the alternatives. That shows they want another flight. It does not show they would trust the app to make the change. Assumed. Candidate 3 (reissue failures) matters as much for the build, but the engineering spike can settle it with data. Only customers can settle this one.

**What the prototype must show:** the moment between Choose and Confirm on the review screen. The passenger sees the new flight, everyone on the booking, seats together, and bags moved, then decides whether to tap Confirm or Contact us. The prototype keeps Contact us visible on that screen, so the choice between them is real. The journey step it is meant to change is `alternatives_viewed` → `contact_us_tapped` (68 of every 100 alternatives viewers today).

**How we will judge it in Validate:**
- *Supports it:* every persona confirms without asking to call, and names what made them trust it (all together, bags shown, boarding passes). In the 30-day real-user test, at least 7 of 10 recently disrupted passengers confirm without tapping Contact us.
- *Contradicts it:* personas or real users say they would still call "to make sure", or they hesitate on missing information (fare difference, extras, agency booking), and fewer than 5 of 10 confirm.
