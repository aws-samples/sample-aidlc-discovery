## Running in Cowork

This build of the skill runs in Claude Cowork. The modules are written for several harnesses; this section says how their steps work here. It applies in every phase.

**Tools.** Where a module names a tool: `Read` reads a file, PDFs included (for Word files, use the docx skill if it is installed); `Write` and `Edit` save files; `Grep` and `Glob` search the working folder; `python3` in the shell does counts, aggregation, and weighted scores. Every artifact is a file, saved with `Write` or `Edit`. When a module says to copy a template exactly (the prototype shell, `compare.html`), do not retype it: extract the code block from the reference file with `python3` in the shell, write it to the new file, then change only the marked region with `Edit`. Check that everything outside the markers is unchanged.

**The working folder** is the folder the user connected to this session. Save `discovery/` there, never in your scratch outputs folder, which the team does not see. If no folder is connected, ask for one before Setup. The file tools and the shell see the same folder under different paths, and your session instructions give the mapping: use the file tool path with `Read`, `Write`, and `Edit`, and the shell path in Python. Keep scripts out of `discovery/`: run Python inline (`python3 - <<'EOF'`) or save the script in your scratch folder. Never delete a file in `discovery/`; a superseded file stays, and Cowork would ask the user first.

**This skill's folder.** `${CLAUDE_SKILL_DIR}` is this skill's folder as the file tools see it. Every `modules/...` and `cowork/...` path in this skill and its modules is relative to it. For the shell, translate it with the same mapping. If the shell cannot reach it, `Read` the file you need and `Write` a copy to your scratch folder, then run the copy.

**Question cards.** Each round still appears in chat in the format in "Asking the team", as the record. Then call `AskUserQuestion` with the questions of the round that have a small set of answers: at most four questions per call, two to four options each, the recommended answer first with "(Recommended)" after its label, and a header of at most 12 characters. The team can always type its own answer, so add no "Other" option. Write each question so it stands on its own: the dialog can hide the chat. Questions that need free text, such as the team's expectations before Signals, stay in chat. A round with more than four card questions takes several calls. In unattended runs, show no cards.

**Lookups in parallel.** Where "Asking the team" says to dispatch a sub-agent, use the `Agent` tool: give it the file paths and the one fact to find, and ask the rest of the round meanwhile.

**The journey app** (see `references/journey-app.md`) works the same way here, with three differences:

1. Never copy the shell by hand. Set `SHELL` in the update to `${CLAUDE_SKILL_DIR}/references/journey-shell.md`, with the shell path, and the update writes `journey.html` from it when the file is missing or changed. `PROJECT` is the project folder, also with the shell path.
2. Publish it as an artifact, with the ids in "Artifact ids" below. After the first update, call `create_artifact` with the journey id, `html_path` set to the file tool path of `journey.html`, and a one-line description. Then call `update_artifact` with the same id and a one-line `update_summary`, such as "Signals complete: top signal is rebooking after disruption", only at the end of every phase (with the progress board), after each new prototype version, and when the team asks. Cowork asks the user to approve every artifact call, so never call it at every step: within a phase, the update rewrites `journey.html` alone, and the browser view of that file (see `references/journey-app.md`) follows every step without asking anything.
3. Before an update at the end of a phase, keep `PROJECT.md`'s `## Phase status` current, in the format in Output: the progress board's table with its Key artifact column, and the three lists. The app reads them from there; the chat alone does not reach it.

**Artifact ids.** Cowork keeps artifacts across tasks and folders, so a plain `discovery-{{project}}` may already belong to an earlier run. Each project gets its own ids, made once and kept in `PROJECT.md`:

- The first time you publish for a project, take the date and time now and make the ids `discovery-{{project}}-[YYYYMMDD-HHMM]` for the journey and the same with `-prototype` for the prototype. Write them in `PROJECT.md` on one line after `Project language:`: `Cowork artifacts: [journey id], [prototype id]`.
- When Discovery continues, in this task or a new one, read the ids from that line and use `update_artifact`. Create one only when the line names no id for it yet.
- If `create_artifact` says an id exists, it belongs to another run: never update it. Add `-2` (or the next free number) to the id, create it, and record the new id in `PROJECT.md`.

`screenshot_artifact` shows only the artifact open in the side panel; a failed screenshot of another one is not an error, so do not retry it.

**The prototype artifact.** Publish every new prototype version on its own as well, so the team can open it at full size: `create_artifact` for the first version, then `update_artifact`, with the prototype id (see "Artifact ids") and `html_path` set to the new `prototype/v[N].html`. The shell works in the artifact view as it is: never edit it to make it fit. Then show the same file with `present_files`, so it also opens in the file preview, and update the journey app.

**Other HTML files** (`compare.html`, a survey or its dashboard): show them with `present_files`. Publish one as an artifact only when the team asks; an artifact can load no external scripts except the few that `create_artifact` lists.

**Unattended runs** follow the same steps without cards: update and publish the journey app at the end of every phase and publish the prototype artifact for every version, and record in `PROJECT.md` under `## Unattended choices` if publishing failed.

