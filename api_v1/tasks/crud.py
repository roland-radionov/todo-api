from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select

from .schemas import TaskCreate

from core.models import Task


async def get_all_tasks(session: AsyncSession) -> list[Task]:
    stmt = select(Task)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def create_task(session: AsyncSession, task_in: TaskCreate) -> Task:
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    return task
