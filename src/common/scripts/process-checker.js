#!/usr/bin/env node
// Minimal deterministic join-barrier checker for discovery.
// Reads the session index and reports whether the join (open-questions) can run.
// Usage: node process-checker.js [path/to/session-index.md]
const fs = require("fs");
const file = process.argv[2] || "Product-Definition/state/session-index.md";

if (!fs.existsSync(file)) {
  console.log(JSON.stringify({ error: `missing ${file}` }));
  process.exit(1);
}

const txt = fs.readFileSync(file, "utf8");
const field = (k) =>
  (txt.match(new RegExp(`^- ${k}:\\s*(.+)$`, "im")) || [])[1]?.trim().toLowerCase();

const business = field("business");
const technical = field("technical");
const ready = business === "complete" && technical === "complete";

console.log(
  JSON.stringify(
    { business, technical, join: ready ? "ready" : "blocked", next: ready ? "open-questions" : "continue-roles" },
    null,
    2
  )
);
