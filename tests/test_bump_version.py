"""The version lives in plugin.json and every SKILL.md; they must agree, and the bump script changes them together."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bump_version", ROOT / "scripts" / "bump_version.py")
bump_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bump_version)


def versions(root: Path) -> dict[str, str]:
    found = {"plugin.json": json.loads((root / "plugin.json").read_text(encoding="utf-8"))["version"]}
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        match = re.search(r'^version: "([^"]+)"$', skill.read_text(encoding="utf-8"), re.M)
        found[skill.parent.name] = match.group(1) if match else "missing"
    return found


class VersionsAgree(unittest.TestCase):
    def test_every_skill_has_the_plugin_version(self) -> None:
        found = versions(ROOT)
        self.assertEqual({k: v for k, v in found.items() if v != found["plugin.json"]}, {},
                         "run python3 scripts/bump_version.py X.Y.Z instead of editing versions by hand")


class Bump(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copy2(ROOT / "plugin.json", self.root)
        shutil.copytree(ROOT / "skills", self.root / "skills")
        self.current = versions(ROOT)["plugin.json"]
        major, minor, patch = bump_version.parse(self.current)
        self.next = f"{major}.{minor}.{patch + 1}"
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n---\n\n## [Unreleased]\n\n### Fixed\n\n- A fix.\n\n---\n\n"
            f"## [{self.current}] — 2026-01-01\n\n- Older.\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_sets_every_version_and_closes_unreleased(self) -> None:
        bump_version.bump(self.root, self.next, "2026-11-12")
        self.assertEqual(set(versions(self.root).values()), {self.next})
        changelog = (self.root / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(f"## [Unreleased]\n\n---\n\n## [{self.next}] — 2026-11-12\n\n### Fixed\n\n- A fix.", changelog)
        self.assertIn(f"## [{self.current}] — 2026-01-01", changelog)

    def test_refuses_a_version_that_is_not_higher(self) -> None:
        with self.assertRaises(ValueError):
            bump_version.bump(self.root, self.current, "2026-11-12")
        self.assertEqual(set(versions(self.root).values()), {self.current})

    def test_refuses_an_empty_unreleased_section(self) -> None:
        (self.root / "CHANGELOG.md").write_text("## [Unreleased]\n\n---\n\n## [1.0.0] — 2026-01-01\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            bump_version.bump(self.root, self.next, "2026-11-12")


if __name__ == "__main__":
    unittest.main()
