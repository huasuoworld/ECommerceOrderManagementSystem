from .NewBaseModel import NewBaseModel

class UsersModel(NewBaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True