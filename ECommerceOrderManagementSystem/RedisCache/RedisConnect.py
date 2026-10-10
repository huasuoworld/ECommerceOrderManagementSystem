from ..Models.UsersModel import UsersModel

sessionCache = {}

def setSessionCache(sessionId, user: UsersModel):
    sessionCache[sessionId] = user

def getSessionCache(sessionId) -> UsersModel:
    return UsersModel.model_validate(sessionCache.get(sessionId))