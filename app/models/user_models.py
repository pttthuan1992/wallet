from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from sqlalchemy import select, text, Column, Integer, String, Identity
from sqlmodel import SQLModel  
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    # id = Column(Integer,Identity(always=True), primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    class Config:
        orm_mode = True
class UserDB(SQLModel):
    id: int
    name: str

class UserInfo(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True