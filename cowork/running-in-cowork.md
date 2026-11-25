## Running in Cowork

This build of the skill runs in Claude Cowork. The modules are written for several harnesses; this section says how their steps work here. It applies in every phase.

**Tools.** Where a module names a tool: `Read` reads a file, PDFs included (for Word files, use the docx skill if it is installed); `Write` and `Edit` save files; `Grep` and `Glob` search the working folder; `python3` in the shell does counts, aggregation, and weighted scores. Every artifact is a file, saved with `Write` or `Edit`. When a module says to copy a template exactly (the prototype shell, `compare.html`), do not retype it: extract the code block from the reference file with `python3` in the shell, write it to the new file, then change only the marked region with `Edit`. Check that everything outside the markers is unchanged.

**The working folder** is the folder the user connected to this session. Save `discovery/` there, never in your scratch outputs folder, which the team does not see. If no folder is connected, ask for one before Setup. The file tools and the shell see the same folder under different paths, and your session instructions give the mapping: use the file tool path with `Read`, `Write`, and `Edit`, and the shell path in Python. Keep scripts out of `discovery/`: run Python inline (`python3 - <<'EOF'`) or save the script in your scratch folder. Never delete a file in `discovery/`; a superseded file stays, and Cowork would ask the user first.

**This skill's folder.** `${CLAUDE_SKILL_DIR}` is this skill's folder as the file tools see it. Every `modules/...` and `cowork/...` path in this skill and its modules is relative to it. For the shell, translate it with the same mapping. If the shell cannot reach it, `Read` the file you need and `Write` a copy to your scratch folder, then run the copy.

**Question cards.** Each round still appears in chat in the format in "Asking the team", as the record. Then call `AskUserQuestion` with the questions of the round that have a small set of answers: at most four questions per call, two to four options each, the recommended answer first with "(Recommended)" after its label, and a header of at most 12 characters. The team can always type its own answer, so add no "Other" option. Write each question so it stands on its own: the dialog can hide the chat. Questions that need free text, such as the team's expectations before Signals, stay in chat. A round with more than four card questions takes several calls. In unattended runs, show no cards.

**Lookups in parallel.** Where "Asking the team" says to dispatch a sub-agent, use the `Agent` tool: give it the file paths and the one fact to find, and ask the rest of the round meanwhile.

**The journey app** (see `references/journey-app.md`) works the same way here, with three differences:

1. Never copy the shell by hand. Set `SHELL` in the update to `${CLAUDE_SKILL_DIR}/references/journey-shell.md`, with the shell path, and the update writes `journey.html` from it when the file is missing or changed. `PROJECT` is the project folder, also with the shell path.
2. Show it with `present_files`, after Setup and at the end of every phase. Do not publish it as an artifact: Cowork asks the user to approve every artifact call. The room follows every step in the browser view of `journey.html` (see `references/journey-app.md`).
3. Before an update at the end of a phase, keep `PROJECT.md`'s `## Phase status` current, in the format in Output: the progress board's table with its Key artifact column, and the three lists. The app reads them from there; the chat alone does not reach it.

**Prototypes.** Show every new version with `present_files`, so it opens in the file preview, then update the journey app, which holds every version, clickable in place. The shell works in the preview as it is: never edit it to make it fit.

**Artifacts only when the team asks.** Cowork asks the user to approve every `create_artifact` and `update_artifact` call, so never publish one on your own. When the team asks for one (the journey, a prototype, `compare.html`, a survey dashboard), say that Cowork will ask to approve it, and each later update too. Give it an id of its own, `discovery-{{project}}-[what]-[YYYYMMDD-HHMM]`, because Cowork keeps artifacts across tasks and folders; record it in `PROJECT.md` on one line after `Project language:` (`Cowork artifacts: [id], ...`), so a new task updates the same one. If `create_artifact` says an id exists, it belongs to another run: never update it; add `-2`. An artifact can load no external scripts except the few that `create_artifact` lists; `screenshot_artifact` shows only the artifact open in the side panel.

**Other HTML files** (`compare.html`, a survey or its dashboard): show them with `present_files`.

**Unattended runs** follow the same steps without cards and without `present_files`: update the journey app at the end of every phase, and publish no artifact.

