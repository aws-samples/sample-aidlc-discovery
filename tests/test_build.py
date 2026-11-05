"""Checks for the bundled skill that scripts/build.py produces."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = build.build(Path(cls.tmp.name) / "aidlc-discovery")
        cls.skill = cls.out / "skills" / "aidlc-discovery"
        cls.text = (cls.skill / "SKILL.md").read_text(encoding="utf-8")
        cls.frontmatter = cls.text.split("---")[1]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_one_skill_installs(self) -> None:
        self.assertEqual(["aidlc-discovery"], sorted(p.name for p in (self.out / "skills").iterdir()))
        for f in build.PACKAGE_FILES:
            self.assertTrue((self.out / f).is_file(), f)

    def test_frontmatter(self) -> None:
        self.assertRegex(self.frontmatter, r"(?m)^name: aidlc-discovery$")
        self.assertNotIn("depends-on", self.frontmatter)
        description = re.search(r'(?m)^description: "(.*)"$', self.frontmatter).group(1)
        self.assertLessEqual(len(description), 1024)
        entries = self.frontmatter.count("- pattern:")
        self.assertEqual(entries, len(re.findall(r"- pattern: .*\n\s+confidence: [0-9.]+", self.frontmatter)))
        self.assertLess(len(self.text.splitlines()), 500)

    def test_a_module_per_job_and_a_route_to_each(self) -> None:
        for name in build.MODULES:
            with self.subTest(module=name):
                self.assertTrue((self.skill / "modules" / f"{name}.md").is_file())
                self.assertIn(f"`modules/{name}.md`", self.text)

    def test_every_module_path_resolves(self) -> None:
        for path in self.skill.rglob("*.md"):
            for ref in re.findall(r"`(modules/[^`\s]+)`", path.read_text(encoding="utf-8")):
                with self.subTest(file=str(path.relative_to(self.skill)), ref=ref):
                    self.assertTrue((self.skill / ref).exists())

    def test_no_unrewritten_paths_in_modules(self) -> None:
        for path in (self.skill / "modules").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            with self.subTest(module=path.name):
                self.assertNotRegex(text, r"(?<![\w/.])(references|templates)/")

    def test_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pkg"
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py"), str(out)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((out / "skills" / "aidlc-discovery" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
