from typing import Optional
from pydantic import BaseModel

class UsersBaseModel(BaseModel):
    id: Optional[int] = None
    seller_id: Optional[int] = None
    created_at: Optional[str]
    updated_at: Optional[str]
    page_number: int = 1
    page_size: int = 10

    class Config:
        from_attributes = True