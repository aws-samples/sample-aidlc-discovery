# Persona document

Save each persona as its own file, `discovery/[project]/working-backwards/personas/[given-name].md`, with the given name in lowercase ASCII, romanized if the name is not in Latin script. The first line is the persona's name; the brief and AI-DLC's team knowledge use it as written.

```markdown
# [Name]
**Tagline:** [The descriptive label, in one sentence]
**Confidence:** HIGH | MEDIUM | LOW

## Identity
- **Age:** [Range]
- **Location:** [City/Region]
- **Background:** [Nationality or culture] (from the data) | (from the data's market, **Assumed**) | (from the company's home market, **Assumed**) | (from the project language, **Assumed**)
- **Occupation:** [Job Title]
- **Bio:** [2-3 sentences background story]

## Goals & Motivations
- **Primary Goal:** [Clear, one sentence]
- **Secondary Goals:** [List]
- **Definition of Success:** [What success means for this person]
- **Deeper Motivation:** [Emotional driver]

## Pain Points
- **Challenges:** [List with context]
- **Blockers:** [What prevents them from reaching their goals]
- **Workarounds:** [How they currently cope]
- **Emotional Impact:** [How it feels]

## Behavior
- **Current Solutions:** [What they use today]
- **Tools:** [List]
- **Frequency:** Daily | Weekly | As needed
- **Tech Affinity:** Low | Medium | High
- **Decision Style:** Data-driven | Gut feeling | Consensus | Research-heavy

## Context & Environment
- **Usage Context:** [When and where]
- **Devices:** [List]
- **Time Pressure:** [How much time the person has]
- **Influencers:** [Who influences their decisions]

## Quotes
> [Customer quote, written as the project language rule says]
> [Another customer quote, written the same way]

## Scenario
**[Title]**
[3-4 sentences showing how this person typically acts.
Trigger → Action → Thought process → Desired outcome.]

## Communication Style
- **Tone:** [Formal | Casual | Direct | Diplomatic]
- **Speech Patterns:** [Typical phrases, vocabulary level]
- **Frustration Signals:** [How they express anger]
- **Enthusiasm Signals:** [How they express joy]
```

## Rules

1. **Real quotes only.** Every quote is copied verbatim from the feedback or a Signal Brief, with identifiers replaced by a bracketed role, as the entry skill's Shared rule 3 says. Never invent one.
2. **Evidence count.** Under the tagline, add `**Based on:** [N] feedback items` or `[N] Signal Briefs`.
3. **Confidence.** High: five or more items. Medium: two to four. Low: one item, or inferred. On a synthetic dataset, never higher than Medium.
4. **No real people.** Names are invented; nothing identifies a real customer.
