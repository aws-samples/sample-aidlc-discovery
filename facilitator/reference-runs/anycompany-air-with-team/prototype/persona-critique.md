# Persona critique: self-service rebooking for disrupted passengers ("Choose My Flight")
Prototype version critiqued: **v2** (`v2.html`, = `index.html`), 2026-10-29. Demonstration run on fictional sample data.

> **Synthetic personas, not customers.** Every reaction below is grounded in the persona's evidence or labeled Assumed. These findings are hypotheses: the real test is the 8 walk-throughs with recently disrupted passengers (head of digital and UX designer, by the 30-day follow-up).

---

## Ingrid Halvorsen: corporate traveller, cancelled at the gate (Mobile)

**[Persona: Ingrid]** Walked 1 → "Keep the 07:20" → 3 → 4, at the gate, phone in one hand, with a meeting at 9:00.

- **Walk-through:**
  - Screen 1: "Keep the 07:20" is exactly what I want. Three taps to a boarding pass; well under three minutes. No hesitation.
  - Screen 1 says "Tomorrow 07:20", screen 2 says "Fri 07:20". Small, but at a gate I double-check dates. Make them match.
  - Screen 4: "Issued", "€0.00", boarding pass, gate. Good. But there is no ticket number. My company's expense and travel tools want one. [Assumed]
  - **Then I stand at the gate at 20:00 with a flight at 07:20 tomorrow, and I still have nowhere to sleep.** Nothing on screen 4 tells me about a hotel. Today the hotel comes through an agent, so I would call for that. [Known that vouchers only come through an agent, from Daniel's evidence; that Ingrid calls for it: Assumed]
- **Pain solved:** "I can see alternative flights on the website but can't move myself onto one." Solved. "Call immediately before the good flights fill up." Solved: I don't have to race the queue. | **Pain not solved:** the night before a next-day flight. My travel manager not knowing I moved.
- **Workflow fit:** I book through my company's travel management company. If I change the flight here, does their booking update? If not, my travel desk sees the old flight and calls me, or I call them. [Assumed; Karim's evidence: "No disruption feed to the travel management company"]
- **Switching:** I would drop "call immediately" the first time this works. What would stop me: a hotel I still have to phone for, or my travel desk calling me to ask where I am.
- **Riskiest assumption:** **Holds for choosing; unclear for not calling.** I trust the flight I chose. I would not call to check it. I would call for the hotel, and my travel desk might call me.
- **Day-one adoption: 8 of 10**, because it does the one thing I have asked for. It loses two points because the night before still needs a phone call.

---

## Daniel Okafor: leisure traveller, family of four, cancelled at 23:00 (no own path in v2; walked Mobile as if it were his booking, and the Desktop path)

**[Persona: Daniel]** It's 23:00 in Paris, the kids are tired, and the phone line is closed.

- **Walk-through:**
  - Screen 1 at 23:00: "You can rebook here… at any hour." That is the line I needed. Good.
  - Screen 2 on Mobile shows "1 of 1 traveller". For me it would have to say "4 of 4 together". The Desktop path shows "2 of 2 together" and "Seated apart", so I believe it works; I don't need my own screens to understand it.
  - Screen 4 shows one boarding pass. With four of us, will I get four? Can I see the kids' seats next to ours? [Assumed]
  - **After 23:00 our new flight is tomorrow afternoon. Where do we sleep tonight?** "Hotel and meal vouchers only come through an agent." The line opens at 07:00. Even with the flight sorted, I'm on hold at 07:00 for the hotel, or I pay for it myself. [Known]
  - Screen 7b: "when the line opens at 07:00" is honest. It is also exactly my problem.
- **Pain solved:** "Cancellation text at 23:00, phone line opens at 07:00, and by then the good flights are full." Solved for the flight. "Our family got split across two flights… and we couldn't fix it online." Solved if "together" really means together. | **Pain not solved:** the hotel tonight.
- **Workflow fit:** Fits: smartphone, evening, no set-up. Doesn't fit: a disruption for my family is a flight and a bed, and this is only the flight.
- **Switching:** I'd use it straight away; I have no workaround that works at 23:00. What would stop me: the airline's suggestion splitting us again and me not noticing.
- **Riskiest assumption:** **Holds for choosing, does not hold for not calling** when the new flight is the next day. I'd trust the flight. I'd still call, for the hotel.
- **Day-one adoption: 7 of 10**, because the flight part answers my worst night. The hotel still sends me to the phone.
- **Does Daniel need his own path in v3?** No, for the riskiest assumption. The "together" pattern is already testable on Desktop. The hotel gap, not the family screens, is what his walk-through found.

---

## Helena Kowalska, through her daughter: passenger who does not use the app (Desktop + text)

**[Persona: Helena]** (and her daughter, at home in Kraków, after Helena calls her from Nice airport)

- **Walk-through (daughter):**
  - Screen 5: "Booking reference R2XN8D". Do I have it? If I booked their trip, it's in my email. If the travel agency booked it, I don't, and I'd have to call my mother back to find it on a printout, or call the agency. There is no hint on the screen where to find it. [Known that "her daughter or a travel agency books for them"; the rest Assumed]
  - Screen 2 (Desktop): clear. "2 of 2 together" and "Seated apart" are exactly what I look for with my parents. The suggestion two days away is clearly marked; choosing tomorrow is easy.
  - Screen 3: "Helena is told by Text to +48 ••• ••• 218". Is that my mother's number, or mine, or the agency's? If the agency booked it, the number on the booking might be theirs. [Assumed]
  - Screen 4: good. "Nobody needs to call us." I believe it.
- **Walk-through (Helena):**
  - Screen 6 (the text): short enough, and "Your daughter changed this booking for you" tells me it's real. "Show this text at the desk" is what I'd do anyway.
  - I would still go to the desk to be sure. [Assumed] That is not a phone call, so it doesn't count against the queue, but it is a desk visit.
- **Pain solved:** "My parents are stuck in Nice… can't get through on the phone." Solved: neither of us needs the phone. | **Pain not solved:** a hotel if the flight is the next day (same as Daniel). Finding the booking reference.
- **Workflow fit:** Fits how the family works: the daughter acts, Helena receives a text. Doesn't fit when the agency holds the booking.
- **Switching:** The daughter would use it the first time. What would stop her: no reference to hand.
- **Riskiest assumption:** **Holds** for the daughter; for Helena, she trusts the text but goes to the desk anyway. That is fine for calls; it is not "self-service" in the sense of the metric. [Assumed]
- **Day-one adoption: daughter 8 of 10; Helena on her own 2 of 10.** This persona's confidence is Low (3 second-hand items).

---

## Karim Haddad: corporate travel manager (watched Ingrid's path; no screens of his own, by design)

**[Persona: Karim]** I don't use this flow. I answer for what happens when my travellers do.

- **Walk-through:**
  - Ingrid's path: quick, and she is "in policy" because there's nothing to pay. Good.
  - Screen 4: she's on the 07:20. **My travel desk and our travel management company still show her on the 19:40.** My duty-of-care team asks "where are our travellers?" and I still can't answer. [Known: "their duty-of-care team wants to know where travellers are during disruptions… We can't give them either today."]
  - Bulk rebooking and a desk view are not here. I understand they are P1. [Known scope]
- **Pain solved:** "Today their agents call our corporate line one traveller at a time." Partly: travellers who rebook themselves need no call from my desk. | **Pain not solved:** visibility; bulk rebooking; my renewal report ("time to rebook").
- **Workflow fit:** It moves the work to my travellers, which I asked for ("self-service rebooking for travellers" in the renewal meeting). It doesn't connect to my desk or the travel management company.
- **Switching:** I'd tell my travellers to use it. What would stop me: my desk seeing stale itineraries and calling travellers to reconcile.
- **Riskiest assumption:** **Holds for the traveller; unclear for my desk.** My desk calls the traveller or the travel management company, not necessarily the airline's line, so it may not show up in the airline's call numbers. [Assumed]
- **Day-one adoption: 6 of 10** as something I'd tell my travellers to use; 3 of 10 for my own desk.

---

## Sofia Lindqvist: the happy regular (satisfied customer)

**[Persona: Sofia]** Never been cancelled. I looked at this as "what if it happens to me".

- **Walk-through:** Screen 1 is what I'd expect from the app that books me in four minutes: "If she ever is disrupted, she expects the same app to sort it out as quickly as it booked her." Three taps to a boarding pass feels like the rest of the app. No hesitation.
- **Pain solved:** none today; I have none. | **Pain not solved:** n/a.
- **What does this change that already works for me, and what would I lose?** On v2, nothing I can see: the prototype doesn't show my normal trip screen, booking, or check-in, so I can't tell whether "Rebook for someone else" or disruption banners get added to them. Please don't put "Rebook for someone else" on my home screen, and don't send me disruption-style messages on trips that run on time. [Assumed, from "What the team could break for Sofia"]
- **Riskiest assumption:** **Holds.** I'd trust it, because I already trust the app.
- **Day-one adoption: 9 of 10**, if I'm ever disrupted.

---

## What the critique shows

| # | Finding | Personas | Points to risk | Fix in v3? (proposed, team decides) |
|---|---------|----------|----------------|-------------------------------------|
| 1 | **Next-day flight, no hotel: passengers rebook themselves, then call for the hotel.** Undermines "trust it enough not to call" for a different reason than distrust | Ingrid, Daniel, Helena | **Valuable** (riskiest assumption) | **Team decision.** A line on screen 4 ("Flying tomorrow? Get a hotel for tonight") tests the moment, but hotel help without an agent is P1-2 and is not confirmed: it depends on vouchers being issued without an agent. If kept, log as Needs evidence; customer service operations lead confirms |
| 2 | **Company and travel management company not told about the change**: travel desk sees the old flight and calls to reconcile | Karim, Ingrid | **Valuable**; calls may move to the travel desk rather than disappear | **Proposed: no change to screens**, because informing the travel management company is P2-1 and unconfirmed. Carry to Validate as an open question; head of corporate accounts confirms with design partners |
| 3 | No hint where to find the booking reference when someone else booked | Helena's daughter | **Usable** | **Proposed: yes**: "Find it in the confirmation email or on the travel agency's document" under the field. Display only |
| 4 | Unclear whose phone gets the text when an agency booked | Helena's daughter | **Usable**; feasibility | **Proposed: no**: depends on contact data on agency bookings. Carry to Validate with the booking-reference security review |
| 5 | Dates inconsistent ("Tomorrow 07:20" on screen 1, "Fri 07:20" on screen 2) | Ingrid | Usable | **Proposed: yes**: same date format on both |
| 6 | No ticket number on the confirmation | Ingrid | Usable (trust) | **Proposed: yes**: show a fictional e-ticket number on screen 4 |
| 7 | One boarding pass shown; families need to see every passenger and seat | Daniel | Usable | **Proposed: no for v3**: Desktop shows two travellers together already; revisit if the real walk-throughs include families |
| 8 | Seat-gone screen says "no seats left together" to a passenger travelling alone | (review of v2) | Usable | **Proposed: yes**: copy says "no seats left" for one traveller |
| 9 | Call-back time depends on the hour: "within the hour" while the line is open (07:00 to 22:00), "when the line opens at 07:00" after 22:00 | Daniel; team request | Usable | **Yes, queued** (customer service operations lead). Note: "within the hour" is a call centre commitment; in summer, holds reach up to three hours, so whether a call-back within the hour holds at peak is [Needs evidence], owned by the customer service operations lead |
| 10 | Nothing added to the normal trip, booking, or check-in screens | Sofia | Guardrail (NF-7) | **No change needed**; keep it that way in the build |

**Does Daniel need his own path?** No, for the riskiest assumption: the "together" pattern is testable on Desktop, and what his walk-through found (the hotel) applies to every next-day rebooking.

**Day-one adoption:** Ingrid 8, Daniel 7, Helena's daughter 8 (Helena alone 2), Karim 6 (his desk 3), Sofia 9.

**On the riskiest assumption:** every disrupted persona chose a flight without help and would trust it. The threat the critique found is not distrust: it is a **second reason to call** (hotel; travel desk reconciliation) that the confirmation does not answer.

Synthetic personas, not customers: test these findings with real users in the follow-up.

## Fixed in the iteration (v3, decided by the team 2026-10-29)
| # | Finding | Decision | Done in v3 |
|---|---------|----------|------------|
| 1 | Next-day flight, no hotel | **Fixed, Needs evidence** (head of digital) | "Tonight: Hotel voucher issued" on "You're rebooked" (Mobile and Desktop) and in Helena's text. Whether vouchers can be issued without an agent: customer service operations lead confirms. Riskiest assumption widened to "no need to call for anything else" |
| 2 | Travel desk not told | **Validate** | No screen change; in `riskiest-assumption.md` and `notes.md` for the risk review |
| 3 | Where to find the booking reference | **Fixed** | Hint under the field: confirmation email or the travel agency's document |
| 4 | Whose phone gets the text on agency bookings | **Validate** | No screen change; goes with the security review |
| 5 | Inconsistent dates | **Fixed** | Every Ingrid screen says "Fri 30 Oct · 07:20"; the cancelled flight says "Thu 29 Oct" |
| 6 | No ticket number | **Fixed** | Fictional e-ticket numbers on "You're rebooked" |
| 7 | One boarding pass for families | **Waits** | Revisit if the real walk-throughs include families |
| 8 | "No seats left together" for one traveller | **Fixed** | "That flight has no seats left now." |
| 9 | Call-back time by the hour | **Fixed** | "We'll call you back within the hour" while the line is open, with the after-22:00 wording shown below it |
| 10 | Normal trip untouched | No change | Guardrail kept |
