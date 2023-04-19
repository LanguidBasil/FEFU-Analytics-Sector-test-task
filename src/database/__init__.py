import asyncio

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ._models import Profile, ScientometricDatabase
from ..config import AppSettings


SETTINGS = AppSettings()

url = f"postgresql+asyncpg://{SETTINGS.POSTGRES_USER}:{SETTINGS.POSTGRES_PASSWORD}" + \
      f"@{SETTINGS.POSTGRES_DB_ADDRESS}:5432/{SETTINGS.POSTGRES_DB}"
engine = create_async_engine(url)

session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        meta = MetaData()
        await conn.run_sync(meta.create_all)

asyncio.gather(asyncio.create_task(create_tables()))


__all__ = [
    "session_maker",
    "Profile",
    "ScientometricDatabase",
]
