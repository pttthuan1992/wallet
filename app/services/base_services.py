from http.client import HTTPException
from os import name
from sqlalchemy.orm import Session
from repository.database import db_session
from models.user_models import User, UserDB, UserInfo
from typing import List, Optional, Callable
from fastapi import HTTPException

def execute_in_session(operation: Callable[[Session], any]):
    with db_session() as session:
        return operation(session)

def get_users() -> List[User]:  
    return execute_in_session(lambda session: session.query(User).all())

def get_user(user_id: int) -> Optional[User]:
    return execute_in_session(lambda session: session.query(User).filter(User.id == user_id).first())

def create_user(username: str) -> User:
    
    def operation(session):
        user = User(name=username)
        # print(f"---------Creating user: {str(user.name)} - {user.id}------------------------", flush=True)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    return execute_in_session(operation)

def modify_user(user: UserInfo) -> Optional[User]:
    def operation(session):
        user_db = session.get(User, user.id)
        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user.dict().items():
            setattr(user_db, key, value)
        # print(f"------------------------user_db {vars(user_db)}")
        session.commit()
        session.refresh(user_db)
        return user_db
    return execute_in_session(operation)

def delete_users(user_ids: List[int]) -> None:
    nonexisted_users = set()
    def operation(session):
        for uid in user_ids:
            user_db = session.query(User).filter(User.id == uid).first()
            if user_db is None:
                nonexisted_users.add(uid)
            else:
                session.delete(user_db)
        session.commit()
        if nonexisted_users:
            raise HTTPException(status_code=404, detail=f"Users with ids {nonexisted_users} not found")
    execute_in_session(operation)
