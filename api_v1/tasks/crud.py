from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select

from .schemas import TaskCreate, TaskUpdate
from core.models import Task, User


async def get_all_tasks(session: AsyncSession, user: User) -> list[Task]:
    stmt = select(Task).where(Task.user_id == user.id)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def get_task_by_id(
    session: AsyncSession, task_id: int, user: User
) -> Task | None:
    stmt = select(Task).where((Task.id == task_id) & (Task.user_id == user.id))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_task(session: AsyncSession, task_in: TaskCreate, user: User) -> Task:
    task = Task(**task_in.model_dump(), user_id=user.id)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(
    session: AsyncSession, task_update: TaskUpdate, task: Task
) -> Task:
    for name, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, name, value)
    await session.commit()
    return task


async def delete_task(session: AsyncSession, task_id: int, user: User) -> None:
    task = await get_task_by_id(session=session, task_id=task_id, user=user)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found.",
        )

    await session.delete(task)
    await session.commit()
