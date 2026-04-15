from http.client import HTTPException
from os import name
from sqlalchemy.orm import Session
from repository.database import db_session
from models.user_models import User, UserDB, UserInfo
from typing import List, Optional, Callable

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
        # print(f"---------Creating user: {str(user.name)} - {user.id}", flush=True)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    return execute_in_session(operation)

def modify_user(user_id: int, user: UserDB) -> Optional[User]:
    
    def operation(session):
        user_db = session.get(User, user_id)
        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        # user = session.query(User).filter(User.id == user_id).first()
        user_db.sqlmodel_update(user_data)    
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    return execute_in_session(operation)

def delete_user(user_id: int) -> Optional[User]:
    
    def operation(session):
        statement = session.delete(User).where(User.id == user_id)
        result = session.execute(statement)
        session.commit()
        if result.rowcount == 0:
            raise HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
    return execute_in_session(operation)
