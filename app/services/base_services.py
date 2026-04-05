from os import name

from sqlalchemy.orm import Session
from repository.database import db_session
from models.user_models import User
from typing import List, Optional, Callable

def execute_in_session(operation: Callable[[Session], any]):
    with db_session() as session:
        return operation(session)

def get_users() -> List[User]:  
    return execute_in_session(lambda session: session.query(User).all())

def get_user(user_id: int) -> Optional[User]:
    return execute_in_session(lambda session: session.query(User).filter(User.id == user_id).first())

def create_user(user: User) -> User:
    def operation(session):
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    return execute_in_session(operation)

def modify_user(user_id: int, user: User) -> Optional[User]:
    
    def operation(session):
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            if name is not None:
                user.name = name
            session.commit()
            session.refresh(user)
        return user
    return execute_in_session(operation)