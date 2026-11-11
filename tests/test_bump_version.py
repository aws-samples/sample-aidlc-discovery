"""The version is decided at release time from the latest tag, and written everywhere it lives."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
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
                         "versions are written only by the release workflow (scripts/bump_version.py)")


class NextVersion(unittest.TestCase):
    def test_bumps(self) -> None:
        self.assertEqual(bump_version.next_version("2.0.1", "major"), "3.0.0")
        self.assertEqual(bump_version.next_version("3.0.0", "patch"), "3.0.1")
        self.assertEqual(bump_version.next_version("3.0.1", "minor"), "3.1.0")
        self.assertEqual(bump_version.next_version("3.1.0", "v3.2.0"), "3.2.0")
        with self.assertRaises(ValueError):
            bump_version.next_version("3.0.0", "bigger")


class Release(unittest.TestCase):
    """A release in a scratch repository whose latest tag is v2.0.1."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copy2(ROOT / "plugin.json", self.root)
        shutil.copytree(ROOT / "skills", self.root / "skills")
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n---\n\n## [Unreleased]\n\n### Added\n\n- v3.\n\n---\n\n"
            "## [2.0.1] — 2026-07-02\n\n- Older.\n", encoding="utf-8")
        plain = ["-c", "user.name=t", "-c", "user.email=t@example.com", "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false"]
        git = lambda *a: subprocess.run(["git", *plain, *a], cwd=self.root, check=True, capture_output=True)
        git("init", "-q")
        git("commit", "-q", "--allow-empty", "-m", "start")
        git("tag", "v2.0.1")
        git("commit", "-q", "--allow-empty", "-m", "a merged pull request")
        self.git = git
        self.notes = self.root / "generated.md"
        self.notes.write_text("## What's Changed\n* feat: rounds by @someone in #6\n\n"
                              "**Full Changelog**: https://example.com/compare/v2.0.1...v3.0.0\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def release(self, bump: str, *extra: str) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            bump_version.main([bump, "--root", str(self.root), "--date", "2026-11-12", *extra])
        return out.getvalue().splitlines()[-1]

    def test_check_changes_nothing(self) -> None:
        before = versions(self.root)
        self.assertEqual(self.release("major", "--check"), "2.0.1 3.0.0")
        self.assertEqual(versions(self.root), before)
        self.assertNotIn("[3.0.0]", (self.root / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_major_after_v2_is_3_0_0_with_highlights_then_generated_notes(self) -> None:
        self.assertEqual(self.release("major", "--notes", str(self.notes)), "3.0.0")
        self.assertEqual(set(versions(self.root).values()), {"3.0.0"})
        changelog = (self.root / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [Unreleased]\n\n---\n\n## [3.0.0] — 2026-11-12\n\n### Added\n\n- v3.\n\n"
                      "### What's Changed\n* feat: rounds by @someone in #6", changelog)
        self.assertIn("\n---\n\n## [2.0.1] — 2026-07-02", changelog)

    def test_nobody_has_to_write_notes(self) -> None:
        (self.root / "CHANGELOG.md").write_text("## [Unreleased]\n\n---\n\n## [2.0.1] — 2026-07-02\n", encoding="utf-8")
        self.assertEqual(self.release("major", "--notes", str(self.notes)), "3.0.0")
        self.assertIn("## [3.0.0] — 2026-11-12\n\n### What's Changed", (self.root / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_refuses_a_version_that_is_not_higher_than_the_latest_tag(self) -> None:
        with self.assertRaises(SystemExit):
            self.release("2.0.1")
        self.assertNotEqual(set(versions(self.root).values()), {"2.0.1"})

    def test_refuses_patch_onto_an_older_major(self) -> None:
        with self.assertRaises(SystemExit):  # latest tag v2.0.1, but main holds 3.x work
            self.release("patch")
        self.assertNotIn("2.0.2", set(versions(self.root).values()))

    def test_refuses_when_nothing_was_merged_since_the_latest_tag(self) -> None:
        self.git("tag", "-f", "v2.0.1")  # the latest tag now points at HEAD
        before = versions(self.root)
        with self.assertRaises(SystemExit):
            self.release("major")
        self.assertEqual(versions(self.root), before)


if __name__ == "__main__":
    unittest.main()
