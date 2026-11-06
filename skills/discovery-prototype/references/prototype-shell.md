# Prototype shell

Every prototype version starts as an exact copy of the HTML below. Copy the whole code block into `prototype/v[N].html`, then change only the region between the `EDIT BELOW` and `EDIT ABOVE` markers near the end of the file: the `PROTOTYPE` settings and the screen templates. Everything else stays exactly as it is: it provides the Flow, Mobile, and Desktop views, the phone and browser frames, routing, steppers, and the test moment toggle.

````html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prototype</title>
<!--
  AI-DLC Discovery prototype shell.
  Copy this file to prototype/v[N].html. Edit ONLY:
    1. the PROTOTYPE settings in the script block with id "prototype-settings", and
    2. the screen templates inside the element with id "screens".
  Keep everything else as it is. The shell provides the Flow, Mobile, and Desktop
  views, the device frames, navigation, steppers, and the test moment toggle.
  One self-contained file: no external requests.
-->
<style>
  :root {
    --bg: #f5f2ed; --surface: #ffffff; --ink: #1d1b18; --muted: #6b665e; --line: #e4ded4;
    --accent: #2f6f4f; --accent-ink: #ffffff; --danger: #b3261e; --warn: #9a6400;
    --radius: 14px; --space: 8px; --shadow: 0 10px 30px rgba(29, 27, 24, .12);
    --font-head: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink); font: 15px/1.45 var(--font-body); }
  button { font: inherit; color: inherit; }
  .topbar { position: sticky; top: 0; z-index: 5; display: flex; align-items: center; gap: calc(var(--space) * 2);
    padding: calc(var(--space) * 1.5) calc(var(--space) * 3); background: var(--surface); border-bottom: 1px solid var(--line); }
  .topbar h1 { margin: 0; font: 600 17px var(--font-head); }
  .topbar .meta { color: var(--muted); font-size: 13px; }
  .tabs { display: flex; gap: 4px; margin-left: auto; background: var(--bg); padding: 4px; border-radius: 999px; }
  .tabs a { padding: 6px 14px; border-radius: 999px; color: var(--ink); text-decoration: none; font-size: 14px; }
  .tabs a[aria-current="page"] { background: var(--surface); box-shadow: 0 1px 3px rgba(0,0,0,.12); font-weight: 600; }
  .toggle { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--muted); cursor: pointer; }
  main { padding: calc(var(--space) * 4) calc(var(--space) * 3); }
  .view { display: none; } .view.active { display: block; }
  .intro { max-width: 760px; margin: 0 auto calc(var(--space) * 4); text-align: center; }
  .intro h2 { font: 600 30px/1.2 var(--font-head); margin: 0 0 8px; }
  .intro p { color: var(--muted); margin: 0; }

  /* Phone frame */
  .phone { width: 300px; height: 620px; flex: 0 0 auto; background: #111; border-radius: 44px; padding: 12px; box-shadow: var(--shadow); position: relative; }
  .screen-area { width: 100%; height: 100%; background: var(--surface); border-radius: 34px; overflow: hidden; display: flex; flex-direction: column; position: relative; }
  .notch { position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 96px; height: 24px; background: #111; border-radius: 0 0 14px 14px; z-index: 2; }
  .statusbar { display: flex; justify-content: space-between; padding: 8px 22px 6px; font-size: 12px; font-weight: 600; }
  .statusbar span:first-child { min-width: 60px; } .statusbar span:last-child { min-width: 60px; text-align: right; }
  .phone .content { flex: 1; overflow-y: auto; padding: 8px 20px 20px; }
  .home { position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); width: 110px; height: 4px; background: var(--ink); opacity: .35; border-radius: 4px; }

  /* Flow board */
  .flow { display: flex; gap: 28px; overflow-x: auto; padding: 8px 8px 32px; align-items: flex-start; }
  .step { display: flex; flex-direction: column; gap: 12px; align-items: center; }
  .caption { width: 300px; }
  .caption b { display: block; font: 600 15px var(--font-head); }
  .caption span { color: var(--muted); font-size: 13px; }
  .arrow { align-self: center; color: var(--muted); font-size: 26px; }
  .flow .content { pointer-events: none; }

  /* Mobile view */
  .stage { display: flex; justify-content: center; gap: 40px; align-items: flex-start; flex-wrap: wrap; }
  .side { max-width: 320px; }
  .side h3 { font: 600 20px var(--font-head); margin: 0 0 6px; }
  .side ol { padding-left: 20px; color: var(--muted); }
  .side li.current { color: var(--ink); font-weight: 600; }

  /* Browser frame */
  .browser { max-width: 1100px; margin: 0 auto; background: var(--surface); border-radius: 12px; box-shadow: var(--shadow); overflow: hidden; border: 1px solid var(--line); }
  .chrome { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: #ece7df; border-bottom: 1px solid var(--line); }
  .dots span { display: inline-block; width: 11px; height: 11px; border-radius: 50%; margin-right: 6px; }
  .dots span:nth-child(1) { background: #ec6a5e; } .dots span:nth-child(2) { background: #f4bf4f; } .dots span:nth-child(3) { background: #61c554; }
  .url { flex: 1; background: var(--surface); border-radius: 8px; padding: 6px 12px; font-size: 13px; color: var(--muted); }
  .page { display: grid; grid-template-columns: 220px 1fr; min-height: 560px; }
  .page nav { border-right: 1px solid var(--line); padding: 20px; }
  .brand { font: 600 16px var(--font-head); margin-bottom: 16px; }
  .page nav a { display: block; padding: 8px 10px; border-radius: 8px; color: var(--muted); text-decoration: none; font-size: 14px; }
  .page nav a.current { background: var(--bg); color: var(--ink); font-weight: 600; }
  .page .content { padding: 32px 40px; max-width: 760px; }

  /* Building blocks for screens */
  .s-title { font: 600 24px/1.2 var(--font-head); margin: 12px 0 6px; }
  .s-sub { color: var(--muted); margin: 0 0 16px; }
  .card { background: var(--bg); border-radius: var(--radius); padding: 14px 16px; margin: 0 0 10px; }
  .row { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--line); }
  .pill { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; background: var(--bg); color: var(--muted); }
  .pill.ok { background: #e3efe7; color: var(--accent); } .pill.warn { background: #f7ead3; color: var(--warn); } .pill.bad { background: #f6dedc; color: var(--danger); }
  .btn { display: block; width: 100%; padding: 14px; border: 0; border-radius: 12px; background: var(--accent); color: var(--accent-ink); font-weight: 600; cursor: pointer; text-align: center; margin-top: 12px; min-height: 44px; }
  .btn.secondary { background: transparent; color: var(--ink); border: 1px solid var(--line); }
  .stepper { display: inline-flex; align-items: center; gap: 10px; }
  .stepper button { width: 32px; height: 32px; border-radius: 50%; border: 1px solid var(--line); background: var(--surface); cursor: pointer; }
  [data-go] { cursor: pointer; }
  .muted { color: var(--muted); } .small { font-size: 13px; }

  /* Test moment */
  .tm-on .test-moment { outline: 3px dashed var(--warn); outline-offset: 4px; border-radius: 8px; }
  .tm-note { display: none; margin-top: 12px; padding: 10px 12px; border-radius: 10px; background: #f7ead3; color: var(--warn); font-size: 13px; max-width: 300px; }
  .tm-on .tm-note { display: block; }
  @media (prefers-reduced-motion: no-preference) { .live > * { animation: fade .18s ease-out; } }
  @keyframes fade { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
</style>
<style id="theme"></style>
</head>
<body>
<header class="topbar">
  <h1 id="product"></h1><span class="meta" id="meta"></span>
  <nav class="tabs" aria-label="Views">
    <a href="#/flow" data-view="flow">Flow</a><a href="#/mobile" data-view="mobile">Mobile</a><a href="#/desktop" data-view="desktop">Desktop</a>
  </nav>
  <label class="toggle"><input type="checkbox" id="tm"> Show test moment</label>
</header>
<main>
  <section class="view" id="view-flow">
    <div class="intro"><h2 id="flow-title"></h2><p id="flow-sub"></p></div>
    <div class="flow" id="flow"></div>
  </section>
  <section class="view" id="view-mobile"><div class="stage">
    <div class="phone"><div class="screen-area"><div class="notch"></div><div class="statusbar"><span class="clock"></span><span>●●● 5G ▮</span></div><div class="content live" id="mobile"></div><div class="home"></div></div></div>
    <aside class="side"><h3>The flow</h3><ol id="steps-m"></ol><div class="tm-note"></div></aside>
  </div></section>
  <section class="view" id="view-desktop">
    <div class="browser"><div class="chrome"><span class="dots"><span></span><span></span><span></span></span><span class="url" id="url"></span></div>
      <div class="page"><nav id="steps-d"></nav><div class="content live" id="desktop"></div></div></div>
    <div class="tm-note" style="margin:16px auto 0"></div>
  </section>
</main>

<!-- ============================== EDIT BELOW ============================== -->
<script id="prototype-settings">
const PROTOTYPE = {
  product: "Product name",
  version: "v1",
  tagline: "One line from the PR/FAQ: who it is for and what it does.",
  url: "app.example.com",
  clock: "9:41",
  theme: {},                 // optional token overrides, for example { "--accent": "#1f5fa8" }
  testMoment: "What the team wants to learn on the highlighted screen.",
  state: { qty: 2 }          // starting values for steppers: data-inc / data-dec / data-bind
};
</script>
<!--
  Screens: one <template data-screen> per step of the flow, in order, 4 to 8 of them.
  Attributes: id, data-title, data-caption, and data-test-moment on the screen that tests
  the riskiest assumption. Optional desktop layout: a second <template data-desktop="id">.
  Navigate with data-go="screen-id". Mark the tested element with class="test-moment".
  Building blocks: s-title, s-sub, card, row, pill ok|warn|bad, btn, btn secondary,
  stepper, muted, small. Stepper example:
    <span class="stepper"><button data-dec="qty">−</button><b data-bind="qty"></b><button data-inc="qty">+</button></span>
-->
<div id="screens" hidden>
  <template data-screen id="start" data-title="Start" data-caption="Where the persona begins">
    <div class="s-title">Hello</div>
    <p class="s-sub">Replace with the first screen.</p>
    <button class="btn" data-go="done">Continue</button>
  </template>
  <template data-screen id="done" data-title="Done" data-caption="The confirmation" data-test-moment>
    <div class="s-title test-moment">All set</div>
    <button class="btn secondary" data-go="start">Start again</button>
  </template>
</div>
<!-- ============================== EDIT ABOVE ============================== -->

<script>
(function () {
  const P = PROTOTYPE, $ = (s) => document.querySelector(s), $$ = (s) => [...document.querySelectorAll(s)];
  const state = Object.assign({}, P.state || {});
  const screens = $$("#screens template[data-screen]").map((t) => ({
    id: t.id, title: t.dataset.title || t.id, caption: t.dataset.caption || "", test: t.hasAttribute("data-test-moment"), tpl: t,
    desktop: document.querySelector(`#screens template[data-desktop="${t.id}"]`)
  }));
  const byId = Object.fromEntries(screens.map((s) => [s.id, s]));
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const fill = (target, tpl) => { target.replaceChildren(tpl.content.cloneNode(true)); bind(target); };
  const bind = (root) => root.querySelectorAll("[data-bind]").forEach((b) => (b.textContent = state[b.dataset.bind]));

  document.title = `${P.product}: prototype ${P.version}`;
  $("#theme").textContent = ":root{" + Object.entries(P.theme || {}).map(([k, v]) => `${k}:${v}`).join(";") + "}";
  $("#product").textContent = P.product;
  $("#meta").textContent = `${P.version} · prototype on fictional data`;
  $("#flow-title").textContent = P.tagline;
  $("#flow-sub").textContent = `${screens.length} screens · tick "Show test moment" to see what this prototype tests`;
  $$(".clock").forEach((c) => (c.textContent = P.clock || "9:41"));
  $$(".tm-note").forEach((n) => (n.textContent = "Test moment: " + P.testMoment));

  function phone(screen) {
    const p = el("div", "phone"), a = el("div", "screen-area"), bar = el("div", "statusbar"), c = el("div", "content");
    bar.append(el("span", "", P.clock || "9:41"), el("span", "", "●●● 5G ▮"));
    a.append(el("div", "notch"), bar, c, el("div", "home")); p.append(a); fill(c, screen.tpl); return p;
  }
  const flow = $("#flow");
  screens.forEach((s, i) => {
    const step = el("div", "step"), cap = el("div", "caption");
    cap.append(el("b", "", `${i + 1}. ${s.title}`), el("span", "", s.caption));
    step.append(phone(s), cap); flow.append(step);
    if (i < screens.length - 1) { const a = el("div", "arrow", "→"); a.setAttribute("aria-hidden", "true"); flow.append(a); }
  });

  function steps(current, target, desktop) {
    const items = screens.map((s) => {
      const item = desktop ? el("a", s.id === current ? "current" : "", s.title) : el("li", s.id === current ? "current" : "", s.title);
      if (desktop) { item.href = `#/desktop/${s.id}`; item.dataset.id = s.id; }
      return item;
    });
    if (desktop) items.unshift(el("div", "brand", P.product));
    target.replaceChildren(...items);
  }
  let current = { view: "flow", id: screens[0] && screens[0].id };
  function setAddress() {
    // Some viewers (sandboxed frames) block address changes; the prototype works without them.
    try { history.replaceState(null, "", `#/${current.view}${current.view === "flow" ? "" : "/" + current.id}`); } catch (e) { /* ignore */ }
  }
  function render(view, id) {
    const s = byId[id] || byId[current.id] || screens[0];
    current = { view, id: s.id };
    $$(".view").forEach((v) => v.classList.toggle("active", v.id === "view-" + view));
    $$(".tabs a").forEach((a) => a.setAttribute("aria-current", a.dataset.view === view ? "page" : "false"));
    if (view === "mobile") { fill($("#mobile"), s.tpl); steps(s.id, $("#steps-m"), false); }
    if (view === "desktop") {
      fill($("#desktop"), s.desktop || s.tpl); steps(s.id, $("#steps-d"), true);
      $("#url").textContent = "https://" + String(P.url || "").replace(/\/?$/, "/") + s.id;
    }
    setAddress();
    window.scrollTo(0, 0);
  }
  function fromAddress() {
    const parts = (location.hash || "").split("/");
    return { view: ["flow", "mobile", "desktop"].includes(parts[1]) ? parts[1] : "flow", id: parts[2] };
  }
  document.addEventListener("click", (e) => {
    const tab = e.target.closest(".tabs a[data-view]"), nav = e.target.closest("#steps-d a[data-id]");
    const go = e.target.closest("[data-go]"), inc = e.target.closest("[data-inc]"), dec = e.target.closest("[data-dec]");
    if (tab) { e.preventDefault(); render(tab.dataset.view, current.id); return; }
    if (nav) { e.preventDefault(); render("desktop", nav.dataset.id); return; }
    if (go && current.view !== "flow") { e.preventDefault(); render(current.view, go.dataset.go); return; }
    if (inc) { state[inc.dataset.inc] = (state[inc.dataset.inc] || 0) + 1; bind(document); }
    if (dec) { state[dec.dataset.dec] = Math.max(0, (state[dec.dataset.dec] || 0) - 1); bind(document); }
  });
  $("#tm").addEventListener("change", (e) => document.body.classList.toggle("tm-on", e.target.checked));
  window.addEventListener("hashchange", () => { const a = fromAddress(); render(a.view, a.id); });
  const start = fromAddress();
  render(start.view, start.id);
})();
</script>
</body>
</html>
````
