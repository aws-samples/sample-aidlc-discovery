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
    "discovery-working-backwards", "discovery-prototype",
    "discovery-validate", "discovery-handoff",
]
OPTIONAL = ["discovery-signal-brief", "discovery-survey"]
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
                       "/aidlc workshop", "[scope] [intent description]", "discovery/data/", "CRM"):
            self.assertIn(needle, text)


class ProjectLanguageTests(unittest.TestCase):
    def test_project_language_contract(self) -> None:
        entry = (SKILLS / ENTRY / "SKILL.md").read_text(encoding="utf-8")
        config = (SKILLS / ENTRY / "config.default.md").read_text(encoding="utf-8")
        persona = (SKILLS / "discovery-personas" / "references" / "persona-document.md").read_text(encoding="utf-8")
        self.assertIn('project_language: ""', config)
        self.assertIn("Project language: [language]", entry)
        self.assertIn("**Project language.** Write every message", entry)
        self.assertIn("- **Background:**", persona)


class MethodContractTests(unittest.TestCase):
    """Fixes from the Cowork end-to-end run (2026-11-25): each closes a gap a run had to guess at."""

    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_unattended_runs_have_a_default_for_every_team_decision(self) -> None:
        text = self.read("skills/aidlc-discovery/SKILL.md")
        table = text.split("## Unattended runs", 1)[1].split("\n## ", 1)[0]
        for decision in ("direction of the metric", "expectations before Signals", "Candidates from Signals",
                         "re-scoring", "Prototype version handed off", "Commit, pivot, or park", "riskiest assumption is open", "Build route"):
            with self.subTest(decision=decision):
                self.assertRegex(table, rf"(?m)^\| [^|]*{re.escape(decision)}[^|]*\| .+ \|$")
        self.assertIn("take the recommended answer", table)
        self.assertIn("none given (unattended run)", table)
        self.assertNotIn("in the team's words", table)

    def test_missing_config_keys_fall_back_to_the_defaults(self) -> None:
        self.assertIn("a key that `config.md` does not set takes its value from `config.default.md`",
                      self.read("skills/aidlc-discovery/SKILL.md"))

    def test_scoring_says_how_many_candidates_reach_the_gate(self) -> None:
        self.assertIn("up to eight candidates can reach the gate", self.read("skills/discovery-use-case-scoring/SKILL.md"))

    def test_brief_tells_greenfield_from_code_not_in_the_folder(self) -> None:
        section = self.read("skills/discovery-handoff/SKILL.md").split("## 12. Current product", 1)[1].split("## 13.", 1)[0]
        self.assertIn("Greenfield: there is no product yet.", section)
        self.assertIn("Existing product: no current-product map", section)

    def test_templates_use_no_arrows(self) -> None:
        for path in SKILLS.rglob("*.md"):
            with self.subTest(file=str(path.relative_to(SKILLS))):
                self.assertNotRegex(path.read_text(encoding="utf-8"), r"[↑↓]")

    def test_persona_count_says_what_it_covers(self) -> None:
        text = self.read("skills/discovery-personas/SKILL.md")
        self.assertIn("the satisfied customer is one of them", text)
        self.assertIn("A buyer persona, when the buyer is a different person, comes on top", text)

    def test_prfaq_word_range_is_a_check_not_a_target(self) -> None:
        text = self.read("skills/discovery-working-backwards/references/prfaq-generation.md")
        self.assertIn("The range is a check, not a target.", text)
        self.assertIn("Never add or cut words only to reach the range", text)

    def test_test_moment_rule_fits_any_flow_length(self) -> None:
        text = self.read("skills/discovery-prototype/references/html-prototype.md")
        self.assertNotIn("two taps", text)
        self.assertIn("every screen before it is a step of the main task", text)

    def test_say_and_do_has_one_column_name(self) -> None:
        header = r"\| Theme \| What customers say \| What the systems show \| Reading \|"
        for rel in ("skills/discovery-signals/SKILL.md", "skills/discovery-signals/references/telemetry-analysis.md"):
            with self.subTest(file=rel):
                self.assertRegex(self.read(rel), header)

    def test_identifiers_in_quotes_become_bracketed_roles(self) -> None:
        self.assertIn("the quote still counts as verbatim", self.read("skills/aidlc-discovery/SKILL.md"))
        self.assertIn("identifiers replaced by a bracketed role",
                      self.read("skills/discovery-personas/references/persona-document.md"))

    def test_press_release_paragraph_two_may_open_with_the_problem(self) -> None:
        self.assertIn("except paragraph 2, whose job is the problem",
                      self.read("skills/discovery-working-backwards/references/prfaq-generation.md"))

    def test_revenue_amounts_not_shares_are_kept_out(self) -> None:
        for rel in ("skills/aidlc-discovery/SKILL.md", "skills/discovery-handoff/SKILL.md"):
            with self.subTest(file=rel):
                self.assertIn('a share that sizes a segment, such as "a third of revenue", is fine', self.read(rel).replace("A share", "a share"))

    def test_signal_scores_use_the_bands_validate_uses(self) -> None:
        signals = self.read("skills/discovery-signals/SKILL.md")
        prioritization = self.read("skills/discovery-validate/references/prioritization.md")
        for signals_band, validate_band in (("under 5%", "< 5%"), ("5% to 15%", "5-15%"), ("over 15%", "> 15%"),
                                            ("one niche segment", "One niche segment")):
            with self.subTest(band=signals_band):
                self.assertIn(signals_band, signals)
                self.assertIn(validate_band, prioritization)

    def test_persona_background_order(self) -> None:
        text = self.read("skills/discovery-personas/SKILL.md")
        order = ["(from the data)", "(from the data's market", "(from the company's home market", "(from the project language"]
        self.assertEqual(order, sorted(order, key=text.index))

    def test_project_md_has_one_template(self) -> None:
        text = self.read("skills/aidlc-discovery/SKILL.md")
        template = text.split("`PROJECT.md`, written at Setup and kept current:", 1)[1].split("```", 2)[1]
        for part in ("Project language: [language]", "| Field | Value | Status |", "| Direction |",
                     "## Phase status", "## Open items", "## Unattended choices", "| Decision | Choice | Source |"):
            with self.subTest(part=part):
                self.assertIn(part, template)

    def test_candidates_keep_the_teams_name(self) -> None:
        text = self.read("skills/discovery-use-case-scoring/SKILL.md")
        self.assertIn("| # | Name | Use case (problem) |", text)
        self.assertIn("#[N] [Name]: [problem]", text)

    def test_no_time_estimates_for_phases_or_steps(self) -> None:
        allowed = ("under five minutes", "prototype in an hour", "is a symptom")  # a limit, a size check, an example
        for path in SKILLS.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r"[^.|]*\b(\d+|five|ten)[- ](minutes?|hours?)\b[^.|]*", text, re.I):
                with self.subTest(file=str(path.relative_to(SKILLS)), text=match.group(0).strip()[:80]):
                    self.assertTrue(any(a in match.group(0) for a in allowed))
        self.assertNotIn("how long each takes", self.read("skills/aidlc-discovery/SKILL.md"))

    def test_finished_press_release_has_no_placeholders(self) -> None:
        text = self.read("skills/discovery-working-backwards/references/prfaq-generation.md")
        self.assertIn("No placeholders such as `[City]` or `[Name]` in the finished release", text)
        self.assertIn("use the title alone", text)
        self.assertIn("write around a missing fact", self.read("skills/aidlc-discovery/SKILL.md"))

    def test_steps_read_only_what_exists_by_then(self) -> None:
        readiness = self.read("skills/discovery-working-backwards/references/readiness-check.md")
        self.assertNotIn("the PRD so far", readiness)
        self.assertIn("before the PRD", readiness)
        self.assertIn("draft the feature description", self.read("skills/discovery-working-backwards/SKILL.md"))
        proto = self.read("skills/discovery-prototype/SKILL.md")
        self.assertLess(proto.index("Write the first entry in `prototype/versions.md`"), proto.index("Then open it on the **Flow** view"))

    def test_kickoff_page_is_what_setup_reads(self) -> None:
        page = self.read("skills/aidlc-discovery/templates/kickoff.md")
        for section in ("## The product", "## The team", "## The business metric", "## Ideas we already have", "## The data"):
            self.assertIn(section, page)
        self.assertIn("Which direction is good", page)  # setup never assumes the direction
        self.assertIn("discovery/kickoff.md", page)
        entry = self.read("skills/aidlc-discovery/SKILL.md")
        self.assertIn("discovery/kickoff.md", entry)
        self.assertIn("templates/kickoff.md", entry)
        self.assertNotIn("scenario", entry.lower())
        ja = self.read("facilitator/ja/kickoff.md")
        self.assertEqual(page.count("\n## "), ja.count("\n## "))  # the translation keeps every section

    def test_plain_language_applies_to_every_reply_and_question(self) -> None:
        entry = self.read("skills/aidlc-discovery/SKILL.md")
        rule = entry.split("12. **Plain writing, everywhere.**", 1)[1].split("\n", 1)[0]
        for needle in ("every question", "answer options", "question cards", "second language", "no idioms",
                       "references/plain-writing.md", "before your first reply"):
            self.assertIn(needle, rule)
        plain = self.read("skills/aidlc-discovery/references/plain-writing.md")
        for needle in ("**Say it literally.**", "bear on", "**Short sentences.**", "**Plain questions.**", "second language"):
            self.assertIn(needle, plain)

    def test_skills_are_not_written_for_the_samples(self) -> None:
        # The skills take their context from the kickoff page; no sample's product or answer belongs in them.
        words = re.compile(r"AnyCompany|airline|flight|passenger|rebook|insurer|claim status|telehealth|broker", re.I)
        for path in sorted((ROOT / "skills").rglob("*.md")) + sorted((ROOT / "cowork").rglob("*.md")):
            if path.name == "journey-shell.md":
                continue
            with self.subTest(file=str(path.relative_to(ROOT))):
                found = words.search(path.read_text(encoding="utf-8"))
                self.assertIsNone(found, found and found.group(0))

    def test_samples_state_the_direction_of_the_metric(self) -> None:
        for rel in ("samples/anycompany-air/discovery/kickoff.md", "samples/anycompany-health/discovery/kickoff.md"):
            with self.subTest(sample=rel):
                self.assertRegex(self.read(rel), r"\*\*Which direction is good:\*\* (Higher|Lower) is better")


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

    def test_shell_provides_the_views(self) -> None:
        text = self.html("prototype-shell.md")
        for needle in ('href="#/flow"', 'href="#/mobile"', 'href="#/desktop"', 'href="#/replay"', 'id="tm"', "data-screen", "data-test-moment"):
            self.assertIn(needle, text)

    def test_walkthroughs_start_empty_inside_the_edit_region(self) -> None:
        text = self.html("prototype-shell.md")
        region = text[text.index("EDIT BELOW"):text.index("EDIT ABOVE")]
        self.assertIn('<script id="persona-walkthroughs">\nconst WALKTHROUGHS = [];\n</script>', region)
