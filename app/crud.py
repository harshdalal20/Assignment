from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from datetime import datetime

# Create a new task
async def create_task(db: AsyncSession, task: TaskCreate):
    new_task = Task(**task.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

# Get a single task by ID
async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


# Get multiple tasks with optional filters
async def get_tasks(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    priority: str = None,
    start_date: datetime = None,
    end_date: datetime = None
):
    query = select(Task)

    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if start_date:
        query = query.where(Task.created_at >= start_date)
    if end_date:
        query = query.where(Task.created_at <= end_date)

    # Get total count for pagination metadata
    total_query = await db.execute(
        select(func.count(Task.id)).select_from(query.subquery())
    )
    total_count = total_query.scalar()

    # Apply pagination
    result = await db.execute(query.offset(skip).limit(limit))
    tasks = result.scalars().all()

    return {"total": total_count, "items": tasks}


# Update a task by ID
async def update_task(db: AsyncSession, task_id: int, task: TaskUpdate):
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    await db.commit()
    await db.refresh(db_task)
    return db_task


# Delete a task by ID
async def delete_task(db: AsyncSession, task_id: int):
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    await db.delete(db_task)
    await db.commit()
    return db_task


# Get stats of tasks (total, pending, done)
async def get_stats(db: AsyncSession):
    total = await db.execute(select(func.count(Task.id)))
    pending = await db.execute(select(func.count(Task.id)).where(Task.status == "pending"))
    done = await db.execute(select(func.count(Task.id)).where(Task.status == "done"))
    return {"total": total.scalar(), "pending": pending.scalar(), "done": done.scalar()}
