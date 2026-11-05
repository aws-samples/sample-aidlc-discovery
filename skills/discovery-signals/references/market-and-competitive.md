# Market and Competitive Analysis

## Purpose
Extract actionable signals from market research documents (PDF, DOCX, Excel, Markdown): trends, competitive signals, behavior shifts, opportunities, and their connection to VoC findings.

---

## System Prompt
```
You are a strategic market analyst extracting actionable intelligence from research documents.
```

## User Prompt Template
```
Analyze this market research document and extract key signals:

DOCUMENT: {document_content}

Provide:
1. **Key Market Trends**: What's changing in the market?
2. **Competitive Signals**: What are competitors doing?
3. **Customer Behavior Shifts**: How is customer behavior evolving?
4. **Opportunity Areas**: Where are the gaps?
5. **Threats**: What should we be worried about?
6. **Data Points**: Specific numbers, percentages, statistics worth noting
7. **Relevance to VoC**: How do these signals connect to our customer feedback?
```

---

## Competitor material

When the location holds competitor material (reports, feature lists, pricing pages, a market research CSV), also extract:

1. **Landscape:** each competitor's strengths, weaknesses, strategy, and threat level (high, medium, low).
2. **Feature comparison:** capabilities the product has or lacks against each competitor.
3. **Gaps:** what the product is missing, who has it, the customer impact, and how urgent it is.
4. **Alternatives customers use today,** including spreadsheets and doing nothing. The GTM positioning needs them.

Every competitive claim needs a source. If a claim cannot be backed up, mark it Assumed.

## Output

Fold the findings into the Signal Analysis Report: connect each market or competitive finding to the customer signals it confirms or contradicts, and list the alternatives under the signal they relate to. When the team asks for a separate report, save it as `discovery/[project]/signals/market-and-competitive.md`.
