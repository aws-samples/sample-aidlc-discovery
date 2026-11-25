"""Checks for the journey app: the shell, the update script the skill runs, and the page's own renderer.

The update script is taken from references/journey-app.md as written, so the test runs what the assistant runs.
The renderer is the page's JavaScript, run in an isolated node vm context (skipped when node is not installed).
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "skills" / "aidlc-discovery" / "references"
APP = (REFS / "journey-app.md").read_text(encoding="utf-8")
SHELL_MD = (REFS / "journey-shell.md").read_text(encoding="utf-8")
SHELL = re.search(r"```html\n(.*)\n```", SHELL_MD, re.S).group(1)
UPDATE = re.search(r"```python\n(.*?)\n```\n", APP, re.S).group(1)
DATA = re.compile(r'(<script id="journey-data" type="application/json">)(.*?)(</script>)', re.S)
NODE = shutil.which("node")

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

# Loads the page's reading functions (between the collect markers) into an isolated vm context.
# Usage: node -e PAGE_FNS <journey.html> collect|markdown   (stdin: markdown for "markdown")
PAGE_FNS = r"""
const fs = require("fs"), vm = require("vm");
const [page, fn] = [fs.readFileSync(process.argv[1], "utf8"), process.argv[2]];
const src = page.slice(page.indexOf("/* collect:begin */"), page.indexOf("/* collect:end */"));
const api = vm.runInNewContext(src + "\n;({ collect, markdown })", {});
if (fn === "markdown") process.stdout.write(api.markdown(fs.readFileSync(0, "utf8")));
else {
  const blob = page.match(/<script id="journey-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
  process.stdout.write(JSON.stringify(api.collect(JSON.parse(blob))));
}
"""


def shape(page: str) -> str:
    return "\n".join(line.rstrip() for line in DATA.sub(r"\1\3", page).strip().splitlines())


class ShellTests(unittest.TestCase):
    def test_update_checks_the_current_shell(self) -> None:
        expected = hashlib.sha256(shape(SHELL).encode()).hexdigest()[:12]
        found = re.search(r'^SHAPE = "([0-9a-f]{12})"$', UPDATE, re.M).group(1)
        self.assertEqual(expected, found, "the shell changed: set SHAPE in references/journey-app.md to " + expected)

    def test_shell_is_self_contained_and_empty(self) -> None:
        self.assertNotRegex(SHELL, r'<(script|link|img|iframe)[^>]+(src|href)="https?:')
        self.assertEqual("", DATA.search(SHELL).group(2))
        self.assertEqual(1, SHELL_MD.count("```html"))
        for marker in ("/* collect:begin */", "/* collect:end */", 'id="now"', 'location.protocol === "file:"'):
            self.assertIn(marker, SHELL)

    def test_update_script_is_short(self) -> None:
        # The assistant types it at every step in AWS Quick: keep it small.
        self.assertLessEqual(len(UPDATE.splitlines()), 30)

    @unittest.skipUnless(NODE, "node not installed")
    def test_app_script_compiles(self) -> None:
        script = SHELL[SHELL.rindex("<script>") + 8: SHELL.rindex("</script>")]
        result = subprocess.run([NODE, "-e", "new (require('vm').Script)(require('fs').readFileSync(0, 'utf8'))"],
                                input=script, capture_output=True, text=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)


class UpdateTests(unittest.TestCase):
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
        (self.project.parent / "data").mkdir()
        (self.project.parent / "data" / "raw.md").write_text("raw customer data", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @property
    def page_file(self) -> Path:
        return self.project / "journey.html"

    def update(self, shell: bool = True, now: dict | None = None) -> subprocess.CompletedProcess:
        code = UPDATE.replace('pathlib.Path("discovery/[project]")', f"pathlib.Path({str(self.project)!r})")
        if shell:
            code = code.replace("SHELL = None", f"SHELL = {str(REFS / 'journey-shell.md')!r}")
        if now is not None:
            code = re.sub(r"^NOW = .*$", lambda m: f"NOW = {json.dumps(now)}", code, count=1, flags=re.M)
        return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=False)

    def data(self) -> dict:
        return json.loads(DATA.search(self.page_file.read_text(encoding="utf-8")).group(2))

    def page(self, fn: str = "collect", stdin: str = "") -> str:
        result = subprocess.run([NODE, "-e", PAGE_FNS, str(self.page_file), fn], input=stdin,
                                capture_output=True, text=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout

    def collect(self) -> dict:
        return json.loads(self.page())

    def test_creates_the_page_from_the_shell(self) -> None:
        result = self.update()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Journey app updated: 2 files", result.stdout)
        self.assertEqual(shape(SHELL), shape(self.page_file.read_text(encoding="utf-8")))

    def test_without_a_shell_path_it_asks_for_a_copy(self) -> None:
        result = self.update(shell=False)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("copy the shell again", result.stderr)
        self.page_file.write_text(SHELL + "\n\n", encoding="utf-8")  # a copy saved by hand, with a stray newline
        self.assertEqual(0, self.update(shell=False).returncode)

    def test_a_changed_shell_is_caught(self) -> None:
        self.page_file.write_text(SHELL.replace("var(--nav)", "var(--navy)", 1), encoding="utf-8")
        self.assertNotEqual(0, self.update(shell=False).returncode)
        self.assertEqual(0, self.update().returncode)  # with the shell path, it writes a fresh copy

    def test_reads_only_the_project_artifacts(self) -> None:
        (self.project / "prototype").mkdir()
        for name in ("v1.html", "index.html", "compare.html"):
            (self.project / "prototype" / name).write_text("<html></html>", encoding="utf-8")
        self.update()
        self.update()  # the second run must not read journey.html itself
        files = set(self.data()["files"])
        self.assertEqual({"PROJECT.md", "signals/signal-summary.md", "prototype/v1.html", "prototype/index.html"}, files)

    def test_data_is_escaped_and_carries_now(self) -> None:
        now = {"phase": "Signals", "step": "Step 2 of 6", "doing": "The team checks the inventory.", "next": "Step 3"}
        self.update(now=now)
        block = DATA.search(self.page_file.read_text(encoding="utf-8")).group(2)
        self.assertNotIn("<", block)
        self.assertEqual(now, self.data()["now"])
        self.assertEqual("demo", self.data()["project"])

    @unittest.skipUnless(NODE, "node not installed")
    def test_reads_status_and_carried_lists(self) -> None:
        self.update()
        d = self.collect()
        self.assertEqual(["Complete", "In progress", "Not started", "Not started", "Not started"],
                         [p["status"] for p in d["phases"]])
        self.assertIn("slow checkout", d["phases"][0]["key"])
        self.assertEqual({"know", "dont", "assume"}, set(d["carried"]))
        self.assertTrue(d["demo"])

    @unittest.skipUnless(NODE, "node not installed")
    def test_evidence_labels_counted_and_marked(self) -> None:
        self.update()
        d = self.collect()
        self.assertEqual({"known": 1, "assumed": 1, "needs": 1}, d["evidence"])
        doc = next(x for x in d["phases"][0]["docs"] if x["path"] == "signals/signal-summary.md")
        self.assertIn('class="ev ev-known"', doc["html"])
        self.assertIn('class="ev ev-needs"', doc["html"])
        self.assertIn('data-doc="signals/hypotheses.md"', doc["html"])
        self.assertNotIn("<script>alert", doc["html"])

    @unittest.skipUnless(NODE, "node not installed")
    def test_missing_artifacts_listed(self) -> None:
        self.update()
        missing = [x["path"] for x in self.collect()["phases"][0]["docs"] if x["status"] == "Missing"]
        self.assertEqual(["signals/team-expectations.md", "signals/hypotheses.md"], missing)

    @unittest.skipUnless(NODE, "node not installed")
    def test_prototypes_and_decision(self) -> None:
        (self.project / "prototype").mkdir()
        for n in (1, 2):
            (self.project / "prototype" / f"v{n}.html").write_text(f"<html><script>v{n}</script></html>", encoding="utf-8")
        shutil.copy(self.project / "prototype" / "v2.html", self.project / "prototype" / "index.html")
        (self.project / "validate").mkdir()
        (self.project / "validate" / "decision.md").write_text("# Decision\n\n**Decision:** commit, test first\n", encoding="utf-8")
        self.update()
        d = self.collect()
        self.assertEqual([("v1", False), ("v2", True)], [(p["id"], p["current"]) for p in d["prototypes"]])
        self.assertEqual("commit", d["decision"]["value"])
        self.assertEqual("In progress", d["phases"][2]["status"])  # versions exist, though the board says Not started

    @unittest.skipUnless(NODE, "node not installed")
    def test_markdown_renderer(self) -> None:
        self.update()
        md = "## Title\n\n- one\n  - nested\n- two\n\n1. first\n\n```\n<b>\n```\n\n> quote\n\n日本語の*強調*ではない\n"
        out = self.page("markdown", md)
        self.assertIn("<h2>Title</h2>", out)
        self.assertEqual(2, out.count("<ul>"))
        self.assertIn("<ol>", out)
        self.assertIn("&lt;b&gt;", out)
        self.assertIn("<blockquote>", out)
        self.assertNotIn("<em>", out)  # as in the Python renderer: no emphasis glued to letters on both sides

    @unittest.skipUnless(NODE, "node not installed")
    def test_reads_the_project_md_template(self) -> None:
        entry = (ROOT / "skills" / "aidlc-discovery" / "SKILL.md").read_text(encoding="utf-8")
        template = entry.split("`PROJECT.md`, written at Setup and kept current:", 1)[1].split("```markdown\n", 1)[1].split("```", 1)[0]
        board = ("| # | Phase | Status | Key artifact |\n|---|-------|--------|--------------|\n"
                 "| 1 | Signals | Complete | Top signal: slow checkout |\n| 2 | Working Backwards | In progress | |\n"
                 "| 3 | Prototype | Not started | |\n| 4 | Validate | Not started | |\n| 5 | Handoff | Not started | |\n\n"
                 "**What we know:** checkout is slow.\n")
        filled = template.replace("[The progress board's first table, with its Key artifact column, and the three lists below it]", board)
        (self.project / "PROJECT.md").write_text(filled.replace("[product]", "Demo"), encoding="utf-8")
        self.update()
        d = self.collect()
        self.assertEqual("Discovery: Demo", d["title"])
        self.assertEqual(["Complete", "In progress", "Not started", "Not started", "Not started"], [p["status"] for p in d["phases"]])
        self.assertEqual("Top signal: slow checkout", d["phases"][0]["key"])
        self.assertIn("Direction", [f["k"] for f in d["facts"]])
        self.assertIn("know", d["carried"])
        self.assertTrue(d["demo"])


if __name__ == "__main__":
    unittest.main()
