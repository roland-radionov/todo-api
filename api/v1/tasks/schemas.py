from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str
    description: str


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedTaskResponse(BaseModel):
    data: list[TaskResponse]
    page: int
    limit: int
    total: int


class FilterParams(BaseModel):
    page: int = Field(1, gt=0)
    limit: int = Field(10, gt=0, le=100)
    sort_by: Literal["created_at", "updated_at"] = "created_at"
    sort_order: Literal["desc", "asc"] = "desc"
    search: str | None = None
