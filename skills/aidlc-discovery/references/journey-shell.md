# Journey app shell

The journey app's page. It reads the project's files from its data block and renders everything itself, so it needs no network and no other file. Copy the code block below **exactly** to `discovery/{{project}}/journey.html`, from `<!doctype html>` to `</html>`, and change nothing: not the styles, not the script, not the empty data block (`<script id="journey-data" type="application/json"></script>`). The update in `references/journey-app.md` fills the data block and checks that the page is this one.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Discovery journey</title>
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
  gap: 0; margin: 18px 0 0; overflow-x: auto; padding: 8px 0 2px 8px; scrollbar-width: thin; }
.line { position: absolute; left: 8px; right: 0; top: 27px; height: 3px; background: var(--rule); }
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
.live-view .line i { transition: none; }
/* Now: what the room is doing, updated at every step. */
.now { display: none; margin: 16px 0 0; padding: 12px 16px; border-left: 4px solid var(--nav); background: var(--sheet);
  border-radius: 0 8px 8px 0; max-width: 1100px; box-shadow: 0 1px 0 var(--rule); }
.now.on { display: block; }
.now .tag { font: 600 12px var(--sans); letter-spacing: .08em; text-transform: uppercase; color: var(--nav); margin-right: 10px; }
.now .where { font: 600 clamp(17px, 2vw, 21px)/1.3 var(--serif); }
.now .doing { display: block; margin-top: 4px; font: clamp(15px, 1.6vw, 18px)/1.5 var(--serif); color: #2b3742; }
.now .next { display: block; margin-top: 4px; font-size: 14px; color: var(--muted); }
.live { font-size: 13px; color: var(--known); }
.live::before { content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--known); margin-right: 6px; vertical-align: 1px; }
.station.here .dot { box-shadow: 0 0 0 5px var(--wash), 0 0 0 7px var(--nav); }
.waiting { padding: 40px clamp(16px, 4vw, 48px); font: 18px/1.6 var(--serif); color: var(--muted); max-width: 60ch; }
@media (prefers-reduced-motion: no-preference) { .station.here .dot { animation: here 2.4s ease-in-out infinite; } }
@keyframes here { 50% { box-shadow: 0 0 0 5px var(--wash), 0 0 0 9px rgba(36, 72, 111, .35); } }

</style>
</head>
<body>
<header class="top">
  <div class="titlebar"><h1 class="project" id="title"></h1><span id="demo"></span><span class="updated" id="updated"></span><span id="live"></span></div>
  <p class="product" id="product"></p>
  <div class="now" id="now" aria-live="polite"></div>
  <nav class="track" id="track" aria-label="Discovery phases"><div class="line" aria-hidden="true"><i></i></div></nav>
</header>
<main id="main"><aside class="rail" id="rail"></aside><section class="pane" id="pane" tabindex="-1"></section></main>
<script id="journey-data" type="application/json"></script>
<script>
(function () {
  /* collect:begin */
  // Reading the project: the page renders the raw files itself.
  const PHASES = [
    ["signals", "Signals", "What are customers telling us?", ["team-expectations.md", "signal-summary.md", "hypotheses.md"]],
    ["working-backwards", "Working Backwards", "Which problem first, for whom, and how would we announce it?",
      ["personas/", "use-case-scoring.md", "working-backwards.md", "feature-description.md", "prfaq.md", "prd.md", "gtm.md", "riskiest-assumption.md"]],
    ["prototype", "Prototype", "What would it look like?", ["notes.md", "persona-critique.md", "versions.md"]],
    ["validate", "Validate", "What could make it fail, and how will we know it worked?", ["risk-review.md", "prioritization.md", "decision.md"]],
    ["handoff", "Handoff", "What does the build start from?", ["discovery-brief.md", "next-steps.md"]],
  ];
  const STATUSES = ["Complete", "In progress", "Not started", "Deferred"];
  const KEY = { "Known": "known", "Assumed": "assumed", "Needs evidence": "needs" };
  const W = "[\\p{L}\\p{N}_]";
  const esc = (s, quote) => {
    s = String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return quote === false ? s : s.replace(/"/g, "&quot;").replace(/'/g, "&#x27;");
  };
  const unesc = (s) => s.replace(/&(lt|gt|quot|#x27|#39|amp);/g, (m, e) => ({ lt: "<", gt: ">", quot: '"', "#x27": "'", "#39": "'", amp: "&" }[e]));
  const chip = (l) => `<span class="ev ev-${KEY[l]}">${l}</span>`;
  const RE = {
    em: new RegExp(`(?<![${W.slice(1, -1)}*])\\*(?!\\s)(.+?)(?<!\\s)\\*(?![${W.slice(1, -1)}*])`, "gu"),
    em2: new RegExp(`(?<!${W})_(?!\\s)(.+?)(?<!\\s)_(?!${W})`, "gu"),
  };
  const plain = (t) => t;

  function inline(text, link) {
    const codes = [];
    text = text.replace(/`([^`]+)`/g, (m, c) => { codes.push(`<code>${esc(c, false)}</code>`); return `\u0000${codes.length - 1}\u0000`; });
    text = esc(text, false);
    text = text.replace(/\[(Known|Assumed|Needs evidence)\](?!\()/g, (m, l) => chip(l));
    text = text.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, t, u) => link(t, unesc(u)));
    text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    text = text.replace(/<strong>(Known|Assumed|Needs evidence)<\/strong>/g, (m, l) => chip(l));
    text = text.replace(RE.em, "<em>$1</em>").replace(RE.em2, "<em>$1</em>");
    return text.replace(/\u0000(\d+)\u0000/g, (m, n) => codes[+n]);
  }
  function cell(text, link) {
    const m = text.trim().match(/^(Known|Assumed|Needs evidence)\b([\s\S]*)$/);
    return m ? chip(m[1]) + inline(m[2], link) : inline(text, link);
  }
  function row(line) {
    line = line.trim();
    if (line.startsWith("|")) line = line.slice(1);
    if (line.endsWith("|")) line = line.slice(0, -1);
    return line.split(/(?<!\\)\|/).map((c) => c.trim());
  }
  const indentOf = (ws) => { let n = 0; for (const ch of ws) n = ch === "\t" ? n + 4 - (n % 4) : n + 1; return n; };
  const ITEM = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/;

  function markdown(md, link) {
    link = link || ((t, u) => `<a href="${esc(u)}" target="_blank" rel="noopener">${t}</a>`);
    const lines = md.replace(/\r\n/g, "\n").split("\n"), out = [], para = [], lists = [];
    let i = 0;
    const flush = () => { if (para.length) { out.push(`<p>${inline(para.join(" "), link)}</p>`); para.length = 0; } };
    const close = (indent = -1) => { while (lists.length && lists[lists.length - 1][1] > indent) out.push(`</li></${lists.pop()[0]}>`); };
    while (i < lines.length) {
      const line = lines[i], s = line.trim();
      const fence = line.match(/^\s*(`{3,}|~{3,})(.*)$/);
      if (fence) {
        flush(); close();
        const body = []; i++;
        while (i < lines.length && !lines[i].trim().startsWith(fence[1])) body.push(lines[i++]);
        out.push(`<pre><code>${esc(body.join("\n"), false)}</code></pre>`); i++; continue;
      }
      if (!s) {
        flush();
        if (lists.length && !(i + 1 < lines.length && /^\s*([-*+]|\d+[.)])\s/.test(lines[i + 1]))) close();
        i++; continue;
      }
      const h = s.match(/^(#{1,6})\s+(.*?)\s*#*\s*$/);
      if (h) { flush(); close(); out.push(`<h${h[1].length}>${inline(h[2], link)}</h${h[1].length}>`); i++; continue; }
      if (/^(-{3,}|\*{3,}|_{3,})$/.test(s)) { flush(); close(); out.push("<hr>"); i++; continue; }
      if (s.startsWith("|") && i + 1 < lines.length && /^\s*\|?\s*:?-{2,}/.test(lines[i + 1])) {
        flush(); close();
        const head = row(s), body = []; i += 2;
        while (i < lines.length && lines[i].trim().startsWith("|")) body.push(row(lines[i++]));
        out.push('<div class="table"><table><thead><tr>' + head.map((c) => `<th>${inline(c, link)}</th>`).join("") + "</tr></thead><tbody>"
          + body.map((r) => "<tr>" + r.map((c) => `<td>${cell(c, link)}</td>`).join("") + "</tr>").join("") + "</tbody></table></div>");
        continue;
      }
      if (s.startsWith(">")) {
        flush(); close();
        const q = [];
        while (i < lines.length && lines[i].trim().startsWith(">")) q.push(lines[i++].replace(/^\s*>\s?/, ""));
        out.push(`<blockquote>${markdown(q.join("\n"), link)}</blockquote>`); continue;
      }
      const item = line.match(ITEM);
      if (item) {
        flush();
        const indent = indentOf(item[1]), tag = /\d/.test(item[2][0]) ? "ol" : "ul";
        if (lists.length && indent > lists[lists.length - 1][1]) { out.push(`<${tag}><li>`); lists.push([tag, indent]); }
        else {
          close(indent);
          if (lists.length && lists[lists.length - 1][1] === indent && lists[lists.length - 1][0] === tag) out.push("</li><li>");
          else { close(indent - 1); out.push(`<${tag}><li>`); lists.push([tag, indent]); }
        }
        let text = item[3];
        const box = text.match(/^\[([ xX])\]\s+([\s\S]*)$/);
        if (box) { out.push(`<span class="box">${box[1].trim() ? "&#9745;" : "&#9744;"}</span> `); text = box[2]; }
        out.push(inline(text, link)); i++; continue;
      }
      if (lists.length && line.startsWith(" ")) { out.push(" " + inline(s, link)); i++; continue; }
      close(); para.push(s); i++;
    }
    flush(); close();
    return out.join("\n");
  }

  function evidence(md) {
    const n = (re) => (md.match(re) || []).length;
    return {
      known: n(/\[Known\](?!\()/g) + n(/\*\*Known\*\*/g) + n(/\|\s*Known\b[^|]*(?=\|)/g),
      assumed: n(/\[Assumed\](?!\()/g) + n(/\*\*Assumed\*\*/g) + n(/\|\s*Assumed\b[^|]*(?=\|)/g),
      needs: n(/\[Needs evidence\](?!\()/g) + n(/\*\*Needs evidence\*\*/g) + n(/\|\s*Needs evidence\b[^|]*(?=\|)/g),
    };
  }
  const titleOf = (md, fallback) => { const m = md.match(/^#\s+(.+?)\s*$/m); return m ? m[1].replace(/[*_`]/g, "") : fallback; };
  function tables(md) {
    const found = []; let cur = [];
    for (const line of md.split(/\r?\n/)) {
      if (line.trim().startsWith("|")) cur.push(row(line));
      else if (cur.length) { found.push(cur); cur = []; }
    }
    if (cur.length) found.push(cur);
    return found.map((t) => t.filter((r) => !r.filter((c) => c).every((c) => /^:?-{2,}:?$/.test(c))));
  }
  function phaseBoard(pmd) {
    const board = {};
    for (const t of tables(pmd)) {
      if (!t.length) continue;
      const head = t[0].map((h) => h.toLowerCase());
      if (!head.includes("phase") || !head.includes("status")) continue;
      const p = head.indexOf("phase"), s = head.indexOf("status");
      const k = head.findIndex((h) => h.includes("key") || h.includes("artifact"));
      const found = {};
      for (const r of t.slice(1)) {
        if (r.length <= Math.max(p, s)) continue;
        const status = STATUSES.find((v) => r[s].toLowerCase().includes(v.toLowerCase())) || r[s].trim();
        found[r[p].trim().toLowerCase()] = { status, key: k >= 0 && k < r.length ? r[k].replace(/[*`]/g, "") : "" };
      }
      for (const [n, v] of Object.entries(found)) {
        board[n] = board[n] || {};
        for (const [x, y] of Object.entries(v)) if (y) board[n][x] = y;
      }
    }
    return board;
  }
  function facts(pmd) {
    for (const t of tables(pmd)) {
      if (t.length && t[0].slice(0, 2).map((h) => h.toLowerCase()).join("|") === "field|value")
        return t.slice(1).filter((r) => r.length >= 2).map((r) => [r[0], r[1]]);
    }
    return [...pmd.matchAll(/^\s*[-*]?\s*\*\*([^*:]+)(?::\*\*|\*\*:)\s*(.+)$/gm)]
      .filter((m) => !/^what we/i.test(m[1])).map((m) => [m[1].trim(), m[2].trim()]).slice(0, 10);
  }
  function carried(pmd) {
    const out = {};
    for (const [key, pat] of [["know", "what we know"], ["dont", "what we don.t know"], ["assume", "what we.re assuming"]]) {
      const hits = [...pmd.matchAll(new RegExp(`^\\s*[-*]?\\s*\\*\\*${pat}:?\\*\\*:?\\s*(.+)$`, "gmi"))];
      if (hits.length) out[key] = hits[hits.length - 1][1].trim();
    }
    return out;
  }
  function decision(md) {
    const m = md.match(/\*\*decision:\*\*\s*\**\s*(commit|pivot|park)\b\**[ ,.:;-]*(.*)/i);
    if (!m) return {};
    const reason = md.match(/\*\*(?:why|reason)[^*]*:\*\*\s*(.+)/i);
    const block = md.match(/\*\*conditions before the build:\*\*\s*([\s\S]*?)(?=^\*\*|$(?![\s\S]))/im);
    let conditions = block ? [...block[1].matchAll(/^\s*[-*]\s+(.+)$/gm)].map((x) => x[1]) : [];
    if (block && !conditions.length && block[1].trim() && !/^\s*none/i.test(block[1])) conditions = [block[1].trim().split(/\r?\n/)[0]];
    const by = md.match(/\*\*decided by:\*\*\s*(.+)/i);
    return { value: m[1].toLowerCase(), line: m[2].trim().replace(/^[ *]+|[ *]+$/g, ""),
      why: reason ? inline(reason[1].trim(), plain) : "", conditions: conditions.map((c) => inline(c, plain)),
      unattended: !!(by && /unattended/i.test(by[1])) };
  }
  function resolve(base, url) {
    const parts = url.startsWith("/") ? null : (base ? base.split("/") : []).concat(url.split("/"));
    if (!parts) return null;
    const out = [];
    for (const p of parts) { if (p === "" || p === ".") continue; if (p === "..") { if (!out.length) return null; out.pop(); } else out.push(p); }
    return out.join("/");
  }
  function linkFor(base) {
    return (text, url) => {
      if (/^(https?:|mailto:)/.test(url)) return `<a href="${esc(url)}" target="_blank" rel="noopener">${text}</a>`;
      const rel = resolve(base, url.split("#")[0]);
      if (rel === null) return `<span class="path" title="${esc(url)}">${text}</span>`;
      if (rel.endsWith(".md")) return `<a href="#" data-doc="${esc(rel)}">${text}</a>`;
      const proto = rel.match(/^prototype\/(v\d+|index)\.html$/);
      if (proto) return `<a href="#" data-proto="${esc(proto[1])}">${text}</a>`;
      return `<span class="path" title="${esc(rel)}">${text}</span>`;
    };
  }
  const byParts = (a, b) => { const x = a.split("/"), y = b.split("/");
    for (let i = 0; i < Math.min(x.length, y.length); i++) if (x[i] !== y[i]) return x[i] < y[i] ? -1 : 1;
    return x.length - y.length; };
  const dirOf = (p) => p.includes("/") ? p.slice(0, p.lastIndexOf("/")) : "";
  const stem = (p) => { const n = p.split("/").pop(); return n.includes(".") ? n.slice(0, n.lastIndexOf(".")) : n; };

  function collect(raw) {
    const F = raw.files || {}, pmd = F["PROJECT.md"] || "", board = phaseBoard(pmd), totals = { known: 0, assumed: 0, needs: 0 }, byPath = {};
    const names = Object.keys(F);
    const phases = PHASES.map(([pid, name, question, expected]) => {
      const docs = [], seen = new Set(), paths = [];
      for (const e of expected) {
        if (e.endsWith("/")) {
          const group = names.filter((n) => dirOf(n) === `${pid}/${e.slice(0, -1)}` && n.endsWith(".md")).sort(byParts);
          if (group.length) group.forEach((n) => paths.push([n, true])); else paths.push([`${pid}/${e}`, false]);
        } else paths.push([`${pid}/${e}`, `${pid}/${e}` in F]);
      }
      names.filter((n) => n.startsWith(pid + "/") && n.endsWith(".md")).sort(byParts).forEach((n) => paths.push([n, true]));
      for (const [rel, present] of paths) {
        if (seen.has(rel)) continue;
        seen.add(rel);
        if (!present) { docs.push({ path: rel, title: rel.replace(/\/$/, "").split("/").pop(), status: "Missing" }); continue; }
        const md = F[rel], ev = evidence(md);
        for (const k in totals) totals[k] += ev[k];
        docs.push({ path: rel, title: titleOf(md, stem(rel)), status: "Saved", html: markdown(md, linkFor(dirOf(rel))), ev });
        byPath[rel] = md;
      }
      const present = docs.filter((d) => d.status === "Saved"), info = board[name.toLowerCase()] || {};
      const started = present.length > 0 || (pid === "prototype" && names.some((n) => /^prototype\/v\d[^/]*\.html$/.test(n)));
      let status = info.status || (docs.length && present.length === docs.length ? "Complete" : started ? "In progress" : "Not started");
      if (status === "Not started" && started) status = "In progress";
      return { id: pid, name, question, status, key: info.key || "", docs };
    });
    const num = (n) => +(stem(n).replace(/\D/g, "") || 0);
    const versions = names.filter((n) => /^prototype\/v\d[^/]*\.html$/.test(n)).sort((a, b) => num(a) - num(b));
    const indexText = F["prototype/index.html"] || "";
    const prototypes = versions.map((n) => ({ id: stem(n), html: F[n], current: F[n] === indexText }));
    if (indexText && !prototypes.some((v) => v.current)) prototypes.push({ id: "index", html: indexText, current: true });
    const pf = facts(pmd), note = pf.map(([, v]) => v).join(" ").toLowerCase() + pmd.toLowerCase();
    const c = carried(pmd), cl = linkFor("");
    return {
      project: raw.project, title: titleOf(pmd, `Discovery: ${raw.project}`),
      facts: pf.map(([k, v]) => ({ k, v: inline(v, cl) })), demo: note.includes("demonstration"),
      phases, prototypes, carried: Object.fromEntries(Object.entries(c).map(([k, v]) => [k, inline(v, cl)])),
      decision: decision(byPath["validate/decision.md"] || ""), evidence: totals, updated: raw.updated || "", now: raw.now || null,
    };
  }
  /* collect:end */

  const blob = document.getElementById("journey-data").textContent.trim();
  const RAW = blob ? JSON.parse(blob) : {};
  if (!RAW.files) {
    document.body.replaceChildren(Object.assign(document.createElement("p"), { className: "waiting",
      textContent: "The journey app is waiting for its first update. The assistant fills it in after Setup." }));
    return;
  }
  const D = collect(RAW);
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
  // Stay current, wherever the page is shown: a browser tab (file:) or an app's preview frame.
  // Reload only when nobody has touched the page for a while, and come back to the same view and scroll.
  const reloadHere = () => {
    try { sessionStorage.setItem("journey-scroll", String(window.scrollY)); } catch (e) { /* storage blocked */ }
    try { location.reload(); } catch (e) { /* reload blocked */ }
  };
  const live = (text) => { document.documentElement.classList.add("live-view"); $("#live").replaceWith(el("span", { class: "live", text })); };
  let touched = Date.now();
  ["click", "keydown", "scroll", "wheel", "touchstart"].forEach((t) => addEventListener(t, () => { touched = Date.now(); }, { passive: true }));
  const whenIdle = (fn) => { const tick = () => (Date.now() - touched >= 15000 ? fn() : setTimeout(tick, 2000)); tick(); };
  const timed = () => { live("Live: refreshes every 15 seconds"); setTimeout(() => whenIdle(reloadHere), 15000); };
  if (location.protocol === "file:") timed();
  else {
    // In a preview: read the file again every 10 seconds and reload only when its data changed.
    // If the preview does not let the page read its own file, reload on a timer instead.
    const url = location.href.split("#")[0];
    let first = true;
    const poll = async () => {
      try {
        const text = await (await fetch(url, { cache: "no-store" })).text();
        const m = text.match(/<script id="journey-data" type="application\/json">([\s\S]*?)<\/script>/);
        if (!m) throw new Error("not the journey page");
        if (m[1].trim() && m[1].trim() !== blob) { whenIdle(reloadHere); return; }
        if (first) live("Live: updates when the files change");
        first = false;
        setTimeout(poll, 10000);
      } catch (e) { if (first) timed(); }
    };
    poll();
  }
  if (D.now && (D.now.phase || D.now.step)) {
    const n = $("#now"); n.classList.add("on");
    n.append(el("span", { class: "tag", text: "Now" }), el("span", { class: "where", text: [D.now.phase, D.now.step].filter(Boolean).join(" \u00b7 ") }));
    if (D.now.doing) n.append(el("span", { class: "doing", text: D.now.doing }));
    if (D.now.next) n.append(el("span", { class: "next", text: "Next: " + D.now.next }));
  }
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
  const here = D.now && D.phases.find((p) => p.name.toLowerCase() === String(D.now.phase || "").toLowerCase());
  if (here) track.querySelector(`[data-view="${here.id}"]`).classList.add("here");
  const reached = D.phases.reduce((n, p, i) => (p.status === "Complete" ? i + 1 : p.status === "In progress" ? Math.max(n, i + 0.5) : n), 0);
  requestAnimationFrame(() => requestAnimationFrame(() =>
    track.style.setProperty("--done", reached >= D.phases.length ? "100%" : `${((reached + 0.5) / (D.phases.length + 1)) * 100}%`)));

  function overview() {
    const pane = $("#pane"); pane.replaceChildren();
    const current = here || D.phases.find((p) => p.status === "In progress") || D.phases.find((p) => p.status !== "Complete");
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
      pane.replaceChildren(el("p", { class: "empty", text: `${d.path} has not been written yet. It is part of the ${D.phases.find((p) => p.id === d.phase).name} phase; ask the assistant to run that step.` }));
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
    const hash = view === "overview" ? "" : "#" + view + (state.doc ? "/" + state.doc : state.proto ? "/proto/" + state.proto : "");
    try { history.replaceState(null, "", hash || location.pathname + location.search); } catch (e) { /* sandboxed viewers */ }
    try { sessionStorage.setItem("journey-view", hash); } catch (e) { /* storage blocked */ }
    if (!opts.keepScroll) window.scrollTo({ top: 0 });
  }

  document.addEventListener("click", (e) => {
    const station = e.target.closest(".station"), doc = e.target.closest("[data-doc]"), proto = e.target.closest("[data-proto]");
    if (station) { go(station.dataset.view); return; }
    if (doc) { e.preventDefault(); const d = docs[doc.dataset.doc]; if (d) go(d.phase, { doc: d.path, focus: true }); return; }
    if (proto) { e.preventDefault(); go("prototype", { proto: proto.dataset.proto, focus: true }); }
  });
  let where = location.hash || "";
  if (!where) { try { where = sessionStorage.getItem("journey-view") || ""; } catch (e) { /* storage blocked */ } }
  const [start, ...rest] = decodeURIComponent(where.replace(/^#\/?/, "")).split("/");
  const sub = rest.join("/");
  if (!D.phases.some((p) => p.id === start)) go("overview", { keepScroll: true });
  else if (sub.startsWith("proto/")) go(start, { proto: sub.slice(6), keepScroll: true });
  else go(start, { doc: docs[sub] ? sub : undefined, keepScroll: true });
  let y = null;
  try { y = sessionStorage.getItem("journey-scroll"); sessionStorage.removeItem("journey-scroll"); } catch (e) { /* private mode */ }
  if (y !== null) requestAnimationFrame(() => window.scrollTo(0, +y));
})();
</script>
</body>
</html>
```
