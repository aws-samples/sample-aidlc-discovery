"""Grade a workspace after a Discovery run in any harness, such as Claude Cowork or AWS Quick.

run_e2e.py drives Claude Code headless and grades its own runs. Cowork and AWS Quick run
in a desktop app, so run Discovery there by hand (or unattended, with config.md), then point
this script at the working folder. It runs the same D and O checks.

Usage: python3 tests/e2e/check_workspace.py <workspace> [--sample air|health] [--project air]
       [--cowork]   also check the Cowork journey app (discovery/<project>/journey.html)

Writes report.md next to the workspace folder; exit code 0 means no check failed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checks  # noqa: E402  # pyright: ignore[reportMissingImports]

SAMPLES = {"air": "anycompany-air", "health": "anycompany-health"}


def check_cowork(workspace: Path, project: str) -> list[checks.Check]:
    page_path = workspace / "discovery" / project / "journey.html"
    page = checks.read(page_path)
    found = [checks.Check("C01", "The journey app was rendered", bool(page))]
    if not page:
        return found
    start = page.find('<script id="journey-data" type="application/json">')
    try:
        data = json.loads(page[page.index(">", start) + 1: page.index("</script>", start)])
    except ValueError as e:
        return found + [checks.Check("C02", "The journey app's data parses", False, str(e)[:120])]
    found.append(checks.Check("C02", "The journey app's data parses", True))
    statuses = [p["status"] for p in data["phases"]]
    found.append(checks.Check("C03", "The journey app shows all five phases complete", statuses == ["Complete"] * 5, ", ".join(statuses)))
    versions = sorted(p.name for p in (workspace / "discovery" / project / "prototype").glob("v[0-9]*.html"))
    found.append(checks.Check("C04", "The journey app holds every prototype version",
                              bool(versions) and [p["id"] + ".html" for p in data["prototypes"] if p["id"] != "index"] == sorted(versions, key=lambda n: int(re.sub(r"\D", "", n))),
                              f"{len(data['prototypes'])} in the app, {len(versions)} files"))
    found.append(checks.Check("C05", "The journey app shows the decision", bool(data.get("decision", {}).get("value"))))
    found.append(checks.Check("C06", "The journey app loads nothing from the web", not re.search(r'<(script|link)[^>]+(src|href)="https?:', page)))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--sample", default="air", choices=sorted(SAMPLES))
    parser.add_argument("--project", default=None, help="project folder under discovery/ (default: the sample's short name)")
    parser.add_argument("--cowork", action="store_true", help="also check the Cowork journey app")
    args = parser.parse_args()

    ws, project = args.workspace.resolve(), args.project or args.sample
    exp = checks.expectations(SAMPLES[args.sample])
    found = checks.check_workshop(ws, project) + checks.check_outcome(ws, project, exp)
    if args.cowork:
        found += check_cowork(ws, project)
    failed = [c for c in found if not c.passed]
    lines = [f"# Discovery workspace check: {ws.name}", "", f"{len(found)} checks, {len(failed)} failed.", ""]
    lines += [f"- {'PASS' if c.passed else 'FAIL'} {c.id} {c.name}" + (f": {c.detail}" if c.detail and not c.passed else "") for c in found]
    (ws.parent / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
