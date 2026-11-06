# Prototype notes: self-service rebooking for disrupted passengers ("Choose My Flight")

> **Screen plan confirmed by the team, 2026-10-29. Current version: v3** (`v3.html`, copied to `index.html`; `compare.html` shows v1, v2, and v3 side by side). Demonstration run on fictional sample data. Deviations from the plan are listed in `versions.md`.

## Visual direction (proposed)
Deep navy and white cards, one teal accent for actions, amber only for the disruption itself; large type and tap targets for a phone held one-handed at a gate (NF-5). No team design system supplied.

## Screens (7)

### 1. Disruption message (entry point)
Ingrid's app at the gate: "Your 19:40 to Milan is cancelled." One primary action, "Choose your new flight"; a secondary "Talk to us". Same message arrives by text or email for passengers without the app. **P0-1, NF-1**

### 2. Your options
The airline's suggested flight at the top, labelled "Our suggestion", then the other flights with seats. Each card shows departure and arrival, connections, "All 1 traveller together" (or "All 4 together" for Daniel), and "Nothing to pay". Daniel's state: the suggestion is two days later; the next-afternoon flight with four seats together sits below it. Link at the bottom: "None of these works for me". **P0-2, P0-3, P0-7**

### 3. Check and confirm
What changes, old flight next to new: times, seat, everyone on the booking, €0.00. One button, "Confirm this flight". **P0-3, P0-4**

### 4. You're rebooked (TEST MOMENT)
Ticket issued, e-ticket number, €0.00 charged, bag moved, confirmation texted, and, for a next-day flight, "Tonight: Hotel voucher issued". "You don't need to call us for anything." New boarding pass. This is where the passenger decides whether anything is left to call about. **P0-5; P1-2 shown for the test (Needs evidence); riskiest assumption**

### 5. Rebook for someone else (desktop layout)
Website, "Manage booking": booking reference and surname. Helena's daughter enters her parents' booking from her laptop and lands on screen 2 for their booking. **P0-6**

### 6. The text Helena receives
SMS on a basic phone: new flight, time, gate, "Your daughter changed this booking for you. Nothing to pay. Show this text at the desk if you need help." **P0-6**

### 7. Unhappy paths
- **(a) Seat gone while you chose:** "The 07:20 filled up while you were choosing. The 08:05 still has a seat." Back to options. **NF-3** (the failure state)
- **(b) None of these works:** call-back with the booking already loaded ("you won't need to explain again"), coming when the line opens at 07:00, and the refund route. **P1-1, nice-to-have**

## Core flow (three paths)
1. **Ingrid (mobile):** 1 → "Keep the 07:20" → 3 → 4 (two taps to the test moment), or 1 → 2 → 3 → 4. Target: under 3 minutes from opening the message.
2. **Daniel (mobile, 23:00):** not its own path in v1; his needs (replace a two-days-later suggestion, party together) appear on the Desktop path with Helena's booking. Candidate for v2.
3. **Helena's daughter (Desktop view) and Helena:** 5 → 2 (Helena's booking: suggestion Sat 31 Oct replaced by Fri 30 Oct 11:15, two together) → 3 → 4 → 6. In the Mobile view, screen 5 leads to Ingrid's options, because the shell shows one booking per view.
Unhappy: 2 → 7a → 2; 2 → 7b.

## Test moment
Screen 4, "You're rebooked". Riskiest assumption (widened after the critique): passengers choose a flight and need to call for nothing else. The team expects to see whether the confirmation leaves anything to call about: is the ticket issued (e-ticket number), was I charged, did everyone move, where do I sleep tonight. Secondary signal on screen 2: how long people hesitate before choosing.

## Known quirks
- v3 issues a hotel voucher to Ingrid at her home airport (Hamburg). The rule for the build is vouchers only when the passenger is away from their home airport (engineering lead, 2026-10-29).
- In the Mobile view, "Rebook for someone else" leads to Ingrid's options (the shell shows one booking per view); use Desktop for the daughter's path.
- On Desktop, choosing the "Seated apart" flight opens the seat-gone screen with Ingrid's flight, not Helena's. Use the 11:15 for the walk-through.

## Questions for Validate
| Question | Type | Owner |
|----------|------|-------|
| Can hotel vouchers be issued without an agent? | Feasibility | Customer service operations lead |
| Does a "within the hour" call-back hold at the summer peak? | Feasibility | Customer service operations lead |
| Do bags follow a self-service rebooking; is the booking final without an agent? | Feasibility | Engineering lead (reissue spike) |
| Does the travel desk / travel management company see the change, or call to reconcile? (finding 2) | Valuable / feasibility | Head of corporate accounts |
| Whose phone gets the text on agency bookings? (finding 4) | Feasibility / security | Engineering lead, security review |
| Is booking reference plus surname safe enough to rebook for someone else? | Security | Engineering lead, security review |

## Out of the prototype
Travel desk view (P1-3), hotel help (P1-2), groups with mixed fares (P1-4), everything P2. Real seat data and reissue: fictional data only; reissue is the engineering spike.
