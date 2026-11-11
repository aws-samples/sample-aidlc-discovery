# Facilitator run-sheet

One day, one product engineering team, five phases. Keep this page open beside you. The skill runs the method; your job is the room: time, energy, and making sure the team does the thinking.

## Before the day

**Install, a day ahead.**
- In AWS Quick Desktop: **Customize**, **Skills**, **Create**, **From folder**, then pick `dist/aidlc-discovery` (built with `python3 scripts/build.py`).
- Import stores a snapshot. Editing the folder afterwards changes nothing. To update: remove the plugin, import again, start a new chat.
- Check the install in a new chat: `List my skills` shows one skill, AI-DLC Discovery Workshop.
- Run the 30-second module check: "Use the aidlc-discovery skill. Load modules/discovery-signals.md with file_read and tell me what Step 1 says." It must answer: the team's expectations, optional, asked once before any analysis. If it cannot find the file, reinstall.

**Rehearse once.** Run a sample end to end (see `dry-run-air.md`). New facilitators can also take the half-day session in `train-the-trainer.md`. You will meet every checkpoint before the team does.

**Agree with the team:**
- **Who is in the room.** The product owner and engineering lead who own the build. Add design, data, support, or sales as needed. 4 to 6 people, or pods of 4 to 5.
- **The data input.** Production data in their own AWS Quick (the default), Signal Briefs when data cannot be loaded into a tool, or a synthetic dataset prepared before the day. Never let the assistant invent data on the day.
- **Telemetry, if the team has it.** Daily aggregates per journey step from their monitoring (CloudWatch, Datadog, or OpenTelemetry exports in S3): sessions per step from real user monitoring, requests, errors, and latency per service, and the top error codes, with a short map from each step to its screen and backend route. Never raw logs or traces: they are too large and carry personal data. Telemetry is read next to the feedback, never instead of it.
- **3 to 5 candidate use cases,** each written as a problem: who has it, the problem, the evidence they think they have, the business metric it moves, and the owner.
- **The business metric and its baseline.** If there is no baseline, name who gets it by the 7-day follow-up.
- **A working folder** AWS Quick can access, ideally the product's own repository.
- **Where the workshop is saved.** Recommended: a team Space (AWS Quick only), so everyone in the room can follow the workshop from their own AWS Quick, open the prototype, and take over facilitation, and the workshop stays in AWS Quick after the day. The team creates the Space and names it (**Spaces**, then **Create space**), shares it with the people who will follow or take over as **Owners**, and each person attaches it to their chat with the **+** menu, then **Spaces**. Or use a local working folder on the facilitator's laptop. **Where the data goes:** everyone a Space is shared with can read it. Put the customer data in the team Space only if it is shared with nobody who should not see the data; otherwise keep it in the working folder or in a separate, restricted Space, and name that in the start prompt. The skill asks you to confirm before it analyzes data that sits in the workshop's Space. Sample data is fictional and can go in the Space.

## The day

### 09:00 Kickoff (30 min)
- **Goal:** everyone knows why they are here and how the day runs.
- **Say:** "Today we decide what to build next, from evidence, and we leave with a brief the build starts from. The assistant drafts; you decide. It stops after every phase, and nothing moves on until you say so."
- **Ask the assistant:** "Start an AI-DLC Discovery workshop. Project: [name]. Engagement reference: [reference or Self-serve]. Save the workshop in the [Space name] space. Data: [input], in [folder]." Leave out the Space sentence to save in the working folder.
- **With a Space attached,** it asks once whether to save the workshop in the Space or the folder. Say the Space, and tell the room AWS Quick may ask to approve each save. Everyone else attaches the Space now and follows along in their own chat, reading, not writing.
- **Good looks like:** it drafts the setup from what it can find (a scenario page, the folder, `config.md`) and asks the room to confirm, or asks in one or two rounds of numbered questions, each with a recommended answer, when there is nothing to draft from. Then it writes `PROJECT.md`. Read the draft aloud and have the product owner confirm the business metric and which direction is good: everything is scored against it.
- **Facilitator practice:** don't confirm the setup yourself. Ask the product owner, "Is anything here wrong or missing?" If the sponsor leaves after the kickoff, ask them now whether the metric is the one they care about.

### 09:30 Signals (60 min)
- **Goal:** the team's beliefs on record, then tested against the data.
- **Say:** "Before we see any analysis, each of you writes down what you think the data will show. We will check ourselves against it."
- **Watch:** it asks once for the team's expectations before showing anything, and accepts "skip". Go round the room, one line per person; if nobody has one, say skip and move on.
- **Facilitator practice, expectations:** it asks one question. Read it aloud and wait. The most senior person tends to answer first and the rest agree; ask the quietest person first.
- **Facilitator practice, the inventory:** before the room confirms the data inventory, ask the person closest to each gap whether that data exists. A gap named now is an open question in the brief; a gap found at the readout costs you credibility.
- **Good looks like:** top signals with counts and quotes, every claim labelled Known, Assumed, or Needs evidence, and a "What the team expected" table. With telemetry, a **Say and do** table: each theme marked as seen in both, feedback only, or telemetry only.
- **Facilitator practice, the dashboard:** when an engineer points at the loudest error, ask "How many customers did it stop?" Then show the journey: a journey that fails as designed returns success, so no dashboard shows it.
- **Facilitator practice, contradicted beliefs:** start with what the person got right. Read the "where you're right" part aloud to them first, then the part that disagrees.
- **Facilitator practice, counter-evidence:** before the challenge, ask "Where does it work well?" The checkpoint summary may skip the positive theme, but the report has it. A team that hears only problems gets defensive; a team that hears "you're good at this, and failing at this one moment" gets focused.
- **Checkpoint:** "What do you challenge before we decide what to work on?" Get at least one real challenge, ideally from the person whose belief the data contradicts.
- **Facilitator practice, closing the phase:** credit the challengers by name: "Your challenge changed the report." Then ask the product owner, "Are we agreed this is the problem we work on?", and wait for a yes.

### 10:45 Working Backwards 1 (75 min)
- **Goal:** personas, scored use cases, one selected.
- **Say:** "Now we score your candidates. The assistant drafts every score with its evidence. You confirm or override each one."
- **Watch:** personas include one satisfied customer. The gate drops a candidate customers would not miss. Strategic fit and feasibility are marked for the team to judge; ask the engineering lead about feasibility.
- **Facilitator practice, personas:** ask the people closest to customers first: "Have you met this person?" Every persona costs time in the critique, so ask whether any two overlap; set-aside personas go to `set-aside-personas.md`.
- **Facilitator practice, feasibility:** it belongs to the engineering lead. Don't let a drafted score stand by silence: ask "What would make this a 2, and what would make it a 4?" The answer is the build's biggest unknown.
- **Facilitator practice, owners:** when a candidate's owner is in the room, ask them before the room agrees: "It's your candidate. Anything the scores miss?" An owner who agrees out loud to defer their own idea is a stronger result than a silent defer.
- **Facilitator practice, overrides:** after an override, show the new weighted score and say whether the decision changed. Often it doesn't, and the person has still been heard.
- **Facilitator practice, when the assistant questions an override:** give the person who made it the last word: "Does that change your view, or do we keep it?" The team owns the score; the assistant makes the evidence visible.
- **Candidates from Signals:** before the gate, the assistant adds two or three from themes the team's candidates do not cover. Keep or drop each in one sentence with a reason; about a minute. Kept ones are scored like the rest.
- **Personas, buyer and end user:** when the person who buys is not the person who uses (a travel manager and a traveller), there should be one persona for each. The buyer judges value and cost; the end user judges the workflow.
- **Facilitator practice, weights:** settle them with the sponsor before the first score, and say why: "Once we see scores, nobody can move a weight to help their favourite."
- **Timing tip:** when the room agrees with a candidate's drafts, choose "agree with all" and move on. Spend the time on the scores people disagree with.
- **Checkpoint:** every score confirmed or overridden, with reasons recorded, and one use case selected (one per pod).

### 12:00 Lunch (60 min)
- **Ask the assistant:** "We're breaking for lunch. Draft the PR/FAQ while we're away."
- It writes a straw-man PR/FAQ, marked as a draft, so the room returns to something to challenge.

### 13:00 Working Backwards 2 (55 min)
- **Goal:** the team owns the PR/FAQ, the PRD scope, the GTM draft, and the riskiest assumption.
- **Say:** "This is the AI's draft. Read the press release aloud. Change anything that doesn't sound like us."
- **Listen for the framing first.** The five questions should produce three sentences the room agrees with: a **Today statement** whose "need a way to" names an outcome, not a feature; a **How Might We**; and a **North Star** that names a capability, not a product, with numbers tied to the business metric. If a feature has crept into the need, ask "what does that give the customer?"
- **Good looks like:** a press release with a headline, a subheading, and exactly seven paragraphs (summary, problem, solution, leader quote, customer experience, testimonial, call to action) in 500 to 700 words, no headings inside, the customer as the subject; a one-line writing-audit result; a readiness verdict of GREEN or AMBER with a Prototype scope section that names the slice the prototype will show; a small P0; and one riskiest assumption.
- **Facilitator practice, targets:** they are the team's commitment, not the assistant's guess. Ask the product owner and the person who will feel it most to say the numbers out loud: "Can we sign up to this?" A target nobody said out loud is a target nobody owns.
- **Facilitator practice, reading aloud:** read the press release slowly. Stop at any sentence where someone winces and ask "How would we say it?" Rewriting one sentence together makes it the team's document.
- **Facilitator practice, the verdict:** AMBER is a good result; don't chase GREEN. Close any gap the room can answer in two minutes, carry the rest as open questions with an owner. A must-have gap that only a test can close is what the prototype is for.
- **The AI feature block (AI features only, about 10 minutes):** in the PRD, a first-draft prompt and 5 to 10 evaluation cases from the quotes and the personas, typical, edge, and negative, plus sample outputs for the prototype. It is a starting point; the build chooses the model, the data, and the final prompt.
- **Facilitator practice, evaluation cases:** have the person closest to customers read the negative cases aloud and say what a good answer is. The cases the feature must refuse come from the room, not from the model.
- **If the verdict is RED,** spend ten minutes closing the gaps before the PRD. A prototype built on a vague PR/FAQ tests nothing.
- **Facilitator practice, the riskiest assumption:** the most anchored decision of the day. Everyone chooses before anyone speaks: on paper shown at once, or typed in the chat at the same moment. Then ask the outliers why: "Which one, if wrong, means we built something nobody uses?"
- **Facilitator practice, the pass mark:** set the thresholds for the riskiest assumption now, before anyone sees a result. A threshold chosen after the test bends to fit it. Ask: "What result would make us stop?"
- **Facilitator practice, owners for open questions:** before the phase closes, put a name and a date on every open question that blocks the build: who recruits real users, who runs the spike, who asks security. An open question without an owner is still open at the 30-day follow-up.
- **Checkpoint:** "What must the prototype prove?"

### 13:55 Prototype (60 min)
- **Goal:** a clickable prototype, critiqued, changed once.
- **Watch:** it plans 4 to 8 screens and marks the test moment. For an AI feature, the screens show the sample outputs from the AI feature block, so the persona critique reacts to real AI output. The file opens on a Flow board of phone frames, with Flow, Mobile, and Desktop tabs. Then your click-through, then the persona critique, then an iteration saved as a new version.
- **Facilitator practice, changes to the plan:** when the assistant changes what the team agreed (a path dropped, a shortcut added), read each change to the room and ask its owner: "Keep it, or change it back?" Decide before the click-through; a change nobody decided becomes a surprise at the readout.
- **Facilitator practice, factual questions:** when the assistant asks one (what time does the line close?), get the answer from the person who knows, or record it as Needs evidence. A guessed fact in the prototype becomes a promise in the brief.
- **Watch, claims on screen:** anything the prototype shows that nobody has confirmed (a bag that moves, a booking that is final, a call-back at any hour) should be marked Needs evidence. Ask the person who would know whether it is true today.
- **Timing tip:** teams often say "looks good" on their first click-through. That is fine. The persona critique finds the problems; let the room pick which to fix.
- **Facilitator practice, choosing fixes:** fix first what touches the riskiest assumption, then what is cheap; send the rest to Validate with an owner. If a finding changes what the riskiest assumption means, update it now.
- **Checkpoint:** "Here is what your personas said and what we changed. Ready to try to break it?"

### 14:55 Break (10 min)

### 15:05 Validate (45 min)
- **Goal:** try to prove it fails, then decide.
- **Say:** "Imagine it's 90 days after launch and it failed. Why?" Take the room's reasons first.
- **Good looks like:** a re-walk of the changed prototype, four risks each with evidence for and against, measurable success criteria (for an AI feature, one is an AI quality target measured on the evaluation cases, also a row in the GTM adoption table), the GTM viability check and adoption table completed, and the prototype version to hand off.
- **Facilitator practice, the pre-mortem:** everyone writes their reason before anyone speaks; go round starting with the most optimistic person. The pre-mortem makes "this fails" safe to say by assuming it already did.
- **Facilitator practice, conditions:** a condition needs four things before the room moves on: what is measured, the threshold, who checks it, and by which follow-up. Check it against what the team already agreed in Working Backwards, so the two do not contradict each other.
- **Watch:** it does not record a decision before the review is finished. A decision given early is saved as the team's intent, with what is still open. That is correct.
- **Checkpoint:** "Commit, pivot, or park, and why?" If the riskiest assumption is still open, make the room choose between building now and testing first, and record the conditions.

- **Facilitator practice, what it drafted for you:** before the brief, confirm, change, or label as a proposal everything the assistant wrote on the team's behalf (the reason, interim targets, kill criteria, owners). The brief carries it to engineering as if the team had decided it.

### 15:50 Handoff (30 min)
- **Good looks like:** `handoff/discovery-brief.md` with 15 sections, and `handoff/next-steps.md` with the build route, conditions, owners for the follow-ups, and a **Now, Next, Later** roadmap for the product owner. It never starts AI-DLC.
- **Facilitator practice, the roadmap:** hand it to the product owner by name. It is theirs to keep current at each follow-up.
- **Ask the room:** "Could an engineer who wasn't here start from this brief?"

### 16:20 Readout (40 min)
- Each pod shows the sponsor its decision, the prototype on the Flow view, the success criteria, and the next steps. Agree the next step and its owner before people leave.
- **Facilitator practice, the sponsor's question:** answer "why not do the thing I believed?" with the evidence from Signals, not an opinion, then bring it back to the next step. A readout ends with a name and a date.

## When things go wrong

- **The skill is not installed, or behaves like an older version.** `List my skills`, then the module check. If either fails, remove the plugin, import again, and start a new chat. Copying files into the AWS Quick profile by hand is not a fix: AWS Quick keeps its own snapshot.
- **It shows analysis before asking for expectations, or jumps ahead to verdicts.** Say: "Stop. Follow the aidlc-discovery skill one step at a time. Load the module for this phase and start at Step 1." If it still improvises, the skill is not loaded; see above.
- **Someone else takes over facilitation, with a team Space.** In their own AWS Quick, with the Space attached: "Continue the AI-DLC Discovery workshop for [project] from discovery/[project]/PROJECT.md in the [space] space. I'm taking over as [role]. Start at [step]." The previous driver stops writing. If two people wrote at once, the last save wins: compare what each changed and redo the lost change.
- **The chat is lost, or you reinstalled the skill mid-workshop.** Start a new chat with access to the working folder and say: "Continue the AI-DLC Discovery workshop for [project] from discovery/[project]/PROJECT.md. [What is done.] Start at [the next step]." It reads the saved files and picks up from there.
- **A module path does not resolve.** It should retry with the skill's full installed path. If it doesn't, tell it to.
- **The data does not match the product.** It should stop and offer real data, Signal Briefs, or a prepared dataset. Never accept data it writes on the spot: it can only echo what the team just said.
- **The prototype is one plain page.** It did not build from the shell. Say: "Load modules/discovery-prototype/references/prototype-shell.md and copy that HTML exactly, filling only the edit region." Ask it to quote the `EDIT BELOW` line first, to prove it read the file.
- **The compare page shows empty frames in AWS Quick.** AWS Quick shows each file from its own copy, so the compare page cannot load the version files next to it. Open `prototype/compare.html` from the working folder in a browser, where it works.
- **Mobile and Desktop tabs do nothing in the session tab.** The version was built from an old shell. Rebuild it from the current shell, or open the file from the working folder in a browser.
- **The press release reads like a vision document:** headings inside it, more than 700 words, or paragraphs doing two jobs. Say: "Rewrite the press release as exactly seven paragraphs, one job each, 500 to 700 words, and run the writing audit."
- **The team accepts everything.** Ask the person whose belief was contradicted to argue their case. Ask "what would make this fail?" before every checkpoint. An override with a reason is a good outcome.
- **Time runs out.** Protect Validate and Handoff. Use "agree with all" in scoring, skip the optional research, and cap prototype iterations at one. A brief with honest open hypotheses beats a perfect PR/FAQ.

## After the day

- **7 days:** the baseline for the business metric is in, the brief is in the build repository, and the owners in `next-steps.md` have started.
- **By 30 days:** real users have tried the prototype (the personas are synthetic), the open hypotheses have been taken to real customers, and deferred use cases are revisited with new evidence.
- **30 and 60 days:** adoption and the business metric against the success criteria and the kill criteria in the GTM section.
- Feed what the team learns back into Signals for the next cycle.
