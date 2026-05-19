"""
Unit tests for TaskService.
Run with: pytest tests/unit/test_task_service.py -v
"""

import pytest

from src.models.schemas import TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from src.services.task_service import TaskService, _tasks


@pytest.fixture(autouse=True)
def clear_tasks():
    """Reset in-memory store before each test."""
    _tasks.clear()
    yield
    _tasks.clear()


@pytest.fixture
def service():
    return TaskService()


@pytest.fixture
def sample_task_data():
    return TaskCreate(
        title="Fix the login bug",
        description="Users can't log in with special characters in email",
        priority=TaskPriority.HIGH,
        tags=["bug", "auth"],
    )


class TestCreateTask:
    @pytest.mark.asyncio
    async def test_create_task_returns_task_response(self, service, sample_task_data):
        task = await service.create_task(sample_task_data, creator_id="user-123")
        assert task.id is not None
        assert task.title == "Fix the login bug"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.HIGH
        assert task.creator_id == "user-123"

    @pytest.mark.asyncio
    async def test_create_task_stores_in_memory(self, service, sample_task_data):
        task = await service.create_task(sample_task_data, creator_id="user-123")
        assert task.id in _tasks

    @pytest.mark.asyncio
    async def test_create_task_default_status_is_todo(self, service, sample_task_data):
        task = await service.create_task(sample_task_data, creator_id="user-123")
        assert task.status == TaskStatus.TODO


class TestGetTask:
    @pytest.mark.asyncio
    async def test_get_existing_task(self, service, sample_task_data):
        created = await service.create_task(sample_task_data, creator_id="user-123")
        retrieved = await service.get_task(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    @pytest.mark.asyncio
    async def test_get_nonexistent_task_returns_none(self, service):
        result = await service.get_task("nonexistent-id")
        assert result is None


class TestUpdateTask:
    @pytest.mark.asyncio
    async def test_update_task_title(self, service, sample_task_data):
        task = await service.create_task(sample_task_data, creator_id="user-123")
        update = TaskUpdate(title="Updated title")
        updated = await service.update_task(task.id, update)
        assert updated.title == "Updated title"
        assert updated.description == task.description  # unchanged

    @pytest.mark.asyncio
    async def test_update_task_status(self, service, sample_task_data):
        task = await service.create_task(sample_task_data, creator_id="user-123")
        update = TaskUpdate(status=TaskStatus.IN_PROGRESS)
        updated = await service.update_task(task.id, update)
        assert updated.status == TaskStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_update_nonexistent_task_returns_none(self, service):
        update = TaskUpdate(title="New title")
        result = await service.update_task("nonexistent-id", update)
        assert result is None


class TestDeleteTask:
    @pytest.mark.asyncio
    async def test_delete_existing_task(self, service, sample_task_data):
        task = await service.create_task(sample_task_data, creator_id="user-123")
        result = await service.delete_task(task.id)
        assert result is True
        assert task.id not in _tasks

    @pytest.mark.asyncio
    async def test_delete_nonexistent_task_returns_false(self, service):
        result = await service.delete_task("nonexistent-id")
        assert result is False


class TestListTasks:
    @pytest.mark.asyncio
    async def test_list_tasks_returns_all(self, service):
        for i in range(3):
            await service.create_task(
                TaskCreate(title=f"Task {i}", priority=TaskPriority.LOW),
                creator_id="user-123",
            )
        tasks = await service.list_tasks()
        assert len(tasks) == 3

    @pytest.mark.asyncio
    async def test_filter_by_status(self, service):
        t1 = await service.create_task(
            TaskCreate(title="Todo task"), creator_id="user-123"
        )
        await service.update_task(t1.id, TaskUpdate(status=TaskStatus.DONE))

        t2 = await service.create_task(
            TaskCreate(title="In progress task"), creator_id="user-123"
        )
        await service.update_task(t2.id, TaskUpdate(status=TaskStatus.IN_PROGRESS))

        done_tasks = await service.list_tasks(status=TaskStatus.DONE)
        assert len(done_tasks) == 1
        assert done_tasks[0].status == TaskStatus.DONE
