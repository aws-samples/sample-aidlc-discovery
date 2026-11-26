# Kickoff page: [product]

> **What this page is for.** The team fills it in before the Discovery workshop. On the day, the assistant reads it and drafts the setup, so the workshop starts with one confirmation instead of rounds of questions. It is also the record of what the team believed before it saw the data. The day tests those beliefs.
>
> **How to fill it in.** One person writes, usually the product owner, after a short call with the facilitator. Write in plain sentences. Rough numbers are fine; say where they come from. If you don't know something, write "don't know": that is useful too. Leave out customer names, account names, and revenue amounts.
>
> **Where it goes.** Save it as `discovery/kickoff.md` in the folder the assistant works in, next to the data in `discovery/data/`. Delete these grey guidance blocks when you are done, or leave them: the assistant skips them.

## The product

> Who you are and what you make, so the assistant does not guess. One line each.
>
> Example (a meal-kit delivery service): "Company: a meal-kit delivery service in three cities, about 40,000 active customers." "Product: the ordering app and website, where customers pick weekly recipes, skip weeks, and manage their subscription."

- **Company:** [what the company does, and roughly how big it is]
- **Product:** [the product this Discovery is about, and what people do with it]
- **Who uses it:** [the main groups of users, with a rough share each, such as "families, about 60% of customers"]
- **Who pays, if not the users:** [such as "employers" or "the IT department"; or "the users"]
- **Why now:** [what makes this the moment: a budget, a deadline, a competitor, a target; or "nothing special"]

## The team

> Who will be in the room, and what each person thinks the main problem is today. Ask each person, not only the product owner, and write their answer in their words, even when people disagree. Disagreement is useful: the data settles it.
>
> Example: "Head of growth: customers leave because our recipes get repetitive." "Operations lead: late deliveries are what make people cancel."

| Role | What they believe the main problem is |
|------|---------------------------------------|
| Product owner | |
| Engineering lead | |
| [design, data, support, sales, operations, or compliance] | |

Joins only the kickoff and the readout: [the sponsor, and what they believe; or "nobody"]

## The business metric

> The one number the work should move. Discovery scores every idea against it, so pick the number leadership already watches. Say which direction is good: the assistant never assumes it.
>
> Example: "Metric: share of new customers who order again within 30 days." "Which direction is good: Higher is better." "Baseline: 34% over January to June, from the orders database."
>
> No baseline yet? Write who will get it and by when. Discovery can still run.

- **Metric:** [the number, and how it is counted]
- **Which direction is good:** [Higher or Lower] is better
- **Baseline:** [value], over [period], from [source]. If there is none yet: [who brings it, and by when]

## Ideas we already have

> The things people on the team already want to build: roadmap items, requests from sales or leadership, something a competitor launched. Most teams have three to five. Write each one as the problem it would solve for a customer, not as the feature. Then the day can compare it fairly with what the data shows.
>
> To turn a feature into a problem, ask: "Who is stuck without it, and what happens to them?" "Add a chatbot" becomes "customers can't find out where their box is, so they email support".
>
> Discovery checks every idea here against the data, and adds problems the data shows that nobody listed. An idea that scores low is not a failure: knowing it before building it is the point. No ideas yet? Leave this section empty, and the assistant will draft them from the data.
>
> Example:
>
> 1. **Recipe variety**
>    - Who has it: customers in their third month and later.
>    - The problem: they see the same recipes again and cancel.
>    - Evidence we think we have: cancellation survey comments.
>    - Business metric it moves: repeat orders within 30 days.
>    - Owner: head of growth.
>    - Our idea, if any: an assistant that suggests recipes from what the customer rated well.

1. **[The name the team uses for it]**
   - Who has it: [which customers or users]
   - The problem: [what goes wrong for them, and what they do then]
   - Evidence we think we have: [what makes the team believe it: a report, complaints, a feeling]
   - Business metric it moves: [the metric above, or another one]
   - Owner: [the role who would own the build]
   - Our idea, if any: [the solution someone already has in mind]

## The data

> What the team brings. Customer feedback is the core: reviews, support tickets, survey comments, call notes, sales notes. Exports as CSV, Excel, PDF, Word, or text all work. Numbers that show behavior (orders by month, funnel steps) make the scores much stronger. Ask the engineering team for telemetry, if it has it: daily totals per journey step, never raw logs.
>
> Before anything goes in the folder, remove personal data with `tools/prepare-data`, on your own machine. If the data cannot leave your environment at all, write Signal Briefs instead: one anonymized page per customer problem, written in your own environment.
>
> Example row: "`support-tickets.csv` | Help desk export: topic, date, and the customer's message | 2,400".

- **Input:** [production for real exports; signal-briefs for one-page summaries; synthetic for a prepared practice set]
- **Where it is:** [a folder in the working folder, such as `discovery/data/`]
- **Period:** [from, to]
- **Sample data:** [No; or Yes: fictional, so the run is a demonstration and its brief is not evidence for a build]

| File | Source | Records |
|------|--------|---------|
| | | |

- **Telemetry, if any:** [what it covers, in `discovery/data/telemetry/`; or "none"]
- **Personal data removed:** [yes, with `tools/prepare-data` on (date); or not needed, because (reason)]

## What we already know we cannot change

> Limits the build has to live with, so Discovery does not recommend something impossible: a regulation, a system another team owns, a contract, a launch date.
>
> Example: "Payments go through our provider's hosted page; we cannot change it." "Nothing can ship during the December peak."

- [a limit, and why; or "nothing known yet"]
