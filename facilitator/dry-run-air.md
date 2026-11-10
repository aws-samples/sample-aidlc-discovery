# Dry run: AnyCompany Air

A rehearsal for a facilitator who has never run a Discovery workshop. You play both parts: the facilitator, out loud, and the team, by pasting their answers. About 2 hours, alone. Air is the default sample.

**Before you start**
- Install the skill (see `run-sheet.md`, "Before the day") and start a new chat.
- Copy `samples/anycompany-air/` to a scratch folder and give AWS Quick access to it. Keep the repository copy clean.
- Read the scenario page, `README.md` in that folder. Do not read `facilitator/anycompany-air.md` yet: it holds the answers.
- After each phase, compare your files with the matching folder in `facilitator/reference-runs/anycompany-air-with-team/`, made with this guide's answers.

**How to play the team.** Six people, each with a belief from the scenario page. Answer as they would, not as you think the answer is. The printable cards are in `role-cards.html`.
- Head of digital (product owner): the booking flow looks dated, and booking is where we make money.
- Engineering lead: cautious about anything that changes a booking after it is made.
- UX designer: a 3D cabin view would make seat upgrades easier to sell.
- Customer service operations lead: the queues need more agents in the summer.
- Head of corporate accounts: listen to corporate customers before leisure ones.
- Commercial director (kickoff and readout only): customers mainly complain about price.

## 0. Set up where the workshop is saved (5 min)

Do this before the kickoff, so the start prompt can name it.

**Recommended: everything in a Space.** The scenario page, the data, and the workshop all live in AWS Quick: any of your chats can open them, you can share the Space with a colleague to rehearse a take-over, and it is all still there after the run. The sample data is fictional, so it can go in a Space; with a real team's data, see "Where the workshop is saved" in `run-sheet.md`.
1. In AWS Quick Desktop, open **Spaces**, then **Create space**, and name it yourself, for example `AnyCompany Air Discovery`.
2. Copy the sample into it. In a chat, attach the Space (the **+** menu, then **Spaces**) and your scratch folder (the **+** menu, then **Local folders**), and paste:
   ```
   Copy README.md and everything in discovery/data/, including the telemetry/ folder, from my dry-run-air folder to the AnyCompany Air Discovery space, keeping the same paths (README.md at the top, the data under discovery/data/). Then list the files in the space with their full paths and sizes.
   ```
   Check that it lists 15 files, about 300 KB in total: README.md, 10 files in discovery/data/, and 4 in discovery/data/telemetry/. Approve the saves when AWS Quick asks.
3. Wait a minute for the Space to index the files, then start a **new chat** and attach **only the Space**.

**Or only the folder.** Skip the Space; the data and the workshop stay in the scratch folder.

## 1. Kickoff (10 min)

**Say out loud:** "Today we decide what to build next for AnyCompany Air. The assistant drafts, you decide, and it stops after every phase."

**Paste, with everything in a Space** (use your Space's name):
```
Start an AI-DLC Discovery workshop. Project: anycompany-air. Engagement reference: Self-serve. Save the workshop in the AnyCompany Air Discovery space. Data: production, in discovery/data/ in the AnyCompany Air Discovery space.
```
When it says the data is in the Space, answer: "It's fictional sample data, keep it in the Space."

**Or, with only the folder:**
```
Start an AI-DLC Discovery workshop. Project: anycompany-air. Engagement reference: Self-serve. Data: production, in discovery/data/ in my anycompany-air folder.
```
Use the name of your scratch folder if it differs. If a Space is attached and you used the folder-only prompt, it asks once where to save.

**Answer as the team:** the product (the website and app), the six roles (one team, no pods; the commercial director joins the kickoff and readout), the business metric (self-service rebooking rate for disrupted passengers, 12%), and the five candidate use cases from the scenario page.

**Watch for:** a draft of the setup filled in from the scenario page, for you to confirm or correct in one step, a `PROJECT.md` file, and a note that sample data makes this a demonstration. With a Space: it confirms the Space's name, reads the scenario page from the Space, says AWS Quick may ask you to approve each save (approve them), and `PROJECT.md` lands in the Space with a **Storage** line and a **Driver** line. In Signals, the data inventory should still show 400 text records from six sources: that is how you know it read every record in the Space.

**Answer:** when it asks whether the scope is right and how the room works, choose **Confirmed: one group** (or type it).

**What `PROJECT.md` is.** The workshop's scope and status, in `discovery/anycompany-air/PROJECT.md`, in the Space or the scratch folder. It holds:
- **Scope:** the project, engagement reference, product, users, people in the room, pods, the business metric and its baseline, and the data input and location, each marked Confirmed once the room agrees.
- **Candidate use cases** the team brought, with their owners.
- **Phase status:** the same progress board the assistant shows at each step, with the key artifact of each phase.
- **With a Space, Storage and Driver:** which Space, and who is writing now. Before every save it checks the driver, so two people never overwrite each other.

The phase status moves with the progress board during the day. The team's decisions live in each phase's own files: hypotheses in `signals/`, scores and overrides in `working-backwards/use-case-scoring.md`, the decision in `validate/decision.md`. Show `PROJECT.md` to the room once, after setup, so they see what they agreed.

**Then:** it shows the progress board, with Signals in progress, and starts Signals.

**Facilitator practice:** don't confirm the setup on your own. Read the draft aloud and ask the product owner, "Is anything here wrong or missing?" The business metric matters most, because every score is judged against it. The commercial director leaves after the kickoff, so ask them now whether this is the metric they care about.

**Reflect:** did the setup take longer than you expected? On the day, collect these answers before the workshop.

## 2. Signals (25 min)

**Say out loud:** "Before we see anything, each of you tells me what you expect the data to show."

**It asks five questions, one at a time.** Answer each one as the room: several voices on the same question is normal. Paste one block per question.

Question 1, the biggest problem customers have with the website and app:
```
Head of digital: the booking flow. Our website looks dated next to the competition, and booking is where we make money.
Commercial director: price. Customers complain about fares.
UX designer: choosing a seat. People can't see what they're paying for, so upgrades don't sell. A 3D seat map would help.
```

Question 2, who has it most:
```
Head of digital: leisure travellers booking on the website.
Head of corporate accounts: corporate travellers. They're a third of revenue and their travel managers complain to me every week.
```

Question 3, why you think so:
```
Head of digital: reviews mention the booking flow, and the competition's sites look better.
Customer service operations lead: every summer the call queues explode. We need more agents from June to September.
Head of corporate accounts: travel managers tell me in every account review.
```

Question 4, what else the feedback will show:
```
Engineering lead: nothing big. The app's ratings for booking and check-in are good, and our dashboards are green apart from payment timeouts in August. I'd be careful with anything that changes bookings after they're made.
Customer service operations lead: lost and delayed bags. That's the biggest call reason.
```

Question 5, what would surprise you:
```
Head of digital: if booking turned out not to matter.
Engineering lead: if customers wanted to change their own bookings in the app.
```

These are written so that the data can contradict some of them: that is the point. Don't steer towards the answer.

**Facilitator practice:** read each question aloud and wait before anyone answers. In a real room, the most senior person tends to answer first and everyone else then agrees with them. Ask the quietest person first.

**Watch for:** no analysis before your hypotheses are saved in `signals/team-hypotheses.md`, each written as "We expect ... because ...", with a "What would surprise us" list. It says it will not change that file again.

**Then the data inventory, before any analysis:** 400 text records from six sources plus four data tables, 1 May to 15 October, no personal data (customers appear only as codes, kept out of the quotes), and the gaps it can see, for example no feedback from passengers who rebooked at an airport desk.

**Facilitator practice:** before the room confirms the inventory, ask the person closest to each gap whether that data exists. A gap named now is an open question in the brief; a gap found at the readout is a credibility problem.

**Paste:**
```
Customer service operations lead: we don't collect feedback at the airport desks, so that gap is real. Note it.
Confirmed, the inventory matches what we brought. Go ahead with the analysis.
```

**If the room challenges early.** Someone may push their view before the full report, as the operations lead might here:
```
Customer service operations lead: I still think this is a staffing problem. If we had enough agents in summer, the queues would go away. What in the data says otherwise?
```
It answers that one question from the data, says the full analysis has not run, and offers to run it. A good answer concedes what is true (the summer peak and the long holds are real), shows what the data says instead (calls follow the number of disrupted passengers, at about 420 per 1,000 every month), labels its claims (that more agents would not reduce calls is Assumed, not Known), and names what the data cannot answer (staffing levels and wait times). Then run the full analysis, so every hypothesis is checked, not only the loudest one.

**Paste:**
```
Yes, run the full analysis.
```

**Facilitator practice:** when the data contradicts someone, start with what they got right. Read the "where you're right" part aloud to them first, then the part that disagrees. People accept being partly wrong more easily when they hear first that they were partly right.

**Watch for, in the report** (`signals/signal-summary.md`):
- **Disruption first**, scored for frequency, severity, and reach (about 28 of 30), across all six sources and all three segments. "Delayed baggage" is the largest single call reason; disruption only shows once the six disruption reasons are added up.
- **Bag tracking second, the booking flow third**: friction, not broken, with web conversion above the industry benchmark.
- **Price and the 3D seat map low**: price mostly mild, from leisure travellers; the seat map requested almost only by happy customers.
- **A "What the team expected" table** with a verdict on every hypothesis. Look for the engineering lead's surprise: customers changing their own bookings in the app turns out to be the clearest request in the data.
- **Five customer quotes in full**, the data's limits, and evidence labels throughout.
- **Counts close to, not exactly, the designed ones.** It groups records by keyword and checks by hand, and says the counts are approximate. That is fine.
- **The telemetry, read next to the feedback.** The inventory lists the four telemetry files, the two journeys in the journey map, and that real user monitoring (RUM) is included. The report has a **Say and do** table: disruption in both (about 60% of opened alerts reach the other flights, and about 68% of those tap Contact us, with no server errors); booking friction mostly in feedback while the booking journey is healthy; the August payment timeouts in telemetry with almost no complaints; and late alerts (about 9 minutes typical, 41 minutes at the slow end in summer) in telemetry only.
- **The error dashboard not taken as the priority list.** Payment timeouts are the loudest errors and must not outrank disruption: the top problem has no errors at all.

**Watch for what the checkpoint leaves out.** "Positive / no issue" is the second-largest theme (about 58 records, average rating 4.3). It is in the saved report, but the checkpoint summary may skip it. This counter-evidence matters: the airline is not broadly disliked, and the problem is specific.

**Facilitator practice:** when an engineer points at the dashboard, ask "How many customers did it stop?" An error count is not a customer cost. Then show the journey: the biggest problem returns success.

**Facilitator practice:** before the room challenges, ask "Where does it work well?" and point to the positive theme. A team that hears only problems gets defensive. A team that hears "you're good at this, and failing at this one moment" gets focused.

**At the checkpoint, challenge it as the room.** Get the challenges from the people whose beliefs were contradicted:
```
Head of digital: this data only covers people who already booked with us. People who gave up on our booking flow and booked with a competitor never appear in it. How do we know booking isn't losing us customers we can't see?
Head of corporate accounts: corporate travellers are heard second-hand, through account managers and agencies. Their own voice is under-represented.
Customer service operations lead: the quote about the parents in Nice worries me. Some passengers won't use an app at all. Self-service won't help them.
Engineering lead: our biggest incident this summer was the payment timeouts. Why isn't that higher?
```

**A good answer:**
- To the head of digital: agrees the blind spot is real (people who never booked are not in the data), uses conversion above the benchmark as partial evidence, and records the gap without changing the ranking.
- To the head of corporate accounts: records the second-hand voice as a data gap.
- To the operations lead: keeps the phone and the desk for passengers who will not use an app. Expect this to come back as a risk in Validate.
- To the engineering lead: agrees the timeouts are real, then sizes them: payment-to-confirmation barely moved and August conversion was the highest of the period, so they are real and small. The disruption journey fails with no errors, which is why no dashboard shows it.

**Then, the phase closes.** A good close:
- adds a "Team challenges" section to `signal-summary.md` and new hypotheses to `hypotheses.md` for each gap the room found (here: where shoppers drop out of booking, and a path for people who will not use the app);
- corrects its own report where a challenge is right. Here it may find that corporate travellers do speak for themselves in the data (reviews, calls, surveys), and that only the travel managers who decide renewals are heard second-hand;
- carries constraints forward: any self-service idea needs a path for people who will not use it, and a way to rebook for someone else;
- shows the progress board, the saved files, and three short lists: what we know, what we don't know, and what we're assuming;
- says what comes next: personas, then scoring.

**Facilitator practice:** credit the challengers by name. "Your challenge changed the report" is the strongest signal a room can get that challenging is wanted. Then close the phase out loud: ask the product owner, "Are we agreed this is the problem we work on?", and wait for a yes before moving on.

**Paste:**
```
Head of digital: agreed, disruption is the problem we work on. Thanks for the challenges, they made the report better. Go ahead with the personas.
```

**Reflect:** whose belief did the data contradict? The head of digital owns the product. How would you let them save face in a real room?

## 3. Working Backwards (45 min)

**Say out loud:** "Now we score your five candidates. You can override any score, as long as you say why."

**Do, in order:**
1. Let it draft the personas: three or more from the data, including one customer who is satisfied today. It may add one for a gap the room raised in Signals, here a passenger who will not use the app. It shows a one-line summary of each (name, tagline, confidence) and asks whether you recognize them.

   **Facilitator practice:** ask the people closest to customers first, the operations lead and the head of corporate accounts: "Have you met this person?" A persona nobody recognizes gets changed or dropped, and the reason recorded. The satisfied customer is there to show what the team could break.

   **Watch for:** one file per persona in `working-backwards/personas/`, quotes copied word for word from the data, and a confidence rating that matches the evidence. Expect four or five: a frequent business traveller, a leisure family cancelled at night, a corporate travel manager (Medium, because heard second-hand), a satisfied regular, and a passenger who won't use the app (Low, because the evidence is thin). It says the personas are hypotheses to test with real customers, not evidence. For corporate travel, the buyer and the end user are different people: the travel manager is the **buyer** (judges value, cost, and duty of care) and the traveller is the **end user** (judges whether rebooking works). It should give each one a persona and say which is which; for leisure travel it should say they are the same person.

   **Facilitator practice:** every persona costs time later, because each one walks through the prototype in the critique. Ask the room whether any two overlap. A persona the room sets aside goes to `working-backwards/set-aside-personas.md`, not deleted.

   **Paste:**
   ```
   Head of corporate accounts: Karim is right. Travel managers want to see where their travellers are during a disruption and rebook several at once. Keep him.
   Customer service operations lead: Helena matches what we see at the desks, mostly older passengers whose family calls for them. Keep her, even at low confidence.
   Head of digital: we recognise all five. Keep them and go on to scoring.
   ```
2. **Candidates from Signals.** Before the gate, it adds two or three candidates from themes the team's five do not cover, each marked "From Signals" with its evidence: expect late disruption alerts (from the telemetry) and fares (from the feedback). Kept ones are scored like the rest; dropped ones are recorded and not scored. This takes about a minute.

   **Facilitator practice:** keep or drop each in one sentence, with a reason. The point is to catch a problem the team did not bring, not to reopen the whole list.

   **Paste:**
   ```
   Head of digital: keep late disruption alerts, the alerts are ours to fix. Drop fares: pricing is the commercial team's decision, not ours.
   ```

3. **Scoring starts before any score.** It rewrites the candidates as problems, each with its owner and the metric it moves, merges the smaller disruption problems into self-service rebooking (bulk rebooking, rebooking for someone else, families split up, no help out of hours), and treats "booking flow redesign" as the problem behind it. It drafts the gate: the 3D seat map drops, because the people asking for it are already happy, and the UX designer's question stays open as a hypothesis with a cheap test. Then it asks you to fix the weights before it scores anything.

   **Facilitator practice:** settle the weights with the sponsor before the first score, and say why out loud: "Once we see scores, nobody can move a weight to help their favourite." If the sponsor wants a shift, for example more weight on strategic fit, agree it now, within 10 points.

   **Paste:**
   ```
   Head of digital: keep the default weights. Go ahead and draft the scores.
   ```

   **Watch for, in the drafts:** self-service rebooking far ahead (about 4.6, High, Build first) and the other three between about 2.5 and 2.7, all Defer. They score 1 on business outcome because none moves the self-service rebooking rate agreed at setup, however real their pain. Each score has its evidence and label; strategic fit and feasibility are marked for the team to confirm, and it asks the engineering lead about feasibility.

   **Watch for:** with the telemetry, feasibility for self-service rebooking cites the reissue service's error rate (about 5%, mostly `FARE_RULE_MISMATCH`) as evidence, and reach and the outcome baseline cite the RUM journey.

   **Facilitator practice:** feasibility belongs to the engineering lead, not to the assistant. Don't let a drafted 3 stand by silence: ask "What would make this a 2, and what would make it a 4?" The answer is the build's biggest unknown, and it belongs in the brief.

   **Paste:**
   ```
   Engineering lead: 3 is right, not lower. Showing alternatives is easy, we already do it. Reissuing the ticket and applying fare rules is the hard part: the reissue service fails about 5% of the time, mostly fare rule mismatches, and that's where today's errors come from. I want a spike on reissue before we commit to a date.
   ```

   Then go through the other candidates, one at a time. For loyalty points and bag tracking, choose "Agree with all six scores", and answer its feasibility question for bag tracking:
   ```
   Engineering lead: agree with all. Feasibility 3 is right: tracing status exists internally but there's no customer-facing way to show it yet. It's my candidate, and I'm fine with deferring it behind rebooking.
   ```

   **Facilitator practice:** when a candidate's owner is in the room, give them the floor before the room agrees: "It's your candidate. Anything the scores miss?" An owner who agrees to defer their own idea out loud is a stronger result than a silent defer.

   For the booking flow, override as the head of digital:
   ```
   Head of digital: raise customer pain for the booking flow redesign to 4. Our reviews mention it all the time.
   ```

   **Watch for:** the override recorded with your reason, the label Assumed, and the new weighted score. Raising pain from 2 to 4 adds 0.5 (to about 3.0), so the decision stays Defer. Say that out loud: an override that does not change the decision lets the person be heard without changing the day.

   It may also check the override against the data without undoing it: for example, booking reviews are frequent (10 of 80) but mild (average 3.1, several "fine" or "works"), so it keeps the team's 4, labels the severity Assumed with the head of digital's reason, and points to the hypotheses that would settle it.

   **Facilitator practice:** when the assistant questions an override, give the person who made it the last word. The team owns the score; the assistant's job is to make the evidence visible, not to win. Ask: "Does that change your view, or do we keep the 4?"

   **Paste**, to confirm the rest and choose:
   ```
   Head of digital: keep the 4. Agree with the other five scores.
   We take forward self-service rebooking for disrupted passengers, as the team.
   ```
4. Once the use case is taken forward, paste:
   ```
   We're breaking for lunch. Draft the PR/FAQ while we're away.
   ```
5. **The straw-man.** While you are "at lunch", it drafts the five Working Backwards answers, a short list of feature ideas, and the PR/FAQ, every file marked straw-man. It does not run the readiness check yet: that comes after the team's review. It lists the placeholders the team must replace: the targets it proposed (for example 12% to 35%, and 42 to 25 rebooking calls per 100 disrupted passengers), the launch date, the leader's name, and a working product name.

   **Watch for:** the Today statement with no solution in it; a North Star that names a capability, not the working product name; a press release of a headline, a subheading, and seven paragraphs in 500 to 700 words, with a label only where a claim is Assumed or Needs evidence; the same targets in the North Star, the PR/FAQ, and the feature description; and a one-line writing-check result, for example a claim removed because the data does not support it.

6. **"After lunch", the team takes it over.** Go through the five answers one at a time, then the feature mix and the targets, then read the press release aloud.

   **Facilitator practice:** the targets are the team's commitment, not the assistant's guess. Ask the product owner and the person who will feel it most (here, the operations lead) to say the numbers out loud: "Can we sign up to 35%?" A target nobody said out loud is a target nobody owns.

   **Facilitator practice:** read the press release aloud, slowly, in the room. Stop at any sentence where someone winces, and ask "How would we say it?" Rewriting one sentence together is what makes it the team's document.

   **Paste:**
   ```
   Head of digital: the five answers are ours, keep them. Keep the features you proposed, including the assistant that recommends the best new flight, with the travel desk view and out-of-hours hotel help as P1.
   Head of digital: we sign up to 35% self-service rebooking and 25 calls per 100 disrupted passengers within 90 days of launch. Keep June 2027 as the target date until the reissue spike reports. The leader quote is from me, Head of Digital. Keep "Choose My Flight" as the working name.
   Customer service operations lead: in paragraph 2, say "wait on hold for up to three hours", that's what our agents hear.
   Now run the readiness check.
   ```

7. **The readiness check.** It applies the team's changes, re-runs the writing check, then drafts an answer to each of the seven questions and gives a verdict. Expect AMBER with about three gaps, for example: no target time from the alert to a boarding pass, no screen for "none of these works for me", and the riskiest assumption not named yet. The Prototype scope section names the slice, here three paths through one flow: a business traveller picking a new flight at the gate, a family swapping the airline's automatic rebooking for one where they sit together, and a relative rebooking from home.

   **Facilitator practice:** AMBER is a good result; don't chase GREEN. Close any gap the room can answer in two minutes, and carry the rest as open questions with an owner. A gap marked must-have that only a test can close is exactly what the prototype is for.

   **Paste:**
   ```
   Customer service operations lead: gap 1, from what callers tell us, people give up and call after about five minutes. Target: a boarding pass in under three minutes from opening the message.
   Head of digital: gap 3, when nothing works, offer a call-back with the booking already loaded, and the refund route. Keep it nice-to-have for the prototype.
   Gap 2 we name after the PRD. Go on to the PRD.
   ```

8. **The PRD.** It carries the closed gaps into the PR/FAQ and `working-backwards.md`, labels a basis it cannot check (callers give up after about five minutes) Assumed, and drafts the PRD: a small P0 on one flow, P1 and P2 lists, guardrails (the phone and desks stay; booking and check-in must not get slower, for the satisfied persona), and, because the assistant recommends flights, the AI feature checklist and the **AI feature block** (about 10 minutes). It lists the claims it assumed for the team to check, for example that disrupted passengers pay no change fee, and that a booking reference is enough for someone else to change a booking.

   **Watch for:** a P0 small enough to prototype in an hour; no technology choices; the satisfied persona protected by a guardrail; and its own assumptions handed back to the team instead of hidden.

   **Watch for, in the AI feature block:** a **first-draft prompt** with the job (recommend one flight for what the passenger says matters, and say why in one sentence), the tone, the inputs, the output format, and what it must not do; **5 to 10 evaluation cases** drawn from the quotes and the personas, split into typical (a traveller with a morning meeting, a family who must sit together), edge (a tight connection, only next-day flights), and negative (asks how much compensation they get, asks for a flight with no seats); and **sample outputs** for three or four cases, for the prototype. It says the block is a starting point: the build chooses the model, the data and retrieval design, and the final prompt.

   **Facilitator practice:** ask the person closest to customers to read the negative cases aloud and say what a good answer is. The cases the feature must refuse are where trust is lost, and they come from the room, not from the model.

   **Paste:**
   ```
   Customer service operations lead: add a negative case: a passenger asks whether they can get a refund instead. The assistant must not decide it; it shows the refund route and says who decides.
   Head of digital: the block is ours. Go on.
   ```

9. **The riskiest assumption.** It proposes candidates and asks which one, if wrong, would end the idea. It should separate what the prototype can test from what it cannot (reissue reliability is the engineering spike's job).

   **Facilitator practice:** this is the most anchored decision of the day, so have everyone choose before anyone speaks. In a room, each writes a letter on paper and shows it at once; remote, everyone types it in the chat at the same moment. Then ask the outliers why. Ask: "Which one, if wrong, means we built something nobody uses?"

   **Paste:**
   ```
   Head of digital: no change fee or fare difference among the offered flights is our policy for disruptions, confirmed.
   Engineering lead: booking reference plus surname is what manage-booking uses today. Keep it, but it goes to Validate as a risk for security to review.
   Team: the riskiest assumption is A and B together: disrupted passengers offered real choices quickly will choose a flight themselves and trust it enough not to call. If they still call, we remove no queue. C goes to Validate as a feasibility and security risk.
   ```

   **Watch for:** `working-backwards/riskiest-assumption.md` with what the prototype must show to test it (the moment of decision in every path, and a confirmation screen that makes plain the ticket is issued, there is nothing to pay, and the party is together), and what would support or contradict it, with thresholds drafted for the team to set. The readiness verdict can move to GREEN once the assumption is named. Labels change with the team's answers: the confirmed fee policy becomes Known, the booking-reference question Needs evidence.

   **Facilitator practice:** set the pass mark now, before anyone sees a result. A threshold chosen after the test bends to fit what happened. Ask: "What result would make us stop?"

   **Paste:**
   ```
   Team: set the thresholds. Supports it: at least 6 of 8 recently disrupted passengers choose a flight without help, in under three minutes, and say they would not call to check. Contradicts it: 3 or more of 8 would still call, or wait for the airline to decide. Go on to the GTM draft.
   ```

   It may point out a result neither threshold covers (for example 5 of 8 pass and the other 3 only miss the time) and say how the team reads it in Validate. It also says the persona critique cannot meet or break the thresholds: only real passengers can, so someone must own recruiting them.

10. **The GTM draft.** Expect first adopters with evidence and an estimate labelled Assumed (here, corporate travellers on single bookings, reached through the disruption message, account managers, and agencies), design partners by role, not by name, a one-paragraph positioning, a business model labelled as an assumption, and a launch path where each step must be met before the next. Viability and adoption are left for Validate. The phase ends with what we know, what we don't know, what we're assuming, and what the prototype must prove.

   **Facilitator practice:** before the phase closes, put a name and a date on every open question that blocks the build: who recruits the real passengers, who runs the reissue spike, who asks security. An open question without an owner is still open at the 30-day follow-up.

   **Paste:**
   ```
   Head of digital: the GTM draft is ours. The UX designer and I recruit the 8 recently disrupted passengers by the 30-day follow-up. The engineering lead owns the reissue spike. The head of corporate accounts confirms the design partners and sizes the revenue at risk by the 7-day follow-up.
   We're ready to prototype.
   ``` As the engineering lead, ask what changing a booking involves; feasibility is the team's call, not the assistant's.

**Watch for:** the override recorded with your reason and labelled Assumed. The 3D seat map dropped at the gate. The PR/FAQ marked as a lunch draft. In the five questions, a Today statement whose need is an outcome ("choose and confirm a new flight within minutes"), not a feature, and a North Star that names a capability, not a product name. A press release of exactly seven paragraphs in 500 to 700 words, a writing-audit line, and a readiness verdict with a Prototype scope section.

**Reflect:** where did the room spend the most time? On the day, that is where you need the most time.

## 4. Prototype (20 min)

**Watch for:** a screen plan of 4 to 8 screens with a test moment (the cancellation alert, alternative flights, a one-tap confirmation), named against the journey step it is meant to change (alternatives viewed, where most sessions leave for Contact us), then a file that opens on a Flow board of phone frames with Flow, Mobile, and Desktop tabs. Click each tab.

**Watch for, in v1:**
- One file that opens on the Flow view with every screen side by side, and Mobile and Desktop tabs that switch. With a Space, it saves the file to the Space and opens the Space copy in the session tab; anyone the Space is shared with can open it the same way. Click each tab; if a tab does nothing, see "When things go wrong" in `run-sheet.md`.
- The assistant's recommendation on the options screen, using the sample outputs from the AI feature block word for word and labelled as sample output from the first-draft prompt, including one negative case.
- A test moment marked, with a "Show test moment" toggle that highlights it. Here it is the confirmation screen: ticket issued, nothing charged, and "You don't need to call us".
- Different bookings in different views. A view shows one booking, so it may put one persona's path in Mobile and another's in Desktop, and say which to use.
- Every way it differs from the plan the team confirmed, listed and logged in `versions.md`. For example, a persona without a path of their own, a shortcut on the first screen, or an extra screen for a failure.
- Claims on screen that nobody has confirmed (a bag that moves with you, "this booking is final", a call-back at any hour) marked Needs evidence for Validate, and promises it removed itself.
- A note that it checked the file against the build rules but has not seen it render.

**Facilitator practice:** when the assistant changes what the team agreed, the team decides, out loud, before the click-through. Read each change to the room and ask the owner: "Keep it, or change it back?" A change nobody decided becomes a surprise at the readout.

**Paste:**
```
Head of digital: we accept the three changes. Daniel's family path waits for v2, if the persona critique shows it's needed.
Engineering lead: keep "Bag moves with you" and "This booking is final" marked Needs evidence; they go to the reissue spike.
Customer service operations lead: the call-back "at any hour" is not true today, the line closes at night. Change it to "We'll call you back when the line opens at 07:00".
```

**At your click-through, say only:** "Looks good." Let the persona critique find the problems: that is what it is for.

**Watch for:** the team's changes saved as a new version, v2, never by overwriting v1, with `versions.md` updated and `compare.html` showing v1 and v2 side by side. It may question a change against a persona: here, "when the line opens at 07:00" is wrong for a business traveller cancelled at 19:52 if the line is still open then.

**Facilitator practice:** when the assistant asks a factual question (what time does the line close?), get the answer from the person who knows, or record it as Needs evidence. Never let the room guess: a guessed fact in the prototype becomes a promise in the brief.

**Paste:**
```
Customer service operations lead: the line is open 07:00 to 22:00. Show the call-back time depending on the hour in the next version: "We'll call you back within the hour" while it's open, "when the line opens at 07:00" after 22:00. Go ahead with the persona critique.
```

**Watch for, in the critique:** every persona walks the current version in their own words and gives a day-one adoption score with a reason, and reacts to what the assistant says: would they trust its recommendation, act on it, or want something else. The disrupted personas test the riskiest assumption (would they trust the confirmation screen, or call to check?), the travel manager looks at it for their travellers, and the satisfied regular checks nothing gets in the way of booking and check-in. Then it shows the findings and asks which to fix. Each fix becomes a new version, logged in `versions.md`.

Expect findings that go beyond the screens. Here, the disrupted personas choose and trust the new flight, but would still call for a second reason the confirmation does not answer: a hotel when the new flight is tomorrow, or a travel desk that still shows the old flight. Each finding gets a proposal (fix now, or carry to Validate), and fixes that promise something unconfirmed, like hotel vouchers without an agent, are left to the team.

**Facilitator practice:** don't fix everything. Fix first what touches the riskiest assumption, then what is cheap; send the rest to Validate with an owner. One iteration is enough. If a finding changes what the riskiest assumption means, say so and update it now: here, "won't call to check" becomes "won't need to call for anything".

**Paste:**
```
Head of digital: keep finding 1 in v3, the hotel line on "You're rebooked", marked Needs evidence. The customer service operations lead confirms whether vouchers can be issued without an agent.
Fix 3, 5, 6, 8 and 9 as you propose. 2 and 4 go to Validate; 7 waits.
Update the riskiest assumption: passengers must not need to call for anything else, such as a hotel, not just to check the flight. Build v3.
```

**Reflect:** what did the personas find that the team missed?

## 5. Validate (25 min)

Validate tries to break the idea before anyone builds it. It will not record a decision until the review is finished: if you give it a decision early, it saves it as the team's intent and lists what is still open. That is correct; finish the review.

**1. Re-walk and the four risks.** It re-walks the current version as the personas and drafts a verdict for each risk: valuable, usable, feasible, viable, each with evidence for and against. Expect valuable supported, and usable, feasible, and viable partly open until the real walk-throughs, the reissue spike, and the revenue sizing report. The re-walk may find something new: here, v3 offers an airport hotel to a passenger whose flight was cancelled at her home airport.

**2. The pre-mortem. Say out loud:** "It's 90 days after launch and this failed. Why?"

**Facilitator practice:** have everyone write their reason before anyone speaks, then go round, starting with the most optimistic person in the room. People name the real risks only when it is safe to say "this fails", and the pre-mortem makes it safe by assuming it already did.

**Paste:**
```
Engineering lead: feasible stays open until the reissue spike reports. Hotel vouchers only when the passenger is away from their home airport; note it for the build.
Pre-mortem:
Customer service operations lead: passengers still called, for the hotel or to check, because the confirmation didn't answer everything.
Engineering lead: reissue failed on complex bookings and agents had to fix them by hand.
Head of corporate accounts: travel desks didn't see the change and called us anyway.
Head of digital: the message arrived late, after the good flights were gone.
UX designer: passengers like Helena never used it, and the desk queues stayed the same.
```

**Watch for:** each reason with an early warning sign and a way to prevent it.

**3. The decision and its condition.** Give the decision with a condition, and expect questions back. A good assistant checks the condition against what the team already agreed: does it repeat or replace the 6 of 8 threshold from Working Backwards, does it measure the agreed metric or a different group, and what exactly counts as "without calling"?

**Facilitator practice:** a condition is only useful if someone can check it later. Before the room moves on, it needs four things: what is measured, the threshold, who checks it, and by which follow-up. "Test first" without them is "build anyway" with extra steps.

**Paste:**
```
Commit, but test the riskiest assumption first.
1. Order: the 8 walk-throughs and the reissue spike in the next 30 days, then a one-route pilot, then the full build.
2. The 6 of 8 walk-throughs come first and gate the pilot.
3. Pilot condition: at least 40% of disrupted passengers who see the options accept one without calling. The 35% of all disrupted passengers stays the 90-day target after full launch.
4. "Without calling" means no call about that booking before departure. Route: Hamburg to Milan, for 4 weeks or 500 disrupted passengers, whichever comes first. The head of digital checks it at the 60-day follow-up.
5. AI quality target for the assistant: a reviewer accepts at least 8 of 10 typical cases, and no negative case passes. The head of digital checks it with the walk-throughs.
Hand off v3. Decided by the head of digital, engineering lead, customer service operations lead, head of corporate accounts, and UX designer; confirmed with the commercial director at the readout.
```

**Watch for:** the AI quality target among the success criteria and as a row in the GTM adoption and success table; success criteria with a metric, a baseline, a target, and a check date, using the North Star's numbers, and written as telemetry measures where they exist (the share of disrupted sessions that reach a rebooked confirmation without Contact us; the alert delay at peak); the GTM viability and adoption tables completed, with no part left as draft; the version to hand off; and `validate/decision.md` with the decision, the conditions in order, their owners, and who decided.

**4. Review what it drafted for you.** It records the decision, then lists what it wrote on the team's behalf: the reason, interim targets, kill criteria, an adoption owner, a new PRD requirement. It also checks the plan against itself, for example that 30 days of gates plus a 4-week pilot barely fits a 60-day check, or that the pilot route needs the hotel-voucher rule working first.

**Facilitator practice:** anything the assistant drafted for the team is confirmed, changed, or labelled a proposal before the brief is written. The brief carries it to engineering as if the team had decided it.

**Paste:**
```
Head of digital: the reason, in our words: disruption is the biggest and most painful problem in the data and it is the metric we agreed; the personas chose and trusted v3, but only real passengers can show they won't call, and reissue is unproven.
Move the pilot check to the 90-day follow-up, so a slipped gate does not break it.
Engineering lead: the home-airport voucher rule must work before the pilot. Add it to condition 2.
Keep the interim targets, the kill criteria, and the message-timing requirement as proposals, labelled Assumed, for the head of digital to set at the 30-day follow-up. The head of digital owns adoption.
Write the brief.
```

**Reflect:** was "test first" the right call? What evidence would let the team build now?

## 6. Handoff and readout (10 min)

**Watch for:** `handoff/discovery-brief.md` with 15 sections, the decision as section 2 in the team's words, the AI quality target in section 7 and the AI feature block in section 9, the conditions with who checks them and by when, and links that open. `handoff/next-steps.md` with the AI-DLC command to run in the build repository (AWS Quick does not run AI-DLC; with a Space, it says to download the `discovery/anycompany-air/` and `aidlc/` folders from the Space into that repository, never the data), the conditions, and owners for the 7, 30, 60, and 90-day follow-ups, including the items still labelled Assumed and who sets them. It ends with a **roadmap for the product owner: Now, Next, Later**. Now: self-service rebooking and its conditions. Next: the deferred candidates, each with the evidence that would move it up and who gets it (for example bag tracking, with repeat calls per bag case). Later: the rest, with why, including the 3D seat map and its open hypothesis. Problems and metrics ordered by conditions, no delivery dates.

**Facilitator practice:** hand the roadmap to the product owner by name. It is theirs to keep current at each follow-up, not the facilitator's.

**Say out loud, as if to the commercial director:** the decision, the prototype on the Flow view, the success criteria, and the next step with its owner. Time yourself: under five minutes.

**Facilitator practice:** expect the sponsor's question from the role card: "Why not lower fares instead?" Answer with the evidence, not an opinion: price came up in 7% of feedback, mostly mild; disruption in 30%, with the worst scores and renewals at risk. Then bring it back to the next step and its owner. A readout ends with a name and a date, not with applause.

**Reflect:** could an engineer who wasn't in the room start from the brief?

## Rehearse a take-over (with a Space)

If you saved the workshop in a Space, rehearse what happens when someone else takes over. Share the Space with a colleague as **Owner**; they attach it to a new chat in their own AWS Quick (the **+** menu, then **Spaces**).

**Watch for:** it confirms the Space attached to the chat, writes `PROJECT.md` there with a Storage line and a Driver line, and saves every artifact at the usual `discovery/anycompany-air/` paths in the Space. After Signals, your colleague takes over in their own chat:
```
Continue the AI-DLC Discovery workshop for anycompany-air from discovery/anycompany-air/PROJECT.md in the [space] space. I'm taking over as head of digital. Start at the personas.
```
It should show who was driving, update the driver, and continue. If you then try to write from your chat, it should stop and ask whether you are taking over.

## After the run

1. Compare your files with `facilitator/reference-runs/anycompany-air-with-team/`, a run made with the same team answers as this guide, and `facilitator/reference-runs/anycompany-air/`, an unattended run.
2. Now read `facilitator/anycompany-air.md`. Did your run find the designed problem? Did the 3D seat map fail the gate? Which traps did you or the assistant fall into?
3. Write down the three moments you'd handle differently with a real team.
