# Kickoff page: AnyCompany Air website and app

Filled in by the AnyCompany Air digital team before the Discovery workshop. AnyCompany Air, its customers, and every record in this folder are fictional.

## The product

- **Company:** AnyCompany Air, a mid-size European airline with about 300 flights a day on short and medium-haul routes.
- **Product:** the website and the app, where customers book, check in, and manage their trips. The team is proud of the app's ratings for booking and check-in.
- **Who uses it:** leisure travellers, about 60% of passengers, who book directly or through travel agencies and fly a few times a year; frequent flyers, about 25%, loyalty members who fly every month, mostly on the app; and travellers of corporate accounts, about 15% of passengers.
- **Who pays, if not the users:** for corporate travel, about 40 companies on annual contracts, a third of revenue, managed by the corporate account team. Their travellers book through their company's travel agency or directly.
- **Why now:** the digital team has budget for one significant improvement next half-year.

## The team

| Role | What they believe the main problem is |
|------|---------------------------------------|
| Head of digital (product owner) | The booking flow is the priority: "Our website looks dated next to the competition, and booking is where we make money." |
| Engineering lead, digital platform | Owns the app and website and their connection to the reservations system. Cautious about anything that changes bookings after they are made. |
| UX designer | Saw a 3D cabin view in a competitor's app, and thinks it would make seat upgrades easier to sell. |
| Customer service operations lead | Runs the call centre and sees the queues. The answer is more agents in the summer. |
| Head of corporate accounts | Hears from travel managers every week. The team should listen to corporate customers before leisure ones. |

Joins only the kickoff and the readout: the commercial director, who believes customers mainly complain about price.

## The business metric

- **Metric:** self-service rebooking rate for disrupted passengers. A disrupted passenger is one whose flight was cancelled or delayed by more than two hours; the rest rebook through the call centre, at an airport desk, or not at all.
- **Which direction is good:** Higher is better
- **Baseline:** 12%, over 1 May to 15 October 2026, from the operations data.

## Ideas we already have

1. **Self-service rebooking**
   - Who has it: passengers whose flight is cancelled or delayed, or who miss a connection.
   - The problem: they cannot choose a new flight themselves, and have to call or queue.
   - Evidence we think we have: call centre queues every summer.
   - Business metric it moves: self-service rebooking rate.
   - Owner: head of digital.
   - Our idea, if any: an assistant in the flow that recommends the best new flight for what the passenger says matters (arriving before a meeting, keeping the family together), and explains why in one sentence.
2. **Booking flow redesign**
   - Who has it: everyone who books on the website or app.
   - The problem: the flow looks dated, has too many upsell steps, and multi-city is missing.
   - Evidence we think we have: reviews, and leadership's view of the competition.
   - Business metric it moves: web booking conversion.
   - Owner: head of digital.
3. **Bag tracking**
   - Who has it: passengers whose bag is delayed or lost.
   - The problem: they cannot see where their bag is.
   - Evidence we think we have: lost-baggage calls.
   - Business metric it moves: baggage-related calls.
   - Owner: engineering lead.
4. **Loyalty points visibility**
   - Who has it: frequent flyers.
   - The problem: points and status progress are confusing or missing.
   - Evidence we think we have: loyalty calls.
   - Business metric it moves: loyalty-related calls.
   - Owner: head of digital.
5. **3D seat map**
   - Who has it: anyone choosing a seat.
   - The problem: the seat map does not show what the seat is like.
   - Evidence we think we have: the competitor demo, and some requests on social media.
   - Business metric it moves: seat upgrade revenue.
   - Owner: UX designer.

## The data

- **Input:** production
- **Where it is:** `discovery/data/`, with the telemetry in `discovery/data/telemetry/`
- **Period:** 1 May to 15 October 2026
- **Sample data:** Yes: fictional, so the run is a demonstration and its brief is not evidence for a build

| File | Source | Records |
|------|--------|---------|
| `app-and-web-reviews.csv` | App store, Google Play, and website reviews, with ratings | 80 |
| `call-center-contacts.csv` | Call centre contacts: contact reason, handle time, and a transcript snippet | 110 |
| `social-posts.csv` | Public social media posts mentioning the airline | 70 |
| `nps-verbatims.csv` | Post-flight survey comments, with score and flight outcome | 80 |
| `corporate-account-notes.csv` | Corporate account managers' notes from reviews and renewals | 30 |
| `travel-agency-escalations.csv` | Escalations from partner travel agencies | 30 |
| `operations-monthly.csv` | Flights, delays, cancellations, disrupted passengers, self-service rebookings, and rebooking calls, by month | 6 months |
| `nps-by-flight-outcome.csv` | NPS by month for on-time, delayed, and cancelled flights | 18 rows |
| `disruption-nps-by-rebooking-channel.csv` | NPS of disrupted passengers by how they rebooked | 4 rows |
| `web-booking-funnel-monthly.csv` | Website sessions, searches, bookings, and conversion | 6 months |

- **Telemetry, if any:** what the systems recorded for the same period, aggregated by day, from real user monitoring (RUM) in the app and on the website, and from traces and logs in the backend: `telemetry/journey-map.csv` (each step of the disruption rebooking and booking journeys, and the RUM view or backend route it maps to, 11 rows), `telemetry/rum-journeys-daily.csv` (sessions reaching each step, by day and channel, with the median time on the step, 2,688 rows), `telemetry/spans-daily.csv` (requests, errors, and p50 and p95 duration per service and span, by day, 1,344 rows), and `telemetry/errors-top.csv` (the most frequent error codes per service, 9 rows).
- **Personal data removed:** yes. Customers appear only as a segment or a code such as "Customer 0412", and staff by role. The telemetry holds no user IDs, IP addresses, or booking references.

## What we already know we cannot change

- Bookings live in the reservations system; the app and website connect to it.
