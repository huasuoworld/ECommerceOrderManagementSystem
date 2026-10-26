from fastapi import Query, Depends
from .APIGatewayDefine import app, getCurrentUser
from ..Models.UsersModel import UsersModel
from ..Models.FrontEndReponseModel import ErrorResponseException
from ..Services.NotificationMessagesService import NotificationMessagesService

notificationMessagesService = NotificationMessagesService()

@app.post("/notification/getMessages")
async def getNotificationMessagesAndVerifyPermission(
    page_number: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    user: UsersModel = Depends(getCurrentUser)):
    try:
        return notificationMessagesService.getNotificationMessagesAndVerifyPermission(user.id, page_number, page_size)
    except ValueError as error:
        raise ErrorResponseException(status=400, message=str(error)) from error