# AnyCompany Health: a member portal under pressure

A fictional sample for AI-DLC Discovery: a health insurer's member portal and app. Its data is regulated and cannot leave its environment, so the team brings Signal Briefs and aggregate statistics instead of raw records. AnyCompany Health, its members, and every record here are made up.

This folder is laid out the way a real team's working folder is:

- `discovery/kickoff.md`, the kickoff page the team filled in before the workshop: the product, the team and what each role believes, the business metric with its baseline, the five candidate use cases, and the data.
- `discovery/signal-briefs/`, the Signal Briefs and aggregates the team brings.

## How to run it

1. Give the app access to this folder (`samples/anycompany-health`): in AWS Quick Desktop, open **Settings**, then **My computer**, then **Local folders**, and add it; in Claude Cowork, connect it to a new task.
2. Start Discovery:

   ```text
   Start AI-DLC Discovery. Project: member-portal.
   ```

   The assistant drafts the setup from `discovery/kickoff.md` and asks you to confirm it.
3. Play the team: read `discovery/kickoff.md`, answer as the roles it lists, and write the team's expectations before the analysis.

The designed answers are in [facilitator/anycompany-health.md](../../facilitator/anycompany-health.md). Read it after the run, not before.
