import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_task(async_client: AsyncClient):
    response = await async_client.post("/tasks/", json={"title": "Test Task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"

@pytest.mark.asyncio
async def test_get_task(async_client: AsyncClient):
    response = await async_client.post("/tasks/", json={"title": "Another Task"})
    task = response.json()
    task_id = task["id"]

    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Another Task"

@pytest.mark.asyncio
async def test_update_task(async_client: AsyncClient):
    response = await async_client.post("/tasks/", json={"title": "Old Title"})
    task_id = response.json()["id"]

    response = await async_client.put(f"/tasks/{task_id}", json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

@pytest.mark.asyncio
async def test_delete_task(async_client: AsyncClient):
    response = await async_client.post("/tasks/", json={"title": "Delete Me"})
    task_id = response.json()["id"]

    response = await async_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

@pytest.mark.asyncio
async def test_task_stats(async_client: AsyncClient):
    response = await async_client.get("/tasks/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "pending" in data
    assert "done" in data
