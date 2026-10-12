from ..DBConnects.UsersDB import UsersDB
from ..Models.UsersModel import UsersModel
from ..CommonUtils.LoggingUtil import logger
from ..RedisCache.RedisConnect import setSessionCache
import uuid
from ..CommonUtils.ConstantUtil import AdminPathWhiteList, SellerPathWhiteList, HttpUrl, AdminPermission, SellerPermission, UsersManagementURL, ProductsManagementURL, SessionId
from ..DBConnects.UsersPermissionRulesDB import UsersPermissionRulesDB

userDB = UsersDB()
usersPermissionRulesDB = UsersPermissionRulesDB()

class UserLoginService(object):
    def login(self, usersModel: UsersModel):
        user = userDB.queryUserByUsername(usersModel.username)
        logger.info("Login user lookup completed; user_found=%s", user is not None)
        if user and user.password == usersModel.password:
            sessionId = str(uuid.uuid4())
            setSessionCache(sessionId, user)
            responseModel = {SessionId: sessionId}
            usersPermissionRulesList = usersPermissionRulesDB.getPermissionByUserId(user.id)
            if usersPermissionRulesList is None:
                return None
            subjectPathList = [usersPermissionRules.permission_subject_path for usersPermissionRules in usersPermissionRulesList]
            if AdminPermission in subjectPathList:
                responseModel[HttpUrl] = UsersManagementURL
            elif SellerPermission in subjectPathList:
                responseModel[HttpUrl] = ProductsManagementURL
            return responseModel
        return None