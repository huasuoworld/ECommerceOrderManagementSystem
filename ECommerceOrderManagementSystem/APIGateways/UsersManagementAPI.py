from fastapi import Query

from .APIGatewayDefine import app
from ..Models.FrontEndReponseModel import PageDataReponseModel, ErrorResponseException, SuccessResponseModel
from ..Models.UserProfileModel import UserProfileModel
from ..Services.PermissionValidationService import PermissionValidationService
from ..Services.UserManagementService import UserManagementService
from ..CommonUtils.ConstantUtil import UserStatusActive, UserStatusInactive, CouldNotFindUserErrorMessage, CouldNotFindUserErrorCode

userManagementService = UserManagementService()
permissionValidationService = PermissionValidationService()

@app.get("/management/users/listUsers", response_model=PageDataReponseModel[UserProfileModel])
async def listUsers(page_number: int = Query(default=1, ge=1), page_size: int = Query(default=10, ge=1, le=100)):
    try:
        userProfile = UserProfileModel.model_construct(page_number=page_number, page_size=page_size)
        return userManagementService.listUsers(userProfile)
    except ValueError as error:
        raise ErrorResponseException(status=400, message=str(error)) from error

@app.patch("/management/users/active")
async def activeUser(userId: str):
    try:
        userProfile = UserProfileModel.model_construct(id = userId, user_status = UserStatusActive)
        user = userManagementService.updateUser(userProfile)
        if user == None:
            raise ErrorResponseException(status = CouldNotFindUserErrorCode, message = CouldNotFindUserErrorMessage)
        return SuccessResponseModel()
    except ValueError as error:
        raise ErrorResponseException(status=400, message=str(error)) from error

@app.patch("/management/users/inactive")
async def inActiveUser(userId: str):
    try:
        userProfile = UserProfileModel.model_construct(id = userId, user_status = UserStatusInactive)
        user = userManagementService.updateUser(userProfile)
        if user == None:
            raise ErrorResponseException(status = CouldNotFindUserErrorCode, message = CouldNotFindUserErrorMessage)
        return SuccessResponseModel()
    except ValueError as error:
        raise ErrorResponseException(status=400, message=str(error)) from error