#!/usr/bin/env python3
"""Prepare customer data for an AI-DLC Discovery workshop, on your own machine.

The workshop's AI assistant reads customer feedback to find the problems that
matter. This script removes personal information first, so that only scrubbed
records ever reach the assistant. Read it before you run it: it is meant to be
reviewed, and it makes no network calls.

Detection is done by Microsoft Presidio (https://microsoft.github.io/presidio/),
which finds names with a local spaCy language model and recognises emails,
phone numbers, card numbers, IBANs, IP addresses, URLs, and national IDs. This
script adds what a workshop needs on top: what to do with each column, a few
patterns Presidio does not have, and a report to review before you share.

Install once (Python 3.9 to 3.13), ideally in a virtual environment:
    pip install -r requirements.txt      (Presidio, pinned to the tested version)
    python -m spacy download en_core_web_lg

Usage:
    python prepare_data.py INPUT [INPUT ...] [options]

    INPUT is a CSV file or a folder of CSV files (read recursively).

Options:
    --out DIR            where to write the results (default: prepared)
    --preset airline     add airline patterns: booking references, flight numbers
    --names-file FILE    one name per line (customers, staff) to remove anywhere
    --pattern LABEL=RE   add a pattern of your own, for example
                         --pattern POLICY='\\bPOL-\\d{6}\\b'  (repeatable)
    --allow WORD         a word that is not personal data: a capitalised word
                         taken for a name, or your own social handle without
                         the @ (repeatable)
    --drop COL           always drop this column (repeatable)
    --id COL             replace this column with a pseudonym (repeatable)
    --text COL           treat this column as free text (repeatable)
    --keep COL           keep this column untouched (repeatable; use with care)
    --dates month        shorten dates in date columns to the month
    --synthetic N        also write N invented rows per file, in the shape of the
                         prepared data, for rehearsals (never evidence)
    --language en        the language of the text (default: en)
    --spacy-model NAME   the spaCy model for that language (default: en_core_web_lg)

It writes two folders:
    DIR/share/        give this to the workshop: scrubbed CSVs and schema.md
    DIR/review-only/  keep this: report.md shows before/after examples, so it
                      contains raw text. Never share it.
    DIR/synthetic/    with --synthetic: invented rows for a rehearsal. Keep them
                      apart from share/, so they are never counted as evidence.

What it does to each column, decided from the header (override with flags):
    drop       names, logins, emails, phones, addresses, card and bank numbers,
               and people columns such as requester, assignee, or owner. Their
               values are also removed wherever they appear in the text.
    pseudonym  customer, account, booking, and similar identifiers become a
               random code that is consistent within this run and cannot be
               reversed (the key is never saved).
    text       free text: everything Presidio finds, including names.
    date       kept, or shortened to the month with --dates month.
    other      kept; Presidio still looks for identifiers in it, but not names.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import hmac
import logging
import random
import re
import secrets
import statistics
import sys
from collections import Counter
from pathlib import Path

# --------------------------------------------------------------------------
# Column rules. Headers are compared in lower case, with spaces and dashes as _.

DROP_HEADERS = re.compile(
    r"^(name|first_?name|last_?name|full_?name|surname|given_?name|"
    r"(customer|contact|passenger|patient|agent|user|account)_?name|"
    r"e_?mail(_?address)?|phone(_?number)?|mobile|telephone|tel|"
    r"(street_?|home_?|postal_?|billing_?)?address|street|post_?code|zip(_?code)?|"
    r"ip(_?address)?|card(_?number)?|iban|passport(_?number)?|"
    r"dob|date_?of_?birth|birth_?date|ssn|national_?id|"
    # people columns in ticket and CRM exports: names or logins
    r"requester|requestor|requested_?by|assignee|assigned_?to|owner|reporter|reported_?by|"
    r"(created|updated|last_?updated|modified|submitted|resolved|closed|approved)_?by|"
    r"submitter|author|approver|agent|user|username|login|alias)$"
)
LOGIN_HEADERS = re.compile(r"^(username|login|alias|user)$")  # values are logins, not names
PEOPLE_HEADERS = re.compile(r"name|^(requester|requestor|assignee|owner|reporter|submitter|author|approver|agent)$|_by$|_to$")


def known_label(header: str) -> str:
    """The placeholder for a dropped column's values when they appear in the text."""
    h = norm(header)
    if LOGIN_HEADERS.match(h):
        return "LOGIN"
    if "mail" in h:
        return "EMAIL"
    if PEOPLE_HEADERS.search(h):
        return "PERSON"
    return h.upper()
ID_HEADERS = re.compile(
    r"^((customer|user|account|member|client|booking|passenger|order|ticket|"
    r"policy|patient|loyalty|frequent_?flyer|contact)_?"
    r"(id|number|num|no|ref|reference|code)|pnr|booking_?ref|record_?locator)$"
)
TEXT_HEADERS = re.compile(
    r"^(text|comments?|feedback|body|message|verbatim|notes?|description|"
    r"review|content|transcript|summary|subject|reason_?detail|title|issue_?title|"
    r"short_?description|details)$"
)
DATE_HEADERS = re.compile(r"(^|_)(date|day|created|updated|timestamp|time)(_|$)")
LOOKS_LIKE_DATE = re.compile(r"^\s*(\d{4}-\d{2}(-\d{2})?|\d{1,2}[/.]\d{1,2}[/.]\d{2,4})")
RECORD_ID_HEADERS = {"id", "record_id"}  # the export's own row id: kept for quoting

# --------------------------------------------------------------------------
# What Presidio finds. A few of its entity types are left out on purpose,
# because on real feedback they replace the signal, not personal data:
#   LOCATION, DATE_TIME  "Vienna", "within 48 hours": often the problem itself
#   ORGANIZATION         "Wi-Fi", "Apple Pay", city names
#   URL                  dotted names such as disruption.alert.send; the URL
#                        pattern below needs http(s):// or www. instead
#   US_DRIVER_LICENSE    ordinary codes such as "Q1" and "AB123"

PRESIDIO_SKIP = {"LOCATION", "DATE_TIME", "ORGANIZATION", "URL", "US_DRIVER_LICENSE"}
NAME_ENTITIES = {"PERSON", "NRP"}  # need a language model: free-text columns only
SHORT_LABELS = {"EMAIL_ADDRESS": "EMAIL", "PHONE_NUMBER": "PHONE", "CREDIT_CARD": "CARD",
                "IBAN_CODE": "IBAN", "IP_ADDRESS": "IP", "US_BANK_NUMBER": "NUMBER"}
MIN_SCORE = 0.35  # Presidio's confidence; phone numbers it validates score 0.4

# --------------------------------------------------------------------------
# Patterns Presidio does not have. Each is (label, regex, score). When a regex
# has a group named v, only that group is replaced, so its context stays.

MONTHS = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*"

PATTERNS = [
    ("HANDLE", r"(?<![\w.@])@[A-Za-z0-9_]{2,30}\b", 0.9),  # social media handles
    ("URL", r"\b(?:https?://|www\.)\S*[^\s.,;:!?)\]\"']", 0.7),
    ("NUMBER", r"\b\d{8,}\b", 0.5),  # account, membership, ticket numbers
    (
        "REFERENCE",  # "booking ref QX7P2L", "account no. 12345", "case #A1234"
        r"(?i:\b(?:account|customer|member(?:ship)?|policy|order|ticket|case|"
        r"loyalty|frequent flyer|reference|ref|booking|confirmation|pnr)"
        r"(?:\s+(?:number|no\.?|num|id|code))?)\s*[:#]?\s*"
        r"(?P<v>(?=[A-Z0-9-]*\d)[A-Z0-9][A-Z0-9-]{4,}|[A-Z]{6}\b)",
        0.8,
    ),
    ("POSTCODE", r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b", 0.5),  # UK
    (
        # A specific date: with a flight or a place, it can identify someone.
        # Durations and "today" are left alone.
        "DATE",
        r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/.]\d{1,2}[/.]\d{2,4}\b|"
        rf"\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:of\s+)?{MONTHS}(?:\s+\d{{4}})?|"
        rf"\b{MONTHS}\s+\d{{1,2}}(?:st|nd|rd|th)?\b(?:,?\s+\d{{4}})?",
        0.6,
    ),
]

PRESETS = {
    "airline": [
        ("BOOKING_REF", r"\b(?=[A-Z]*\d)(?=\d*[A-Z])[A-Z0-9]{6}\b", 0.6),  # QX7P2L
        ("FLIGHT", r"\b(?:[A-Z]{2}|[A-Z]\d|\d[A-Z])\s?\d{2,4}\b", 0.5),  # AB123
    ],
}

# Ordinary words: never a name on their own, and left out of the review list.
COMMON_WORDS = set(
    """a about after again all also always am an and angry annoyed any app are as
    at back bad because been before being best but by can cannot customer could
    delighted desk did disappointed dm do does done don't email even every
    extremely for frankly from fully furious get going good great happy had has
    have he hello her here hi him his honestly how i if in is it its just last
    let like literally lost me more most much my never new next no not now of
    off ok okay on once one only or our out over please pretty quite really sad
    same see service she so sorry still stuck such support sure team thanks that
    the their them then there these they this those time to today too totally
    truly unhappy upset us very was we well were what when where which who why
    will with without would yes yet you your absolutely beyond completely
    genuinely i'll i'm i've i'd i’ll i’m i’ve i’d monday tuesday wednesday
    thursday friday saturday sunday january february march april june july
    august september october november december""".split()
)

PLACEHOLDER = re.compile(r"\[[A-Z_]+(?:_\d+)?\]")


def norm(header: str) -> str:
    return re.sub(r"[\s-]+", "_", header.strip().lower())


def is_number(value: str) -> bool:
    return bool(re.fullmatch(r"-?\d+(?:[.,]\d+)?%?", value.strip()))


SLASH_DATE = re.compile(r"^\s*(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})")


def date_order(values) -> str | None:
    """dmy or mdy for a column of 10/11/2026-style dates, or None if it cannot tell."""
    parts = [m.groups() for v in values if (m := SLASH_DATE.match(v))]
    if any(int(a) > 12 for a, _, _ in parts):
        return "dmy"
    if any(int(b) > 12 for _, b, _ in parts):
        return "mdy"
    return None


def to_month(value: str, order: str | None) -> str:
    """2026-11-10T14:21 or 10/11/2026 as 2026-11; the year alone when the order is unknown."""
    iso = re.match(r"^\s*(\d{4}-\d{2})", value)
    if iso:
        return iso.group(1)
    m = SLASH_DATE.match(value)
    if not m:
        return value
    a, b, year = m.groups()
    year = year if len(year) == 4 else f"20{year}"
    if order is None:
        return year
    return f"{year}-{int(b if order == 'dmy' else a):02d}"


def load_presidio(language: str, model: str):
    """Presidio's analyzer, set up to run offline."""
    try:
        import tldextract
        from presidio_analyzer import AnalyzerEngine
        from presidio_analyzer.nlp_engine import NlpEngineProvider
    except ImportError:
        sys.exit("This script needs Microsoft Presidio. Install it once with:\n"
                 f"    pip install -r {Path(__file__).with_name('requirements.txt')}\n"
                 f"    python -m spacy download {model}")
    # Presidio's email check uses tldextract, which by default downloads the
    # public list of domain suffixes. Use the copy bundled with it instead.
    tldextract.extract = tldextract.TLDExtract(suffix_list_urls=(), cache_dir=None)
    logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)
    try:
        nlp = NlpEngineProvider(nlp_configuration={
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": language, "model_name": model}],
        }).create_engine()
    except OSError:
        sys.exit(f"The spaCy model {model} is not installed. Install it once with:\n"
                 f"    python -m spacy download {model}")
    return AnalyzerEngine(nlp_engine=nlp, supported_languages=[language])


class Scrubber:
    def __init__(self, analyzer, language, extra_patterns, allow):
        self.analyzer, self.language = analyzer, language
        entities = set(analyzer.get_supported_entities(language)) - PRESIDIO_SKIP
        self.text_entities = sorted(entities)
        self.field_entities = sorted(entities - NAME_ENTITIES)
        self.patterns = [(label, re.compile(rx), score) for label, rx, score in PATTERNS + list(extra_patterns)]
        self.allow = {w.lower().lstrip("@") for w in allow}
        self.known: list[tuple[re.Pattern, str]] = []
        self.counts: Counter = Counter()
        self.cache: dict[tuple[str, bool], str] = {}

    def add_known(self, values, label="PERSON") -> None:
        """Values from dropped columns and the names file, removed anywhere.

        A whole value matches in any case ("jsmith", "Maria Silva"). The parts
        of a name match only when capitalised, so "Rose" goes but "rose" stays.
        """
        whole, parts = set(), set()
        for value in values:
            value = value.strip()
            if len(value) < 3 or is_number(value) or value.lower() in COMMON_WORDS:
                continue
            whole.add(value)
            if label == "PERSON":
                parts.update(t for t in value.split() if len(t) >= 3 and t.lower() not in COMMON_WORDS)
            if label == "EMAIL" and "@" in value:  # the login before the @ often appears alone
                local = value.split("@")[0]
                if len(local) >= 3 and local.lower() not in COMMON_WORDS:
                    self.known.append((re.compile(rf"(?<![\w.@]){re.escape(local)}(?![\w@])", re.I), "LOGIN"))
        terms = [(t, re.I) for t in whole] + [(t, 0) for t in parts - whole]
        for term, flags in sorted(terms, key=lambda x: len(x[0]), reverse=True):
            self.known.append((re.compile(rf"(?<!\w){re.escape(term)}(?!\w)", flags), label))

    def _spans(self, text: str, free_text: bool):
        found = []  # (start, end, label, score)
        for result in self.analyzer.analyze(
                text=text, language=self.language, score_threshold=MIN_SCORE,
                entities=self.text_entities if free_text else self.field_entities):
            value = text[result.start:result.end]
            if result.entity_type == "PERSON" and value.lower() in COMMON_WORDS | self.allow:
                continue
            label = SHORT_LABELS.get(result.entity_type, result.entity_type)
            found.append((result.start, result.end, label, result.score))
        for rx, label in self.known:
            found += [(m.start(), m.end(), label, 1.0) for m in rx.finditer(text)]
        for label, rx, score in self.patterns:
            if label == "DATE" and not free_text:
                continue  # dates in structured columns are data, not personal details
            for m in rx.finditer(text):
                if label == "HANDLE" and m.group(0)[1:].lower() in self.allow:
                    continue  # your own brand's handle, kept with --allow
                start, end = m.span("v") if "v" in rx.groupindex else m.span()
                found.append((start, end, label, score))
        # Overlapping finds merge into one replacement, labelled by the most
        # confident, so no part of a value is ever left behind.
        merged: list[list] = []
        for start, end, label, score in sorted(found):
            if merged and start < merged[-1][1]:
                last = merged[-1]
                last[1] = max(last[1], end)
                if score > last[3]:
                    last[2], last[3] = label, score
            else:
                merged.append([start, end, label, score])
        return [(start, end, label) for start, end, label, _ in merged]

    def scrub(self, text: str, free_text: bool) -> str:
        key = (text, free_text)
        if key not in self.cache:  # the same value often repeats in a column
            self.cache[key] = self._replace(text, free_text)
        new, counts = self.cache[key]
        self.counts.update(counts)
        return new

    def _replace(self, text: str, free_text: bool):
        spans = self._spans(text, free_text)
        numbers: dict[tuple[str, str], int] = {}
        per_label: Counter = Counter()
        counts: Counter = Counter()
        out, pos = [], 0
        for start, end, label in spans:
            key = (label, text[start:end].lower())
            if key not in numbers:
                per_label[label] += 1
                numbers[key] = per_label[label]
            out += [text[pos:start], f"[{label}_{numbers[key]}]" if label == "PERSON" else f"[{label}]"]
            pos = end
            counts[label] += 1
        out.append(text[pos:])
        return "".join(out), counts


def classify(header: str, values: list[str], overrides: dict[str, str]) -> str:
    h = norm(header)
    if h in overrides:
        return overrides[h]
    if DROP_HEADERS.match(h):
        return "drop"
    if h in RECORD_ID_HEADERS:
        return "record id"
    if ID_HEADERS.match(h):
        return "pseudonym"
    if TEXT_HEADERS.match(h):
        return "text"
    filled = [v for v in values if v.strip()]
    if DATE_HEADERS.search(h) and filled and sum(bool(LOOKS_LIKE_DATE.match(v)) for v in filled) > len(filled) / 2:
        return "date"
    if filled and statistics.mean(len(v) for v in filled) > 40 and sum(" " in v for v in filled) > len(filled) / 2:
        return "text"
    return "other"


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    raw = path.read_text(encoding="utf-8-sig")
    try:
        dialect = csv.Sniffer().sniff(raw[:4096], delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.reader(raw.splitlines(keepends=True), dialect))
    return (rows[0], rows[1:]) if rows else ([], [])


def capitalised_words(texts) -> Counter:
    """Capitalised words left mid-sentence: the reviewer's list of possible names."""
    found: Counter = Counter()
    for text in texts:
        text = PLACEHOLDER.sub(" ", text)
        for sentence in re.split(r"[.!?\n:;\"“”()]+", text):
            for word in re.findall(r"[^\W\d_][\w'’-]*", sentence)[1:]:
                if word[0].isupper() and not word.isupper() and word.lower() not in COMMON_WORDS:
                    found[word] += 1
    return found


def fake_value(kind: str, values: list[str], rng: random.Random, min_count: int) -> str:
    filled = [v for v in values if v.strip()]
    if not filled:
        return ""
    if kind == "text":
        return rng.choice(["Example feedback about [PERSON_1] and a delay.", "Example comment.", "Example note with a [REFERENCE]."])
    if kind == "pseudonym":
        return f"P-{rng.randrange(16**8):08x}"
    if kind == "record id":
        return f"FAKE-{rng.randrange(10000):04d}"
    if all(is_number(v) for v in filled):
        nums = sorted(float(v.replace(",", ".").rstrip("%")) for v in filled)
        lo, hi = nums[len(nums) // 4], nums[3 * len(nums) // 4]
        decimals = max((len(v.split(".")[1]) if "." in v else 0) for v in filled)
        return f"{rng.uniform(lo, hi):.{decimals}f}"
    common = sorted(v for v, n in Counter(filled).items() if n >= min_count)
    return rng.choice(common) if common else "example"


def describe(kind: str, values: list[str], min_count: int) -> str:
    filled = [v for v in values if v.strip()]
    if kind in ("text", "pseudonym", "record id", "date") or not filled:
        return ""
    if all(is_number(v) for v in filled):
        return "number"
    counts = Counter(filled)
    if len(counts) > 30:
        return f"{len(counts)} distinct values"
    common = sorted(v for v, n in counts.items() if n >= min_count)
    hidden = len(counts) - len(common)
    return ", ".join(common) + (f" ({hidden} rare values hidden)" if hidden else "")


SYNTHETIC_README = """# Synthetic data: invented, not evidence

Every row here is invented, {n} per file, in the shape of the prepared data:
the same columns, the common values in roughly their real shares, numbers in
their usual range, and dates in the real period, by month. Columns are
generated independently, so links between them are lost, and the free text is
a marker, not customer words.

Use it to rehearse a workshop or to check the pipeline, with data input
`synthetic`. Never put it in the same folder as real data, and never use a
finding from it as evidence for a build.
"""


def synthesize(header: list[str], kinds: list[str], columns: list[list[str]], n: int,
               rng: random.Random, min_count: int = 5) -> list[list[str]]:
    """N invented rows from the scrubbed columns. Each column is drawn on its own.

    Rare values (fewer than min_count) never appear, so no single record shows through.
    """
    makers = []
    for h, kind, col in zip(header, kinds, columns):
        filled = [v for v in col if v.strip()]
        blank = 1 - len(filled) / len(col) if col else 1.0
        if not filled:
            makers.append(lambda i: "")
            continue
        if kind == "record id":
            make = lambda i: f"SYN-{i + 1:04d}"
        elif kind == "pseudonym":
            pool = [f"P-{rng.randrange(16**8):08x}" for _ in range(max(1, round(n * len(set(filled)) / len(filled))))]
            make = lambda i, pool=pool: rng.choice(pool)
        elif kind == "text":
            make = lambda i, h=h: f"[SYNTHETIC] {h} {i + 1}"
        elif kind == "date":
            order = date_order(filled)
            months = [m for v in filled if re.match(r"^\d{4}-\d{2}$", m := to_month(v, order))]
            make = lambda i, months=months: rng.choice(months) if months else ""
        elif all(is_number(v) for v in filled):
            nums = sorted(float(v.replace(",", ".").rstrip("%")) for v in filled)
            lo, hi = nums[len(nums) // 20], nums[-1 - len(nums) // 20]
            decimals = max((len(v.split(".")[1]) if "." in v else 0) for v in filled)
            make = lambda i, lo=lo, hi=hi, d=decimals: f"{rng.uniform(lo, hi):.{d}f}"
        else:
            counts = {v: c for v, c in Counter(filled).items() if c >= min_count}
            values, weights = list(counts), list(counts.values())
            make = lambda i, values=values, weights=weights: (
                rng.choices(values, weights)[0] if values else "[SYNTHETIC]")
        makers.append(lambda i, make=make, blank=blank: "" if rng.random() < blank else make(i))
    return [[make(i) for make in makers] for i in range(n)]


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("inputs", nargs="+", type=Path)
    p.add_argument("--out", type=Path, default=Path("prepared"))
    p.add_argument("--preset", choices=sorted(PRESETS), action="append", default=[])
    p.add_argument("--names-file", type=Path)
    p.add_argument("--pattern", action="append", default=[], metavar="LABEL=REGEX")
    p.add_argument("--allow", action="append", default=[])
    for kind in ("drop", "id", "text", "keep"):
        p.add_argument(f"--{kind}", action="append", default=[], metavar="COL")
    p.add_argument("--dates", choices=["month"])
    p.add_argument("--synthetic", type=int, default=0, metavar="N")
    p.add_argument("--language", default="en")
    p.add_argument("--spacy-model", default="en_core_web_lg")
    args = p.parse_args(argv)

    extra = [pattern for preset in args.preset for pattern in PRESETS[preset]]
    for item in args.pattern:
        label, _, rx = item.partition("=")
        if not rx:
            p.error(f"--pattern needs LABEL=REGEX, got {item!r}")
        extra.append((re.sub(r"\W", "_", label.upper()), rx, 0.9))
    overrides = {norm(c): kind for kind, cols in
                 (("drop", args.drop), ("pseudonym", args.id), ("text", args.text), ("other", args.keep))
                 for c in cols}
    keep_untouched = {norm(c) for c in args.keep}

    files: list[tuple[Path, Path]] = []  # (source, path relative to share/)
    for item in args.inputs:
        if item.is_dir():
            files += [(f, f.relative_to(item)) for f in sorted(item.rglob("*.csv"))]
        elif item.is_file():
            files.append((item, Path(item.name)))
        else:
            p.error(f"not found: {item}")
    if not files:
        p.error("no CSV files found")

    share, review = args.out / "share", args.out / "review-only"
    tables = []
    for source, rel in files:
        header, rows = read_csv(source)
        columns = [[row[i] if i < len(row) else "" for row in rows] for i in range(len(header))]
        kinds = [classify(h, col, overrides) for h, col in zip(header, columns)]
        tables.append((source, rel, header, rows, columns, kinds))

    print(f"Loading Presidio and {args.spacy_model}...")
    scrubber = Scrubber(load_presidio(args.language, args.spacy_model), args.language, extra, args.allow)
    if args.names_file:
        scrubber.add_known(args.names_file.read_text(encoding="utf-8-sig").splitlines())
    for *_, header, rows, columns, kinds in tables:  # values of dropped columns, from every file
        for h, col, kind in zip(header, columns, kinds):
            if kind == "drop":
                scrubber.add_known(set(col), known_label(h))

    key = secrets.token_bytes(32)  # pseudonym key: random, used once, never saved
    rng = random.Random(7)
    report = ["# Data preparation review", "",
              "**This file contains raw customer text. Keep it; do not share it.**", "",
              "Before you share the `share/` folder:", "",
              "1. Read the examples below. Is anything personal left?",
              "2. Scan the capitalised words at the end for names.",
              "3. If something slipped through, rerun with `--names-file`, `--pattern`, or `--drop`.",
              "4. Share only `share/`.", "",
              f"Presidio looked for ({args.language}): " + ", ".join(scrubber.text_entities) + ".",
              "Anything not on this list, other than this script's own patterns, was not looked for.", ""]
    schema = ["# Schema", "",
              "The structure of the prepared data, and a few fake rows to write analysis code against.",
              "Fake rows are invented: their values say nothing about the real data.", ""]
    all_text: list[str] = []

    for source, rel, header, rows, columns, kinds in tables:
        before = dict(scrubber.counts)
        out_header = [h for h, k in zip(header, kinds) if k != "drop"]
        out_rows, changed, unchanged = [], [], []
        pseudonyms: dict[str, str] = {}
        orders = {i: date_order(col) for i, (col, k) in enumerate(zip(columns, kinds)) if k == "date"}
        for row in rows:
            out_row = []
            for i, (h, kind) in enumerate(zip(header, kinds)):
                value = row[i] if i < len(row) else ""
                if kind == "drop":
                    continue
                if kind == "pseudonym" and value.strip():
                    digest = hmac.new(key, value.strip().lower().encode(), hashlib.sha256).hexdigest()[:8]
                    value = pseudonyms.setdefault(value, f"P-{digest}")
                elif kind == "date":
                    if args.dates == "month" and value.strip():
                        value = to_month(value, orders[i])
                elif kind in ("text", "other") and norm(h) not in keep_untouched and value and not is_number(value):
                    new = scrubber.scrub(value, free_text=kind == "text")
                    if kind == "text":
                        (changed if new != value else unchanged).append((value, new))
                        all_text.append(new)
                    value = new
                out_row.append(value)
            out_rows.append(out_row)

        target = share / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f, lineterminator="\n").writerows([out_header] + out_rows)

        found = {k: v - before.get(k, 0) for k, v in scrubber.counts.items() if v - before.get(k, 0)}
        report += [f"## {rel}", "", f"{len(rows)} rows from `{source}`.", "",
                   "| Column | Treatment |", "|---|---|"]
        report += [f"| {h} | {k} |" for h, k in zip(header, kinds)]
        report += ["", "Replaced: " + (", ".join(f"{k} {v}" for k, v in sorted(found.items())) or "nothing"), ""]
        if changed:
            report += ["### Changed (random examples)", ""]
            for old, new in rng.sample(changed, min(20, len(changed))):
                report += [f"- Before: {old}", f"  After:  {new}"]
            report.append("")
        if unchanged:
            report += ["### Unchanged (random examples: check nothing was missed)", ""]
            report += [f"- {old}" for old, _ in rng.sample(unchanged, min(10, len(unchanged)))]
            report.append("")

        schema += [f"## {rel}", "", f"{len(rows)} rows.", "", "| Column | Kind | Values |", "|---|---|---|"]
        # Describe the scrubbed values, never the raw ones: schema.md is shared.
        kept_kinds = [k for k in kinds if k != "drop"]
        out_columns = [[row[i] for row in out_rows] for i in range(len(out_header))]
        cols_out = list(zip(out_header, kept_kinds, out_columns))
        # Rare values can single out a customer in per-record files; aggregates show them all.
        per_record = any(k in ("record id", "pseudonym", "drop") for k in kinds) or (
            "text" in kinds and len(rows) > 50)
        min_count = 5 if per_record else 1
        schema += [f"| {h} | {k} | {describe(k, c, min_count)} |" for h, k, c in cols_out]
        schema += ["", "Fake rows:", "", "```csv", ",".join(out_header)]
        for _ in range(min(5, len(rows))):
            fake = []
            for h, k, c in cols_out:
                if k == "date":
                    fake.append(rng.choice([v for v in c if v.strip()] or [""])[:7] + ("" if args.dates else "-01"))
                else:
                    fake.append(fake_value(k, c, rng, min_count))
            schema.append(",".join(f'"{v}"' if "," in v else v for v in fake))
        schema += ["```", ""]

        if args.synthetic:
            target = args.out / "synthetic" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f, lineterminator="\n").writerows(
                    [out_header] + synthesize(out_header, kept_kinds, out_columns, args.synthetic, rng))

    words = capitalised_words(all_text)
    report += ["## Capitalised words left in the text", "",
               "Mostly places, products, and brands. Any person's name here was missed: "
               "add it with `--names-file` and rerun. Add words that are not names with `--allow`.", ""]
    report += [", ".join(f"{w} ({n})" for w, n in words.most_common(150)) or "None.", ""]

    if args.synthetic:
        (args.out / "synthetic" / "README.md").write_text(SYNTHETIC_README.format(n=args.synthetic), encoding="utf-8")
    review.mkdir(parents=True, exist_ok=True)
    (review / "report.md").write_text("\n".join(report), encoding="utf-8")
    (share / "schema.md").write_text("\n".join(schema), encoding="utf-8")

    # Print counts only, never record text.
    print(f"Prepared {len(tables)} files, {sum(len(t[3]) for t in tables)} rows.")
    print("Replaced: " + (", ".join(f"{k} {v}" for k, v in sorted(scrubber.counts.items())) or "nothing"))
    print(f"Share:  {share}/")
    print(f"Review: {review / 'report.md'}  (contains raw text: do not share)")
    if args.synthetic:
        print(f"Synthetic: {args.out / 'synthetic'}/  (invented rows for rehearsals: never evidence)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
