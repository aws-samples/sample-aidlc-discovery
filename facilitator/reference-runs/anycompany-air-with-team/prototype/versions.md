# Prototype versions: self-service rebooking for disrupted passengers ("Choose My Flight")
Current: v3 | Chosen for the handoff: **v3** (team, 2026-10-29). Known gap carried to the build: v3 shows a hotel voucher at the home airport; the rule is vouchers only away from home.

| Version | Date | What changed | Why | Asked by |
|---------|------|--------------|-----|----------|
| v1 | 2026-10-29 | First build from the confirmed screen plan: 8 screens (disruption message, options, check and confirm, rebooked [test moment], rebook for someone else, Helena's text, seat gone while choosing, none of these works). Mobile carries Ingrid's booking; Desktop carries Helena's booking for her daughter's path. | - | - |
| v2 | 2026-10-29 | Screen 7b (None of these works): call-back line changed from "As soon as an agent is free, at any hour" to "We'll call you back when the line opens at 07:00". Nothing else changed. | Team click-through: the line closes at night, so "at any hour" is not true today | Customer service operations lead |
| v3 | 2026-10-29 | (1) "Tonight: Hotel voucher issued" on "You're rebooked" (Mobile, Desktop) and in Helena's text; confirmation now says "You don't need to call us for anything". (3) Booking-reference hint. (5) Dates match across screens (Fri 30 Oct · 07:20; cancelled Thu 29 Oct). (6) E-ticket numbers on the confirmation. (8) "No seats left now". (9) Call-back "within the hour" while the line is open 07:00 to 22:00, after-22:00 wording beneath. Test-moment note updated to the widened assumption. | Persona critique findings 1, 3, 5, 6, 8; team request 9 | Head of digital (1); team (3, 5, 6, 8); customer service operations lead (9) |

## Deviations from the confirmed screen plan (accepted by the head of digital, 2026-10-29)
- **"Keep the 07:20" on the disruption message.** Ingrid's suggested flight is the one she wants, so screen 1 offers to keep it directly. This puts the test moment two taps from the start (quality bar) without removing the options screen.
- **Daniel has no screens of his own in v1.** His two needs are covered on the Desktop path: the airline's suggestion is two days later and is replaced, and the party stays together (Helena and Tomasz). His 23:00 family-of-four booking becomes its own path in a later version only if the persona critique shows it is needed (head of digital).
- **Unhappy paths are two screens (7a, 7b)**, making 8 screens in total instead of 7.

## Shown on screens but not confirmed (Needs evidence, for Validate)
- **Hotel voucher issued without an agent** (v3): today vouchers only come through an agent. [Needs evidence]; customer service operations lead confirms.
- **"Within the hour" call-back** (v3): holds at the summer peak? [Needs evidence]; customer service operations lead.
- "Bag moves with you" / "Bag moved to AY 1181" on confirm and rebooked: whether bags follow a self-service rebooking is not in the PRD. [Needs evidence]; goes to the reissue spike (engineering lead, 2026-10-29).
- "This booking is final": depends on reissue working without an agent. [Needs evidence]; goes to the reissue spike (engineering lead, 2026-10-29).
- ~~Call-back "at any hour"~~: fixed in v2. The line closes at night; the screen now says the call-back comes when the line opens at 07:00 (customer service operations lead).

## Queued (done in v3)
- Call-back time by hour on screen 7b: "We'll call you back within the hour" while the line is open (07:00 to 22:00), "We'll call you back when the line opens at 07:00" after 22:00. Asked by the customer service operations lead, 2026-10-29. Whether "within the hour" holds at the summer peak: [Needs evidence], customer service operations lead.
