"""
Task business logic service.
Handles all task-related operations with in-memory storage for demo purposes.
"""

import logging
import uuid
from datetime import UTC, datetime

from src.models.schemas import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

logger = logging.getLogger(__name__)

# In-memory store (replace with real DB in production)
_tasks: dict[str, dict] = {}


class TaskService:
    """Service layer for task management operations."""

    async def list_tasks(
        self,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        assignee_id: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[TaskResponse]:
        """Retrieve tasks with optional filters."""
        tasks = list(_tasks.values())

        if status:
            tasks = [t for t in tasks if t["status"] == status]
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority]
        if assignee_id:
            tasks = [t for t in tasks if t.get("assignee_id") == assignee_id]

        return [TaskResponse(**t) for t in tasks[offset : offset + limit]]

    async def create_task(self, task: TaskCreate, creator_id: str) -> TaskResponse:
        """Create a new task."""
        task_id = str(uuid.uuid4())
        now = datetime.now(UTC)
        task_dict = {
            "id": task_id,
            "creator_id": creator_id,
            "created_at": now,
            "updated_at": now,
            **task.model_dump(),
        }
        _tasks[task_id] = task_dict
        logger.info("Task created: %s by user %s", task_id, creator_id)
        return TaskResponse(**task_dict)

    async def get_task(self, task_id: str) -> TaskResponse | None:
        """Retrieve a single task by ID."""
        task = _tasks.get(task_id)
        return TaskResponse(**task) if task else None

    async def update_task(self, task_id: str, update: TaskUpdate) -> TaskResponse | None:
        """Apply partial update to a task."""
        task = _tasks.get(task_id)
        if not task:
            return None

        update_data = update.model_dump(exclude_unset=True)
        task.update(update_data)
        task["updated_at"] = datetime.now(UTC)
        _tasks[task_id] = task
        logger.info("Task updated: %s", task_id)
        return TaskResponse(**task)

    async def delete_task(self, task_id: str) -> bool:
        """Delete a task. Returns True if deleted, False if not found."""
        if task_id not in _tasks:
            return False
        del _tasks[task_id]
        logger.info("Task deleted: %s", task_id)
        return True

    async def assign_task(self, task_id: str, user_id: str) -> TaskResponse | None:
        """Assign a task to a specific user."""
        task = _tasks.get(task_id)
        if not task:
            return None
        task["assignee_id"] = user_id
        task["updated_at"] = datetime.now(UTC)
        return TaskResponse(**task)
