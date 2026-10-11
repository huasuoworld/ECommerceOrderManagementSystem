from typing import Optional

from pydantic import BaseModel


class UserProfileModel(BaseModel):
    id: int
    username: str
    display_name: Optional[str] = None
    user_email: Optional[str] = None
    user_phone: Optional[str] = None
    user_status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
