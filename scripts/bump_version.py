"""Set the release version everywhere it lives, and close the changelog's Unreleased section.

The version is written in plugin.json and in the `version:` line of every skills/*/SKILL.md,
and the release workflow checks they all match the tag. This script changes them together.

Usage: python3 scripts/bump_version.py X.Y.Z [--date YYYY-MM-DD] [--root DIR]

It refuses a version that is not higher than the current one, and an empty Unreleased section.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def parse(version: str) -> tuple[int, int, int]:
    match = SEMVER.match(version)
    if not match:
        raise ValueError(f"{version!r} is not a version like 3.0.1")
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def bump(root: Path, version: str, date: str) -> list[Path]:
    plugin = root / "plugin.json"
    current = json.loads(plugin.read_text(encoding="utf-8"))["version"]
    if parse(version) <= parse(current):
        raise ValueError(f"{version} is not higher than the current version {current}")

    changelog = root / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    match = re.search(r"^## \[Unreleased\]\n(.*?)(?=^---$|^## \[)", text, re.M | re.S)
    if not match:
        raise ValueError("CHANGELOG.md has no ## [Unreleased] section")
    if not match.group(1).strip():
        raise ValueError("the Unreleased section is empty: nothing to release")
    text = (text[:match.start()] + f"## [Unreleased]\n\n---\n\n## [{version}] — {date}\n"
            + text[match.start() + len("## [Unreleased]\n"):])

    skills = {}
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        old = skill.read_text(encoding="utf-8")
        new = re.sub(r'^version: "[^"]+"$', f'version: "{version}"', old, count=1, flags=re.M)
        if new == old:
            raise ValueError(f"{skill} has no version line")
        skills[skill] = new

    # Everything checked: write it all.
    plugin.write_text(re.sub(r'("version":\s*")[^"]+(")', rf"\g<1>{version}\2",
                             plugin.read_text(encoding="utf-8"), count=1), encoding="utf-8")
    changelog.write_text(text, encoding="utf-8")
    for skill, new in skills.items():
        skill.write_text(new, encoding="utf-8")
    changed = [plugin, changelog, *skills]
    return changed


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("version")
    p.add_argument("--date", default=datetime.date.today().isoformat())
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = p.parse_args(argv)
    try:
        changed = bump(args.root, args.version.lstrip("v"), args.date)
    except ValueError as error:
        sys.exit(f"Not changed: {error}")
    print(f"Set version {args.version.lstrip('v')} in {len(changed)} files.")
    print("Next: open a pull request with these changes, merge it, then start the release "
          f"(Actions, Release v3, Run workflow, version {args.version.lstrip('v')}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
