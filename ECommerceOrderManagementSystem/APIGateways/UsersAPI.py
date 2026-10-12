from fastapi import Depends, HTTPException, Request

from ..Models.UsersModel import UsersModel
from ..Models.FrontEndReponseModel import SuccessResponseModel, ErrorResponseModel
from ..Models.UserProfileModel import UserProfileModel
from ..Services.UserLoginService import UserLoginService
from ..Services.UsersService import UsersService
from ..CommonUtils import LoggingUtil
from .APIGatewayDefine import app, getCurrentUser
from ..CommonUtils.ConstantUtil import SessionId, HttpUrl

# Initialize logger
user_login_service = UserLoginService()
users_service = UsersService()

# Define the login endpoint
@app.post("/users/login")
async def login(userModel: UsersModel):
    LoggingUtil.logger.info("Login request received")
    responseModel = user_login_service.login(userModel)
    
    if responseModel == None:
        return ErrorResponseModel()
    else:
        return SuccessResponseModel(
            session_id=responseModel[SessionId],
            http_url=responseModel.get(HttpUrl),
        )


@app.get("/users/me", response_model=UserProfileModel)
async def getCurrentUserProfile(user: UsersModel = Depends(getCurrentUser)):
    if user.id is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    userProfile = users_service.getUserProfile(user.id)
    if userProfile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return userProfile