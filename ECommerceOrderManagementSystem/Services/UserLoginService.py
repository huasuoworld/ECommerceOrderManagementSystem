from typing import Optional

from ..DBConnects.UsersDB import UsersDB
from ..Models.UsersModel import UsersModel
from ..CommonUtils.LoggingUtil import logger
from ..RedisCache.RedisConnect import setSessionCache
import uuid

userDB = UsersDB()

class UserLoginService(object):
    def login(self, usersModel: UsersModel) -> Optional[str]:
        user = userDB.queryUserByUsername(usersModel.username)
        logger.info("Login user lookup completed; user_found=%s", user is not None)
        if user and user.password == usersModel.password:
            sessionId = str(uuid.uuid4())
            setSessionCache(sessionId, user)
            return sessionId
        return None