"""Grade a workspace after a Discovery run in any harness, such as Claude Cowork or AWS Quick.

run_e2e.py drives Claude Code headless and grades its own runs. Cowork and AWS Quick run
in a desktop app, so run Discovery there by hand (or unattended, with config.md), then point
this script at the working folder. It runs the same D and O checks.

Usage: python3 tests/e2e/check_workspace.py <workspace> [--sample air|health] [--project air]
       [--journey]  also check the journey app (discovery/<project>/journey.html); --cowork is the same

Writes report.md next to the workspace folder; exit code 0 means no check failed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checks  # noqa: E402  # pyright: ignore[reportMissingImports]

SAMPLES = {"air": "anycompany-air", "health": "anycompany-health"}


REFS = Path(__file__).resolve().parents[2] / "skills" / "aidlc-discovery" / "references"
DATA = re.compile(r'(<script id="journey-data" type="application/json">)(.*?)(</script>)', re.S)
# Runs the page's own collect() in an isolated node vm context and prints the phases and the decision.
COLLECT_JS = r"""
const fs = require("fs"), vm = require("vm"), page = fs.readFileSync(process.argv[1], "utf8");
const src = page.slice(page.indexOf("/* collect:begin */"), page.indexOf("/* collect:end */"));
const d = vm.runInNewContext(src + "\n;collect", {})(JSON.parse(fs.readFileSync(0, "utf8")));
process.stdout.write(JSON.stringify({ statuses: d.phases.map((p) => p.status), decision: d.decision.value || "" }));
"""


def check_journey(workspace: Path, project: str) -> list[checks.Check]:
    folder = workspace / "discovery" / project
    page = checks.read(folder / "journey.html")
    found = [checks.Check("C01", "The journey app was created", bool(page))]
    if not page:
        return found
    try:
        data = json.loads(DATA.search(page).group(2))
    except (AttributeError, ValueError) as e:
        return found + [checks.Check("C02", "The journey app's data parses", False, str(e)[:120])]
    found.append(checks.Check("C02", "The journey app's data parses", bool(data.get("files"))))
    shape = "\n".join(line.rstrip() for line in DATA.sub(r"\1\3", page).strip().splitlines())
    expected = re.search(r'^SHAPE = "([0-9a-f]{12})"$', (REFS / "journey-app.md").read_text(encoding="utf-8"), re.M).group(1)
    found.append(checks.Check("C03", "The journey app is the shell, unchanged", hashlib.sha256(shape.encode()).hexdigest()[:12] == expected))
    on_disk = sorted(f.relative_to(folder).as_posix() for f in folder.rglob("*") if f.is_file()
                     and (f.suffix == ".md" or re.fullmatch(r"prototype/(v\d[^/]*|index)\.html", f.relative_to(folder).as_posix())))
    stale = sorted(set(on_disk) - set(data.get("files", {})))
    found.append(checks.Check("C04", "The journey app holds every artifact and prototype version", not stale, ", ".join(stale[:5])))
    found.append(checks.Check("C05", "The journey app shows what the team is doing now", bool((data.get("now") or {}).get("phase"))))
    found.append(checks.Check("C06", "The journey app loads nothing from the web", not re.search(r'<(script|link)[^>]+(src|href)="https?:', page)))
    node = shutil.which("node")
    if node:
        out = subprocess.run([node, "-e", COLLECT_JS, str(folder / "journey.html")], input=json.dumps(data),
                             capture_output=True, text=True, check=False)
        seen = json.loads(out.stdout) if out.returncode == 0 else {"statuses": [], "decision": ""}
        found.append(checks.Check("C07", "The journey app shows all five phases complete", seen["statuses"] == ["Complete"] * 5,
                                  ", ".join(seen["statuses"]) or out.stderr[:120]))
        found.append(checks.Check("C08", "The journey app shows the decision", bool(seen["decision"])))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--sample", default="air", choices=sorted(SAMPLES))
    parser.add_argument("--project", default=None, help="project folder under discovery/ (default: the sample's short name)")
    parser.add_argument("--journey", "--cowork", dest="journey", action="store_true", help="also check the journey app")
    args = parser.parse_args()

    ws, project = args.workspace.resolve(), args.project or args.sample
    exp = checks.expectations(SAMPLES[args.sample])
    found = checks.check_workshop(ws, project) + checks.check_outcome(ws, project, exp)
    if args.journey:
        found += check_journey(ws, project)
    failed = [c for c in found if not c.passed]
    lines = [f"# Discovery workspace check: {ws.name}", "", f"{len(found)} checks, {len(failed)} failed.", ""]
    lines += [f"- {'PASS' if c.passed else 'FAIL'} {c.id} {c.name}" + (f": {c.detail}" if c.detail and not c.passed else "") for c in found]
    (ws.parent / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
