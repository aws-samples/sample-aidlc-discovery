# AnyCompany Health: a member portal under pressure

A fictional sample for AI-DLC Discovery. AnyCompany Health's data is regulated and cannot leave its environment, so the team brings Signal Briefs and aggregate statistics instead of raw records.

## The company and its product

AnyCompany Health is a regional health insurer that sells group health plans to employers through brokers. Its web portal and mobile app serve three audiences: members check claims, find doctors, and show their digital ID card; employer HR teams manage enrollment; brokers quote plans and look after their clients.

## Customers and segments

- **Members:** about 420,000 people covered through employer group plans.
- **Employer groups:** about 1,900 companies, from 50 to 5,000 employees. HR teams are the day-to-day contact; the HR account team reviews the largest 180 each year.
- **Brokers:** about 260 broker firms, which sell and service most of the employer groups.

## The team

- **Director of digital member experience** (product owner). Believes the app is the problem: it has a 2.9-star rating, and she has asked for budget to rebuild it.
- **Engineering lead, member portal.** Believes the portal is fine and the claims system is slow. Owns the portal and app, not the claims system.
- **Head of member services.** Runs the contact center. Feels call volume is too high, but has never seen it broken down next to the other teams' data.
- **Broker relations manager.** Believes telehealth wins renewals: "every competitor has it, and our brokers keep asking."
- **UX designer.** Believes members are confused by the explanation of benefits letters.
- **Privacy and compliance lead.** Attends to make sure no member data leaves the insurer. The reason the team works from Signal Briefs.

## The business metric

**Claim-status calls per 1,000 claims.** Baseline: 120, from 1 May to 15 October 2026. Every call that asks "where is my claim?" costs agent time and means the member could not find the answer alone.

## Candidate use cases the team brings

1. **Claim tracker.**
   - Who: members who file claims, and the brokers and HR teams they turn to.
   - Problem: members cannot see where a claim is or what is needed from them, so they call.
   - Evidence the team thinks it has: member services says claim status is "one of our top call reasons".
   - Metric: claim-status calls per 1,000 claims.
   - Owner: director of digital member experience.
2. **Telehealth.**
   - Who: employees of employer groups.
   - Problem: employers say the plan falls behind competitors without virtual visits.
   - Evidence the team thinks it has: broker and employer requests at renewal.
   - Metric: employer renewal rate.
   - Owner: broker relations manager.
3. **Mobile app rebuild.**
   - Who: members who use the app.
   - Problem: the app is rated 2.9 stars, and members complain about it.
   - Evidence the team thinks it has: the app store rating and reviews.
   - Metric: app rating and monthly active app users.
   - Owner: director of digital member experience.
4. **Wellness rewards.**
   - Who: employees of employer groups.
   - Problem: employers want more employee engagement with the plan.
   - Evidence the team thinks it has: a few HR teams have asked for it.
   - Metric: member engagement.
   - Owner: broker relations manager.
5. **Provider directory accuracy.**
   - Who: members looking for a new doctor or dentist.
   - Problem: the directory lists providers who are out of network, have moved, or are not taking patients.
   - Evidence the team thinks it has: occasional complaints about surprise bills.
   - Metric: directory-related calls and complaints.
   - Owner: engineering lead, member portal.

## The data

Everything is in `discovery/signal-briefs/`, covering 1 May to 15 October 2026. There is no record-level member data.

- `sb-01` to `sb-10`: 10 Signal Briefs, one problem each, written by member services, the broker team, and the HR account team.
- `calls-by-contact-reason.csv`: member services calls by contact reason, 6 monthly rows (October covers 1 to 15).
- `claim-volumes.csv`: claims received, decided, and waiting for member information, with claim-status calls per 1,000 claims, 6 monthly rows.
- `portal-search-terms.csv`: 12 portal search terms with their volume, and the share followed by a call within 48 hours.
- `broker-escalations.csv`: broker escalations by category, 7 rows.
- `employer-review-themes.csv`: themes raised by the 180 employer groups reviewed, 6 rows.

## How to run it

1. In AWS Quick Desktop, open **Settings**, then **My computer**, then **Local folders**, and add this folder (`samples/anycompany-health`).
   Optional, recommended: create a Space in AWS Quick and name it yourself (**Spaces**, then **Create space**), attach it and this folder to a chat (the **+** menu), and ask Quick to copy `README.md` and the `discovery/` data folder into the Space, keeping the same paths. Then work from a new chat with only the Space attached: the scenario, the data, and the Discovery artifacts all live in the Space, and you can share it with your team. The data is fictional, so it can go in a Space.
2. In a new chat, ask:

   ```text
   Start AI-DLC Discovery. Project: member-portal. Product: AnyCompany Health's member portal and app. Data: signal-briefs, in discovery/signal-briefs/ in my anycompany-health folder.
   ```

   With everything in a Space, name it for Discovery and the data:

   ```text
   Start AI-DLC Discovery. Project: member-portal. Product: AnyCompany Health's member portal and app. Save Discovery in the [your Space] space. Data: signal-briefs, in discovery/signal-briefs/ in the [your Space] space.
   ```

3. Answer the setup questions as the team above, and write the team's expectations before the analysis.

The data is fictional. A run on it demonstrates Discovery; it is not evidence for a build. The designed answers are in [facilitator/anycompany-health.md](../../facilitator/anycompany-health.md). Read it after the run, not before.
