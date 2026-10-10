from ..Models.UsersModel import UsersModel

sessionCache = {}

def setSessionCache(sessionId, user: UsersModel):
    sessionCache[sessionId] = user

def getSessionCache(sessionId):
    user = sessionCache.get(sessionId)
    return UsersModel.model_validate(user) if user is not None else None