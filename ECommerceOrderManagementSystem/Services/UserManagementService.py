from typing import Optional
from DBConnects.UsersDB import UsersDB
from DBConnects.UsersPermissionRulesDB import UsersPermissionRulesDB
from ..Models.UserProfileModel import UserProfileModel
from ..Models.FrontEndReponseModel import PageDataReponseModel, SuccessResponseModel
from ..Models.UsersPermissionRulesModel import UsersPermissionRulesModel
from ..CommonUtils.ConstantUtil import PermissionStatusActive, PermissionStatusInactive, UserStatusInactive, UserStatusActive

class UserManagementService:
    def __init__(self):
        self.usersDB = UsersDB()
        self.usersPermissionRulesDB = UsersPermissionRulesDB()

    def getUserProfile(self, userId: int) -> Optional[UserProfileModel]:
            return self.usersDB.queryUserProfileById(userId)
    
    def listUsers(self, userProfile: UserProfileModel) -> PageDataReponseModel[UserProfileModel]:
        return self.usersDB.listUsers(userProfile)

    def updateUser(self, userProfileModel: UserProfileModel):
        #1. update user_status
        user = self.usersDB.updateUser(userProfileModel)
        if user == None:
            return None
        #2. update permission_status
        usersPermissionRulesModel = UsersPermissionRulesModel.model_construct(users_id = userProfileModel.id)
        if userProfileModel.user_status == UserStatusActive:
            usersPermissionRulesModel.permission_status = PermissionStatusActive
        elif userProfileModel.user_status == UserStatusInactive:
            usersPermissionRulesModel.permission_status = PermissionStatusInactive
        else:
            return None
        usersPermissionRules = self.usersPermissionRulesDB.updatePermission(usersPermissionRulesModel)
        if usersPermissionRules == None:
            return None
        return SuccessResponseModel()
        