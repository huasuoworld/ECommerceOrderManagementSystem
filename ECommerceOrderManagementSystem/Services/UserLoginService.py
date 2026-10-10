from ..DBConnects.SQLiteDB import get_db
from ..DBConnects import UsersDB
from ..APIGateways.UsersAPI import UsersModel
from ..CommonUtils.LoggingUtil import logger
from ..RedisCache.RedisConnect import getSessionCache, setSessionCache
import uuid

user_db = UsersDB()

class UserLoginService(object):
    # 
    def login(usersModel: UsersModel) -> UsersModel:
        user = user_db.query_user_by_username(usersModel.username)
        logger.info("Login user lookup completed; user_found=%s", user is not None)
        if user and user.password == usersModel.password:
            sessionId = str(uuid.uuid4())
            setSessionCache(sessionId, user)
            return sessionId
        return None