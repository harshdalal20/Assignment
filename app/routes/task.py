import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_task_crud():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 1. POST /tasks/ - Create a new task
        create_response = await ac.post("/tasks/", json={
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending",
            "priority": "high"
        })
        assert create_response.status_code == 200
        task = create_response.json()
        assert task["title"] == "Test Task"
        task_id = task["id"]

        # 2. GET /tasks/ - List all tasks
        list_response = await ac.get("/tasks/")
        assert list_response.status_code == 200
        tasks = list_response.json()
        assert any(t["id"] == task_id for t in tasks)

        # 3. GET /tasks/{task_id} - Get a specific task
        get_response = await ac.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        task_data = get_response.json()
        assert task_data["id"] == task_id
        assert task_data["title"] == "Test Task"

        # 4. PUT /tasks/{task_id} - Update a task
        update_response = await ac.put(f"/tasks/{task_id}", json={
            "title": "Updated Task",
            "status": "done"
        })
        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["title"] == "Updated Task"
        assert updated_task["status"] == "done"

        # 5. DELETE /tasks/{task_id} - Delete a task
        delete_response = await ac.delete(f"/tasks/{task_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Task deleted successfully"

        # Confirm deletion
        get_deleted_response = await ac.get(f"/tasks/{task_id}")
        assert get_deleted_response.status_code == 404

        # 6. GET /tasks/stats - Get task statistics
        stats_response = await ac.get("/tasks/stats")
        assert stats_response.status_code == 200
        stats = stats_response.json()
        assert "total" in stats
        assert "pending" in stats
        assert "done" in stats
