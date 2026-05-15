# Welcome Message

Display this message ONCE at the start of a new `aidlc-discovery` workflow invocation.

Do NOT display this message when resuming an existing session (session-continuity.md handles resume).

**Language**: display the banner in the user's detected language once `common/language-handling.md` has run. If detection has not run yet (very first turn of a new session), display in English — the detection stage runs next and will confirm. Keep the trigger word `ready` exactly as-is in the banner regardless of language; translated equivalents are accepted (see `language-handling.md` §"Special case — the trigger word").

---

## Message Template

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                        AI-DLC DISCOVERY                          ║
║              Define what to build before AI builds it            ║
║                                                                  ║
║  A role-based interview workflow that produces the two           ║
║  canonical inputs AI-DLC needs before Inception:                 ║
║                                                                  ║
║    1) Vision Document             (Business role)                ║
║    2) Technical Environment Doc   (Technical role)               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

How this works
──────────────
  • You pick a role: Business, Technical, or Both (sequential).
  • You pick a depth: Quick pass (~10 min) or Full interview (~25 min).
  • I ask questions in a markdown file, not in chat.
  • You fill in the [Answer]: tags.
  • When you're done with a batch, reply with a single word: ready
  • I re-read the file, validate, and move on.
  • Progress (X/N questions, time remaining) is shown at the top of every batch.
  • You can stop mid-way and resume later — state is saved per question.

Outputs land in
───────────────
  ./Product-Definition/
    ├── vision-document.md            ← Business output
    ├── technical-environment.md      ← Technical output
    ├── open-questions.md             ← Hand-off to AI-DLC
    ├── visual/  (optional)           ← User journey + HTML mockups
    └── interview/                    ← Process workspace (drafts, batches)

Let's get started.
```

After displaying the message, proceed to `session-continuity.md` to detect or create state.
