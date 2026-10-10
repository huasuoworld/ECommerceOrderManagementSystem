from pydantic import BaseModel

class NewBaseModel(BaseModel):
    id: int
    created_at: str
    updated_at: str
    page_number: int = 1
    page_size: int = 10

    class Config:
        from_attributes = True