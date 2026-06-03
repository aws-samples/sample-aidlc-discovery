# How to use AI-DLC Discovery

End-to-end walkthrough of a v2 session. Install first — see [install.md](install.md); architecture in [README.md](README.md).

## Invocation

- **Kiro:** `start aidlc-discovery`
- **Claude Code / Cowork:** `/aidlc-discovery` (or `start aidlc-discovery`)
- **Amazon Quick:** `start aidlc-discovery`

You can hand over your idea in the same message. Example used throughout this guide:

```
start aidlc-discovery. Ideation Portal: A digital platform that enables employees to submit innovative
ideas for transparent evaluation, scoring, and recognition to foster a culture of innovation within the
organization.

- A user-friendly submission interface with structured idea input fields and draft saving functionality.
- A robust evaluation framework with quantifiable metrics (feasibility, impact, innovation) enabling
  independent assessment by authorized panel members.
- Secure, role-based access allowing panel members to independently review and score submitted ideas
  across multiple evaluation dimensions.
- Real-time dashboards and leaderboards displaying aggregated panel scores with multi-dimensional views.
- Analytics highlighting top-performing ideas and detailed comparative analysis across criteria.
- A recognition system to formally acknowledge and reward the three highest-scoring ideas.
```

**Pre-load context (optional).** Prefix your invocation to give the agent sources to draw from — it will propose answers from them (you still review at the gate):

- **Files:** *"Read ./docs/vision.md and ./package.json first, then start aidlc-discovery."*
- **MCP:** *"Use the Confluence MCP to pull the 'Platform Architecture' page, then start aidlc-discovery."*

**On-demand stages.** Ask any time for *"make a visual sketch"* or to *"show the AI-DLC handoff prompt"*.

## The flow

1. **Welcome + session detection.** A new session scaffolds `Product-Definition/`; an existing one resumes where you left off (reads `state/session-index.md`).
2. **Shared selection (once, before the roles).** The tool asks four things:
   - **Project type** — brand-new / feature on existing / migration (plain language; maps to greenfield/brownfield internally).
   - **Depth** — Quick (~10 min, `[CORE]` questions) or Full (~25–35 min, every section).
   - **Mode** — single · sequential · parallel (PM ∥ tech lead in separate sessions).
   - **Interaction** — `batch` (questions written to a file, you fill `[Answer]:` and reply `ready`) or `conversational` (asked one at a time in chat).
3. **Role interviews.** Business (PM → `vision-document.md`) and Technical (tech lead → `technical-environment.md`).
   - Give a rich prompt like the one above and the tool **pre-fills** answers for you to review.
   - **Approval & adjust gate:** choose **Approve** or **Request changes**. It **never advances without an explicit Approve**. On "request changes" it applies your edit, re-shows it, and re-asks (batch: edit the file + `ready`; conversational: say the change in chat).
   - Every validated answer is appended to `*-answers-history.md` (nothing is lost) and tracked in `*-state.md`.
4. **Join.** When both roles are complete, the tool consolidates `open-questions.md` and flags any contradiction between the vision and the technical constraints.
5. **Visual Sketch (opt-in).** Five short questions → a Mermaid user journey + self-contained HTML mockups under `visual/`. Default is to skip.
6. **Handoff.** A paste-ready prompt (in English) telling AI-DLC which `Product-Definition/` files to load and to resolve the open questions first; the visual files are referenced automatically when the sketch exists.

## What the Ideation Portal example yields

From that single prompt, the Business interview pre-fills (Quick pass), e.g.:

- **Q1 name/type** → Ideation Portal — new internal platform.
- **Q2 users** → employees who submit ideas + an authorised evaluation panel.
- **Q14 MVP IN** → structured submission form, multi-dimensional scoring (feasibility/impact/innovation), role-based access, real-time leaderboard, analytics, top-3 recognition.

You review, adjust anything, approve → Technical interview → join → handoff. Output:

```
Product-Definition/  vision-document.md · technical-environment.md · open-questions.md · [visual/]
```

## Side-flows

- **Resume:** re-invoke in the same folder; the tool reads `state/session-index.md` and continues from the next unanswered question.
- **Change an answer:** at any gate pick **Request changes**; in `batch` mode you can also edit `*-questions.md` and reply `ready`.
- **Hand off to AI-DLC:** copy the paste-ready block from the final handoff into your AI-DLC session at the start of Requirements Analysis.

## Per platform

Behaviour is identical across Kiro, Claude Code/Cowork, and Amazon Quick — only the **question transport** differs (file `[Answer]:` vs. conversational chat). Install and reference tables: [install.md](install.md).
