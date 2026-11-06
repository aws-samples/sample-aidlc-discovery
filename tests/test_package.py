"""Package contract tests: every skill loads, links resolve, and the phases connect.

Run: python3 -m unittest discover tests
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
ENTRY = "aidlc-discovery"
REQUIRED_JOBS = [
    "discovery-signals", "discovery-personas", "discovery-use-case-scoring",
    "discovery-working-backwards", "discovery-gtm", "discovery-prototype",
    "discovery-validate", "discovery-handoff",
]
OPTIONAL = ["discovery-signal-brief", "discovery-survey", "discovery-team-space"]
SECTIONS = ["## Overview", "## Workflow", "## Output", "## Lessons Learned"]


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, "missing frontmatter"
    fields = {}
    for line in match.group(1).splitlines():
        key = re.match(r"^([a-z_-]+):\s*(.*)$", line)
        if key:
            fields[key.group(1)] = key.group(2)
    return fields


def skill_dirs() -> list[Path]:
    return sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


class SkillShapeTests(unittest.TestCase):
    def test_the_twelve_skills_exist(self) -> None:
        self.assertEqual(sorted([ENTRY, *REQUIRED_JOBS, *OPTIONAL]), [p.name for p in skill_dirs()])

    def test_frontmatter_and_sections(self) -> None:
        for d in skill_dirs():
            text = (d / "SKILL.md").read_text(encoding="utf-8")
            fm = frontmatter(text)
            with self.subTest(skill=d.name):
                self.assertEqual(d.name, fm.get("name"))
                for key in ("display_name", "description", "trigger", "tools", "version"):
                    self.assertIn(key, fm)
                self.assertTrue(fm["description"].startswith('"') and fm["description"].endswith('"'),
                                "keep description a one-line quoted string")
                for section in SECTIONS:
                    self.assertIn(section, text)
                self.assertLess(len(text.splitlines()), 500)

    def test_every_input_placeholder_is_declared(self) -> None:
        for d in skill_dirs():
            text = (d / "SKILL.md").read_text(encoding="utf-8")
            declared = set(re.findall(r"^\s+- name: ([a-z_]+)$", text, re.M))
            used = set(re.findall(r"\{\{([a-z_]+)\}\}", text))
            with self.subTest(skill=d.name):
                self.assertLessEqual(used, declared)


class LinkTests(unittest.TestCase):
    def test_referenced_files_exist(self) -> None:
        for d in skill_dirs():
            for md in d.rglob("*.md"):
                for ref in re.findall(r"`((?:references|templates)/[^`]+)`", md.read_text(encoding="utf-8")):
                    with self.subTest(file=str(md.relative_to(ROOT)), ref=ref):
                        self.assertTrue((d / ref).is_file() or (md.parent / ref).is_file())

    def test_entry_depends_on_every_required_job(self) -> None:
        fm = frontmatter((SKILLS / ENTRY / "SKILL.md").read_text(encoding="utf-8"))
        deps = re.findall(r"[a-z-]+", fm["depends-on"])
        self.assertEqual(sorted(REQUIRED_JOBS), sorted(deps))

    def test_no_leftover_agent_paths(self) -> None:
        for md in SKILLS.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            with self.subTest(file=str(md.relative_to(ROOT))):
                self.assertNotIn("AGENT.md", text)
                self.assertNotRegex(text, r"agents/0[1-5]-")


class HandoffContractTests(unittest.TestCase):
    HANDOFF = SKILLS / "discovery-handoff" / "SKILL.md"

    def table(self) -> list[tuple[str, str, str]]:
        text = self.HANDOFF.read_text(encoding="utf-8")
        section = text.split("### Step 1:", 1)[1].split("### Step 2:", 1)[0]
        return re.findall(r"^\| (.+?) \| `([^`]+)` \| ([a-z-]+) \|$", section, re.M)

    def test_every_required_artifact_is_written_by_its_skill(self) -> None:
        rows = self.table()
        self.assertGreaterEqual(len(rows), 13)
        for label, path, producer in rows:
            text = "\n".join(p.read_text(encoding="utf-8") for p in (SKILLS / producer).rglob("*.md"))
            target = path.replace("*.md", "")
            with self.subTest(artifact=label):
                self.assertIn(target, text, f"{producer} never writes {path}")

    def test_brief_has_fifteen_sections_in_order(self) -> None:
        text = self.HANDOFF.read_text(encoding="utf-8")
        template = text.split("## Output", 1)[1].split("## Lessons Learned", 1)[0]
        titles = re.findall(r"^## (\d+)\. (.+)$", template, re.M)
        self.assertEqual([str(i) for i in range(1, 16)], [n for n, _ in titles])
        self.assertEqual("Decision", titles[1][1])
        self.assertEqual("Full artifacts", titles[-1][1])

    def test_aidlc_contract(self) -> None:
        text = self.HANDOFF.read_text(encoding="utf-8")
        for needle in ("2.10.0", "200,000", "aidlc/spaces/[space]/knowledge/aidlc-product-agent/",
                       "/aidlc workshop", "/aidlc classic", "discovery/data/", "CRM"):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()


class PrototypeTemplateTests(unittest.TestCase):
    """The shells ship as one HTML code block inside a Markdown reference, which Quick can read."""

    REFS = SKILLS / "discovery-prototype" / "references"

    def html(self, name: str) -> str:
        text = (self.REFS / name).read_text(encoding="utf-8")
        blocks = re.findall(r"````html\n(.*?)````", text, re.S)
        self.assertEqual(1, len(blocks), f"{name} must hold exactly one HTML code block")
        return blocks[0]

    def test_shells_have_one_edit_region_and_no_external_requests(self) -> None:
        for name in ("prototype-shell.md", "prototype-compare.md"):
            text = self.html(name)
            with self.subTest(template=name):
                self.assertTrue(text.lstrip().startswith("<!doctype html>"))
                self.assertEqual(1, text.count("EDIT BELOW"))
                self.assertEqual(1, text.count("EDIT ABOVE"))
                self.assertLess(text.index("EDIT BELOW"), text.index("EDIT ABOVE"))
                self.assertNotRegex(text, r"(?:src|href)=[\"']https?://")
                self.assertNotIn("innerHTML", text)

    def test_shell_provides_the_three_views(self) -> None:
        text = self.html("prototype-shell.md")
        for needle in ('href="#/flow"', 'href="#/mobile"', 'href="#/desktop"', 'id="tm"', "data-screen", "data-test-moment"):
            self.assertIn(needle, text)
