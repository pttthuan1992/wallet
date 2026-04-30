from fastapi import Body, FastAPI, Depends, HTTPException, status
from services.base_services import get_users, get_user, create_user, modify_user, delete_users, create_wallet, get_wallets
from typing import Annotated, List
from models.user_models import User, UserInfo
from models.wallet_models import WalletCreate, WalletInfo
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

@app.put("/users", response_model=str)
def update_user(user: UserInfo):
    db_user = modify_user(user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return f"User {db_user.name} updated"

@app.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
def delete_users_api(user_ids: List[int] = Body(...)):
    delete_users(user_ids)
    return "ok"

@app.get("/wallets", response_model=List[WalletInfo])
def read_wallets():
    wallets = get_wallets()
    return [WalletInfo(id=wallet.id, user_id=wallet.user_id, balance=wallet.balance) for wallet in wallets]

@app.post("/wallets", response_model=WalletInfo)
def create_wallet_endpoint(wallet: WalletCreate):
    db_wallet = create_wallet(wallet)
    return db_wallet
