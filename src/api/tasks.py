"""
Tasks API endpoints.
CRUD operations for task management.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.models.schemas import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)
from src.services.task_service import TaskService
from src.utils.auth import get_current_user

router = APIRouter()


def get_task_service() -> TaskService:
    return TaskService()


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    status: TaskStatus | None = Query(None, description="Filter by status"),
    priority: TaskPriority | None = Query(None, description="Filter by priority"),
    assignee_id: str | None = Query(None, description="Filter by assignee"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """List all tasks with optional filters."""
    return await service.list_tasks(
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        limit=limit,
        offset=offset,
    )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """Create a new task."""
    return await service.create_task(task, creator_id=current_user["id"])


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """Get a specific task by ID."""
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """Update a task (partial update)."""
    task = await service.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """Delete a task."""
    deleted = await service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("/{task_id}/assign/{user_id}", response_model=TaskResponse)
async def assign_task(
    task_id: str,
    user_id: str,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """Assign a task to a user."""
    task = await service.assign_task(task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task or user not found")
    return task
