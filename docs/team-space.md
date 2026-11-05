# Design: a team Space for collaborative workshops

Status: built as the optional `discovery-team-space` skill (Amazon Quick only). Checks 1 and 2 below are still to run with a second person.

## Problem

Today one Amazon Quick Desktop runs the workshop and every artifact lives in that laptop's working folder. The rest of the team watches a shared screen. Nobody else can open the PR/FAQ, click through the prototype on their own phone view, ask a question about the signals, or take over facilitation without moving the folder. Pods in one room each need their own laptop and folder, and their work never meets.

## What Amazon Quick can do

Verified in Quick Desktop on 29 October 2026, with a Space attached to the chat (the chat's **+** menu, then **Spaces**):

| Check | Result |
|-------|--------|
| Write a file to the Space from a chat | Works. Quick also keeps a local copy |
| Save the same file again | Replaces it, with the same document ID: no duplicates |
| Folder paths, for example `discovery/x/signals/notes.md` | Kept, folders created as needed |
| Read a file back word for word | Works right away; search indexing follows a moment later |
| An HTML prototype saved to the Space | Opens and works in the session tab. Opened from the Space in a browser, it downloads |
| The data in the Space | Works: a chat copied the sample (11 files, before the telemetry was added) into the Space at the same paths, and Signals, run from the Space only, read every record (400 records, exact counts per source) |

Not yet verified:

1. How soon a second person, in their own Quick with the Space attached, sees a change.
2. Whether a Viewer can write, or only Owners. The documentation says Owners upload and Viewers view, query, and download.

## Proposal

**The team Space becomes the working folder.** At setup the team chooses where the workshop is saved: a local folder (today's default) or a team Space. With a Space, every artifact is written to and read from the same `discovery/[project]/` paths inside it. Everyone attaches the Space in their own Quick.

```text
Team Space: anycompany-air-discovery
└── discovery/
    └── anycompany-air/            PROJECT.md, signals/, working-backwards/, prototype/, validate/, handoff/
```

### One driver at a time

Saving replaces files, so two people writing the same workshop at once would overwrite each other. The skill enforces one driver:

1. `PROJECT.md` gets a line: `Driver: [role or name], since [date and time]`.
2. Before it writes anything, the skill reads `PROJECT.md` from the Space. If the driver is someone else, it stops and asks: "[Driver] is driving this workshop. Take over?" Taking over updates the line.
3. Anyone else can attach the Space and read, ask questions ("what did the persona critique find?"), and open the prototype in their session tab, without writing.

Hand-over uses the resume prompt that already works: "Continue the AI-DLC Discovery workshop for [project] from discovery/[project]/PROJECT.md in the [Space] space. I'm taking over. Start at [step]."

### Pods

Each pod is its own project in the same Space, `discovery/[project]-[pod]/`, with its own driver. Pods never write to each other's files, and the facilitator sees all of them in one place. At the readout, each pod's brief is one click away.

### Customer data in the team Space

Everything in a Space is queryable by everyone it is shared with. Sample data is fictional and can go in the Space: the guides copy it in at setup. Real customer data goes in the team Space only if the Space is shared with nobody who should not see it; the skill asks the team to confirm, and records the answer in `PROJECT.md`. Otherwise:

- The data stays where it is today: `discovery/data/` in the driver's local folder, or a separate, restricted data Space named in `data_location`.
- Only artifacts go into the team Space, and artifacts already carry anonymized quotes only. The skill checks for emails, names, and account identifiers before each write, as the end-to-end tests do.
- Handoff no longer writes `.gitignore` in Space mode; next-steps says to copy the artifacts, not the data, into the build repository.

### What changes in the skill

| Where | Change |
|-------|--------|
| `config.default.md` | `storage: local \| space` and `space_name` |
| Setup (`aidlc-discovery`) | Opt-in: the team asks for it ("save the workshop in our team Space") or sets `storage: space`; nothing is asked otherwise. The team creates and names the Space; the skill uses the one attached to the chat and checks it with a test write of `PROJECT.md` before Signals |
| Shared rules | "Write through the storage": every artifact path is relative to the folder or the Space. Read `PROJECT.md` and check the driver before every write |
| Prototype | Save versions to the Space; open them in the session tab from the Space copy. `compare.html` has the same limit as today in the session tab (frames cannot load sibling files) |
| Handoff | Space mode: no `.gitignore`; next-steps says how to export the artifacts from the Space to the build repository |
| Facilitator material | Run-sheet: "Before the day" creates the Space and shares it with the team as Owners (or Viewers, depending on check 2); a "Run it with a team Space" section in the Workshop Studio pages |

### What does not change

The method, the phases, the files and their paths, the checkpoints. The local folder stays the default, so self-serve runs, samples, and the automated tests (Claude Code has no Spaces) work as today. Space mode is tested by hand in Quick, and `TESTING.md` says so.

## Open questions

1. **Second user** (check 1 above): does a teammate's Quick see the driver's last write within seconds? If not, the take-over step must say to wait, or re-read.
2. **Who can write** (check 2): if only Owners, the facilitator shares the Space with the room as Owners, or the team accepts that only the driver writes.
3. **Limits**: file size and file count in a Space, and whether a 30 KB HTML file stays usable after indexing.
4. **Deleting**: set-aside personas and dropped versions are never deleted today; confirm nothing in the flow needs a delete in the Space.

## Plan

1. Run checks 1 and 2 with a colleague.
2. Build `storage: space` in the skill, behind the setup question, local stays the default.
3. Run the AnyCompany Air dry run with two people in one Space: one drives Kickoff and Signals, the other takes over for Working Backwards.
4. Update the run-sheet, the train-the-trainer guide (teams could each use one Space), and the Workshop Studio pages.
