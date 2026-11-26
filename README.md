# AI-DLC Discovery

Agent skills that run product discovery (see [Supported tools](#supported-tools)). A product engineering team brings its customer feedback and leaves with a decision on what to build first, a clickable prototype, and a **Discovery brief**: one document the build starts from, whether the team builds it itself, with agents, or with [AI-DLC](https://github.com/awslabs/aidlc-workflows).

Discovery is the part of the AI-Driven Development Lifecycle (AI-DLC) that decides what to build and for whom. When a team continues into AI-DLC, the brief takes the place of AI-DLC's own Ideation phase, and AI-DLC starts at Inception.

**Workshop:** to learn the method hands-on, follow the [AI-DLC Discovery workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/cd263623-2478-48f8-b5bf-f7cd56d731f6/en-US) in AWS Workshop Studio. The workshop uses AWS Quick. To run Discovery in Claude Cowork, follow [Run it in Claude Cowork](#run-it-in-claude-cowork) below.

## What this sample demonstrates

- **A product method packaged as agent skills.** Five phases (Signals, Working Backwards, Prototype, Validate, Handoff), run by one entry skill that calls ten job skills. Each job also works on its own.
- **AI that drafts and humans who decide.** The skills analyze, draft, and cite evidence, then stop at a checkpoint after every phase. The team reviews every score, writes or challenges every document, and makes the build decision.
- **Evidence you can trace.** Every claim in the PR/FAQ, PRD, go-to-market section, and brief is labeled Known (backed by the data), Assumed, or Needs evidence. Anything still unproven goes into the brief as an open question.
- **Customer data handled with care.** The skills work on production data, on anonymized Signal Briefs written in the team's own environment, or on a synthetic dataset prepared beforehand. They never invent data during a run, and raw data stays out of version control. Beforehand, the team runs [`tools/prepare-data`](tools/prepare-data/README.md) on its own machine: a short, readable Python script around [Microsoft Presidio](https://presidio.dataprivacystack.org/) that removes personal information offline, so raw records never reach the AI assistant.
- **A handoff a build can read.** The Discovery brief is plain Markdown under 200,000 characters, written for a person or an agent who took no part in Discovery. For AI-DLC 2.10.0 or later, the skills also write the personas into AI-DLC team knowledge and give the command that starts Inception from the brief.

## How Discovery runs

| Phase | The question | What the team leaves with |
|-------|--------------|---------------------------|
| 1. Signals | What are customers telling us? | The team's expectations, written first; a Signal Analysis Report; testable hypotheses |
| 2. Working Backwards | Which problem first, for whom, and how would we announce it? | Personas; 3 to 5 use cases scored on six weighted dimensions; PR/FAQ; PRD; go-to-market draft; the riskiest assumption |
| 3. Prototype | What would it look like? | A multi-screen prototype with Flow, Mobile, and Desktop views, critiqued by the personas; every iteration kept as a version |
| 4. Validate | What could make it fail, and how will we know it worked? | Four risks (valuable, usable, feasible, viable); a pre-mortem; testable success criteria; commit, pivot, or park |
| 5. Handoff | What does the build start from? | The Discovery brief, and the next steps |

A team can run the phases in one sitting or across several sessions; every artifact is saved as a file, so Discovery picks up where it stopped.

## The skills

| Skill | Phase | Job |
|-------|-------|-----|
| `aidlc-discovery` | All | Runs Discovery: setup, phase order, checkpoints, and shared rules |
| `discovery-signals` | Signals | Team expectations, then the analysis of feedback, Signal Briefs, or a synthetic dataset |
| `discovery-personas` | Working Backwards, Prototype | Personas from the data; the persona critique of the prototype; persona role-play and panels |
| `discovery-use-case-scoring` | Working Backwards, Validate | Gate, six weighted scores, confidence, and a decision for each candidate use case |
| `discovery-working-backwards` | Working Backwards | The five Working Backwards questions, PR/FAQ, readiness check, PRD, riskiest assumption |
| `discovery-gtm` | Working Backwards, Validate | First adopters, positioning, viability check, adoption and success targets |
| `discovery-prototype` | Prototype | The clickable prototype, the critique, and the iteration |
| `discovery-validate` | Validate | Four risks, pre-mortem, success criteria, prioritized problems, and the decision |
| `discovery-handoff` | Handoff | The Discovery brief, AI-DLC team knowledge, and next steps |
| `discovery-signal-brief` | Before Discovery | Optional. The team writes anonymized Signal Briefs from its own data |
| `discovery-survey` | After Discovery | Optional. Surveys that test the open hypotheses with real users, and a results dashboard |

In this repository each skill is its own folder under [`skills/`](skills/), with a `SKILL.md` and, where needed, `references/` that hold the detailed prompts, so each job is easy to read, change, and test. For installation, [`scripts/build.py`](scripts/build.py) bundles them into **one** skill, `aidlc-discovery`, with a module per job that loads only when its step runs. You install, update, and remove one item. The skills follow the [Agent Skills](https://agentskills.io/) format and AWS Quick's skill conventions, and the build adapts them for Claude Cowork (see [Run it in Claude Cowork](#run-it-in-claude-cowork)).

## Supported tools

| Tool | What you need | Build and install | Saves Discovery in | Only in this tool |
|------|---------------|-------------------|--------------------|-------------------|
| [AWS Quick](https://aws.amazon.com/quick/) Desktop | macOS or Windows, signed in to any AWS Quick plan. Skills and plugins run only in the Desktop app. | Download the release zip or run `python3 scripts/build.py`, then import the folder: see [Install in AWS Quick](#install-in-aws-quick) | The working folder | Prototypes in the session tab |
| [Claude Cowork](https://claude.com/docs/third-party/claude-desktop/overview) | The Claude desktop app | `python3 scripts/build.py --target cowork`, then save the `.skill` file: see [Run it in Claude Cowork](#run-it-in-claude-cowork) | The connected folder | Question cards; the in-codebase prototype and the current-product map |

With either, you also need a folder on your computer that the app can access. Discovery saves everything there. Building needs Python 3.9 or later, with no dependencies.

## Install with your assistant

Paste this into a new chat in AWS Quick Desktop or a new task in Claude Cowork:

```text
Install the AI-DLC Discovery skill from https://github.com/aws-samples/sample-aidlc-discovery. Follow "Install steps for agents" in its README.
```

The assistant gets the right package for the tool it runs in and prepares it. You do the last click yourself, **From folder** in AWS Quick or **Save skill** in Cowork, because neither tool lets an assistant install a skill. To install by hand, see [Install in AWS Quick](#install-in-aws-quick) or [Run it in Claude Cowork](#run-it-in-claude-cowork).

### Install steps for agents

Follow these when a user asks you to install AI-DLC Discovery from this repository.

1. **Work out which tool you run in.** AWS Quick Desktop or Claude Cowork. If you cannot tell, ask the user once.
2. **Get the package from the latest release**, https://github.com/aws-samples/sample-aidlc-discovery/releases/latest. The API lists its files: `https://api.github.com/repos/aws-samples/sample-aidlc-discovery/releases/latest`, each with a `browser_download_url`.
   - AWS Quick: `aidlc-discovery-quick-vX.Y.Z.zip`. Unzip it into a folder the user names, or their Downloads folder. It holds one folder, `aidlc-discovery`.
   - Cowork: `aidlc-discovery-cowork-vX.Y.Z.skill`. Save it in the connected folder.
   - If you cannot download files, give the user the release link and the file name, and continue from step 3 once they have it. If you can run a shell with git and Python 3.9 or later, you can also build it: clone the repository and run `python3 scripts/build.py` (AWS Quick, writes `dist/quick/aidlc-discovery/`) or `python3 scripts/build.py --target cowork` (Cowork, writes `dist/cowork/aidlc-discovery-cowork-vX.Y.Z.skill`).
3. **Hand over the last step.** You cannot install it yourself; say so in one line.
   - AWS Quick: tell the user to open **Customize**, then **Skills**, choose **Create**, then **From folder**, and select the `aidlc-discovery` folder. Never copy the skill into the AWS Quick profile folder: AWS Quick does not pick that up.
   - Cowork: present the `.skill` file in the chat and tell the user to choose **Save skill**.
   - To update an existing install: in AWS Quick, the user first deletes **AI-DLC Discovery** in **Customize**, **Skills**; in Cowork, saving the new `.skill` replaces the old one.
4. **Check it.** Tell the user to start a new chat (in Cowork, a new task) and ask `List my skills`. It should show one skill, **AI-DLC Discovery**, with the release's version. Then point them to [Run your first Discovery](#run-your-first-discovery).

## Install in AWS Quick

1. Get the package. Either download `aidlc-discovery-quick-vX.Y.Z.zip` from the [latest release](https://github.com/aws-samples/sample-aidlc-discovery/releases/latest) and unzip it, which gives you an `aidlc-discovery` folder, or clone this repository and build it (Python 3.9 or later, no dependencies):

   ```bash
   python3 scripts/build.py
   ```

   This writes `dist/quick/aidlc-discovery/`, the plugin manifest and one skill, `aidlc-discovery`, with its modules, and the same folder zipped as `dist/quick/aidlc-discovery-quick-vX.Y.Z.zip`.
2. In AWS Quick Desktop, open **Customize**, then **Skills**, choose **Create**, then **From folder**. Select the unzipped `aidlc-discovery` folder, or `dist/quick/aidlc-discovery` if you built it.
3. In a new chat, ask `List my skills`. You should see one skill, **AI-DLC Discovery**.

**How AWS Quick stores the skill.** Importing from a folder uploads a snapshot of the skill to AWS Quick's own storage. AWS Quick reads that snapshot, not the folder on your computer, so you can move or delete the folder after importing, and changing files in it has no effect until you import again.

**To update:** delete **AI-DLC Discovery** in **Customize**, **Skills** (the ⋮ menu on its row); build again (or download and unzip the new release); import the new `aidlc-discovery` folder; and start a new chat. Check the version in `List my skills`. A build from anything but a release ends its description with the commit it was built from, such as "Development build f149ce5 of 3.0.0.", so you can see which build is installed.

Copying the skill folder by hand into the AWS Quick profile folder is not a supported install: AWS Quick may not pick up later changes to it. Import from a folder.

**Viewing prototypes.** Prototypes open in AWS Quick's session tab, and as plain files in any browser. If a view does not switch in the session tab, open the file from your working folder (`discovery/[project]/prototype/`).

## Run it in Claude Cowork

The same skills also build for [Claude Cowork](https://claude.com/docs/third-party/claude-desktop/overview). The Cowork build is one skill, with the tool names and steps rewritten for Cowork, and two differences:

- **No artifact prompts.** Cowork asks you to approve every artifact it creates or updates, so the skill publishes none on its own. The journey app and every prototype version open in the file preview, and the browser view of `journey.html` follows every step. Ask for an artifact when you want one.
- **Question cards.** Each round of questions also appears as Cowork's multiple-choice cards, with the recommended answer first. Free-text questions, such as the team's expectations, stay in chat.

To install:

1. Build it (Python 3.9 or later, no dependencies):

   ```bash
   python3 scripts/build.py --target cowork
   ```

   This writes the skill folder `dist/cowork/aidlc-discovery/` and the same folder packaged as `dist/cowork/aidlc-discovery-cowork-vX.Y.Z.skill`.
2. In Cowork, open the `.skill` file in a chat (or ask Claude to present it) and choose **Save skill**.
3. Connect the folder of a sample, for example `samples/anycompany-air`, start a new task, and use the prompt on the sample's page.

To update, build again and save the new `.skill` file over the old skill. Start a new task, and check with `List my skills` that the description ends with the commit you built. The build fails if a source sentence it rewrites for Cowork has changed, so a change in `skills/` cannot reach the Cowork build unadapted: update `COWORK_REWRITES` in `scripts/build.py` when it does.

## What Discovery covers

Discovery ends with a decision on what to build and why. Building, running, and operating the product come after, with the team's own engineers, AI-DLC, or AAP, and the Discovery brief is what they start from.

- **Covered:** customer signals, personas, use case scoring, the PR/FAQ and PRD, a clickable prototype, and, for AI features, a first-draft prompt and evaluation cases. Also the business side of launch: the viability check, go-to-market, success criteria, and the commit, pivot, or park decision.
- **Owned by the build:** architecture, model selection, the data and retrieval design, the final prompt, evaluation automation, operational readiness, rollout, and support.
- **Out of scope:** product strategy across several products, product management operating models, and AI use case selection outside a product team's own product.

## Run your first Discovery

Two samples are ready to run. AnyCompany Air is the default: start there if you are new. Each is a realistic, fictional business with feedback from customers, frontline staff, account teams, and sales, and each hides an answer the method has to find. Pick one:

- [**AnyCompany Air**](samples/anycompany-air/): an airline whose customers and corporate accounts complain. 400 records from reviews, call center contacts, social posts, NPS, corporate account notes, and travel agencies, plus operations data and the app's telemetry (real user monitoring journeys, backend spans, and top errors). Production data with telemetry.
- [**AnyCompany Health**](samples/anycompany-health/): an insurer's portal for members, employers, and brokers. Regulated, so the data never leaves the insurer: 10 Signal Briefs and aggregate statistics only. Signal Briefs.

Each sample folder is laid out the way a real team's working folder is: its kickoff page, `discovery/kickoff.md`, holds the company, who is on the team and what they believe, the business metric with its baseline, the candidate use cases, and the data, and the data sits next to it. The skills take all their context from that page, exactly as they do for a customer. To run one:

1. Give the app the sample's folder, for example `samples/anycompany-air`. In AWS Quick Desktop, open **Settings**, then **My computer**, then **Local folders**, and add it. In Cowork, connect it to a new task.
2. Start Discovery with the prompt in the sample's `README.md`, confirm the setup the assistant drafts from the kickoff page, and answer as that team.

The skill asks once, optionally, for the team's expectations before it shows any analysis, and stops for review at the end of every phase. With sample data it says the run is a demonstration: the flow is real, but the brief is not evidence for a build.

**Answer keys:** each sample has notes in [`facilitator/`](facilitator/) with the designed answers, the expected scoring, and the traps to watch for. Read them after a run, not before. The same folder holds material for running Discovery as a facilitated session: [`facilitator/kickoff-call.md`](facilitator/kickoff-call.md), [`facilitator/run-sheet.md`](facilitator/run-sheet.md), [`facilitator/dry-run-air.md`](facilitator/dry-run-air.md), and [`facilitator/train-the-trainer.md`](facilitator/train-the-trainer.md). [`samples/CONVENTIONS.md`](samples/CONVENTIONS.md) explains how the samples are built, for anyone adding one; the data is generated by the scripts in [`scripts/samples/`](scripts/samples/).

## Use your own data

**Start with the kickoff page.** Give the team [`skills/aidlc-discovery/templates/kickoff.md`](skills/aidlc-discovery/templates/kickoff.md) (in Japanese, [`facilitator/ja/kickoff.md`](facilitator/ja/kickoff.md)) a week before the workshop: one page with the product, the team and what each role believes, the business metric with its direction and baseline, the ideas the team already has, the data, and what cannot change. [`facilitator/kickoff-call.md`](facilitator/kickoff-call.md) has the email to send with it and what to ask on a 30-minute call. Save the filled-in page as `discovery/kickoff.md` in the working folder, next to the data, the same layout as the samples, and setup drafts everything from it in one confirmation. The assistant can also save a blank copy for you: ask for the kickoff page.

Choose how the data comes in at setup:

- **Production data** (the default). Feedback the team can load into its own AWS Quick or Cowork: exports in `discovery/data/` in the working folder, or, in AWS Quick, a Space with connectors to the team's sources. JSON, CSV, Excel, PDF, DOCX, and plain text work.
- **Signal Briefs.** When the data cannot be loaded into a tool for Discovery, the team runs `discovery-signal-brief` in its own environment to write one anonymized page per customer problem, and brings only the briefs.
- **Synthetic dataset.** When neither is possible yet, prepare a dataset beforehand, and plan a follow-up on real data. To rehearse with your own columns, `tools/prepare-data` can write invented rows in the shape of your scrubbed data (`--synthetic 500`). They show the structure only, never evidence.

With any of them, add **telemetry** if the team has it: daily aggregates per journey step from CloudWatch, Datadog, or OpenTelemetry exports (real user monitoring, spans, top errors), in a `telemetry/` folder next to the feedback. Signals reads it next to the feedback and writes a Say and do table: what customers say against what the systems show. See `skills/discovery-signals/references/telemetry-analysis.md` and [docs/telemetry-signals.md](docs/telemetry-signals.md).

For the best result, the team also brings 3 to 5 candidate use cases, each written as a problem, and the business metric it wants to move with its current value. Use the product's own repository as the working folder, so the brief lands where the team will build.

If your feedback contains personal or confidential information, follow your organization's data handling rules before you use it, and run [`tools/prepare-data`](https://github.com/aws-samples/sample-aidlc-discovery/tree/main/tools/prepare-data) on your own machine first: it removes names, logins, emails, and other identifiers offline, and writes a report to review before you share anything. The skills keep raw data in `discovery/data/`, add that folder to `.gitignore`, and quote customers only in anonymized form in the artifacts they save.

## What you get

```text
discovery/
├── data/                       raw data, never committed
└── [project]/
    ├── PROJECT.md              scope, choices, phase status
    ├── journey.html            the journey app, generated from the files
    ├── signals/                team-expectations.md, signal-summary.md, hypotheses.md
    ├── working-backwards/      personas/, use-case-scoring.md, working-backwards.md,
    │                           feature-description.md, prfaq.md, prd.md, gtm.md,
    │                           riskiest-assumption.md
    ├── prototype/              v1.html, v2.html, ... (every version), index.html (the chosen one),
    │                           versions.md, compare.html, persona-critique.md, notes.md
    ├── validate/               risk-review.md, prioritization.md, decision.md
    └── handoff/                discovery-brief.md, next-steps.md (with the roadmap)
```

**The journey app**, `journey.html`, lets the room follow along, in AWS Quick and in Cowork. It shows the five phases and their status, a **Now** banner with the step the team is on and what comes next, every artifact rendered from its file, the prototype versions clickable in place, the decision with its conditions, and how many claims are Known, Assumed, or Needs evidence. The skill creates it after Setup from a fixed page (`skills/aidlc-discovery/references/journey-shell.md`) and updates it at the start of every step with a short Python script that copies the project's files into the page, so the files stay the record. In AWS Quick it opens in the session tab; in Cowork, in the file preview. It never reloads by itself, so nobody loses their place while reading: reload it, or click a phase, to see the latest step. To put it on the room's screen, open `discovery/[project]/journey.html` from the working folder in a browser.

**Running again, and resuming.** Every run is a project folder, `discovery/[project]/`, so runs never mix. When Discovery starts, it lists the projects already in the working folder and asks whether to continue one or start a new one; a new run with a name already used becomes `[project]-2`, and nothing is overwritten. To resume in a new chat, even after the old chat is gone, say "Continue AI-DLC Discovery for [project]": the journey update keeps a `Now:` line in `PROJECT.md` with the step the team is on, and the skill picks up there.

The Discovery brief has fifteen sections: context (date, route, and data), decision, problem and evidence, personas, prioritized use cases, PR/FAQ summary, success criteria, go-to-market, scope, prioritized backlog, prototype screens and flows, current product, constraints, open hypotheses, and links to every artifact. It contains no architecture or technology choices; those belong to the build. For an AI feature, it also carries the AI feature block and the AI quality target.

`next-steps.md` ends with a **roadmap for the product owner: Now, Next, Later**. Now is the use case taken forward and its conditions; Next is each deferred candidate with the evidence that would move it up and who gets it; Later is the rest, with why. Customer problems and the metrics they move, ordered by conditions, with no delivery dates.

## From the brief to a build

`handoff/next-steps.md` says what to do with the brief. To build with AI-DLC 2.10.0 or later, commit the `discovery/` and `aidlc/` folders to the repository where the team will build, and run there:

```text
aidlc config --harness <claude | kiro | kiro-ide | codex | cursor | opencode | copilot>
/aidlc workshop Read ./discovery/[project]/handoff/discovery-brief.md and build what it describes, [product or feature name]
```

The command is `/aidlc [scope] [intent description]`. `workshop` is one scope: use another, such as `classic`, or leave the scope out, and AI-DLC suggests the one that fits. The skills write the intent description in the project language. AI-DLC reads the brief as its single input and generates the requirements, user stories, and design from it. Neither AWS Quick nor Cowork runs AI-DLC itself, so the skills print the command and stop.

## Things to know

- **Personas are synthetic.** They are drawn from the data, but they are not customers. Validate never waits for surveys; the real-user test of the prototype, and the open hypotheses, belong in the follow-up. `discovery-survey` helps with that.
- **The prototype is a single HTML file** with no backend, meant to start a conversation. Surveys are generated as HTML previews and as questions to paste into a form tool, because the assistant cannot host a form.
- **AWS Quick and Cowork change often.** Menu names in these instructions may differ slightly in your version.
- **The skills are tool-agnostic in format,** and are written and tested for AWS Quick Desktop and Claude Cowork. The in-codebase prototype and the current-product map need a tool that can read and run code, and are skipped in AWS Quick.

## Repository layout

```text
plugin.json, mcps.json, tasks.json   plugin manifest for AWS Quick Desktop
skills/                              the eleven skills, one folder each (the source)
scripts/build.py                     bundles skills/ into one installable skill in dist/quick/ (AWS Quick) or dist/cowork/ (Cowork)
cowork/                              Cowork only: the "Running in Cowork" section
scripts/bump_version.py              works out the release version from the latest tag, at release time
samples/                             two runnable business cases, and how they are built
scripts/samples/                     the generators that write each sample's data
tests/                               checks for the skills and the bundle
tools/prepare-data/                  removes personal data from exports before a workshop
facilitator/                         answer keys, run sheet, dry run, and train-the-trainer
docs/                                design notes: telemetry signals
```

## Tests

```bash
python3 -m unittest discover tests
```

End-to-end runs in Claude Code and in Cowork, graded against each sample's answer key, are described in [TESTING.md](TESTING.md).

The tests check that every skill has the required frontmatter and sections, that every referenced file exists, that the entry skill depends on every job skill, that each artifact the Handoff requires is written by the skill that owns it, and that the brief keeps its fifteen sections and the AI-DLC contract. They check that every sample follows the conventions, has no duplicate records, and is reproduced exactly by its generator. They also build the bundle and check it: one skill, a module and a route for every job, every path resolving, and no path left pointing at the source layout.

## Acknowledgements

Several Working Backwards practices in `discovery-working-backwards` (the seven-paragraph press release and its structural checks, the prototype readiness questions, the framing rules, and the writing audit) are adapted from the AI-Driven Working Backwards delivery kit by the AWS Digital Innovation team.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.
