# Discovery Orchestrator Protocol

Single source of truth for the discovery flow. Simpler than AI-DLC's: near-linear with a parallel role stage.

## Flow

```
welcome → shared selection (project-type · depth · mode · interaction)
   ├─ product-discovery  (PM)
   └─ tech-discovery     (tech lead)      [run in parallel when mode = parallel]
   ▼
  JOIN (barrier): wait until both roles = complete
     → reconcile cross-role contradictions (vision ↔ constraints) into open-questions
   → [visual-sketch, opt-in] → handoff
```

## Steps

1. **Welcome + session detection.** New session → scaffold `Product-Definition/` per `conventions/state-schema.md`. Resume → read `state/session-index.md`; if the other role has an active session, work only in this role's lane.
2. **Shared selection** (once, before fan-out): project-type, depth (quick/full), mode (single | sequential | parallel), interaction (batch | conversational). Write shared fields to `session-index.md`.
3. **Role skills.** Run `product-discovery` and/or `tech-discovery`. Each presents questions per the chosen interaction mode (`conventions/question-format.md`) and is single-writer on its `<role>-state.md`. Per-skill flags: `human-clarification: true`, `plan-creation: false`, `artefact-verification: true` (the per-role approval gate). The gate follows the **Approval & adjust loop** in `conventions/question-format.md` — never advance to the next stage without an explicit Approve.
4. **Join barrier.** When a role completes, set its status in `session-index.md` and check the other. When both are `complete`, set `Join: ready` and run `open-questions` (consolidate + flag contradictions). On platforms with script execution, `scripts/process-checker.js` verifies the barrier deterministically.
5. **Visual sketch** (opt-in) → **handoff**: render the paste-ready handoff prompt per `conventions/handoff-format.md` — a localised instruction line plus an English, copy-clean fenced prompt that tells AI-DLC which `Product-Definition/` files to load, the open-questions count, and to resolve those questions before proceeding past Requirements Analysis.

## Builder / validator

Skills follow the generic v2 builder/validator pattern (the builder produces artifacts; the validator
checks `validation-spec.md`). Discovery does not redefine those protocols.
