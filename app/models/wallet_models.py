from pydantic import BaseModel
from sqlalchemy import Column, Integer, Numeric, ForeignKey
from models.user_models import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    balance = Column(Numeric(12, 2), nullable=False, default=0)

    class Config:
        orm_mode = True


class WalletCreate(BaseModel):
    user_id: int
    balance: float = 0.0


class WalletInfo(BaseModel):
    id: int
    user_id: int
    balance: float

    class Config:
        orm_mode = True
