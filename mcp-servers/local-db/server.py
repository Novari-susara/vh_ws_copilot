#!/usr/bin/env python3
"""
TaskManager Local MCP Server
============================
Provides tools for querying and managing the TaskManager database
directly from Copilot Chat, without going through the HTTP API.

Protocol: MCP (Model Context Protocol) over stdio
Usage: python3 mcp-servers/local-db/server.py

This server exposes these tools to Copilot:
  - list_tasks        : query tasks with filters
  - get_task_stats    : summary statistics
  - search_tasks      : full-text search across task titles/descriptions
  - export_tasks_csv  : export tasks as CSV string
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any

# ── In-memory demo data (mirrors src/services/task_service.py) ─────────────
DEMO_TASKS = [
    {
        "id": "task-001",
        "title": "Implement JWT refresh token endpoint",
        "description": "Add /api/v1/auth/refresh endpoint that validates refresh tokens",
        "status": "in_progress",
        "priority": "high",
        "creator_id": "user-alice",
        "assignee_id": "user-bob",
        "tags": ["auth", "api"],
        "created_at": "2025-01-10T09:00:00Z",
        "updated_at": "2025-01-12T14:30:00Z",
    },
    {
        "id": "task-002",
        "title": "Add pagination to list endpoints",
        "description": "All list endpoints should support cursor-based pagination",
        "status": "todo",
        "priority": "medium",
        "creator_id": "user-alice",
        "assignee_id": None,
        "tags": ["api", "performance"],
        "created_at": "2025-01-11T10:00:00Z",
        "updated_at": "2025-01-11T10:00:00Z",
    },
    {
        "id": "task-003",
        "title": "Write integration tests for auth endpoints",
        "description": "Cover login, token validation, and expired token scenarios",
        "status": "todo",
        "priority": "high",
        "creator_id": "user-bob",
        "assignee_id": "user-alice",
        "tags": ["testing", "auth"],
        "created_at": "2025-01-12T08:00:00Z",
        "updated_at": "2025-01-12T08:00:00Z",
    },
    {
        "id": "task-004",
        "title": "Set up CI/CD pipeline",
        "description": "GitHub Actions: lint → test → build → deploy on push to main",
        "status": "done",
        "priority": "critical",
        "creator_id": "user-bob",
        "assignee_id": "user-bob",
        "tags": ["devops", "ci"],
        "created_at": "2025-01-08T09:00:00Z",
        "updated_at": "2025-01-09T17:00:00Z",
    },
    {
        "id": "task-005",
        "title": "Replace in-memory storage with PostgreSQL",
        "description": "Use asyncpg + SQLAlchemy for persistent storage",
        "status": "todo",
        "priority": "critical",
        "creator_id": "user-alice",
        "assignee_id": None,
        "tags": ["database", "backend"],
        "created_at": "2025-01-13T09:00:00Z",
        "updated_at": "2025-01-13T09:00:00Z",
    },
]

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("taskmanager-mcp")


# ── MCP Tool Implementations ───────────────────────────────────────────────


def list_tasks(
    status: str | None = None,
    priority: str | None = None,
    assignee_id: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Filter and return tasks from the database."""
    tasks = DEMO_TASKS.copy()

    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    if assignee_id:
        tasks = [t for t in tasks if t.get("assignee_id") == assignee_id]

    return {
        "tasks": tasks[:limit],
        "total": len(tasks),
        "filters_applied": {
            "status": status,
            "priority": priority,
            "assignee_id": assignee_id,
        },
    }


def get_task_stats() -> dict[str, Any]:
    """Return summary statistics about tasks."""
    by_status: dict[str, int] = {}
    by_priority: dict[str, int] = {}

    for task in DEMO_TASKS:
        by_status[task["status"]] = by_status.get(task["status"], 0) + 1
        by_priority[task["priority"]] = by_priority.get(task["priority"], 0) + 1

    unassigned = sum(1 for t in DEMO_TASKS if not t.get("assignee_id"))
    overdue_count = 0  # Would check due_date vs now in real implementation

    return {
        "total_tasks": len(DEMO_TASKS),
        "by_status": by_status,
        "by_priority": by_priority,
        "unassigned_count": unassigned,
        "overdue_count": overdue_count,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def search_tasks(query: str) -> dict[str, Any]:
    """Full-text search across task titles and descriptions."""
    query_lower = query.lower()
    results = [
        t
        for t in DEMO_TASKS
        if query_lower in t["title"].lower()
        or query_lower in (t.get("description") or "").lower()
        or any(query_lower in tag.lower() for tag in t.get("tags", []))
    ]
    return {
        "query": query,
        "results": results,
        "count": len(results),
    }


def export_tasks_csv() -> dict[str, Any]:
    """Export all tasks as CSV format."""
    headers = ["id", "title", "status", "priority", "assignee_id", "tags", "created_at"]
    lines = [",".join(headers)]
    for task in DEMO_TASKS:
        row = [
            task["id"],
            f'"{task["title"]}"',
            task["status"],
            task["priority"],
            task.get("assignee_id") or "",
            "|".join(task.get("tags", [])),
            task["created_at"],
        ]
        lines.append(",".join(row))
    return {"csv": "\n".join(lines), "row_count": len(DEMO_TASKS)}


# ── MCP Protocol Handler ───────────────────────────────────────────────────

TOOLS = {
    "list_tasks": {
        "description": "List and filter tasks from the TaskManager database",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["todo", "in_progress", "done", "cancelled"],
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                },
                "assignee_id": {
                    "type": "string",
                    "description": "Filter by assignee user ID",
                },
                "limit": {"type": "integer", "default": 20, "maximum": 100},
            },
        },
    },
    "get_task_stats": {
        "description": "Get summary statistics: total tasks, breakdown by status and priority, unassigned count",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "search_tasks": {
        "description": "Search tasks by keyword in title, description, or tags",
        "inputSchema": {
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {"type": "string", "description": "Search keyword or phrase"},
            },
        },
    },
    "export_tasks_csv": {
        "description": "Export all tasks as a CSV string for analysis or download",
        "inputSchema": {"type": "object", "properties": {}},
    },
}


def handle_request(request: dict) -> dict | None:
    """Route MCP requests to the appropriate handler.

    Returns None for notifications (no 'id'), which must not receive a response.
    """
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    # JSON-RPC notifications have no 'id' — must not send a response
    if req_id is None:
        logger.debug("Received notification: %s (ignored)", method)
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "taskmanager-local-db", "version": "1.0.0"},
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [{"name": name, **schema} for name, schema in TOOLS.items()]
            },
        }

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        handlers = {
            "list_tasks": lambda: list_tasks(**arguments),
            "get_task_stats": lambda: get_task_stats(),
            "search_tasks": lambda: search_tasks(**arguments),
            "export_tasks_csv": lambda: export_tasks_csv(),
        }

        handler = handlers.get(tool_name)
        if not handler:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool not found: {tool_name}"},
            }

        try:
            result = handler()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                },
            }
        except Exception as e:
            logger.error("Tool error: %s", e, exc_info=True)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": str(e)},
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> None:
    """Main stdio loop for MCP protocol communication."""
    logger.info("TaskManager MCP Server started (stdio mode)")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            if response is not None:
                print(json.dumps(response), flush=True)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON: %s", e)
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    main()
