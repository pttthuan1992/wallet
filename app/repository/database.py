# database.py
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
import pandas

# Replace with your actual database credentials
DATABASE_URL = "postgresql+psycopg2://postgres:ThuanPhan_92@localhost:5432/wallet" 

# Create the SQLAlchemy engine to manage connections
engine = create_engine(DATABASE_URL)

def test_connection():
    try:
        with engine.connect() as connection:
            # Check if connection is successful by executing a dummy query
            result = connection.execute(text("SELECT * FROM users"))
            for row in result.fetchall():
                print(row)
            print("Connection successful!")
    except Exception as ex:
        print(f"Connection failed: {ex}")


# Configure the SessionLocal factory
# SessionLocal = sessionmaker(
#     autocommit=False, 
#     autoflush=False, 
#     bind=engine
# )


# async def get_session() -> AsyncSession:
#     async with SessionLocal() as session:
#         yield session