# Sample conventions

Every sample is a realistic, fictional business case that a team can run a full Discovery workshop on. The samples share one structure, so a facilitator who knows one knows them all.

## Layout

```text
samples/<slug>/
├── README.md               the scenario page participants read
└── discovery/
    ├── data/               exports, for production-data samples
    └── signal-briefs/      briefs and aggregates, for the Signal Brief sample
scripts/samples/<slug>.py   the generator that writes discovery/
facilitator/<slug>.md       spoilers: the designed truths and what good looks like
```

The sample folder is the working folder a team gives Amazon Quick access to, so it holds no scripts and no answers: the assistant can read everything in it. Generators live under `scripts/samples/`, and facilitator notes under `facilitator/`.

## The scenario page (`README.md`)

1. **The company and its product**, in two or three sentences.
2. **Customers and segments**, with rough sizes.
3. **Who is in the room**: four to six roles, each with what they believe before the workshop. At least one belief must be the loud request the data does not support.
4. **The business metric** the team wants to move, with its current baseline and the period it covers.
5. **Candidate use cases** the team brings, 3 to 5, each written as a problem with five fields: who has it, the problem, the evidence the team thinks it has, the business metric it moves, and the owner.
6. **The data**: one line per file with its source, record count, and period.
7. **How to run it**: the folder to grant, the data input, and the prompt to start the workshop.

Never reveal the designed truths on this page.

## The data

- **Fictional and anonymized.** Company names use AnyCompany. No real people, emails, phone numbers, or account numbers. Staff appear by role ("account manager"), and customers by a code ("Customer 0412") or a segment.
- **Realistic exports.** CSV for tabular exports, with the columns a real tool would export. Each record has an `id`, an ISO `date`, the `channel`, the customer `segment`, and the `text`, plus fields the channel would really have (rating, contact reason, account tier, order value).
- **Period.** 1 May to 15 October 2026.
- **Volume.** About 400 qualitative records for production-data samples, plus at least one quantitative file (operations or usage aggregates) consistent with the qualitative data. The Signal Brief sample has 10 briefs plus aggregate statistics.
- **Varied text.** Write a bank of hand-written phrasings per theme and channel, and vary them. No two records have identical text. Records sound like their channel: short and angry on social, structured in a ticket, factual in an account manager's note.
- **A designed truth,** documented in the facilitator notes:
  - the real top problem, spread thinly across channels so no single channel shows it whole;
  - the loud request leadership or sales believes in, frequent in some channels but weaker in evidence;
  - a real secondary pain;
  - a distractor that looks popular but fails the gate's painkiller test;
  - counter-evidence (customers for whom the top problem does not apply, or who are happy);
  - about 10% noise: off-topic, duplicates in spirit, one-word reviews.
- **Quantitative data that agrees.** The aggregates are what let confidence reach High for the real problem, so they must line up with the qualitative counts.
- **Telemetry (optional, AnyCompany Air has it).** In `discovery/data/telemetry/`, at most four files, aggregated by day: a journey map (step, order, source `rum` or `trace`, RUM view, backend route), journey steps from real user monitoring, spans per service (requests, errors, p50 and p95), and the top error codes. OpenTelemetry field names where one exists. No user IDs, IP addresses, or booking references. Generate it with its own seed, so adding it never changes the other files. It needs its own designed truths: the real problem visible in the journey (ideally with no errors), a loud error that is real but small, and one telemetry-only signal.

## The generator

- Python 3 standard library only, with `random.Random(<fixed seed>)`, so it writes byte-identical files on every run.
- Theme weights are constants at the top of the file, and they match the facilitator notes.
- Running it prints the record count per file and per theme; the facilitator notes quote those counts.

## The facilitator notes (`facilitator/<slug>.md`)

Start with a spoiler warning. Then:

1. **The story** in three sentences.
2. **The designed truths**, each with its counts per channel.
3. **What Signals should find**, and how the team's likely hypotheses compare.
4. **Expected scoring**: for each candidate, the gate result, draft scores on the six dimensions, the confidence, and the expected decision.
5. **The likely riskiest assumption** for the top use case.
6. **A good decision** and why.
7. **Traps**: where teams and the assistant typically go wrong with this data.
8. **Expectations for automated tests**, as a YAML block:

```yaml
expectations:
  top_signal: "..."            # words the top signal should contain; separate alternatives with |
  loud_request: "..."
  distractor_fails_gate: "..." # the candidate that should fail the gate
  build_first_or_learn: "..."  # the candidate that should be taken forward
  data_input: production | signal-briefs
```
