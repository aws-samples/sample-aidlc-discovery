# Install aidlc-discovery (one-prompt installer)

Copy the prompt below and paste it into your AI agent (Claude Code, Kiro, Cursor, Cline, Amazon Q, Antigravity, or any agent with shell access). The agent downloads the latest release, installs it into `.aidlc/aidlc-discovery/` in your current project, and wires up the correct rules / steering file for your IDE so invocation is natural-language from then on.

**Note**: this approach requires your agent to have shell access (`curl`, `unzip`, file ops). If your agent cannot run shell commands, follow the [Manual install](#manual-install) section below.

---

## The install prompt

Paste this verbatim into your agent. You do not create any files yourself — the agent performs every step (download, extract, create the rules / steering file for your IDE, update `.gitignore`) and reports back when done.

```
Set up aidlc-discovery in this project by doing the following. Perform every
step — the user should not have to create any file manually.

1. Download the latest aidlc-discovery release:
   - Use the GitHub API to find the latest release asset URL:
     curl -sL https://api.github.com/repos/aws-samples/sample-aidlc-discovery/releases/tags/v1.0.0 \
       | grep -o '"browser_download_url": *"[^"]*\.zip"' \
       | head -1 \
       | cut -d'"' -f4
   - Download the zip from that URL to /tmp/aidlc-discovery.zip
   - Extract it: unzip -o /tmp/aidlc-discovery.zip -d /tmp/aidlc-discovery-release
   - Copy the aidlc-discovery/ folder from the extracted contents into
     .aidlc/aidlc-discovery at the project root (create .aidlc/ if it does
     not exist). The resulting layout must be:
       .aidlc/
         aidlc-discovery/
           aidlc-discovery-rules/
             aidlc-discovery-core-workflow.md
             aidlc-discovery-rule-details/...
           VERSION
           README.md
           how-to-use.md
           CHANGELOG.md
   - Clean up: rm -rf /tmp/aidlc-discovery.zip /tmp/aidlc-discovery-release

2. Create or update the appropriate rules / steering file for your IDE.
   Pick the one that matches the agent you are running in:

   - Kiro IDE or Kiro CLI    → .kiro/steering/aidlc-discovery.md
   - Amazon Q Developer      → .amazonq/rules/aidlc-discovery.md
   - Antigravity             → .agent/rules/aidlc-discovery.md
   - Cursor                  → .cursor/rules/aidlc-discovery.mdc with frontmatter:
                                 ---
                                 description: "aidlc-discovery workflow"
                                 alwaysApply: true
                                 ---
   - Cline                   → .clinerules/aidlc-discovery.md
   - Claude Code             → CLAUDE.md (append if file exists — see step 3)
   - GitHub Copilot          → .github/copilot-instructions.md (append if exists)
   - Any other agent         → AGENTS.md (append if exists)

3. File content / section to append (use this exact text):

   <!-- aidlc-discovery:begin -->
   ## aidlc-discovery

   When the user invokes aidlc-discovery by saying any of:
     - "start aidlc-discovery"
     - "inicia aidlc-discovery"
     - "prepare AI-DLC discovery"
     - "run aidlc-discovery"

   read and follow `.aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md`
   to start the role-based interview that produces the Vision Document and
   Technical Environment Document AI-DLC needs before Inception.

   Invoke the workflow in the user's current working directory. Do not run
   it automatically on chat load — only when explicitly invoked.
   <!-- aidlc-discovery:end -->

   IMPORTANT behavior:
   - If the rules file does NOT exist yet, create it with that content.
   - If the file ALREADY exists and does NOT contain the `<!-- aidlc-discovery:begin -->`
     marker, APPEND the block above to the end of the file — do not overwrite
     other content.
   - If the file already contains a `<!-- aidlc-discovery:begin -->`…`<!-- aidlc-discovery:end -->`
     block, REPLACE only the content between those markers (this is how updates
     work without touching the rest of the file).

4. Add `.aidlc/` to `.gitignore` (create it if it does not exist, append the
   line if it does). Do not re-add if the entry is already present. Skip this
   step only if I explicitly ask you to commit `.aidlc/` to the repo.

5. Confirm back to me:
   - The aidlc-discovery version installed (read from .aidlc/aidlc-discovery/VERSION)
   - The exact rules / steering file path you created or modified
   - Whether .aidlc/ is now in .gitignore
   - The natural-language phrase I can use to invoke the workflow
```

That's it. The agent will stop and confirm when done.

---

## What happens after install

From any chat in this project, you invoke aidlc-discovery in natural language:

```
start aidlc-discovery
```

or in Spanish:

```
inicia aidlc-discovery
```

The agent reads the rules file you just set up, follows it to load `.aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md`, and begins the interview. Your workflow proceeds exactly as described in [how-to-use.md](how-to-use.md).

---

## Updating aidlc-discovery

Re-run the install prompt above. The agent:

- Downloads the latest release into `.aidlc/aidlc-discovery/`, overwriting the previous version.
- Re-writes only the content between the `<!-- aidlc-discovery:begin -->` / `<!-- aidlc-discovery:end -->` markers in your rules file — your other instructions stay untouched.
- Leaves your `.gitignore` alone if the entry is already there.

To check which version is installed:

```
cat .aidlc/aidlc-discovery/VERSION
```

To pin a specific version (rollback or fix a team on one release while others move forward): replace step 1 of the prompt with `curl -sL https://api.github.com/repos/aws-samples/sample-aidlc-discovery/releases/tags/v0.1.0 | ...` using your desired tag.

---

## Experimental IDE status

| IDE | Rules file path | Status |
|---|---|---|
| Claude Code CLI | `CLAUDE.md` | ✅ Validated |
| Claude Code (alternative) | `.claude/CLAUDE.md` | ✅ Validated |
| Kiro IDE | `.kiro/steering/aidlc-discovery.md` | ⚠️ Experimental — please report back |
| Kiro CLI | `.kiro/steering/aidlc-discovery.md` | ⚠️ Experimental — please report back |
| Cursor | `.cursor/rules/aidlc-discovery.mdc` | ⚠️ Experimental |
| Cline | `.clinerules/aidlc-discovery.md` | ⚠️ Experimental |
| Amazon Q Developer | `.amazonq/rules/aidlc-discovery.md` | ⚠️ Experimental |
| GitHub Copilot | `.github/copilot-instructions.md` | ⚠️ Experimental |
| Antigravity | `.agent/rules/aidlc-discovery.md` | ⚠️ Experimental |
| Other / generic agent | `AGENTS.md` | ⚠️ Experimental — fallback for anything else |

**"Experimental"** means the install pattern matches the official AI-DLC convention for that IDE, but we have not yet validated the end-to-end invocation flow in that IDE specifically. If the `start aidlc-discovery` trigger is not recognised, use the [universal fallback](#universal-fallback) below and tell us which IDE you were on.

---

## Universal fallback

If for any reason the rules file does not get picked up (you switched IDEs, the file was moved, your agent does not load project-scoped rules), you can always invoke the workflow directly:

```
Read .aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md
and execute the workflow in the current working directory.
```

This works in any agent that can read local files. It is the original portable invocation and does not depend on any rules / steering file.

---

## Manual install

If your agent does not have shell access (for example, a web-only assistant), do this yourself:

### 1. Download and extract the release

- Go to `https://github.com/aws-samples/sample-aidlc-discovery/releases/tag/v1.0.0` and download the zip asset named `aidlc-discovery-v1.0.0.zip`.
- Alternative: clone the repo at a specific tag: `git clone --branch v1.0.0 https://github.com/aws-samples/sample-aidlc-discovery.git`.
- Extract the contents. You should see a top-level `aidlc-discovery/` directory containing `aidlc-discovery-rules/`, `README.md`, `how-to-use.md`, `CHANGELOG.md`, `VERSION`, `.source`.

### 2. Copy into your project

Copy the extracted `aidlc-discovery/` directory into `.aidlc/aidlc-discovery/` at your project root. The resulting layout must be exactly:

```
<your-project>/
└── .aidlc/
    └── aidlc-discovery/
        ├── VERSION
        ├── .source
        ├── README.md
        ├── how-to-use.md
        ├── CHANGELOG.md
        └── aidlc-discovery-rules/
            ├── aidlc-discovery-core-workflow.md
            └── aidlc-discovery-rule-details/...
```

Create the `.aidlc/` directory first if it does not exist.

### 3. Create the rules / steering file for your IDE

Pick the row from the table below that matches the agent / IDE you will use, create the file at the path shown, and paste **exactly the content block for that row** (the only row that needs a frontmatter header is Cursor — all others start directly with the `<!-- aidlc-discovery:begin -->` marker).

#### 3a. Agents that use a plain markdown file (no frontmatter)

**Applies to**: Kiro IDE, Kiro CLI, Amazon Q Developer, Cline, Claude Code, GitHub Copilot, Antigravity, any generic agent using `AGENTS.md`.

**File path** (pick the one matching your IDE from the [IDE status table](#experimental-ide-status) above):

- `.kiro/steering/aidlc-discovery.md` (Kiro)
- `.amazonq/rules/aidlc-discovery.md` (Amazon Q Developer)
- `.clinerules/aidlc-discovery.md` (Cline)
- `CLAUDE.md` (Claude Code — **append** if the file already exists, don't overwrite)
- `.github/copilot-instructions.md` (GitHub Copilot — append if exists)
- `.agent/rules/aidlc-discovery.md` (Antigravity)
- `AGENTS.md` (generic fallback — append if exists)

**Content to write** (copy everything between the triple backticks — not the backticks themselves):

```
<!-- aidlc-discovery:begin -->
## aidlc-discovery

When the user invokes aidlc-discovery by saying any of:
  - "start aidlc-discovery"
  - "inicia aidlc-discovery"
  - "prepare AI-DLC discovery"
  - "run aidlc-discovery"

read and follow `.aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md`
to start the role-based interview that produces the Vision Document and
Technical Environment Document AI-DLC needs before Inception.

Invoke the workflow in the user's current working directory. Do not run
it automatically on chat load — only when explicitly invoked.
<!-- aidlc-discovery:end -->
```

**Important if the target file already exists** (common with `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`):

- Open the file.
- **Append** the block above to the end — do not overwrite existing content.
- When updating later, find the existing `<!-- aidlc-discovery:begin -->` … `<!-- aidlc-discovery:end -->` block and replace only what's between those markers.

#### 3b. Cursor (requires frontmatter)

**File path**: `.cursor/rules/aidlc-discovery.mdc`

**Content to write** (note the `---` frontmatter at the top — this is required by Cursor, do not remove it):

```
---
description: "aidlc-discovery workflow"
alwaysApply: true
---

<!-- aidlc-discovery:begin -->
## aidlc-discovery

When the user invokes aidlc-discovery by saying any of:
  - "start aidlc-discovery"
  - "inicia aidlc-discovery"
  - "prepare AI-DLC discovery"
  - "run aidlc-discovery"

read and follow `.aidlc/aidlc-discovery/aidlc-discovery-rules/aidlc-discovery-core-workflow.md`
to start the role-based interview that produces the Vision Document and
Technical Environment Document AI-DLC needs before Inception.

Invoke the workflow in the user's current working directory. Do not run
it automatically on chat load — only when explicitly invoked.
<!-- aidlc-discovery:end -->
```

`.mdc` is Cursor's markdown-with-config format. Other IDEs will ignore this file.

### 4. Add `.aidlc/` to `.gitignore`

Open `.gitignore` at your project root (create it if it does not exist) and add this line on its own:

```
.aidlc/
```

If the line is already present, leave it. Skip this step only if you explicitly want to commit `.aidlc/` to the repository (e.g. a centrally-pinned version for a shared team environment).

### 5. Verify

- Check the version: `cat .aidlc/aidlc-discovery/VERSION` should print a semver like `0.1.0`.
- Check the rules file: open it in an editor and confirm the `<!-- aidlc-discovery:begin -->` block is there.
- Check `.gitignore`: `grep -q '^\.aidlc/$' .gitignore && echo "ignored"`.

### Manual install vs automated install produce identical results

The layout on disk, the file contents, and the trigger behaviour are the same either way.

---

## Troubleshooting

**The prompt failed at the `curl` step.**
Your agent probably does not have shell access. Use [Manual install](#manual-install).

**The rules file was overwritten and I lost other instructions.**
This should not happen with the prompt above because it appends or replaces only the marked block. If it did, restore your file from git (`git checkout -- CLAUDE.md` or similar). Report the agent and version — it's a real bug.

**The trigger phrase `start aidlc-discovery` does nothing.**
Either (a) the rules file was not created in the right location for your IDE, or (b) your IDE does not auto-load that file. Use the [universal fallback](#universal-fallback). Then check the table above to confirm the expected path, and move the file there.

**I am behind a corporate proxy / the GitHub API call fails.**
If your network requires auth to reach `api.github.com`, set `HTTPS_PROXY` before the prompt, or download the release manually and point the prompt's step 1 at a local file.

**I want to pre-load context (a repo, a Word doc, an MCP) before the interview.**
That is independent of install. See [Pre-loading context from files or MCP](README.md#pre-loading-context-from-files-or-mcp).
