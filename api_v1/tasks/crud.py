from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select

from .schemas import TaskCreate, TaskUpdate

from core.models import Task


async def get_all_tasks(session: AsyncSession) -> list[Task]:
    stmt = select(Task)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def get_task_by_id(session: AsyncSession, task_id: int) -> Task:
    return await session.get(Task, task_id)


async def create_task(session: AsyncSession, task_in: TaskCreate) -> Task:
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    return task


async def update_task(session: AsyncSession, task_update: TaskUpdate, task: Task) -> Task:
    for name, value in task_update.model_dump().items():
        setattr(task, name, value)
    await session.commit()
    return task