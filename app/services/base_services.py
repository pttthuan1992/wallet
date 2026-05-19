from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user_models import User, UserInfo
from models.wallet_models import Wallet, WalletCreate, TransferRequest, TransferResult
from typing import List, Optional
from fastapi import HTTPException


async def get_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(name=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def modify_user(session: AsyncSession, user: UserInfo) -> User:
    user_db = await session.get(User, user.id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(user_db, key, value)
    await session.commit()
    await session.refresh(user_db)
    return user_db


async def delete_users(session: AsyncSession, user_ids: List[int]) -> None:
    nonexisted_users = set()
    for uid in user_ids:
        user_db = await session.get(User, uid)
        if user_db is None:
            nonexisted_users.add(uid)
        else:
            await session.delete(user_db)
    await session.commit()
    if nonexisted_users:
        raise HTTPException(status_code=404, detail=f"Users with ids {nonexisted_users} not found")


async def get_wallets(session: AsyncSession) -> List[Wallet]:
    result = await session.execute(select(Wallet))
    return result.scalars().all()


async def create_wallet(session: AsyncSession, wallet: WalletCreate) -> Wallet:
    user_db = await session.get(User, wallet.user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    db_wallet = Wallet(user_id=wallet.user_id, balance=wallet.balance)
    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_wallet)
    return db_wallet


async def delete_wallets(session: AsyncSession, wallet_ids: List[int]) -> None:
    nonexisted_wallets = set()
    for wid in wallet_ids:
        wallet_db = await session.get(Wallet, wid)
        if wallet_db is None:
            nonexisted_wallets.add(wid)
        else:
            await session.delete(wallet_db)
    await session.commit()
    if nonexisted_wallets:
        raise HTTPException(status_code=404, detail=f"Wallets with ids {nonexisted_wallets} not found")


async def transfer_funds(session: AsyncSession, transfer: TransferRequest) -> TransferResult:
    if transfer.amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive")

    # Lock rows in consistent ID order to avoid deadlocks
    first_id, second_id = sorted([transfer.from_wallet_id, transfer.to_wallet_id])
    await session.execute(select(Wallet).where(Wallet.id.in_([first_id, second_id])).with_for_update())

    from_wallet = await session.get(Wallet, transfer.from_wallet_id)
    if not from_wallet:
        raise HTTPException(status_code=404, detail=f"Source wallet {transfer.from_wallet_id} not found")

    to_wallet = await session.get(Wallet, transfer.to_wallet_id)
    if not to_wallet:
        raise HTTPException(status_code=404, detail=f"Destination wallet {transfer.to_wallet_id} not found")

    if from_wallet.id == to_wallet.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same wallet")

    if float(from_wallet.balance) < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    from_wallet.balance = float(from_wallet.balance) - transfer.amount
    to_wallet.balance = float(to_wallet.balance) + transfer.amount

    await session.commit()
    await session.refresh(from_wallet)
    await session.refresh(to_wallet)
    return TransferResult(from_wallet=from_wallet, to_wallet=to_wallet)
