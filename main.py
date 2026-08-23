from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as api_v1_router
from core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(api_v1_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
