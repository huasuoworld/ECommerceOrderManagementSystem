from sqlalchemy import Column, Integer
from .NewBaseDB import NewBaseDB
from .SQLiteDB import getDB
from .NotificationMessagesDB import NotificationMessagesDB
from ..Models.NotificationMessagesModel import NotificationMessagesModel
from ..CommonUtils.ConstantUtil import getCurrentTime, DBExcludeColumns

class NotificationReadLogsDB(NewBaseDB):
    __tablename__ = 'notification_read_logs'

    message_id = Column(Integer)
    users_id = Column(Integer)

    def getMessagesByReadLogs(self, usersId: int, notificationMessage: NotificationMessagesDB):
        with getDB() as db:
            notificationReadLogsDBData = db.query(NotificationReadLogsDB).filter(NotificationReadLogsDB.users_id == usersId, NotificationReadLogsDB.message_id == notificationMessage.id).first()
        return notificationReadLogsDBData

    def addNotificationReadLogs(self, notificationMessagesModel: NotificationMessagesModel):
        with getDB() as db:
            timestamp = getCurrentTime()
            notificationMessage = notificationMessagesModel.model_dump(exclude = DBExcludeColumns)
            notificationReadLogsDBData = NotificationReadLogsDB(**notificationMessage)
            notificationReadLogsDBData.created_at = timestamp
            notificationReadLogsDBData.updated_at = timestamp
            db.add(notificationReadLogsDBData)
            db.commit()
                