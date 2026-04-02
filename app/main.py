from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from services.base_services import get_users, get_user, create_user, modify_user
from typing import List
import pdb

app = FastAPI()

class UserInfo(BaseModel): 
    id: int
    name: str

@app.get("/")
def root():
    return {"message": "hellooo"}

@app.get("/users", response_model=List[UserInfo])
def read_users():
    users = get_users()
    return [UserInfo(id=user.id, name=user.name) for user in users]

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=user.id, name=user.name, age=user.age)

@app.post("/users", response_model=UserResponse)
def create_user_endpoint(user: UserInfo):
    db_user = create_user(name=user.name, age=user.age)
    return UserResponse(id=db_user.id, name=db_user.name, age=db_user.age)

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserInfo):
    db_user = modify_user(user_id=user_id, name=user.name, age=user.age)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=db_user.id, name=db_user.name, age=db_user.age)


# @app.get("/users")
# async def getAllUsers(session: AsyncSession = Depends(get_session)):
#     items = session.query(UserInfo.Item).all()
#     return items

