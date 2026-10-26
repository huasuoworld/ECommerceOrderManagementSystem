from sqlalchemy import Column, String, Boolean
from .NewBaseDB import NewBaseDB
from .SQLiteDB import getDB
from ..Models.NotificationMessagesModel import NotificationMessagesModel
from ..CommonUtils.ConstantUtil import getCurrentTime, DBExcludeColumns
from sqlalchemy.orm import Session


class NotificationMessagesDB(NewBaseDB):
    __tablename__ = 'notification_messages'

    message_code = Column(String)
    message = Column(String)
    message_type = Column(String)
    message_status = Column(Boolean)

    #get all NotificationMessages by offset and page_size
    def getNotificationMessages(self, offset: int, page_size: int):
        with getDB() as db:
            notificationMessagesDBData = db.query(NotificationMessagesDB).offset(offset).limit(page_size).all()
        return notificationMessagesDBData

    def getNotificationMessagesCount(self) -> int:
        with getDB() as db:
            count = db.query(NotificationMessagesDB).count()
        return count

    def addNotificationMessages(self, notificationMessagesModel: NotificationMessagesModel):
        with getDB() as db:
            return self.addNotificationMessagesWithSession(db, notificationMessagesModel)

    def addNotificationMessagesWithSession(self, db: Session, notificationMessagesModel: NotificationMessagesModel):
        timestamp = getCurrentTime()
        notificationMessagesModel.message_type = "NOTIFICATION"
        notificationMessagesModel.message_status = False
        notificationMessage = notificationMessagesModel.model_dump(exclude = DBExcludeColumns)
        notificationMessagesDBData = NotificationMessagesDB(**notificationMessage)
        notificationMessagesDBData.created_at = timestamp
        notificationMessagesDBData.updated_at = timestamp
        db.add(notificationMessagesDBData)
        return notificationMessagesDBData