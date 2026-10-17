from ..DBConnects.UsersDB import UsersDB
from ..Models.UsersModel import UsersModel
from ..CommonUtils.LoggingUtil import logger
from ..RedisCache.RedisConnect import setSessionCache
import uuid
from ..CommonUtils.ConstantUtil import HttpUrl, SessionId, BuyerHomePageURL
from ..DBConnects.UsersPermissionRulesDB import UsersPermissionRulesDB
from ..CommonUtils.LoggingUtil import logger
from ..Services.PermissionValidationService import PermissionValidationService

userDB = UsersDB()
usersPermissionRulesDB = UsersPermissionRulesDB()
permissionValidationService = PermissionValidationService()

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
            subjectPathList = [permissionValidationService.hasPermission(None, usersPermissionRules) for usersPermissionRules in usersPermissionRulesList]
            homePage = next(iter(subjectPathList), BuyerHomePageURL)
            logger.info("homePage = %s", homePage)
            responseModel[HttpUrl] = homePage
            return responseModel
        return None