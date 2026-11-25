"""Bundle the separate skills under skills/ into one installable AWS Quick skill.

The repository keeps one folder per skill, so each job is easy to edit and test.
Installed, they become a single skill, `aidlc-discovery`: the entry skill's
SKILL.md plus a module per job under modules/, loaded only when its step runs.

Usage: python3 scripts/build.py [output_dir]                  AWS Quick (default: dist/aidlc-discovery)
       python3 scripts/build.py --target cowork [output_dir]  Claude Cowork (default: dist/cowork/aidlc-discovery)
       --release                                             a release build: no development stamp

A build from anything but a clean checkout of the release tag says so at the end of the
skill's description, for example "Development build f149ce5 of 3.0.0.", so `List my skills`
shows which build is installed. The version fields stay X.Y.Z.

The AWS Quick build writes aidlc-discovery-v<version>.zip next to the output folder.
The Cowork build is the skill folder itself, with the tool names, paths, and steps
rewritten for Cowork (see COWORK_REWRITES and cowork/), and writes
aidlc-discovery-v<version>.skill next to it: Cowork installs a .skill file in one click.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
ENTRY = "aidlc-discovery"
PACKAGE_FILES = ["plugin.json", "mcps.json", "tasks.json", "LICENSE", "README.md"]
REPO_URL = "https://github.com/aws-samples/sample-aidlc-discovery/blob/main/"
COWORK = ROOT / "cowork"
TARGETS = ("quick", "cowork")


def absolute_links(markdown: str) -> str:
    """Point the README's relative links at the repository: the bundle holds only the skill."""
    return re.sub(r"\]\((?!https?:|mailto:|#)([^)\s]+)\)", lambda m: f"]({REPO_URL}{m.group(1)})", markdown)

# One line per module for the routing table and the bundled description.
MODULES = {
    "discovery-signals": ("Signals", "analyze customer feedback, Signal Briefs, or a synthetic dataset"),
    "discovery-personas": ("Working Backwards, Prototype", "generate personas, run a persona critique, panel, or role-play"),
    "discovery-use-case-scoring": ("Working Backwards, Validate", "score and prioritize 3 to 5 use cases"),
    "discovery-working-backwards": ("Working Backwards", "write or challenge a PR/FAQ and PRD, name the riskiest assumption"),
    "discovery-gtm": ("Working Backwards, Validate", "draft and complete the go-to-market section"),
    "discovery-prototype": ("Prototype", "build and iterate a clickable prototype"),
    "discovery-validate": ("Validate", "run the four risks, a pre-mortem, success criteria, and the decision"),
    "discovery-handoff": ("Handoff", "write the Discovery brief and next steps"),
    "discovery-signal-brief": ("Before Discovery", "write anonymized Signal Briefs"),
    "discovery-survey": ("After Discovery", "survey real users on open hypotheses"),
}


def split(text: str) -> tuple[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        raise ValueError("missing frontmatter")
    return match.group(1), match.group(2)


def field(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", frontmatter, re.M)
    return match.group(1).strip() if match else ""


def block(frontmatter: str, key: str) -> list[str]:
    """Indented lines that belong to a top-level list key, such as patterns: or inputs:."""
    lines = frontmatter.splitlines()
    out, inside = [], False
    for line in lines:
        if re.match(rf"^{re.escape(key)}:\s*$", line):
            inside = True
            continue
        if inside:
            if line.startswith(" "):
                out.append(line)
            else:
                break
    return out


def pattern_entries(frontmatter: str) -> list[str]:
    """Each pattern with its confidence line, kept together as one entry."""
    entries: list[str] = []
    for line in block(frontmatter, "patterns"):
        if line.lstrip().startswith("- "):
            entries.append(line)
        elif entries:
            entries[-1] += "\n" + line
    return entries


def inline_list(value: str) -> list[str]:
    return [v.strip() for v in value.strip("[]").split(",") if v.strip()]


def inputs_as_markdown(frontmatter: str) -> str:
    rows, current = [], {}
    for line in block(frontmatter, "inputs"):
        name = re.match(r"^\s+- name:\s*(.+)$", line)
        if name:
            if current:
                rows.append(current)
            current = {"name": name.group(1).strip()}
            continue
        kv = re.match(r"^\s+([a-z_]+):\s*(.+)$", line)
        if kv and current:
            current[kv.group(1)] = kv.group(2).strip().strip('"')
    if current:
        rows.append(current)
    if not rows:
        return ""
    lines = ["**Inputs.** Take each from the context so far, or ask:", ""]
    for r in rows:
        extra = f" Default: `{r['default']}`." if "default" in r else ""
        lines.append(f"- `{{{{{r['name']}}}}}`: {r.get('description', '')}{extra}")
    return "\n".join(lines) + "\n\n"


def link_modules(body: str, modules: dict | None = None) -> str:
    """Point **discovery-x** mentions at their module file."""
    modules = MODULES if modules is None else modules
    return re.sub(
        r"\*\*(discovery-[a-z-]+)\*\*(?! \(`modules/)",
        lambda m: f"**{m.group(1)}** (`modules/{m.group(1)}.md`)" if m.group(1) in modules else m.group(0),
        body,
    )


def rewrite_paths(body: str, name: str) -> str:
    return re.sub(r"(?<![\w/.])(references|templates)/", rf"modules/{name}/\1/", body)


ROUTING = {
    "quick": "Each job lives in its own module, a companion file of this skill. Before you start any phase or job, load its module by calling `file_read` on its path, for example `file_read(\"modules/discovery-signals.md\")`, and follow it from the top. Never do a phase's work without its module loaded. Load a module's `references/` files the same way, only when the module says so. These files ship with the skill; they are not in the user's folders, so do not search the user's folders for them. If a relative path such as `modules/discovery-signals.md` does not resolve, put the skill's full installed folder path in front of it. When the user asks for one job on its own, load just that module.",
    "cowork": "Each job lives in its own module, a companion file of this skill. Before you start any phase or job, read its module with `Read` at `${CLAUDE_SKILL_DIR}/` followed by its path, for example `${CLAUDE_SKILL_DIR}/modules/discovery-signals.md`, and follow it from the top. Never do a phase's work without its module loaded. Read a module's `references/` files the same way, only when the module says so. These files ship with the skill; they are not in the user's folders, so do not search the user's folders for them. When the user asks for one job on its own, read just that module, and \"Running in Cowork\" below.",
}

def dev_stamp(version: str) -> str:
    """'' for a clean checkout of the release tag; otherwise the commit, marked when there are uncommitted changes."""
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False).stdout.strip()
    sha = git("rev-parse", "--short", "HEAD")
    if not sha:
        return ""
    dirty = bool(git("status", "--porcelain", "--", ".", ":!dist", ":!.e2e"))
    if not dirty and git("tag", "--points-at", "HEAD") and f"v{version}" in git("tag", "--points-at", "HEAD").split():
        return ""
    return f"Development build {sha}{' with local changes' if dirty else ''} of {version}."


def build(out: Path, target: str = "quick", stamp: str = "") -> Path:
    if target not in TARGETS:
        raise ValueError(f"unknown target {target!r}: use one of {', '.join(TARGETS)}")
    if out.exists():
        shutil.rmtree(out)
    modules = MODULES
    if target == "quick":
        skill_out = out / "skills" / ENTRY
        (skill_out / "modules").mkdir(parents=True)
        for f in PACKAGE_FILES:
            shutil.copy2(ROOT / f, out / f)
        readme = out / "README.md"
        readme.write_text(absolute_links(readme.read_text(encoding="utf-8")), encoding="utf-8")
    else:
        skill_out = out
        (skill_out / "modules").mkdir(parents=True)
        shutil.copy2(ROOT / "LICENSE", skill_out / "LICENSE")

    entry_fm, entry_body = split((SKILLS / ENTRY / "SKILL.md").read_text(encoding="utf-8"))
    triggers = field(entry_fm, "trigger").strip('"').split()
    patterns = pattern_entries(entry_fm)
    tools = inline_list(field(entry_fm, "tools"))

    routing = ["## Modules", "", ROUTING[target], "",
               "| Module | Phase | Use it to |", "|--------|-------|-----------|"]

    for name, (phase, purpose) in modules.items():
        src = SKILLS / name
        fm, body = split((src / "SKILL.md").read_text(encoding="utf-8"))
        triggers += field(fm, "trigger").strip('"').split()
        patterns += pattern_entries(fm)
        tools += inline_list(field(fm, "tools"))
        routing.append(f"| `modules/{name}.md` | {phase} | {purpose} |")

        body = body.lstrip("\n")
        title, _, rest = body.partition("\n")
        module = f"{title}\n\n{inputs_as_markdown(fm)}{rest.lstrip()}"
        module = link_modules(rewrite_paths(module, name), modules)
        (skill_out / "modules" / f"{name}.md").write_text(module, encoding="utf-8")
        for sub in ("references", "templates"):
            if (src / sub).is_dir():
                shutil.copytree(src / sub, skill_out / "modules" / name / sub)

    for extra in (SKILLS / ENTRY).iterdir():
        if extra.name != "SKILL.md":
            (shutil.copytree if extra.is_dir() else shutil.copy2)(extra, skill_out / extra.name)

    def unique(seq: list[str]) -> list[str]:
        return list(dict.fromkeys(seq))

    purposes = "; ".join(p for _, p in modules.values())
    description = (
        "Runs AI-DLC Discovery end to end in five phases (Signals, Working Backwards, Prototype, "
        "Validate, Handoff), from customer feedback to a Discovery brief the team builds from. Use it to start or "
        f"continue Discovery, or for one job on its own: {purposes}."
    ) + (f" {stamp}" if stamp else "")
    # Keep the entry's frontmatter, minus the keys rebuilt from all skills.
    kept, skipping = [], False
    for line in entry_fm.splitlines():
        key = re.match(r"^([a-z_-]+):", line)
        if key:
            skipping = key.group(1) in ("description", "trigger", "patterns", "depends-on", "tools")
            if skipping:
                continue
        elif skipping and line.startswith(" "):
            continue
        kept.append(line)
    if target == "quick":
        frontmatter = "\n".join(
            kept[:3]
            + [f'description: "{description}"', f'trigger: "{" ".join(unique(triggers))}"', "patterns:"]
            + unique(patterns)
            + kept[3:]
            + [f"tools: [{', '.join(unique(tools))}]"]
        )
    else:
        # Agent Skills frontmatter: name and description are what Cowork reads.
        frontmatter = "\n".join([f"name: {ENTRY}", f'description: "{description}"', "license: MIT-0",
                                  "metadata:", f'  version: "{field(entry_fm, "version").strip(chr(34))}"',
                                  "  harness: cowork"])

    body = link_modules(entry_body, modules)
    marker = "## Shared rules"
    extra = ""
    if target == "cowork":
        extra = (COWORK / "running-in-cowork.md").read_text(encoding="utf-8").rstrip() + "\n\n"
    body = body.replace(marker, "\n".join(routing) + "\n\n" + extra + marker, 1)
    (skill_out / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
    if target == "cowork":
        cowork_rewrite(skill_out)
    return out


# Cowork: each rewrite is (file in the built skill, text in the source, replacement). The build
# fails if a text is no longer there, so a change to a source sentence cannot slip through unadapted.
COWORK_REWRITES: list[tuple[str, str, str]] = [
    ("SKILL.md", "- When the harness shows answer buttons (for example decision cards), make the recommended answer the first option. The chat text still uses the format above.",
     "- In Cowork, also put the round on question cards, with the recommended answer as the first option (see \"Running in Cowork\"). The chat text still uses the format above."),
    ("references/journey-app.md", "1. Load `references/journey-shell.md` with `file_read`, and save its HTML code block to `discovery/{{project}}/journey.html` with `file_write`, exactly as it is. Never retype it from memory, shorten it, or reformat it.",
     "1. Set `SHELL` in the update, as \"Running in Cowork\" says: the update writes `journey.html` from the shell."),
    ("references/journey-app.md", "3. Open `journey.html` with `open_in_session_tab`. Then tell",
     "3. Publish it as the journey artifact (see \"Running in Cowork\"). Then tell"),
    ("references/journey-app.md", "At a checkpoint, also open `journey.html` again with `open_in_session_tab`, so the session tab shows the new version.",
     "After every update, update the journey artifact (see \"Running in Cowork\")."),
    ("references/journey-app.md", "If it stops with \"copy the shell again\", do step 1 of \"Create it once\" again, then run the update again.",
     "If it stops with \"copy the shell again\", check that `SHELL` points at this skill's `references/journey-shell.md`, then run the update again."),
    ("config.default.md", "# Where it is: a folder relative to the working folder, or an AWS Quick Space name.",
     "# Where it is: a folder relative to the working folder."),
    ("modules/discovery-prototype.md", "`file_write`, then `open_in_session_tab`", "`Write`, then the prototype artifact"),
    ("modules/discovery-prototype.md", "; the build open in a session tab",
     "; the build published as the prototype artifact"),
    ("modules/discovery-prototype.md", "Then open it on the **Flow** view (`v1.html#/flow`), so the team sees the whole journey before clicking through it.",
     "Then publish it as the prototype artifact and refresh the journey app (see \"Running in Cowork\" in the entry skill). It opens on the **Flow** view, so the team sees the whole journey before clicking through it."),
    ("modules/discovery-prototype.md", "It is never offered in AWS Quick, and never started without the team asking.",
     "It is never started without the team asking."),
    ("modules/discovery-prototype/references/html-prototype.md",
     "In AWS Quick, also follow the bundled `html_design` skill's design principles where they apply.\n", ""),
    ("modules/discovery-prototype/references/html-prototype.md",
     "and open it for a live preview (Quick: `open_in_session_tab`; other tools: open the file in a browser).",
     "and publish it as the prototype artifact (see \"Running in Cowork\" in the entry skill)."),
    ("modules/discovery-prototype/references/codebase-prototype.md", "for AWS Quick (no repository), ", ""),
    ("modules/discovery-signals/references/current-product-map.md", "(greenfield) or in AWS Quick.", "(greenfield)."),
    ("modules/discovery-signals.md", "an AWS Quick Space name, or a folder relative", "a folder relative"),
    ("modules/discovery-signals.md", "`file_rag_search` for a Space; `file_read` for a folder", "`Read`, `Grep`, and `Glob`"),
    ("modules/discovery-signals.md", " It never blocks Discovery, and in AWS Quick it is skipped.", " It never blocks Discovery."),
    ("modules/discovery-signal-brief.md", "a folder, a Space, or files the team names", "a folder or files the team names"),
    ("modules/discovery-signal-brief.md", "in its own AWS Quick,", "in its own Cowork or AWS Quick,"),
    ("modules/discovery-handoff.md", "AWS Quick does not run AI-DLC:", "Cowork does not run AI-DLC:"),
    ("modules/discovery-survey/references/results-dashboard.md",
     "(Quick: `open_in_session_tab`; Kiro/Claude Code: open it in the editor or browser)",
     "(Cowork: show it with `present_files`; see \"Running in Cowork\" in the entry skill)"),
    ("modules/discovery-survey.md", "`file_write`, `open_in_session_tab`", "`Write`, then `present_files`"),
]

# Cowork tool names, applied to every Markdown file after the rewrites above.
COWORK_TOOLS = {
    "`file_read_pdf`": "`Read`",
    "`file_read_docx`": "`Read`",
    "`file_rag_search`": "`Grep`",
    "`file_read`": "`Read`",
    "`file_write`": "`Write`",
    "`run_python`": "`python3` in the shell",
    "`open_in_session_tab`": "the prototype artifact",
}


def cowork_rewrite(skill: Path) -> None:
    for rel, old, new in COWORK_REWRITES:
        path = skill / rel
        text = path.read_text(encoding="utf-8")
        if old not in text:
            raise ValueError(f"Cowork rewrite no longer matches {rel}: {old[:70]!r}. Update COWORK_REWRITES.")
        path.write_text(text.replace(old, new), encoding="utf-8")
    for path in skill.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for old, new in COWORK_TOOLS.items():
            text = text.replace(old, new)
        text = re.sub(r"`Read`(, `Read`)+", "`Read`", text)
        path.write_text(text, encoding="utf-8")


def package(out: Path, target: str = "quick") -> Path:
    """Zip the built folder beside it, with the folder at the top: .zip for AWS Quick, .skill for Cowork."""
    version = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))["version"]
    archive = out.parent / f"aidlc-discovery-v{version}.{'zip' if target == 'quick' else 'skill'}"
    archive.unlink(missing_ok=True)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(out.rglob("*")):
            if f.is_file():
                z.write(f, Path(ENTRY) / f.relative_to(out))
    return archive


def main(argv: list[str]) -> int:
    target, release = "quick", "--release" in argv
    argv = [a for a in argv if a != "--release"]
    if argv[:1] == ["--target"] and len(argv) > 1:
        target, argv = argv[1], argv[2:]
    if target not in TARGETS:
        print(f"Unknown target {target!r}: use one of {', '.join(TARGETS)}", file=sys.stderr)
        return 2
    default = ROOT / "dist" / ("aidlc-discovery" if target == "quick" else "cowork/aidlc-discovery")
    version = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))["version"]
    stamp = "" if release else dev_stamp(version)
    out = build((Path(argv[0]) if argv else default).resolve(), target, stamp)
    if stamp:
        print(stamp)
    print(f"Built {out}")
    print(f"Packaged {package(out, target)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
