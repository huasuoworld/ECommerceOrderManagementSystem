from sqlalchemy import create_engine, Column, Integer, String
from .SQLiteDB import Base

class UsersPermissionRulesDB(Base):
    __tablename__ = 'users_permission_rules'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    permission_subject_path = Column(String)
    permission_resource_path = Column(String)
    permission_action = Column(String)
    permission_status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)