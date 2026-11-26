# Kickoff page: AnyCompany Health member portal and app

Filled in by the AnyCompany Health digital team before the Discovery workshop. AnyCompany Health, its members, and every record in this folder are fictional.

## The product

- **Company:** AnyCompany Health, a regional health insurer that sells group health plans to employers through brokers.
- **Product:** the web portal and the mobile app. Members check claims, find doctors, and show their digital ID card; employer HR teams manage enrollment; brokers quote plans and look after their clients.
- **Who uses it:** members, about 420,000 people covered through employer group plans; employer HR teams, at about 1,900 companies from 50 to 5,000 employees; and brokers, at about 260 firms.
- **Who pays, if not the users:** the employer groups, which brokers sell and service. The HR account team reviews the largest 180 each year.
- **Why now:** the app has a 2.9-star rating, and the director of digital member experience has asked for budget to rebuild it.

## The team

| Role | What they believe the main problem is |
|------|---------------------------------------|
| Director of digital member experience (product owner) | The app is the problem: it has a 2.9-star rating, and she has asked for budget to rebuild it. |
| Engineering lead, member portal | The portal is fine and the claims system is slow. Owns the portal and app, not the claims system. |
| Head of member services | Runs the contact center. Call volume is too high, but she has never seen it broken down next to the other teams' data. |
| Broker relations manager | Telehealth wins renewals: "every competitor has it, and our brokers keep asking." |
| UX designer | Members are confused by the explanation of benefits letters. |
| Privacy and compliance lead | Attends to make sure no member data leaves the insurer. The reason the team works from Signal Briefs. |

Joins only the kickoff and the readout: nobody.

## The business metric

- **Metric:** claim-status calls per 1,000 claims. Every call that asks "where is my claim?" costs agent time and means the member could not find the answer alone.
- **Which direction is good:** Lower is better
- **Baseline:** 120, over 1 May to 15 October 2026, from the member services call data.

## Ideas we already have

1. **Claim tracker**
   - Who has it: members who file claims, and the brokers and HR teams they turn to.
   - The problem: members cannot see where a claim is or what is needed from them, so they call.
   - Evidence we think we have: member services says claim status is "one of our top call reasons".
   - Business metric it moves: claim-status calls per 1,000 claims.
   - Owner: director of digital member experience.
2. **Telehealth**
   - Who has it: employees of employer groups.
   - The problem: employers say the plan falls behind competitors without virtual visits.
   - Evidence we think we have: broker and employer requests at renewal.
   - Business metric it moves: employer renewal rate.
   - Owner: broker relations manager.
3. **Mobile app rebuild**
   - Who has it: members who use the app.
   - The problem: the app is rated 2.9 stars, and members complain about it.
   - Evidence we think we have: the app store rating and reviews.
   - Business metric it moves: app rating and monthly active app users.
   - Owner: director of digital member experience.
4. **Wellness rewards**
   - Who has it: employees of employer groups.
   - The problem: employers want more employee engagement with the plan.
   - Evidence we think we have: a few HR teams have asked for it.
   - Business metric it moves: member engagement.
   - Owner: broker relations manager.
5. **Provider directory accuracy**
   - Who has it: members looking for a new doctor or dentist.
   - The problem: the directory lists providers who are out of network, have moved, or are not taking patients.
   - Evidence we think we have: occasional complaints about surprise bills.
   - Business metric it moves: directory-related calls and complaints.
   - Owner: engineering lead, member portal.

## The data

- **Input:** signal-briefs
- **Where it is:** `discovery/signal-briefs/`
- **Period:** 1 May to 15 October 2026
- **Sample data:** Yes: fictional, so the run is a demonstration and its brief is not evidence for a build

| File | Source | Records |
|------|--------|---------|
| `sb-01` to `sb-10` | Signal Briefs, one problem each, written by member services, the broker team, and the HR account team | 10 |
| `calls-by-contact-reason.csv` | Member services calls by contact reason (October covers 1 to 15) | 6 monthly rows |
| `claim-volumes.csv` | Claims received, decided, and waiting for member information, with claim-status calls per 1,000 claims | 6 monthly rows |
| `portal-search-terms.csv` | Portal search terms with their volume, and the share followed by a call within 48 hours | 12 rows |
| `broker-escalations.csv` | Broker escalations by category | 7 rows |
| `employer-review-themes.csv` | Themes raised by the 180 employer groups reviewed | 6 rows |

- **Telemetry, if any:** none.
- **Personal data removed:** not needed: there is no record-level member data. The data is regulated and cannot leave the insurer's environment, so the team brings Signal Briefs and aggregate statistics instead of raw records.

## What we already know we cannot change

- No member data leaves the insurer's environment.
- The claims system belongs to another team; the portal team owns the portal and app only.
