from fastapi import Body, FastAPI, Depends, HTTPException
from services.base_services import get_users, get_user, create_user, modify_user
from typing import Annotated, List
from models.user_models import User, UserInfo
import pdb
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hellooo"}

@app.get("/users", response_model=List[UserInfo])
def read_users():
    users = get_users()
    return [UserInfo(id=user.id, name=user.name) for user in users]

@app.get("/users/{user_id}", response_model=UserInfo)
def read_user(user_id: int):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
async def create_user_endpoint(username: Annotated[str, Body()] ):
    db_user = create_user(username)
    return f"User {db_user.name} created"

@app.put("/users/{user_id}", response_model=str)
def update_user(user_id: int, user: UserInfo):
    user = User(name=user.name, id=user.id)
    db_user = modify_user(user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return f"User {db_user.name} updated"


# @app.get("/users")
# async def getAllUsers(session: AsyncSession = Depends(get_session)):
#     items = session.query(UserInfo.Item).all()
#     return items

