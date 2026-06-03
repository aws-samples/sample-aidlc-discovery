# Install AI-DLC Discovery v2

Two ways to install:

- **Automated (paste a prompt)** — your agent downloads the matching bundle from the `v2.0.0` release and installs it. No Node, no local build. *Recommended for users.*
- **From source (build)** — run `node build.js` and copy `dist/<target>/` yourself (the per-platform sections below). *For contributors / offline.*

## Automated install (paste a prompt)

Paste this into your agent (Kiro, Claude Code, or Amazon Quick desktop):

```
Set up aidlc-discovery v2 in this project. Do every step yourself and report back when done:

1. Detect which platform you are running in: Kiro, Claude Code, or Amazon Quick desktop.
2. Download the matching asset from the v2.0.0 release (replace <platform> with kiro | claude | quick):
   https://github.com/aws-samples/sample-aidlc-discovery/releases/download/v2.0.0/aidlc-discovery-<platform>-v2.0.0.zip
3. Unzip and install to the platform's location:
   - kiro   -> merge the bundle into ./.kiro/
   - claude -> merge the bundle into ./.claude/
   - quick  -> copy the aidlc-discovery/ skill folder into ~/.quickwork/profiles/federate-prod/skills/
4. Confirm the install path and the invocation phrase
   (Kiro / Quick: "start aidlc-discovery"; Claude Code: "/aidlc-discovery").
```

> `v2.0.0` is a pre-release, so the prompt pins the `v2.0.0` tag explicitly — it works even while `releases/latest` still points to v1.

## Prerequisites

- [Node.js](https://nodejs.org/) (runs `build.js` and the deterministic `process-checker.js`).
- One supported platform: **Kiro IDE/CLI**, **Claude Code** (or Claude Cowork desktop), **Amazon Quick desktop**.

## Build

```bash
node build.js              # all targets → dist/<target>/
node build.js kiro         # a single target
```

Each bundle is the shared **core** (`skills/` + `aidlc-common/` + `aidlc-discovery-rules/`) plus that
platform's **adapter** (entry point + hook).

---

## Kiro (IDE & CLI)

Kiro IDE and Kiro CLI share the same `.kiro/` directory.

| Piece | Location | Role |
|---|---|---|
| Skills (5) | `.kiro/skills/` | core skills, loaded by Kiro |
| Core | `.kiro/aidlc-common/` + `.kiro/aidlc-discovery-rules/` | protocol, conventions, question banks |
| Agent | `.kiro/agents/aidlc-discovery-agent.json` | entry point — starts the orchestrator |
| Hook | `.kiro/hooks/aidlc-discovery-join-check.kiro.hook` | join-barrier reminder (runs `process-checker`) |

**Install:**
```bash
node build.js kiro
mkdir -p <your-project>/.kiro
cp -R dist/kiro/.kiro/* <your-project>/.kiro/
```
**Invoke:** `start aidlc-discovery` (verify with `/context show` in Kiro CLI).

---

## Claude Code (and Claude Cowork desktop)

Claude Code reads `.claude/` at the project root. Same Anthropic toolchain as Cowork desktop.

| Piece | Location | Role |
|---|---|---|
| Skills (5) | `.claude/skills/` | core skills, auto-activated by `description` |
| Core | `.claude/aidlc-common/` + `.claude/aidlc-discovery-rules/` | protocol, conventions, question banks |
| Slash command | `.claude/commands/aidlc-discovery.md` | explicit entry point `/aidlc-discovery` |
| Hook | `.claude/settings.json` | join-barrier `process-checker` (PostToolUse) |

**Install:**
```bash
node build.js claude
mkdir -p <your-project>/.claude
cp -R dist/claude/.claude/* <your-project>/.claude/
```
**Invoke:** `/aidlc-discovery` — or say `start aidlc-discovery` to auto-activate the skill.

---

## Amazon Quick desktop

Quick installs each skill as an **isolated, self-contained folder** under your user profile.

| Piece | Location | Role |
|---|---|---|
| Skill | `~/.quickwork/profiles/federate-prod/skills/aidlc-discovery/SKILL.md` | the Quick skill (conversational transport) |
| Core (bundled inside) | `…/aidlc-discovery/aidlc-common/` + `skills/` + `aidlc-discovery-rules/` | core packaged inside the skill folder (Quick does not load siblings) |

**Install (copy):**
```bash
node build.js amazon-quick
mkdir -p ~/.quickwork/profiles/federate-prod/skills
cp -R dist/amazon-quick/skills/aidlc-discovery ~/.quickwork/profiles/federate-prod/skills/
```
**Install (UI):** Settings → Capabilities → Skills → **Import** → select `…/aidlc-discovery/SKILL.md` (or **Upload** a zip of the folder).
**Invoke:** `start aidlc-discovery`. Requires the Amazon Quick **desktop** app and sign-in.

---

## Output (all platforms)

A `Product-Definition/` folder in your project: `vision-document.md`, `technical-environment.md`,
`open-questions.md`, optional `visual/`. See [how-to-use.md](how-to-use.md) for the walkthrough and
[README.md](README.md) for the architecture.
