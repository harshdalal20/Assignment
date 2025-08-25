import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_task(async_client: AsyncClient):
    response = await async_client.post("/tasks/", json={"title": "Test Task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_task(async_client: AsyncClient):
    # Create task
    create_resp = await async_client.post("/tasks/", json={"title": "Another Task"})
    task_id = create_resp.json()["id"]

    # Fetch task
    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Another Task"

@pytest.mark.asyncio
async def test_update_task(async_client: AsyncClient):
    # Create task
    create_resp = await async_client.post("/tasks/", json={"title": "Old Title"})
    task_id = create_resp.json()["id"]

    # Update task
    response = await async_client.put(f"/tasks/{task_id}", json={"title": "New Title"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["id"] == task_id

@pytest.mark.asyncio
async def test_delete_task(async_client: AsyncClient):
    # Create task
    create_resp = await async_client.post("/tasks/", json={"title": "Delete Me"})
    task_id = create_resp.json()["id"]

    # Delete task
    response = await async_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

    # Verify deletion
    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_task_stats(async_client: AsyncClient):
    # Create tasks
    await async_client.post("/tasks/", json={"title": "Task 1"})
    await async_client.post("/tasks/", json={"title": "Task 2"})

    # Last 7 days as date range
    start_date = (datetime.utcnow() - timedelta(days=7)).isoformat()
    end_date = datetime.utcnow().isoformat()

    response = await async_client.get(f"/tasks/stats?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "pending" in data
    assert "done" in data
