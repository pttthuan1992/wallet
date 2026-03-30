from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from repository.database import test_connection
import pdb
app = FastAPI()

class UserInfo(BaseModel): 
    name: str
    age: int

@app.get("/")
def root():
    test_connection()
    print(f"{1}")
    return {"message": "hellooo"}


# @app.get("/users")
# async def getAllUsers(session: AsyncSession = Depends(get_session)):
#     items = session.query(UserInfo.Item).all()
#     return items

