# PR/FAQ: Choose your flight
Demonstration run on fictional sample data. Written unattended as a straw-man for the team to read aloud and change.

## Press release

**Disrupted AnyCompany Air passengers can now choose their own new flight in minutes**

*Passengers whose flight is cancelled or delayed can pick and confirm a new flight for everyone on their booking in the app or on the website, without waiting for an agent.*

**1.** Lisbon, 1 June 2027. Passengers whose AnyCompany Air flight is cancelled, delayed by more than two hours, or whose connection is missed can now choose their new flight themselves in the AnyCompany Air app and on the website. Choose your flight shows the flights that can still get them there, lets them confirm one for everyone on the booking, and puts the new boarding passes on their trip. Passengers decide which flight works for them, and they no longer queue for an agent to make that change.

**2.** Every summer, hundreds of thousands of passengers have their plans broken by a cancellation or a long delay. Between May and mid-October 2026, 350,108 passengers were disrupted, and only 12% rebooked themselves. The rest called, queued at an airport desk, or gave up. Many could already see other flights on their phone but had no way to take one, so they waited on hold for up to three hours while the seats they wanted filled up. Families were split across flights, business travellers missed the meetings they were flying for, and some travellers bought tickets on other airlines.

**3.** Choose your flight turns the disruption alert into a decision the passenger makes. Each option shows when it arrives, how many stops it has, whether everyone on the booking stays together, and whether seats and bags move to the new ticket. Passengers can say what matters most to them, such as arriving before a set time or staying together, and the option that fits best is marked with one sentence explaining why. If a change cannot be completed on the spot, the passenger keeps the choice they made and an agent calls them back to finish it.

**4.** "Our passengers told us the delay was rarely the worst part. The worst part was being unable to fix it themselves," says Ana Ruiz, Head of Digital at AnyCompany Air. "The people who know which flight works for them are the passengers. Now they can choose it."

**5.** When a family's evening flight home is cancelled at the gate, the parent gets an alert that opens directly on Choose your flight. The screen shows the airline's suggested flight two days later next to three alternatives, including one that leaves tonight via another city with four seats left, marked "keeps all four of you together and gets you home tonight". The parent taps it, sees that the children's seats stay next to theirs, confirms, and the four new boarding passes appear before the family has left the gate. A consultant whose first leg lands three hours late sees two later connections, chooses the one that arrives at 12:40 for a 14:00 meeting, checks that her aisle seat and bag move with her, and confirms from the taxi queue. Her company's travel agency sees the change on its own booking record.

**6.** "The flight got cancelled and I had our new one booked before the kids had finished their snack. We were together, we got home the same night, and I never had to call anyone," says Amara, a parent who flies with her family a few times a year. *(Synthetic testimonial from a persona built on customer feedback.)*

**7.** Choose your flight is available to every AnyCompany Air passenger in the latest version of the app and under Manage booking on the website. Passengers who receive a disruption alert can tap it to see their options right away.

## Customer FAQ

**Q: How does it work?**
A: When your flight is cancelled, delayed by more than two hours, or you miss a connection, the alert opens on a screen with your new options. Choose one and confirm it for everyone on your booking. Known (the alert and the alternatives screen exist today: 251,453 alert opens, 150,845 alternatives views); the choose and confirm step is new.

**Q: Does it cost anything?**
A: No. Changing to another offered flight after a cancellation or long delay is free, as it is when an agent makes the change. Known (CALL-0045: an agent confirmed a change fee "shouldn't happen after a cancellation").

**Q: Will my family stay together, and will my seats and bags move?**
A: The choice applies to everyone on the booking, and each option shows before you confirm whether you will be seated together and whether your seats and bags move. Options that would split the group are marked. Needs evidence: extras are not carried over today in 835 rejected changes (EMD_NOT_REASSOCIATED).

**Q: What if none of the flights work for me?**
A: You can still keep the suggested flight, ask for a call-back, or contact us. A refund instead of a new flight stays with an agent for now. Known (refund requests: CALL-0011, CALL-0085, CALL-0105).

**Q: What if the change fails?**
A: Your choice is saved and an agent calls you back to complete it, so you do not start again on hold. Assumed: call-back capacity in peak months is not yet sized.

**Q: How does it decide which flight to mark?**
A: It compares the options with what you said matters (arrival time, staying together, fewest stops) and marks the closest match with one sentence on why. It never books for you. Assumed.

**Q: I booked through a travel agency or my company. Can I use it?**
A: Yes, and your agency sees the change. Needs evidence: agency bookings today show the automatic flight in the portal without a way to change it (AGY-0013).

## Internal FAQ

**Q: Why this, and why now?**
A: It is the top signal in every source and segment (116 of 400 records), it is the business metric itself (self-service rebooking 12%), and four corporate accounts tie renewal or a tender to it, one of them in February. Known. Summer 2027 is the next peak: July and August 2026 had almost twice the disrupted passengers of other months (90,752 and 88,308). Known.

**Q: What has to be true in the systems?**
A: The alternatives and keep-suggestion steps already exist and are reliable (0 errors on alternatives; 0.08% on keep-suggestion). Known. A passenger's own choice needs a ticket reissue, and that service rejects 5.0% of requests today, mostly fare rule mismatches. Known. Whether those rejections can be handled for offered alternatives is Needs evidence (engineering spike).

**Q: What are the biggest risks?**
A: Passengers may not trust a change they made themselves and call anyway. Assumed: this is the riskiest assumption. Reissue failures could leave passengers with no valid ticket. Needs evidence. A recommendation that misses what matters could cost trust. Assumed.

**Q: How do we measure success?**
A: The North Star: self-service rebooking rate from 12% to 30%, and rebooking calls from about 415 to 300 per 1,000 disrupted passengers, June to September 2027. In the pilot: alternatives viewers who confirm a choice or keep the pick, from 28% to 60%, and Contact us taps per alert opened, from 41% to 25%. Assumed targets, from the telemetry baselines (Known).

**Q: Does this replace summer agents?**
A: No. Agents handle the passengers who cannot or will not self-serve, and the call-backs. Calls per 1,000 disrupted passengers have stayed between 401 and 424 every month, so without a product change the queue grows with every disruption. Known.

**Q: What about the booking redesign and the 3D seat map?**
A: Both scored below the gate or threshold on today's evidence: conversion is 3.1% against a 3.0% benchmark, and 3D seat mentions are wishes, not pain. Known. They remain open hypotheses with cheap tests.

**Q: Timeline?**
A: Prototype and persona critique today; test with real disrupted passengers within 30 days; a pilot before June 2027. Assumed.

## Writing audit
Checked voice (customer as subject, active, third person in the press release), banned words, em dashes, firsts, scope of claims, and the North Star numbers. Changed: "easily" removed from paragraph 3; the one-account agency claim in the FAQ scoped to one escalation; the testimonial rewritten to avoid "I used to, now I".

## Readiness check
Verdict: AMBER, because two gaps remain: how passengers will trust a self-made change, and how reissue failures show up for offered alternatives.

## Prototype scope
**Q: Who is the primary user, and what are they accountable for?**
A: Amara, a parent travelling with her family, and Mei, a weekly corporate traveller. Each is accountable for getting themselves (and, for Amara, three others) to the destination in time for what the trip is for: home the same night, or a 14:00 meeting. Henrik, the travel manager, is the buyer, not the user of this screen.

**Q: What is the pain today?**
A: The alert arrives (11 minutes after the event at p95 in normal months, about 41 minutes in July and August). The passenger opens the trip, sees the alternatives for a median 84 seconds, and either keeps the airline's pick (17%) or taps Contact us (41%). Then comes a hold of 50 to 175 minutes and a 38-minute average call. The worst part is watching good flights fill up while waiting. All Known.

**Q: What is the prototype experience?**
A: Full journey: alert → disruption screen with the current pick and alternatives → optional "what matters" → choose → review what moves (seats, bags, everyone together) → confirm → new boarding passes → fallback with call-back on failure. **Slice the prototype shows:** the disruption screen with alternatives, the "what matters" marker, the choose-and-review step, the confirmation, and the failure fallback. It does not show the alert itself, the agency view, or refunds.

**Q: What is the vision?**
A: Automatic: the alternatives, the seat and bag check, the marker for the best match, the boarding passes, and informing the agency. With the passenger: which flight, and whether to confirm. Speed: confirmed in under two minutes from opening the alert. [GAP] How fast a confirmation must come back before passengers give up and call: needs the real-user test.

**Q: What views and signals are needed?**
A: One disruption screen: the current pick and two to four alternatives, each with departure, arrival, stops, seats left, together or split, and whether seats and bags move; a review screen; a confirmation; a fallback screen. At a glance: arrival time and "everyone together". The passenger is told to act by the alert and by a banner on the trip.

**Q: What data is needed?**
A: The disrupted booking and its passengers; the offered alternative flights with seats left; each passenger's seats and bags; what the passenger said matters; the result of the ticket change. Business objects: a booking has passengers and flights; each passenger has a ticket with extras; a disruption offers alternatives for a booking. Fresh to the minute: seats left change fast in a disruption. [GAP] Which alternatives the airline allows per fare: the 3,985 fare rule mismatches suggest the offered list and the allowed list differ. Engineering lead to confirm.

**Q: What does the prototype measure?**
A: Whether persona walk-throughs, and then real disrupted passengers, confirm a choice without tapping Contact us, and what makes them hesitate. This maps to the pilot metric (confirm or keep, 28% → 60%) and to the riskiest assumption.

| # | Gap | Question that would close it | Must-have or nice-to-have |
|---|-----|------------------------------|---------------------------|
| 1 | Trust in a self-made change | Do passengers confirm without calling to check? | Must-have (riskiest assumption) |
| 2 | Allowed vs offered alternatives | Can every offered alternative be confirmed without a fare rule rejection? | Must-have before pilot |
