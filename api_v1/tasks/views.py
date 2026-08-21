from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.models import User
from .schemas import TaskResponse, TaskCreate, TaskUpdate
from .crud import get_all_tasks, get_task_by_id, create_task, update_task, delete_task
from api_v1.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
async def get_tasks_view(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> list[TaskResponse]:
    return await get_all_tasks(session=session, user=user)


@router.post("/", response_model=TaskResponse)
async def create_task_view(
    task_in: TaskCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> TaskResponse:
    task = await create_task(session=session, task_in=task_in, user=user)
    return task


@router.put("/{task_id}", response_model=TaskResponse)
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
