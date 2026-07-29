from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings

engine = create_async_engine(
    settings.db_url,
    echo=settings.debug,
)


AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionFactory() as session:
        yield session
