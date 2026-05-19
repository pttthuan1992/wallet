from fastapi import Body, FastAPI, Depends, HTTPException, status
from repository.database import get_db
from services.base_services import get_users, get_user, create_user, modify_user, delete_users, create_wallet, get_wallets, delete_wallets, transfer_funds
from typing import Annotated, List
from models.user_models import User, UserInfo
from models.wallet_models import WalletCreate, WalletInfo, TransferRequest, TransferResult
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hellooo"}

@app.get("/users", response_model=List[UserInfo])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    return [UserInfo(id=user.id, name=user.name) for user in users]

@app.get("/user/{user_id}", response_model=UserInfo)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
async def create_user_endpoint(username: Annotated[str, Body()], db: AsyncSession = Depends(get_db)):
    db_user = await create_user(db, username)
    return f"User {db_user.name} created"

@app.put("/users", response_model=str)
async def update_user(user: UserInfo, db: AsyncSession = Depends(get_db)):
    db_user = await modify_user(db, user=user)
    return f"User {db_user.name} updated"

@app.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_api(user_ids: List[int] = Body(...), db: AsyncSession = Depends(get_db)):
    await delete_users(db, user_ids)

@app.get("/wallets", response_model=List[WalletInfo])
async def read_wallets(db: AsyncSession = Depends(get_db)):
    wallets = await get_wallets(db)
    return [WalletInfo(id=wallet.id, user_id=wallet.user_id, balance=wallet.balance) for wallet in wallets]

@app.post("/wallets", response_model=WalletInfo)
async def create_wallet_endpoint(wallet: WalletCreate, db: AsyncSession = Depends(get_db)):
    return await create_wallet(db, wallet)

@app.delete("/wallets", response_model=object)
async def delete_wallets_api(wallet_ids: List[int] = Body(...), db: AsyncSession = Depends(get_db)):
    await delete_wallets(db, wallet_ids)
    return {"ok": True}

@app.post("/wallets/transfer", response_model=TransferResult)
async def transfer_wallet(transfer: TransferRequest, db: AsyncSession = Depends(get_db)):
    return await transfer_funds(db, transfer)
