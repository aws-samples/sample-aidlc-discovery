# Testing

## Package tests (free, every change)

```bash
python3 -m unittest discover tests
```

They check the skills, the bundle that `scripts/build.py` produces, the samples and their generators, and the end-to-end checks themselves on a synthetic workspace. CI runs them on every push.

## Data preparation tests (Presidio, when the tool changes)

The tests for `tools/prepare-data/` that need Microsoft Presidio and its 400 MB spaCy model are skipped above. The `prepare-data` workflow runs them only when the tool or its tests change, or when started by hand. To run them locally:

```bash
pip install -r tools/prepare-data/requirements.txt && python -m spacy download en_core_web_lg
python3 -m unittest tests.test_prepare_data -v
```

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
| `team` | A second model plays the team on the sample's kickoff page turn by turn, so the checkpoints, overrides, iteration, and test-first decision are tested |

Measured cost per sample: the `workshop`, `mismatch`, and `missing-prd` legs together about $3.50 to $4.60 (AnyCompany Air and Health); the team leg about $110 (measured on a former sample, 36 turns, each resuming the whole session). Run the team leg before a release, not on every change.

Checks:

- **D (mechanics):** required artifacts, the brief's 15 sections, links, no emails or CRM identifiers, `.gitignore`, no scripts, prototypes built from the shell, versions logged, the critique in `prototype/`, every persona's walk recorded in the prototype and fitting its screens, the decision, no GTM part left as draft, team expectations written before the analysis, `next-steps.md` with its Now, Next, Later roadmap.
- **O (outcome):** graded against the `expectations` block in `facilitator/<sample>.md`: the top signal, the distractor failing the gate, and the use case taken forward. For samples with telemetry, also the Say and do table (O04), the telemetry trap not ranked first (O05), a telemetry-only signal (O06), and the feasibility evidence from telemetry (O07). Alternative phrasings are separated by `|`.
- **N (negative)** and **T (team)**, for those legs.

Each run writes `.e2e/<timestamp>/` with every workspace, transcript, and cost, plus `report.md`. Calls are billed to the AWS account the Claude Code CLI uses, and `--budget-usd` caps every call.

These runs test the method and the artifacts. They run in Claude Code, not AWS Quick or Cowork, so check a release in AWS Quick by hand as well (and in Cowork, see below): import it, start Discovery on a sample, and build a prototype.

## Cowork runs (by hand, or unattended)

Cowork runs in the desktop app, so it has no headless runner. Build the Cowork skill, run Discovery in Cowork on a copy of a sample, then grade the working folder with the same checks:

```bash
python3 scripts/build.py --target cowork
mkdir -p .e2e/cowork-air && cp -r samples/anycompany-air .e2e/cowork-air/workspace
# add config.md with unattended: true (as run_e2e.py writes it), connect the folder in Cowork,
# and start the run with the prompt in tests/e2e/prompts/workshop.md
python3 tests/e2e/check_workspace.py .e2e/cowork-air/workspace --sample air --journey
```

`--journey` (or `--cowork`) adds the journey app checks (C), for a run in either tool: the app was created, its data parses, the page is the shell unchanged, it holds every artifact and prototype version, the Now banner is set, it loads nothing from the web, and, with node installed, it shows the five phases complete and the decision. `tests/test_cowork.py` covers the Cowork build, and `tests/test_journey.py` the shell, the update script as the skill states it, and the page's renderer (in node), without model calls.

Measured on AnyCompany Air (2026-11-25, three unattended runs, one Cowork session each): 36 checks, 0 failed in the first two; the third failed O03 only because scoring renamed the team's candidates, which scoring now keeps. About 100 to 140 tool calls and 40 to 90 minutes a run; the journey app updated 7 to 8 times and the prototype artifact twice.
