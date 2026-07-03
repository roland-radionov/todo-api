from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from .schemas import TaskResponse, TaskCreate
from .crud import get_all_tasks, create_task


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
async def get_all_tasks_view(session: AsyncSession = Depends(get_db)) -> list[TaskResponse]:
    return await get_all_tasks(session=session)


@router.post("/", response_model=TaskResponse)
async def create_task_view(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_db),
) -> TaskResponse:
    task = await create_task(session=session, task_in=task_in)
    return task