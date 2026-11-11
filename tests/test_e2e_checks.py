"""Self-tests for the end-to-end checks, on a synthetic workspace. Free: no model calls."""

from __future__ import annotations

import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "e2e"))
import checks  # noqa: E402  # pyright: ignore[reportMissingImports]

PROJECT = "supply"
EXPECT = {"top_signal": "reorder | repeat order", "loud_request": "price", "distractor_fails_gate": "recipe inspiration",
          "build_first_or_learn": "reorder my usual with a delivery slot", "data_input": "production"}


def build(root: Path) -> Path:
    d = root / "discovery" / PROJECT
    for rel in checks.required_artifacts():
        if rel.endswith("*.md"):
            for name in ("marco", "sofia"):
                p = d / rel[:-4] / f"{name}.md"
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(f"# {name.title()}\n", encoding="utf-8")
        else:
            p = d / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("# artifact\n", encoding="utf-8")
    (d / "signals" / "team-expectations.md").write_text("# Team expectations\n", encoding="utf-8")
    time.sleep(0.02)
    (d / "signals" / "signal-summary.md").unlink()
    (d / "signals" / "signal-summary.md").write_text("# Signals\n\n### 1. Repeat order on a phone takes too long\n", encoding="utf-8")
    (d / "working-backwards" / "use-case-scoring.md").write_text(
        "# Scoring\n\n## Gate\n| # | Use case | Result |\n| 5 | Recipe inspiration | Drop |\n\n"
        "## Overrides\n| # | Dimension | Draft | Team | Reason |\n| 2 | Pain (price matching) | 2 | 5 | reps hear it |\n\n"
        "## Taken forward\nReorder my usual, with the delivery slot, build first\n", encoding="utf-8")
    (d / "working-backwards" / "prfaq.md").write_text("# PR/FAQ\n\n## Readiness check\nVerdict: AMBER, two gaps\n\n## Prototype scope\n", encoding="utf-8")
    (d / "working-backwards" / "gtm.md").write_text("## 1. First adopters · Status: **validated**\n", encoding="utf-8")
    (d / "validate" / "decision.md").write_text(
        "# Decision\n**Decision:** commit, test first\n**Conditions before the build:** 8 of 10 owners confirm\n", encoding="utf-8")
    proto = d / "prototype"
    shell = checks.shell_html()
    for v in ("v1", "v2"):
        (proto / f"{v}.html").write_text(shell, encoding="utf-8")
    (proto / "index.html").write_text(shell, encoding="utf-8")
    (proto / "versions.md").write_text("| v1 | first |\n| v2 | iteration |\n", encoding="utf-8")
    links = "\n".join(f"- [x](../{p.relative_to(d)})" for p in [d / "working-backwards" / "prd.md", proto / "v1.html"])
    body = {"Context": "Date: 2026-01-01 | Route: AI-DLC classic | Data: synthetic", "Full artifacts": links}
    brief = "# Discovery brief\n\n" + "".join(f"## {i}. {t}\n{body.get(t, 'Content.')}\n\n"
                                               for i, t in enumerate(checks.brief_sections(), 1))
    (d / "handoff").mkdir(parents=True, exist_ok=True)
    (d / "handoff" / "discovery-brief.md").write_text(brief, encoding="utf-8")
    (d / "handoff" / "next-steps.md").write_text("# Next steps\n\n## Roadmap: Now, Next, Later\n**Now** x\n**Next** y\n**Later** z\n", encoding="utf-8")
    (root / ".gitignore").write_text("discovery/data/\n", encoding="utf-8")
    return d


class ChecksTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self.tmp.name)
        self.d = build(self.ws)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def failed(self) -> set[str]:
        found = checks.check_workshop(self.ws, PROJECT) + checks.check_outcome(self.ws, PROJECT, EXPECT) \
            + checks.check_team(self.ws, PROJECT, EXPECT)
        return {c.id for c in found if not c.passed}

    def test_a_good_workspace_passes(self) -> None:
        self.assertEqual(set(), self.failed())

    def test_gate_rows_by_number_are_understood(self) -> None:
        scoring = self.d / "working-backwards" / "use-case-scoring.md"
        scoring.write_text("## Candidates\n| 5 | Recipe and menu inspiration | Chefs |\n\n## Gate\n| # | Passed | Reason |\n| 5 | ❌ | Painkiller |\n\n"
                           "## Overrides\n| 2 | Pain (price) | 2 | 5 | reps |\n\n## Taken forward\nReorder my usual\n", encoding="utf-8")
        self.assertNotIn("O02", self.failed())
        scoring.write_text(scoring.read_text(encoding="utf-8").replace("| 5 | ❌ | Painkiller |", "| 5 | ✅ | |"), encoding="utf-8")
        self.assertIn("O02", self.failed())

    def test_a_distractor_deferred_at_the_gate_fails(self) -> None:
        scoring = self.d / "working-backwards" / "use-case-scoring.md"
        scoring.write_text(scoring.read_text(encoding="utf-8").replace("| 5 | Recipe inspiration | Drop |", "| 5 | Recipe inspiration | ❌ Deferred |"), encoding="utf-8")
        self.assertIn("O02", self.failed())

    def test_formats_from_a_hand_run_are_understood(self) -> None:
        scoring = self.d / "working-backwards" / "use-case-scoring.md"
        text = scoring.read_text(encoding="utf-8")
        text = "## Merges (before the gate)\nNothing merged.\n\n" + text.replace("## Gate", "## Gate (draft, for the team to confirm)")
        text = text.replace("| 2 | Pain (price matching) | 2 | 5 | reps hear it |", "| 2 | Pain (price matching) | 2 | 4 | reps hear it |")
        scoring.write_text(text, encoding="utf-8")
        decision = self.d / "validate" / "decision.md"
        decision.write_text(decision.read_text(encoding="utf-8").replace("**Decision:** commit", "**Decision:** **Commit"), encoding="utf-8")
        v1 = self.d / "prototype" / "v1.html"
        v1.write_text(v1.read_text(encoding="utf-8").rstrip() + "\n\n", encoding="utf-8")
        self.assertEqual(set(), self.failed())

    def test_telemetry_checks(self) -> None:
        expect = {**EXPECT, "say_and_do": "true", "telemetry_trap": "payment", "telemetry_only": "alert | notification",
                  "feasibility_evidence": "reissue"}
        summary = self.d / "signals" / "signal-summary.md"
        scoring = self.d / "working-backwards" / "use-case-scoring.md"
        failed = lambda: {c.id for c in checks.check_outcome(self.ws, PROJECT, expect) if not c.passed}
        self.assertTrue({"O04", "O06", "O07"} <= failed())
        summary.write_text(summary.read_text(encoding="utf-8") + "\n## Say and do\n| Theme | Say | Do |\n| Late alerts | none | p95 41 min |\n", encoding="utf-8")
        scoring.write_text(scoring.read_text(encoding="utf-8") + "\nFeasibility 3: reissue errors 5%\n", encoding="utf-8")
        self.assertEqual(set(), failed())
        summary.write_text(summary.read_text(encoding="utf-8").replace("### 1. Repeat order on a phone takes too long", "### 1. Payment timeouts"), encoding="utf-8")
        self.assertIn("O05", failed())

    def test_signals_candidates_and_ai_block(self) -> None:
        expect = {**EXPECT, "signals_candidates": "2", "ai_feature_block": "true"}
        failed = lambda: {c.id for c in checks.check_outcome(self.ws, PROJECT, expect) if not c.passed}
        self.assertTrue({"O08", "O09", "O10"} <= failed())
        scoring = self.d / "working-backwards" / "use-case-scoring.md"
        scoring.write_text(scoring.read_text(encoding="utf-8") + "\n## From Signals\n| Candidate | Evidence | Kept or dropped | Reason |\n|---|---|---|---|\n| Late disruption alerts | p95 41 min | Kept | ours |\n| Fares | 29 records | Dropped | commercial |\n", encoding="utf-8")
        cases = "".join(f"| {i} | {'Negative' if i > 4 else 'Typical'} | input | output | quote |\n" for i in range(1, 7))
        (self.d / "working-backwards" / "prd.md").write_text("# PRD\n\n## AI feature block\n### Evaluation cases\n" + cases, encoding="utf-8")
        (self.d / "validate" / "decision.md").write_text((self.d / "validate" / "decision.md").read_text(encoding="utf-8") + "\nAI quality target: 8 of 10 typical accepted\n", encoding="utf-8")
        self.assertFalse({"O08", "O09", "O10"} & failed())

    def test_a_missing_roadmap_fails(self) -> None:
        (self.d / "handoff" / "next-steps.md").write_text("# Next steps\n", encoding="utf-8")
        self.assertIn("D20", self.failed())

    def test_missing_prd_fails(self) -> None:
        (self.d / "working-backwards" / "prd.md").unlink()
        self.assertIn("D01", self.failed())

    def test_a_prototype_not_built_from_the_shell_fails(self) -> None:
        (self.d / "prototype" / "v2.html").write_text("<html><body>my own layout</body></html>", encoding="utf-8")
        self.assertIn("D11", self.failed())

    def test_critique_in_validate_fails(self) -> None:
        (self.d / "validate" / "persona-critique.md").write_text("x", encoding="utf-8")
        self.assertIn("D14", self.failed())

    def test_gtm_left_as_draft_fails(self) -> None:
        (self.d / "working-backwards" / "gtm.md").write_text("## 4. Viability check · Status: draft\n", encoding="utf-8")
        self.assertIn("D16", self.failed())

    def test_analysis_before_expectations_fails(self) -> None:
        th = self.d / "signals" / "team-expectations.md"
        th.unlink()
        time.sleep(0.02)
        th.write_text("# written after\n", encoding="utf-8")
        self.assertIn("D17", self.failed())

    def test_wrong_top_signal_and_wrong_pick_fail(self) -> None:
        (self.d / "signals" / "signal-summary.md").write_text("### 1. Price is too high\n", encoding="utf-8")
        scoring = self.d / "working-backwards" / "use-case-scoring.md"
        scoring.write_text(scoring.read_text(encoding="utf-8").replace("Reorder my usual, with the delivery slot", "Price matching"), encoding="utf-8")
        self.assertTrue({"O01", "O03"} <= self.failed())

    def test_leaks_fail(self) -> None:
        with (self.d / "handoff" / "discovery-brief.md").open("a", encoding="utf-8") as f:
            f.write("\nContact jane.doe@anycompany.com about 006Ab00000XyZ12AAB\n")
        self.assertTrue({"D06", "D07"} <= self.failed())

    def test_no_conditions_fails_the_team_check(self) -> None:
        (self.d / "validate" / "decision.md").write_text("**Decision:** commit\n**Conditions before the build:** none\n", encoding="utf-8")
        self.assertIn("T02", self.failed())

    def test_mismatch_and_missing_prd_checks(self) -> None:
        data = self.ws / "discovery" / "data"
        data.mkdir(parents=True, exist_ok=True)
        (data / "made-up.json").write_text("[]", encoding="utf-8")
        mismatch = {c.id for c in checks.check_mismatch(self.ws, PROJECT, set(), "no options offered") if not c.passed}
        self.assertTrue({"N01", "N02", "N03"} <= mismatch)
        refused = {c.id for c in checks.check_missing_prd(self.ws, PROJECT, "The PRD is missing.") if not c.passed}
        self.assertEqual({"N04"}, refused)  # the brief exists in this workspace, so N04 fails; N05 passes


if __name__ == "__main__":
    unittest.main()
