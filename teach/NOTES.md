# Notes

- The user is the author of the method and the skills. Material is for **new facilitators** first, and for presentations.
- The workspace lives in `teach/` and is committed alongside `facilitator/`.
- Wants both short lessons with quizzes and printable reference sheets.
- Keep vocabulary aligned with `reference/glossary.html`, which follows the skills' own words (phase, step, checkpoint, artifact, Known / Assumed / Needs evidence).
- When the skills change, re-check `reference/phase-map.html` against `skills/*/SKILL.md` and `facilitator/run-sheet.md`.

## Lesson plan (draft)
1. The shape of the day: five phases, one spine (done)
2. Setup and Signals (done)
3. Working Backwards I: personas and scoring (done)
4. Working Backwards II: the five questions, PR/FAQ, readiness, PRD, riskiest assumption, GTM draft (done)
5. Prototype (done)
6. Validate (done)
7. Handoff and the follow-ups (done)
8. Interleaved review: the failure drill (done; with reference/recovery-card.html)
9. Running in a team Space (done)
10. Play the day (done): the six-room 16-bit role play, 19 moments, summary links misses to lessons. Grew from prototypes/rpg-office.prototype.html (variants B + C). To add a moment, append to ROOMS[r].moments; vary the good answer's position.

## Slide outline
`reference/slide-outline.md`: 20 slides, assertion headlines, Show/Say per slide, examples from the Air reference run. Keep it in step with the phase map.

## Components
- `assets/quiz.js`: multiple choice with feedback.
- `assets/scorer.js`: weighted-score exercise (scores, confidence → learner enters score and decision).

## Known spread
Air answer key (`facilitator/anycompany-air.md` §4) expects rebooking 4.45 and booking flow 2.50 (defer); the reference run has 4.60 and 2.20 (drop). Lesson 0003 tells facilitators to judge runs on decisions, not exact scores.

## Repository changes absorbed
- 2026-10-29, up to ef30e61: team Space skill (lesson 0009, phase map, glossary, recovery card, slide 6b), new install path (Customize, Skills, Create, From folder), eleven job skills, new run-sheet facilitator practices, and the `anycompany-air-with-team` reference run (used as "with a team" examples in 0003–0005 and the slide outline).

## Next sessions
All eight planned lessons exist. Next: ask the user for quiz scores per lesson, write learning records from them, and build spaced review on what slipped. Offer role-play rehearsals (each lesson's "Ask your teacher" box).
