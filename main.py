from fastapi import FastAPI
from api_v1.tasks import tasks_router
from core.models import Base
from core.database import engine
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)

@app.get("/")
def index():
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)