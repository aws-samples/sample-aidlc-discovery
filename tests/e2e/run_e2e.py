"""Run AI-DLC Discovery end to end in Claude Code, headless, and check the results.

Each leg runs in a fresh scratch workspace: a copy of a sample's working folder
with the bundled skill installed as a project skill, so the run uses only this
package and none of the user's own settings.

Legs:
  workshop     the whole workshop, unattended, ending with the Discovery brief
  mismatch     the data is about a different product; the skill must not analyze or invent data
  missing-prd  Handoff on the workshop's results without the PRD; it must refuse
  team         a second model plays the scenario's team turn by turn, so the checkpoints are tested

Usage:
  python3 tests/e2e/run_e2e.py --sample air --legs workshop,mismatch --budget-usd 15
  python3 tests/e2e/run_e2e.py --sample all

Each run writes to --out (default .e2e/<timestamp>/): one folder per sample and leg
with the workspace, the transcript, and the cost; report.md and report.json at the top.
Exit code 0 means no check failed. Model calls are billed to the AWS account the
Claude Code CLI uses; --budget-usd caps every call.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import uuid
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checks  # noqa: E402  # pyright: ignore[reportMissingImports]

ROOT = checks.ROOT
PROMPTS = Path(__file__).resolve().parent / "prompts"
SAMPLES = {"air": "anycompany-air", "health": "anycompany-health"}
LEGS = ["workshop", "mismatch", "missing-prd", "team"]
TOOLS = "Read,Write,Edit,Glob,Grep,Skill,Bash(python3:*),Bash(ls:*),Bash(mkdir:*),Bash(cp:*)"
MISMATCH_PRODUCT = {"air": "AnyCompany Health's member portal", "health": "AnyCompany Air's website and app"}


def log(message: str) -> None:
    print(f"[e2e {datetime.now():%H:%M:%S}] {message}", flush=True)


def build_skill(out: Path) -> Path:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py"), str(out / "dist")], check=True, capture_output=True)
    return out / "dist" / "skills" / "aidlc-discovery"


def prepare(workspace: Path, skill: Path, slug: str, project: str, data_input: str, unattended: bool) -> None:
    shutil.copytree(ROOT / "samples" / slug, workspace)
    shutil.copytree(skill, workspace / ".claude" / "skills" / "aidlc-discovery")
    subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
    location = "discovery/signal-briefs/" if data_input == "signal-briefs" else "discovery/data/"
    (workspace / "config.md").write_text(
        "# AI-DLC Discovery Workshop Configuration (end-to-end test)\n\n```yaml\n"
        f'data_input: "{data_input}"\ndata_location: "{location}"\n'
        f'project: "{project}"\nengagement_reference: "E2E-{project}"\nunattended: {"true" if unattended else "false"}\n'
        "default_days: 0  # 0 means the whole period in the data\n```\n", encoding="utf-8")


def claude(prompt: str, cwd: Path, budget: float, model: str | None, session: str | None = None,
           resume: bool = False, tools: str = TOOLS) -> dict:
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--setting-sources", "project",
           "--permission-mode", "acceptEdits", "--allowedTools", tools, "--max-budget-usd", str(budget)]
    if model:
        cmd += ["--model", model]
    if session:
        cmd += (["--resume", session] if resume else ["--session-id", session])
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = {"result": result.stdout, "is_error": True}
    data["stderr"] = result.stderr[-2000:]
    return data


def prompt(name: str, **values: str) -> str:
    text = (PROMPTS / f"{name}.md").read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{" + key + "}", value)
    return text


def save(folder: Path, name: str, data: dict) -> None:
    (folder / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def run_leg(leg: str, short: str, out: Path, skill: Path, args: argparse.Namespace,
            cache: dict[str, Path]) -> tuple[list[checks.Check], float]:
    slug, project = SAMPLES[short], short
    exp = checks.expectations(slug)
    data_input = exp.get("data_input", "production")
    folder = out / short / leg
    folder.mkdir(parents=True)
    ws = folder / "workspace"
    cost = 0.0

    if leg == "workshop":
        prepare(ws, skill, slug, project, data_input, unattended=True)
        r = claude(prompt("workshop"), ws, args.budget_usd, args.model)
        save(folder, "transcript", r)
        cost += r.get("total_cost_usd", 0) or 0
        cache[short] = ws
        return checks.check_workshop(ws, project, f"E2E-{project}") + checks.check_outcome(ws, project, exp), cost

    if leg == "mismatch":
        prepare(ws, skill, slug, project, data_input, unattended=True)
        before = {p.name for p in (ws / "discovery" / "data").iterdir()} if (ws / "discovery" / "data").is_dir() else set()
        r = claude(prompt("mismatch", product=MISMATCH_PRODUCT[short]), ws, args.budget_usd, args.model)
        save(folder, "transcript", r)
        return checks.check_mismatch(ws, project, before, r.get("result", "")), (r.get("total_cost_usd", 0) or 0)

    if leg == "missing-prd":
        source = cache.get(short)
        if not source:
            return [checks.Check("N00", "Needs the workshop leg's workspace", False, "run the workshop leg first")], 0.0
        shutil.copytree(source, ws)
        for f in ("discovery-brief.md", "next-steps.md"):
            (ws / "discovery" / project / "handoff" / f).unlink(missing_ok=True)
        (ws / "discovery" / project / "working-backwards" / "prd.md").unlink(missing_ok=True)
        r = claude(prompt("handoff-only"), ws, args.budget_usd, args.model)
        save(folder, "transcript", r)
        return checks.check_missing_prd(ws, project, r.get("result", "")), (r.get("total_cost_usd", 0) or 0)

    if leg == "team":
        prepare(ws, skill, slug, project, data_input, unattended=False)
        scenario = (ws / "README.md").read_text(encoding="utf-8")
        session = str(uuid.uuid4())
        r = claude(prompt("team-start"), ws, args.budget_usd, args.model, session=session)
        turns = [{"facilitator": r.get("result", "")}]
        cost += r.get("total_cost_usd", 0) or 0
        scratch = folder / "team-scratch"
        scratch.mkdir()
        for _ in range(args.max_turns):
            if (ws / "discovery" / project / "handoff" / "next-steps.md").is_file():
                break
            reply = claude(prompt("team-player", scenario=scenario, message=turns[-1]["facilitator"]),
                           scratch, 2.0, args.team_model or args.model, tools="Read")
            cost += reply.get("total_cost_usd", 0) or 0
            turns[-1]["team"] = reply.get("result", "").strip()
            r = claude(turns[-1]["team"], ws, args.budget_usd, args.model, session=session, resume=True)
            cost += r.get("total_cost_usd", 0) or 0
            turns.append({"facilitator": r.get("result", "")})
        (folder / "conversation.json").write_text(json.dumps(turns, indent=2), encoding="utf-8")
        found = checks.check_workshop(ws, project, f"E2E-{project}") + checks.check_outcome(ws, project, exp) + checks.check_team(ws, project, exp)
        found.append(checks.Check("T00", f"Finished within {args.max_turns} team turns", (ws / "discovery" / project / "handoff" / "next-steps.md").is_file(),
                                  f"{len(turns) - 1} turns"))
        return found, cost

    raise ValueError(leg)


def report(out: Path, results: list[dict]) -> int:
    failed = sum(1 for r in results for c in r["checks"] if not c["passed"])
    lines = [f"# AI-DLC Discovery end-to-end report", "",
             f"{datetime.now():%Y-%m-%d %H:%M}. {sum(len(r['checks']) for r in results)} checks, {failed} failed. "
             f"Cost: ${sum(r['cost'] for r in results):.2f}.", ""]
    for r in results:
        lines += [f"## {r['sample']} / {r['leg']} (${r['cost']:.2f})", ""]
        lines += [f"- {'✅' if c['passed'] else '❌'} {c['id']} {c['name']}" + (f": {c['detail']}" if c["detail"] and not c["passed"] else "")
                  for c in r["checks"]]
        lines.append("")
    (out / "report.md").write_text("\n".join(lines), encoding="utf-8")
    (out / "report.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("\n".join(lines))
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sample", default="air", help="air, health, or all")
    parser.add_argument("--legs", default="workshop,mismatch,missing-prd", help=f"comma-separated: {', '.join(LEGS)}")
    parser.add_argument("--model", default=None, help="model for the Discovery runs (default: the CLI's default)")
    parser.add_argument("--team-model", default=None, help="model that plays the team (default: --model)")
    parser.add_argument("--budget-usd", type=float, default=15.0, help="cost cap for each Claude Code call")
    parser.add_argument("--max-turns", type=int, default=60, help="team leg: most team replies before giving up")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    samples = list(SAMPLES) if args.sample == "all" else [args.sample]
    legs = [l for l in LEGS if l in args.legs.split(",")]
    out = (args.out or ROOT / ".e2e" / datetime.now().strftime("%Y%m%d-%H%M%S")).resolve()
    out.mkdir(parents=True)
    skill = build_skill(out)
    cache: dict[str, Path] = {}
    results = []
    for short in samples:
        for leg in legs:
            log(f"{short} / {leg}")
            found, cost = run_leg(leg, short, out, skill, args, cache)
            results.append({"sample": short, "leg": leg, "cost": round(cost, 4), "checks": [asdict(c) for c in found]})
            log(f"{short} / {leg}: {sum(not c.passed for c in found)} failed, ${cost:.2f}")
    return report(out, results)


if __name__ == "__main__":
    sys.exit(main())
