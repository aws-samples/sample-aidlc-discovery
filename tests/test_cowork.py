"""Checks for the Cowork build (scripts/build.py --target cowork)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402

QUICK_ONLY = re.compile(r"file_read|file_write|run_python|file_rag_search|open_in_session_tab|session tab|"
                        r"html_design|team Space|discovery-team-space|\bQuick:")


class CoworkBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.skill = build.build(Path(cls.tmp.name) / "aidlc-discovery", "cowork")
        cls.text = (cls.skill / "SKILL.md").read_text(encoding="utf-8")
        cls.frontmatter = cls.text.split("---")[1]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_frontmatter_is_agent_skills(self) -> None:
        keys = re.findall(r"(?m)^([a-z_-]+):", self.frontmatter)
        self.assertEqual(["name", "description", "license", "metadata"], keys)
        self.assertRegex(self.frontmatter, r"(?m)^name: aidlc-discovery$")
        description = re.search(r'(?m)^description: "(.*)"$', self.frontmatter).group(1)
        self.assertLessEqual(len(description), 1024)
        self.assertNotIn("team Space", description)

    def test_quick_only_parts_are_gone(self) -> None:
        self.assertFalse((self.skill / "modules" / "discovery-team-space.md").exists())
        for path in self.skill.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            with self.subTest(file=str(path.relative_to(self.skill))):
                self.assertIsNone(QUICK_ONLY.search(text), QUICK_ONLY.search(text) and QUICK_ONLY.search(text).group(0))

    def test_every_module_path_resolves(self) -> None:
        for path in self.skill.rglob("*.md"):
            for ref in re.findall(r"`(?:\$\{CLAUDE_SKILL_DIR\}/)?((?:modules|references)/[^`\s]+)`", path.read_text(encoding="utf-8")):
                if ref.endswith("..."):
                    continue
                with self.subTest(file=str(path.relative_to(self.skill)), ref=ref):
                    self.assertTrue((self.skill / ref).exists())

    def test_cowork_section_and_journey_app_ship(self) -> None:
        self.assertIn("## Running in Cowork", self.text)
        self.assertLess(self.text.index("## Running in Cowork"), self.text.index("## Shared rules"))
        for term in ("AskUserQuestion", "create_artifact", "update_artifact", "present_files", "${CLAUDE_SKILL_DIR}"):
            self.assertIn(term, self.text)
        for ref in ("journey-app.md", "journey-shell.md"):
            self.assertTrue((self.skill / "references" / ref).is_file())
        self.assertLess(len(self.text.splitlines()), 500)

    def test_every_rewrite_applies(self) -> None:
        for rel, old, new in build.COWORK_REWRITES:
            with self.subTest(file=rel, text=old[:50]):
                if new and len(new) > 20:
                    self.assertIn(new, (self.skill / rel).read_text(encoding="utf-8"))

    def test_skill_package(self) -> None:
        archive = build.package(self.skill, "cowork")
        self.assertEqual(".skill", archive.suffix)
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
        self.assertIn("aidlc-discovery/SKILL.md", names)
        self.assertIn("aidlc-discovery/references/journey-shell.md", names)
        self.assertTrue(all(n.startswith("aidlc-discovery/") for n in names))

    def test_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "aidlc-discovery"
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py"), "--target", "cowork", str(out)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((out / "SKILL.md").is_file())
            self.assertTrue(list(Path(tmp).glob("aidlc-discovery-v*.skill")))



if __name__ == "__main__":
    unittest.main()
