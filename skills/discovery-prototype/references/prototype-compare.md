# Prototype compare page

`prototype/compare.html` starts as an exact copy of the HTML below. Copy the whole code block, then change only the `COMPARE` settings in the marked edit region near the end: one entry per version file, oldest first, and `chosen` once Validate picks a version.

````html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prototype versions</title>
<!--
  AI-DLC Discovery prototype compare page.
  Copy this file to prototype/compare.html and edit ONLY the COMPARE settings in the
  marked edit region near the end: one entry per version file, oldest first.
-->
<style>
  :root { --bg: #f5f2ed; --surface: #fff; --ink: #1d1b18; --muted: #6b665e; --line: #e4ded4; --accent: #2f6f4f;
    --font-head: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink); font: 15px/1.45 var(--font-body); }
  header { display: flex; align-items: center; gap: 16px; padding: 14px 24px; background: var(--surface); border-bottom: 1px solid var(--line); position: sticky; top: 0; }
  header h1 { margin: 0; font: 600 18px var(--font-head); }
  header .meta { color: var(--muted); font-size: 13px; }
  .views { margin-left: auto; display: flex; gap: 4px; background: var(--bg); padding: 4px; border-radius: 999px; }
  .views button { border: 0; background: transparent; padding: 6px 14px; border-radius: 999px; cursor: pointer; font: inherit; }
  .views button[aria-pressed="true"] { background: var(--surface); font-weight: 600; box-shadow: 0 1px 3px rgba(0,0,0,.12); }
  .grid { display: grid; gap: 20px; padding: 24px; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); }
  .col { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; }
  .col.chosen { outline: 3px solid var(--accent); }
  .col header { position: static; border: 0; border-bottom: 1px solid var(--line); padding: 12px 16px; display: block; }
  .col h2 { margin: 0; font: 600 16px var(--font-head); }
  .col p { margin: 4px 0 0; color: var(--muted); font-size: 13px; }
  .col a { font-size: 13px; color: var(--accent); }
  iframe { border: 0; width: 100%; height: 720px; background: var(--bg); }
</style>
</head>
<body>
<header><h1 id="title"></h1><span class="meta" id="meta"></span>
  <div class="views" role="group" aria-label="View">
    <button data-view="flow" aria-pressed="true">Flow</button><button data-view="mobile" aria-pressed="false">Mobile</button><button data-view="desktop" aria-pressed="false">Desktop</button>
  </div>
</header>
<div class="grid" id="grid"></div>

<!-- ============================== EDIT BELOW ============================== -->
<script id="compare-settings">
const COMPARE = {
  product: "Product name",
  chosen: "",   // the version chosen for the handoff, for example "v3"; empty until Validate
  versions: [
    { version: "v1", file: "v1.html", change: "First build from the screen plan" },
    { version: "v2", file: "v2.html", change: "What changed, and the finding behind it" }
  ]
};
</script>
<!-- ============================== EDIT ABOVE ============================== -->

<script>
(function () {
  const C = COMPARE, grid = document.getElementById("grid");
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  document.title = `${C.product}: prototype versions`;
  document.getElementById("title").textContent = `${C.product}: prototype versions`;
  document.getElementById("meta").textContent = C.versions.length + " versions" + (C.chosen ? ` · chosen for the handoff: ${C.chosen}` : "");
  const frames = C.versions.map((v) => {
    const col = el("section", "col" + (v.version === C.chosen ? " chosen" : "")), head = el("header");
    const h = el("h2", "", v.version + (v.version === C.chosen ? " · chosen" : "")), link = el("a", "", "open alone");
    link.href = v.file + "#/flow"; link.target = "_blank";
    head.append(h, el("p", "", v.change), link);
    const frame = el("iframe"); frame.title = v.version; frame.loading = "lazy"; frame.src = v.file + "#/flow";
    col.append(head, frame); grid.append(col);
    return { v, frame, link };
  });
  document.querySelectorAll(".views button").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll(".views button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    frames.forEach(({ v, frame, link }) => { frame.src = `${v.file}#/${b.dataset.view}`; link.href = frame.src; });
  }));
})();
</script>
</body>
</html>
````
