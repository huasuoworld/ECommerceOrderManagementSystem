from .NewBaseModel import NewBaseModel

class NotificationMessagesModel(NewBaseModel):

    message_code: str
    message: str
    message_type: str
    message_status: bool

    class Config:
        from_attributes = True