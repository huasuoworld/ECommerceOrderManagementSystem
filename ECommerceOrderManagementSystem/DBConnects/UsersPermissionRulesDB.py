from sqlalchemy import create_engine, Column, Integer, String
from .NewBaseDB import NewBaseDB

class UsersPermissionRulesDB(NewBaseDB):
    __tablename__ = 'users_permission_rules'

    user_id = Column(Integer)
    permission_subject_path = Column(String)
    permission_resource_path = Column(String)
    permission_action = Column(String)
    permission_status = Column(String)