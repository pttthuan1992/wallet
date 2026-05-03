from http.client import HTTPException
from os import name
from sqlalchemy.orm import Session
from repository.database import db_session
from models.user_models import User, UserInfo
from models.wallet_models import Wallet, WalletCreate
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

def get_wallets() -> List[Wallet]:  
    return execute_in_session(lambda session: session.query(Wallet).all())

def create_wallet(wallet: WalletCreate) -> Wallet:
    def operation(session):
        user_db = session.get(User, wallet.user_id)
        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")

        db_wallet = Wallet(user_id=wallet.user_id, balance=wallet.balance)
        session.add(db_wallet)
        session.commit()
        session.refresh(db_wallet)
        return db_wallet
    return execute_in_session(operation)

def delete_wallets(wallet_ids: List[int]) -> None:
    nonexisted_wallets = set()
    def operation(session):
        for uid in wallet_ids:
            wallet_db = session.query(Wallet).filter(Wallet.id == uid).first()
            if wallet_db is None:
                nonexisted_wallets.add(uid)
            else:
                session.delete(wallet_db)
        session.commit()
        if nonexisted_wallets:
            raise HTTPException(status_code=404, detail=f"Wallets with ids {nonexisted_wallets} not found")
    execute_in_session(operation)