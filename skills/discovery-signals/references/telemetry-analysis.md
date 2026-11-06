# Telemetry analysis

Use this when the data includes telemetry: what the systems recorded, from real user monitoring (RUM), traces, metrics, and logs, usually exported from CloudWatch, Datadog, or OpenTelemetry. Telemetry shows what customers and systems **do**; the feedback shows what customers **say**. Telemetry is always read next to the feedback, never instead of it: on its own it has no customer voice, and it pushes a team toward the loudest error.

## What to expect

Aggregated tables, not raw logs or traces, usually in a `telemetry/` folder next to the feedback:

- **A journey map**: each journey step, its order, its source (`rum`, `trace`, or both), and the RUM view or backend route it maps to. Read it first: it turns technical names into the customer's journey.
- **Journey steps by day** (RUM, or sessions rebuilt from traces): sessions reaching each step, by channel, with time on the step.
- **Spans or metrics by day**: per service and span or route, requests, errors, and latency (p50, p95).
- **Top errors**: error codes per service, with a message and a count.

If the team brings raw logs or traces, do not analyze them in the chat: they are too large and carry personal data. Ask for daily aggregates per journey step instead, with user IDs, IP addresses, and request bodies removed at the source.

## Steps

1. **Map the journeys.** From the journey map, list each journey and its steps in order. Mark the steps that exist only in RUM: without RUM, the team cannot see them.
2. **Measure each step** with Python over the whole period and by month: sessions (reach), drop-off to the next step, where the sessions that leave go (for example a Contact us step), and time on the step.
3. **Measure each service**: requests, error rate, and p95 latency, by month and on the worst days. Note which journey step each route serves.
4. **Read the top errors** for what they mean in the customer's terms (for example, "extras not moved to the new ticket").
5. **Line telemetry up with the feedback themes** by journey and by date: does the theme's peak match a peak in drop-off, errors, or latency?
6. **Write the Say and do table** (below), and use the telemetry in the top signals: reach and baselines from the journey, severity from drop-off and errors.

## Say and do

For every theme from the feedback, and every telemetry finding with no feedback behind it:

| Theme | What customers say | What the systems show | Reading |
|-------|-------------------|-----------------------|---------|
| [theme] | [count, a quote] | [drop-off, errors, latency, with numbers] | Both (Known), Feedback only, or Telemetry only |

- **Both:** the strongest evidence. Label it Known.
- **Feedback only:** the systems do not see it. It may be outside the product (a policy, a phone queue), or the telemetry does not cover that step.
- **Telemetry only:** a silent problem. Nobody complains, but it costs customers. Label the measurement Known and its effect on customers Assumed, unless the feedback explains it.

## Traps

- **The error dashboard is not the priority list.** A journey can fail as designed, with no errors: a page that only offers "Contact us" returns success. Rank problems by what they cost customers, not by error counts.
- **Drop-off is not intent.** It shows people did not complete a step; only the feedback says what they wanted.
- **Backend-only journeys are weaker.** Steps rebuilt from traces without RUM miss what happened on the screen. Say so, and label those steps' drop-off Assumed.
- **Size the loud errors.** For every error peak, check whether the journey's completion moved. If it did not, it is real and small.

## Feeding later steps

- **Scoring:** reach and the outcome baseline from the journey; error rates on the services a candidate depends on as feasibility evidence, for the engineering lead to confirm.
- **Prototype:** name the journey step the test moment is meant to change.
- **Validate:** write success criteria as the same journey measures, so the follow-ups read the same telemetry.
