from sqlalchemy import create_engine, Column, Integer, String
from .SQLiteDB import Base

class UsersSubjectsDB(Base):
    __tablename__ = 'users_subjects'

    id = Column(Integer, primary_key=True, index=True)
    subject_code = Column(String)
    subject_name = Column(String)
    subject_path = Column(String)
    subject_parent_path = Column(String)
    created_at = Column(String)
    updated_at = Column(String)