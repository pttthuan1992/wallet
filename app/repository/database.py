# database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

DATABASE_URL_ASYNC = "postgresql+asyncpg://postgres:ThuanPhan_92@localhost:5432/wallet"


async def _init_connection(conn):
    await conn.set_type_codec(
        "numeric",
        encoder=str,
        decoder=float,
        schema="pg_catalog",
        format="text",
    )


engine_async = create_async_engine(
    DATABASE_URL_ASYNC,
    echo=True,
    connect_args={"init": _init_connection},
)

async_session = async_sessionmaker(engine_async, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
