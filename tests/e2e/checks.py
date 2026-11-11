"""Deterministic checks on a workspace after a Discovery run.

Mechanical checks (D, N, T) test that the method ran: artifacts, order, and
format. Outcome checks (O) grade the result against the sample's facilitator
notes. Every check returns pass or fail with a short detail.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
HANDOFF = SKILLS / "discovery-handoff" / "SKILL.md"
SHELL_REF = SKILLS / "discovery-prototype" / "references" / "prototype-shell.md"
BRIEF_LIMIT = 200_000
EDIT_BELOW = "<!-- ============================== EDIT BELOW ============================== -->"
EDIT_ABOVE = "<!-- ============================== EDIT ABOVE ============================== -->"


@dataclass
class Check:
    id: str
    name: str
    passed: bool
    detail: str = ""


def required_artifacts() -> list[str]:
    """Paths from the Handoff skill's required-artifact table, minus the codebase-only row."""
    text = HANDOFF.read_text(encoding="utf-8")
    section = text.split("### Step 1:", 1)[1].split("### Step 2:", 1)[0]
    rows = re.findall(r"^\| (.+?) \| `([^`]+)` \| [a-z-]+ \|$", section, re.M)
    return [path for label, path in rows if "codebase" not in label.lower()]


def brief_sections() -> list[str]:
    text = HANDOFF.read_text(encoding="utf-8")
    template = text.split("## Output", 1)[1].split("## Lessons Learned", 1)[0]
    return re.findall(r"^## \d+\. (.+)$", template, re.M)


def shell_html() -> str:
    match = re.search(r"````html\n(.*?)````", SHELL_REF.read_text(encoding="utf-8"), re.S)
    assert match, "prototype-shell.md has no HTML code block"
    return match.group(1)


def outside_edit_region(html: str) -> str:
    if html.count(EDIT_BELOW) != 1 or html.count(EDIT_ABOVE) != 1:
        return ""
    outside = html[: html.index(EDIT_BELOW)] + html[html.index(EDIT_ABOVE) + len(EDIT_ABOVE):]
    return "\n".join(line.rstrip() for line in outside.strip().splitlines())  # ignore trailing whitespace


def section(text: str, heading: str) -> str:
    """The body of the first heading that starts with `heading` (after any numbering), else the first that contains it."""
    for prefix in (r"(?:\d+\.\s*)?", r"[^\n]*"):
        match = re.search(rf"^##+ {prefix}{re.escape(heading)}[^\n]*$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
        if match:
            return match.group(1)
    return ""


def phrases(expectation: str) -> list[str]:
    """Alternative phrasings, separated by | in the facilitator notes."""
    return [a.strip().lower() for a in expectation.split("|") if a.strip()]


def words(phrase: str) -> list[str]:
    """Distinctive words of an expectation, for loose matching."""
    stop = {"with", "from", "that", "this", "their", "them", "your", "the", "and", "for"}
    return [w for w in re.findall(r"[a-z0-9]+", phrase.lower()) if len(w) > 3 and w not in stop] or [phrase.lower()]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def check_workshop(workspace: Path, project: str) -> list[Check]:
    d = workspace / "discovery" / project
    checks: list[Check] = []

    missing = []
    for rel in required_artifacts():
        if rel.endswith("*.md"):
            if len(list((d / rel[:-4]).glob("*.md"))) < 2:
                missing.append(f"{rel} (fewer than 2)")
        elif not (d / rel).is_file():
            missing.append(rel)
    checks.append(Check("D01", "Required artifacts exist", not missing, ", ".join(missing)))

    brief_path = d / "handoff" / "discovery-brief.md"
    brief = read(brief_path)
    checks.append(Check("D02", "Discovery brief exists", bool(brief)))
    found = re.findall(r"^## \d+\. (.+?)\s*$", brief, re.M)
    expected = brief_sections()
    checks.append(Check("D03", f"Brief has the {len(expected)} sections in order", found == expected,
                        "" if found == expected else f"found {found}"))
    checks.append(Check("D04", f"Brief is under {BRIEF_LIMIT:,} characters", 0 < len(brief) < BRIEF_LIMIT, f"{len(brief):,}"))
    context = section(brief, "Context")
    checks.append(Check("D05", "Brief context gives the date, route, and data", all(f"{k}:" in context for k in ("Date", "Route", "Data"))))

    texts = {p: read(p) for p in d.rglob("*") if p.suffix in (".md", ".html")}
    emails = sorted({e for t in texts.values() for e in re.findall(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", t)
                     if not re.search(r"@example\.(com|org)$", e)})
    checks.append(Check("D06", "No email addresses in artifacts", not emails, ", ".join(emails[:5])))
    crm = sorted({c for t in texts.values() for c in re.findall(r"\b00[16][A-Za-z0-9]{12}(?:[A-Za-z0-9]{3})?\b", t)})
    checks.append(Check("D07", "No CRM identifiers in artifacts", not crm, ", ".join(crm[:5])))

    links = re.findall(r"\]\(([^)#\s]+)\)", brief)
    broken = [l for l in links if not l.startswith("http") and not (brief_path.parent / l).resolve().exists()]
    checks.append(Check("D08", "Brief links resolve", bool(links) and not broken, ", ".join(broken[:5])))
    checks.append(Check("D09", ".gitignore excludes discovery/data/", "discovery/data/" in read(workspace / ".gitignore")))
    scripts = [str(p.relative_to(workspace)) for p in (workspace / "discovery").rglob("*") if p.suffix in (".py", ".sh", ".js", ".ipynb")]
    checks.append(Check("D10", "No scripts saved under discovery/", not scripts, ", ".join(scripts[:5])))

    proto = d / "prototype"
    versions = sorted(proto.glob("v[0-9]*.html"))
    shell_outside = outside_edit_region(shell_html())
    not_shell = [p.name for p in versions if outside_edit_region(read(p)) != shell_outside]
    checks.append(Check("D11", "Every prototype version is built from the shell", bool(versions) and not not_shell,
                        "no v*.html" if not versions else ", ".join(not_shell)))
    index = read(proto / "index.html")
    checks.append(Check("D12", "index.html is one of the versions", any(index == read(p) for p in versions)))
    checks.append(Check("D13", "versions.md logs the versions", bool(versions) and all(p.stem in read(proto / "versions.md") for p in versions)))
    checks.append(Check("D14", "Persona critique sits in prototype/", (proto / "persona-critique.md").is_file()
                        and not (d / "validate" / "persona-critique.md").exists()))
    decision = read(d / "validate" / "decision.md").lower()
    checks.append(Check("D15", "Decision is commit, pivot, or park", bool(re.search(r"\*\*decision:\*\*\s*\**\s*(commit|pivot|park)", decision, re.I))))
    drafts = [l.strip() for l in read(d / "working-backwards" / "gtm.md").splitlines() if re.search(r"status:?\**\s*\**draft", l, re.I)]
    checks.append(Check("D16", "No GTM part left as draft", not drafts, "; ".join(drafts[:3])))
    th, ss = d / "signals" / "team-expectations.md", d / "signals" / "signal-summary.md"
    first = th.is_file() and ss.is_file() and _created(th) <= _created(ss)
    checks.append(Check("D17", "Team expectations written before the analysis", first))
    checks.append(Check("D18", "next-steps.md written", (d / "handoff" / "next-steps.md").is_file()))
    steps = read(d / "handoff" / "next-steps.md").lower()
    checks.append(Check("D20", "next-steps.md has a Now, Next, Later roadmap",
                        "roadmap" in steps and all(re.search(rf"\b{w}\b", steps) for w in ("now", "next", "later"))))
    prfaq = read(d / "working-backwards" / "prfaq.md")
    checks.append(Check("D19", "PR/FAQ has a readiness verdict and a Prototype scope section",
                        bool(re.search(r"verdict:?\**\s*\**(green|amber|red)", prfaq, re.I)) and "prototype scope" in prfaq.lower()))
    return checks


def _created(path: Path) -> float:
    stat = path.stat()
    return getattr(stat, "st_birthtime", stat.st_mtime)


def check_outcome(workspace: Path, project: str, expectations: dict[str, str]) -> list[Check]:
    d = workspace / "discovery" / project
    summary = read(d / "signals" / "signal-summary.md")
    scoring = read(d / "working-backwards" / "use-case-scoring.md")
    checks: list[Check] = []

    top = re.search(r"^###\s*1\.\s*(.+)$", summary, re.M)
    top_text = top.group(1).lower() if top else ""
    checks.append(Check("O01", f"Top signal is about \"{expectations['top_signal']}\"",
                        any(p in top_text for p in phrases(expectations["top_signal"])), top_text[:120]))

    distractor = words(expectations["distractor_fails_gate"])
    numbers = {m.group(1) for l in scoring.splitlines() if any(w in l.lower() for w in distractor)
               for m in [re.match(r"^\|\s*#?(\d+)\s*\|", l)] if m}
    gate_rows = [l for l in section(scoring, "Gate").splitlines()
                 if (m := re.match(r"^\|\s*#?(\d+)\s*\|", l)) and (m.group(1) in numbers or any(w in l.lower() for w in distractor))]
    failed = any(re.search(r"❌|\b(drop|dropped|fail|failed|no)\b", r.lower()) and not re.search(r"\bdefer(red)?\b", r.lower()) for r in gate_rows)
    if not gate_rows:  # no gate row found: fall back to a drop decision near the distractor's name
        failed = bool(re.search(rf"({'|'.join(distractor)}).{{0,200}}\b(drop|dropped)\b", scoring.lower(), re.S))
    checks.append(Check("O02", f"\"{expectations['distractor_fails_gate']}\" fails the gate or is dropped", failed))

    if expectations.get("say_and_do") == "true":
        say_do = section(summary, "Say and do")
        checks.append(Check("O04", "The report has a Say and do table", bool(say_do.strip()) and "|" in say_do))
        trap = phrases(expectations.get("telemetry_trap", ""))
        checks.append(Check("O05", f"The telemetry trap ({expectations.get('telemetry_trap')}) is not the top signal",
                            bool(top_text) and not any(p in top_text for p in trap)))
        only = phrases(expectations.get("telemetry_only", ""))
        checks.append(Check("O06", f"A telemetry-only signal about \"{expectations.get('telemetry_only')}\" is reported",
                            any(p in say_do.lower() for p in only)))
        feas = phrases(expectations.get("feasibility_evidence", ""))
        checks.append(Check("O07", f"\"{expectations.get('feasibility_evidence')}\" is used as feasibility evidence",
                            any(p in scoring.lower() for p in feas)))

    if expectations.get("signals_candidates"):
        from_signals = section(scoring, "From Signals")
        rows = [l for l in from_signals.splitlines() if l.startswith("|") and not re.match(r"^\|\s*[-:|\s]+$", l)][1:]
        least = int(expectations["signals_candidates"])
        checks.append(Check("O08", f"At least {least} candidates from Signals are added, each kept or dropped",
                            len(rows) >= least and all(re.search(r"\b(kept|keep|dropped|drop|merged)\b", l.lower()) for l in rows),
                            f"{len(rows)} candidates"))
    if expectations.get("ai_feature_block") == "true":
        prd = read(d / "working-backwards" / "prd.md")
        block = section(prd, "AI feature block") or (prd[prd.lower().find("ai feature block"):] if "ai feature block" in prd.lower() else "")
        rows = [l for l in block.splitlines() if re.match(r"^\|\s*\d+\s*\|", l)]
        checks.append(Check("O09", "The PRD has an AI feature block with 5 to 10 evaluation cases, including negative ones",
                            5 <= len(rows) <= 10 and any("negative" in l.lower() for l in rows), f"{len(rows)} cases"))
        later = read(d / "validate" / "decision.md") + read(d / "validate" / "risk-review.md") + read(d / "working-backwards" / "gtm.md")
        checks.append(Check("O10", "An AI quality target is in the success criteria or the GTM table", "ai quality" in later.lower()))

    forward = section(scoring, "Taken forward") or scoring[-1500:]
    checks.append(Check("O03", f"\"{expectations['build_first_or_learn']}\" is taken forward",
                        any(w in forward.lower() for w in words(expectations["build_first_or_learn"])), forward.strip()[:160]))
    return checks


def check_mismatch(workspace: Path, project: str, data_before: set[str], transcript: str) -> list[Check]:
    data = workspace / "discovery" / "data"
    after = {p.name for p in data.iterdir()} if data.is_dir() else set()
    new = sorted(after - data_before)
    return [
        Check("N01", "No data was generated to fill the gap", not new, ", ".join(new)),
        Check("N02", "No Signal Analysis Report on mismatched data",
              not (workspace / "discovery" / project / "signals" / "signal-summary.md").exists()),
        Check("N03", "It offered real data, Signal Briefs, or a prepared dataset",
              bool(re.search(r"signal brief|real data|prepared (before|ahead)|synthetic dataset", transcript, re.I))),
    ]


def check_missing_prd(workspace: Path, project: str, transcript: str) -> list[Check]:
    return [
        Check("N04", "No brief while the PRD is missing", not (workspace / "discovery" / project / "handoff" / "discovery-brief.md").exists()),
        Check("N05", "It named the missing PRD", bool(re.search(r"\bPRD\b|prd\.md", transcript))),
    ]


def check_team(workspace: Path, project: str, expectations: dict[str, str]) -> list[Check]:
    d = workspace / "discovery" / project
    overrides = section(read(d / "working-backwards" / "use-case-scoring.md"), "Overrides")
    loud = words(expectations["loud_request"])
    decision = read(d / "validate" / "decision.md")
    conditions = re.search(r"\*\*conditions before the build:\*\*\s*(.+)", decision, re.I)
    return [
        Check("T01", "The team's override of the loud request is recorded",
              any(any(w in l.lower() for w in loud) and re.search(r"\|\s*\d\s*\|\s*\d\s*\|", l) for l in overrides.splitlines())),
        Check("T02", "Test-first conditions are recorded", bool(conditions) and not re.match(r"\s*none", conditions.group(1), re.I)),
        Check("T03", "The prototype was iterated (two versions or more)", len(list((d / "prototype").glob("v[0-9]*.html"))) >= 2),
    ]


def expectations(sample_slug: str) -> dict[str, str]:
    notes = (ROOT / "facilitator" / f"{sample_slug}.md").read_text(encoding="utf-8")
    match = re.search(r"```yaml\n(expectations:.*?)```", notes, re.S)
    assert match, f"no expectations block in facilitator/{sample_slug}.md"
    block = match.group(1)
    return {k: v.strip().strip('"') for k, v in re.findall(r"^\s+(\w+):\s*(\"[^\"]*\"|[^#\n]+)", block, re.M)}
