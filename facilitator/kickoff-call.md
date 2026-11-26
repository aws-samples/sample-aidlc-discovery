# Before the workshop: the kickoff page

The kickoff page (`skills/aidlc-discovery/templates/kickoff.md`) is how a customer team tells Discovery who they are, what they believe, and what data they bring. A good page saves the first hour of the workshop and puts the team's beliefs on record before anyone sees the data. This guide covers getting it: the email to send, the 30-minute call, and the checks before the day.

## Timeline

| When | What | Who |
|------|------|-----|
| Two weeks before | Send the invitation email below, with the kickoff page attached. Book the call. | Facilitator |
| About ten days before | The 30-minute kickoff call. | Facilitator, product owner, engineering lead (the sponsor if possible) |
| One week before | The product owner sends back the filled-in page. The data owner starts the exports. | Customer |
| Three days before | The page and the data are in the working folder. Run the checks at the end of this guide. | Facilitator and customer |
| The day before | Send the reminder email. | Facilitator |

## The invitation email

Send it to the product owner, copy the sponsor and the engineering lead. Attach the kickoff page; in Japanese, `facilitator/ja/kickoff.md`.

```text
Subject: AI-DLC Discovery workshop on [date]: one page and some data to prepare

Hi [name],

Thanks for setting up the Discovery workshop for [product] on [date]. In one day, your team will go from customer feedback to a decision on what to build first, a clickable prototype, and a brief your build can start from.

To make the day count, we need two things from you beforehand.

1. The kickoff page (attached). One page about your product, who will be in the room, the business number you want to move, and the ideas the team already has. It takes about 30 minutes once we have talked it through. Please send it back by [date, one week before].

2. Your customer data. What customers tell you, exported as files:
   - reviews, support tickets, survey comments, call notes, or sales notes, ideally six months of each source you have;
   - if you have them, numbers that show behavior, such as orders or sign-ups by month, or the steps of a funnel;
   - if your engineers have it, telemetry: daily totals per journey step. No raw logs.
   Please remove personal data before anything leaves your systems. Our data preparation tool can do it on your own machine: [link to tools/prepare-data]. If the data cannot leave your environment at all, tell us: your team can write one-page summaries instead, and we will show you how.

I'd like a 30-minute call with you and [engineering lead] on [two options] to go through the page together. Bring the names of the people who will attend, and any idea someone on the team is already pushing.

Who should come on the day: the product owner and engineering lead who own the build, plus whoever knows the customers best (design, support, sales, or operations). Four to six people. If [sponsor] can join the first 30 minutes and the last 40, the decision lands better.

Thanks,
[your name]
```

## The kickoff call (30 minutes)

Your goal is a filled-in page, in the team's words, and no surprises on the day. You ask; they answer; you don't judge any idea. Fill in the page as they talk, or let the product owner type while you ask.

### Open (2 minutes)

**Say:** "This page is how the assistant learns about you before the workshop. Most of it is what you already know. The important part is what each of you believes today, because on the day we test it against your customers' data. There are no wrong answers: an idea that the data does not support is exactly what we want to find before you build it."

### The product (3 minutes)

**Ask:**
- "In one sentence, what does the product do, and for whom?"
- "Who are the main groups of users? Roughly what share is each?"
- "Does someone else pay for it, such as an employer or a buyer in another team?"
- "Why now? Is there a budget, a deadline, or a target behind this?"

Rough shares are fine. "About half" is useful; "we don't know" is a finding.

### The team (7 minutes)

**Ask each person, one at a time:** "What do you think is the main reason [the metric] is not where you want it to be?"

- Write each answer in the person's own words, with their role.
- Ask the quietest person first. If the most senior person answers first, the others tend to agree.
- If people disagree, say "Good, that's what the day will settle," and write both.
- Ask who else should be in the room, and what they would say. Add them.

### The business metric (5 minutes)

**Ask:**
- "What one number would leadership look at to say this worked?"
- "Is higher better or lower better?" Always ask, even when it seems obvious: every score depends on it.
- "What is it today, over which period, and where does that number come from?"
- "If it moved five points next year, would anyone notice?" If not, it is the wrong number.

If they give three numbers, ask which one the sponsor watches, and keep that one. If there is no baseline, agree who gets it and by when. Discovery can still run.

### The ideas they already have (8 minutes)

This is the "Ideas we already have" section. It records what the team wants to build before the data speaks.

**Ask:**
- "What would you build next if nobody asked you why?"
- "What do sales, leadership, or your biggest customers keep asking for?"
- "Is there something a competitor launched that people keep mentioning?"

Then turn each feature into a problem. **Ask:**
- "Who is stuck without it?"
- "What happens to them today? What do they do instead?"
- "How do you know? Complaints, a report, a feeling?"
- "Which number would it move?"
- "Who would own building it?"

For example, "an AI assistant in the app" becomes "customers can't find the right option themselves, so they call support". Keep the original idea in "Our idea, if any".

**Don't:** rank the ideas, push back, or say which one you think will win. **Say instead:** "On the day, the data scores every one of these, and adds problems none of us listed. We'll see together."

Three to five ideas is typical. None is fine: the assistant drafts them from the data.

### The data (5 minutes)

**Ask:**
- "Where do customers tell you things? Reviews, tickets, surveys, calls, sales notes?"
- "Who can export six months of each, and by when?"
- "Do you have numbers that show what customers do, such as orders, sign-ups, or funnel steps?"
- "Do your engineers have monitoring or analytics, aggregated by day?"
- "Can this data leave your environment once personal data is removed?"

If it can: point them to `tools/prepare-data`, and agree on the folder (`discovery/data/`). If it cannot: they write Signal Briefs in their own environment, one page per customer problem, with the `discovery-signal-brief` skill. Agree on who writes them.

### Close (2 minutes)

**Say:** "Thanks. [Name] finishes the page by [date] and sends it back with the data. Three days before the workshop I'll check that everything is in the folder. On the day, the assistant reads the page and we start with one confirmation."

Write down who sends what by when, and send it as a one-line follow-up.

## Red flags, and what to do

| You hear | What to do |
|----------|------------|
| "We already know what to build." | Keep the idea on the page. Say: "Then the day will show you the evidence for it, and anything that could make it fail." |
| Nobody owns the metric, or there are several. | Ask the sponsor to pick one before the day. Without one, scoring has nothing to aim at. |
| The data cannot leave, and nobody can write Signal Briefs. | Move the date, or run on a prepared synthetic dataset and plan a second session on real data. Never let the assistant invent data. |
| Only the sponsor's idea is on the page. | Ask each team member for theirs on the call. One idea means the day can only say yes or no to it. |
| The page names customers or accounts. | Replace them with a role or a segment before it goes in the folder. |

## Checks three days before

- [ ] `discovery/kickoff.md` is in the working folder, filled in, with no placeholders left.
- [ ] Every person on the team has a belief written in their words.
- [ ] One business metric, with "Higher is better" or "Lower is better", and a baseline or an owner for it.
- [ ] The ideas are written as problems: who is stuck, and what happens to them.
- [ ] The data files listed on the page are in the folder, and personal data is removed.
- [ ] Optional: open the page in the assistant and ask "Read discovery/kickoff.md and tell me what is missing." Fix what it names.

## The reminder email

```text
Subject: Tomorrow: AI-DLC Discovery for [product]

Hi all,

See you tomorrow at [time] in [room or link]. The kickoff page and the data are in place, so we start straight away.

Two things to bring: your own view of what the main problem is (you wrote it on the page; we'll check it against the data before lunch), and the person who can answer questions about the data, if it isn't you.

[sponsor], we'd love you for the first 30 minutes and the readout at [time].

[your name]
```
