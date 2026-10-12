from typing import Optional

from .NewBaseModel import NewBaseModel


class UserProfileModel(NewBaseModel):
    username: str
    display_name: Optional[str] = None
    user_email: Optional[str] = None
    user_phone: Optional[str] = None
    user_status: Optional[str] = None

    class Config:
            from_attributes = True
