from typing import Optional

from ..DBConnects.UsersDB import UsersDB
from ..Models.UserProfileModel import UserProfileModel


class UsersService:
    def __init__(self):
        self.usersDB = UsersDB()

    def getUserProfile(self, userId: int) -> Optional[UserProfileModel]:
        userProfile = self.usersDB.queryUserProfileById(userId)
        return UserProfileModel.model_validate(userProfile) if userProfile else None
