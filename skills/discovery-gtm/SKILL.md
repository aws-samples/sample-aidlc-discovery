---
name: discovery-gtm
display_name: "AI-DLC Discovery: Go-to-market"
icon: "📣"
description: "Go-to-market section for AI-DLC Discovery: drafts first adopters, positioning, business model, and launch plan in Working Backwards, then completes the viability check and the adoption and success table in Validate. Use when the user asks who adopts first, how to position the idea, how adoption will be measured, or wants the GTM or adoption plan."
trigger: "gtm go-to-market adoption positioning"
patterns:
  - pattern: '(?i)\b(?:go-to-market|gtm|adoption plan|positioning)\b'
    confidence: 0.85
  - pattern: '(?i)\bwho (?:adopts|uses) (?:it|this) first\b'
    confidence: 0.80
inputs:
  - name: project
    description: "Project folder name under discovery/."
    type: string
    required: true
  - name: mode
    description: "draft (Working Backwards: parts 1, 2, 3, 5) or complete (Validate: parts 4, 6, 7)."
    type: string
    default: draft
tools: [file_read, file_write]
version: "3.0.0"
license: MIT-0
---

# AI-DLC Discovery: Go-to-market

## Overview

The GTM section answers: if we build it, who uses it first, how do we describe it, and how will we know it worked? Every Discovery brief has one. Working Backwards drafts it in about 10 minutes, from the press release and the signals. Validate completes it in about 10 more: the viability check and the adoption and success table, with targets the follow-ups check. Parts marked required are finished on the day; the rest are hypotheses with an owner and a date.

## Workflow

### Step 1: Draft (mode `draft`)
- **Mode**: `agentic`
- **Input**: `working-backwards/prfaq.md`, the personas, the Signal Analysis Report (including the alternatives customers use today)
- **Output**: `discovery/{{project}}/working-backwards/gtm.md` with parts 1, 2, 3, and 5
- **Validate**: First adopters name a segment and two or three design partners; the positioning line names the main alternative
- **On failure**: If the team has no design partners in mind, write the profile of one and mark it Needs evidence

Write:

1. **First adopters** (required). The segment that adopts first and roughly how many users or accounts it covers; how the team reaches them (in product, sales, customer success, partners); and two or three design partners. Use roles, not personal names.
2. **Positioning** (required). One line, taken from the press release:
   > For **[segment]** who **[problem]**, **[product or feature]** is a **[category]** that **[benefit]**. Unlike **[the main alternative, including doing nothing or a spreadsheet]**, it **[differentiator]**.

   Every claim points to evidence from Signals. If the honest alternative is doing nothing, the benefit has to beat the cost of changing; say so.
3. **Business model and pricing** (hypothesis). Included to drive retention, an upgrade or add-on, or a new product; the pricing hypothesis and any willingness-to-pay evidence; and for an AI feature, the cost to serve per active user per month and whether the price or the retention gain covers it.
5. **Launch plan** (hypothesis). Internal use, design partners, limited release, general availability, with what each stage needs to exit, and the enablement sales and support need before the limited release.

Leave parts 4 and 6 as "to complete in Validate".

### Step 2: Complete (mode `complete`)
- **Mode**: `agentic`
- **Input**: `gtm.md`, `validate/risk-review.md`, `prototype/persona-critique.md`
- **Output**: `gtm.md` with parts 4, 6, and 7
- **Validate**: Every viability area has an owner role and a concern or "none"; the adoption table has a baseline, targets, and kill criteria
- **On failure**: If the business metric has no baseline, record "baseline needed by the 7-day follow-up" and who gets it

4. **Viability check** (required). For each area, an owner role and the main concern, or "none":

   | Area | Question |
   |------|----------|
   | Legal and compliance | Does it touch regulated data, contracts, or terms of service? |
   | Privacy and security | What customer data does it use, and does it leave its current boundary? |
   | Sales | Can the sales team explain and sell it, and does it change existing deals? |
   | Support and success | What new questions will support get, and who answers them? |
   | Marketing | Is there a story to tell, and does it fit the brand? |

6. **Adoption and success** (required):

   | Item | Content |
   |------|---------|
   | Adoption owner | A named role on the product engineering team, not marketing |
   | Adoption metric | For example, weekly active users of the feature as a share of the target segment |
   | Leading indicators | Early signs that adoption is on track |
   | Business metric | The metric agreed at setup, with its baseline |
   | AI quality (AI features only) | The AI quality target from the success criteria, measured on the PRD's evaluation cases |
   | Targets | At 30, 60, and 90 days after launch |
   | Kill criteria | The result after launch that means the idea did not work and the team stops |

7. **Risks and open hypotheses.** The GTM assumptions Validate could not confirm, as named questions.

Then update the status line of **all seven parts**, including parts 1, 2, 3, and 5 drafted in Working Backwards: **validated** when Validate supported it, **open** when it did not settle it. No part stays "draft" after this step, so check every heading before you finish.

## Output

`discovery/{{project}}/working-backwards/gtm.md`, with the seven parts as headings. Mark each part **required** or **hypothesis**, and its status: draft, validated, or open.

## Lessons Learned

### Do
- Take the positioning from the press release, so the two stay consistent.
- Name real design partners when the team can.
- Put the adoption owner on the product engineering team.

### Don't
- Spend more than 10 minutes on the draft; it is completed in Validate.
- Write pricing as a decision; it is a hypothesis with an owner.
- Leave "do nothing" out of the alternatives.

### Common Failures
- **No baseline for the business metric.** Record who will get it by the 7-day follow-up.
- **Kill criteria that never trigger.** Make them a specific number by a specific date.
- **The viability check is all "none".** Ask the room again, area by area; in regulated industries, check legal and privacy first.

### When to Ask the User
- Who owns adoption.
- Which design partners the team would really call.
- Whether a viability concern is serious enough to change the decision.
