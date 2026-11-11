# Facilitator notes: AnyCompany Health

> **Spoilers. Facilitators only.** This page describes the designed truths in the sample data. Participants should not read it before the workshop.

All counts come from `scripts/samples/anycompany-health.py`, which prints them, and cover 1 May to 15 October 2026.

## 1. The story

The team arrives split between a new mobile app and telehealth, the two requests leadership and brokers repeat most. The briefs and aggregates show that the biggest problem is simpler: members cannot see where their claim is or what is needed from them, and that one question drives about 40% of all calls and the largest share of broker escalations and employer complaints. The app's poor rating is mostly the same complaint, and telehealth is an employer request that members barely mention.

## 2. The designed truths

**Top problem: claim status and "what do you need from me".**
- Member services: 34,334 of 85,519 calls were about claim status (40.1%), or 119.7 calls per 1,000 claims (the metric's baseline of 120).
- Claims system: 28,052 of 286,842 claims (9.8%) waited for information from the member. Agents estimate about half of claim-status calls are about one of these (SB-02).
- Portal: "claim status" was searched 49,250 times and "where is my claim" 21,960 times; 61% and 66% of those searches were followed by a call within 48 hours. Members look first, fail, then call.
- Brokers: 498 of 1,240 escalations (40.2%) were claim delays or status for client employees.
- Employers: 62 of 180 employer groups reviewed raised employees' claim complaints, the most common theme.
- Briefs: SB-01, SB-02, SB-03, and SB-04 describe this one problem from four angles. Signals should merge them.

**Loud requests: telehealth and a new mobile app.**
- Telehealth (SB-07): 43 of 180 employers asked, and 116 broker escalations (9.4%) passed the request on. Among members, telehealth was 1,601 calls (1.9%), and "telehealth" plus "virtual visit" were searched 3,140 and 1,370 times, with few followed by a call.
- Mobile app (SB-08): 34 of 180 employers asked for a better app, and 100 broker escalations (8.1%). The app is rated 2.9 from 1,860 reviews, but 54% of the 1 and 2-star reviews complain about claim status, not the app.

**Secondary real pain: provider directory accuracy.**
- Member services: 12,005 calls (14.0%).
- Portal: "find a doctor" was searched 31,290 times, 27% followed by a call; "in network dentist" 8,030 times, 32% followed by a call.
- Brokers: 206 escalations (16.6%) about directory errors or surprise bills.
- Employers: 29 of 180 raised directory errors.
- Briefs: SB-05 and SB-06 describe it. Signals should merge them.

**Distractor: wellness rewards (SB-09).** 24 of 180 employers mentioned it. "wellness rewards" was searched 930 times, no contact reason covers it, and employers call it a nice extra. It should fail the gate's painkiller test.

**Counter-evidence: the digital ID card works (SB-10).** Only 2,519 calls (2.9%). "id card" was searched 26,570 times and only 3% of those searches were followed by a call. 16 employers praised it unprompted. It shows what members do when information is easy to find.

**Noise.** Benefits and coverage (16.1%), billing and premiums (9.9%), prior authorization (8.0%), and portal login (4.0%) are real call reasons that none of the briefs focus on. Signals should mention them as data gaps, not invent briefs for them.

## 3. What Signals should find

The top signal is claim status, merged from four briefs, with High confidence: four independent sources, including the call and search aggregates. Provider directory accuracy is second. Telehealth and the app should appear as requests from employers and brokers, with weak member evidence.

How the team's expectations usually compare:
- "Members want a new app" (product owner): contradicted as stated. The app's complaints are claim complaints.
- "Telehealth wins renewals" (broker relations): not settled. The request is real among employers, but there is no member demand and no renewal evidence in this data.
- "The claims system is slow" (engineering lead): partly supported. The average decision takes 10 to 12 days, but the bigger problem is that members cannot see progress or what is needed.
- "Members are confused by explanation of benefits letters" (UX designer): weakly supported. "explanation of benefits" was searched 9,160 times, 40% followed by a call, but no brief focuses on it.

## 4. Expected scoring

Default weights. Draft scores; the team should confirm or override strategic fit and feasibility.

| Candidate | Gate | Pain | Outcome | Reach | Fit | Feasibility | Adoption | Weighted | Confidence | Decision |
|-----------|------|:----:|:-------:|:-----:|:---:|:-----------:|:--------:|:--------:|------------|----------|
| Claim tracker | Pass | 5 | 5 | 5 | 4 | 3 | 4 | 4.50 | High | Build first |
| Provider directory accuracy | Pass | 4 | 3 | 4 | 4 | 3 | 5 | 3.70 | High | Build first |
| Mobile app rebuild | Pass, but merge | 3 | 2 | 4 | 3 | 1 | 3 | 2.60 | Medium | Defer |
| Telehealth | Pass | 2 | 3 | 3 | 4 | 2 | 3 | 2.70 | Low | Defer |
| Wellness rewards | Fails: painkiller, evidence | | | | | | | | | Drop |

Why:
- **Claim tracker.** Pain 5: the largest call reason every month, and members try the portal first. Outcome 5: it moves the metric directly. Reach 5: every claimant, plus brokers and HR teams. Feasibility 3: the claims system holds the status and pended reason, but exposing them to the portal is real work; the engineering lead should confirm. Adoption 4: members already search for it.
- **Provider directory accuracy.** Strong evidence and no change for members (adoption 5), but it moves directory calls and complaints, not the claim-status metric (outcome 3).
- **Mobile app rebuild.** It scores a solution, not a problem. When the team states the problem ("members cannot get claim information on the phone"), it is the claim tracker's problem and should be merged into it. Feasibility 1: a rebuild is large.
- **Telehealth.** Employers and brokers ask, members barely do. Its outcome is renewal, which this data cannot measure, so confidence is Low and it is deferred to the follow-up with a question for employers.
- **Wellness rewards.** Members would not notice if it never shipped (painkiller), and the only evidence is a minority of employers (evidence).

## 5. The likely riskiest assumption

For the claim tracker: members who can see a claim's status and exactly what is needed from them will check the portal instead of calling. The search data shows members already look before calling, so the risk is in the information, not the channel. A close second: the claims system can show a member's real status and pended reason in near real time. The engineering lead should name it under feasibility.

## 6. A good decision

**Commit, testing first.** The pain and the metric link are strong, but the decision depends on two things the workshop cannot settle: whether the claims system can expose status and pended reasons to the portal, and whether members stop calling when they can see them. Good conditions before the build: the claims team confirms the data is available, and a test with members on pended claims shows they find what is needed without calling. Provider directory accuracy goes forward as a second pod or the next brief.

## 7. Traps

- **Taking employer requests as member demand.** Telehealth and wellness rewards are loud in renewal meetings but nearly absent from member signals.
- **Scoring the app rebuild as its own problem.** Its low rating is the claim complaint again. Merge it.
- **Missing "what do you need from me".** Pended claims are about half of claim-status calls. A tracker that only shows "in process" solves half the problem.
- **Asking for raw data.** The team works from briefs and aggregates on purpose. The assistant must not request call transcripts or member records, and must not invent them.
- **Fixing what works.** The digital ID card is the counter-example: it is what easy-to-find information looks like.
- **Leaving the briefs unmerged.** Four briefs describe claim status and two describe the directory. Counting them separately inflates the number of themes and hides the size of the top one.

## 8. Expectations for automated tests

```yaml
expectations:
  top_signal: "claim status | where is my claim | claim"
  loud_request: "telehealth"
  distractor_fails_gate: "wellness rewards"
  build_first_or_learn: "claim tracker"
  data_input: signal-briefs
```
