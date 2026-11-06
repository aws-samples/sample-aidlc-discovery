"""Generate the AnyCompany Health sample: 10 Signal Briefs and aggregate statistics.

AnyCompany Health is a fictional regional health insurer. Its data is regulated,
so the sample holds no record-level data: only Signal Briefs written by three
internal teams, and aggregate CSVs that agree with them.

Usage: python3 scripts/samples/anycompany-health.py
Writes samples/anycompany-health/discovery/signal-briefs/ and prints the counts
that facilitator/anycompany-health.md quotes.
"""

from __future__ import annotations

import csv
import io
import random
from pathlib import Path

SEED = 4212
ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "samples" / "anycompany-health" / "discovery" / "signal-briefs"

WRITTEN = "2026-10-20"
PERIOD = ("2026-05-01", "2026-10-15")
MONTHS = [("2026-05", 31, 31), ("2026-06", 30, 30), ("2026-07", 31, 31), ("2026-08", 31, 31), ("2026-09", 30, 30), ("2026-10", 15, 31)]  # month, days covered, days in month

CLAIMS_PER_FULL_MONTH = 52_000
CALLS_PER_CLAIM = 0.30

# Share of member services calls by contact reason. The designed truth: claim status
# is about 40%, provider directory is the real secondary pain, and the ID card and
# telehealth are small.
CONTACT_REASONS = {
    "claim_status": 0.40,
    "benefits_and_coverage": 0.16,
    "provider_directory": 0.14,
    "billing_and_premiums": 0.10,
    "prior_authorization": 0.08,
    "app_or_portal_login": 0.04,
    "member_id_card": 0.03,
    "telehealth": 0.02,
    "other": 0.03,
}
PENDED_SHARE = (0.088, 0.102)          # claims waiting for information from the member
PORTAL_SEARCHES = {                    # term: (searches in the period, share followed by a call within 48 hours)
    "claim status": (48_000, 0.61),
    "where is my claim": (21_000, 0.66),
    "find a doctor": (30_000, 0.28),
    "explanation of benefits": (9_500, 0.42),
    "in network dentist": (8_200, 0.31),
    "prior authorization": (7_800, 0.35),
    "premium payment": (6_500, 0.18),
    "id card": (26_000, 0.04),
    "download app": (4_200, 0.05),
    "telehealth": (3_100, 0.12),
    "virtual visit": (1_400, 0.10),
    "wellness rewards": (900, 0.03),
}
BROKER_ESCALATIONS_TOTAL = 1_240
BROKER_CATEGORIES = {
    "claim_delay_or_status_for_client_employees": 0.38,
    "provider_directory_error_or_surprise_bill": 0.17,
    "plan_administration_and_enrollment": 0.15,
    "telehealth_request_from_employer": 0.09,
    "mobile_app_request_from_employer": 0.08,
    "billing_and_invoices": 0.08,
    "other": 0.05,
}
EMPLOYERS_IN_REVIEW = 180              # employer groups with a renewal or quarterly review in the period
EMPLOYER_THEMES = {                    # theme: employers that raised it
    "employees_complain_about_claim_status": 64,
    "requested_telehealth": 41,
    "requested_a_better_mobile_app": 33,
    "provider_directory_errors": 29,
    "requested_a_wellness_rewards_program": 22,
    "praised_the_digital_id_card": 18,
}
APP_RATING, APP_REVIEWS, APP_LOW_REVIEWS_ABOUT_CLAIMS = 2.9, 1_860, 0.54


def to_csv(header: list[str], rows: list[list]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return buf.getvalue()


def generate() -> tuple[dict[str, str], dict]:
    rng = random.Random(SEED)
    files: dict[str, str] = {}

    # Calls and claims, month by month.
    call_rows, claim_rows = [], []
    totals = {reason: 0 for reason in CONTACT_REASONS}
    claims_total = pended_total = 0
    for month, days, month_days in MONTHS:
        claims = round(CLAIMS_PER_FULL_MONTH * days / month_days * (1 + rng.uniform(-0.04, 0.04)))
        calls = round(claims * CALLS_PER_CLAIM * (1 + rng.uniform(-0.03, 0.03)))
        counts = {}
        for reason, share in CONTACT_REASONS.items():
            if reason == "other":
                continue
            jitter = rng.uniform(-0.015, 0.015) if reason == "claim_status" else rng.uniform(-0.006, 0.006)
            counts[reason] = round(calls * max(share + jitter, 0.005))
        counts["other"] = calls - sum(counts.values())
        for reason in CONTACT_REASONS:
            totals[reason] += counts[reason]
        call_rows.append([month, days, calls] + [counts[r] for r in CONTACT_REASONS])

        pended = round(claims * rng.uniform(*PENDED_SHARE))
        avg_days = round(rng.uniform(10.2, 11.8), 1)
        per_1000 = round(counts["claim_status"] / claims * 1000, 1)
        claim_rows.append([month, days, claims, claims - pended, pended, avg_days, per_1000])
        claims_total += claims
        pended_total += pended

    files["calls-by-contact-reason.csv"] = to_csv(
        ["month", "days_covered", "total_calls"] + [f"{r}_calls" for r in CONTACT_REASONS], call_rows)
    files["claim-volumes.csv"] = to_csv(
        ["month", "days_covered", "claims_received", "decided_without_member_action",
         "pended_waiting_for_member_information", "average_days_to_decision",
         "claim_status_calls_per_1000_claims"], claim_rows)

    # Portal searches over the period.
    search_rows, searches = [], {}
    for term, (volume, follow) in PORTAL_SEARCHES.items():
        count = round(volume * (1 + rng.uniform(-0.05, 0.05)), -1)
        share = round(follow + rng.uniform(-0.02, 0.02), 2)
        searches[term] = (int(count), share)
        search_rows.append([term, int(count), share])
    files["portal-search-terms.csv"] = to_csv(["search_term", "searches", "share_followed_by_call_within_48h"], search_rows)

    # Broker escalations over the period.
    broker = {}
    for category, share in BROKER_CATEGORIES.items():
        if category != "other":
            broker[category] = round(BROKER_ESCALATIONS_TOTAL * share * (1 + rng.uniform(-0.06, 0.06)))
    broker["other"] = BROKER_ESCALATIONS_TOTAL - sum(broker.values())
    files["broker-escalations.csv"] = to_csv(
        ["category", "escalations", "share"],
        [[c, n, round(n / BROKER_ESCALATIONS_TOTAL, 3)] for c, n in broker.items()])

    # Themes raised by employer groups in renewal and quarterly reviews.
    employers = {theme: n + rng.randint(-2, 2) for theme, n in EMPLOYER_THEMES.items()}
    files["employer-review-themes.csv"] = to_csv(
        ["theme", "employers_raising_it", "employers_in_review", "share"],
        [[t, n, EMPLOYERS_IN_REVIEW, round(n / EMPLOYERS_IN_REVIEW, 2)] for t, n in employers.items()])

    calls_total = sum(totals.values())
    stats = {
        "claims_total": claims_total,
        "calls_total": calls_total,
        "calls": totals,
        "share": {r: totals[r] / calls_total for r in totals},
        "pended_total": pended_total,
        "pended_share": pended_total / claims_total,
        "claim_status_per_1000": totals["claim_status"] / claims_total * 1000,
        "searches": searches,
        "broker": broker,
        "employers": employers,
    }
    files.update(briefs(stats))
    return files, stats


def pct(x: float) -> str:
    return f"{round(x * 100)}%"


def num(n: int) -> str:
    return f"{n:,}"


def brief(number: int, slug: str, title: str, author: str, theme: str, job: str, evidence: list[str],
          impact: str, confidence: str, segment: str, next_step: str) -> tuple[str, str]:
    lines = [
        f"# Signal Brief: {title}",
        f"Brief ID: SB-{number:02d} | Written: {WRITTEN} | Period covered: {PERIOD[0]} to {PERIOD[1]} | Author: {author}",
        "",
        f"**Theme:** {theme}",
        "",
        f"**Job or desired outcome:** {job}",
        "",
        "**Evidence:**",
        *[f"- {e}" for e in evidence],
        "",
        f"**Estimated impact:** {impact}",
        "",
        f"**Confidence:** {confidence}",
        "",
        f"**Segment:** {segment}",
        "",
        f"**Suggested next step:** {next_step}",
        "",
    ]
    return f"sb-{number:02d}-{slug}.md", "\n".join(lines)


def briefs(s: dict) -> dict[str, str]:
    calls, share, srch, brk, emp = s["calls"], s["share"], s["searches"], s["broker"], s["employers"]
    out = [
        brief(1, "claim-status-calls", "members cannot see where their claim is", "member services team",
              "Members call to ask where their claim is, because the portal shows only \"received\" or \"processed\".",
              "Know what is happening with a claim, and when it will be paid, without calling.",
              [f"\"I've called three times this month. Every time I'm told it's in process. In process where?\" (member call, summarized by the agent)",
               f"\"The portal just says received. Received three weeks ago. That tells me nothing.\" (member call, summarized by the agent)",
               f"\"I don't want to call. I want to look it up like a parcel.\" (member call, summarized by the agent)",
               f"{num(calls['claim_status'])} of {num(s['calls_total'])} member services calls in the period were about claim status ({pct(share['claim_status'])}), about {round(s['claim_status_per_1000'])} calls for every 1,000 claims"],
              f"About {num(round(calls['claim_status'] / 5.5))} calls a month. At an estimated 6 minutes a call, about {num(round(calls['claim_status'] * 6 / 60 / 5.5))} agent hours a month (estimate).",
              "High, because the pattern is the largest contact reason every month, and brokers and employer HR teams report the same thing.",
              "Members in employer group plans who file claims often, mostly families and people with ongoing treatment.",
              "Check whether the claims system can show a member the real status of each claim and the expected decision date."),
        brief(2, "pended-claims", "members do not know what we need from them", "member services team",
              "When a claim is waiting for information, members do not know what is missing, so they call or send the wrong document.",
              "Send the right document once, and get the claim paid.",
              [f"\"The letter says additional information required. What information? From me or from my doctor?\" (member call, summarized by the agent)",
               f"\"I uploaded the receipt twice. Then they told me they needed the referral, not the receipt.\" (member call, summarized by the agent)",
               f"\"I only found out it was stuck when the dentist sent me the bill.\" (member call, summarized by the agent)",
               f"{num(s['pended_total'])} of {num(s['claims_total'])} claims in the period waited for information from the member ({pct(s['pended_share'])}). Agents estimate about half of claim-status calls are about one of these"],
              "Pended claims take about two weeks longer to decide, and many generate two or three calls each (estimate).",
              "High, because the pended volume comes from the claims system and agents see the same questions daily.",
              "Members with claims that need a referral, a receipt, or information from their provider.",
              "List the five most common reasons a claim is pended, and check whether the claims system records which one applies."),
        brief(3, "broker-claim-escalations", "brokers chase claims for their clients' employees", "broker team",
              "Brokers spend their time chasing claim status for the employees of the companies they serve.",
              "Answer a client's question about a claim without opening an escalation.",
              [f"\"Half my week is chasing claims for my clients' staff. I can't see anything either, so I email you.\" (broker, in a quarterly review)",
               f"\"My client's CFO asked why an employee's surgery claim has been pending for five weeks. I had no answer.\" (broker escalation)",
               f"{num(brk['claim_delay_or_status_for_client_employees'])} of {num(BROKER_ESCALATIONS_TOTAL)} broker escalations in the period were about claim delays or status ({pct(brk['claim_delay_or_status_for_client_employees'] / BROKER_ESCALATIONS_TOTAL)}), the largest category"],
              "Brokers say slow claim answers come up in renewal conversations; we have no measure of lost renewals (estimate).",
              "Medium, because the escalation counts are solid, but they show what brokers chase, not what members experience.",
              "Brokers serving companies with 50 to 1,000 employees.",
              "Ask five brokers which claim information they would need to answer a client without escalating."),
        brief(4, "hr-claim-complaints", "employees complain to HR about claims", "HR account team",
              "Employer HR teams field employees' complaints about claims that seem stuck, and pass them on to us.",
              "Keep employees happy with their health plan without HR becoming a claims help desk.",
              [f"\"Our people come to HR because they can't get a straight answer about their claims.\" (HR director, renewal meeting)",
               f"\"We like the plan. We don't like being the middleman for claim questions.\" (HR manager, quarterly review)",
               f"{emp['employees_complain_about_claim_status']} of {EMPLOYERS_IN_REVIEW} employer groups reviewed in the period raised employees' claim complaints, the most common theme"],
              "Claim complaints come up in renewal meetings, and account managers believe they weaken renewals (estimate, not measured).",
              "Medium, because it is a consistent theme across employers, but we hear it second hand through HR.",
              "HR teams at employer groups with more than 200 employees.",
              "Compare renewal outcomes for employers who raised claim complaints with those who did not."),
        brief(5, "directory-calls", "the provider directory sends members to the wrong place", "member services team",
              "Members call because the provider directory shows doctors who are not in network, have moved, or are not taking new patients.",
              "Find an in-network doctor who will actually see them.",
              [f"\"Three of the five dentists the site listed said they don't take our plan anymore.\" (member call, summarized by the agent)",
               f"\"The phone number for the clinic was a pizza place.\" (member call, summarized by the agent)",
               f"{num(calls['provider_directory'])} member services calls in the period were about the provider directory ({pct(share['provider_directory'])})",
               f"{num(srch['find a doctor'][0])} portal searches for \"find a doctor\"; {pct(srch['find a doctor'][1])} were followed by a call within 48 hours"],
              "Wasted appointments for members, and some out-of-network bills that later become complaints (estimate).",
              "High, because the call volume and the search follow-up rate agree, and brokers report the same problem.",
              "Members looking for a new doctor or dentist, often after moving or a change of plan.",
              "Sample 100 directory listings and call them, to measure how many are wrong."),
        brief(6, "directory-surprise-bills", "directory errors turn into surprise bills", "broker team",
              "Employees see a provider the directory listed as in network, then receive an out-of-network bill.",
              "Trust that a listed provider is covered.",
              [f"\"My client's employee checked the directory, saw the specialist, and got a bill for the full amount.\" (broker escalation)",
               f"\"Every surprise bill turns into a complaint to the employer, then to me.\" (broker, in a quarterly review)",
               f"{num(brk['provider_directory_error_or_surprise_bill'])} broker escalations in the period were about directory errors or surprise bills ({pct(brk['provider_directory_error_or_surprise_bill'] / BROKER_ESCALATIONS_TOTAL)})"],
              "Each case usually ends in a complaint, and some in a refund or an exception payment (estimate).",
              "Medium, because escalations are solid but we do not know how many members pay a surprise bill without escalating.",
              "Employees of client companies who see specialists.",
              "Count the exception payments made for directory errors in the period."),
        brief(7, "telehealth-requests", "employers ask for telehealth", "HR account team",
              "Some employers ask whether the plan will add a telehealth service.",
              "Offer employees a quick way to see a doctor without leaving work.",
              [f"\"Our competitor's plan includes virtual visits. Can yours?\" (HR director, renewal meeting)",
               f"\"It would be nice for employees to have telehealth.\" (HR manager, quarterly review)",
               f"{emp['requested_telehealth']} of {EMPLOYERS_IN_REVIEW} employer groups reviewed asked about telehealth. {num(brk['telehealth_request_from_employer'])} broker escalations ({pct(brk['telehealth_request_from_employer'] / BROKER_ESCALATIONS_TOTAL)}) passed on the same request",
               f"Among members, telehealth was {pct(share['telehealth'])} of calls, and \"telehealth\" was searched {num(srch['telehealth'][0])} times in the period"],
              "Employers say it would help renewals; we have no evidence it moved any renewal (estimate).",
              "Low, because the request comes from employers and brokers, not from members, and member signals are small.",
              "HR teams at employer groups comparing plans at renewal.",
              "Ask members who used a virtual visit elsewhere what they used it for, before deciding anything."),
        brief(8, "mobile-app-rating", "the app has a poor rating", "broker team",
              "The member app has a low store rating, and some employers ask for a better app.",
              "Handle health plan tasks on the phone.",
              [f"\"Your app is 2.9 stars. Our employees notice.\" (HR director, passed on by the broker)",
               f"\"Rebuild the app and half these calls go away.\" (broker, in a quarterly review)",
               f"App store rating {APP_RATING} from {num(APP_REVIEWS)} reviews. In {pct(APP_LOW_REVIEWS_ABOUT_CLAIMS)} of the 1 and 2-star reviews, the complaint is about claim status, not about the app itself",
               f"{emp['requested_a_better_mobile_app']} of {EMPLOYERS_IN_REVIEW} employer groups reviewed asked for a better app"],
              "A low rating may hurt how employers see the plan at renewal (estimate).",
              "Medium, because the rating is solid, but the reviews point at claim information more than at the app.",
              "Members who use the app, and the employers who hear about it.",
              "Read 100 low-rated reviews and sort them by what is actually missing."),
        brief(9, "wellness-rewards", "some employers want a wellness rewards program", "HR account team",
              "A few employers ask for a wellness rewards program with points and challenges.",
              "Encourage employees to stay healthy and engaged with the plan.",
              [f"\"A step challenge with rewards would be a nice extra for our people.\" (HR manager, quarterly review)",
               f"\"Engagement is our theme this year. Could the plan help?\" (HR director, renewal meeting)",
               f"{emp['requested_a_wellness_rewards_program']} of {EMPLOYERS_IN_REVIEW} employer groups reviewed mentioned it. \"wellness rewards\" was searched {num(srch['wellness rewards'][0])} times in the period, and no member services contact reason covers it"],
              "None measured. Employers describe it as a nice extra.",
              "Low, because the only source is a minority of employers, and members show almost no interest.",
              "HR teams running employee engagement programs.",
              "Ask the employers who raised it whether they would choose a plan because of it."),
        brief(10, "digital-id-card", "the digital ID card works", "member services team",
              "Members find and use the digital member ID card without help.",
              "Show proof of coverage at a pharmacy or a doctor's office.",
              [f"\"Pulled it up on my phone at the pharmacy. Easy.\" (member feedback, post-call survey)",
               f"\"The only part of the app I never have trouble with is the ID card.\" (member call, summarized by the agent)",
               f"Only {pct(share['member_id_card'])} of member services calls were about the ID card. \"id card\" was searched {num(srch['id card'][0])} times, and only {pct(srch['id card'][1])} of those searches were followed by a call within 48 hours",
               f"{emp['praised_the_digital_id_card']} of {EMPLOYERS_IN_REVIEW} employer groups reviewed praised it without being asked"],
              "Positive: calls about ID cards dropped after the digital card launched (estimate; the before figure is not in this data).",
              "High, because calls, searches, and employer comments agree.",
              "All members.",
              "Keep it as it is, and use it as the pattern for how members want to find information."),
    ]
    return dict(out)


def main() -> None:
    files, s = generate()
    OUT.mkdir(parents=True, exist_ok=True)
    for name in list(OUT.iterdir()):
        name.unlink()
    for name, text in files.items():
        (OUT / name).write_text(text, encoding="utf-8")

    print(f"Wrote {len(files)} files to {OUT.relative_to(ROOT)}")
    print(f"  claims in period: {s['claims_total']:,}")
    print(f"  member services calls in period: {s['calls_total']:,}")
    for reason, n in s["calls"].items():
        print(f"    {reason}: {n:,} ({s['share'][reason]:.1%})")
    print(f"  claim-status calls per 1,000 claims: {s['claim_status_per_1000']:.1f}")
    print(f"  claims pended waiting for the member: {s['pended_total']:,} ({s['pended_share']:.1%})")
    print("  portal searches:")
    for term, (n, share) in s["searches"].items():
        print(f"    {term}: {n:,} (followed by a call: {share:.0%})")
    print(f"  broker escalations: {BROKER_ESCALATIONS_TOTAL:,}")
    for cat, n in s["broker"].items():
        print(f"    {cat}: {n:,} ({n / BROKER_ESCALATIONS_TOTAL:.1%})")
    print(f"  employer review themes (of {EMPLOYERS_IN_REVIEW} employers):")
    for theme, n in s["employers"].items():
        print(f"    {theme}: {n}")


if __name__ == "__main__":
    main()
