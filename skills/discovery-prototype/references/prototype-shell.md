# Prototype shell

Every prototype version starts as an exact copy of the HTML below. Copy the whole code block into `prototype/v[N].html`, then change only the region between the `EDIT BELOW` and `EDIT ABOVE` markers near the end of the file: the `PROTOTYPE` settings, the persona walkthroughs, and the screen templates. Everything else stays exactly as it is: it provides the Flow, Mobile, Desktop, and Personas views, the phone and browser frames, routing, steppers, the test moment toggle, and the persona replay.

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
    1. the PROTOTYPE settings in the script block with id "prototype-settings",
    2. the WALKTHROUGHS list in the script block with id "persona-walkthroughs"
       (empty in a new version; the persona critique fills it in), and
    3. the screen templates inside the element with id "screens".
  Keep everything else as it is. The shell provides the Flow, Mobile, Desktop, and
  Personas views, the device frames, navigation, steppers, the test moment toggle,
  and the persona replay.
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

  /* Persona replay */
  .tabs a[hidden] { display: none; }
  .rp-ok { --rp: #2e7d4f; } .rp-warn { --rp: #965a00; } .rp-bad { --rp: #c0392b; }  /* fixed, so moods read the same in every theme */
  .rp-people { display: flex; flex-direction: column; gap: 8px; width: 220px; }
  .rp-person { display: flex; flex-direction: column; gap: 2px; text-align: left; padding: 10px 12px; border-radius: 12px;
    border: 1px solid var(--line); background: var(--surface); cursor: pointer; }
  .rp-person[aria-pressed="true"] { border-color: var(--ink); box-shadow: 0 1px 3px rgba(0,0,0,.12); }
  .rp-phone .content { pointer-events: none; }
  .rp-target, .rp-look { position: relative; outline: 3px solid var(--rp); outline-offset: 3px; border-radius: 10px; }
  .rp-look { outline-style: dashed; }
  .rp-target::after { content: ""; position: absolute; left: 50%; top: 50%; width: 30px; height: 30px; margin: -15px 0 0 -15px;
    border-radius: 50%; background: rgba(255,255,255,.18); border: 2px solid #fff; box-shadow: 0 0 0 2px var(--rp); pointer-events: none; }
  .rp-side h3 { margin-bottom: 2px; } .rp-side p { margin: 0; }
  .rp-bubble { background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--rp); border-radius: var(--radius);
    padding: 14px 16px; box-shadow: var(--shadow); margin: 12px 0; }
  .rp-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .rp-mood { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; color: #fff; background: var(--rp); }
  .rp-side .rp-say { font: 17px/1.4 var(--font-head); margin: 10px 0 8px; }
  .rp-tap.dead { color: var(--danger); font-weight: 600; }
  .rp-finding { margin-top: 6px; color: var(--muted); }
  .rp-check { margin-top: 8px; padding: 6px 8px; border-radius: 8px; background: #f6dedc; color: var(--danger); }
  .rp-controls { display: flex; gap: 8px; }
  .rp-controls button { flex: 1; min-height: 44px; border-radius: 10px; border: 1px solid var(--line); background: var(--surface); cursor: pointer; }
  .rp-controls button:disabled { opacity: .4; cursor: default; }
  .side ol.rp-steps { list-style: none; padding: 0; margin: 12px 0; }
  .rp-steps button { display: flex; gap: 8px; width: 100%; text-align: left; padding: 6px 8px; border: 0; background: none;
    border-radius: 8px; cursor: pointer; color: var(--muted); font-size: 13px; }
  .rp-steps button[aria-current="step"] { background: var(--surface); color: var(--ink); font-weight: 600; }
  .rp-dot { flex: 0 0 auto; width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; background: var(--rp); }
  @media (prefers-reduced-motion: no-preference) { .rp-target::after { animation: rp-tap 1.4s ease-out infinite; } }
  @keyframes rp-tap { 0%, 100% { transform: scale(.7); opacity: 1; } 60% { transform: scale(1.35); opacity: .25; } }
</style>
<style id="theme"></style>
</head>
<body>
<header class="topbar">
  <h1 id="product"></h1><span class="meta" id="meta"></span>
  <nav class="tabs" aria-label="Views">
    <a href="#/flow" data-view="flow">Flow</a><a href="#/mobile" data-view="mobile">Mobile</a><a href="#/desktop" data-view="desktop">Desktop</a><a href="#/replay" data-view="replay" id="tab-replay" hidden>Personas</a>
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
  <section class="view" id="view-replay"><div class="stage">
    <div class="rp-people" id="rp-people" aria-label="Personas"></div>
    <div id="rp-phone"></div>
    <aside class="side rp-side">
      <div id="rp-who"></div>
      <div class="rp-bubble" id="rp-bubble" aria-live="polite"></div>
      <div class="rp-controls"><button id="rp-prev">← Back</button><button id="rp-play">Play</button><button id="rp-next">Next →</button></div>
      <ol class="rp-steps" id="rp-steps"></ol>
      <p class="small muted">A replay of the persona critique on the real screens. Synthetic personas, not customers.</p>
    </aside>
  </div></section>
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
  Persona walkthroughs: empty in a new version. The persona critique writes them into the
  version it critiques, as JSON (double-quoted keys and strings), one entry per persona, with
  the steps in the order the persona took them:
    {"id": "sam", "name": "Sam Okafor", "role": "Shop owner",
     "context": "Between customers, phone in one hand", "score": 7, "steps": [
      {"screen": "start", "tap": "Continue", "say": "Quick enough.", "mood": "ok"},
      {"screen": "done", "look": "All set", "say": "All set? Where is my order number?", "mood": "hesitate", "finding": 2}]}
  id: the persona's file name without .md. screen: a screen id. tap: the text of the button or
  card the persona taps, copied from that screen; leave it out when they only look, or stop.
  look: text on the screen they read or look for. mood: ok, hesitate, stuck, or gave-up.
  finding: the number of the finding in the critique's table. The Personas view replays every
  step on the real screen, shows where each tap leads, and flags a step that does not fit.
-->
<script id="persona-walkthroughs">
const WALKTHROUGHS = [];
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
  const W = typeof WALKTHROUGHS === "undefined" ? [] : WALKTHROUGHS;
  $("#tab-replay").hidden = !W.length;
  $("#flow-sub").textContent = `${screens.length} screens · tick "Show test moment" to see what this prototype tests`
    + (W.length ? ` · open Personas to watch ${W.length} personas walk through it` : "");
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
  let rp = { p: 0, s: 0 }, timer = null;
  function setAddress() {
    const tail = current.view === "flow" ? "" : current.view === "replay" ? `/${W[rp.p].id || rp.p + 1}/${rp.s + 1}` : "/" + current.id;
    // Some viewers (sandboxed frames) block address changes; the prototype works without them.
    try { history.replaceState(null, "", `#/${current.view}${tail}`); } catch (e) { /* ignore */ }
  }

  // Persona replay: each persona's walk through the flow, recorded by the persona critique.
  const MOOD = { ok: ["Fine", "rp-ok"], hesitate: ["Hesitates", "rp-warn"], stuck: ["Stuck", "rp-bad"], "gave-up": ["Gives up", "rp-bad"] };
  const mood = (m) => MOOD[m] || MOOD.ok;
  const title = (id) => (byId[id] || { title: id }).title;
  const norm = (t) => String(t || "").replace(/[“”"]/g, "").replace(/[‘’]/g, "'").replace(/\s+/g, " ").trim().toLowerCase();
  function findText(root, text) {
    // The innermost element that shows the text: exact match first, then one that contains it.
    const want = norm(text), all = [...root.querySelectorAll("*")];
    if (!want) return null;
    const exact = all.filter((e) => norm(e.textContent) === want);
    const pool = exact.length ? exact : all.filter((e) => norm(e.textContent).includes(want));
    return pool.find((e) => !pool.some((o) => o !== e && e.contains(o))) || null;
  }
  function tapResult(t) {
    const go = t.closest("[data-go]");
    if (go && byId[go.dataset.go]) return { to: go.dataset.go, text: `goes to ${title(go.dataset.go)}` };
    if (t.closest("[data-inc], [data-dec]")) return { text: "changes the number" };
    return { dead: true, text: "nothing happens, it is not linked to a screen" };
  }
  function stopPlay() { clearInterval(timer); timer = null; $("#rp-play").textContent = "Play"; }
  function showStep() {
    const w = W[rp.p], list = w.steps || [];
    rp.s = Math.min(Math.max(rp.s, 0), Math.max(list.length - 1, 0));
    const st = list[rp.s] || {}, next = list[rp.s + 1], s = byId[st.screen] || screens[0], [label, ring] = mood(st.mood);
    current.id = s.id;
    $("#rp-people").replaceChildren(...W.map((x, i) => {
      const b = el("button", "rp-person"), stops = (x.steps || []).filter((y) => y.mood === "stuck" || y.mood === "gave-up").length;
      b.dataset.rp = i; b.setAttribute("aria-pressed", String(i === rp.p));
      b.append(el("b", "", x.name), el("span", "small muted", x.role || ""),
        el("span", "small", `Day one: ${x.score != null ? x.score : "–"}/10 · ${stops ? stops + " stuck" : "never stuck"}`));
      return b;
    }));
    const ph = phone(s); ph.classList.add("rp-phone", ring);
    $("#rp-phone").replaceChildren(ph);
    const c = ph.querySelector(".content"), checks = [];
    const tapHit = st.tap ? findText(c, st.tap) : null, tap = tapHit && (tapHit.closest("[data-go], button, a, [data-inc], [data-dec]") || tapHit);
    const lookHit = st.look ? findText(c, st.look) : null, look = lookHit && (lookHit.closest(".card, .row, .btn, p") || lookHit);
    if (look && look !== tap) look.classList.add("rp-look");
    if (tap) tap.classList.add("rp-target");
    const focus = tap || look;
    if (focus) c.scrollTop += focus.getBoundingClientRect().top - c.getBoundingClientRect().top - c.clientHeight / 3;

    const meta = el("div", "rp-meta");
    meta.append(el("span", "rp-mood", label), el("span", "small muted", `Step ${rp.s + 1} of ${list.length} · ${s.title}`));
    const parts = [meta, el("p", "rp-say", st.say ? `“${st.say}”` : "")];
    if (!byId[st.screen]) checks.push(`There is no screen “${st.screen}”.`);
    if (st.look && !look) checks.push(`“${st.look}” is not on this screen.`);
    if (st.tap && !tap) checks.push(`“${st.tap}” is not on this screen.`);
    if (tap) {
      const r = tapResult(tap);
      parts.push(el("div", "small rp-tap" + (r.dead ? " dead" : ""), `Taps “${st.tap}”: ${r.text}.`));
      if (next && r.to && next.screen !== r.to) checks.push(`This tap goes to ${title(r.to)}, but the next step is on ${title(next.screen)}.`);
      if (next && r.dead && next.screen !== s.id) checks.push(`This tap leads nowhere, but the next step is on ${title(next.screen)}.`);
    } else if (!st.tap) {
      parts.push(el("div", "small rp-tap", next ? "Looks, does not tap." : "Stops here."));
      if (next && next.screen !== s.id) checks.push(`Nothing is tapped, but the next step is on ${title(next.screen)}.`);
    }
    if (st.finding) parts.push(el("div", "small rp-finding", `Finding ${st.finding} in the persona critique`));
    if (checks.length) parts.push(el("div", "small rp-check", "Replay check: " + checks.join(" ")));
    $("#rp-bubble").className = "rp-bubble " + ring;
    $("#rp-bubble").replaceChildren(...parts);
    $("#rp-who").replaceChildren(el("h3", "", w.name), el("p", "small muted", [w.role, w.context].filter(Boolean).join(" · ")));
    $("#rp-steps").replaceChildren(...list.map((x, i) => {
      const li = el("li"), b = el("button", mood(x.mood)[1]);
      b.dataset.rpStep = i; if (i === rp.s) b.setAttribute("aria-current", "step");
      b.append(el("span", "rp-dot"), el("span", "", `${i + 1}. ${title(x.screen)}: ${x.tap ? `taps “${x.tap}”` : x.look ? `looks at “${x.look}”` : "stops"}`));
      li.append(b); return li;
    }));
    $("#rp-prev").disabled = rp.s === 0; $("#rp-next").disabled = rp.s >= list.length - 1;
    setAddress();
  }
  const stepBy = (d) => { rp.s += d; showStep(); };
  $("#rp-prev").addEventListener("click", () => { stopPlay(); stepBy(-1); });
  $("#rp-next").addEventListener("click", () => { stopPlay(); stepBy(1); });
  $("#rp-play").addEventListener("click", () => {
    if (timer) return stopPlay();
    if (rp.s >= (W[rp.p].steps || []).length - 1) { rp.s = 0; showStep(); }
    $("#rp-play").textContent = "Pause";
    timer = setInterval(() => (rp.s >= (W[rp.p].steps || []).length - 1 ? stopPlay() : stepBy(1)), 3500);
  });
  document.addEventListener("keydown", (e) => {
    if (current.view !== "replay" || e.target.closest("input, textarea")) return;
    if (e.key === "ArrowRight") { stopPlay(); stepBy(1); }
    if (e.key === "ArrowLeft") { stopPlay(); stepBy(-1); }
  });

  function render(view, id) {
    if (view === "replay" && !W.length) view = "flow";
    if (view === "replay") {
      const [pid, n] = String(id || "").split("/");
      let i = W.findIndex((w) => w.id === pid);
      if (i < 0 && /^\d+$/.test(pid)) i = Math.min(+pid, W.length) - 1;
      if (i >= 0) rp = { p: i, s: (parseInt(n, 10) || 1) - 1 };
    } else stopPlay();
    const s = byId[id] || byId[current.id] || screens[0];
    current = { view, id: s.id };
    $$(".view").forEach((v) => v.classList.toggle("active", v.id === "view-" + view));
    $$(".tabs a").forEach((a) => a.setAttribute("aria-current", a.dataset.view === view ? "page" : "false"));
    if (view === "mobile") { fill($("#mobile"), s.tpl); steps(s.id, $("#steps-m"), false); }
    if (view === "desktop") {
      fill($("#desktop"), s.desktop || s.tpl); steps(s.id, $("#steps-d"), true);
      $("#url").textContent = "https://" + String(P.url || "").replace(/\/?$/, "/") + s.id;
    }
    if (view === "replay") showStep();
    setAddress();
    window.scrollTo(0, 0);
  }
  function fromAddress() {
    const parts = (location.hash || "").split("/");
    const view = ["flow", "mobile", "desktop", "replay"].includes(parts[1]) ? parts[1] : "flow";
    return { view, id: view === "replay" ? parts.slice(2).join("/") : parts[2] };
  }
  document.addEventListener("click", (e) => {
    const tab = e.target.closest(".tabs a[data-view]"), nav = e.target.closest("#steps-d a[data-id]");
    const go = e.target.closest("[data-go]"), inc = e.target.closest("[data-inc]"), dec = e.target.closest("[data-dec]");
    const person = e.target.closest("[data-rp]"), jump = e.target.closest("[data-rp-step]");
    if (tab) { e.preventDefault(); render(tab.dataset.view, current.id); return; }
    if (nav) { e.preventDefault(); render("desktop", nav.dataset.id); return; }
    if (person) { stopPlay(); rp = { p: +person.dataset.rp, s: 0 }; showStep(); return; }
    if (jump) { stopPlay(); rp.s = +jump.dataset.rpStep; showStep(); return; }
    if (go && (current.view === "mobile" || current.view === "desktop")) { e.preventDefault(); render(current.view, go.dataset.go); return; }
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
