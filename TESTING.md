# Testing

## Package tests (free, every change)

```bash
python3 -m unittest discover tests
```

They check the skills, the bundle that `scripts/build.py` produces, the samples and their generators, and the end-to-end checks themselves on a synthetic workspace. CI runs them on every push.

## End-to-end runs (model calls, on demand)

`tests/e2e/run_e2e.py` runs the bundled skill in Claude Code, headless, in a fresh copy of a sample's working folder, then checks the results with `tests/e2e/checks.py`.

```bash
python3 tests/e2e/run_e2e.py --sample air --legs workshop,mismatch,missing-prd
python3 tests/e2e/run_e2e.py --sample all --legs workshop,team --budget-usd 20
```

| Leg | What it tests |
|-----|---------------|
| `workshop` | A full Discovery run, unattended, ending with the Discovery brief |
| `mismatch` | Data about a different product: no analysis, and no invented data |
| `missing-prd` | Handoff without the PRD refuses to write a brief (reuses the workshop leg's results) |
| `team` | A second model plays the scenario's team turn by turn, so the checkpoints, overrides, iteration, and test-first decision are tested |

Measured cost per sample: the `workshop`, `mismatch`, and `missing-prd` legs together about $3.50 to $4.60 (AnyCompany Air and Health); the team leg about $110 (measured on a former sample, 36 turns, each resuming the whole session). Run the team leg before a release, not on every change.

Checks:

- **D (mechanics):** required artifacts, the brief's 15 sections, links, no emails or CRM identifiers, `.gitignore`, no scripts, prototypes built from the shell, versions logged, the critique in `prototype/`, the decision, no GTM part left as draft, team expectations written before the analysis, `next-steps.md` with its Now, Next, Later roadmap.
- **O (outcome):** graded against the `expectations` block in `facilitator/<sample>.md`: the top signal, the distractor failing the gate, and the use case taken forward. For samples with telemetry, also the Say and do table (O04), the telemetry trap not ranked first (O05), a telemetry-only signal (O06), and the feasibility evidence from telemetry (O07). Alternative phrasings are separated by `|`.
- **N (negative)** and **T (team)**, for those legs.

Each run writes `.e2e/<timestamp>/` with every workspace, transcript, and cost, plus `report.md`. Calls are billed to the AWS account the Claude Code CLI uses, and `--budget-usd` caps every call.

These runs test the method and the artifacts. They run in Claude Code, not AWS Quick, so check a release in AWS Quick by hand as well: import it, start Discovery on a sample, and build a prototype.

## Team Space mode

The automated tests run in Claude Code, which has no AWS Quick Spaces, so they cover the local folder only. Test team Space mode by hand in AWS Quick Desktop with two people, following "Optional: run it in a team Space" in `facilitator/dry-run-air.md`: the Space confirmed, `PROJECT.md` with the Storage and Driver lines, artifacts at the usual paths in the Space, the take-over, the stop when the other person tries to write, and no customer data in the Space.
