from pydantic import BaseModel
from ..CommonUtils.ConstantUtil import SuccessStatusCode, ErrorStatusCode, SuccessMessage, ErrorMessage
from fastapi.responses import FileResponse
from typing import Optional, TypeVar, Generic, List
from ..Models.NewBaseModel import NewBaseModel

T = TypeVar('T')

class SuccessResponseModel(BaseModel):
    status: int = SuccessStatusCode
    message: str = SuccessMessage
    http_url: Optional[str] = None
    session_id: Optional[str] = None
    data: Optional[T] = None

class ErrorResponseModel(BaseModel):
    status: int = ErrorStatusCode
    message: str = ErrorMessage
    error_code: int = None
    details: dict = None

class FileResponseModel(FileResponse):
    def __init__(self, path: str, filename: str = None, media_type: str = None, headers: dict = None):
        super().__init__(path=path, media_type=media_type, headers=headers)
        if filename:
            self.headers["Content-Disposition"] = f"attachment; filename={filename}"

class PageDataReponseModel(NewBaseModel, Generic[T]):
    status: int = SuccessStatusCode
    message: str = SuccessMessage
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    page_number: int = 1
    page_size: int = 10
    total_items: int = 1
    total_pages: int = 1
    items: List[T] = []