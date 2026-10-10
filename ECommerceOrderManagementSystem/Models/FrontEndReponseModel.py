from pydantic import BaseModel
from ..CommonUtils.ConstantUtil import SuccessStatusCode, ErrorStatusCode, SuccessMessage, ErrorMessage
from fastapi.responses import FileResponse
from typing import Optional, TypeVar, Generic, List
from ..Models.NewBaseModel import NewBaseModel

T = TypeVar('T')

class SuccessResponseModel(BaseModel):
    status: str = SuccessStatusCode
    message: str = SuccessMessage
    data: Optional[T] = None

class ErrorResponseModel(BaseModel):
    status: str = ErrorStatusCode
    message: str = ErrorMessage
    error_code: int = None
    details: dict = None

class FileResponseModel(FileResponse):
    def __init__(self, path: str, filename: str = None, media_type: str = None, headers: dict = None):
        super().__init__(path=path, media_type=media_type, headers=headers)
        if filename:
            self.headers["Content-Disposition"] = f"attachment; filename={filename}"

class PageDataReponseModel(BaseModel, Generic[T], NewBaseModel):
    status: str = SuccessStatusCode
    message: str = SuccessMessage
    page_number: int = 1
    page_size: int = 10
    total_items: int = 1
    total_pages: int = 1
    items: List[T] = []