# AnyCompany Air

A fictional sample for AI-DLC Discovery. AnyCompany Air, its customers, and every record here are made up.

## The company and its product

AnyCompany Air is a mid-size European airline with about 300 flights a day on short and medium-haul routes. Customers book, check in, and manage their trips on the website and in the app. The digital team is proud of the app's ratings for booking and check-in, and has budget for one significant improvement next half-year.

## Customers and segments

- **Leisure travellers**, about 60% of passengers. Book directly or through travel agencies, and fly a few times a year.
- **Frequent flyers**, about 25%. Members of the loyalty programme who fly every month, mostly on the app.
- **Corporate accounts**, about 15% of passengers and a third of revenue. Around 40 companies on annual contracts, managed by the corporate account team, with travellers who book through their company's travel agency or directly.

## The team

- **Head of digital (product owner).** Believes the booking flow is the priority. "Our website looks dated next to the competition, and booking is where we make money."
- **Engineering lead, digital platform.** Owns the app and website and their connection to the reservations system. Cautious about anything that changes bookings after they are made.
- **UX designer.** Saw a 3D cabin view in a competitor's app and thinks it would make seat upgrades easier to sell.
- **Customer service operations lead.** Runs the call centre. Sees the queues and believes the answer is more agents in the summer.
- **Head of corporate accounts.** Hears from travel managers every week and wants the team to listen to corporate customers before leisure ones.
- **Commercial director** (joins the kickoff and the readout). Believes customers mainly complain about price.

## The business metric

**Self-service rebooking rate for disrupted passengers: 12%** from May to mid-October 2026. A disrupted passenger is one whose flight was cancelled or delayed by more than two hours. The rest rebook through the call centre, at an airport desk, or not at all.

## Candidate use cases the team brings

1. **Self-service rebooking**
   - Who has it: passengers whose flight is cancelled, delayed, or who miss a connection.
   - The problem: they cannot choose a new flight themselves and have to call or queue.
   - Evidence the team thinks it has: call centre queues every summer.
   - Business metric: self-service rebooking rate.
   - Owner: head of digital.
   - The head of digital's idea: an assistant in the flow that recommends the best new flight for what the passenger says matters (arriving before a meeting, keeping the family together), and explains why in one sentence.
2. **Booking flow redesign**
   - Who has it: everyone who books on the website or app.
   - The problem: the flow looks dated, has too many upsell steps, and multi-city is missing.
   - Evidence the team thinks it has: reviews and leadership's view of the competition.
   - Business metric: web booking conversion.
   - Owner: head of digital.
3. **Bag tracking**
   - Who has it: passengers whose bag is delayed or lost.
   - The problem: they cannot see where their bag is.
   - Evidence the team thinks it has: lost-baggage calls.
   - Business metric: baggage-related calls.
   - Owner: engineering lead.
4. **Loyalty points visibility**
   - Who has it: frequent flyers.
   - The problem: points and status progress are confusing or missing.
   - Evidence the team thinks it has: loyalty calls.
   - Business metric: loyalty-related calls.
   - Owner: head of digital.
5. **3D seat map**
   - Who has it: anyone choosing a seat.
   - The problem: the seat map does not show what the seat is like.
   - Evidence the team thinks it has: the competitor demo, and some requests on social media.
   - Business metric: seat upgrade revenue.
   - Owner: UX designer.

## The data

All files are in `discovery/data/` and cover 1 May to 15 October 2026.

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

The engineering team also exported its telemetry for the same period, aggregated by day, in `discovery/data/telemetry/`: what the systems recorded, from real user monitoring (RUM) in the app and on the website, and from traces and logs in the backend.

| File | Source | Rows |
|------|--------|------|
| `telemetry/journey-map.csv` | Each step of the disruption rebooking and booking journeys, and the RUM view or backend route it maps to | 11 |
| `telemetry/rum-journeys-daily.csv` | Sessions reaching each journey step, by day and channel, with the median time on the step | 2,688 |
| `telemetry/spans-daily.csv` | Requests, errors, and p50 and p95 duration per service and span, by day | 1,344 |
| `telemetry/errors-top.csv` | The most frequent error codes per service, with a message and a count | 9 |

Customers appear only as a segment or a code such as "Customer 0412". Staff appear by role. The telemetry holds no user IDs, IP addresses, or booking references.

## How to run it

1. Give Amazon Quick access to this folder (`samples/anycompany-air`).
   Optional, recommended: create a Space in Amazon Quick and name it yourself (**Spaces**, then **Create space**), attach it and this folder to a chat (the **+** menu), and ask Quick to copy `README.md` and the `discovery/` data folder into the Space, keeping the same paths. Then work from a new chat with only the Space attached: the scenario, the data, and the Discovery artifacts all live in the Space, and you can share it with your team. The data is fictional, so it can go in a Space.
2. Start Discovery:

   ```text
   Start AI-DLC Discovery. Project: anycompany-air. Data: production, in discovery/data/ in my anycompany-air folder.
   ```

   With everything in a Space, name it for Discovery and the data:

   ```text
   Start AI-DLC Discovery. Project: anycompany-air. Save Discovery in the [your Space] space. Data: production, in discovery/data/ in the [your Space] space.
   ```

3. Play the team: answer the setup questions with the roles and beliefs above, and write your hypotheses before you see any analysis.

The designed answers are in [facilitator/anycompany-air.md](../../facilitator/anycompany-air.md). Read it after the run, not before.
