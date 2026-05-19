# VS Code Copilot Quick Reference Guide
### For the TaskManager Demo Project

> Open this file in VS Code and keep it alongside Chat for reference.

---

## 🟦 Custom Instructions (Always Active)

**File:** `.github/copilot-instructions.md`  
**Status:** Applied automatically to every request. No action needed.

**What it enforces:**
- Python 3.11+ syntax, async/await everywhere
- Type annotations on all functions
- `snake_case` variables, `PascalCase` classes
- Logging over print(), try/except on async calls
- Security rules (no plaintext passwords, env vars for secrets)

**Try it:** Ask Copilot to write a new function — notice it follows the rules automatically.

---

## 🟦 File-Specific Instructions

| File | Applies To | Key Rules |
|------|-----------|-----------|
| `tests/tests.instructions.md` | `tests/**/*.py` | pytest classes, fixtures, assertion style |
| `src/api/api.instructions.md` | `src/api/*.py` | router patterns, HTTP status codes, thin handlers |

---

## 🟣 Custom Agents

Access via: **Chat view → Agent dropdown (top of Chat panel)**

| Agent | Select When | Key Behaviour |
|-------|------------|---------------|
| `Planner` | Starting a new feature | Read-only, asks questions, generates structured plan |
| `Implementer` | Ready to write code | Full tools, writes + tests + verifies |
| `Security Reviewer` | Before PR or deploy | Read-only, OWASP findings, no code changes |
| `Documenter` | After implementation | Writes to docs/ only |

### Agent Handoff Flow
```
Chat → @Planner → [Approve] → 🔘 "Start Implementation"
                                      ↓
                               @Implementer → [Tests pass] → 🔘 "Security Review"  
                                                                    ↓
                                                      @Security Reviewer → 🔘 "Fix Issues"
                                                                                  ↓
                                                                      @Implementer → 🔘 "Document It"
                                                                                          ↓
                                                                              @Documenter ✅
```

---

## 🟡 Agent Skills

Skills load automatically when your request matches their description.

| Skill | Trigger | Location |
|-------|---------|----------|
| `security-audit` | "run security audit", "check vulnerabilities" | `.github/skills/security-audit/` |
| `api-doc-generator` | "generate API docs", "document the endpoints" | `.github/skills/api-doc-generator/` |
| `code-review` | "review this code", "code review" | `.github/skills/code-review/` |
| `quick-test-runner` | "run tests", "what tests are failing" | `plugin/skills/quick-test-runner/` |

**Try it:**
```
Run a security audit on the authentication code.
```

---

## 🔷 Prompt Files (Slash Commands)

Type `/` in the Chat input to see these commands:

| Command | Use case | File |
|---------|----------|------|
| `/new-endpoint` | Scaffold a new CRUD resource | `.github/prompts/new-endpoint.prompt.md` |
| `/pr-description` | Generate PR description from git diff | `.github/prompts/pr-description.prompt.md` |
| `/debug-test` | Systematically debug a failing test | `.github/prompts/debug-test.prompt.md` |

**Try it:**
```
/new-endpoint  (then describe the resource: "comments on tasks")
```

---

## 🔴 Agent Hooks (Automatic)

Hooks fire without any action from you.

### What's Running
```
📁 .github/hooks/hooks.json  ←  configuration

    SessionStart  →  block-dangerous-commands.sh is NOT called here
                  →  git branch + Python version injected into context ✅

    PreToolUse    →  block-dangerous-commands.sh
                     Blocks: rm -rf /, DROP TABLE, curl|bash, push to main

    PostToolUse   →  auto-format.sh
                     Runs: ruff format + ruff check --fix on .py files ✅
                  →  audit-log.sh  
                     Appends: .copilot-audit.log ✅

    Stop          →  require-tests-pass.sh
                     Runs: pytest tests/ — blocks if tests fail ✅
```

### Check the Audit Log
```bash
cat .copilot-audit.log
```

### View Hook Output
`Output panel → GitHub Copilot Chat Hooks`

---

## 🟢 MCP Servers

**Config:** `.vscode/mcp.json`

| Server | Type | Provides |
|--------|------|---------|
| `taskmanager-local-db` | stdio (local Python) | list_tasks, get_task_stats, search_tasks, export_csv |
| `github` | HTTP (remote) | Repo, issues, PR access |
| `playwright` | stdio (npx) | Browser automation |
| `filesystem` | stdio (npx) | Safe file operations |

**Start the local DB server manually:**
```bash
python3 mcp-servers/local-db/server.py
```

**Try in Chat:**
```
Using the MCP server, show me task statistics and list all high-priority tasks.
```

---

## 📦 Agent Plugin

**Location:** `plugin/`

**Install:**
```
Ctrl+Shift+P → Chat: Install Plugin From Source → select plugin/ folder
```

**What it adds:**
- `@Dev Assistant` agent in agent picker
- `quick-test-runner` skill
- Auto-format hook
- Welcome message on session start

---

## 🔄 Complete Workflow Demo

### Scenario: Add a "Labels" feature to tasks

**Step 1 — Plan it**
```
@Planner I want to add a "labels" system to tasks — users can create custom
labels (name + color) and attach multiple labels to tasks. What's the plan?
```

**Step 2 — Approve plan, implement**
Click **"🚀 Start Implementation"** handoff button

**Step 3 — Security check**
Click **"🔍 Security Review"** handoff button

**Step 4 — Document**
Click **"📝 Document It"** handoff button

**Step 5 — PR**
```
/pr-description
```

**Total AI prompts typed by you:** 1 (the feature request)  
**Everything else:** agents, handoffs, hooks, and skills handle it 🎯

---

## 🛠️ Useful Commands

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term

# Lint + format
ruff check src/ tests/
ruff format src/ tests/

# Type check
mypy src/ --ignore-missing-imports

# Security audit
pip-audit -r requirements.txt
bandit -r src/ -ll

# Start API server
uvicorn src.main:app --reload

# Test MCP server directly
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python3 mcp-servers/local-db/server.py
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_task_stats","arguments":{}}}' | python3 mcp-servers/local-db/server.py
```
