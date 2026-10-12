from sqlalchemy import Column, String
from .SQLiteDB import getDB
from ..Models.UsersModel import UsersModel
from .NewBaseDB import NewBaseDB
from ..Models.UserProfileModel import UserProfileModel
from ..Models.FrontEndReponseModel import PageDataReponseModel

class UsersDB(NewBaseDB):
    __tablename__ = 'users'

    username = Column(String, unique=True, index=True)
    password = Column(String)
    display_name = Column(String)
    user_email = Column(String)
    user_phone = Column(String)
    user_status = Column(String)

    def queryUserByUsername(self, username: str) -> UsersModel:
        with getDB() as db:
            user =  db.query(UsersDB).filter(UsersDB.username == username).first()
        return UsersModel.model_validate(user) if user else None

    def queryUserProfileById(self, userId: int):
        with getDB() as db:
            user = db.query(UsersDB).filter(UsersDB.id == userId).first()
            if user is None:
                return None
            return UserProfileModel.model_validate(user)

    def listUsers(
        self, userProfile: UserProfileModel
    ) -> PageDataReponseModel[UserProfileModel]:
        with getDB() as db:
            total = db.query(UsersDB).count()
            offset = (userProfile.page_number - 1) * userProfile.page_size
            usersDBData = db.query(
                UsersDB.id,
                UsersDB.username,
                UsersDB.display_name,
                UsersDB.user_email,
                UsersDB.user_phone,
                UsersDB.user_status,
                UsersDB.created_at,
                UsersDB.updated_at,
            ).order_by(UsersDB.id).offset(offset).limit(userProfile.page_size).all()
            return PageDataReponseModel(
                page_number=userProfile.page_number,
                page_size=userProfile.page_size,
                total_items=total,
                total_pages=(total + userProfile.page_size - 1) // userProfile.page_size,
                items=[
                    UserProfileModel.model_validate(user._asdict())
                    for user in usersDBData
                ],
            )