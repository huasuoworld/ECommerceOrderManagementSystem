from sqlalchemy import Column, Integer, String, Boolean
from .SQLiteDB import Base, getDB
from ..Models.UsersModel import UsersModel

class UsersDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    display_name = Column(String)
    user_email = Column(String)
    user_phone = Column(String)
    user_status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)

    def query_user_by_username(self, username) -> UsersModel:
        with getDB() as db:
            user =  db.query(UsersDB).filter(UsersDB.username == username).first()
        return UsersModel.model_validate(user) if user else None