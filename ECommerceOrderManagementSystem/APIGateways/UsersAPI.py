from fastapi import Depends

from ..Models.UsersModel import UsersModel
from ..Models.FrontEndReponseModel import SuccessResponseModel, ErrorResponseException
from ..Models.UserProfileModel import UserProfileModel
from ..Services.UserLoginService import UserLoginService
from ..Services.UsersService import UsersService
from ..CommonUtils import LoggingUtil
from .APIGatewayDefine import app, getCurrentUser
from ..CommonUtils.ConstantUtil import SessionId, HttpUrl, DoNotHavePermissionErrorCode, DoNotHavePermissionErrorMessage, CouldNotFindUserErrorMessage

# Initialize logger
userLoginService = UserLoginService()
usersService = UsersService()

# Define the login endpoint
@app.post("/users/login")
async def login(userModel: UsersModel):
    try:
        LoggingUtil.logger.info("Login request received")
        responseModel = userLoginService.login(userModel)
        
        if responseModel == None:
            raise ErrorResponseException(status = DoNotHavePermissionErrorCode, message = DoNotHavePermissionErrorMessage)
        else:
            return SuccessResponseModel(
                session_id=responseModel[SessionId],
                http_url=responseModel.get(HttpUrl),
            )
    except ValueError as error:
        raise ErrorResponseException(status=400, message=str(error)) from error


@app.get("/users/me", response_model=UserProfileModel)
async def getCurrentUserProfile(user: UsersModel = Depends(getCurrentUser)):
    if user.id is None:
        raise ErrorResponseException(status = DoNotHavePermissionErrorCode, message = CouldNotFindUserErrorMessage)
    userProfile = usersService.getUserProfile(user.id)
    if userProfile is None:
        raise ErrorResponseException(status = DoNotHavePermissionErrorCode, message = CouldNotFindUserErrorMessage)
    return userProfile