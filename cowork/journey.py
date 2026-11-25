"""Render one Discovery project as a self-contained HTML journey app for a Cowork artifact.

The app shows the five phases as a track, every artifact of each phase rendered from its
Markdown file, the prototype versions clickable in place, the decision, and how much of the
work is Known, Assumed, or Needs evidence. It reads discovery/<project>/ and writes one HTML
file with no external requests, so the Cowork artifact sandbox can show it as it is.

Usage: python3 journey.py <discovery/project folder> [output.html]
       (default output: <project folder>/journey.html)

Standard library only, Python 3.9 or later.
"""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# The method's phases, the question each answers, and the artifacts the entry skill expects.
PHASES = [
    ("signals", "Signals", "What are customers telling us?",
     ["team-expectations.md", "signal-summary.md", "hypotheses.md"]),
    ("working-backwards", "Working Backwards", "Which problem first, for whom, and how would we announce it?",
     ["personas/", "use-case-scoring.md", "working-backwards.md", "feature-description.md", "prfaq.md",
      "prd.md", "gtm.md", "riskiest-assumption.md"]),
    ("prototype", "Prototype", "What would it look like?",
     ["notes.md", "persona-critique.md", "versions.md"]),
    ("validate", "Validate", "What could make it fail, and how will we know it worked?",
     ["risk-review.md", "prioritization.md", "decision.md"]),
    ("handoff", "Handoff", "What does the build start from?",
     ["discovery-brief.md", "next-steps.md"]),
]
LABELS = {"known": "Known", "assumed": "Assumed", "needs": "Needs evidence"}
STATUSES = ("Complete", "In progress", "Not started", "Deferred")


# ---------------------------------------------------------------- Markdown

def _inline(text: str, link) -> str:
    """Inline Markdown to HTML: code, evidence labels, links, bold, italic."""
    codes: list[str] = []

    def keep_code(m: re.Match) -> str:
        codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[(Known|Assumed|Needs evidence)\](?!\()",
                  lambda m: f'<span class="ev ev-{_key(m.group(1))}">{m.group(1)}</span>', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: link(m.group(1), html.unescape(m.group(2))), text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"<strong>(Known|Assumed|Needs evidence)</strong>",
                  lambda m: f'<span class="ev ev-{_key(m.group(1))}">{m.group(1)}</span>', text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def _key(label: str) -> str:
    return {"Known": "known", "Assumed": "assumed", "Needs evidence": "needs"}[label]


def _cell(text: str, link) -> str:
    """A table cell; a cell that is only an evidence label becomes a chip."""
    m = re.match(r"^(Known|Assumed|Needs evidence)\b(.*)$", text.strip())
    if m:
        return f'<span class="ev ev-{_key(m.group(1))}">{m.group(1)}</span>{_inline(m.group(2), link)}'
    return _inline(text, link)


def _row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def markdown(md: str, link=None) -> str:
    """A small, safe Markdown renderer: enough for the artifacts the Discovery skills write."""
    link = link or (lambda t, u: f'<a href="{html.escape(u)}" target="_blank" rel="noopener">{t}</a>')
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    para: list[str] = []
    lists: list[tuple[str, int]] = []  # (tag, indent)
    i = 0

    def flush_para() -> None:
        if para:
            out.append(f"<p>{_inline(' '.join(para), link)}</p>")
            para.clear()

    def close_lists(indent: int = -1) -> None:
        while lists and lists[-1][1] > indent:
            out.append(f"</li></{lists.pop()[0]}>")

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        fence = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence:
            flush_para(); close_lists()
            mark, body = fence.group(1), []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(mark):
                body.append(lines[i]); i += 1
            out.append(f"<pre><code>{html.escape(chr(10).join(body))}</code></pre>")
            i += 1
            continue
        if not stripped:
            flush_para()
            if lists and not (i + 1 < len(lines) and re.match(r"^\s*([-*+]|\d+[.)])\s", lines[i + 1])):
                close_lists()
            i += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", stripped)
        if heading:
            flush_para(); close_lists()
            level = len(heading.group(1))
            out.append(f"<h{level}>{_inline(heading.group(2), link)}</h{level}>")
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            flush_para(); close_lists()
            out.append("<hr>")
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            flush_para(); close_lists()
            head = _row(stripped)
            i += 2
            body = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                body.append(_row(lines[i])); i += 1
            out.append('<div class="table"><table><thead><tr>'
                       + "".join(f"<th>{_inline(c, link)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{_cell(c, link)}</td>" for c in r) + "</tr>" for r in body)
                       + "</tbody></table></div>")
            continue
        if stripped.startswith(">"):
            flush_para(); close_lists()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            out.append(f"<blockquote>{markdown(chr(10).join(quote), link)}</blockquote>")
            continue
        item = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if item:
            flush_para()
            indent, tag = len(item.group(1).expandtabs(4)), ("ol" if item.group(2)[0].isdigit() else "ul")
            if lists and indent > lists[-1][1]:
                out.append(f"<{tag}><li>")
                lists.append((tag, indent))
            else:
                close_lists(indent)
                if lists and lists[-1][1] == indent and lists[-1][0] == tag:
                    out.append("</li><li>")
                else:
                    close_lists(indent - 1)
                    out.append(f"<{tag}><li>")
                    lists.append((tag, indent))
            text = item.group(3)
            box = re.match(r"^\[([ xX])\]\s+(.*)$", text)
            if box:
                mark = "&#9745;" if box.group(1).strip() else "&#9744;"
                text = box.group(2)
                out.append(f'<span class="box">{mark}</span> ')
            out.append(_inline(text, link))
            i += 1
            continue
        if lists and line.startswith(" "):
            out.append(" " + _inline(stripped, link))
            i += 1
            continue
        close_lists()
        para.append(stripped)
        i += 1
    flush_para(); close_lists()
    return "\n".join(out)


# ---------------------------------------------------------------- Reading the project

def evidence(md: str) -> dict[str, int]:
    """Count evidence labels: bracketed in prose, or leading a table cell."""
    counts = {k: 0 for k in LABELS}
    for label, key in (("Known", "known"), ("Assumed", "assumed"), ("Needs evidence", "needs")):
        counts[key] += len(re.findall(rf"\[{label}\](?!\()", md))
        counts[key] += len(re.findall(rf"\*\*{label}\*\*", md))
        counts[key] += len(re.findall(rf"\|\s*{label}\b[^|]*(?=\|)", md))
    return counts


def title_of(md: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+?)\s*$", md, re.M)
    return re.sub(r"[*_`]", "", m.group(1)) if m else fallback


def tables(md: str) -> list[list[list[str]]]:
    found, current = [], []
    for line in md.splitlines():
        if line.strip().startswith("|"):
            current.append(_row(line))
        elif current:
            found.append(current); current = []
    if current:
        found.append(current)
    return [[r for r in t if not all(re.match(r"^:?-{2,}:?$", c) for c in r if c)] for t in found]


def phase_board(project_md: str) -> dict[str, dict[str, str]]:
    """Phase status and key artifact from PROJECT.md: the last table with Phase and Status columns."""
    board: dict[str, dict[str, str]] = {}
    for table in tables(project_md):
        head = [h.lower() for h in table[0]]
        if "phase" not in head or "status" not in head:
            continue
        p, s = head.index("phase"), head.index("status")
        k = next((n for n, h in enumerate(head) if "key" in h or "artifact" in h), None)
        found = {}
        for row in table[1:]:
            if len(row) <= max(p, s):
                continue
            status = next((v for v in STATUSES if v.lower() in row[s].lower()), row[s].strip())
            found[row[p].strip().lower()] = {"status": status, "key": re.sub(r"[*`]", "", row[k]) if k is not None and k < len(row) else ""}
        for n, v in found.items():  # later tables win, but an empty key artifact keeps the earlier one
            board.setdefault(n, {}).update({x: y for x, y in v.items() if y})
    return board


def facts(project_md: str) -> list[tuple[str, str]]:
    for table in tables(project_md):
        if [h.lower() for h in table[0][:2]] == ["field", "value"]:
            return [(r[0], r[1]) for r in table[1:] if len(r) >= 2]
    rows = re.findall(r"^\s*[-*]?\s*\*\*([^*:]+)(?::\*\*|\*\*:)\s*(.+)$", project_md, re.M)
    rows = [(k, v) for k, v in rows if not re.match(r"what we", k, re.I)]
    return [(k.strip(), v.strip()) for k, v in rows][:10]


def carried(project_md: str) -> dict[str, str]:
    """The last What we know / don't know / assuming lines in PROJECT.md."""
    out = {}
    for key, pattern in (("know", r"what we know"), ("dont", r"what we don.t know"), ("assume", r"what we.re assuming")):
        hits = re.findall(rf"^\s*[-*]?\s*\*\*{pattern}:?\*\*:?\s*(.+)$", project_md, re.M | re.I)
        if hits:
            out[key] = hits[-1].strip()
    return out


def decision(md: str) -> dict[str, str]:
    m = re.search(r"\*\*decision:\*\*\s*\**\s*(commit|pivot|park)\b\**[ ,.:;-]*(.*)", md, re.I)
    if not m:
        return {}
    reason = re.search(r"\*\*(?:why|reason)[^*]*:\*\*\s*(.+)", md, re.I)
    block = re.search(r"\*\*conditions before the build:\*\*\s*(.*?)(?=^\*\*|\Z)", md, re.I | re.S | re.M)
    conditions = re.findall(r"^\s*[-*]\s+(.+)$", block.group(1), re.M) if block else []
    if block and not conditions and block.group(1).strip() and not re.match(r"\s*none", block.group(1), re.I):
        conditions = [block.group(1).strip().splitlines()[0]]
    by = re.search(r"\*\*decided by:\*\*\s*(.+)", md, re.I)
    return {"value": m.group(1).lower(), "line": m.group(2).strip(" *"),
            "why": _inline(reason.group(1).strip(), lambda t, u: t) if reason else "",
            "conditions": [_inline(c, lambda t, u: t) for c in conditions],
            "unattended": bool(by and re.search(r"unattended", by.group(1), re.I))}


def collect(project: Path) -> dict:
    project_md = (project / "PROJECT.md").read_text(encoding="utf-8") if (project / "PROJECT.md").is_file() else ""
    board = phase_board(project_md)
    docs_by_path: dict[str, str] = {}

    def link_for(base: Path):
        def link(text: str, url: str) -> str:
            if re.match(r"^(https?:|mailto:)", url):
                return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{text}</a>'
            target = (base / url.split("#")[0]).resolve()
            try:
                rel = target.relative_to(project.resolve()).as_posix()
            except ValueError:
                return f'<span class="path" title="{html.escape(url)}">{text}</span>'
            if rel.endswith(".md"):
                return f'<a href="#" data-doc="{html.escape(rel)}">{text}</a>'
            if re.match(r"^prototype/(v\d+|index)\.html$", rel):
                return f'<a href="#" data-proto="{html.escape(Path(rel).stem)}">{text}</a>'
            return f'<span class="path" title="{html.escape(rel)}">{text}</span>'
        return link

    phases, totals = [], {k: 0 for k in LABELS}
    for pid, name, question, expected in PHASES:
        folder = project / pid
        docs, seen = [], set()
        paths: list[tuple[str, Path | None]] = []
        for e in expected:
            if e.endswith("/"):
                group = sorted((folder / e).glob("*.md")) if (folder / e).is_dir() else []
                paths += [(p.relative_to(project).as_posix(), p) for p in group] or [(f"{pid}/{e}", None)]
            else:
                p = folder / e
                paths.append((f"{pid}/{e}", p if p.is_file() else None))
        if folder.is_dir():
            paths += [(p.relative_to(project).as_posix(), p) for p in sorted(folder.rglob("*.md"))]
        for rel, p in paths:
            if rel in seen:
                continue
            seen.add(rel)
            if p is None:
                docs.append({"path": rel, "title": Path(rel.rstrip("/")).name, "status": "Missing"})
                continue
            md = p.read_text(encoding="utf-8")
            ev = evidence(md)
            for k in totals:
                totals[k] += ev[k]
            docs.append({"path": rel, "title": title_of(md, p.stem), "status": "Saved",
                         "html": markdown(md, link_for(p.parent)), "ev": ev})
            docs_by_path[rel] = md
        present = [d for d in docs if d["status"] == "Saved"]
        info = board.get(name.lower(), {})
        started = bool(present) or (pid == "prototype" and any((project / "prototype").glob("v[0-9]*.html")))
        status = info.get("status") or ("Complete" if docs and len(present) == len(docs)
                                        else "In progress" if started else "Not started")
        if status == "Not started" and started:  # PROJECT.md is updated at phase ends; the files show the work began
            status = "In progress"
        phases.append({"id": pid, "name": name, "question": question, "status": status,
                       "key": info.get("key", ""), "docs": docs})

    versions = sorted((project / "prototype").glob("v[0-9]*.html"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
    index = project / "prototype" / "index.html"
    index_text = index.read_text(encoding="utf-8") if index.is_file() else ""
    protos = [{"id": p.stem, "html": p.read_text(encoding="utf-8"),
               "current": p.read_text(encoding="utf-8") == index_text} for p in versions]
    if index_text and not any(v["current"] for v in protos):
        protos.append({"id": "index", "html": index_text, "current": True})

    project_facts = facts(project_md)
    note = " ".join(v for k, v in project_facts).lower() + project_md.lower()
    return {
        "project": project.name,
        "title": title_of(project_md, f"Discovery: {project.name}"),
        "facts": [{"k": k, "v": _inline(v, link_for(project))} for k, v in project_facts],
        "demo": "demonstration" in note,
        "phases": phases,
        "prototypes": protos,
        "carried": {k: _inline(v, link_for(project)) for k, v in carried(project_md).items()},
        "decision": decision(docs_by_path.get("validate/decision.md", "")),
        "evidence": totals,
        "project_html": markdown(project_md, link_for(project)) if project_md else "",
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


# ---------------------------------------------------------------- The page

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  color-scheme: light;
  --paper: #f6f7f4; --sheet: #ffffff; --ink: #18232e; --muted: #5d6873; --rule: #d8ddd9; --wash: #eceee9;
  --known: #1d6b57; --known-bg: #e2f0ea; --assumed: #9a6c0c; --assumed-bg: #f7ecd2;
  --needs: #a83346; --needs-bg: #f7e1e4; --nav: #24486f;
  --serif: Charter, "Bitstream Charter", "Sitka Text", Cambria, Georgia, serif;
  --sans: "Avenir Next", Avenir, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--paper); color: var(--ink); }
body { font: 15px/1.55 var(--sans); -webkit-font-smoothing: antialiased; }
button { font: inherit; color: inherit; }
:focus-visible { outline: 2px solid var(--nav); outline-offset: 2px; border-radius: 4px; }
a { color: var(--nav); text-underline-offset: 2px; }

header.top { padding: 28px clamp(16px, 4vw, 48px) 0; }
.titlebar { display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px 16px; }
h1.project { font: 600 clamp(24px, 3.2vw, 34px)/1.15 var(--serif); margin: 0; letter-spacing: -0.01em; }
.updated { color: var(--muted); font-size: 13px; }
.demo { font-size: 13px; color: var(--assumed); background: var(--assumed-bg); padding: 2px 10px; border-radius: 999px; }
.product { color: var(--muted); max-width: 80ch; margin: 6px 0 0; }

/* The track: the five phases as one line, the memorable element of the page. */
nav.track { position: relative; display: grid; grid-template-columns: minmax(110px, .8fr) repeat(5, minmax(120px, 1fr));
  gap: 0; margin: 26px 0 0; overflow-x: auto; padding-bottom: 2px; scrollbar-width: thin; }
.line { position: absolute; left: 0; right: 0; top: 19px; height: 3px; background: var(--rule); }
.line i { display: block; height: 100%; width: var(--done, 0%); background: var(--ink); transition: width .9s cubic-bezier(.2,.7,.2,1); }
.station { position: relative; align-self: start; text-align: left; background: none; border: 0; padding: 0 14px 16px 0; cursor: pointer; }
.dot { position: relative; z-index: 1; display: grid; place-items: center; width: 40px; height: 40px; border-radius: 50%;
  background: var(--sheet); border: 3px solid var(--rule); font: 600 15px var(--serif); color: var(--muted); }
.station[data-status="Complete"] .dot { background: var(--ink); border-color: var(--ink); color: #fff; }
.station[data-status="In progress"] .dot { border-color: var(--ink); color: var(--ink); }
.station[data-status="Deferred"] .dot { border-style: dashed; }
.station .name { display: block; margin-top: 10px; font-weight: 600; }
.station .status { display: block; font-size: 13px; color: var(--muted); }
.station .key { display: block; font-size: 13px; color: var(--ink); margin-top: 4px; max-width: 26ch;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.station[aria-current="true"] .name { color: var(--nav); text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 5px; }
.station.home .dot { border-radius: 10px; font: 600 13px var(--sans); }

main { display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 0; border-top: 1px solid var(--rule); margin-top: 6px; min-height: 70vh; }
main.wide { grid-template-columns: minmax(0, 1fr); }
aside.rail { border-right: 1px solid var(--rule); padding: 22px 0 40px; background: var(--wash); }
.rail h2 { font: 600 19px/1.25 var(--serif); margin: 0 20px 4px; }
.rail .question { margin: 0 20px 16px; color: var(--muted); font-size: 14px; }
.rail ul { list-style: none; margin: 0; padding: 0; }
.rail li button { display: block; width: 100%; text-align: left; border: 0; background: none; padding: 10px 20px; cursor: pointer; border-left: 3px solid transparent; }
.rail li button:hover { background: rgba(24, 35, 46, .04); }
.rail li button[aria-current="true"] { background: var(--sheet); border-left-color: var(--ink); }
.rail .doc-title { display: block; font-weight: 600; font-size: 14px; line-height: 1.35; }
.rail .doc-path { display: block; color: var(--muted); font-size: 12px; overflow-wrap: anywhere; }
.rail .missing .doc-title { color: var(--muted); font-weight: 400; font-style: italic; }
.rail .sub { margin: 18px 20px 6px; font-size: 13px; color: var(--muted); }

.bar { display: flex; height: 5px; border-radius: 3px; overflow: hidden; margin-top: 6px; background: var(--rule); max-width: 180px; }
.bar span { display: block; height: 100%; }
.bar .known, .big .known { background: var(--known); } .bar .assumed, .big .assumed { background: var(--assumed); } .bar .needs, .big .needs { background: var(--needs); }

section.pane { padding: 28px clamp(16px, 4vw, 56px) 64px; min-width: 0; }
.doc { max-width: 76ch; }
.doc h1 { font: 600 28px/1.2 var(--serif); margin: 0 0 18px; letter-spacing: -0.01em; }
.doc h2 { font: 600 21px/1.3 var(--serif); margin: 34px 0 10px; }
.doc h3 { font: 600 17px/1.35 var(--serif); margin: 26px 0 8px; }
.doc h4, .doc h5, .doc h6 { font-size: 15px; margin: 20px 0 6px; }
.doc p, .doc li { font-family: var(--serif); font-size: 16px; line-height: 1.65; }
.doc ul, .doc ol { padding-left: 1.3em; }
.doc li { margin: 3px 0; }
.doc blockquote { margin: 16px 0; padding: 2px 0 2px 18px; border-left: 3px solid var(--rule); color: #33404c; }
.doc code { font-size: .88em; background: var(--wash); padding: 1px 5px; border-radius: 4px; }
.doc pre { background: var(--wash); padding: 14px 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; line-height: 1.5; }
.doc pre code { background: none; padding: 0; }
.doc hr { border: 0; border-top: 1px solid var(--rule); margin: 28px 0; }
.table { overflow-x: auto; margin: 14px 0 18px; max-width: 100%; }
.doc table { border-collapse: collapse; font-size: 14px; min-width: 60%; }
.doc th { text-align: left; font-weight: 600; border-bottom: 2px solid var(--ink); padding: 6px 12px 6px 0; vertical-align: bottom; }
.doc td { border-bottom: 1px solid var(--rule); padding: 7px 12px 7px 0; vertical-align: top; }
.doc td, .doc th { font-family: var(--sans); }
.ev { display: inline-block; font: 600 12px/1.6 var(--sans); padding: 0 7px; border-radius: 4px; white-space: nowrap; vertical-align: 1px; }
.ev-known { color: var(--known); background: var(--known-bg); }
.ev-assumed { color: var(--assumed); background: var(--assumed-bg); }
.ev-needs { color: var(--needs); background: var(--needs-bg); }
.path { border-bottom: 1px dotted var(--muted); }
.empty { max-width: 60ch; color: var(--muted); font-family: var(--serif); font-size: 17px; }

/* Overview */
.verdict { max-width: 900px; }
.verdict .state { font: 600 clamp(26px, 3.6vw, 40px)/1.15 var(--serif); margin: 0 0 10px; letter-spacing: -0.015em; }
.verdict p { font: 17px/1.6 var(--serif); margin: 0; max-width: 70ch; color: #2b3742; }
.verdict h3.cond { font: 600 16px var(--serif); margin: 22px 0 6px; }
.verdict ul.cond { margin: 0; padding-left: 1.2em; max-width: 72ch; }
.verdict ul.cond li { font: 15.5px/1.55 var(--serif); margin: 4px 0; }
.verdict .note { margin-top: 14px; font: 14px var(--sans); color: var(--muted); }
.decision-commit .word { color: var(--known); } .decision-pivot .word { color: var(--assumed); } .decision-park .word { color: var(--needs); }
.ledger { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 28px; margin: 36px 0 0; max-width: 1100px; }
.ledger div { border-top: 3px solid var(--k); padding-top: 12px; }
.ledger h3 { font: 600 16px var(--serif); margin: 0 0 6px; color: var(--k); }
.ledger p { margin: 0; font-size: 14.5px; }
.weight { margin: 40px 0 0; max-width: 900px; }
.weight h3 { font: 600 16px var(--serif); margin: 0 0 10px; }
.weight .big { display: flex; height: 14px; border-radius: 7px; overflow: hidden; background: var(--rule); }
.weight .big span { height: 100%; }
.weight .legend { display: flex; flex-wrap: wrap; gap: 6px 22px; margin-top: 10px; font-size: 14px; }
.weight .legend b { font-variant-numeric: tabular-nums; }
.facts { margin: 40px 0 0; max-width: 900px; display: grid; grid-template-columns: max-content minmax(0, 1fr); gap: 8px 24px; font-size: 14px; }
.facts dt { color: var(--muted); } .facts dd { margin: 0; }

/* Prototype */
.proto-head { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px; margin-bottom: 14px; }
.proto-head h1 { font: 600 24px var(--serif); margin: 0; }
.versions { display: flex; gap: 6px; flex-wrap: wrap; }
.versions button { border: 1px solid var(--rule); background: var(--sheet); border-radius: 999px; padding: 3px 12px; cursor: pointer; font-size: 14px; }
.versions button[aria-pressed="true"] { background: var(--ink); color: #fff; border-color: var(--ink); }
.versions .cur { font-size: 11px; margin-left: 4px; opacity: .75; }
iframe.proto { width: 100%; height: max(640px, 78vh); border: 1px solid var(--rule); border-radius: 10px; background: #fff; }

@media (max-width: 860px) {
  main { grid-template-columns: minmax(0, 1fr); }
  aside.rail { border-right: 0; border-bottom: 1px solid var(--rule); padding: 16px 0 14px; }
  .rail .question { margin-bottom: 10px; }
  .rail ul { display: flex; gap: 8px; overflow-x: auto; padding: 0 20px 6px; scrollbar-width: thin; }
  .rail li { flex: 0 0 auto; }
  .rail li button { width: auto; max-width: 240px; padding: 7px 12px; border: 1px solid var(--rule); border-radius: 8px; background: var(--paper); }
  .rail li button[aria-current="true"] { border-color: var(--ink); background: var(--sheet); }
  .rail .doc-path { display: none; }
  .rail .sub { margin: 10px 20px 6px; }
  .ledger { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 700px) {
  nav.track { grid-template-columns: repeat(6, minmax(92px, 1fr)); }
  .station .key { display: none; }
}
@media (prefers-reduced-motion: reduce) { .line i { transition: none; } }
</style>
</head>
<body>
<header class="top">
  <div class="titlebar"><h1 class="project" id="title"></h1><span id="demo"></span><span class="updated" id="updated"></span></div>
  <p class="product" id="product"></p>
  <nav class="track" id="track" aria-label="Discovery phases"><div class="line" aria-hidden="true"><i></i></div></nav>
</header>
<main id="main"><aside class="rail" id="rail"></aside><section class="pane" id="pane" tabindex="-1"></section></main>
<script id="journey-data" type="application/json">__DATA__</script>
<script>
(function () {
  const D = JSON.parse(document.getElementById("journey-data").textContent);
  const $ = (s) => document.querySelector(s);
  const el = (tag, attrs, ...kids) => {
    const e = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => (k === "html" ? (e.innerHTML = v) : k === "text" ? (e.textContent = v) : e.setAttribute(k, v)));
    kids.forEach((k) => k && e.append(k));
    return e;
  };
  const docs = {}; D.phases.forEach((p) => p.docs.forEach((d) => (docs[d.path] = Object.assign({ phase: p.id }, d))));
  const state = { view: "overview", doc: null, proto: null };

  const bar = (ev, cls) => {
    const total = ev ? ev.known + ev.assumed + ev.needs : 0;
    if (!total) return null;
    const b = el("div", { class: cls || "bar", role: "img",
      "aria-label": `${ev.known} Known, ${ev.assumed} Assumed, ${ev.needs} Needs evidence` });
    ["known", "assumed", "needs"].forEach((k) => ev[k] && b.append(el("span", { class: k, style: `width:${(100 * ev[k]) / total}%` })));
    return b;
  };

  $("#title").textContent = D.title;
  document.title = D.title;
  $("#updated").textContent = "Updated " + D.updated;
  if (D.demo) $("#demo").replaceWith(el("span", { class: "demo", text: "Demonstration run on sample data" }));
  const product = D.facts.find((f) => /product/i.test(f.k));
  const cap = (h) => h.replace(/^([a-z])/, (c) => c.toUpperCase());
  D.facts.forEach((f) => (f.v = cap(f.v)));
  if (product) $("#product").innerHTML = product.v;

  const track = $("#track");
  track.append(el("button", { class: "station home", "data-view": "overview", "data-status": "Complete" },
    el("span", { class: "dot", text: "All" }), el("span", { class: "name", text: "Overview" }),
    el("span", { class: "status", text: "Where it stands" })));
  D.phases.forEach((p, i) => track.append(el("button", { class: "station", "data-view": p.id, "data-status": p.status },
    el("span", { class: "dot", text: String(i + 1) }), el("span", { class: "name", text: p.name }),
    el("span", { class: "status", text: p.status }), p.key ? el("span", { class: "key", text: p.key }) : null)));
  const reached = D.phases.reduce((n, p, i) => (p.status === "Complete" ? i + 1 : p.status === "In progress" ? Math.max(n, i + 0.5) : n), 0);
  requestAnimationFrame(() => requestAnimationFrame(() =>
    track.style.setProperty("--done", reached >= D.phases.length ? "100%" : `${((reached + 0.5) / (D.phases.length + 1)) * 100}%`)));

  function overview() {
    const pane = $("#pane"); pane.replaceChildren();
    const current = D.phases.find((p) => p.status === "In progress") || D.phases.find((p) => p.status !== "Complete");
    const v = el("div", { class: "verdict" });
    if (D.decision && D.decision.value) {
      v.className += " decision-" + D.decision.value;
      v.append(el("p", { class: "state", html: `Decision: <span class="word">${D.decision.value}</span>${D.decision.line ? ", " + D.decision.line.replace(/[.]$/, "") : ""}.` }));
      if (D.decision.why) v.append(el("p", { html: D.decision.why }));
      if (D.decision.conditions && D.decision.conditions.length) {
        v.append(el("h3", { class: "cond", text: "Conditions before the build" }));
        const ul = el("ul", { class: "cond" }); D.decision.conditions.forEach((c) => ul.append(el("li", { html: c }))); v.append(ul);
      }
      if (D.decision.unattended) v.append(el("p", { class: "note", text: "Unattended run: the recommended decision is recorded, not confirmed by a team." }));
    } else if (current) {
      v.append(el("p", { class: "state", text: `${current.name} ${current.status === "In progress" ? "is under way" : "comes next"}.` }));
      v.append(el("p", { text: current.question }));
    } else {
      v.append(el("p", { class: "state", text: "All five phases are complete." }));
    }
    pane.append(v);
    if (D.carried && Object.keys(D.carried).length) {
      const L = el("div", { class: "ledger" });
      [["know", "What we know", "var(--known)"], ["dont", "What we don't know", "var(--needs)"], ["assume", "What we're assuming", "var(--assumed)"]]
        .forEach(([k, h, c]) => D.carried[k] && L.append(el("div", { style: `--k:${c}` }, el("h3", { text: h }), el("p", { html: D.carried[k] }))));
      pane.append(L);
    }
    const ev = D.evidence, total = ev.known + ev.assumed + ev.needs;
    if (total) {
      const w = el("div", { class: "weight" }, el("h3", { text: "How the claims in the documents are labelled" }), bar(ev, "big"));
      const legend = el("div", { class: "legend" });
      [["known", "Known"], ["assumed", "Assumed"], ["needs", "Needs evidence"]].forEach(([k, n]) =>
        legend.append(el("span", { html: `<span class="ev ev-${k}">${n}</span> <b>${ev[k]}</b>` })));
      w.append(legend); pane.append(w);
    }
    if (D.facts.length) {
      const dl = el("dl", { class: "facts" });
      D.facts.forEach((f) => dl.append(el("dt", { text: f.k }), el("dd", { html: f.v })));
      pane.append(dl);
    }
  }

  function rail(phase) {
    const r = $("#rail"); r.replaceChildren(el("h2", { text: phase.name }), el("p", { class: "question", text: phase.question }));
    if (phase.id === "prototype" && D.prototypes.length) {
      r.append(el("p", { class: "sub", text: "Clickable prototype" }));
      r.append(el("ul", {}, el("li", {}, el("button", { "data-proto": (D.prototypes.find((p) => p.current) || D.prototypes.at(-1)).id,
        "aria-current": String(state.view === "prototype" && state.proto !== null) },
        el("span", { class: "doc-title", text: `Open the prototype (${D.prototypes.length} version${D.prototypes.length > 1 ? "s" : ""})` })))));
      r.append(el("p", { class: "sub", text: "Documents" }));
    }
    const ul = el("ul");
    phase.docs.forEach((d) => ul.append(el("li", { class: d.status === "Missing" ? "missing" : "" },
      el("button", { "data-doc": d.path, "aria-current": String(state.doc === d.path) },
        el("span", { class: "doc-title", text: d.status === "Missing" ? `${d.title} (not written yet)` : d.title }),
        el("span", { class: "doc-path", text: d.path }), bar(d.ev)))));
    r.append(ul);
  }

  function showDoc(path) {
    const d = docs[path], pane = $("#pane");
    state.doc = path; state.proto = null;
    if (!d) return;
    if (d.status === "Missing") {
      pane.replaceChildren(el("p", { class: "empty", text: `${d.path} has not been written yet. It is part of the ${D.phases.find((p) => p.id === d.phase).name} phase; ask Claude to run that step.` }));
    } else pane.replaceChildren(el("article", { class: "doc", html: d.html }));
  }

  function showProto(id) {
    const pane = $("#pane"), p = D.prototypes.find((x) => x.id === id) || D.prototypes.at(-1);
    state.proto = p.id; state.doc = null;
    const vs = el("div", { class: "versions", role: "group", "aria-label": "Prototype versions" });
    D.prototypes.forEach((x) => vs.append(el("button", { "data-proto": x.id, "aria-pressed": String(x.id === p.id) },
      document.createTextNode(x.id), x.current ? el("span", { class: "cur", text: "current" }) : null)));
    const frame = el("iframe", { class: "proto", title: `Prototype ${p.id}` });
    frame.srcdoc = p.html;
    pane.replaceChildren(el("div", { class: "proto-head" }, el("h1", { text: "Prototype" }), vs), frame);
  }

  function go(view, opts) {
    opts = opts || {};
    state.view = view;
    document.querySelectorAll(".station").forEach((s) => s.setAttribute("aria-current", String(s.dataset.view === view)));
    const main = $("#main");
    if (view === "overview") {
      main.classList.add("wide"); $("#rail").hidden = true; state.doc = null; overview();
    } else {
      main.classList.remove("wide"); $("#rail").hidden = false;
      const phase = D.phases.find((p) => p.id === view);
      if (opts.proto !== undefined) showProto(opts.proto);
      else if (opts.doc) showDoc(opts.doc);
      else if (phase.id === "prototype" && D.prototypes.length) showProto(null);
      else showDoc((phase.docs.find((d) => d.status === "Saved") || phase.docs[0] || {}).path);
      rail(phase);
    }
    if (opts.focus) $("#pane").focus({ preventScroll: true });
    window.scrollTo({ top: 0 });
  }

  document.addEventListener("click", (e) => {
    const station = e.target.closest(".station"), doc = e.target.closest("[data-doc]"), proto = e.target.closest("[data-proto]");
    if (station) { go(station.dataset.view); return; }
    if (doc) { e.preventDefault(); const d = docs[doc.dataset.doc]; if (d) go(d.phase, { doc: d.path, focus: true }); return; }
    if (proto) { e.preventDefault(); go("prototype", { proto: proto.dataset.proto, focus: true }); }
  });
  const start = (location.hash || "").replace(/^#\/?/, "");
  go(D.phases.some((p) => p.id === start) ? start : "overview");
})();
</script>
</body>
</html>
"""


def render(project: Path) -> str:
    data = collect(project)
    blob = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return PAGE.replace("__TITLE__", html.escape(data["title"])).replace("__DATA__", blob)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    project = Path(argv[1]).resolve()
    if not project.is_dir():
        print(f"Not a folder: {project}", file=sys.stderr)
        return 1
    out = Path(argv[2]).resolve() if len(argv) > 2 else project / "journey.html"
    out.write_text(render(project), encoding="utf-8")
    data = collect(project)
    saved = sum(d["status"] == "Saved" for p in data["phases"] for d in p["docs"])
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB): {saved} documents, {len(data['prototypes'])} prototype versions")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
