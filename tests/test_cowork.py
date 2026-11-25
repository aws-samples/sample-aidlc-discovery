"""Checks for the Cowork build (scripts/build.py --target cowork) and the journey app renderer."""

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
sys.path.insert(0, str(ROOT / "cowork"))
import build  # noqa: E402
import journey  # noqa: E402  # pyright: ignore[reportMissingImports]

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
            for ref in re.findall(r"`(?:\$\{CLAUDE_SKILL_DIR\}/)?((?:modules|cowork)/[^`\s]+)`", path.read_text(encoding="utf-8")):
                if ref.endswith("..."):
                    continue
                with self.subTest(file=str(path.relative_to(self.skill)), ref=ref):
                    self.assertTrue((self.skill / ref).exists())

    def test_cowork_section_and_renderer_ship(self) -> None:
        self.assertIn("## Running in Cowork", self.text)
        self.assertLess(self.text.index("## Running in Cowork"), self.text.index("## Shared rules"))
        for term in ("AskUserQuestion", "create_artifact", "update_artifact", "present_files", "${CLAUDE_SKILL_DIR}"):
            self.assertIn(term, self.text)
        self.assertTrue((self.skill / "cowork" / "journey.py").is_file())
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
        self.assertIn("aidlc-discovery/cowork/journey.py", names)
        self.assertTrue(all(n.startswith("aidlc-discovery/") for n in names))

    def test_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "aidlc-discovery"
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py"), "--target", "cowork", str(out)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((out / "SKILL.md").is_file())
            self.assertTrue(list(Path(tmp).glob("aidlc-discovery-v*.skill")))


PROJECT_MD = """# Discovery project: demo

| Field | Value |
|-------|-------|
| Product | Demo app for testing |
| Note | Fictional sample. This run is a **demonstration**. |

## Progress board

| # | Phase | Status | Key artifact |
|---|-------|--------|--------------|
| 1 | Signals | Complete | Signal Analysis Report: top signal "slow checkout" |
| 2 | Working Backwards | In progress | Use case scoring: #1 "fast checkout" build first |
| 3 | Prototype | Not started | |
| 4 | Validate | Not started | |
| 5 | Handoff | Not started | |

**What we know:** checkout is slow.
**What we don't know:** why.
**What we're assuming:** mobile users matter most.
"""


class JourneyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "discovery" / "demo"
        (self.project / "signals").mkdir(parents=True)
        (self.project / "PROJECT.md").write_text(PROJECT_MD, encoding="utf-8")
        (self.project / "signals" / "signal-summary.md").write_text(
            "# Signal Analysis Report\n\nCheckout is slow [Known]. People leave [Assumed].\n\n"
            "| Claim | Label |\n|---|---|\n| Cart | Needs evidence |\n\n"
            "A tricky quote: </script><script>alert(1)</script> <!-- x\n\nSee [hypotheses](hypotheses.md).\n",
            encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def data(self, page: str) -> dict:
        start = page.index('<script id="journey-data" type="application/json">')
        blob = page[page.index(">", start) + 1: page.index("</script>", start)]
        return json.loads(blob)

    def test_reads_status_and_carried_lists(self) -> None:
        d = journey.collect(self.project)
        self.assertEqual(["Complete", "In progress", "Not started", "Not started", "Not started"],
                         [p["status"] for p in d["phases"]])
        self.assertIn("slow checkout", d["phases"][0]["key"])
        self.assertEqual({"know", "dont", "assume"}, set(d["carried"]))
        self.assertTrue(d["demo"])

    def test_evidence_labels_counted_and_marked(self) -> None:
        d = journey.collect(self.project)
        self.assertEqual({"known": 1, "assumed": 1, "needs": 1}, d["evidence"])
        doc = next(x for x in d["phases"][0]["docs"] if x["path"] == "signals/signal-summary.md")
        self.assertIn('class="ev ev-known"', doc["html"])
        self.assertIn('class="ev ev-needs"', doc["html"])
        self.assertIn('data-doc="signals/hypotheses.md"', doc["html"])

    def test_missing_artifacts_listed(self) -> None:
        d = journey.collect(self.project)
        missing = [x["path"] for x in d["phases"][0]["docs"] if x["status"] == "Missing"]
        self.assertEqual(["signals/team-expectations.md", "signals/hypotheses.md"], missing)

    def test_page_is_self_contained_and_escaped(self) -> None:
        page = journey.render(self.project)
        self.assertNotRegex(page, r'<(script|link)[^>]+(src|href)="https?:')
        self.assertNotIn("alert(1)</script>", page.split("journey-data", 1)[1].split("</script>", 1)[0])
        self.assertEqual("demo", self.data(page)["project"])

    def test_prototypes_and_decision(self) -> None:
        (self.project / "prototype").mkdir()
        for n in (1, 2):
            (self.project / "prototype" / f"v{n}.html").write_text(f"<html><script>v{n}</script></html>", encoding="utf-8")
        shutil.copy(self.project / "prototype" / "v2.html", self.project / "prototype" / "index.html")
        (self.project / "validate").mkdir()
        (self.project / "validate" / "decision.md").write_text("# Decision\n\n**Decision:** commit, test first\n", encoding="utf-8")
        d = self.data(journey.render(self.project))
        self.assertEqual([("v1", False), ("v2", True)], [(p["id"], p["current"]) for p in d["prototypes"]])
        self.assertEqual("commit", d["decision"]["value"])

    def test_markdown_renderer(self) -> None:
        out = journey.markdown("## Title\n\n- one\n  - nested\n- two\n\n1. first\n\n```\n<b>\n```\n\n> quote\n")
        self.assertIn("<h2>Title</h2>", out)
        self.assertEqual(2, out.count("<ul>"))
        self.assertIn("<ol>", out)
        self.assertIn("&lt;b&gt;", out)
        self.assertIn("<blockquote>", out)

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_app_script_parses(self) -> None:
        page = journey.render(self.project)
        script = page[page.rindex("<script>") + 8: page.rindex("</script>")]
        result = subprocess.run(["node", "-e", "new Function(require('fs').readFileSync(0, 'utf8'))"],
                                input=script, capture_output=True, text=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_reads_the_project_md_template(self) -> None:
        entry = (ROOT / "skills" / "aidlc-discovery" / "SKILL.md").read_text(encoding="utf-8")
        template = entry.split("`PROJECT.md`, written at Setup and kept current:", 1)[1].split("```markdown\n", 1)[1].split("```", 1)[0]
        board = ("| # | Phase | Status | Key artifact |\n|---|-------|--------|--------------|\n"
                 "| 1 | Signals | Complete | Top signal: slow checkout |\n| 2 | Working Backwards | In progress | |\n"
                 "| 3 | Prototype | Not started | |\n| 4 | Validate | Not started | |\n| 5 | Handoff | Not started | |\n\n"
                 "**What we know:** checkout is slow.\n")
        filled = template.replace("[The progress board's first table, with its Key artifact column, and the three lists below it]", board)
        (self.project / "PROJECT.md").write_text(filled.replace("[product]", "Demo"), encoding="utf-8")
        d = journey.collect(self.project)
        self.assertEqual("Discovery: Demo", d["title"])
        self.assertEqual(["Complete", "In progress", "Not started", "Not started", "Not started"], [p["status"] for p in d["phases"]])
        self.assertEqual("Top signal: slow checkout", d["phases"][0]["key"])
        self.assertIn("Direction", [f["k"] for f in d["facts"]])
        self.assertIn("know", d["carried"])
        self.assertTrue(d["demo"])

    def test_cli(self) -> None:
        result = subprocess.run([sys.executable, str(ROOT / "cowork" / "journey.py"), str(self.project)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.project / "journey.html").is_file())


if __name__ == "__main__":
    unittest.main()
