"""
Integration tests for the Tasks API.
Run with: pytest tests/integration/test_tasks_api.py -v
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.services.task_service import _tasks


@pytest.fixture(autouse=True)
def clear_store():
    _tasks.clear()
    yield
    _tasks.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """Get valid auth headers for test requests."""
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "Demo1234!"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestTasksAPI:
    def test_create_task(self, client, auth_headers):
        resp = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Write tests",
                "description": "Cover all edge cases",
                "priority": "high",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Write tests"
        assert data["status"] == "todo"
        assert "id" in data

    def test_list_tasks_empty(self, client, auth_headers):
        resp = client.get("/api/v1/tasks/", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_task_not_found(self, client, auth_headers):
        resp = client.get("/api/v1/tasks/nonexistent", headers=auth_headers)
        assert resp.status_code == 404

    def test_update_task(self, client, auth_headers):
        create_resp = client.post(
            "/api/v1/tasks/",
            json={"title": "Original"},
            headers=auth_headers,
        )
        task_id = create_resp.json()["id"]

        update_resp = client.patch(
            f"/api/v1/tasks/{task_id}",
            json={"status": "in_progress", "title": "Updated"},
            headers=auth_headers,
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["status"] == "in_progress"
        assert update_resp.json()["title"] == "Updated"

    def test_delete_task(self, client, auth_headers):
        create_resp = client.post(
            "/api/v1/tasks/",
            json={"title": "To delete"},
            headers=auth_headers,
        )
        task_id = create_resp.json()["id"]

        del_resp = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert del_resp.status_code == 204

        get_resp = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert get_resp.status_code == 404

    def test_unauthenticated_request_rejected(self, client):
        resp = client.get("/api/v1/tasks/")
        assert resp.status_code in (
            401,
            403,
        )  # FastAPI HTTPBearer returns 403 for missing token

    def test_health_check(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"
