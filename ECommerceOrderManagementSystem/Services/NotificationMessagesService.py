from sqlalchemy.orm import Session
from ..DBConnects.NotificationMessagesDB import NotificationMessagesDB
from ..DBConnects.NotificationReadLogsDB import NotificationReadLogsDB
from ..DBConnects.UsersPermissionRulesDB import UsersPermissionRulesDB
from ..Models.NotificationReadLogsModel import NotificationReadLogsModel
from ..Models.NotificationMessagesModel import NotificationMessagesModel
from ..Models.FrontEndReponseModel import PageDataReponseModel
from ..CommonUtils.LoggingUtil import logger
from ..CommonUtils.ConstantUtil import OrderPaidMessageCode

class NotificationMessagesService:
    def __init__(self):
        self.notificationMessagesDB = NotificationMessagesDB()
        self.notificationReadLogsDB = NotificationReadLogsDB()
        self.usersPermissionRulesDB = UsersPermissionRulesDB()

    def getNotificationMessagesAndVerifyPermission(self, usersId: int, page_number: int, page_size: int):
        usersPermissionRulesModel = self.usersPermissionRulesDB.isAdminAndSubscribed(usersId)
        logger.info(f"usersPermissionRulesModel: {usersPermissionRulesModel}")
        if usersPermissionRulesModel is None:
            return PageDataReponseModel()
        else:
            return self.getNotificationMessages(usersId, page_number, page_size)

    def getNotificationMessages(self, usersId: int, page_number: int, page_size: int) -> PageDataReponseModel:
        total = self.notificationMessagesDB.getNotificationMessagesCount()
        offset = (page_number - 1) * page_size
        notificationMessages = self.notificationMessagesDB.getNotificationMessages(offset, page_size)
        newNotificationMessages = []
        for notificationMessage in notificationMessages:
            notificationReadLog = self.notificationReadLogsDB.getMessagesByReadLogs(usersId, notificationMessage)
            notificationMessagesModel = NotificationMessagesModel.model_validate(notificationMessage)
            logger.info(f"notificationMessagesModel: {notificationMessagesModel}")
            if notificationReadLog is not None:
                notificationMessagesModel.message_status = True
            else:
                notificationReadLogsModel = NotificationReadLogsModel.model_construct(users_id = usersId, message_id = notificationMessage.id)
                self.notificationReadLogsDB.addNotificationReadLogs(notificationReadLogsModel)
                notificationMessagesModel.message_status = False
            newNotificationMessages.append(notificationMessagesModel)
        return PageDataReponseModel(
            page_number = page_number,
            page_size = page_size,
            total_items = total,
            total_pages = (total + page_size - 1) // page_size,
            items = newNotificationMessages)

    def addNotificationMessages(self, message: str):
        notificationMessagesModel = NotificationMessagesModel.model_construct(message_code = OrderPaidMessageCode,message = message)
        return self.notificationMessagesDB.addNotificationMessages(notificationMessagesModel)

    def addNotificationMessagesWithSession(self, db: Session, message: str):
            notificationMessagesModel = NotificationMessagesModel.model_construct(message_code = OrderPaidMessageCode,message = message)
            return self.notificationMessagesDB.addNotificationMessagesWithSession(db, notificationMessagesModel)