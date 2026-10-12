from fastapi import Depends, HTTPException, Query

from .APIGatewayDefine import app, getCurrentUser
from ..Models.UsersModel import UsersModel
from ..Services.UsersService import UsersService
from ..Models.FrontEndReponseModel import PageDataReponseModel
from ..Models.UserProfileModel import UserProfileModel
from ..Services.PermissionValidationService import PermissionValidationService

usersService = UsersService()
permissionValidationService = PermissionValidationService()

@app.get(
    "/management/users/listUsers",
    response_model=PageDataReponseModel[UserProfileModel],
)
async def listUsers(
    page_number: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100)):
    userProfile = UserProfileModel.model_construct(page_number=page_number, page_size=page_size)
    return usersService.listUsers(userProfile)