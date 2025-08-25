from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import models, schemas, crud, database
from datetime import datetime
from contextlib import asynccontextmanager

# Logging imports
import logging
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Logging middleware class
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms"
        )
        return response


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield  # app runs here


# ✅ Create single app instance with lifespan
app = FastAPI(title="Task Management API", lifespan=lifespan)

# ✅ Add middleware AFTER app is defined
app.add_middleware(LoggingMiddleware)


# Routes
@app.post("/tasks/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_task(db, task)


@app.get("/tasks/")
async def list_tasks(
    skip: int = 0,
    limit: int = 10,
    status: str = Query(None, description="Filter by status"),
    priority: str = Query(None, description="Filter by priority"),
    start_date: datetime = Query(None, description="Filter tasks created after this date"),
    end_date: datetime = Query(None, description="Filter tasks created before this date"),
    db: AsyncSession = Depends(database.get_db)
):
    return await crud.get_tasks(
        db,
        skip=skip,
        limit=limit,
        status=status,
        priority=priority,
        start_date=start_date,
        end_date=end_date,
    )


@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def get_task(task_id: int, db: AsyncSession = Depends(database.get_db)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(database.get_db)):
    updated_task = await crud.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(database.get_db)):
    deleted_task = await crud.delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@app.get("/tasks/stats")
async def task_stats(db: AsyncSession = Depends(database.get_db)):
    return await crud.get_stats(db)


# ✅ Root route
@app.get("/")
async def root():
    return {"message": "Task Management API is running"}
