#!/usr/bin/env node
// Minimal build: assembles dist/<target>/ from src/skills + src/common + src/targets/<target>.
// Usage: `node build.js` (all targets) or `node build.js kiro`.
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const SRC = path.join(ROOT, "src");
const RULES = path.join(ROOT, "aidlc-discovery-rules", "aidlc-discovery-rule-details");
const TARGETS = ["kiro", "claude", "amazon-quick"];

function copyDir(from, to) {
  if (!fs.existsSync(from)) return;
  fs.mkdirSync(to, { recursive: true });
  for (const e of fs.readdirSync(from, { withFileTypes: true })) {
    if (e.name === ".keep" || e.name === ".DS_Store") continue;
    const s = path.join(from, e.name);
    const d = path.join(to, e.name);
    e.isDirectory() ? copyDir(s, d) : fs.copyFileSync(s, d);
  }
}

// Place the shared core (skills + aidlc-common + question banks) under `base`.
function copyCore(base) {
  copyDir(path.join(SRC, "skills"), path.join(base, "skills"));
  copyDir(path.join(SRC, "common"), path.join(base, "aidlc-common"));
  copyDir(RULES, path.join(base, "aidlc-discovery-rules", "aidlc-discovery-rule-details"));
}

function build(target) {
  const dist = path.join(ROOT, "dist", target);
  fs.rmSync(dist, { recursive: true, force: true });

  if (target === "kiro" || target === "claude") {
    // Kiro/Claude load skills/ + aidlc-common/ from the install dir; adapter overlays on top.
    const out = path.join(dist, target === "kiro" ? ".kiro" : ".claude");
    copyCore(out);
    copyDir(path.join(SRC, "targets", target), out);
    console.log(`built ${path.relative(ROOT, out)}`);
  } else if (target === "amazon-quick") {
    // Quick installs ONE self-contained skill folder (imported via the UI); everything is bundled inside it.
    const skill = path.join(dist, "skills", "aidlc-discovery");
    copyDir(path.join(SRC, "targets", "amazon-quick"), skill); // SKILL.md
    copyCore(skill);                                           // core bundled INSIDE the skill folder
    console.log(`built ${path.relative(ROOT, skill)}`);
  } else {
    throw new Error(`unknown target: ${target}`);
  }
}

const arg = process.argv[2];
(arg ? [arg] : TARGETS).forEach(build);
