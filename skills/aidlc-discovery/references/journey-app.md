# The journey app

One page per project, `discovery/{{project}}/journey.html`, that the room can follow: the five phases and their status, a **Now** banner with the step the team is on and what comes next, every artifact rendered from its file, the prototype versions clickable in place, the decision with its conditions, and how many claims are Known, Assumed, or Needs evidence. It is generated from the files, so the files stay the record. The update also keeps the `Now:` line in `PROJECT.md`, which is how a new chat knows the step to resume at.

## Create it once, after Setup

1. Load `references/journey-shell.md` with `file_read`, and save its HTML code block to `discovery/{{project}}/journey.html` with `file_write`, exactly as it is. Never retype it from memory, shorten it, or reformat it.
2. Run the update below, with Now set to Setup.
3. Open `journey.html` with `open_in_session_tab`. Then tell the team in one line: "To put the journey on the room's screen, open `discovery/{{project}}/journey.html` from the working folder in a browser. Reload the page to see the latest step."

## Update it at every step

Run the update with `run_python`:

- at the start of every step of a module (each `### Step` heading), with Now set to that step;
- after each checkpoint, with the progress board, and after each new prototype version;
- when the team asks;
- when Discovery resumes in a new chat: run it, then open `journey.html` again as in step 3 of "Create it once".

The update is silent: say nothing about it in chat. At a checkpoint, also open `journey.html` again with `open_in_session_tab`, so the session tab shows the new version.

Before you run it, fill in:

- `PROJECT`: the project folder, `discovery/{{project}}` in the working folder, as Python sees it.
- `NOW`: `phase` is Setup, Signals, Working Backwards, Prototype, Validate, or Handoff, always in English. `step` is the step, such as "Step 2 of 6: find and check the data". `doing` is one sentence on what the team is doing or deciding now, such as "The team checks the data inventory before any analysis." `next` is the next step. Write `step`, `doing`, and `next` in the project language, with no customer names or quotes.

If it stops with "copy the shell again", do step 1 of "Create it once" again, then run the update again. If it fails a second time, say so in one line and carry on: Discovery never waits for the journey app.

In unattended runs, update it only at the end of every phase, with Now set to the phase just finished.

```python
import datetime, hashlib, json, pathlib, re

PROJECT = pathlib.Path("discovery/[project]")  # the project folder, as Python sees it
SHELL = None  # where references/journey-shell.md is, if Python can read it; None otherwise
NOW = {"phase": "Signals", "step": "[step]", "doing": "[what the team is doing now]", "next": "[the next step]"}

SHAPE = "7f70f3714d46"
DATA = re.compile(r'(<script id="journey-data" type="application/json">)(.*?)(</script>)', re.S)
page_file = PROJECT / "journey.html"
page = page_file.read_text(encoding="utf-8") if page_file.is_file() else ""
shape = "\n".join(line.rstrip() for line in DATA.sub(r"\1\3", page).strip().splitlines())
if hashlib.sha256(shape.encode()).hexdigest()[:12] != SHAPE:
    if not SHELL:
        raise SystemExit("journey.html is missing or is not the shell: copy the shell again")
    page = re.search(r"```html\n(.*)\n```", pathlib.Path(SHELL).read_text(encoding="utf-8"), re.S).group(1)
stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
pm = PROJECT / "PROJECT.md"
if pm.is_file():  # keep the Now line in PROJECT.md, so a new chat can resume at this step
    text, line = pm.read_text(encoding="utf-8"), f"Now: {NOW['phase']}, {NOW['step']}. Next: {NOW['next']}. Updated {stamp}."
    for where in (r"^Now: .*$", r"^Project language: .*$", r"^# .*$"):  # replace the line, or add it after one of these
        text, n = re.subn(where, lambda m: line if m.group(0).startswith("Now: ") else m.group(0) + "\n" + line, text, count=1, flags=re.M)
        if n:
            break
    pm.write_text(text, encoding="utf-8")
files = {}
for f in sorted(PROJECT.rglob("*")):
    rel = f.relative_to(PROJECT).as_posix()
    if f.is_file() and (f.suffix == ".md" or re.fullmatch(r"prototype/(v\d[^/]*|index)\.html", rel)):
        files[rel] = f.read_text(encoding="utf-8")
data = {"project": PROJECT.name, "updated": stamp, "now": NOW, "files": files}
blob = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
page_file.write_text(DATA.sub(lambda m: m.group(1) + blob + m.group(3), page, count=1), encoding="utf-8")
print(f"Journey app updated: {len(files)} files, {page_file.stat().st_size // 1024} KB")
```
