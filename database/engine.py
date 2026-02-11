from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from database.config import settings

from database.models import Base


URL = settings.get_db_url()

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=URL, echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db ():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db ():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    