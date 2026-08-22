from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select, func, or_

from .schemas import TaskCreate, TaskUpdate, PaginatedTaskResponse, FilterParams
from core.models import Task, User


async def get_all_tasks(
    session: AsyncSession, user: User, filter_query: FilterParams
) -> PaginatedTaskResponse:
    page = filter_query.page
    limit = filter_query.limit
    sort_by = filter_query.sort_by
    sort_order = filter_query.sort_order
    search = filter_query.search
    offset = (page - 1) * limit

    stmt = select(Task).where(Task.user_id == user.id)
    if search:
        stmt = stmt.where(Task.title.like(f"%{search}%"))

    sort_field = getattr(Task, sort_by, Task.created_at)
    if sort_order == "desc":
        stmt = stmt.order_by(sort_field.desc()).offset(offset).limit(limit)
    else:
        stmt = stmt.order_by(sort_field).offset(offset).limit(limit)

    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()

    stmt = select(func.count(Task.id)).select_from(Task).where(Task.user_id == user.id)
    if search:
        stmt = stmt.where(Task.title.like(f"%{search}%"))
    total = await session.scalar(stmt)

    return PaginatedTaskResponse(
        data=tasks,
        page=page,
        limit=limit,
        total=total,
    )


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
