# TaskManager API 🚀
### A complete Python FastAPI demo project — showcasing every VS Code Copilot customization feature

[![CI](https://github.com/your-org/taskmanager/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/taskmanager/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)

---

## 🗺️ Project Purpose

This project is a **living demo** for VS Code Copilot customization features.
Every file has been crafted to show a specific capability:

| File/Folder | Copilot Feature | What it demonstrates |
|---|---|---|
| `.github/copilot-instructions.md` | **Custom Instructions** | Always-on coding standards for the whole project |
| `tests/tests.instructions.md` | **File Instructions** | Rules applied only to test files |
| `src/api/api.instructions.md` | **File Instructions** | Rules applied only to API router files |
| `.github/agents/*.agent.md` | **Custom Agents** | Specialized AI personas (Planner, Implementer, Security Reviewer, Documenter) |
| `.github/agents/*.agent.md` → `handoffs:` | **Agent Handoffs** | Guided workflows between agents |
| `.github/skills/*/SKILL.md` | **Agent Skills** | On-demand domain toolkits (security audit, API docs, code review) |
| `.github/prompts/*.prompt.md` | **Prompt Files** | Reusable slash commands for common tasks |
| `.github/hooks/hooks.json` | **Agent Hooks** | Lifecycle automation (block commands, auto-format, require tests) |
| `.vscode/mcp.json` | **MCP Servers** | External tool integration (local DB, GitHub, Playwright) |
| `mcp-servers/local-db/server.py` | **MCP Server** | Custom Python MCP server implementation |
| `plugin/` | **Agent Plugin** | Bundled package of agents + skills + hooks + MCP |
| `.claude/agents/` | **Claude Format** | Cross-tool compatible agent definitions |

---

## ⚡ Quickstart

```bash
# 1. Clone and setup
git clone https://github.com/your-org/taskmanager
cd taskmanager
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and set SECRET_KEY

# 3. Run the API
uvicorn src.main:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/docs

# 4. Run tests
pytest tests/ -v
```

---

## 🏗️ Project Structure

```
taskmanager/
│
├── src/                            # Application source
│   ├── main.py                     # FastAPI app, lifespan, middleware
│   ├── api/                        # Route handlers (thin layer)
│   │   ├── tasks.py                # Task CRUD endpoints
│   │   ├── users.py                # User endpoints
│   │   └── auth.py                 # Login/logout endpoints
│   ├── models/
│   │   └── schemas.py              # Pydantic models (request/response)
│   ├── services/                   # Business logic layer
│   │   ├── task_service.py
│   │   ├── user_service.py
│   │   └── auth_service.py
│   └── utils/
│       ├── auth.py                 # JWT dependency injection
│       ├── logger.py               # Logging setup
│       └── database.py             # DB lifecycle (stub)
│
├── tests/                          # Test suite
│   ├── unit/test_task_service.py   # Service unit tests
│   └── integration/test_tasks_api.py # API integration tests
│
├── docs/                           # Documentation
│   └── api-test.http               # REST Client test file
│
├── mcp-servers/                    # Custom MCP server implementations
│   └── local-db/server.py          # Python MCP server for local DB
│
├── plugin/                         # Agent Plugin bundle
│   ├── plugin.json                 # Plugin manifest
│   ├── agents/                     # Plugin-bundled agents
│   ├── skills/                     # Plugin-bundled skills
│   ├── hooks.json                  # Plugin lifecycle hooks
│   └── .mcp.json                   # Plugin MCP servers
│
├── .github/                        # VS Code Copilot customizations
│   ├── copilot-instructions.md     # 🔵 Always-on custom instructions
│   ├── agents/                     # 🟣 Custom agents
│   │   ├── planner.agent.md        #    Plan → hand off to Implementer
│   │   ├── implementer.agent.md    #    Write code + run tests
│   │   ├── security-reviewer.agent.md # Read-only security auditor
│   │   └── documenter.agent.md     #    Generate docs
│   ├── prompts/                    # 🔷 Prompt files (slash commands)
│   │   ├── new-endpoint.prompt.md  #    /new-endpoint scaffold
│   │   ├── pr-description.prompt.md #   /pr-description
│   │   └── debug-test.prompt.md    #    /debug-test
│   ├── skills/                     # 🟡 Agent skills
│   │   ├── security-audit/         #    OWASP audit + shell script
│   │   ├── api-doc-generator/      #    Generate API docs
│   │   └── code-review/            #    Structured code review
│   ├── hooks/                      # 🔴 Agent lifecycle hooks
│   │   ├── hooks.json              #    Hook configuration
│   │   └── scripts/                #    Shell scripts called by hooks
│   │       ├── block-dangerous-commands.sh
│   │       ├── auto-format.sh
│   │       ├── audit-log.sh
│   │       └── require-tests-pass.sh
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI/CD
│
├── .claude/agents/                 # Claude Code compatible agents
├── .vscode/
│   ├── mcp.json                    # 🟢 MCP server configuration
│   ├── settings.json               # Editor + Copilot settings
│   └── extensions.json             # Recommended extensions
│
└── Config files
    ├── requirements.txt / requirements-dev.txt
    ├── pytest.ini
    ├── ruff.toml
    ├── Dockerfile
    └── .env.example
```

---

## 🤖 Using the Custom Agents

Open Chat (`Ctrl+Shift+I`) and select an agent from the dropdown:

### 📋 Planner
Best for: starting new features from scratch.
```
@Planner I want to add email notifications when a task is assigned.
```
Planner researches the codebase, asks questions, presents a plan,
then offers a **"Start Implementation"** handoff button.

### 🔧 Implementer
Best for: writing code after a plan is agreed.
```
@Implementer Add a GET /api/v1/tasks/stats endpoint that returns task counts by status.
```
Implementer writes the service, router, and tests. Offers a **"Security Review"** handoff.

### 🔍 Security Reviewer
Best for: auditing before a PR or deployment.
```
@Security Reviewer Review the auth flow in src/services/auth_service.py
```
Read-only review with OWASP references. Offers a **"Fix Issues Found"** handoff to Implementer.

### 📝 Documenter
Best for: generating API docs after implementation.
```
@Documenter Generate complete API documentation for the tasks endpoints.
```

---

## 🎣 Agent Hooks in Action

Hooks fire automatically — you don't invoke them.

| Hook | When | What it does |
|------|------|-------------|
| `SessionStart` | New chat session | Injects git branch, Python version into context |
| `PreToolUse` | Before terminal commands | Blocks `rm -rf /`, `DROP TABLE`, `curl\|bash` |
| `PostToolUse` | After file edits | Auto-formats Python with ruff |
| `PostToolUse` | After any tool | Appends to `.copilot-audit.log` |
| `Stop` | Agent finishing | Runs pytest — blocks if tests fail |

---

## 🔌 MCP Servers

The `.vscode/mcp.json` configures 4 MCP servers:

```
VS Code Copilot
    │
    ├── taskmanager-local-db  →  mcp-servers/local-db/server.py
    │                            Query tasks, get stats, search, export CSV
    │
    ├── github                →  https://api.githubcopilot.com/mcp
    │                            Access repos, issues, PRs from chat
    │
    ├── playwright            →  npx @microsoft/mcp-server-playwright
    │                            Browser automation for E2E testing
    │
    └── filesystem            →  npx @modelcontextprotocol/server-filesystem
                                 Safe file operations scoped to workspace
```

**Try it in chat:**
```
Using the taskmanager-local-db MCP server, show me all high-priority tasks.
```

---

## 📁 Reusable Prompt Files (Slash Commands)

Type `/` in chat to see available commands:

| Command | What it does |
|---------|-------------|
| `/new-endpoint` | Scaffolds complete CRUD endpoint with tests |
| `/pr-description` | Generates PR description from git diff |
| `/debug-test` | Systematically debugs a failing test |

---

## 🧪 Agent Skills

Skills activate when their description matches your request:

| Skill | Trigger phrases |
|-------|----------------|
| `security-audit` | "security audit", "check vulnerabilities", "OWASP scan" |
| `api-doc-generator` | "generate docs", "document the API", "create API reference" |
| `code-review` | "review this code", "code review", "review my changes" |

---

## 📦 Plugin

The `plugin/` folder is a self-contained **Agent Plugin** that bundles:
- `@Dev Assistant` agent (quick commands)
- `quick-test-runner` skill
- Auto-format PostToolUse hook
- Plugin welcome SessionStart hook
- Local DB MCP server

**Install from source:**
```
Command Palette → Chat: Install Plugin From Source
→ Enter path to the plugin/ folder
```

---

## 🔄 Recommended Workflow

```
1. New Feature Request
   └── @Planner → research + plan + questions
       └── [Approve plan] → 🤝 Hand off to Implementer
           └── @Implementer → write code + tests
               └── [Tests green] → 🤝 Hand off to Security Reviewer
                   └── @Security Reviewer → OWASP audit
                       └── [Issues found] → 🤝 Hand off to Implementer (fix)
                           └── [Fixed] → 🤝 Hand off to Documenter
                               └── @Documenter → API docs + CHANGELOG
                                   └── /pr-description → PR ready! ✅
```

---

## 🔐 Security Notes

- JWT secret must be in `.env` (never hardcoded)
- In-memory storage is for demo only — use asyncpg + PostgreSQL in production
- Hash passwords with bcrypt before any real use
- CORS origins are locked to localhost — configure for your domain
- Run `pip-audit -r requirements.txt` regularly

---

## 📄 License

MIT — use freely for learning and demos.
