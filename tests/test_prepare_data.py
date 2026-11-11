"""The data preparation tool removes planted personal data and leaves clean data alone.

Needs Microsoft Presidio and its spaCy model, as the tool does:
    pip install presidio-analyzer && python -m spacy download en_core_web_lg
Without them, these tests are skipped.
"""

from __future__ import annotations

import contextlib
import csv
import importlib.util
import io
import random
import re
import socket
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "tools" / "prepare-data" / "prepare_data.py"
AIR = ROOT / "samples" / "anycompany-air" / "discovery" / "data"

spec = importlib.util.spec_from_file_location("prepare_data", SCRIPT)
prepare_data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare_data)

try:
    import spacy
    ANALYZER = prepare_data.load_presidio("en", "en_core_web_lg") if spacy.util.is_package("en_core_web_lg") else None
except ImportError:
    ANALYZER = None
needs_presidio = unittest.skipUnless(ANALYZER, "needs presidio-analyzer and en_core_web_lg")


def scrubber(allow=()):
    return prepare_data.Scrubber(ANALYZER, "en", [], list(allow))

FIXTURE = [
    ["id", "date", "customer_name", "email", "customer_id", "segment", "rating", "text", "requester", "title"],
    ["T-1", "2026-05-03", "Maria Silva", "maria.silva@example.com", "C-99812", "leisure", "2",
     "Hi, my name is Maria Silva, booking ref QX7P2L on flight AB123. Call me on +44 20 7946 0958. msilva22 raised it.",
     "msilva22", "Refund for Maria"],
    ["T-2", "2026-05-04", "Tomasz Nowak", "t.nowak@example.org", "C-99812", "corporate", "1",
     "I spoke to agent Sarah who was lovely, and Joaquín sorted it, but Tomasz was charged twice on card 4111 1111 1111 1111.",
     "tnowak", "Charged twice"],
    ["T-3", "2026-05-05", "Jean Dupont", "jd@example.net", "C-10001", "leisure", "4",
     "Refund to IBAN GB82 WEST 1234 5698 7654 32 please. Mr Jones at the desk said 3 May. Thanks, Jean",
     "jdupont", "Refund request"],
    ["T-4", "2026-05-06", "Ana Costa", "ana@example.com", "C-10002", "leisure", "5",
     "My booking was cancelled and the app crashed. Account number 88812345, IP 203.0.113.7. - Ana",
     "acosta", "App crashed"],
    ["T-5", "2026-05-07", "Priya Shah", "priya@example.com", "C-10003", "leisure", "3",
     "Email me at priya.s@example.com, DM @priya_travels, or see https://example.com/trip?id=QX7P2L. The calendar view is hard to read.",
     "pshah", "Calendar view"],
]
PLANTED = ["Maria", "Silva", "maria.silva@example.com", "QX7P2L", "AB123", "7946 0958", "Sarah", "Joaquín",
           "Tomasz", "4111 1111 1111 1111", "GB82 WEST", "Jones", "3 May", "Jean", "88812345",
           "203.0.113.7", "113.7", "Ana", "priya.s@example.com", "example.com/trip", "priya_travels", "C-99812", "Nowak",
           "msilva22", "tnowak", "ops-desk@example.com"]
# A summary file, where schema.md lists every value: the email must not reach it.
SUMMARY = [["week", "contact", "tickets"], ["2026-W18", "ops-desk@example.com", "4"], ["2026-W19", "web", "7"]]
KEPT = ["said [DATE]. Thanks", "[URL]. The calendar", "My booking was cancelled and the app crashed", "The calendar view is hard to read",
        "who was lovely", "leisure", "2026-05-03"]


def run(*args: str) -> str:
    """Run the tool with the network blocked: any connection attempt fails the test."""
    def refuse(*_args, **_kwargs):
        raise AssertionError("the tool tried to open a network connection")

    out = io.StringIO()
    real = prepare_data.load_presidio
    prepare_data.load_presidio = lambda *_: ANALYZER  # load the model once for all tests
    saved = socket.socket.connect, socket.create_connection
    socket.socket.connect, socket.create_connection = refuse, refuse
    try:
        with contextlib.redirect_stdout(out):
            prepare_data.main(list(args))
    finally:
        socket.socket.connect, socket.create_connection = saved
        prepare_data.load_presidio = real
    return out.getvalue()


@needs_presidio
class PlantedPersonalData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls.tmp.name)
        source = tmp / "feedback.csv"
        with source.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(FIXTURE)
        with (tmp / "summary.csv").open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(SUMMARY)
        cls.stdout = run(str(source), str(tmp / "summary.csv"), "--preset", "airline", "--synthetic", "20",
                         "--out", str(tmp / "out"))
        cls.synthetic = tmp / "out" / "synthetic"
        cls.share = tmp / "out" / "share"
        cls.shared = "\n".join(p.read_text(encoding="utf-8") for p in cls.share.rglob("*") if p.is_file())
        cls.report = (tmp / "out" / "review-only" / "report.md").read_text(encoding="utf-8")
        with (cls.share / "feedback.csv").open(encoding="utf-8") as f:
            cls.rows = list(csv.DictReader(f))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_a_customer_handle_is_removed_and_an_allowed_brand_kept(self) -> None:
        self.assertEqual(scrubber(["AnyCompanyAir"]).scrub("@AnyCompanyAir thanks to @jo_22", True),
                         "@AnyCompanyAir thanks to [HANDLE]")

    def test_phone_formats(self) -> None:
        s = scrubber()
        for phone in ("+44 20 7946 0958", "07911 123456", "(212) 555-0147", "+49 30 901820"):
            self.assertEqual(s.scrub(f"call {phone} now", True), "call [PHONE] now", phone)

    def test_names_without_context(self) -> None:
        s = scrubber()
        self.assertEqual(s.scrub("Sarah sorted it out", True), "[PERSON_1] sorted it out")
        self.assertEqual(s.scrub("lisa was rude", True), "[PERSON_1] was rude")

    def test_signal_words_are_kept(self) -> None:
        text = "Stuck in Vienna for 48 hours, the Wi-Fi was down and Apple Pay failed today."
        self.assertEqual(scrubber().scrub(text, True), text)

    def test_dotted_names_in_fields_are_kept(self) -> None:
        self.assertEqual(scrubber().scrub("disruption.alert.send", False), "disruption.alert.send")

    def test_no_planted_value_reaches_the_shared_folder(self) -> None:
        leaked = [value for value in PLANTED if value in self.shared]
        self.assertEqual(leaked, [])

    def test_ordinary_text_and_fields_survive(self) -> None:
        for value in KEPT:
            self.assertIn(value, self.shared)

    def test_personal_columns_are_dropped(self) -> None:
        for column in ("customer_name", "email", "requester"):
            self.assertNotIn(column, self.rows[0])

    def test_logins_and_titles_are_scrubbed(self) -> None:
        self.assertRegex(self.rows[0]["text"], r"\[(PERSON_\d|LOGIN)\] raised it")
        self.assertEqual(self.rows[0]["title"], "Refund for [PERSON_1]")

    def test_synthetic_rows_are_kept_apart_and_invented(self) -> None:
        self.assertFalse((self.share / "synthetic").exists())
        self.assertIn("invented, not evidence", (self.synthetic / "README.md").read_text(encoding="utf-8"))
        with (self.synthetic / "feedback.csv").open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(row["text"].startswith("[SYNTHETIC]") for row in rows))
        invented = "\n".join(p.read_text(encoding="utf-8") for p in self.synthetic.rglob("*") if p.is_file())
        self.assertEqual([value for value in PLANTED if value in invented], [])

    def test_identifiers_become_consistent_pseudonyms(self) -> None:
        ids = [row["customer_id"] for row in self.rows]
        self.assertTrue(all(re.fullmatch(r"P-[0-9a-f]{8}", i) for i in ids))
        self.assertEqual(ids[0], ids[1])
        self.assertNotEqual(ids[0], ids[2])

    def test_placeholders_are_typed(self) -> None:
        text = self.rows[0]["text"]
        for placeholder in ("[PERSON_1]", "[FLIGHT]", "[PHONE]"):
            self.assertIn(placeholder, text)
        self.assertRegex(text, r"\[(REFERENCE|BOOKING_REF)\]")

    def test_raw_text_stays_in_the_review_folder(self) -> None:
        self.assertIn("Maria Silva", self.report)
        self.assertFalse(any("report" in p.name for p in self.share.rglob("*")))

    def test_stdout_has_counts_only(self) -> None:
        for value in PLANTED:
            self.assertNotIn(value, self.stdout)


@needs_presidio
class CleanData(unittest.TestCase):
    def test_the_air_sample_passes_through_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stdout = run(str(AIR), "--preset", "airline", "--allow", "AnyCompanyAir", "--out", tmp)
            self.assertIn("Replaced: nothing", stdout)
            for source in AIR.rglob("*.csv"):
                prepared = Path(tmp) / "share" / source.relative_to(AIR)
                self.assertEqual(prepared.read_bytes(), source.read_bytes(), source.name)


class Helpers(unittest.TestCase):
    """Parts that need no Presidio."""

    def test_people_and_title_columns(self) -> None:
        for header in ("Requester", "Assigned To", "Last Updated By", "owner", "alias", "username"):
            self.assertEqual(prepare_data.classify(header, ["x"], {}), "drop", header)
        self.assertEqual(prepare_data.classify("title", ["x"], {}), "text")
        self.assertEqual(prepare_data.classify("resolver_group", ["x"], {}), "other")
        self.assertEqual(prepare_data.known_label("alias"), "LOGIN")
        self.assertEqual(prepare_data.known_label("Assigned To"), "PERSON")

    def test_dates_to_the_month_in_any_order(self) -> None:
        to_month, order = prepare_data.to_month, prepare_data.date_order
        self.assertEqual(to_month("2026-11-10T14:21:00Z", None), "2026-11")
        self.assertEqual(to_month("10/11/2026", order(["10/11/2026", "25/11/2026"])), "2026-11")
        self.assertEqual(to_month("11/10/2026", order(["11/10/2026", "11/25/2026"])), "2026-11")
        self.assertEqual(to_month("10/11/26", None), "2026")  # cannot tell day from month: year only

    def test_synthetic_rows_never_show_a_rare_value(self) -> None:
        columns = [[f"T-{i}" for i in range(40)], ["Resolved"] * 39 + ["Escalated to Maria"],
                   ["github"] * 20 + [""] * 20, [f"2026-0{1 + i % 9}" for i in range(40)], ["text"] * 40]
        rows = prepare_data.synthesize(["id", "status", "repo", "created", "text"],
                                       ["record id", "other", "other", "date", "text"], columns, 200, random.Random(1))
        self.assertEqual(len(rows), 200)
        self.assertEqual({r[1] for r in rows}, {"Resolved"})
        self.assertTrue(40 < sum(r[2] == "" for r in rows) < 160)  # about half blank, as in the data
        self.assertTrue(all(r[0].startswith("SYN-") and r[4].startswith("[SYNTHETIC]") for r in rows))
        self.assertTrue(all(re.fullmatch(r"2026-0[1-9]", r[3]) for r in rows))


class Reviewable(unittest.TestCase):
    def test_top_level_imports_are_standard_library(self) -> None:
        """Presidio is imported in one place, load_presidio, so a reviewer finds it."""
        source = SCRIPT.read_text(encoding="utf-8")
        imports = set(re.findall(r"^(?:from|import) (\w+)", source, re.M))
        self.assertLessEqual(imports, {"__future__", "argparse", "csv", "hashlib", "hmac", "logging", "random",
                                       "re", "secrets", "statistics", "sys", "collections", "pathlib"})
        self.assertEqual(re.findall(r"^[ \t]+(?:from|import) (\w+)", source, re.M),
                         ["tldextract", "presidio_analyzer", "presidio_analyzer"])


if __name__ == "__main__":
    unittest.main()
