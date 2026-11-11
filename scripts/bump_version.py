"""Decide the release version from the latest tag, and set it everywhere it lives.

The version is chosen at release time, never before: the release workflow runs this
with patch, minor, or major, and it works out the next version from the latest vX.Y.Z
tag. It then writes that version in plugin.json and in the `version:` line of every
skills/*/SKILL.md, and adds the version's section to the changelog: any highlights
someone left under Unreleased (optional), then the release notes GitHub generated from
the merged pull requests (--notes). Between releases, those files hold the last
released version.

Usage:
    python3 scripts/bump_version.py patch|minor|major|X.Y.Z --check
        print the latest release and the next version, change nothing
    python3 scripts/bump_version.py patch|minor|major|X.Y.Z [--notes FILE] [--date YYYY-MM-DD]
        write the version and the changelog section; the last line printed is the version

It refuses a version that is not higher than the latest tag, one under an older major
version than main holds, and a release with no commits since the latest tag.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


def parse(version: str) -> tuple[int, int, int]:
    match = SEMVER.match(version)
    if not match:
        raise ValueError(f"{version!r} is not a version like 3.0.1")
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def latest_tag(root: Path) -> str:
    """The highest vX.Y.Z tag in the repository, or 0.0.0 when there is none."""
    tags = subprocess.run(["git", "tag", "--list", "v*"], cwd=root, capture_output=True, text=True, check=True)
    versions = [parse(t) for t in tags.stdout.split() if SEMVER.match(t)]
    return ".".join(map(str, max(versions))) if versions else "0.0.0"


def next_version(latest: str, bump: str) -> str:
    major, minor, patch = parse(latest)
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    if bump == "patch":
        return f"{major}.{minor}.{patch + 1}"
    parse(bump)
    return bump.lstrip("v")


def commits_since(root: Path, latest: str) -> int:
    if latest == "0.0.0":
        return 1
    out = subprocess.run(["git", "rev-list", "--count", f"v{latest}..HEAD"], cwd=root,
                         capture_output=True, text=True, check=True)
    return int(out.stdout.strip())


def check(root: Path, version: str, latest: str) -> None:
    if parse(version) <= parse(latest):
        raise ValueError(f"{version} is not higher than the latest release, {latest}")
    current = json.loads((root / "plugin.json").read_text(encoding="utf-8"))["version"]
    if parse(version)[0] < parse(current)[0]:
        raise ValueError(f"main holds version {current} work, so {version} would release it under an older "
                         f"major version: choose major")
    if not commits_since(root, latest):
        raise ValueError(f"nothing has been merged since v{latest}")


def section(highlights: str, notes: str) -> str:
    """Highlights first, then GitHub's notes, with their headings nested under the version."""
    notes = re.sub(r"^## ", "### ", notes.strip(), flags=re.M)
    return "\n\n".join(part for part in (highlights.strip(), notes) if part) + "\n\n"


def apply(root: Path, version: str, date: str, latest: str, notes: str = "") -> list[Path]:
    """Write the version and the changelog section. Checks everything before writing anything."""
    check(root, version, latest)
    changelog = root / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    if re.search(rf"^## \[{re.escape(version)}\]", text, re.M):
        raise ValueError(f"CHANGELOG.md already has a [{version}] section")
    match = re.search(r"^## \[Unreleased\]\n(.*?)(?=^---$|^## \[)", text, re.M | re.S)
    if not match:
        raise ValueError("CHANGELOG.md has no ## [Unreleased] section")
    body = section(match.group(1), notes) or "No notes.\n\n"
    text = (text[:match.start()] + f"## [Unreleased]\n\n---\n\n## [{version}] — {date}\n\n{body}"
            + text[match.end():])

    skills = {}
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        old = skill.read_text(encoding="utf-8")
        new = re.sub(r'^version: "[^"]+"$', f'version: "{version}"', old, count=1, flags=re.M)
        if not re.search(r'^version: "[^"]+"$', old, re.M):
            raise ValueError(f"{skill} has no version line")
        skills[skill] = new

    plugin = root / "plugin.json"
    plugin.write_text(re.sub(r'("version":\s*")[^"]+(")', rf"\g<1>{version}\2",
                             plugin.read_text(encoding="utf-8"), count=1), encoding="utf-8")
    changelog.write_text(text, encoding="utf-8")
    for skill, new in skills.items():
        skill.write_text(new, encoding="utf-8")
    return [plugin, changelog, *skills]


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("bump", help="patch, minor, major, or an exact version such as 3.0.1")
    p.add_argument("--check", action="store_true", help="print the latest and next version, change nothing")
    p.add_argument("--notes", type=Path, help="release notes to add, such as GitHub's generated notes")
    p.add_argument("--date", default=datetime.date.today().isoformat())
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args(argv)
    try:
        latest = latest_tag(args.root)
        version = next_version(latest, args.bump)
        if args.check:
            check(args.root, version, latest)
            print(f"{latest} {version}")
            return 0
        notes = args.notes.read_text(encoding="utf-8") if args.notes else ""
        changed = apply(args.root, version, args.date, latest, notes)
    except (ValueError, subprocess.CalledProcessError) as error:
        sys.exit(f"Not changed: {error}")
    print(f"Latest release: {latest}. Set {version} in {len(changed)} files.")
    print(version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
