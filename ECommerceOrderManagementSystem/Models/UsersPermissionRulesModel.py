from .NewBaseModel import NewBaseModel


class UsersPermissionRulesModel(NewBaseModel):
    users_id: int
    permission_subject_path: str
    permission_resource_path: str
    permission_action: str
    permission_status: str

    class Config:
        from_attributes = True