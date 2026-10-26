from .NewBaseModel import NewBaseModel
from typing import Optional

class NotificationReadLogsModel(NewBaseModel):

    message_id: Optional[int] = None
    users_id: Optional[int] = None

    class Config:
        from_attributes = True