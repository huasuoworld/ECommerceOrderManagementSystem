from sqlalchemy import create_engine, Column, Integer, String
from .NewBaseDB import NewBaseDB

class UsersSubjectsDB(NewBaseDB):
    __tablename__ = 'users_subjects'

    subject_code = Column(String)
    subject_name = Column(String)
    subject_path = Column(String)
    subject_parent_path = Column(String)