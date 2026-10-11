from pydantic import BaseModel
from typing import Optional

class NewBaseModel(BaseModel):
    id: Optional[int] = None
    created_at: Optional[str] = str
    updated_at: Optional[str] = str
    page_number: int = 1
    page_size: int = 10

    class Config:
        from_attributes = True