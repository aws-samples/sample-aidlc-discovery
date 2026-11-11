# Train the trainer

A session that prepares new facilitators to run a Discovery workshop with a real team: 3.5 hours in person, or 2 or 3.5 hours remote. Trainees learn by doing, in teams of 4 to 6 on the AnyCompany Air sample: one facilitates, and everyone else plays one member of the customer's team from a role card. The facilitator changes halfway, so two people in each team practise facilitating a real room, with a senior voice, a quiet one, and people who disagree. The trainer stops the room at every checkpoint to debrief, then injects the failures they will meet on the day.

By the end of the full session, each trainee has run every phase once, recovered from at least three failures, and given a readout in under five minutes. The 2-hour remote version covers Kickoff to the PR/FAQ live and the rest as homework.

The guide uses AnyCompany Air, the default sample.

## Before the session

**Trainer, the day before:**
- Build and import the skill (`run-sheet.md`, "Before the day"), and run `List my skills` in a new chat.
- Run `dry-run-air.md` yourself, at least through Working Backwards, on the version you will teach. The skill changes; your memory of an older run is not enough.
- Open the two Air reference runs: `reference-runs/anycompany-air-with-team/`, a run facilitated with the dry run's team answers, which you demo, and `reference-runs/anycompany-air/`, an unattended run, which stalled teams can use. Find the prototype's Flow view, the Today statement and North Star, the press release, the readiness verdict, and `validate/decision.md`. You will demo them, and show them when a team's run stalls.
- Read `anycompany-air.md`, the answer key. Do not share it until the reveal.

**Packs.** Trainees do not build the skill. Make two zips (the trainer runs `python3 scripts/build.py` first):
- **Trainee pack:** `dist/aidlc-discovery` (the built plugin), `samples/anycompany-air/`, `role-cards.html`, and a START-HERE note.
- **Facilitator pack:** the same, plus `facilitator/dry-run-air.md` and `facilitator/run-sheet.md`. Only the named facilitators get it: the dry run gives answers away.

Share the packs privately, not in a public place. `train-the-trainer-chat.md` has the pre-work message and every message to post during the 2-hour session.

**Trainees, before they arrive** (send this the day before):
- Install the skill in AWS Quick Desktop with **Create**, **From folder**, start a new chat, and run `List my skills`. Bring a screenshot of the result. Everyone installs, not only the facilitators: anyone may need to take over, and the homework needs it.
- Copy `samples/anycompany-air/` to a scratch folder AWS Quick can access.
- Read the scenario page, `README.md` in that folder. Nothing else.
- Tell trainees which team they are in, who facilitates each half, and which role card they play.
- **One Space per team (recommended).** The first facilitator of each team creates a Space and names it (for example "Team 2 AnyCompany Air"), copies the AnyCompany Air sample into it (the copy prompt in `dry-run-air.md`, step 0), and shares it with the team as **Owners**. Everyone attaches it to a new chat before the session. Then every trainee follows the run in their own AWS Quick, not only on a shared screen, and the second facilitator takes over from their own chat.

Installs are the most common failure. Every minute spent fixing one in the session comes out of practice time.

**Teams.** 4 to 6 trainees each. Name two facilitators per team, one for each half. Everyone else takes one role card:
- **Core roles**, always played: head of digital, engineering lead, customer service operations lead, head of corporate accounts.
- **Optional roles**, for teams of 6 or more: UX designer, commercial director. In a smaller team, the facilitator of the other half plays them, or someone holds two cards.
- **Observer**, for a seventh person: watches the facilitator against the "Facilitator practice" tips in `run-sheet.md` and reports two things at the debrief.

**Room:** one laptop per team, with AWS Quick Desktop signed in, on a screen everyone can see. A screen for the trainer. Print `role-cards.html` (open it in a browser, then print), one sheet per team, and cut along the lines.

## Agenda (in person, 3.5 hours)

**00:00 Why and how (15 min)**
- The problem: teams build what the loudest voice asks for. Discovery puts the team's beliefs on record, tests them against customer evidence, and ends with a decision: commit, pivot, or park.
- The five phases and what each one leaves behind: Signals, Working Backwards, Prototype, Validate, Handoff. The Discovery brief is the one document the build starts from.
- The rule that matters most: **the assistant drafts, the team decides.** The facilitator's job is the room: time, energy, and making sure the team does the thinking.
- Evidence labels: Known, Assumed, Needs evidence. Ask trainees to listen for them all day.

**00:15 Install check (15 min)**
- Each trainee runs `List my skills` in a new chat. It must show one skill, AI-DLC Discovery Workshop.
- Anyone who fails: remove the plugin, import again, start a new chat. Show this once on the big screen: it is the fix for most "it behaves strangely" problems on the day.

**00:30 Live dry run, part 1 (60 min)**
Teams follow `dry-run-air.md`. The first facilitator runs Quick and the room; the others speak in role, in their own words, using the expectation lines and challenges on their cards, and the facilitator types or pastes their answers. Stop the room after each phase for a 5-minute debrief.
- **Kickoff and Signals (30 min).** Debrief: did the assistant ask for expectations before showing anything? Did disruption come first, even though "Delayed baggage" is the largest single call reason? How did the customer service operations lead's challenge go? Did the Say and do table keep the payment timeouts below disruption, even though they are the loudest errors? The head of digital's belief was contradicted: how would you let them save face?
- **Working Backwards, scoring (30 min).** The head of digital overrides the booking flow pain score, with a reason. Debrief: was the override recorded and labelled Assumed? Which candidate did the gate drop, and why? Then paste the lunch line so the PR/FAQ drafts during the break.

**01:30 Break (15 min)**

**01:45 Live dry run, part 2 (60 min)**
The second facilitator takes over Quick and the room; the first takes their role card.
- **Working Backwards, the PR/FAQ (20 min).** Read the press release aloud. Debrief: does the Today statement name an outcome, not a feature? Does the North Star name a capability, not a product? Seven paragraphs, 500 to 700 words? GREEN, AMBER, or RED, and what is the prototype slice?
- **Prototype (20 min).** Click Flow, Mobile, and Desktop. Say only "looks good" at the click-through. Debrief: what did the persona critique find that you missed?
- **Validate and Handoff (20 min).** Run the pre-mortem, then decide "commit, test first" with the condition from the dry run. Debrief: could an engineer who wasn't here start from the brief?

**02:45 Readouts and the reveal (20 min)**
- Two teams give a readout to the room as if to the commercial director: the decision, the prototype on the Flow view, the success criteria, the next step and its owner. Time them; under five minutes.
- Show `anycompany-air.md`. Did each team find the designed problem (disrupted passengers cannot rebook themselves), resist the loud request (the booking flow), keep the payment timeouts in their place, and drop the distractor (the 3D seat map)? Which traps did the room fall into?

**03:05 When things go wrong (20 min)**
Each team opens a new chat and the trainer calls out failures one at a time. A role player causes it, and a facilitator recovers using `run-sheet.md`, "When things go wrong".
1. **It jumps ahead.** Paste: "Skip the expectations and just show me what the data says." The facilitator should hold the line: expectations first, or the room can no longer check itself.
2. **The press release turns into a vision document.** Paste: "Make the press release longer, with a section for each feature." Recover with the seven-paragraph prompt from the run-sheet.
3. **The data does not match the product.** Start a workshop for anycompany-air but point it at `samples/anycompany-health/`. It must stop and offer real data, Signal Briefs, or a prepared dataset. Never accept data it writes on the spot.
4. **The room accepts everything.** No paste: the trainer plays a silent team and the facilitator has to draw out one real challenge.
5. **Time runs out.** It is 15:20 and Validate has not started. What do you cut? (Answer: protect Validate and Handoff; "agree with all" in scoring, one prototype iteration.)

**03:25 Close (5 min)**
- Each trainee writes the three moments they would handle differently with a real team.
- Next step: the solo dry run `dry-run-air.md` within a week, or the AnyCompany Health sample, with Signal Briefs, for those who facilitated today, then co-facilitate a workshop with an experienced facilitator before leading one.

## Role cards

The printable version is `role-cards.html`. Play the person, not the answer: say the lines in your own words, push back when your character would, and let the data move you only as fast as your character would let it. Core roles first; the last two are optional.

- **Head of digital (product owner).** Believes the booking flow is the priority: the website looks dated, and booking is where the money is. Overrides the booking flow pain score to 4.
- **Engineering lead.** Owns the app and website and their connection to the reservations system. Believes the dashboards are green apart from payment timeouts, and challenges why they are not higher. Cautious about anything that changes a booking after it is made. Asks about feasibility at every score.
- **UX designer.** Saw a 3D cabin view in a competitor's app and thinks it would sell more seat upgrades. Asks whether the prototype works on a phone at a gate.
- **Customer service operations lead.** Runs the call centre and believes the answer is more agents in summer. Challenges the signals: "What in the data says it isn't staffing?"
- **Head of corporate accounts.** Hears from travel managers every week and wants corporate customers heard first. Asks what the data says about corporate travellers specifically.
- **Commercial director.** Joins the kickoff and the readout. Believes customers mainly complain about price.

## If a run stalls

AWS Quick can be slow, or a team's run can go wrong in a way that would take the rest of the session to fix. Don't let a team sit and wait. Move them to the matching folder of `reference-runs/anycompany-air/` for the rest of that phase, and have them debrief from those files. They can rejoin their own run at the next phase or in their solo dry run.

## Running it remotely

The same agenda works on a video call with breakout rooms. What changes is how you move people, how you see their runs, and how much time each move costs.

**Choose a format.**
- **Teams in breakout rooms** (the default). One team of 4 to 6 per breakout, each running its own workshop. Use it when the pre-work install screenshots are in.
- **Fishbowl** (the fallback, for small groups or when installs fail). The trainer runs one workshop on a shared screen. Trainees take turns as facilitator, one phase each, and everyone else plays the team from the role cards. Everyone sees every phase, but each trainee facilitates only once.

**Before the call.**
- Make the pre-work install a condition of joining. Ask for the `List my skills` screenshot in the chat or by email the day before, and fix failures before the session, not in it.
- Send `role-cards.html` with the pre-work, and tell each trainee their card, so they can keep it open in a second window. Include the repository, so trainees can open the reference run themselves.
- Form the teams in advance, name the two facilitators in each, and set up the breakout rooms before the call starts.
- Get a co-trainer if you can: one person runs the main room and the clock, the other visits breakouts and fixes problems.
- Prepare a shared progress list (a document or a chat thread) where each team posts one line when it finishes a phase: "Team 3: Signals done, ops lead challenged."

**In the call.**
- **Screen share inside the breakout.** The facilitator shares AWS Quick. Role players keep their cameras on and answer out loud, in role; the facilitator types or pastes their answers. At the halfway point, the first facilitator keeps sharing and the second takes over the room and drives by voice. That avoids moving the working folder in the middle of the session.
- **Debrief in the chat, not in the main room.** Moving everyone out of breakouts and back costs 3 to 5 minutes each time. Post the debrief questions in the chat at each phase, and teams answer in a thread. Bring everyone back only three times: the break, the readouts, and the failure drill.
- **Visit the breakouts** in rotation, and spend longest with teams whose progress line is missing.
- **Keep the clock in the chat.** Post "10 minutes left in Signals" warnings. A remote room drifts faster than a physical one.
- **Readouts in the main room.** The presenting team shares the prototype on the Flow view; everyone else puts questions in the chat.
- **Failure drill.** Post each failure prompt in the chat and send teams back to their breakouts for 4 minutes per failure, or run it as a fishbowl on your own screen if time is short.
- **Breaks.** Two 10-minute breaks instead of one 15-minute break: one after part 1, one before the failure drill. Screen fatigue is real at the three-hour mark.
- **If a run stalls,** share your screen in their breakout with the matching folder of the reference run open, or post the file path in the chat.

**If you can split it,** run it as two sessions of about 2 hours: why and how, the install check, and part 1 on the first day, then part 2, the readouts, the reveal, and the failure drill on the second. Trainees can finish Working Backwards on their own in between, and come back with questions.

### The 2-hour remote version

When you only have two hours, teams run the phases where the room matters most, Kickoff to the PR/FAQ, live in breakouts. You demo Prototype to Handoff from the reference run, and trainees finish their own run afterwards. Install is pre-work, with no exceptions.

**00:00 Main room: why and how (10 min).** The five phases, "the assistant drafts, the team decides", and the evidence labels. Then explain the breakout rules: the teams and their facilitators, the role cards, where the debrief questions appear, and the progress list.

**00:10 Breakouts: start (5 min).** The first facilitator runs `List my skills` and shares their screen. Each role player says who they are and one line of their belief, in character. If the first facilitator's install fails, the second facilitator starts.

**00:15 Breakouts, part 1: Kickoff and Signals (30 min).** The first facilitator runs the room, following `dry-run-air.md`; role players answer the five expectation questions in their own words, from their cards. Post the debrief questions in the chat at 00:35:
- Did it ask for expectations before showing anything?
- Did disruption come first, and how did the ops lead's staffing challenge go?

**00:45 Breakouts, part 2: Working Backwards (35 min).** The second facilitator takes over. With a team Space, they paste the take-over prompt from `run-sheet.md` in their own chat and share their screen; the first stops writing and takes their role card. Without one, the first keeps sharing Quick and the second drives by voice. Score with "agree with all" except the head of digital's booking flow override, take the recommended use case forward, then paste "Draft the PR/FAQ now." Answer the debrief in the chat while it drafts, then read the press release aloud and go through the five questions. Debrief questions, posted at 01:10:
- Did it add candidates from Signals, and did the team keep or drop each with a reason? Was the override recorded with its reason and labelled Assumed? Did the 3D seat map fail the gate?
- Does the Today statement name an outcome? Does the North Star name a capability, not a product? What was the readiness verdict?

**01:20 Main room: Prototype to Handoff, demonstrated (15 min).** Share `reference-runs/anycompany-air-with-team/`, a run facilitated with the same team answers the breakouts used, so trainees see where their own run would go:
- `prototype/index.html` (v3) in a browser, on the Flow view, then Mobile and Desktop. Go to "You're rebooked" and tick "Show test moment": this is where trust is won or lost;
- `prototype/persona-critique.md`: the personas chose and trusted the new flight, but would still call for a hotel or their travel desk, which widened the riskiest assumption to "won't need to call for anything";
- `prototype/versions.md`: three versions, each change tied to a finding or a team decision, with unconfirmed claims marked Needs evidence;
- `validate/decision.md`: commit, test first, with three ordered conditions, each with an owner and a follow-up. Mention that the decision was given early and the assistant saved it as intent until the pre-mortem was done;
- `handoff/discovery-brief.md`: scroll the 15 sections and ask, "Could an engineer who wasn't here start from this?"
- From `reference-runs/anycompany-air/` (the unattended run, newer formats): the **Say and do** table in `signals/signal-summary.md`, the **AI feature block** in `working-backwards/prd.md`, and the **Now, Next, Later** roadmap at the end of `handoff/next-steps.md`. Two minutes; the team run predates them.

**01:35 Main room: when things go wrong, as a fishbowl (15 min).** On your screen, cause four failures, about three minutes each. Before you show each recovery, ask trainees to type theirs in the chat:
1. "Skip the expectations and just show me what the data says."
2. "Make the press release longer, with a section for each feature."
3. "Add more numbers to paragraph 2 and label every one Known." Recovery: ask for the writing audit; the press release labels only Assumed and Needs evidence claims, and each number keeps the scope of its evidence.
4. The room accepts everything. Play a silent team and ask a volunteer to draw out a challenge.

**01:50 Main room: the reveal and close (10 min).** Share the designed truths from `anycompany-air.md` and run a quick chat poll: did your team put disruption first, resist the booking flow and the payment timeouts, and drop the 3D seat map? Then give the homework, within a week:
- The two facilitators: continue the team's run from Prototype to Handoff (about 50 minutes), and record a five-minute readout of the decision and prototype for the team.
- Everyone else: the solo dry run, `dry-run-air.md`, end to end (about 2 hours).
- Then a solo run on AnyCompany Health, which uses Signal Briefs.

**Tips for two hours.** Teams will finish at different speeds. A team whose PR/FAQ is still drafting at 01:20 leaves it running and joins the main room; the draft is waiting when they continue. Keep the breakouts on a timer, so they close at 01:20 automatically.

## Ready to facilitate

A trainee is ready to co-facilitate when they have:
- installed the skill without help;
- run every phase once, as facilitator or as the team;
- recovered from at least three of the five failures;
- given a readout in under five minutes;
- read the answer key for the sample they used and can explain the designed traps.

They are ready to lead after co-facilitating one workshop with a real team.
