# database.py
from sqlalchemy import create_engine, select, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator

# Replace with your actual database credentials
DATABASE_URL = "postgresql+psycopg2://postgres:ThuanPhan_92@localhost:5432/wallet" 
DATABASE_URL_ASYNC = "postgresql+asyncpg://postgres:ThuanPhan_92@localhost:5432/wallet" 
# Create the SQLAlchemy engine to manage connections
engine = create_engine(DATABASE_URL, connect_args={"options": "-c statement_timeout=10000"})

session = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)
#  use scoped_session to provide a unique session for each thread or request
db_session = scoped_session(session)

engine_async = create_async_engine(
    DATABASE_URL_ASYNC, echo=True
)
from sqlalchemy.ext.asyncio import AsyncSession

async_session = async_sessionmaker(engine_async, expire_on_commit=False, class_=AsyncSession)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
# def test_connection():
#     try:
#         with db_session() as connection:
#             # Check if connection is successful by executing a dummy query
#             result = connection.execute(text("SELECT * FROM users"))
#             for row in result.fetchall():
#                 print(row)
#             print("Connection successful!")
#     except Exception as ex:
#         print(f"Connection failed: {ex}")
