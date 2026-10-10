from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import DeclarativeBase

class BaseDB(DeclarativeBase):
    pass

class NewBaseDB(BaseDB):
    __abstract__ = True
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    created_at = Column(String, server_default = func.now())
    updated_at = Column(String, server_default = func.now())