from sqlalchemy.orm import declarative_base
from sqlalchemy import select, text, Column, Integer, String

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)