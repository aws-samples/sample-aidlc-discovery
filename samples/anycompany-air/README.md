# AnyCompany Air

A fictional sample for AI-DLC Discovery: an airline's website and app, with customer feedback, operations data, and telemetry. AnyCompany Air, its customers, and every record here are made up.

This folder is laid out the way a real team's working folder is:

- `discovery/kickoff.md`, the kickoff page the team filled in before the workshop: the product, the team and what each role believes, the business metric with its baseline, the five candidate use cases, and the data.
- `discovery/data/`, the exports the team brings, with the telemetry in `discovery/data/telemetry/`.

## How to run it

1. Give the app access to this folder (`samples/anycompany-air`): in AWS Quick, add it as a local folder; in Claude Cowork, connect it to a new task.
2. Start Discovery:

   ```text
   Start AI-DLC Discovery. Project: anycompany-air.
   ```

   The assistant drafts the setup from `discovery/kickoff.md` and asks you to confirm it.
3. Play the team: read `discovery/kickoff.md`, answer as the roles it lists, and write your expectations before you see any analysis.

The designed answers are in [facilitator/anycompany-air.md](../../facilitator/anycompany-air.md). Read it after the run, not before.
