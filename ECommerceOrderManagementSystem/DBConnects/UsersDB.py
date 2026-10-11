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

    def queryUserProfileById(self, userId: int):
        with getDB() as db:
            user = db.query(
                UsersDB.id,
                UsersDB.username,
                UsersDB.display_name,
                UsersDB.user_email,
                UsersDB.user_phone,
                UsersDB.user_status,
                UsersDB.created_at,
                UsersDB.updated_at,
            ).filter(UsersDB.id == userId).first()
            if user is None:
                return None
            return {
                "id": user.id,
                "username": user.username,
                "display_name": user.display_name,
                "user_email": user.user_email,
                "user_phone": user.user_phone,
                "user_status": user.user_status,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }