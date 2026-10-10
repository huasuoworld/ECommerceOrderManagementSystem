from sqlalchemy import Column, Integer, String, Boolean
from .SQLiteDB import getDB
from ..Models.UsersModel import UsersModel
from .NewBaseDB import NewBaseDB

class UsersDB(NewBaseDB):
    __tablename__ = 'users'

    username = Column(String, unique=True, index=True)
    password = Column(String)
    display_name = Column(String)
    user_email = Column(String)
    user_phone = Column(String)
    user_status = Column(String)

    def queryUserByUsername(self, username) -> UsersModel:
        with getDB() as db:
            user =  db.query(UsersDB).filter(UsersDB.username == username).first()
        return UsersModel.model_validate(user) if user else None