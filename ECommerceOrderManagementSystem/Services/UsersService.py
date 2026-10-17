from typing import Optional

from ..DBConnects.UsersDB import UsersDB
from ..Models.UserProfileModel import UserProfileModel
from ..Models.FrontEndReponseModel import PageDataReponseModel

class UsersService:
    def __init__(self):
        self.usersDB = UsersDB()

    def getUserProfile(self, userId: int) -> Optional[UserProfileModel]:
        return self.usersDB.queryUserProfileById(userId)

    def listUsers(self, userProfile: UserProfileModel) -> PageDataReponseModel[UserProfileModel]:
        return self.usersDB.listUsers(userProfile)