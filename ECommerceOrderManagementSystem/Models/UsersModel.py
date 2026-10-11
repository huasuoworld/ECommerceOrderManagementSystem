from typing import Optional

from .NewBaseModel import NewBaseModel

class UsersModel(NewBaseModel):
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    seller_id: Optional[int] = None
    username: str
    password: str

    class Config:
        from_attributes = True