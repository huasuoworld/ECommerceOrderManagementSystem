from typing import Optional
from pydantic import BaseModel

class UsersBaseModel(BaseModel):
    id: int
    seller_id: Optional[int] = None
    created_at: str
    updated_at: str
    page_number: int = 1
    page_size: int = 10

    class Config:
        from_attributes = True