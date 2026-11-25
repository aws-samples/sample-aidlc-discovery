## Running in Cowork

This build of the skill runs in Claude Cowork. The modules are written for several harnesses; this section says how their steps work here. It applies in every phase.

**Tools.** Where a module names a tool: `Read` reads a file, PDFs included (for Word files, use the docx skill if it is installed); `Write` and `Edit` save files; `Grep` and `Glob` search the working folder; `python3` in the shell does counts, aggregation, and weighted scores. Every artifact is a file, saved with `Write` or `Edit`. When a module says to copy a template exactly (the prototype shell, `compare.html`), do not retype it: extract the code block from the reference file with `python3` in the shell, write it to the new file, then change only the marked region with `Edit`. Check that everything outside the markers is unchanged.

**The working folder** is the folder the user connected to this session. Save `discovery/` there, never in your scratch outputs folder, which the team does not see. If no folder is connected, ask for one before Setup. The file tools and the shell see the same folder under different paths, and your session instructions give the mapping: use the file tool path with `Read`, `Write`, and `Edit`, and the shell path in Python. Keep scripts out of `discovery/`: run Python inline (`python3 - <<'EOF'`) or save the script in your scratch folder. Never delete a file in `discovery/`; a superseded file stays, and Cowork would ask the user first.

**This skill's folder.** `${CLAUDE_SKILL_DIR}` is this skill's folder as the file tools see it. Every `modules/...` and `cowork/...` path in this skill and its modules is relative to it. For the shell, translate it with the same mapping. If the shell cannot reach it, `Read` the file you need and `Write` a copy to your scratch folder, then run the copy.

**Question cards.** Each round still appears in chat in the format in "Asking the team", as the record. Then call `AskUserQuestion` with the questions of the round that have a small set of answers: at most four questions per call, two to four options each, the recommended answer first with "(Recommended)" after its label, and a header of at most 12 characters. The team can always type its own answer, so add no "Other" option. Write each question so it stands on its own: the dialog can hide the chat. Questions that need free text, such as the team's expectations before Signals, stay in chat. A round with more than four card questions takes several calls. In unattended runs, show no cards.

**Lookups in parallel.** Where "Asking the team" says to dispatch a sub-agent, use the `Agent` tool: give it the file paths and the one fact to find, and ask the rest of the round meanwhile.

**The journey app.** One Cowork artifact per project shows the whole of Discovery: the five phases and their status, every artifact rendered, the prototype versions clickable in place, the decision, and how many claims are Known, Assumed, or Needs evidence. It is generated from the files, so the files stay the record.

1. Render it in the shell: `python3 [skill folder]/cowork/journey.py [working folder]/discovery/{{project}}`, with shell paths. It writes `discovery/{{project}}/journey.html`.
2. Publish it. The first time, call `create_artifact` with id `discovery-{{project}}`, `html_path` set to the file tool path of `journey.html`, and a one-line description. After that, call `update_artifact` with the same id and a one-line `update_summary`, such as "Signals complete: top signal is rebooking after disruption". If `create_artifact` says the id exists, update it instead.
3. Do it after Setup, at the end of every phase together with the progress board, after each new prototype version, and when the team asks. Not after every file.
4. Before you render, keep `PROJECT.md`'s `## Phase status` current, in the format in Output: the progress board's table with its Key artifact column, and the three lists (What we know, What we don't know, What we're assuming). The app reads them from there; the chat alone does not reach it.
5. In chat, one line is enough: "Journey app updated: [what changed]."

If the script fails, say so in one line and carry on: Discovery does not depend on it. `screenshot_artifact` shows only the artifact open in the side panel; a failed screenshot of another one is not an error, so do not retry it.

**The prototype artifact.** Publish every new prototype version on its own as well, so the team can open it at full size: `create_artifact` for the first version, then `update_artifact`, with id `discovery-{{project}}-prototype` and `html_path` set to the new `prototype/v[N].html`. The shell works in the artifact view as it is: never edit it to make it fit. Then show the same file with `present_files`, so it also opens in the file preview, and refresh the journey app.

**Other HTML files** (`compare.html`, a survey or its dashboard): show them with `present_files`. Publish one as an artifact only when the team asks; an artifact can load no external scripts except the few that `create_artifact` lists.

**Unattended runs** follow the same steps without cards: render and publish the journey app at the end of every phase and the prototype artifact for every version, and record in `PROJECT.md` under `## Unattended choices` if publishing failed.

