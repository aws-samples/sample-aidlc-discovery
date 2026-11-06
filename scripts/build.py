"""Bundle the separate skills under skills/ into one installable Amazon Quick skill.

The repository keeps one folder per skill, so each job is easy to edit and test.
Installed, they become a single skill, `aidlc-discovery`: the entry skill's
SKILL.md plus a module per job under modules/, loaded only when its step runs.

Usage: python3 scripts/build.py [output_dir]   (default: dist/aidlc-discovery)
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
ENTRY = "aidlc-discovery"
PACKAGE_FILES = ["plugin.json", "mcps.json", "tasks.json", "LICENSE", "README.md"]

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
    "discovery-signal-brief": ("Before the workshop", "write anonymized Signal Briefs"),
    "discovery-survey": ("After the workshop", "survey real users on open hypotheses"),
    "discovery-team-space": ("Any phase, Amazon Quick only", "save the workshop in a team Space so several people can follow and take over"),
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
    lines = ["**Inputs.** Take each from the workshop's context, or ask:", ""]
    for r in rows:
        extra = f" Default: `{r['default']}`." if "default" in r else ""
        lines.append(f"- `{{{{{r['name']}}}}}`: {r.get('description', '')}{extra}")
    return "\n".join(lines) + "\n\n"


def link_modules(body: str) -> str:
    """Point **discovery-x** mentions at their module file."""
    return re.sub(
        r"\*\*(discovery-[a-z-]+)\*\*(?! \(`modules/)",
        lambda m: f"**{m.group(1)}** (`modules/{m.group(1)}.md`)" if m.group(1) in MODULES else m.group(0),
        body,
    )


def rewrite_paths(body: str, name: str) -> str:
    return re.sub(r"(?<![\w/.])(references|templates)/", rf"modules/{name}/\1/", body)


def build(out: Path) -> Path:
    if out.exists():
        shutil.rmtree(out)
    skill_out = out / "skills" / ENTRY
    (skill_out / "modules").mkdir(parents=True)
    for f in PACKAGE_FILES:
        shutil.copy2(ROOT / f, out / f)

    entry_fm, entry_body = split((SKILLS / ENTRY / "SKILL.md").read_text(encoding="utf-8"))
    triggers = field(entry_fm, "trigger").strip('"').split()
    patterns = pattern_entries(entry_fm)
    tools = inline_list(field(entry_fm, "tools"))

    routing = ["## Modules", "",
               "Each job lives in its own module, a companion file of this skill. Before you start any phase or job, load its module by calling `file_read` on its path, for example `file_read(\"modules/discovery-signals.md\")`, and follow it from the top. Never do a phase's work without its module loaded. Load a module's `references/` files the same way, only when the module says so. These files ship with the skill; they are not in the user's folders, so do not search the user's folders for them. If a relative path such as `modules/discovery-signals.md` does not resolve, put the skill's full installed folder path in front of it. When the user asks for one job on its own, load just that module.", "",
               "| Module | Phase | Use it to |", "|--------|-------|-----------|"]

    for name, (phase, purpose) in MODULES.items():
        src = SKILLS / name
        fm, body = split((src / "SKILL.md").read_text(encoding="utf-8"))
        triggers += field(fm, "trigger").strip('"').split()
        patterns += pattern_entries(fm)
        tools += inline_list(field(fm, "tools"))
        routing.append(f"| `modules/{name}.md` | {phase} | {purpose} |")

        body = body.lstrip("\n")
        title, _, rest = body.partition("\n")
        module = f"{title}\n\n{inputs_as_markdown(fm)}{rest.lstrip()}"
        module = link_modules(rewrite_paths(module, name))
        (skill_out / "modules" / f"{name}.md").write_text(module, encoding="utf-8")
        for sub in ("references", "templates"):
            if (src / sub).is_dir():
                shutil.copytree(src / sub, skill_out / "modules" / name / sub)

    for extra in (SKILLS / ENTRY).iterdir():
        if extra.name != "SKILL.md":
            (shutil.copytree if extra.is_dir() else shutil.copy2)(extra, skill_out / extra.name)

    def unique(seq: list[str]) -> list[str]:
        return list(dict.fromkeys(seq))

    purposes = "; ".join(p for _, p in MODULES.values())
    description = (
        "Runs an AI-DLC Discovery workshop end to end in five phases (Signals, Working Backwards, Prototype, "
        "Validate, Handoff), from customer feedback to a Discovery brief the team builds from. Use it to start or "
        f"continue a Discovery workshop, or for one job on its own: {purposes}."
    )
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
    frontmatter = "\n".join(
        kept[:3]
        + [f'description: "{description}"', f'trigger: "{" ".join(unique(triggers))}"', "patterns:"]
        + unique(patterns)
        + kept[3:]
        + [f"tools: [{', '.join(unique(tools))}]"]
    )

    body = link_modules(entry_body)
    marker = "## Shared rules"
    body = body.replace(marker, "\n".join(routing) + "\n\n" + marker, 1)
    (skill_out / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
    return out


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist" / "aidlc-discovery"
    print(f"Built {build(target.resolve())}")
