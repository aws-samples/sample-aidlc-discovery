"""The samples follow samples/CONVENTIONS.md and their generators are reproducible."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ["anycompany-air", "anycompany-health"]
README_SECTIONS = ["How to run it"]
TEMPLATE = ROOT / "skills" / "aidlc-discovery" / "templates" / "kickoff.md"
EXPECTATION_KEYS = ["top_signal", "loud_request", "distractor_fails_gate", "build_first_or_learn", "data_input"]


def digest(folder: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        h.update(str(path.relative_to(folder)).encode())
        h.update(path.read_bytes())
    return h.hexdigest()


class SampleTests(unittest.TestCase):
    def test_readme_sections(self) -> None:
        for name in SAMPLES:
            text = (ROOT / "samples" / name / "README.md").read_text(encoding="utf-8")
            with self.subTest(sample=name):
                self.assertEqual(README_SECTIONS, re.findall(r"^## (.+)$", text, re.M))

    def test_kickoff_page_follows_the_template(self) -> None:
        # Each sample is laid out the way a customer's working folder is: the kickoff page holds the context.
        sections = re.findall(r"^## (.+)$", TEMPLATE.read_text(encoding="utf-8"), re.M)
        for name in SAMPLES:
            text = (ROOT / "samples" / name / "discovery" / "kickoff.md").read_text(encoding="utf-8")
            with self.subTest(sample=name):
                self.assertEqual(sections, re.findall(r"^## (.+)$", text, re.M))
                self.assertRegex(text, r"\*\*Which direction is good:\*\* (Higher|Lower) is better")
                self.assertIn("**Sample data:** Yes", text)
                self.assertEqual(5, len(re.findall(r"^\d\. \*\*", text, re.M)), "five candidate use cases")
                self.assertNotRegex(text, r"\[(the|a|what|who|value|from|its|regulation)\b", "a template placeholder left in")

    def test_facilitator_notes(self) -> None:
        for name in SAMPLES:
            text = (ROOT / "facilitator" / f"{name}.md").read_text(encoding="utf-8")
            block = re.search(r"```yaml\n(expectations:.*?)```", text, re.S)
            with self.subTest(sample=name):
                self.assertIn("spoiler", text[:500].lower())
                self.assertIsNotNone(block)
                for key in EXPECTATION_KEYS:
                    self.assertRegex(block.group(1), rf"(?m)^\s+{key}:")

    def test_no_answers_inside_the_working_folder(self) -> None:
        """The assistant can read the whole sample folder, so the answers live in facilitator/."""
        for name in SAMPLES:
            # Only the committed sample: a demo run inside the folder (discovery/<project>/) is ignored by git.
            tracked = subprocess.run(["git", "ls-files", f"samples/{name}"], cwd=ROOT, capture_output=True, text=True).stdout.split()
            for path in [ROOT / f for f in tracked] or (ROOT / "samples" / name).rglob("*"):
                if path.is_file():
                    text = path.read_text(encoding="utf-8").lower()
                    with self.subTest(file=str(path.relative_to(ROOT))):
                        self.assertNotIn("expectations:", text)
                        self.assertNotIn("spoiler", text)
                        self.assertNotIn("designed truth", text)

    def test_records_are_unique_and_anonymized(self) -> None:
        for name in SAMPLES:
            folder = ROOT / "samples" / name / "discovery"
            texts, files = [], list(folder.rglob("*.csv")) + list(folder.rglob("*.md"))
            for path in folder.rglob("*.csv"):
                rows = list(csv.DictReader(path.open(encoding="utf-8")))
                texts += [r["text"] for r in rows if "text" in r]
            with self.subTest(sample=name):
                self.assertTrue(files)
                self.assertEqual(len(texts), len(set(texts)), "duplicate record texts")
                for path in files:
                    self.assertNotRegex(path.read_text(encoding="utf-8"), r"[\w.+-]+@[\w-]+\.[a-z]{2,}", str(path))

    def test_generators_reproduce_the_committed_data(self) -> None:
        for name in SAMPLES:
            folder = ROOT / "samples" / name / "discovery"
            before = digest(folder)
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "samples" / f"{name}.py")],
                                    capture_output=True, text=True, check=False)
            with self.subTest(sample=name):
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(before, digest(folder), "generator output differs from the files in the repo")


if __name__ == "__main__":
    unittest.main()
