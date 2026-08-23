from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import get_current_user
from core.database import get_db
from core.models import User

from .crud import create_task, delete_task, get_all_tasks, get_task_by_id, update_task
from .schemas import (
    FilterParams,
    PaginatedTaskResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=PaginatedTaskResponse, status_code=status.HTTP_200_OK)
async def get_tasks_view(
    filter_query: Annotated[FilterParams, Query()],
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> PaginatedTaskResponse:
    return await get_all_tasks(
        session=session,
        user=user,
        filter_query=filter_query,
    )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_view(
    task_in: TaskCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> TaskResponse:
    task = await create_task(session=session, task_in=task_in, user=user)
    return task


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task_view(
    task_id: int,
    task_in: TaskUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> TaskResponse:
    task = await get_task_by_id(session=session, task_id=task_id, user=user)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found."
        )

    return await update_task(session=session, task_update=task_in, task=task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_view(
    task_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await delete_task(session=session, task_id=task_id, user=user)
