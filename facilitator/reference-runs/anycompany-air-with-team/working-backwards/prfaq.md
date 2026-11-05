# PR/FAQ: self-service rebooking for disrupted passengers

> **Reviewed by the team, 2026-10-29.** Drafted during the break, then reviewed: the head of digital confirmed the five Working Backwards answers, features A, B, and C, the targets, the date, the leader quote, and the working name; the customer service operations lead changed paragraph 2. Demonstration run on fictional sample data.
>
> Targets used throughout are the North Star's, signed up to by the head of digital: self-service rebooking rate 12% to 35%, and rebooking calls 42 to 25 per 100 disrupted passengers, within 90 days of launch. Target launch date June 2027, held until the reissue spike reports.

## Customer thinking (from the personas and signals)
1. **What problem does this solve for me?** I can see flights that would get me there, but I have to wait on hold to get onto one. (Ingrid, Daniel) [Known]
2. **Why should I care?** The good flights fill up while I wait. (Ingrid) [Known]
3. **How will it make my life better?** A disruption costs me a few minutes on my phone, not an afternoon. (Ingrid's definition of success) [Known]
4. **What would make me skeptical?** Whether the new ticket is really issued, or whether I will be charged a change fee, as has happened before (13 records). Whether my family stays together. [Known]
5. **What would delight me?** Fixing it at 23:00 without waiting for the phone line to open at 07:00. (Daniel) [Known]

## Press release

**Disrupted AnyCompany Air passengers can now choose their own new flight**

*When a flight is cancelled or delayed by more than two hours, passengers can pick and confirm a new flight in the app or on the website in minutes, or have someone they trust do it for them.*

LISBON, 1 June 2027. AnyCompany Air passengers whose flight is cancelled or delayed by more than two hours can now choose their new flight themselves, in the AnyCompany Air app or on the website, from the moment they hear about the disruption. Choose My Flight shows the flight the airline suggests and the other flights with seats, and confirms the new ticket and boarding pass on the spot. A family member, an assistant, or a travel agency can make the same change for a passenger who does not use the app. Passengers no longer have to phone to change a disrupted flight.

Between May and mid-October 2026, about 350,000 AnyCompany Air passengers had a flight cancelled or delayed by more than two hours. The app and the website showed them alternative flights but gave them no way to pick one, so only 12 in every 100 rebooked themselves and about 42 in every 100 phoned. Callers wait on hold for up to three hours while the flights they could see fill up. Others were moved automatically onto flights days later, or split from their family, and had to call again to undo it. Corporate travel managers report that disruption costs them more than the fare difference.

Choose My Flight turns the disruption message into a decision the passenger makes. The passenger sees what the airline suggests, compares it with the other flights that still have seats, and either accepts it or picks another one, with no change fee for a disrupted flight. The new ticket is issued straight away, and the passenger leaves with a confirmation and a boarding pass. It works at any hour, including late at night when the phone line is closed. Passengers who prefer a person can still call or go to an airport desk, where agents now have more time for them because fewer people need to call. [Assumed]

"Our passengers told us the delay was not the worst part. Having no way to fix it was," says the Head of Digital at AnyCompany Air. "They could already see their options. Now they can act on them, from a departure gate or from a sofa in another country."

Ingrid, a sales director from Hamburg, has her evening flight to Milan cancelled at the gate. Her phone shows the suggested flight at 07:20 the next morning and two others; she taps the 07:20, sees there is nothing extra to pay, confirms, and has a new boarding pass before she leaves the gate. Daniel, on holiday with his partner and two children, gets a cancellation text at 23:00. He replaces the flight the airline picked, two days later, with one the next afternoon where the four of them sit together, and puts the children to bed. Helena, who does not use the app, is stuck in Nice with her husband; her daughter opens the website at home, enters the booking reference, and moves them onto the morning flight, and Helena receives a text with the new flight and gate.

"My flight was cancelled at the gate, and by the time I reached the taxi rank I was booked on the 07:20. I texted my customer that I would see her at nine, and I did," says Ingrid Halvorsen, regional sales director. (Synthetic testimonial, written from a persona, not a real customer.)

Choose My Flight is available to every AnyCompany Air passenger with a disrupted flight, in the AnyCompany Air app and under Manage booking on the website. Partner travel agencies can make the same change for their customers with the booking reference.

## Customer FAQ

**1. Which flights can I change myself?**
Any booking where the flight is cancelled or delayed by more than two hours, the same definition of disruption the airline uses today. [Known] for the definition; covering every fare type and route at launch [Needs evidence] (engineering spike).

**2. Will it cost me anything?**
No. Choosing another flight after a disruption carries no change fee or fare difference among the flights offered. Today 13 records describe errors or change fees charged after a disruption, which is why the engineering lead wants a spike on reissue and fare rules first. [Known] for the policy (confirmed by the head of digital); [Needs evidence] that reissue works reliably.

**3. The airline already moved me to another flight. Can I change it?**
Yes. The airline's choice is shown as a suggestion you can keep or replace. 9 records describe automatic rebookings 6 to 21 days later or with long layovers when a direct flight existed. [Known] for the problem; [Assumed] that a suggestion removes those calls (research hypothesis 4).

**4. We are travelling as a family. Will we stay together?**
The flights offered keep everyone on the same booking together. 11 records describe families and groups split or rebooked one at a time. [Known] for the problem; [Assumed] that enough seats exist together on the alternatives.

**5. I don't use the app. What can I do?**
You can still call or go to an airport desk. Someone you trust, such as a family member, an assistant, or your travel agency, can also make the change with your booking reference and surname, as manage-booking works today. [Needs evidence] that this is safe enough for rebooking (security review in Validate). Several records show people already rebooking for someone else by phone. [Known] for the need; how many passengers will never self-serve [Needs evidence] (research hypothesis 11).

**6. What if none of the flights works for me?**
You can call or go to the desk as today, and the app tells you so. Refunds and compensation stay with the current process. [Assumed]

**7. My company's travel desk books for me. Can they do this?**
At launch, your travel management company or agency can rebook you with your booking reference. A view for travel desks to see and rebook all affected travellers at once comes later. [Assumed] scope; travel managers' needs [Needs evidence] (research hypothesis 3).

## Internal FAQ

**1. Why this, and why now?**
It scored 4.60 of 5, with high confidence: 118 of 400 records (30%) across all six sources, the agreed metric at 12%, about 42 rebooking calls per 100 disrupted passengers, and 62% of agent handle time in the call sample. Four corporate notes tie a renewal, risk, or tender to disruption handling. Every summer the problem doubles with disruption volume. [Known]

**2. Why not hire more agents for the summer?**
Rebooking calls stay at about 42 per 100 disrupted passengers every month, so they follow disruptions, not staffing. More agents may shorten holds but would not change how many passengers need to call. [Known] for the call rate; staffing and wait-time data [Needs evidence] (research hypothesis 8).

**3. What is the hardest part?**
Reissuing the ticket and applying fare rules when a passenger chooses a new flight. Showing alternatives already works. The engineering lead rates feasibility 3 of 5 and wants a spike on reissue before committing to a date. [Known]

**4. How do we measure success?**
The self-service rebooking rate for disrupted passengers rises from 12% to 35%, and rebooking calls fall from 42 to 25 per 100 disrupted passengers, within 90 days of launch. Passengers reach a boarding pass in under three minutes from opening the message (team target; callers give up after about five). Survey scores for passengers who rebook online stay at or above today's +4, and fewer than 2% of self-service rebookings need an agent to fix. The first two targets are the team's commitment (head of digital, 2026-10-29); the survey and fix-up targets are [Assumed] and go to Validate.

**5. What are the biggest risks?**
Reissue errors that create more calls than they remove; passengers who do not trust a flight they chose and call to check; passengers who cannot self-serve being left behind; and the +4 versus −58 survey gap being partly selection, since harder cases may be more likely to call. [Assumed]

**6. What does it take, and when?**
The target is June 2027, held until the reissue spike reports; the spike can move it. The proposed path is a pilot for single-passenger bookings on a set of routes, measured against comparable disrupted passengers, then families and groups, then rebooking for someone else. The travel desk view and out-of-hours hotel help are P1. [Assumed]

**7. What happens to the call centre?**
Agents keep handling the passengers who call, and the cases self-service cannot solve. If self-service takes a share of today's 37-minute disruption calls, those agents have more time for passengers like Helena. [Known] for handle time; [Assumed] for the effect.

## Writing audit
Checked: customer as subject, active voice, third person outside quotes, positive paragraph openings, no superlatives, buzzwords, unproven firsts, or em dashes, claims kept to their scope, one set of targets, light labels in the press release. Fixed in the draft: "seat and fare stay the same" (not backed by evidence) changed to "nothing extra to pay"; the agency portal claim narrowed to what feature C covers.
Re-run after the team's changes: "wait on hold for up to three hours" (customer service operations lead, from what agents hear) agrees with the data, where the longest reported hold is 175 minutes, so it needs no label. Leader quote attributed by title, with no personal name. Press release: headline, subheading, 7 paragraphs, about 640 words.

## Readiness check
Verdict: **GREEN**, because all seven questions are answered: the team closed the speed target and the no-option path, and named the riskiest assumption after the PRD (2026-10-29). Open risks (reissue, booking-reference security) go to Validate.

## Prototype scope

**Q1: Who is the primary user, and what are they accountable for?**
A: Ingrid Halvorsen, a regional sales director who flies for work every week on a corporate contract. She is accountable for turning up to her customer meetings: a disruption that costs her an afternoon costs her a meeting. Daniel (a leisure traveller with a family) is the second journey, accountable for getting four people home together. Helena's daughter is the third, acting for a passenger who does not use the app. All three are disrupted-passenger personas built from Signals; Ingrid's is backed by 27 of her segment's own records.

**Q2: What is the pain today, end to end?**
A: A notification says the flight is cancelled or delayed and to contact the airline. The app and website show alternative flights but offer only "contact us". The passenger phones and waits on hold for up to three hours (50 to 175 minutes reported), or queues at an airport desk, while the flights they could see fill up. An agent rebooks them in a call that averages 37 minutes in the sample; sometimes the ticket is not reissued or a change fee is charged (13 records), and an automatic rebooking may already have put them on a flight days later (9 records). The worst part, in their words: "Not being able to change my flight myself."

**Q3: What does the prototype show?**
A: The full journey runs from the disruption notification to a confirmed new flight and boarding pass, for the passenger or someone acting for them, with a hand-off to a person when no option works. The prototype shows the slice below.

**Full journey:** notification of the disruption → open it in the app, on the website, or with a booking reference → see the airline's suggested flight and the alternatives with seats → compare what changes (times, connection, seats together, nothing extra to pay) → keep the suggestion or choose another → confirm → new ticket and boarding pass, with a text for passengers without the app → if none works, a clear route to a person. P1 additions: hotel for a next-day flight; travel desk view for bulk rebooking.

**Prototype slice:** three paths on one flow. (1) Ingrid, cancelled at the gate: notification → suggestion and two alternatives → pick the 07:20 → confirm → boarding pass (feature A). (2) Daniel at 23:00: the airline's suggestion is two days later; he replaces it with a next-afternoon flight with four seats together (feature B). (3) Helena's daughter at home: enters the booking reference, sees her parents' options, rebooks them, and Helena gets a text (feature C). Why this slice: it covers all three P0 features and the moment where the customer decides, which is where the riskiest assumption will sit.

**Q4: What happens automatically, what stays with the person, and how fast?**
A: The airline detects the disruption, sends the message, proposes a suggested flight, and lists the alternatives with seats; after the passenger confirms, it reissues the ticket and issues the boarding pass with no extra charge. The decision stays with the person: keep the suggestion, pick another, or ask for a person. The phone and the desk stay for anyone who wants them. Speed: a boarding pass in **under three minutes** from opening the message (team target, 2026-10-29). Basis: callers give up and call after about five minutes, from what callers tell the call centre (customer service operations lead). [Assumed]

**Q5: Which views does the user need, and how are they told to act?**
A: Four views: (1) the disruption message, which says what happened and offers "choose your new flight"; (2) the options view, with the suggested flight marked and the alternatives listed; (3) the comparison and confirmation, showing departure and arrival, connection, seats together for everyone on the booking, and that there is nothing to pay; (4) the confirmation, with the new boarding pass. A fifth entry, "rebook for someone else", takes a booking reference. At a glance the passenger must see departure time, arrival time, whether the party sits together, and the cost. They are told to act by the disruption notification in the app, by text, or by email, at any hour; passengers without the app get the text. When none of the alternatives works, the passenger is offered a call-back with the booking already loaded, and the refund route (head of digital, 2026-10-29). Nice-to-have for the prototype; P1-1 in the PRD.

**Q6: Which data does the product need, at business level?**
A: The main business objects: the **booking** (with its booking reference), the **passengers** on it, the **original flight**, the **disruption** (cancellation, or delay of more than two hours), the **alternative flights** with their seat availability, the airline's **suggested rebooking**, the **fare rules** that apply after a disruption, the reissued **ticket**, and the **boarding pass**. A booking holds one or more passengers and one or more flights; a disruption affects a flight and so every booking on it; each booking gets one suggestion and a list of alternatives. Alternatives already appear in the app and on the website today [Known]; reissue and fare rules work reliably only through an agent today [Known]. Seat availability has to be current at the moment the passenger confirms, because seats fill up while people wait. Whether that is true of what the app shows today is a question for the reissue spike, not for the prototype, which uses fictional data.

**Q7: What does the prototype measure?**
A: In the walk-throughs, the share of participants who reach a confirmed new flight without help, the time it takes, and whether they say they would still call to check. Completing without help maps to the self-service rebooking rate (12% to 35%); "would still call" maps to rebooking calls (42 to 25 per 100 disrupted passengers). For the persona critique today and real disrupted passengers later (research hypothesis 1). The riskiest assumption (team, 2026-10-29, widened after the persona critique): disrupted passengers offered real choices quickly will choose a flight themselves and will not need to call for anything else, such as a hotel, not only to check the flight. The prototype tests it with the three measures above; see `riskiest-assumption.md`.

| # | Gap | Question that would close it | Must-have or nice-to-have |
|---|-----|------------------------------|---------------------------|
| 1 | ~~No target time~~ **Closed:** under 3 minutes (callers give up after about 5) | Answered by the customer service operations lead | Must-have: the prototype measures it |
| 2 | ~~Riskiest assumption not named~~ **Closed:** choose and trust, without calling | "Which assumption, if wrong, ends the idea: that passengers trust a flight they chose, that they will choose at all, or something else?" (Reissue reliability is tested by the engineering spike, not by the prototype.) | Must-have: closes at step 6, after the PRD |
| 3 | ~~No "none works" screen~~ **Closed:** call-back with the booking loaded, plus the refund route | Answered by the head of digital | Nice-to-have for the prototype |
